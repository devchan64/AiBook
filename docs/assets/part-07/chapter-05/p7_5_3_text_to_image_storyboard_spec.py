#!/usr/bin/env python3
"""Generate a two-stage storyboard without character reference images; derive guides only from an approved PNG."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import cv2
import numpy as np
import torch
from diffusers import Flux2KleinPipeline
from PIL import Image
from p7_5_image_output_naming import candidate_stem


ASSET_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ASSET_DIR.parents[3]
DEPTH_ANYTHING_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-depth-anything-v2-small"
FLUX2_KLEIN_MODEL = "black-forest-labs/FLUX.2-klein-4B"
FLUX2_KLEIN_CACHE = PROJECT_ROOT / ".tmp/p7-5-3-flux2-klein-cache"


@dataclass(frozen=True)
class FluxStoryboardDefaults:
    seed: int = 5420
    background_steps: int = 3
    character_steps: int = 3
    width: int = 768
    height: int = 1152
    guidance_scale: float = 1.0
    max_sequence_length: int = 256


DEFAULTS = FluxStoryboardDefaults()


@dataclass(frozen=True)
class CameraAngle:
    """A deliberate camera contract for one RGB storyboard candidate."""

    label_ko: str
    prompt: str


CAMERA_ANGLES: dict[str, CameraAngle] = {
    "eye-level": CameraAngle(
        "아이레벨 정면", "an eye-level frontal camera, at the dancer's torso height, with a natural horizon",
    ),
    "low-angle": CameraAngle(
        "로우 앵글", "a low-angle camera close to floor height, looking upward while keeping the full body visible",
    ),
    "extreme-low-angle": CameraAngle(
        "강화 로우 앵글", "an extreme low-angle ground-level camera, looking steeply upward; preserve a readable full-body silhouette",
    ),
    "high-angle": CameraAngle(
        "하이 앵글", "a high-angle camera looking down, with the canyon floor visibly receding behind the dancer",
    ),
    "bird-eye": CameraAngle(
        "버드아이", "a near-overhead bird's-eye camera, looking steeply down while keeping the full body readable",
    ),
    "overhead": CameraAngle(
        "수직 오버헤드", "a vertical overhead camera directly above the dancer, with the canyon floor pattern visible around the full body",
    ),
    "dutch": CameraAngle(
        "더치 앵글", "an eye-level three-quarter camera with a deliberate 20-degree Dutch tilt; keep the dancer upright relative to gravity",
    ),
    "left-profile": CameraAngle(
        "왼쪽 프로필", "a left-side profile camera perpendicular to the dancer's travel direction",
    ),
    "front-three-quarter": CameraAngle(
        "정면 3/4", "a frontal three-quarter camera, showing the dancer's face and the forward travel direction",
    ),
    "rear-three-quarter": CameraAngle(
        "후면 3/4", "a rear three-quarter camera, showing the dancer's back and the direction of travel",
    ),
    "front-on": CameraAngle(
        "정면", "a straight-on frontal camera aligned with the dancer's travel direction",
    ),
    "rear-on": CameraAngle(
        "후면", "a straight-on rear camera aligned with the dancer's travel direction",
    ),
}


@dataclass(frozen=True)
class LensProfile:
    """A 35 mm-equivalent lens prompt, separate from the camera position."""

    label_ko: str
    prompt: str


LENS_PROFILES: dict[str, LensProfile] = {
    "ultra-wide": LensProfile(
        "초광각 18 mm", "an 18 mm full-frame-equivalent ultra-wide lens, close to the dancer, with strongly expanded foreground-to-background depth",
    ),
    "wide": LensProfile(
        "광각 24 mm", "a 24 mm full-frame-equivalent wide-angle lens, with an expansive canyon and emphatic depth",
    ),
    "standard": LensProfile(
        "표준 50 mm", "a 50 mm full-frame-equivalent standard lens, with a natural field of view",
    ),
    "short-telephoto": LensProfile(
        "중망원 85 mm", "an 85 mm full-frame-equivalent short-telephoto lens, from farther back, with moderately compressed canyon depth",
    ),
    "telephoto": LensProfile(
        "망원 135 mm", "a 135 mm full-frame-equivalent telephoto lens, from far back, with visibly compressed canyon depth",
    ),
}


def character_stage_prompt(camera: CameraAngle, lens: LensProfile) -> str:
    return (
        f"Vertical RGB storyboard, {camera.prompt}, shot with {lens.prompt}: one full-body adult contemporary dancer airborne in an expressive leap above an empty neutral floor, no scenery or props. "
        "Short jaw-length bob. She turns her eyes and face toward the right side of the frame; her rightward gaze is clearly visible. "
        "Black sleeveless leotard and opaque black tights. She leaps forward through the air like a contemporary dancer running forward: one leg extends ahead in the travel direction and the other stretches straight behind. "
        "Natural anatomy, no cropped limbs."
    )

def background_stage_prompt(camera: CameraAngle, lens: LensProfile) -> str:
    return (
        "Keep the supplied dancer completely unchanged, including her pose, anatomy, silhouette, clothing, framing, and lighting. "
        f"Preserve {camera.prompt} and {lens.prompt}; do not change them while adding scenery. "
        "Replace only the empty floor with a pale sandstone-and-gravel canyon floor and tall craggy cliffs at both sides and behind. "
        "No extra people, animals, props, or text."
    )

def character_on_background_prompt(camera: CameraAngle, lens: LensProfile) -> str:
    return (
        f"Use the supplied empty canyon as fixed scenery. Add one full-body adult dancer with {camera.prompt}, shot with {lens.prompt}: short bob, gaze toward the right side of the frame, "
        "black leotard and tights, airborne in a forward-traveling contemporary-dance leap with one leg forward and one leg straight behind. No extra people, props, or text."
    )

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FLUX.2 Klein으로 캐릭터→배경 후보 스토리보드를 만들거나, 승인 PNG에서만 guide를 추출합니다."
    )
    parser.add_argument("--seed", type=int, help="재현용 시작 seed; 생략하면 FLUX 기본값")
    parser.add_argument("--runs", type=int, default=1, help="seed를 1씩 늘릴 횟수")
    parser.add_argument("--background-steps", type=int, help="배경 단계 확산 반복 수; 생략하면 3")
    parser.add_argument("--character-steps", type=int, help="캐릭터 단계 확산 반복 수; 생략하면 3")
    parser.add_argument("--steps", type=int, help="호환용: 두 단계에 같은 확산 반복 수를 적용")
    parser.add_argument("--background-from", type=Path, help="호환용: 기존 배경 PNG에 캐릭터 단계만 실행")
    parser.add_argument("--character-from", type=Path, help="1차 캐릭터 PNG를 입력으로 받아 2차 배경 단계만 실행")
    parser.add_argument("--character-only", action="store_true", help="1차 캐릭터 단계만 생성하고 2차 배경 단계는 건너뜀")
    parser.add_argument("--width", type=int, help="출력 너비; 생략하면 모델별 기본값")
    parser.add_argument("--height", type=int, help="출력 높이; 생략하면 모델별 기본값")
    parser.add_argument("--output-dir", type=Path, default=ASSET_DIR, help="후보 PNG 저장 폴더")
    parser.add_argument(
        "--camera-angle",
        choices=tuple(CAMERA_ANGLES),
        default="high-angle",
        help="영화 촬영 관점 한 가지. 기본값은 기존의 높은 시점과 가까운 high-angle입니다.",
    )
    parser.add_argument(
        "--all-camera-angles",
        action="store_true",
        help="선택한 렌즈로 12개 카메라 관점의 RGB 후보를 각각 생성합니다.",
    )
    parser.add_argument(
        "--lens",
        choices=tuple(LENS_PROFILES),
        default="standard",
        help="35 mm 환산 렌즈 프로필. 카메라 위치·방향과 별개로 적용합니다.",
    )
    parser.add_argument(
        "--all-lenses",
        action="store_true",
        help="선택한 카메라 관점으로 5개 렌즈 프로필의 RGB 후보를 각각 생성합니다.",
    )
    parser.add_argument(
        "--shot-steps",
        action="append",
        metavar="CAMERA/LENS=CHARACTER,BACKGROUND",
        help="특정 화면의 단계 수만 덮어씁니다. 예: --shot-steps extreme-low-angle/ultra-wide=5,4",
    )
    parser.add_argument("--dry-run", action="store_true", help="생성하지 않고 선택한 카메라 계약만 출력합니다.")
    parser.add_argument(
        "--derive-guides-from",
        type=Path,
        help="사람 검수로 지정한 스토리보드 PNG에서만 Canny·depth를 추출",
    )
    return parser


def require_cuda() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU를 사용할 수 없습니다. NVIDIA 드라이버와 CUDA 접근을 확인하세요.")


def save(image: Image.Image, output_dir: Path, stem: str) -> Path:
    path = output_dir / f"{stem}.png"
    image.save(path)
    return path


def derive_canny(image: Image.Image) -> Image.Image:
    grayscale = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    return Image.fromarray(cv2.Canny(grayscale, 100, 200)).convert("RGB")


def derive_depth(image: Image.Image) -> Image.Image | None:
    """Estimate relative depth; do not replace a failed estimator with a fake map."""
    try:
        from transformers import AutoImageProcessor, AutoModelForDepthEstimation

        if not DEPTH_ANYTHING_MODEL.exists():
            raise FileNotFoundError(f"Depth Anything V2 Small이 없습니다: {DEPTH_ANYTHING_MODEL}")
        processor = AutoImageProcessor.from_pretrained(
            DEPTH_ANYTHING_MODEL, local_files_only=True, use_fast=False
        )
        model = AutoModelForDepthEstimation.from_pretrained(
            DEPTH_ANYTHING_MODEL, local_files_only=True, dtype=torch.float16
        ).to("cuda").eval()
        inputs = {name: value.to("cuda") for name, value in processor(images=image, return_tensors="pt").items()}
        with torch.inference_mode():
            predicted_depth = model(**inputs).predicted_depth
        depth = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1), size=(image.height, image.width), mode="bicubic", align_corners=False
        ).squeeze().float().cpu().numpy()
        minimum, maximum = float(depth.min()), float(depth.max())
        if maximum <= minimum:
            raise RuntimeError("깊이 추정값의 범위가 0입니다.")
        normalized = ((depth - minimum) / (maximum - minimum) * 255).astype(np.uint8)
        del model
        torch.cuda.empty_cache()
        return Image.fromarray(normalized).convert("RGB")
    except Exception as error:
        print(f"[depth 생략] 실제 깊이 추정기를 사용할 수 없습니다: {error}")
        return None


def derive_and_save_guides(image_path: Path, output_dir: Path) -> list[Path]:
    image = Image.open(image_path).convert("RGB")
    stem = f"{image_path.stem}-guide"
    outputs = [save(derive_canny(image), output_dir, f"{stem}-canny")]
    depth = derive_depth(image)
    if depth is not None:
        outputs.append(save(depth, output_dir, f"{stem}-depth"))
    return outputs


def parse_shot_step_overrides(values: list[str] | None) -> dict[tuple[str, str], tuple[int, int]]:
    """Parse per-shot steps without changing the shared 3+3 comparison default."""
    overrides: dict[tuple[str, str], tuple[int, int]] = {}
    for value in values or []:
        try:
            target, raw_steps = value.split("=", maxsplit=1)
            camera_angle, lens_name = target.split("/", maxsplit=1)
            raw_character_steps, raw_background_steps = raw_steps.split(",", maxsplit=1)
            character_steps, background_steps = int(raw_character_steps), int(raw_background_steps)
        except ValueError as error:
            raise ValueError(
                "--shot-steps는 CAMERA/LENS=CHARACTER,BACKGROUND 형식이어야 합니다."
            ) from error
        if camera_angle not in CAMERA_ANGLES:
            raise ValueError(f"--shot-steps의 카메라 관점이 없습니다: {camera_angle}")
        if lens_name not in LENS_PROFILES:
            raise ValueError(f"--shot-steps의 렌즈 프로필이 없습니다: {lens_name}")
        if character_steps < 1 or background_steps < 1:
            raise ValueError("--shot-steps의 캐릭터·배경 step은 각각 1 이상이어야 합니다.")
        key = (camera_angle, lens_name)
        if key in overrides:
            raise ValueError(f"--shot-steps가 중복되었습니다: {camera_angle}/{lens_name}")
        overrides[key] = (character_steps, background_steps)
    return overrides


def main() -> None:
    args = build_parser().parse_args()
    if args.runs < 1:
        raise ValueError("--runs는 1 이상이어야 합니다.")
    if args.background_from and not args.background_from.is_file():
        raise FileNotFoundError(f"기존 배경 PNG를 찾지 못했습니다: {args.background_from}")
    if args.character_from and not args.character_from.is_file():
        raise FileNotFoundError(f"1차 캐릭터 PNG를 찾지 못했습니다: {args.character_from}")
    if sum(value is not None for value in (args.background_from, args.character_from)) > 1:
        raise ValueError("--background-from과 --character-from은 함께 사용할 수 없습니다.")
    if args.character_only and (args.background_from or args.character_from):
        raise ValueError("--character-only는 --background-from 또는 --character-from과 함께 사용할 수 없습니다.")
    selected_camera_angles = tuple(CAMERA_ANGLES) if args.all_camera_angles else (args.camera_angle,)
    selected_lenses = tuple(LENS_PROFILES) if args.all_lenses else (args.lens,)
    base_background_steps = args.background_steps if args.background_steps is not None else (args.steps if args.steps is not None else DEFAULTS.background_steps)
    base_character_steps = args.character_steps if args.character_steps is not None else (args.steps if args.steps is not None else DEFAULTS.character_steps)
    if base_background_steps < 1 or base_character_steps < 1:
        raise ValueError("--background-steps와 --character-steps는 1 이상이어야 합니다.")
    shot_step_overrides = parse_shot_step_overrides(args.shot_steps)
    if args.dry_run:
        for camera_angle, lens_name in product(selected_camera_angles, selected_lenses):
            camera = CAMERA_ANGLES[camera_angle]
            lens = LENS_PROFILES[lens_name]
            character_steps, background_steps = shot_step_overrides.get(
                (camera_angle, lens_name), (base_character_steps, base_background_steps)
            )
            print(f"{camera_angle}\t{lens_name}\t{character_steps}\t{background_steps}\t{camera.label_ko}\t{lens.label_ko}\t{camera.prompt}\t{lens.prompt}")
        return
    require_cuda()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.derive_guides_from:
        if not args.derive_guides_from.is_file():
            raise FileNotFoundError(f"승인 스토리보드를 찾지 못했습니다: {args.derive_guides_from}")
        for output in derive_and_save_guides(args.derive_guides_from, args.output_dir):
            print(f"[승인 스토리보드 guide] {output}")
        return
    if not FLUX2_KLEIN_CACHE.exists():
        raise FileNotFoundError(f"로컬 FLUX.2 Klein cache를 찾지 못했습니다: {FLUX2_KLEIN_CACHE}")
    defaults = DEFAULTS
    background_pipeline = Flux2KleinPipeline.from_pretrained(
        FLUX2_KLEIN_MODEL, torch_dtype=torch.bfloat16, cache_dir=FLUX2_KLEIN_CACHE, local_files_only=True
    )
    character_pipeline = background_pipeline
    background_pipeline.enable_sequential_cpu_offload()
    background_pipeline.set_progress_bar_config(disable=True)
    try:
        for camera_angle, lens_name in product(selected_camera_angles, selected_lenses):
            camera = CAMERA_ANGLES[camera_angle]
            lens = LENS_PROFILES[lens_name]
            for run_index in range(args.runs):
                seed = (args.seed if args.seed is not None else defaults.seed) + run_index
                character_steps, background_steps = shot_step_overrides.get(
                    (camera_angle, lens_name), (base_character_steps, base_background_steps)
                )
                width, height = args.width or defaults.width, args.height or defaults.height
                if args.character_from:
                    stage_name, total_steps = "background-only", background_steps
                elif args.background_from or args.character_only:
                    stage_name, total_steps = "character-only", character_steps
                else:
                    stage_name, total_steps = f"character-steps-{character_steps}-background-steps-{background_steps}", background_steps + character_steps
                stem = candidate_stem(
                    f"p7-5-3-flux2-klein-{camera_angle}-{lens_name}-run-{run_index + 1:02d}-{stage_name}",
                    seed=seed,
                    steps=total_steps,
                    contract={
                        "model": "flux2-klein",
                        "camera_angle": camera_angle,
                        "camera_prompt": camera.prompt,
                        "lens": lens_name,
                        "lens_prompt": lens.prompt,
                        "character_steps": character_steps,
                        "background_steps": background_steps,
                        "background_input": str(args.background_from) if args.background_from else None,
                        "character_input": str(args.character_from) if args.character_from else None,
                        "character_only": args.character_only,
                        "character_prompt": character_stage_prompt(camera, lens),
                        "background_prompt": background_stage_prompt(camera, lens),
                        "size": [width, height],
                    },
                )
                torch.cuda.reset_peak_memory_stats()
                if args.character_from:
                    stage_input = Image.open(args.character_from).convert("RGB")
                    stage_input_output = args.character_from
                    final_prompt = background_stage_prompt(camera, lens)
                    final_steps = background_steps
                elif args.background_from:
                    stage_input = Image.open(args.background_from).convert("RGB")
                    stage_input_output = args.background_from
                    final_prompt = character_on_background_prompt(camera, lens)
                    final_steps = character_steps
                else:
                    stage_input = background_pipeline(
                        prompt=character_stage_prompt(camera, lens),
                        width=width,
                        height=height,
                        num_inference_steps=character_steps,
                        guidance_scale=defaults.guidance_scale,
                        generator=torch.Generator(device="cpu").manual_seed(seed),
                        max_sequence_length=DEFAULTS.max_sequence_length,
                    ).images[0]
                    stage_input_output = save(stage_input, args.output_dir, f"{stem}-character-stage")
                    if args.character_only:
                        print(f"[{camera.label_ko}·{lens.label_ko} 1차 캐릭터 검수 후보] {stage_input_output}")
                        continue
                    final_prompt = background_stage_prompt(camera, lens)
                    final_steps = background_steps
                final_kwargs = {
                    "prompt": final_prompt,
                    "image": [stage_input],
                    "num_inference_steps": final_steps,
                    "guidance_scale": defaults.guidance_scale,
                    "generator": torch.Generator(device="cpu").manual_seed(seed + 1),
                }
                final_kwargs["width"] = width
                final_kwargs["height"] = height
                final_kwargs["max_sequence_length"] = DEFAULTS.max_sequence_length
                storyboard = character_pipeline(**final_kwargs).images[0]
                output = save(storyboard, args.output_dir, f"{stem}-storyboard")
                print(f"[{camera.label_ko}·{lens.label_ko} 1단계 입력 또는 캐릭터 후보] {stage_input_output}")
                print(f"[{camera.label_ko}·{lens.label_ko} 사람 검수 후보] {output}")
                print("[guide 보류] 승인 뒤 --derive-guides-from으로 이 PNG를 명시하세요.")
                print(f"[{camera_angle}/{lens_name} run {run_index + 1}/{args.runs} VRAM peak] {torch.cuda.max_memory_allocated() / 1024**2:.1f} MiB")
    finally:
        del background_pipeline
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate a two-stage storyboard without character reference images; derive guides only from an approved PNG."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
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


CHARACTER_STAGE_PROMPT = (
    "Vertical storyboard, wide view from a gently elevated camera: one full-body adult contemporary dancer airborne in an expressive leap above an empty neutral floor, no scenery or props. "
    "Short jaw-length bob. She turns her eyes and face toward the right side of the frame; her rightward gaze is clearly visible. "
    "Black sleeveless leotard and opaque black tights. She leaps forward through the air like a contemporary dancer running forward: one leg extends ahead in the travel direction and the other stretches straight behind. "
    "Natural anatomy, no cropped limbs."
)

BACKGROUND_STAGE_PROMPT = (
    "Keep the supplied dancer completely unchanged, including her pose, anatomy, silhouette, clothing, framing, and lighting. "
    "Replace only the empty floor with a pale sandstone-and-gravel canyon floor and tall craggy cliffs at both sides and behind. "
    "No extra people, animals, props, or text."
)

CHARACTER_ON_BACKGROUND_PROMPT = (
    "Use the supplied empty canyon as fixed scenery. Add one full-body adult dancer in a wide gently elevated view: short bob, gaze toward the right side of the frame, "
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
        for run_index in range(args.runs):
            seed = (args.seed if args.seed is not None else defaults.seed) + run_index
            background_steps = args.background_steps if args.background_steps is not None else (args.steps if args.steps is not None else defaults.background_steps)
            character_steps = args.character_steps if args.character_steps is not None else (args.steps if args.steps is not None else defaults.character_steps)
            if background_steps < 1 or character_steps < 1:
                raise ValueError("--background-steps와 --character-steps는 1 이상이어야 합니다.")
            width, height = args.width or defaults.width, args.height or defaults.height
            if args.character_from:
                stage_name, total_steps = "background-only", background_steps
            elif args.background_from or args.character_only:
                stage_name, total_steps = "character-only", character_steps
            else:
                stage_name, total_steps = f"character-steps-{character_steps}-background-steps-{background_steps}", background_steps + character_steps
            stem = candidate_stem(
                f"p7-5-3-flux2-klein-run-{run_index + 1:02d}-{stage_name}",
                seed=seed,
                steps=total_steps,
                contract={
                    "model": "flux2-klein",
                    "background_input": str(args.background_from) if args.background_from else None,
                    "character_input": str(args.character_from) if args.character_from else None,
                    "character_only": args.character_only,
                    "character_prompt": CHARACTER_STAGE_PROMPT,
                    "background_prompt": BACKGROUND_STAGE_PROMPT,
                    "size": [width, height],
                },
            )
            torch.cuda.reset_peak_memory_stats()
            if args.character_from:
                stage_input = Image.open(args.character_from).convert("RGB")
                stage_input_output = args.character_from
                final_prompt = BACKGROUND_STAGE_PROMPT
                final_steps = background_steps
            elif args.background_from:
                stage_input = Image.open(args.background_from).convert("RGB")
                stage_input_output = args.background_from
                final_prompt = CHARACTER_ON_BACKGROUND_PROMPT
                final_steps = character_steps
            else:
                stage_input = background_pipeline(
                    prompt=CHARACTER_STAGE_PROMPT,
                    width=width,
                    height=height,
                    num_inference_steps=character_steps,
                    guidance_scale=defaults.guidance_scale,
                    generator=torch.Generator(device="cpu").manual_seed(seed),
                    max_sequence_length=DEFAULTS.max_sequence_length,
                ).images[0]
                stage_input_output = save(stage_input, args.output_dir, f"{stem}-character-stage")
                if args.character_only:
                    print(f"[1차 캐릭터 검수 후보] {stage_input_output}")
                    continue
                final_prompt = BACKGROUND_STAGE_PROMPT
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
            print(f"[1단계 입력 또는 캐릭터 후보] {stage_input_output}")
            print(f"[사람 검수 후보] {output}")
            print("[guide 보류] 승인 뒤 --derive-guides-from으로 이 PNG를 명시하세요.")
            print(f"[run {run_index + 1}/{args.runs} VRAM peak] {torch.cuda.max_memory_allocated() / 1024**2:.1f} MiB")
    finally:
        del background_pipeline
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate Scene A as a fixed RGB + relative-depth storyboard pair."""

from __future__ import annotations

import argparse
import json
import secrets
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
import torch
from diffusers import Flux2KleinPipeline
from PIL import Image

from p7_5_image_output_naming import preview_callback


ASSET_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ASSET_DIR.parents[3]
DEPTH_ANYTHING_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-depth-anything-v2-small"
FLUX2_KLEIN_MODEL = "black-forest-labs/FLUX.2-klein-4B"
FLUX2_KLEIN_CACHE = PROJECT_ROOT / ".tmp/p7-5-3-flux2-klein-cache"


@dataclass(frozen=True)
class FluxStoryboardDefaults:
    steps: int = 6
    width: int = 1152
    height: int = 1152
    guidance_scale: float = 1.0
    max_sequence_length: int = 256


DEFAULTS = FluxStoryboardDefaults()
COMMON_DANCER_PROMPT = (
    "One adult dancer, full body, airborne split leap right. "
    "Exactly two arms and two legs: right arm points right; one straight leg forward, the other back. "
    "Bob haircut, black sleeveless leotard and tights, looking right. No extra person, limb, or text."
)

SCENE_A_PROMPT = (
    "Wide elevated view in a narrow pale sandstone canyon. "
    + COMMON_DANCER_PROMPT
    + " Craggy cliffs beside and behind her; visible gravel floor and clear space around her."
)

SCENE_B_PROMPT = (
    "Very wide elevated establishing shot over a vast pale sandstone plain. "
    + COMMON_DANCER_PROMPT
    + " Centered, uncropped, about 40 percent of frame height, ample space around her. "
    "Broad gravel floor, low horizon, small distant rocks. No canyon, cliff, or wall."
)

SCENE_C_PROMPT = (
    "Vertical bird's-eye view straight down over open pale sandstone gravel. "
    + COMMON_DANCER_PROMPT
    + " Centered, uncropped, about 40 percent of frame height, ground around her. "
    "Natural overhead foreshortening; small soft full-body shadow far below. No horizon, canyon, cliff, or wall."
)

SCENES = {
    "A": {
        "slug": "scene-a",
        "description": "넓고 완만하게 높은 구도의 협곡 전진 도약 장면",
        "seed": 5420,
        "prompt": SCENE_A_PROMPT,
    },
    "B": {
        "slug": "scene-b",
        "description": "넓고 완만하게 높은 구도의 열린 공간 전진 도약 장면",
        "seed": 5421,
        "prompt": SCENE_B_PROMPT,
    },
    "C": {
        "slug": "scene-c",
        "description": "넓은 열린 공간을 수직으로 내려다보는 전진 도약 장면",
        "seed": 5422,
        "prompt": SCENE_C_PROMPT,
    },
}

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FLUX.2 Klein으로 A/B/C씬의 RGB·상대 depth 후보를 만들거나 승인 PNG에서 guide를 추출합니다."
    )
    parser.add_argument("--scene", choices=tuple(SCENES), default="A", help="장면 계약; 기본값 A")
    parser.add_argument("--seed", type=int, help="재현용 시작 seed; 생략하면 A=5420, B=5421, C=5422")
    parser.add_argument("--runs", type=int, default=1, help="seed를 1씩 늘릴 후보 수")
    parser.add_argument("--steps", type=int, default=DEFAULTS.steps, help="단일 RGB 생성 반복 수; 기본값 6")
    parser.add_argument("--width", type=int, help="출력 너비; 생략하면 768")
    parser.add_argument("--height", type=int, help="출력 높이; 생략하면 1152")
    parser.add_argument("--output-dir", type=Path, default=ASSET_DIR, help="후보 저장 폴더")
    parser.add_argument(
        "--preview-every",
        type=int,
        default=0,
        help="단계별 preview 저장 간격. 기본값 0은 저장하지 않으며 1은 매 step 저장합니다.",
    )
    parser.add_argument("--preview-dir", type=Path, help="단계별 preview 저장 폴더")
    parser.add_argument("--dry-run", action="store_true", help="생성 계약과 파일명만 출력")
    parser.add_argument("--derive-guides-from", type=Path, help="승인 PNG에서만 Canny·depth 추출")
    return parser


def require_cuda() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU를 사용할 수 없습니다. NVIDIA 드라이버와 CUDA 접근을 확인하세요.")


def save(image: Image.Image, output_dir: Path, stem: str) -> Path:
    path = output_dir / f"{stem}.png"
    image.save(path)
    return path


def write_contract(path: Path, contract: dict[str, object]) -> None:
    path.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_prompt_words(prompt: str) -> int:
    """Count whitespace-delimited prompt words for a reproducible contract metric."""
    return len(prompt.split())


def candidate_stem(scene_slug: str, execution_code: str, seed: int, steps: int) -> str:
    return f"p7-5-3-{scene_slug}-{execution_code}-seed-{seed}-s{steps}"


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
        inputs = {
            name: value.to("cuda")
            for name, value in processor(images=image, return_tensors="pt").items()
        }
        with torch.inference_mode():
            predicted_depth = model(**inputs).predicted_depth
        depth = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=(image.height, image.width),
            mode="bicubic",
            align_corners=False,
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
    if args.preview_every < 0:
        raise ValueError("--preview-every는 0 이상이어야 합니다.")
    if args.steps < 1:
        raise ValueError("--steps는 1 이상이어야 합니다.")
    scene = SCENES[args.scene]
    start_seed = args.seed if args.seed is not None else int(scene["seed"])
    scene_slug = str(scene["slug"])
    prompt = str(scene["prompt"])
    execution_code = f"{secrets.randbelow(1_000_000):06d}"
    stems = [
        candidate_stem(scene_slug, execution_code, start_seed + index, args.steps)
        for index in range(args.runs)
    ]
    if args.dry_run:
        for index, stem in enumerate(stems, start=1):
            print(f"{index:02d}/{args.runs}\t{stem}-00-contract.json")
            print(f"          \t{stem}-01-storyboard-rgb.png")
            print(f"          \t{stem}-02-storyboard-depth.png")
            print(f"          \tprompt_word_count={count_prompt_words(prompt)}")
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

    width, height = args.width or DEFAULTS.width, args.height or DEFAULTS.height
    preview_root = args.preview_dir or args.output_dir / "p7-5-3-storyboard-previews"
    pipeline = Flux2KleinPipeline.from_pretrained(
        FLUX2_KLEIN_MODEL,
        torch_dtype=torch.bfloat16,
        cache_dir=FLUX2_KLEIN_CACHE,
        local_files_only=True,
    )
    pipeline.enable_sequential_cpu_offload()
    pipeline.set_progress_bar_config(disable=True)
    try:
        for run_index, stem in enumerate(stems):
            seed = start_seed + run_index
            preview_dir = preview_root / f"{execution_code}-seed-{seed}"
            contract_path = args.output_dir / f"{stem}-00-contract.json"
            contract = {
                "model": FLUX2_KLEIN_MODEL,
                "scene_id": args.scene,
                "scene_slug": scene_slug,
                "scene_description": scene["description"],
                "execution_code": execution_code,
                "candidate_index": run_index + 1,
                "total_candidates": args.runs,
                "seed": seed,
                "generation_stages": 1,
                "steps": args.steps,
                "size": [width, height],
                "guidance_scale": DEFAULTS.guidance_scale,
                "prompt": prompt,
                "prompt_word_count": count_prompt_words(prompt),
                "preview_every": args.preview_every,
                "artifacts": {
                    "contract": f"{stem}-00-contract.json",
                    "storyboard_rgb": f"{stem}-01-storyboard-rgb.png",
                    "storyboard_depth": f"{stem}-02-storyboard-depth.png",
                },
                "storyboard_outputs": [
                    f"{stem}-01-storyboard-rgb.png",
                    f"{stem}-02-storyboard-depth.png",
                ],
                "depth_type": "relative_depth",
                "depth_model": str(DEPTH_ANYTHING_MODEL),
            }
            write_contract(contract_path, contract)
            torch.cuda.reset_peak_memory_stats()
            storyboard = pipeline(
                prompt=prompt,
                width=width,
                height=height,
                num_inference_steps=args.steps,
                guidance_scale=DEFAULTS.guidance_scale,
                generator=torch.Generator(device="cpu").manual_seed(seed),
                max_sequence_length=DEFAULTS.max_sequence_length,
                callback_on_step_end=preview_callback(
                    pipeline,
                    height=height,
                    width=width,
                    every=args.preview_every,
                    directory=preview_dir,
                    prefix="storyboard",
                ),
                callback_on_step_end_tensor_inputs=["latents"],
            ).images[0]
            rgb_output = save(storyboard, args.output_dir, f"{stem}-01-storyboard-rgb")
            depth = derive_depth(storyboard)
            if depth is None:
                rgb_output.unlink(missing_ok=True)
                raise RuntimeError("RGB와 상대 depth를 한 쌍으로 만들지 못해 RGB 단독 출력을 폐기했습니다.")
            depth_output = save(depth, args.output_dir, f"{stem}-02-storyboard-depth")
            print(f"[{run_index + 1:02d}/{args.runs} RGB 검수 후보] {rgb_output}")
            print(f"[{run_index + 1:02d}/{args.runs} 상대 depth] {depth_output}")
            print(f"[생성 계약] {contract_path}")
            print(f"[프롬프트 단어 수] {contract['prompt_word_count']}")
            print("[guide 보류] 승인 뒤 --derive-guides-from으로 이 PNG를 명시하세요.")
            print(f"[VRAM peak] {torch.cuda.max_memory_allocated() / 1024**2:.1f} MiB")
    finally:
        del pipeline
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

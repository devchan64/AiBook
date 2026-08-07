#!/usr/bin/env python3
"""Generate a text-only FLUX storyboard; derive guides only from an approved PNG."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
import torch
from diffusers import Flux2KleinPipeline, StableDiffusionXLPipeline
from PIL import Image
from p7_5_image_output_naming import candidate_stem


ASSET_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ASSET_DIR.parents[3]
DEPTH_ANYTHING_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-depth-anything-v2-small"
FLUX2_KLEIN_MODEL = "black-forest-labs/FLUX.2-klein-4B"
FLUX2_KLEIN_CACHE = PROJECT_ROOT / ".tmp/p7-5-3-flux2-klein-cache"
ANIMAGINE_MODEL = Path("/home/cbsim/.cache/huggingface/hub/models--cagliostrolab--animagine-xl-4.0/snapshots/2b7c1b397761bf5bd3cc42e5b39ec99314a75a96")


@dataclass(frozen=True)
class FluxStoryboardDefaults:
    seed: int = 5420
    steps: int = 12
    width: int = 768
    height: int = 1152
    guidance_scale: float = 1.0
    max_sequence_length: int = 256


DEFAULTS = FluxStoryboardDefaults()


@dataclass(frozen=True)
class AnimagineStoryboardDefaults:
    seed: int = 5413
    steps: int = 28
    width: int = 832
    height: int = 1216
    guidance_scale: float = 5.0


ANIMAGINE_DEFAULTS = AnimagineStoryboardDefaults()

FLUX_STORYBOARD_PROMPT = (
    "One vertical storyboard panel: an adult contemporary dancer with a short jaw-length bob stands alone on a pale sandstone-and-gravel canyon floor that continues into the bases of the nearby cliffs, "
    "framed by tall craggy cliffs immediately behind and at both sides, with a narrow visible gap from her silhouette. "
    "Full-body contemporary dance balance with natural adult anatomy: one long, straight raised left leg extends high on a front diagonal, knee extended; right foot planted. "
    "Show her full body in a left-facing side profile, with her eyes looking along the canyon toward the left. Her torso gently tilts toward the right supporting leg, and both arms open outward in balance at shoulder height. "
    "She wears a black sleeveless leotard and opaque black tights."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="FLUX.2 Klein 또는 Animagine XL로 텍스트 전용 후보 스토리보드를 만들거나, 승인 PNG에서만 guide를 추출합니다."
    )
    parser.add_argument("--model", choices=("flux2-klein", "animagine-xl"), default="flux2-klein")
    parser.add_argument("--seed", type=int, help="재현용 시작 seed; 생략하면 모델별 기본값")
    parser.add_argument("--runs", type=int, default=1, help="seed를 1씩 늘릴 횟수")
    parser.add_argument("--steps", type=int, help="확산 반복 수; 생략하면 모델별 기본값")
    parser.add_argument("--width", type=int, help="출력 너비; 생략하면 모델별 기본값")
    parser.add_argument("--height", type=int, help="출력 높이; 생략하면 모델별 기본값")
    parser.add_argument("--output-dir", type=Path, default=ASSET_DIR, help="후보 PNG 저장 폴더")
    parser.add_argument(
        "--derive-guides-from",
        type=Path,
        help="사람 검수로 승인한 스토리보드 PNG에서만 lineart·Canny·depth를 추출",
    )
    return parser


def require_cuda() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU를 사용할 수 없습니다. NVIDIA 드라이버와 CUDA 접근을 확인하세요.")


def save(image: Image.Image, output_dir: Path, stem: str) -> Path:
    path = output_dir / f"{stem}.png"
    image.save(path)
    return path


def derive_lineart(image: Image.Image) -> Image.Image:
    grayscale = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    lineart = cv2.adaptiveThreshold(
        grayscale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 7
    )
    return Image.fromarray(lineart).convert("RGB")


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
    outputs = [save(derive_lineart(image), output_dir, f"{stem}-lineart")]
    outputs.append(save(derive_canny(image), output_dir, f"{stem}-canny"))
    depth = derive_depth(image)
    if depth is not None:
        outputs.append(save(depth, output_dir, f"{stem}-depth"))
    return outputs


def main() -> None:
    args = build_parser().parse_args()
    if args.runs < 1:
        raise ValueError("--runs는 1 이상이어야 합니다.")
    require_cuda()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.derive_guides_from:
        if not args.derive_guides_from.is_file():
            raise FileNotFoundError(f"승인 스토리보드를 찾지 못했습니다: {args.derive_guides_from}")
        for output in derive_and_save_guides(args.derive_guides_from, args.output_dir):
            print(f"[승인 스토리보드 guide] {output}")
        return
    if args.model == "flux2-klein":
        if not FLUX2_KLEIN_CACHE.exists():
            raise FileNotFoundError(f"로컬 FLUX.2 Klein cache를 찾지 못했습니다: {FLUX2_KLEIN_CACHE}")
        defaults = DEFAULTS
        pipeline = Flux2KleinPipeline.from_pretrained(
            FLUX2_KLEIN_MODEL, torch_dtype=torch.bfloat16, cache_dir=FLUX2_KLEIN_CACHE, local_files_only=True
        )
    else:
        if not ANIMAGINE_MODEL.is_dir():
            raise FileNotFoundError(f"로컬 Animagine XL 모델을 찾지 못했습니다: {ANIMAGINE_MODEL}")
        defaults = ANIMAGINE_DEFAULTS
        pipeline = StableDiffusionXLPipeline.from_pretrained(ANIMAGINE_MODEL, torch_dtype=torch.float16, local_files_only=True)
    pipeline.enable_sequential_cpu_offload()
    pipeline.set_progress_bar_config(disable=True)
    try:
        for run_index in range(args.runs):
            seed = (args.seed if args.seed is not None else defaults.seed) + run_index
            steps = args.steps if args.steps is not None else defaults.steps
            stem = candidate_stem(f"p7-5-3-{args.model}-run-{run_index + 1:02d}", seed=seed, steps=steps, contract={"model": args.model, "prompt": FLUX_STORYBOARD_PROMPT, "size": [args.width or defaults.width, args.height or defaults.height]})
            torch.cuda.reset_peak_memory_stats()
            storyboard = pipeline(
                prompt=FLUX_STORYBOARD_PROMPT,
                width=args.width or defaults.width,
                height=args.height or defaults.height,
                num_inference_steps=args.steps or defaults.steps,
                guidance_scale=defaults.guidance_scale,
                generator=torch.Generator(device="cpu" if args.model == "flux2-klein" else "cuda").manual_seed(seed),
                **({"max_sequence_length": DEFAULTS.max_sequence_length} if args.model == "flux2-klein" else {}),
            ).images[0]
            output = save(storyboard, args.output_dir, f"{stem}-storyboard")
            print(f"[사람 검수 후보] {output}")
            print("[guide 보류] 승인 뒤 --derive-guides-from으로 이 PNG를 명시하세요.")
            print(f"[run {run_index + 1}/{args.runs} VRAM peak] {torch.cuda.max_memory_allocated() / 1024**2:.1f} MiB")
    finally:
        del pipeline
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate a storyboard first, then derive structural guides from its pixels.

The scene prompt is intentionally fixed. The experiment rejects an output when
the storyboard is unreadable; it does not ask a diffusion model to invent a
lineart, depth, or canny guide before a storyboard exists.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import torch
from diffusers import Flux2KleinPipeline, StableDiffusionXLPipeline
from PIL import Image


ASSET_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ASSET_DIR.parents[3]
ANIMAGINE_MODEL = Path(
    "/home/cbsim/.cache/huggingface/hub/"
    "models--cagliostrolab--animagine-xl-4.0/"
    "snapshots/2b7c1b397761bf5bd3cc42e5b39ec99314a75a96"
)
DEPTH_ANYTHING_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-depth-anything-v2-small"
FLUX2_KLEIN_MODEL = "black-forest-labs/FLUX.2-klein-4B"
FLUX2_KLEIN_CACHE = PROJECT_ROOT / ".tmp/p7-5-3-flux2-klein-cache"


@dataclass(frozen=True)
class ModelDefaults:
    """One explicit input contract for each supported storyboard model."""

    steps: int
    width: int
    height: int
    guidance_scale: float
    generator_device: str


MODEL_DEFAULTS = {
    "animagine": ModelDefaults(
        steps=28,
        width=832,
        height=1216,
        guidance_scale=5.0,
        generator_device="cuda",
    ),
    "flux2-klein": ModelDefaults(
        steps=50,
        width=512,
        height=768,
        guidance_scale=1.0,
        generator_device="cpu",
    ),
}
MODEL_CHOICES = (*MODEL_DEFAULTS, "both")

# 사용자 제공 자세를 글로만 풀어 쓴 스토리보드 기준 장면입니다.
# 참조 사진 자체는 어떤 모델 입력에도 전달하지 않습니다.
STORYBOARD_PROMPT = (
    "1girl, solo, full body, contemporary dancer, standing split, exactly two arms, "
    "exactly two legs, one leg vertical, one leg planted, both feet visible, "
    "raised leg in foreground, both arms behind raised leg, arms occluded by raised leg where they cross, "
    "black sleeveless leotard, black opaque tights, one arm up, one arm out, "
    "wide shot, empty canyon ground, distant craggy cliffs, "
    "grayscale sketch, masterpiece, high score"
)
NEGATIVE_PROMPT = (
    "lowres, bad anatomy, bad hands, text, missing fingers, extra digits, cropped, "
    "low quality, watermark, blurry, extra arms, extra legs, floating, hidden feet, "
    "fused foot, ground overlap, standing on rock, pedestal, boulder, skirt, dress, "
    "flowing fabric, bare legs"
)
FLUX_STORYBOARD_PROMPT = (
    "Create exactly one full-bleed vertical grayscale storyboard panel for a Korean webtoon: no comic layout, no extra panels, "
    "no empty frames, and no blank regions. One adult contemporary dancer stands alone "
    "on open flat canyon ground, with distant craggy cliffs clearly separated in the background. Full body, wide shot: "
    "the left leg is lifted straight upward vertically in front of the torso with its foot near the top edge, never a sideways split or side kick; "
    "the right leg is planted on the ground, both feet visible, "
    "and both arms make an open balancing gesture behind the raised left leg in depth order; where an arm crosses the leg, "
    "the arm is occluded and never drawn in front of the leg. She wears a black sleeveless leotard and black opaque tights. "
    "Use clear sketch line art, correct anatomy, readable silhouette, no text, no watermark, no extra limbs, no cropped feet, "
    "and do not merge feet with rocks or terrain."
)


def build_parser() -> argparse.ArgumentParser:
    """Create reproducible local-GPU options; prompt text remains fixed."""
    parser = argparse.ArgumentParser(
        description="고정 텍스트로 한 장면 스토리보드를 생성하고 그 PNG에서 guide를 추출합니다."
    )
    parser.add_argument("--seed", type=int, default=5411, help="재현용 seed (기본값: 5411)")
    parser.add_argument(
        "--model",
        choices=MODEL_CHOICES,
        default="both",
        help="텍스트 스토리보드 모델 또는 두 모델 연속 실행 (기본값: both)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="seed를 1씩 늘려 반복 생성할 횟수 (기본값: 1)",
    )
    parser.add_argument("--steps", type=int, help="확산 반복 수 (모델별 기본값 사용)")
    parser.add_argument("--width", type=int, help="출력 너비 (모델별 기본값 사용)")
    parser.add_argument("--height", type=int, help="출력 높이 (모델별 기본값 사용)")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ASSET_DIR,
        help="타임스탬프 PNG를 저장할 폴더",
    )
    return parser


def require_cuda() -> None:
    """Stop before loading models if this shell cannot access a local GPU."""
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA GPU를 사용할 수 없습니다. NVIDIA 드라이버와 CUDA 접근을 확인하세요.")


def derive_lineart(image: Image.Image) -> Image.Image:
    """Extract a black-on-white line guide from the generated storyboard."""
    grayscale = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    lineart = cv2.adaptiveThreshold(
        grayscale,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        7,
    )
    return Image.fromarray(lineart).convert("RGB")


def derive_canny(image: Image.Image) -> Image.Image:
    """Extract strong boundaries; inspect the result before using it as a guide."""
    grayscale = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(grayscale, 100, 200)
    return Image.fromarray(edges).convert("RGB")


def derive_depth(image: Image.Image) -> Image.Image | None:
    """Estimate relative depth from the generated storyboard, never a fake grayscale map."""
    try:
        from transformers import AutoImageProcessor, AutoModelForDepthEstimation

        if not DEPTH_ANYTHING_MODEL.exists():
            raise FileNotFoundError(
                f"Depth Anything V2 Small이 없습니다: {DEPTH_ANYTHING_MODEL}"
            )

        device = "cuda" if torch.cuda.is_available() else "cpu"
        processor = AutoImageProcessor.from_pretrained(
            DEPTH_ANYTHING_MODEL,
            local_files_only=True,
            use_fast=False,
        )
        model = AutoModelForDepthEstimation.from_pretrained(
            DEPTH_ANYTHING_MODEL,
            local_files_only=True,
            dtype=torch.float16 if device == "cuda" else torch.float32,
        ).to(device).eval()
        inputs = processor(images=image, return_tensors="pt")
        inputs = {name: value.to(device) for name, value in inputs.items()}
        with torch.inference_mode():
            predicted_depth = model(**inputs).predicted_depth
        depth = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1),
            size=(image.height, image.width),
            mode="bicubic",
            align_corners=False,
        ).squeeze()
        depth = depth.float().cpu().numpy()
        minimum, maximum = float(depth.min()), float(depth.max())
        if maximum <= minimum:
            raise RuntimeError("깊이 추정값의 범위가 0입니다.")
        normalized = ((depth - minimum) / (maximum - minimum) * 255).astype(np.uint8)
        del model
        if device == "cuda":
            torch.cuda.empty_cache()
        return Image.fromarray(normalized).convert("RGB")
    except Exception as error:  # The guide must not be replaced by a fake depth map.
        print(f"[depth 생략] 실제 깊이 추정기를 사용할 수 없습니다: {error}")
        return None


def selected_models(model: str) -> tuple[str, ...]:
    """Expand the convenience selector without admitting a third model."""
    return tuple(MODEL_DEFAULTS) if model == "both" else (model,)


def resolve_generation_contract(
    args: argparse.Namespace, model: str
) -> tuple[int, int, int, ModelDefaults]:
    """Apply optional overrides to the selected model's explicit defaults."""
    defaults = MODEL_DEFAULTS[model]
    return (
        args.steps or defaults.steps,
        args.width or defaults.width,
        args.height or defaults.height,
        defaults,
    )


def load_pipeline(model: str) -> StableDiffusionXLPipeline | Flux2KleinPipeline:
    """Load one text-only storyboard pipeline once for one or more seeds."""
    if model == "animagine":
        pipeline = StableDiffusionXLPipeline.from_pretrained(
            ANIMAGINE_MODEL, torch_dtype=torch.float16, local_files_only=True
        )
    else:
        pipeline = Flux2KleinPipeline.from_pretrained(
            FLUX2_KLEIN_MODEL,
            torch_dtype=torch.bfloat16,
            cache_dir=FLUX2_KLEIN_CACHE,
            local_files_only=True,
        )
    # 8 GB GPU에서는 모델 구성요소를 한 번에 올리지 않도록 더 보수적으로 offload한다.
    pipeline.enable_sequential_cpu_offload()
    if model == "animagine":
        pipeline.vae.enable_slicing()
    pipeline.set_progress_bar_config(disable=True)
    return pipeline


def generate_storyboard(
    pipeline: StableDiffusionXLPipeline | Flux2KleinPipeline,
    model: str,
    seed: int,
    steps: int,
    width: int,
    height: int,
    defaults: ModelDefaults,
) -> Image.Image:
    """Generate one text-only storyboard with the requested reproducible seed."""
    if model == "flux2-klein":
        return pipeline(
            prompt=FLUX_STORYBOARD_PROMPT,
            width=width,
            height=height,
            num_inference_steps=steps,
            guidance_scale=defaults.guidance_scale,
            generator=torch.Generator(device=defaults.generator_device).manual_seed(seed),
            max_sequence_length=256,
        ).images[0]
    return pipeline(
        prompt=STORYBOARD_PROMPT,
        negative_prompt=NEGATIVE_PROMPT,
        width=width,
        height=height,
        num_inference_steps=steps,
        guidance_scale=defaults.guidance_scale,
        generator=torch.Generator(device=defaults.generator_device).manual_seed(seed),
    ).images[0]


def save(image: Image.Image, output_dir: Path, stem: str) -> Path:
    """Save one timestamped output and return its path for human review."""
    path = output_dir / f"{stem}.png"
    image.save(path)
    return path


def main() -> None:
    """Create a storyboard and its lineart, canny, and optional depth guides."""
    args = build_parser().parse_args()
    if args.runs < 1:
        raise ValueError("--runs는 1 이상이어야 합니다.")
    models = selected_models(args.model)
    if "animagine" in models and not ANIMAGINE_MODEL.exists():
        raise FileNotFoundError(f"로컬 Animagine XL 모델을 찾지 못했습니다: {ANIMAGINE_MODEL}")
    if "flux2-klein" in models and not FLUX2_KLEIN_CACHE.exists():
        raise FileNotFoundError(f"로컬 FLUX.2 Klein cache를 찾지 못했습니다: {FLUX2_KLEIN_CACHE}")
    require_cuda()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for model in models:
        steps, width, height, defaults = resolve_generation_contract(args, model)
        pipeline = load_pipeline(model)
        try:
            for run_index in range(args.runs):
                seed = args.seed + run_index
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                stem = f"p7-5-3-{timestamp}-{model}-run-{run_index + 1:02d}-seed-{seed}"
                torch.cuda.reset_peak_memory_stats()
                storyboard = generate_storyboard(
                    pipeline, model, seed, steps, width, height, defaults
                )
                outputs = [save(storyboard, args.output_dir, f"{stem}-storyboard")]
                outputs.append(save(derive_lineart(storyboard), args.output_dir, f"{stem}-lineart"))
                outputs.append(save(derive_canny(storyboard), args.output_dir, f"{stem}-canny"))
                depth = derive_depth(storyboard)
                if depth is not None:
                    outputs.append(save(depth, args.output_dir, f"{stem}-depth"))
                for output in outputs:
                    print(f"[{model} 검수 대상] {output}")
                print(f"[{model} run {run_index + 1}/{args.runs} VRAM peak] "
                      f"{torch.cuda.max_memory_allocated() / 1024**2:.1f} MiB")
        finally:
            del pipeline
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

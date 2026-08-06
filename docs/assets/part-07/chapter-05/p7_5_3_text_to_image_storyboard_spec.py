#!/usr/bin/env python3
"""Generate a storyboard first, then derive structural guides from its pixels.

The scene prompt is intentionally fixed. The experiment rejects an output when
the storyboard is unreadable; it does not ask a diffusion model to invent a
lineart, depth, or canny guide before a storyboard exists.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image


ASSET_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ASSET_DIR.parents[3]
ANIMAGINE_MODEL = Path(
    "/home/cbsim/.cache/huggingface/hub/"
    "models--cagliostrolab--animagine-xl-4.0/"
    "snapshots/2b7c1b397761bf5bd3cc42e5b39ec99314a75a96"
)
DEPTH_ANYTHING_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-depth-anything-v2-small"

# 사용자 제공 자세를 글로만 풀어 쓴 스토리보드 기준 장면입니다.
# 참조 사진 자체는 어떤 모델 입력에도 전달하지 않습니다.
STORYBOARD_PROMPT = (
    "1girl, solo, full body, contemporary dancer, standing split, raised leg, "
    "black sleeveless leotard, black opaque tights, planted supporting leg, visible foot, "
    "arms up and out, wide shot, empty canyon ground, distant craggy cliffs, "
    "grayscale sketch, masterpiece, high score"
)
NEGATIVE_PROMPT = (
    "lowres, bad anatomy, bad hands, text, missing fingers, extra digits, cropped, "
    "low quality, watermark, blurry, extra arms, extra legs, floating, hidden feet, "
    "fused foot, ground overlap, standing on rock, pedestal, boulder, skirt, dress, "
    "flowing fabric, bare legs"
)


def build_parser() -> argparse.ArgumentParser:
    """Create reproducible local-GPU options; prompt text remains fixed."""
    parser = argparse.ArgumentParser(
        description="고정 텍스트로 한 장면 스토리보드를 생성하고 그 PNG에서 guide를 추출합니다."
    )
    parser.add_argument("--seed", type=int, default=5411, help="재현용 seed (기본값: 5411)")
    parser.add_argument("--steps", type=int, default=28, help="확산 반복 수 (기본값: 28)")
    parser.add_argument("--width", type=int, default=832, help="출력 너비 (기본값: 832)")
    parser.add_argument("--height", type=int, default=1216, help="출력 높이 (기본값: 1216)")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ASSET_DIR / "p7-5-3-storyboard-guides",
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


def generate_storyboard(args: argparse.Namespace) -> Image.Image:
    """Generate the source storyboard once on the local GPU."""
    pipeline = StableDiffusionXLPipeline.from_pretrained(
        ANIMAGINE_MODEL, torch_dtype=torch.float16, local_files_only=True
    )
    # 8 GB GPU에서는 모델 구성요소를 한 번에 올리지 않도록 더 보수적으로 offload한다.
    pipeline.enable_sequential_cpu_offload()
    pipeline.vae.enable_slicing()
    pipeline.set_progress_bar_config(disable=True)
    image = pipeline(
        prompt=STORYBOARD_PROMPT,
        negative_prompt=NEGATIVE_PROMPT,
        width=args.width,
        height=args.height,
        num_inference_steps=args.steps,
        guidance_scale=5.0,
        generator=torch.Generator(device="cuda").manual_seed(args.seed),
    ).images[0]
    del pipeline
    torch.cuda.empty_cache()
    return image


def save(image: Image.Image, output_dir: Path, stem: str) -> Path:
    """Save one timestamped output and return its path for human review."""
    path = output_dir / f"{stem}.png"
    image.save(path)
    return path


def main() -> None:
    """Create a storyboard and its lineart, canny, and optional depth guides."""
    args = build_parser().parse_args()
    if not ANIMAGINE_MODEL.exists():
        raise FileNotFoundError(f"로컬 Animagine XL 모델을 찾지 못했습니다: {ANIMAGINE_MODEL}")
    require_cuda()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    stem = f"{timestamp}-animagine-seed-{args.seed}"

    torch.cuda.reset_peak_memory_stats()
    storyboard = generate_storyboard(args)
    outputs = [save(storyboard, args.output_dir, f"{stem}-storyboard")]
    outputs.append(save(derive_lineart(storyboard), args.output_dir, f"{stem}-lineart"))
    outputs.append(save(derive_canny(storyboard), args.output_dir, f"{stem}-canny"))
    depth = derive_depth(storyboard)
    if depth is not None:
        outputs.append(save(depth, args.output_dir, f"{stem}-depth"))

    for output in outputs:
        print(f"[검수 대상] {output}")
    print(f"[VRAM peak] {torch.cuda.max_memory_allocated() / 1024**2:.1f} MiB")


if __name__ == "__main__":
    main()

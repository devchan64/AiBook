#!/usr/bin/env python3
"""Run a manually masked SDXL inpaint comparison only after full-frame approval.

The input image and mask are required. White mask pixels are editable and black
pixels are preserved. The default is offline-only so preparing the experiment
cannot silently download the roughly 20 GB checkpoint.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import AutoPipelineForInpainting
from PIL import Image, ImageDraw, ImageFilter


MODEL_ID = "diffusers/stable-diffusion-xl-1.0-inpainting-0.1"


def gpu_memory_mib() -> int | None:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        return int(result.stdout.splitlines()[0])
    except (IndexError, ValueError):
        return None


def load_mask(path: Path, size: tuple[int, int]) -> Image.Image:
    mask = Image.open(path).convert("L")
    if mask.size != size:
        raise ValueError(f"mask size {mask.size} must match input size {size}")
    values = mask.getextrema()
    if values[0] == values[1]:
        raise ValueError("mask must contain both preserved black pixels and editable white pixels")
    return mask


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="human-approved full-frame PNG")
    parser.add_argument("mask", type=Path, help="human-drawn L mask: white edits, black preserves")
    parser.add_argument("output", type=Path)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--negative-prompt", default="extra limbs, extra fingers, text, watermark")
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--strength", type=float, default=0.65)
    parser.add_argument(
        "--guidance-scale",
        type=float,
        default=7.5,
        help="classifier-free guidance; increase only to test prompt adherence inside the fixed mask",
    )
    parser.add_argument("--seed", type=int, default=5501)
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=768)
    parser.add_argument(
        "--mask-feather-px",
        type=float,
        default=2.0,
        help="feather only the final source/output composite boundary; 0 preserves a hard edge",
    )
    parser.add_argument("--allow-download", action="store_true", help="allow first-time checkpoint download")
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this 8 GB inpaint probe")
    if not args.input.is_file() or not args.mask.is_file():
        raise FileNotFoundError("input and manually drawn mask must both exist")
    if not 0.0 < args.strength < 1.0:
        raise ValueError("--strength must be between 0 and 1")
    if args.guidance_scale <= 0:
        raise ValueError("--guidance-scale must be positive")
    if args.mask_feather_px < 0:
        raise ValueError("--mask-feather-px must be zero or positive")

    source = Image.open(args.input).convert("RGB")
    mask = load_mask(args.mask, source.size)
    size = (args.width, args.height)
    source = source.resize(size, Image.Resampling.LANCZOS)
    mask = mask.resize(size, Image.Resampling.NEAREST)
    args.output.mkdir(parents=True, exist_ok=True)
    before = gpu_memory_mib()
    peak = before or 0
    stop = threading.Event()

    def observe_peak() -> None:
        nonlocal peak
        while not stop.is_set():
            observed = gpu_memory_mib()
            if observed is not None:
                peak = max(peak, observed)
            time.sleep(0.2)

    observer = threading.Thread(target=observe_peak, daemon=True)
    observer.start()
    started = time.monotonic()
    try:
        pipe = AutoPipelineForInpainting.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
            local_files_only=not args.allow_download,
        )
        pipe.enable_sequential_cpu_offload()
        pipe.enable_attention_slicing()
        pipe.enable_vae_slicing()
        pipe.set_progress_bar_config(disable=True)
        result = pipe(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            image=source,
            mask_image=mask,
            strength=args.strength,
            guidance_scale=args.guidance_scale,
            num_inference_steps=args.steps,
            width=args.width,
            height=args.height,
            generator=torch.Generator(device="cuda").manual_seed(args.seed),
        ).images[0]
        if result.size != source.size:
            raise RuntimeError(
                f"inpaint output size {result.size} did not match requested source size {source.size}"
            )
        # Diffusion output can alter unmasked pixels despite the mask contract.
        # The production candidate therefore restores those pixels from the fixed
        # source and exposes the raw model output beside the composited result.
        composite_mask = mask.filter(ImageFilter.GaussianBlur(radius=args.mask_feather_px))
        composite = Image.composite(result, source, composite_mask)
        source.save(args.output / "source.png")
        mask.save(args.output / "manual-mask.png")
        result.save(args.output / "raw-model-output.png")
        composite.save(args.output / "inpaint-output.png")
        sheet = Image.new("RGB", (args.width * 4, args.height + 28), "white")
        draw = ImageDraw.Draw(sheet)
        for index, (label, image) in enumerate(
            (
                ("fixed source", source),
                ("operator-defined mask", mask.convert("RGB")),
                ("raw model output", result),
                ("masked composite candidate", composite),
            )
        ):
            x = index * args.width
            draw.text((x + 6, 6), label, fill="black")
            sheet.paste(image, (x, 28))
        sheet.save(args.output / "contact-sheet.png")
    finally:
        stop.set()
        observer.join(timeout=2)

    report = {
        "status": "generated_for_human_review",
        "model": MODEL_ID,
        "input": str(args.input),
        "mask": str(args.mask),
        "mask_contract": "white edit / black preserve; mask is supplied by the operator and reviewed separately",
        "prompt": args.prompt,
        "resolution": list(size),
        "steps": args.steps,
        "strength": args.strength,
        "guidance_scale": args.guidance_scale,
        "mask_feather_px": args.mask_feather_px,
        "seed": args.seed,
        "gpu_memory_before_mib": before,
        "gpu_memory_peak_mib": peak if peak else None,
        "elapsed_seconds": round(time.monotonic() - started, 1),
        "outputs": [
            "source.png",
            "manual-mask.png",
            "raw-model-output.png",
            "inpaint-output.png",
            "contact-sheet.png",
        ],
    }
    (args.output / "run.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output / "inpaint-output.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run CatVTON with the approved person, garment, and operator jacket mask."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import torch
from huggingface_hub import snapshot_download
from PIL import Image, ImageDraw, ImageFilter

catvton_repo = Path(os.environ.get("CATVTON_REPO", ""))
if catvton_repo.is_dir():
    sys.path.insert(0, str(catvton_repo.resolve()))

from model.pipeline import CatVTONPipeline
from utils import init_weight_dtype, resize_and_crop, resize_and_padding


def gpu_memory_mib() -> int | None:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        capture_output=True,
        check=False,
        text=True,
    )
    try:
        return int(result.stdout.splitlines()[0])
    except (IndexError, ValueError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("mask", type=Path)
    parser.add_argument("garment", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=768)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--guidance", type=float, default=2.5)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument(
        "--mask-blur",
        type=int,
        default=0,
        help="Gaussian blur radius for the operator mask; CatVTON's app uses 9",
    )
    parser.add_argument(
        "--repaint",
        action="store_true",
        help="blend the generated result with the original outside the operator mask",
    )
    args = parser.parse_args()

    if not torch.cuda.is_available() or not torch.cuda.is_bf16_supported():
        raise RuntimeError("CatVTON preflight requires a CUDA GPU with bfloat16 support")
    if args.mask_blur < 0:
        raise ValueError("--mask-blur must be zero or positive")
    if not all(path.is_file() for path in (args.source, args.mask, args.garment)):
        raise FileNotFoundError("source, mask, and garment must exist")

    catvton_path = snapshot_download("zhengchong/CatVTON", local_files_only=True)
    base_path = snapshot_download("booksforcharlie/stable-diffusion-inpainting", local_files_only=True)
    person = resize_and_crop(Image.open(args.source).convert("RGB"), (args.width, args.height))
    mask = resize_and_crop(Image.open(args.mask).convert("L"), (args.width, args.height))
    repaint_mask = mask.copy()
    if args.mask_blur:
        mask = mask.filter(ImageFilter.GaussianBlur(args.mask_blur))
    garment = resize_and_padding(Image.open(args.garment).convert("RGB"), (args.width, args.height))
    args.output.mkdir(parents=True, exist_ok=True)

    before = gpu_memory_mib()
    peak = before or 0
    stop = threading.Event()

    def observe_peak() -> None:
        nonlocal peak
        while not stop.is_set():
            used = gpu_memory_mib()
            if used is not None:
                peak = max(peak, used)
            time.sleep(0.2)

    observer = threading.Thread(target=observe_peak, daemon=True)
    observer.start()
    started = time.monotonic()
    try:
        pipeline = CatVTONPipeline(
            base_ckpt=base_path,
            attn_ckpt=catvton_path,
            attn_ckpt_version="mix",
            weight_dtype=init_weight_dtype("bf16"),
            use_tf32=True,
            skip_safety_check=True,
            device="cuda",
        )
        result = pipeline(
            image=person,
            condition_image=garment,
            mask=mask,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance,
            generator=torch.Generator(device="cuda").manual_seed(args.seed),
        )[0]
        if result.size != (args.width, args.height):
            raise RuntimeError(
                "CatVTON output size contract failed: "
                f"requested {(args.width, args.height)}, received {result.size}"
            )
        if args.repaint:
            repaint_mask = repaint_mask.filter(ImageFilter.GaussianBlur(max(1, args.height // 50)))
            result = Image.composite(result, person, repaint_mask)
        person.save(args.output / "source.png")
        mask.save(args.output / "operator-mask.png")
        garment.save(args.output / "garment-reference.png")
        result.save(args.output / "candidate.png")
        sheet = Image.new("RGB", (args.width * 4, args.height + 28), "white")
        draw = ImageDraw.Draw(sheet)
        for index, (label, image) in enumerate(
            (("approved person", person), ("operator mask", mask.convert("RGB")), ("approved garment", garment), ("CatVTON candidate", result))
        ):
            draw.text((index * args.width + 6, 6), label, fill="black")
            sheet.paste(image, (index * args.width, 28))
        sheet.save(args.output / "contact-sheet.png")
    finally:
        stop.set()
        observer.join(timeout=2)

    (args.output / "result.json").write_text(
        json.dumps(
            {
                "status": "generated_for_human_review",
                "model": "zhengchong/CatVTON mix-48k-1024",
                "base_model": "booksforcharlie/stable-diffusion-inpainting",
                "source": str(args.source),
                "mask": str(args.mask),
                "garment": str(args.garment),
                "resolution": [args.width, args.height],
                "steps": args.steps,
                "guidance": args.guidance,
                "mask_blur": args.mask_blur,
                "repaint": args.repaint,
                "seed": args.seed,
                "gpu_memory_before_mib": before,
                "gpu_memory_peak_mib": peak if peak else None,
                "elapsed_seconds": round(time.monotonic() - started, 1),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

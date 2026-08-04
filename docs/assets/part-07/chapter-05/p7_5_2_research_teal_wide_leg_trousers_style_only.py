#!/usr/bin/env python3
"""Generate a style-only trouser detail for Mira's wardrobe reference."""

from __future__ import annotations

import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
STYLE_LEDGER = ROOT / "p7-5-1-local-style-pack-review.json"
STYLE_SCENE_ID = "outdoor-day-wide"
OUTPUT = ROOT / "p7-5-2-teal-wide-leg-trousers-style-only-candidate.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"

PROMPT = """Mira's deep blue-teal high-waisted wide-leg trousers, isolated garment detail in a clean front view on off-white paper. Use the reference image only for thin charcoal lines and transparent pale-blue and muted-teal watercolor style. Show a fitted high waistband with belt loops, a center fly, long straight wide legs, crisp vertical seams, and hems that fall to the shoe collar without pooling on the ground. Make the fabric clearly dark, saturated petrol teal, with deep teal seam shadows; not white, pale aqua, gray, or pastel. No person, body, leg, foot, hanger, text, logo, border, or other object."""


def approved_style_source() -> Path:
    ledger = json.loads(STYLE_LEDGER.read_text(encoding="utf-8"))
    for run in ledger["reviewed_runs"]:
        if run.get("scene_id") == STYLE_SCENE_ID and run.get("status") == "approved":
            source = ROOT / run["asset"]
            if source.is_file():
                return source
    raise LookupError(f"No approved style source for {STYLE_SCENE_ID}")


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    started = time.monotonic()
    image = pipe(
        image=Image.open(approved_style_source()).convert("RGB"),
        prompt=PROMPT,
        width=768,
        height=1024,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62270),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate an unapproved Mira front-face reference from her face and hair-clip masters."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
FACE_MASTER = ROOT / "p7-5-2-face-master-v1.png"
HAIR_CLIP_MASTER = ROOT / "p7-5-2-prop-reference-v2-hair-clip.png"
STYLE_REFERENCE = ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png"
OUTPUT = ROOT / "p7-5-2-face-front-v1-candidate.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"

PROMPT = """One original adult Korean webtoon woman in a strict zero-yaw front head-and-shoulders portrait on off-white paper. Preserve the face master: oval face, warm light-peach skin, soft tapered jaw, equal almond eyes, and a calm neutral expression. Both eyes have matching chestnut-brown irises with a dark limbal ring, centered black pupils, and one upper viewer-left oval catchlight. Preserve the dark petrol-teal rounded bob, deep viewer-left side part, diagonal fringe, and jaw-length tapered side locks. Use the hair-clip master only for one silver long-rhombus plate with a matching central long-rhombus cutout, positioned above the viewer-left temple. Use the style reference only for thin charcoal lines and transparent pale-blue and muted-teal watercolor washes. No full body, clothing detail, bag, text, border, or extra person."""


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
        image=[
            Image.open(FACE_MASTER).convert("RGB"),
            Image.open(HAIR_CLIP_MASTER).convert("RGB"),
            Image.open(STYLE_REFERENCE).convert("RGB"),
        ],
        prompt=PROMPT,
        width=768,
        height=1024,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62272),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

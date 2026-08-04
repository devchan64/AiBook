#!/usr/bin/env python3
"""Generate an unapproved front-face master for Mira from a style reference and prompt."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
STYLE_REFERENCE = ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png"
OUTPUT = ROOT / "p7-5-2-face-master-v1-candidate.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"

PROMPT = """One original adult Korean webtoon woman in a strict front head-and-shoulders portrait on off-white paper. Mira has an oval face, warm light-peach skin, a soft tapered jaw, and equal almond eyes. Each eye has a medium chestnut-brown iris with a dark limbal ring, subtle radial amber-brown texture, a centered round black pupil, and one small oval white catchlight at its upper viewer-left; match both eyes exactly. Her hair is a saturated dark petrol-teal bob, never gray, pale aqua, or bright blue: a rounded crown, deep side part above the viewer-left temple, a broad diagonal fringe across the forehead, and separate tapered side locks ending at the jaw. Place one silver long-rhombus hair clip with a matching long-rhombus cutout above that viewer-left temple. Calm neutral expression. Use the style reference only for thin charcoal lines and transparent pale-blue and muted-teal watercolor washes. No full body, bag, text, border, or extra person."""


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
        image=Image.open(STYLE_REFERENCE).convert("RGB"),
        prompt=PROMPT,
        width=768,
        height=1024,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62271),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

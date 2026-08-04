#!/usr/bin/env python3
"""Test a deep-teal-blue Mira trousers reference from prompt only."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
OUTPUT = ROOT / "p7-5-2-prop-trousers-deep-teal-blue-candidate.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"

PROMPT = """One isolated pair of deep teal blue high-waisted wide-leg trousers in a clean front view on a plain off-white background. Use one blue-dominant dark teal base color, neither green turquoise nor gray. Belt loops, center fly, crisp vertical seams, straight wide legs, and hems above the shoe collar. Clean product illustration. No person, hanger, text, logo, or other object."""


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
        prompt=PROMPT,
        width=768,
        height=1024,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62280),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

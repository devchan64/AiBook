#!/usr/bin/env python3
"""Probe a right front-quarter face using only the frontal full-body master."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
FRONT = ROOT / "p7-5-2-multireference-turnaround-v1-front.png"
OUTPUT = ROOT / "p7-5-2-face-detail-right-quarter-from-fullbody-candidate.png"

PROMPT = """One original Korean webtoon character face detail, from the top of the hair to the upper chest, on off-white paper. The sole reference is the frontal full-body master for this exact woman.
Turn her head 15 degrees toward image-right. Keep both eyes visible, the far eye slightly narrower, and the nose diagonal rather than a profile. Preserve the teal jaw-length bob, white jacket, charcoal shirt, thin charcoal lines, and transparent pale-blue and muted-teal watercolor finish. No new person, hair redesign, strict profile, cropped chin, text, logo, or watermark."""


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B",
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    started = time.monotonic()
    image = pipe(
        image=[Image.open(FRONT).convert("RGB")],
        prompt=PROMPT,
        width=768,
        height=1024,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62256),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

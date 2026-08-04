#!/usr/bin/env python3
"""Generate an unapproved prompt-only hair-clip reference candidate."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
OUTPUT = ROOT / "p7-5-2-prop-reference-v2-hair-clip-candidate.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
PROMPT = """One isolated silver hair clip in a clean horizontal product view on a plain off-white background. Use one flat, elongated long-rhombus metal plate with four sharp pointed corners and a broad smooth silver rim. Cut one smaller elongated long-rhombus hole with four sharp pointed corners through the center, parallel to the outer plate; show the off-white background through it. Add one short barrette clasp behind the plate. No rounded slot, gem, pattern, person, text, logo, or other object."""


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
        height=768,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62285),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

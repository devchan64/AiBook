#!/usr/bin/env python3
"""Generate a prompt-only Mira front-face candidate without a hair accessory."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
OUTPUT = ROOT / "p7-5-2-face-front-no-accessory-v3-candidate.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"

PROMPT = """Original adult Korean webtoon woman, strict front head-and-shoulders portrait on off-white paper. Oval face with warm light-peach skin, a soft tapered jaw, a slightly higher straight nose bridge, and a defined nose tip; calm neutral expression. Equal almond cat eyes with subtly upturned outer corners, two-color irises of chestnut brown and amber blended in a subtle radial wave pattern, dark limbal rings, and centered black pupils. Deep teal blue hair in a rounded jaw-length bob: a deep viewer-right side part, one broad fringe sweeping across to the viewer-left forehead, and tapered side locks at the jaw. No hair accessory. No full body, bag, text, border, or extra person."""


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
        generator=torch.Generator(device="cpu").manual_seed(62282),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

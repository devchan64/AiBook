#!/usr/bin/env python3
"""Generate a Mira front-face candidate with a cropped-top neckline reference."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
OUTPUT = ROOT / "p7-5-2-face-front-no-accessory-v3-candidate.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
CROPPED_TOP = ROOT / "p7-5-2-prop-reference-v2-gray-cropped-top.png"

PROMPT = """Original adult Korean webtoon woman, strict front head-and-neck portrait on off-white paper. A tight crop runs from hair top through the lower neck, with a narrow charcoal-gray crew-neckline arc touching the bottom edge. Oval face with warm light-peach skin, broad low-set cheekbones, visibly soft cheek fullness, and a smooth taper into a soft jaw. Slightly higher straight nose bridge and a defined nose tip; calm neutral expression. Equal almond cat eyes with subtly upturned outer corners, two-color irises of chestnut brown and amber blended in a subtle radial wave pattern, dark limbal rings, and centered black pupils. Deep teal blue hair in a rounded jaw-length bob: a deep viewer-right side part, one broad fringe sweeping across to the viewer-left forehead, and tapered side locks at the jaw. Use the gray cropped-top reference only for the charcoal-gray crew-neckline arc."""


def main() -> None:
    if not CROPPED_TOP.is_file():
        raise FileNotFoundError(CROPPED_TOP.name)
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
        image=[Image.open(CROPPED_TOP).convert("RGB")],
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

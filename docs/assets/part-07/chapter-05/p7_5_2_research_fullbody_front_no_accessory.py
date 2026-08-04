#!/usr/bin/env python3
"""Generate a front full-body Mira candidate from approved face and prop references."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
REFERENCES = [
    ROOT / "p7-5-2-face-front-v2.png",
    ROOT / "p7-5-2-prop-reference-v2-jacket.png",
    ROOT / "p7-5-2-prop-reference-v2-trousers.png",
    ROOT / "p7-5-2-prop-reference-v2-shoes.png",
    ROOT / "p7-5-2-prop-reference-v2-crossbody-bag.png",
]
OUTPUT = ROOT / "p7-5-2-fullbody-front-v5-candidate.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"

PROMPT = """Original adult Korean webtoon woman, isolated full-body front reference on a blank off-white studio backdrop. Keep the face reference identity: warm light-peach skin, almond cat eyes with chestnut-brown and amber irises, deep teal blue jaw-length bob, and no hair accessory. She is 165 cm tall with crown-to-sole height 7.5 times her head height, standing neutrally with head, shoulders, torso, hips, knees, feet, and gaze facing forward; show both shoe soles with space above her crown and below her feet. Use the wardrobe references: a short white cropped utility jacket over a charcoal crew-neck shirt, with its hem ending at the natural waist just above the trouser waistband; deep teal blue wide-leg trousers; and white low-top sneakers. Wear one deep-navy canvas crossbody bag naturally at the viewer-right hip: its top meets the waistband and its base reaches the upper thigh. One long charcoal strap starts at the viewer-left shoulder and crosses diagonally over the torso to the bag. No extra person, prop, text, or border."""


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    if missing := [path.name for path in REFERENCES if not path.is_file()]:
        raise FileNotFoundError(", ".join(missing))

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    started = time.monotonic()
    image = pipe(
        image=[Image.open(path).convert("RGB") for path in REFERENCES],
        prompt=PROMPT,
        width=768,
        height=1280,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62285),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

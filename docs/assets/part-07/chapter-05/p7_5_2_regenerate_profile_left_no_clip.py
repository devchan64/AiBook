#!/usr/bin/env python3
"""Create an unapproved left-profile turnaround without a clip or hair part."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
FRONT = ROOT / "p7-5-2-multireference-turnaround-v1-front.png"
REAR = ROOT / "p7-5-2-multireference-turnaround-v1-rear.png"
STYLE = ROOT / "p7-5-1-style-downtown-clear-day-wide-local-gpu-v1.png"
OUTPUT = ROOT / "p7-5-2-multireference-turnaround-v1-profile-left-no-clip-v3-candidate.png"

PROMPT = """Create exactly one original full-body adult Korean webtoon character turnaround illustration.
Reference 1 is the authoritative front identity for the same woman. Reference 2 establishes her unornamented rear hair, jacket, trousers, and footwear. Reference 3 establishes only the watercolor rendering treatment.
Use a neutral orthographic studio-camera view, not a posed portrait. Rotate the entire body, including face, gaze, shoulders, torso, hips, knees, and both feet, to a strict 90-degree left side profile facing image-left. Show the complete body from the top of her head to both shoe soles.
Both feet are planted parallel, knees relaxed, weight centered, and both arms hang naturally at the sides. Keep warm light-peach skin, a white cropped utility jacket, charcoal crew-neck shirt, teal wide-leg trousers, and white sneakers.
Draw a single continuous jaw-length deep teal-blue bob with a smooth uninterrupted fringe. Do not draw a center part, side part, scalp division line, separated bangs, exposed forehead wedge, or any hairline gap. Show no hair clip, pin, ornament, diamond, rectangle, metallic object, or decorative accessory anywhere in the hair.
Transfer thin charcoal contours, transparent pale-blue and muted-teal watercolor washes, subtle pigment pooling, soft off-white paper, and cool-gray reflected shadows. Use a quiet off-white watercolor studio background.
No bag, jewelry, handheld object, extra person, walking, front-facing head or torso, cropped body, panel border, outer frame, text, logo, watermark, photorealism, screentones, glossy cel shading, opaque shadows, or heavy hatching."""


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
        image=[Image.open(FRONT).convert("RGB"), Image.open(REAR).convert("RGB"), Image.open(STYLE).convert("RGB")],
        prompt=PROMPT,
        width=768,
        height=1152,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(420903),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Create an unapproved left-profile face from front identity and rear hair."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
FRONT_FACE = ROOT / "p7-5-2-face-detail-v2-front-iris-pupil-spec.png"
REAR_HAIR = ROOT / "p7-5-2-face-detail-v2-rear-hair.png"
STYLE = ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png"
OUTPUT = ROOT / "p7-5-2-face-detail-v3-profile-left-no-clip-candidate.png"

PROMPT = """Create exactly one original Korean webtoon character face-detail reference, cropped from the top of the hair to the upper chest.
Reference 1 is the authoritative front identity for the same adult woman. Reference 2 is the authoritative unornamented rear hair. Reference 3 supplies only thin charcoal lines and transparent watercolor treatment.
Create a strict 90-degree left side profile: the nose, lips, chin, gaze, neck, and shoulders all point image-left. Show exactly one visible eye and one eyebrow; do not show a far-eye contour, a frontal face, or a three-quarter turn.
Keep warm light-peach skin, one dark chestnut-brown iris with a centered pupil, a white cropped utility jacket, and charcoal crew-neck shirt. Draw a continuous jaw-length deep teal-blue bob with a smooth uninterrupted fringe.
The character's silver temple clip is omitted in this left side profile: draw no hair clip, pin, ornament, diamond, rectangle, metallic shape, scalp part, hair division line, exposed forehead wedge, or hairline gap.
Keep one coherent head, neck, and pair of shoulders. No bag, strap, jewelry, handheld object, extra person, duplicate face, extra eyes, cropped chin, text, logo, watermark, panel border, outer frame, photorealism, glossy cel shading, opaque shadows, or heavy hatching."""


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
        image=[Image.open(FRONT_FACE).convert("RGB"), Image.open(REAR_HAIR).convert("RGB"), Image.open(STYLE).convert("RGB")],
        prompt=PROMPT,
        width=768,
        height=1024,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62188),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

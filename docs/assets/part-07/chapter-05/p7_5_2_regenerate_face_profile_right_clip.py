#!/usr/bin/env python3
"""Create a right-profile face from a profile and front-clip reference."""

from __future__ import annotations

import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
RIGHT_PROFILE = ROOT / "p7-5-2-multireference-turnaround-v1-profile-right.png"
FRONT_FACE = ROOT / "p7-5-2-face-detail-v2-front-iris-pupil-spec.png"
STYLE = ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png"
OUTPUT = ROOT / "p7-5-2-face-detail-v3-profile-right-front-clip-candidate.png"

PROMPT = """Create exactly one original Korean webtoon character face-detail reference, cropped from the top of the hair to the upper chest.
Reference 1 is the authoritative right-profile silhouette and identity for the same adult woman. Reference 2 is the authoritative front identity and hair-clip shape. Reference 3 supplies only thin charcoal lines and transparent watercolor treatment.
Create a strict 90-degree right side profile: the nose, lips, chin, gaze, neck, and shoulders all point image-right. Show exactly one visible eye and one eyebrow; do not show a far-eye contour, a frontal face, or a three-quarter turn.
Keep warm light-peach skin, one dark chestnut-brown iris with a centered pupil, a white cropped utility jacket, and charcoal crew-neck shirt. Draw a jaw-length deep teal-blue bob with one visible natural side part and a coherent visible ear behind the side lock.
Show exactly one small diamond-shaped silver hair clip, tilted 45 degrees, on the outer hair surface at the front fringe-side-lock junction. Relative to the front reference, move it forward toward the bangs and hairline above the cheekbone; it must sit clearly in front of the ear, never beside or behind it. Keep the visible ear, its outer rim, and the surrounding side-lock silhouette coherent with the right-profile reference.
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
        image=[Image.open(RIGHT_PROFILE).convert("RGB"), Image.open(FRONT_FACE).convert("RGB"), Image.open(STYLE).convert("RGB")],
        prompt=PROMPT,
        width=768,
        height=1024,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62193),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    print(f"{time.monotonic() - started:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

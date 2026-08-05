#!/usr/bin/env python3
"""Generate a chin-cropped Mira front-face candidate."""

from __future__ import annotations

import time
import json
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
OUTPUT = ROOT / "p7-5-2-face-front-chin-crop-v4-candidate.png"
REPORT = ROOT / "p7-5-2-face-front-chin-crop-v4-review.json"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"

PROMPT = """Original adult Korean webtoon woman, strict front head-only portrait on off-white paper. The image contains the full hair mass, face, jaw, and chin only; its lower edge ends directly beneath the chin. Oval face with warm light-peach skin, broad low-set cheekbones, visibly soft cheek fullness, and a smooth taper into a soft jaw. High straight nose bridge and a defined nose tip; calm neutral expression. Equal almond cat eyes with subtly upturned outer corners, two-color irises of chestnut brown and amber blended in a subtle radial wave pattern, dark limbal rings, and centered black pupils. Deep teal-blue hair in a rounded jaw-length bob: a deep viewer-right side part, one broad fringe sweeping across to the viewer-left forehead, and tapered side locks at the jaw."""


def prompt_word_count(text: str) -> int:
    return len(text.split())


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
        generator=torch.Generator(device="cpu").manual_seed(62282),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    elapsed = round(time.monotonic() - started, 2)
    REPORT.write_text(
        json.dumps(
            {
                "status": "review_required",
                "output": OUTPUT.name,
                "seed": 62282,
                "prompt": PROMPT,
                "prompt_word_count": prompt_word_count(PROMPT),
                "model": MODEL_ID,
                "image_size": [768, 768],
                "elapsed_seconds": elapsed,
                "decision": "Candidate only; human review is required before it becomes the front-face reference.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"{elapsed:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

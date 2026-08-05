#!/usr/bin/env python3
"""Generate a chin-cropped Mira front-face candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
OUTPUT = ROOT / "p7-5-2-face-front-with-hair-v3-candidate.png"
REPORT = ROOT / "p7-5-2-face-front-with-hair-v3-review.json"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"

PROMPT = """Strict frontal head-only portrait of a twenty-two-year-old Asian female on off-white. Very fair pale-peach skin. A small, pronounced cat-like face: elongated forehead above the brows, compact oval, fuller soft cheeks, slender V-shaped jawline, and short rounded chin. High slim nose bridge, small rounded tip, and small lips with a fuller lower lip. Very large symmetric upturned almond cat eyes with centered pupils; chestnut-brown and orange-amber irises. Deep petrol-teal, extremely voluminous jaw-length bob with medium-density hair. A deep viewer-right side part and full short fringe sweep across the viewer-left forehead, ending above the eyebrow. Large loose S-waves, pronounced inward C-curls, and tapered side locks create an expansive rounded silhouette. Crop directly below the chin."""


def prompt_word_count(text: str) -> int:
    return len(text.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed-offset",
        type=int,
        default=0,
        help="Add an offset to the face-with-hair seed.",
    )
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    seed = 62294 + args.seed_offset
    started = time.monotonic()
    image = pipe(
        prompt=PROMPT,
        width=768,
        height=768,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(seed),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    elapsed = round(time.monotonic() - started, 2)
    REPORT.write_text(
        json.dumps(
            {
                "status": "review_required",
                "seed_offset": args.seed_offset,
                "output": OUTPUT.name,
                "seed": seed,
                "prompt": PROMPT,
                "prompt_word_count": prompt_word_count(PROMPT),
                "references": [],
                "model": MODEL_ID,
                "image_size": [768, 768],
                "elapsed_seconds": elapsed,
                "decision": "Candidate only; human review is required before it becomes a front-face or geometry reference.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"{elapsed:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

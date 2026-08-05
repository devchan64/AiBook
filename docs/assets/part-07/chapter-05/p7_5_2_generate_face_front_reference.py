#!/usr/bin/env python3
"""Generate one or more chin-cropped Mira front-face candidates."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
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
        help="Offset applied to the first face-with-hair seed.",
    )
    parser.add_argument(
        "--seed-count",
        type=int,
        default=1,
        help="Number of consecutive seed variants to generate.",
    )
    parser.add_argument(
        "--seed-step",
        type=int,
        default=1,
        help="Increment between consecutive seed variants.",
    )
    parser.add_argument(
        "--output-prefix",
        help="Filename prefix placed before the automatic timestamp and seed suffixes.",
    )
    args = parser.parse_args()
    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    first_seed = 62294 + args.seed_offset
    prefix = args.output_prefix or "p7-5-2-face-front-with-hair-v3"
    run_timestamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%f%z")
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        output = ROOT / f"{prefix}-{run_timestamp}-seed-{seed}-candidate.png"
        report = ROOT / f"{prefix}-{run_timestamp}-seed-{seed}-review.json"
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
        image.save(output)
        elapsed = round(time.monotonic() - started, 2)
        report.write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "seed_offset": args.seed_offset,
                    "seed_step": args.seed_step,
                    "batch_index": batch_index,
                    "batch_size": args.seed_count,
                    "run_timestamp": run_timestamp,
                    "output_prefix": prefix,
                    "output": output.name,
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
        print(f"[{batch_index + 1}/{args.seed_count}] {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

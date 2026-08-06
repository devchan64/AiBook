#!/usr/bin/env python3
"""Generate one or more face turnaround sheets from the frontal reference."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path(__file__).resolve().parent
FRONT = ROOT / "p7-5-2-face-front-reference.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
BASE_SEED = 62377
TIMESTAMP_FORMAT = "%Y%m%dT%H%M%S%f%z"
HEAD_INPUT_BOTTOM = 720
SHEET_SIZE = 1024
VIEW_RULES = {
    "front": "front view at 0 degrees, with the nose centered and both eyes equally visible",
    "front_quarter": "45-degree front-quarter view, with the near eye fully visible and the far eye half visible",
    "profile": "90-degree profile view, with one near eye visible in side view and the far eye hidden",
    "rear": "180-degree rear view, facing away from the camera, with no nose or eyes visible",
}
APPEARANCE_RULE = (
    "Keep chestnut-brown and orange-amber irises with visible radial texture, "
    "a consistent iris diameter and pupil-to-iris ratio in every panel, "
    "allowing only perspective foreshortening; "
    "keep the gaze direction aligned with the nose direction in every visible face; "
    "a high slim nose bridge and a small rounded nose tip; "
    "and deep petrol-teal, voluminous jaw-length bob hair with a deep side part, "
    "short swept fringe, loose S-waves, inward C-curls, and tapered side locks."
)


def prompt_word_count(text: str) -> int:
    return len(text.split())


def build_prompt(views: tuple[str, ...]) -> str:
    layout = "2 by 2" if len(views) == 4 else f"{len(views)}-panel"
    positions = {
        1: ("single panel",),
        2: ("left panel", "right panel"),
        3: ("top-left", "top-right", "bottom-center"),
        4: ("top-left", "top-right", "bottom-left", "bottom-right"),
    }[len(views)]
    view_list = "; ".join(
        f"{position}: {VIEW_RULES[view]}" for position, view in zip(positions, views, strict=True)
    )
    return (
        f"{layout} face turnaround of the same woman from the reference image. "
        f"{APPEARANCE_RULE} Panel directions: {view_list}. Use one distinct view per panel."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(VIEW_RULES),
        default=("front", "profile"),
        help="Face views to include in reading order; defaults to front and profile for review.",
    )
    parser.add_argument(
        "--seed-offset",
        type=int,
        default=0,
        help="Offset applied to the first turnaround-sheet seed.",
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
        default="p7-5-2-face-turnaround-sheet-v9",
        help="Filename prefix placed before the automatic timestamp and seed suffixes.",
    )
    args = parser.parse_args()
    if len(args.views) > 4:
        raise ValueError("A turnaround sheet accepts at most four views")
    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")
    if not FRONT.is_file():
        raise FileNotFoundError(FRONT.name)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    source = Image.open(FRONT).convert("RGB")
    anchor = source.crop((0, 0, source.width, HEAD_INPUT_BOTTOM))
    prompt = build_prompt(tuple(args.views))
    first_seed = BASE_SEED + args.seed_offset
    run_timestamp = datetime.now().astimezone().strftime(TIMESTAMP_FORMAT)
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        output = ROOT / f"{args.output_prefix}-{run_timestamp}-seed-{seed}-candidate.png"
        report = ROOT / f"{args.output_prefix}-{run_timestamp}-seed-{seed}-review.json"
        started = time.monotonic()
        sheet = pipe(
            image=anchor,
            prompt=prompt,
            width=SHEET_SIZE,
            height=SHEET_SIZE,
            num_inference_steps=12,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(seed),
            max_sequence_length=256,
        ).images[0]
        sheet.save(output)
        elapsed = round(time.monotonic() - started, 2)
        report.write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "output": output.name,
                    "seed": seed,
                    "seed_offset": args.seed_offset,
                    "seed_step": args.seed_step,
                    "batch_index": batch_index,
                    "batch_size": args.seed_count,
                    "run_timestamp": run_timestamp,
                    "output_prefix": args.output_prefix,
                    "prompt": prompt,
                    "prompt_word_count": prompt_word_count(prompt),
                    "references": [FRONT.name],
                    "input_transform": f"Cropped the frontal anchor at y={HEAD_INPUT_BOTTOM} before inference.",
                    "sheet_layout": args.views,
                    "style_reference": None,
                    "model": MODEL_ID,
                    "image_size": [SHEET_SIZE, SHEET_SIZE],
                    "elapsed_seconds": elapsed,
                    "decision": "Candidate only; review each view for layout, direction, and identity consistency.",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"[{batch_index + 1}/{args.seed_count}] {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

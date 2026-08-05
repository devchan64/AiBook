#!/usr/bin/env python3
"""Generate full-body turnaround-sheet candidates from approved face and outfit references."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
BASE_SEED = 62377
TIMESTAMP_FORMAT = "%Y%m%dT%H%M%S%f%z"
FACE_TURNAROUND = ROOT / "p7-5-2-face-turnaround-reference.png"
FRONT_BODY = ROOT / "p7-5-2-fullbody-front-reference.png"
OUTFIT_REFERENCES = [
    ROOT / "p7-5-2-outfit-crop-top-waist-reference.png",
    ROOT / "p7-5-2-prop-reference-v2-trousers.png",
    ROOT / "p7-5-2-prop-reference-v2-shoes.png",
]
REFERENCES = [FACE_TURNAROUND, FRONT_BODY, *OUTFIT_REFERENCES]
SHEET_WIDTH = 1024
SHEET_HEIGHT = 1536
VIEW_RULES = {
    "front": "front view at 0 degrees, with face, chest, pelvis, knees, and feet facing forward",
    "front_quarter": "45-degree front-quarter view, with face, chest, pelvis, knees, and feet turning together",
    "profile": "90-degree profile view, with one near arm visible beside the torso and the far arm hidden",
    "rear": "180-degree rear view, with head, shoulders, torso, hips, knees, and feet facing away",
}
APPEARANCE_RULE = (
    "Use the face turnaround sheet for the same face, gaze, nose, and hair in every visible view. "
    "Use the frontal body for a consistent 7.5-head body proportion and full hair-to-sole framing. "
    "Keep the charcoal-gray micro-crop crew-neck top, bare-midriff gap, deep teal-blue wide-leg trousers, "
    "and white lace-up low-top sneakers from the outfit references."
)


def prompt_word_count(text: str) -> int:
    return len(text.split())


def build_prompt(views: tuple[str, ...]) -> str:
    if len(views) != 4:
        raise ValueError("A full-body turnaround sheet requires exactly four views")
    positions = ("top-left", "top-right", "bottom-left", "bottom-right")
    view_list = "; ".join(
        f"{position}: {VIEW_RULES[view]}" for position, view in zip(positions, views, strict=True)
    )
    return (
        "2 by 2 full-body turnaround reference sheet of the same woman on an off-white studio background. "
        f"{APPEARANCE_RULE} Panel directions: {view_list}. "
        "Each panel shows one distinct neutral upright standing pose from hair to soles."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(VIEW_RULES),
        default=("front", "front_quarter", "profile", "rear"),
        help="Four views in panel reading order.",
    )
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset applied to the first seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seed variants.")
    parser.add_argument("--seed-step", type=int, default=1, help="Increment between seed variants.")
    parser.add_argument(
        "--output-prefix",
        default="p7-5-2-fullbody-turnaround-sheet",
        help="Filename prefix placed before the automatic timestamp and seed suffixes.",
    )
    args = parser.parse_args()
    if len(args.views) != 4:
        raise ValueError("A full-body turnaround sheet requires exactly four views")
    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")
    if missing := [path.name for path in REFERENCES if not path.is_file()]:
        raise FileNotFoundError(", ".join(missing))
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    prompt = build_prompt(tuple(args.views))
    run_timestamp = datetime.now().astimezone().strftime(TIMESTAMP_FORMAT)
    first_seed = BASE_SEED + args.seed_offset
    reference_images = [Image.open(path).convert("RGB") for path in REFERENCES]
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        output = ROOT / f"{args.output_prefix}-{run_timestamp}-seed-{seed}-candidate.png"
        report = ROOT / f"{args.output_prefix}-{run_timestamp}-seed-{seed}-review.json"
        started = time.monotonic()
        sheet = pipe(
            image=reference_images,
            prompt=prompt,
            width=SHEET_WIDTH,
            height=SHEET_HEIGHT,
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
                    "references": [path.name for path in REFERENCES],
                    "sheet_layout": args.views,
                    "model": MODEL_ID,
                    "image_size": [SHEET_WIDTH, SHEET_HEIGHT],
                    "elapsed_seconds": elapsed,
                    "decision": "Experiment only; review body proportion, outfit continuity, view separation, and face identity before approval.",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"[{batch_index + 1}/{args.seed_count}] {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

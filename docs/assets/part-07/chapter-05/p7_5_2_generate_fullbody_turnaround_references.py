#!/usr/bin/env python3
"""Generate individual full-body turnaround candidates from face and outfit references."""

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
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
BASE_SEED = 62294
TIMESTAMP_FORMAT = "%Y%m%dT%H%M%S%f%z"
FACE_TURNAROUND = ROOT / "p7-5-2-face-turnaround-reference.png"
OUTFIT_REFERENCES = [
    ROOT / "p7-5-2-outfit-crop-top-waist-reference.png",
    ROOT / "p7-5-2-prop-reference-v2-trousers.png",
    ROOT / "p7-5-2-prop-reference-v2-shoes.png",
]
REFERENCES = [FACE_TURNAROUND, *OUTFIT_REFERENCES]
IMAGE_WIDTH = 768
IMAGE_HEIGHT = 1152
VIEW_RULES = {
    "front": "front view, facing the camera",
    "front_quarter": "front three-quarter view, with face, chest, pelvis, knees, and feet turned together",
    "profile": "side profile, with one near arm beside the torso and the far arm hidden",
    "rear": "rear view, facing away from the camera",
}
APPEARANCE_RULE = (
    "Use the face turnaround sheet for the same face, gaze, nose, and hair in every visible view. "
    "Keep the charcoal-gray micro-crop crew-neck top, bare-midriff gap, deep teal-blue wide-leg trousers, "
    "and white lace-up low-top sneakers from the outfit references."
)


def prompt_word_count(text: str) -> int:
    return len(text.split())


def build_prompt(view: str) -> str:
    return (
        "Full-body character turnaround reference of one woman on an off-white studio background. "
        f"{APPEARANCE_RULE} {VIEW_RULES[view]}. "
        "One neutral upright standing figure, fully visible from hair to shoe soles, centered in the frame. "
        "No crop, no duplicate body, no other person, no text, and no labels."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(VIEW_RULES),
        default=("front", "front_quarter", "profile", "rear"),
        help="Individual views to generate; each view is written as a separate PNG.",
    )
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset applied to the first seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seed variants.")
    parser.add_argument("--seed-step", type=int, default=1, help="Increment between seed variants.")
    parser.add_argument(
        "--output-prefix",
        default="p7-5-2-fullbody-turnaround",
        help="Filename prefix placed before the automatic timestamp and seed suffixes.",
    )
    args = parser.parse_args()
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

    run_timestamp = datetime.now().astimezone().strftime(TIMESTAMP_FORMAT)
    first_seed = BASE_SEED + args.seed_offset
    reference_images = [Image.open(path).convert("RGB") for path in REFERENCES]
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        for view in args.views:
            prompt = build_prompt(view)
            output = ROOT / f"{args.output_prefix}-{view}-{run_timestamp}-seed-{seed}-candidate.png"
            report = ROOT / f"{args.output_prefix}-{view}-{run_timestamp}-seed-{seed}-review.json"
            started = time.monotonic()
            image = pipe(
                image=reference_images,
                prompt=prompt,
                width=IMAGE_WIDTH,
                height=IMAGE_HEIGHT,
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
                        "output": output.name,
                        "view": view,
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
                        "model": MODEL_ID,
                        "image_size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                        "elapsed_seconds": elapsed,
                        "decision": "Experiment only; review body proportion, outfit continuity, direction, and face identity before approval.",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            print(f"[{batch_index + 1}/{args.seed_count}] {view}: {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

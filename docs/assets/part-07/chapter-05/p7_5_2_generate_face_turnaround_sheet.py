#!/usr/bin/env python3
"""Generate one face turnaround sheet from the approved frontal reference."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
FRONT = ROOT / "p7-5-2-face-front-with-hair-v3.png"
OUTPUT = ROOT / "p7-5-2-face-turnaround-sheet-v4-candidate.png"
REPORT = ROOT / "p7-5-2-face-turnaround-sheet-v4-review.json"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
HEAD_INPUT_BOTTOM = 720
SHEET_SIZE = 1024
VIEW_RULES = {
    "front": "front view at 0 degrees, with the nose centered and both eyes equally visible",
    "right_front_quarter": "45-degree right-facing view, with the nose pointing diagonally toward the sheet's right edge, the near eye fully visible, and the far eye half visible",
    "profile_right": "90-degree right-facing profile, with the nose pointing directly toward the sheet's right edge, one near eye visible in side view, and the far eye hidden",
    "rear": "180-degree rear view, facing away from the camera, with no nose or eyes visible",
}


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
        f"Panel directions: {view_list}. Use one distinct view per panel."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(VIEW_RULES),
        default=("front", "profile_right"),
        help="Face views to include in reading order; defaults to front and right profile for review.",
    )
    parser.add_argument(
        "--seed-offset",
        type=int,
        default=0,
        help="Add an offset to the turnaround-sheet seed.",
    )
    args = parser.parse_args()
    if len(args.views) > 4:
        raise ValueError("A turnaround sheet accepts at most four views")
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
    seed = 62370 + args.seed_offset
    prompt = build_prompt(tuple(args.views))
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
    sheet.save(OUTPUT)
    elapsed = round(time.monotonic() - started, 2)
    REPORT.write_text(
        json.dumps(
            {
                "status": "review_required",
                "output": OUTPUT.name,
                "seed": seed,
                "seed_offset": args.seed_offset,
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
    print(f"{elapsed:.2f}s -> {OUTPUT}")


if __name__ == "__main__":
    main()

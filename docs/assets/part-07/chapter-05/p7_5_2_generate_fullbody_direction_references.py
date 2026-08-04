#!/usr/bin/env python3
"""Generate directional full-body candidates from an approved front body and face views."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
FRONT_BODY = ROOT / "p7-5-2-fullbody-front-reference.png"
VIEW_SPECS = {
    "left_front_quarter": (ROOT / "p7-5-2-face-left-front-quarter-v1.png", 62411),
    "right_front_quarter": (ROOT / "p7-5-2-face-right-front-quarter-v1.png", 62412),
    "profile_left": (ROOT / "p7-5-2-face-profile-left-v1.png", 62403),
    "profile_right": (ROOT / "p7-5-2-face-profile-right-v1.png", 62404),
    "rear": (ROOT / "p7-5-2-face-rear-v1.png", 62405),
}
COMMON_PROMPT = (
    "Full-body reference of the same woman on an off-white studio background. "
    "Use one frontal full-body reference for proportion, outfit, and bag continuity, and one directional face reference for head continuity."
)
COMMON_CONSTRAINTS = "Neutral standing pose, complete from hair to soles. No extra person, text, or border."
VIEW_RULES = {
    "left_front_quarter": (
        "Show the shoulders and torso in a left-front-quarter view. Keep hips, knees, and feet facing forward. "
        "Keep exactly one navy crossbody bag with one diagonal strap."
    ),
    "right_front_quarter": (
        "Show the shoulders and torso in a right-front-quarter view. Keep hips, knees, and feet facing forward. "
        "Keep exactly one navy crossbody bag with one diagonal strap."
    ),
    "profile_left": (
        "She faces image-left in a strict side profile. Show exactly one navy crossbody bag clearly at the image-right rear hip, "
        "with its complete body visible behind her torso and one diagonal shoulder strap."
    ),
    "profile_right": (
        "She faces image-right in a strict side profile. Show one diagonal crossbody shoulder strap over the visible shoulder and chest, "
        "but hide the navy bag body completely behind her torso: no bag, bag silhouette, or pouch may be visible at either hip."
    ),
    "rear": (
        "She faces directly away from the viewer. Keep the crossbody bag on the image-left hip. "
        "The strap must run from the image-right shoulder diagonally across her back to that image-left hip; do not mirror this diagonal."
    ),
}


def build_prompt(view: str) -> str:
    return f"{COMMON_PROMPT} {VIEW_RULES[view]} {COMMON_CONSTRAINTS}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--views", nargs="+", choices=VIEW_SPECS, required=True)
    parser.add_argument(
        "--reference-orders",
        nargs="+",
        choices=["body-first", "face-first"],
        default=["body-first", "face-first"],
        help="Reference orders to render for every requested direction.",
    )
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    selected_views = args.views
    all_references = [FRONT_BODY, *(VIEW_SPECS[view][0] for view in selected_views)]
    if missing := [path.name for path in all_references if not path.is_file()]:
        raise FileNotFoundError(", ".join(missing))

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    runs = []
    for view in selected_views:
        face, seed = VIEW_SPECS[view]
        for reference_order in args.reference_orders:
            if reference_order == "face-first":
                references = [face, FRONT_BODY]
                output = ROOT / f"p7-5-2-fullbody-reference-v2-{view}-candidate-face-first.png"
            else:
                references = [FRONT_BODY, face]
                output = ROOT / f"p7-5-2-fullbody-reference-v2-{view}-candidate-body-first.png"
            started = time.monotonic()
            prompt = build_prompt(view)
            image = pipe(
                image=[Image.open(path).convert("RGB") for path in references],
                prompt=prompt,
                width=768,
                height=1280,
                num_inference_steps=12,
                guidance_scale=1.0,
                generator=torch.Generator(device="cpu").manual_seed(seed),
                max_sequence_length=256,
            ).images[0]
            image.save(output)
            runs.append({
                "view": view,
                "reference_order": reference_order,
                "references": [path.name for path in references],
                "output": output.name,
                "seed": seed,
                "prompt": prompt,
                "elapsed_seconds": round(time.monotonic() - started, 2),
            })
    report = ROOT / "p7-5-2-fullbody-reference-v2-review.json"
    report.write_text(
        json.dumps(
            {
                "status": "review_required",
                "requested_views": selected_views,
                "reference_orders": args.reference_orders,
                "runs": runs,
                "model": MODEL_ID,
                "decision": "Candidate only; human review is required before it becomes a full-body reference.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

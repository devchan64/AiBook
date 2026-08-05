#!/usr/bin/env python3
"""Generate head-and-neck rotation candidates from one approved frontal face."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
FRONT = ROOT / "p7-5-2-face-front-v2.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
REPORT = ROOT / "p7-5-2-face-rotation-from-front-v2-review.json"
COMMON_PROMPT = (
    "Close head-and-neck rotation reference of the same woman as the frontal reference, on off-white. "
    "Her head fills the frame from hair top to the base of the neck; only a narrow band of charcoal-gray crew-neck shirt and its round neckline may appear below the neck. "
    "Shoulders, collarbones, jacket, and full torso are outside the frame. "
    "Keep the frontal reference's side-parted jaw-length bob and face shape as identity priority: broad flat cheekbones, "
    "slightly soft full cheeks, and a smooth taper into the jaw."
)
COMMON_CONSTRAINTS = "Calm neutral expression. No accessory, text, or border."
VIEW_SPECS = {
    "left_front_quarter": ("left-front-quarter", 62350),
    "right_front_quarter": ("right-front-quarter", 62351),
    "profile_left": ("profile-left", 62352),
    "profile_right": ("profile-right", 62353),
    "rear_hair": ("rear-hair", 62356),
}
VIEW_RULES = {
    "left_front_quarter": "Show her head in a left-front-quarter view; the far eye is narrower.",
    "right_front_quarter": "Show her head in a right-front-quarter view; the far eye is narrower.",
    "profile_left": "Face viewer-left in strict profile with one visible eye and ear.",
    "profile_right": "Face viewer-right in strict profile with one visible eye and ear.",
    "rear_hair": (
        "Use a true 180-degree rear camera view: the camera is directly behind her head, and the back of the centered bob and nape face the viewer. "
        "Keep the head and neck aligned straight away from the camera, with no sideways turn, profile contour, or three-quarter angle. "
        "Show only the back hair mass and nape; the bob fully covers both temples and all front hair. "
        "No eye, eyebrow, ear, nose, lips, chin profile, cheek, face skin, front hairline, or fringe is visible."
    ),
}


def build_prompt(view_id: str) -> str:
    return f"{COMMON_PROMPT} {VIEW_RULES[view_id]} {COMMON_CONSTRAINTS}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=VIEW_SPECS,
        default=tuple(VIEW_SPECS),
        help="Directional face views to generate. Omit to generate every rotation from the same frontal anchor in one loaded pipeline.",
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
    face = Image.open(FRONT).convert("RGB")
    runs = []
    for view_id in args.views:
        name, seed = VIEW_SPECS[view_id]
        started = time.monotonic()
        prompt = build_prompt(view_id)
        output = ROOT / f"p7-5-2-face-rotation-v2-{name}-candidate.png"
        image = pipe(
            image=[face],
            prompt=prompt,
            width=768,
            height=768,
            num_inference_steps=12,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(seed),
            max_sequence_length=256,
        ).images[0]
        image.save(output)
        runs.append({
            "view_id": view_id,
            "output": output.name,
            "seed": seed,
            "prompt": prompt,
            "elapsed_seconds": round(time.monotonic() - started, 2),
        })

    REPORT.write_text(
        json.dumps(
            {
                "status": "review_required",
                "purpose": "Create compact-prompt directional face candidates from the approved frontal-face reference.",
                "input": FRONT.name,
                "requested_views": args.views,
                "shared_pipeline": "All requested rotations reuse one loaded pipeline and the same frontal anchor; the frontal anchor itself is not regenerated.",
                "model": MODEL_ID,
                "runs": runs,
                "decision": "Review each view before replacing a directional reference.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

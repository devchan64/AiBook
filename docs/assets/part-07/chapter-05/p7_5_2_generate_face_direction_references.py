#!/usr/bin/env python3
"""Generate head-and-neck rotation candidates from the current frontal-face candidate."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
FRONT = ROOT / "p7-5-2-face-front-no-accessory-v3-candidate.png"
CROPPED_TOP = ROOT / "p7-5-2-prop-reference-v2-gray-cropped-top.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
REPORT = ROOT / "p7-5-2-face-rotation-from-front-v2-review.json"
COMMON_PROMPT = (
    "Head-and-neck rotation reference of the same woman on off-white. "
    "Use the frontal face reference for identity and hair; use the gray cropped-top reference only for a narrow charcoal-gray crew-neckline arc. "
    "Keep broad low-set cheekbones and slight cheek fullness. "
    "A tight crop runs from hair top through the lower neck, with the neckline arc touching the bottom edge."
)
COMMON_CONSTRAINTS = "Neutral expression."
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
    "profile_left": "Face viewer-left in strict profile with one visible eye, one iris, and one ear.",
    "profile_right": "Face viewer-right in strict profile with one visible eye, one iris, and one ear.",
    "rear_hair": (
        "Use a true 180-degree rear camera view: the camera is directly behind her head, and the back of the centered bob and nape face the viewer. "
        "Keep the head and neck aligned straight away from the camera. "
        "The visible content is the centered back hair mass and nape, with the bob covering both temples; a small ear edge may remain visible."
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
    if missing := [path.name for path in (FRONT, CROPPED_TOP) if not path.is_file()]:
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
    face = Image.open(FRONT).convert("RGB")
    cropped_top = Image.open(CROPPED_TOP).convert("RGB")
    runs = []
    for view_id in args.views:
        name, seed = VIEW_SPECS[view_id]
        started = time.monotonic()
        prompt = build_prompt(view_id)
        output = ROOT / f"p7-5-2-face-rotation-v2-{name}-candidate.png"
        image = pipe(
            image=[face, cropped_top],
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
                "purpose": "Create compact-prompt directional face candidates from the current frontal-face candidate.",
                "inputs": [FRONT.name, CROPPED_TOP.name],
                "requested_views": args.views,
                "shared_pipeline": "All requested rotations reuse one loaded pipeline, the same frontal-face candidate, and the same cropped-top prop reference; the frontal candidate itself is not regenerated in this script.",
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

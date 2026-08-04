#!/usr/bin/env python3
"""Generate full-body reference candidates from the approved front body and face views."""

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
FRONT_FACE = ROOT / "p7-5-2-face-front-v2.png"
PROPS = [
    ROOT / "p7-5-2-prop-reference-v2-jacket.png",
    ROOT / "p7-5-2-prop-reference-v2-trousers.png",
    ROOT / "p7-5-2-prop-reference-v2-shoes.png",
    ROOT / "p7-5-2-prop-reference-v2-crossbody-bag.png",
]
VIEWS = {
    "front": (FRONT_FACE, 62400, "Face, shoulders, torso, hips, knees, feet, and gaze face forward."),
    "left_front_quarter": (ROOT / "p7-5-2-face-left-front-quarter-v1.png", 62401, "Turn the complete body 50 degrees toward viewer-left."),
    "right_front_quarter": (ROOT / "p7-5-2-face-right-front-quarter-v1.png", 62402, "Turn the complete body 50 degrees toward viewer-right."),
    "profile_left": (ROOT / "p7-5-2-face-profile-left-v1.png", 62403, "Turn the complete body to a strict viewer-left profile."),
    "profile_right": (ROOT / "p7-5-2-face-profile-right-v1.png", 62404, "Turn the complete body to a strict viewer-right profile."),
    "rear": (ROOT / "p7-5-2-face-rear-v1.png", 62405, "Turn the complete body directly away from the viewer."),
}


def build_prompt(view: str, direction: str) -> str:
    if view == "front":
        return (
            "Full-body front reference of the same woman on an off-white studio background. "
            "Use the face and prop references for her identity, cropped white utility jacket, teal wide-leg trousers, "
            "white sneakers, and navy crossbody bag. Show the complete body from hair to soles. "
            "Keep a neutral standing pose. No extra person, text, or border."
        )
    return (
        "Full-body rotation reference of the same woman on an off-white studio background. "
        "Reference 1 defines her body, clothing, proportions, and bag; reference 2 defines her head and hair at this view. "
        f"{direction} Keep head and body direction matched, with a neutral standing pose and the complete body from hair to soles. "
        "No extra person, text, or border."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", choices=VIEWS, required=True)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    face, seed, direction = VIEWS[args.view]
    references = [FRONT_FACE, *PROPS] if args.view == "front" else [FRONT_BODY, face]
    if missing := [path.name for path in references if not path.is_file()]:
        raise FileNotFoundError(", ".join(missing))

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    started = time.monotonic()
    prompt = build_prompt(args.view, direction)
    output = ROOT / f"p7-5-2-fullbody-reference-v2-{args.view}-candidate.png"
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
    report = ROOT / "p7-5-2-fullbody-reference-v2-review.json"
    report.write_text(
        json.dumps(
            {
                "status": "review_required",
                "view": args.view,
                "references": [path.name for path in references],
                "output": output.name,
                "model": MODEL_ID,
                "seed": seed,
                "prompt": prompt,
                "elapsed_seconds": round(time.monotonic() - started, 2),
                "decision": "Candidate only; human review is required before it becomes a full-body reference.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

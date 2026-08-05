#!/usr/bin/env python3
"""Generate direct directional full-body candidates from approved references."""

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
BASE_OUTFIT_COMPONENTS = [
    ROOT / "p7-5-2-outfit-crop-top-waist-reference.png",
    ROOT / "p7-5-2-prop-reference-v2-trousers.png",
    ROOT / "p7-5-2-prop-reference-v2-shoes.png",
]
VIEW_SPECS = {
    "left_front_quarter": (ROOT / "p7-5-2-face-left-front-quarter-v3.png", 62411),
    "right_front_quarter": (ROOT / "p7-5-2-face-right-front-quarter-v3.png", 62412),
    "profile_left": (ROOT / "p7-5-2-face-profile-left-v3.png", 62403),
    "profile_right": (ROOT / "p7-5-2-face-profile-right-v3.png", 62404),
    "rear": (ROOT / "p7-5-2-face-rear-v3.png", 62405),
}
PROPORTION_CONTRACT = (
    "Match the frontal full-body reference at approximately 7.5 head heights: keep the head length, shoulder width, "
    "torso length, natural waist, hip line, crotch level, knee level, lower-leg length, foot scale, and full hair-to-sole framing consistent."
)
DIRECTION_RULES = {
    "left_front_quarter": "Full-body 35-degree left-front three-quarter view; face, chest, pelvis, knees, and feet turn together toward image-left.",
    "right_front_quarter": "Full-body 35-degree right-front three-quarter view; face, chest, pelvis, knees, and feet turn together toward image-right.",
    "profile_left": "Full-body strict left side profile; head, torso, hips, knees, and feet face image-left.",
    "profile_right": "Full-body strict right side profile; head, torso, hips, knees, and feet face image-right.",
    "rear": "Full-body rear view; head, shoulders, torso, hips, knees, and feet face directly away from the viewer.",
}
STYLE_AND_SCALE = "Same woman, neutral upright pose, full body from hair to soles, off-white studio background, clean ink outlines and watercolor fills. Match the front body's 7.5-head scale."
PROFILE_OCCLUSION = "Show one near-side arm along the torso; the far arm is fully hidden behind the torso."
QUARTER_DEPTH = "Near shoulder, hip, arm, and leg are closer; far shoulder, hip, arm, and leg recede behind the body."
OUTFIT_CONTRACT = "Keep the charcoal-gray micro-crop top, bare-midriff gap, deep teal-blue wide-leg trousers, and white lace-up low-top sneakers."
VIEW_STAGES = {
    "left_front_quarter": ("orient", "depth", "outfit"),
    "right_front_quarter": ("orient", "depth", "outfit"),
    "profile_left": ("orient", "outfit"),
    "profile_right": ("orient", "outfit"),
    "rear": ("orient",),
}


def output_for(stage: str, view: str) -> Path:
    return ROOT / f"p7-5-2-fullbody-v4-{view}-{stage}-candidate.png"


def prompt_for(stage: str, view: str) -> str:
    direction = DIRECTION_RULES[view]
    if stage == "orient":
        extra = PROFILE_OCCLUSION if view.startswith("profile_") else ""
        return f"{direction} {extra} {STYLE_AND_SCALE}"
    if stage == "depth":
        return f"{direction} {QUARTER_DEPTH} Preserve the completed identity and neutral pose."
    extra = PROFILE_OCCLUSION if view.startswith("profile_") else QUARTER_DEPTH
    return f"{direction} {extra} {OUTFIT_CONTRACT} Preserve the completed body rotation and scale."


def prompt_word_count(text: str) -> int:
    return len(text.split())


def references_for(stage: str, view: str) -> list[Path]:
    face, _ = VIEW_SPECS[view]
    if stage == "orient":
        return [FRONT_BODY, face]
    if stage == "depth":
        return [output_for("orient", view), face]
    previous = "depth" if "depth" in VIEW_STAGES[view] else "orient"
    return [output_for(previous, view), face, *BASE_OUTFIT_COMPONENTS]


def render(
    pipe: Flux2KleinPipeline,
    *,
    stage: str,
    view: str,
    seed: int,
) -> dict[str, object]:
    references = references_for(stage, view)
    rendered_prompt = prompt_for(stage, view)
    started = time.monotonic()
    image = pipe(
        image=[Image.open(path).convert("RGB") for path in references],
        prompt=rendered_prompt,
        width=768,
        height=1280,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(seed),
        max_sequence_length=256,
    ).images[0]
    output = output_for(stage, view)
    image.save(output)
    return {
        "stage": stage,
        "references": [path.name for path in references],
        "output": output.name,
        "seed": seed,
        "prompt": rendered_prompt,
        "prompt_word_count": prompt_word_count(rendered_prompt),
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--views", nargs="+", choices=VIEW_SPECS, required=True)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    required = [FRONT_BODY, *BASE_OUTFIT_COMPONENTS, *(VIEW_SPECS[view][0] for view in args.views)]
    if missing := [path.name for path in required if not path.is_file()]:
        raise FileNotFoundError(", ".join(missing))

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    runs = []
    for view in args.views:
        _, seed = VIEW_SPECS[view]
        for offset, stage in enumerate(VIEW_STAGES[view]):
            run = render(pipe, stage=stage, view=view, seed=seed + offset * 1000)
            run["view"] = view
            runs.append(run)

    report = ROOT / "p7-5-2-fullbody-direction-v13-review.json"
    report.write_text(
        json.dumps(
            {
                "status": "review_required",
                "requested_views": args.views,
                "view_stages": {view: VIEW_STAGES[view] for view in args.views},
                "branching": {
                    "rear": "One orientation pass from the front body and rear face.",
                    "profiles": "Orientation, then outfit refinement without reintroducing the frontal body.",
                    "front_quarters": "Orientation, depth refinement, then outfit refinement without reintroducing the frontal body.",
                },
                "proportion_contract": PROPORTION_CONTRACT,
                "review_focus": "Compare every final output with the approved front body for 7.5-head height, shoulder, waist, hip, knee, foot, and full-frame consistency.",
                "model": MODEL_ID,
                "runs": runs,
                "decision": "Only each view's final stage is a reference candidate; human review is required before it becomes a reference asset.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

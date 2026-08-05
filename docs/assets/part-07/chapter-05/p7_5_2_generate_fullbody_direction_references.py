#!/usr/bin/env python3
"""Generate directional full-body candidates through one fixed multi-stage sequence."""

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
ROTATION_COMMON_PROMPT = (
    "Rotated full-body reference of the same woman on an off-white studio background. "
    "Use the frontal full-body reference as the complete body anchor for identity, 7.5-head-height proportion, pose, clothing silhouette, and full hair-to-sole framing. "
    "Use the directional face reference only for head direction, facial identity, and hair orientation. "
    "Render the same neutral standing full body from hair to soles with clean ink outlines, watercolor fills, and flat illustrated rendering."
)
PROPORTION_COMMON_PROMPT = (
    "Proportion-calibrated full-body directional reference of the same woman on an off-white studio background. "
    "Use the generated full-body reference for identity, body direction, and pose. "
    "Use the frontal full-body reference to match its 165 cm and 55 kg figure. "
    f"{PROPORTION_CONTRACT} "
    "Do not change the body direction or pose."
)
OUTFIT_COMMON_PROMPT = (
    "Outfit-unified full-body directional reference of the same woman on an off-white studio background. "
    "Use the proportion-calibrated full-body reference for identity, body direction, pose, and body proportions. "
    "Use the frontal full-body reference for overall proportion. Use the approved crop-top-waist relation, trousers, and shoes references "
    "for the complete outfit and garment construction. Render a charcoal-gray regular-fit short-sleeve micro-crop crew-neck top, "
    "a visible bare-midriff gap, deep teal-blue high-waisted wide-leg trousers, and matching white lace-up low-top sneakers. "
    f"{PROPORTION_CONTRACT} "
    "Keep the body direction and neutral standing pose, complete from hair to soles."
)
COMMON_CONSTRAINTS = "No extra person, text, or border."
FOOTWEAR_CONTRACT = (
    "Both feet are fully visible in the matching pair of lace-up white low-top sneakers from the shoe reference."
)
DIRECTION_RULES = {
    "left_front_quarter": "Show head, shoulders, torso, hips, knees, and feet together in a left-front-three-quarter view.",
    "right_front_quarter": "Show head, shoulders, torso, hips, knees, and feet together in a right-front-three-quarter view.",
    "profile_left": "She faces image-left in a strict full-body side profile; head, torso, hips, knees, and feet all face image-left.",
    "profile_right": "She faces image-right in a strict full-body side profile; head, torso, hips, knees, and feet all face image-right.",
    "rear": "She faces directly away from the viewer; head, shoulders, torso, hips, knees, and feet all show the rear view.",
}


def stage_output(stage: str, view: str) -> Path:
    names = {
        "rotation": f"p7-5-2-fullbody-rotation-v1-{view}-candidate.png",
        "proportion": f"p7-5-2-fullbody-proportion-v3-{view}-candidate.png",
        "outfit": f"p7-5-2-fullbody-reference-v10-{view}-candidate.png",
    }
    return ROOT / names[stage]


def prompt_for(stage: str, view: str) -> str:
    if stage == "rotation":
        return f"{ROTATION_COMMON_PROMPT} {DIRECTION_RULES[view]} {COMMON_CONSTRAINTS}"
    if stage == "proportion":
        return f"{PROPORTION_COMMON_PROMPT} {DIRECTION_RULES[view]} {COMMON_CONSTRAINTS}"
    return f"{OUTFIT_COMMON_PROMPT} {DIRECTION_RULES[view]} {FOOTWEAR_CONTRACT} {COMMON_CONSTRAINTS}"


def stage_references(stage: str, view: str) -> list[Path]:
    face, _ = VIEW_SPECS[view]
    if stage == "rotation":
        return [FRONT_BODY, face]
    if stage == "proportion":
        return [stage_output("rotation", view), FRONT_BODY]
    return [stage_output("proportion", view), FRONT_BODY, *BASE_OUTFIT_COMPONENTS]


def render(
    pipe: Flux2KleinPipeline,
    *,
    stage: str,
    view: str,
    seed: int,
) -> dict[str, object]:
    references = stage_references(stage, view)
    started = time.monotonic()
    image = pipe(
        image=[Image.open(path).convert("RGB") for path in references],
        prompt=prompt_for(stage, view),
        width=768,
        height=1280,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(seed),
        max_sequence_length=256,
    ).images[0]
    output = stage_output(stage, view)
    image.save(output)
    return {
        "stage": stage,
        "references": [path.name for path in references],
        "output": output.name,
        "seed": seed,
        "prompt": prompt_for(stage, view),
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
        for stage, stage_seed in (
            ("rotation", seed),
            ("proportion", seed + 1000),
            ("outfit", seed + 2000),
        ):
            run = render(pipe, stage=stage, view=view, seed=stage_seed)
            run["view"] = view
            runs.append(run)

    report = ROOT / "p7-5-2-fullbody-direction-v10-review.json"
    report.write_text(
        json.dumps(
            {
                "status": "review_required",
                "requested_views": args.views,
                "sequence": [
                    "front_body_and_directional_face_to_rotated_body",
                    "rotated_body_to_proportion_calibrated",
                    "proportion_calibrated_to_outfit_unified",
                ],
                "proportion_contract": PROPORTION_CONTRACT,
                "review_focus": "Compare every final output with the approved front body for 7.5-head height, shoulder, waist, hip, knee, foot, and full-frame consistency.",
                "model": MODEL_ID,
                "runs": runs,
                "decision": "All intermediates and final outputs are candidates; human review is required before a final output becomes a reference asset.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

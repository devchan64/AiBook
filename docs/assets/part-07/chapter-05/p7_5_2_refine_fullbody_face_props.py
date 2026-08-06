#!/usr/bin/env python3
"""Refine approved full-body references with frontal-face identity and selected props."""

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
FACE_IDENTITY = ROOT / "p7-5-2-face-turnaround-codeformer-front-2x.png"
BODY_REFERENCES = {
    "front": ROOT / "p7-5-2-fullbody-front-reference.png",
    "front_quarter": ROOT / "p7-5-2-fullbody-front-quarter-reference.png",
    "profile": ROOT / "p7-5-2-fullbody-profile-reference.png",
    "rear": ROOT / "p7-5-2-fullbody-rear-reference.png",
}
LAYERED_OUTFIT_REFERENCE_BY_VIEW = {
    "front": ROOT / "p7-5-2-prop-reference-v2-jacket-crop-top-front.png",
    "front_quarter": ROOT / "p7-5-2-prop-reference-v2-jacket-crop-top-front.png",
    "profile": ROOT / "p7-5-2-prop-reference-v2-jacket-crop-top-front.png",
    "rear": ROOT / "p7-5-2-prop-reference-v2-jacket-crop-top-rear.png",
}
COMPLETE_OUTFIT_REFERENCE_BY_VIEW = {
    "front": ROOT / "p7-5-2-prop-reference-v2-complete-outfit-front-hip.png",
    "front_quarter": ROOT / "p7-5-2-prop-reference-v2-complete-outfit-front-hip.png",
    "profile": ROOT / "p7-5-2-prop-reference-v2-complete-outfit-front-hip.png",
    "rear": ROOT / "p7-5-2-prop-reference-v2-complete-outfit-rear-hip.png",
}
PROPS = {
    "layered_jacket_crop_top": {
        "instruction": "Add the supplied white cropped utility-jacket outfit layer.",
    },
    "crossbody_bag": {
        "path": ROOT / "p7-5-2-prop-reference-v2-crossbody-bag.png",
        "instruction": "Add the approved deep-navy canvas crossbody bag and strap.",
    },
    "complete_outfit": {
        "instruction": "Apply the supplied complete outfit reference, including its jacket, crop top, trousers, and crossbody bag placement.",
    },
}
VIEW_RULES = {
    "front": "Keep a front view facing the camera.",
    "front_quarter": "Keep a front three-quarter view with face, torso, pelvis, knees, and feet turned together.",
    "profile": "Keep a side profile with one near arm visible and the far arm hidden behind the torso.",
    "rear": "Keep a rear view facing away; do not show a frontal face.",
}
LAYERED_OUTFIT_VIEW_RULES = {
    "profile": "Profile: keep the white cropped jacket as the outer layer over the gray crop top; show its collar, long sleeve, cropped hem, and side-back panel.",
    "rear": "Rear: use the supplied rear outfit reference as the construction anchor; keep its uninterrupted white jacket back panel, long sleeves, cropped hem, and a clear bare-skin midriff band above the trousers. No inner top is visible from the rear.",
}
BAG_VIEW_RULES = {
    "front": "Front: hang the bag side-on beside the wearer's outer-left trouser seam, its top at the waistband; show one continuous taut strap from the outer wearer's-right shoulder diagonally across the chest into the bag's upper inner attachment.",
    "front_quarter": "Front three-quarter: place the bag at the outer wearer's-left hip, its top at the waistband, below the ribs and clear of the front thigh.",
    "profile": "Profile: keep the bag at the outer wearer's-left hip with its top at the waistband, below the ribs, and keep its strap behind the jacket.",
    "rear": "Rear: run the strap across the jacket back from the wearer's right shoulder to the bag at the outer wearer's-left hip, with its top at the waistband and clear of the back center and ribs.",
}
COMPLETE_OUTFIT_VIEW_RULES = {
    "front": "Front: retain the bag side-on beside the wearer's outer-left trouser seam, its top aligned to the waistband, and one continuous taut strap from the outer wearer's-right shoulder diagonally across the chest into the bag's upper inner attachment.",
    "front_quarter": "Front three-quarter: retain the bag at the outer wearer's-left hip, its top aligned to the waistband, below the ribs and clear of the front thigh.",
    "profile": "Profile: retain the bag at the outer wearer's-left rearward hip, its top aligned to the waistband, with the strap behind the jacket.",
    "rear": "Rear: retain the bag at the outer wearer's-left hip, its top aligned to the waistband, with its long strap across the jacket back from the wearer's right shoulder.",
}
IMAGE_WIDTH = 768
IMAGE_HEIGHT = 1152


def prompt_word_count(text: str) -> int:
    return len(text.split())


def prop_reference_path(prop_id: str, view: str) -> Path:
    if prop_id == "complete_outfit":
        return COMPLETE_OUTFIT_REFERENCE_BY_VIEW[view]
    if prop_id == "layered_jacket_crop_top":
        return LAYERED_OUTFIT_REFERENCE_BY_VIEW[view]
    return PROPS[prop_id]["path"]


def build_prompt(view: str, prop_ids: tuple[str, ...]) -> str:
    prop_instructions = " ".join(PROPS[prop_id]["instruction"] for prop_id in prop_ids)
    if "complete_outfit" in prop_ids:
        prop_instructions = PROPS["complete_outfit"]["instruction"]
    elif "layered_jacket_crop_top" in prop_ids and view == "front":
        prop_instructions = (
            "Add the supplied layered white cropped utility jacket worn open over the charcoal-gray crop top."
        )
    base_clothing = "deep teal-blue trousers and white low-top sneakers"
    if not {"layered_jacket_crop_top", "complete_outfit"}.intersection(prop_ids):
        base_clothing = f"charcoal-gray crop top, {base_clothing}"
    view_prop_rules = []
    if "layered_jacket_crop_top" in prop_ids and view in LAYERED_OUTFIT_VIEW_RULES:
        view_prop_rules.append(LAYERED_OUTFIT_VIEW_RULES[view])
    if "crossbody_bag" in prop_ids and view in BAG_VIEW_RULES:
        view_prop_rules.append(BAG_VIEW_RULES[view])
    if "complete_outfit" in prop_ids:
        view_prop_rules.append(COMPLETE_OUTFIT_VIEW_RULES[view])
    return (
        "Refine the supplied full-body reference into one full-body studio image of the same woman. "
        "Use the CodeFormer frontal face as the identity anchor for face, eyes, nose, skin tone, hairline, and petrol-teal bob whenever visible. "
        f"Keep the supplied full-body reference's upright pose, direction, hair-to-sole framing, and {base_clothing}. "
        f"{VIEW_RULES[view]} {prop_instructions} {' '.join(view_prop_rules)} "
        "One person, complete limbs, no text or labels."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(BODY_REFERENCES),
        default=tuple(BODY_REFERENCES),
        help="Approved full-body directions to refine as separate PNGs.",
    )
    parser.add_argument(
        "--props",
        nargs="+",
        choices=tuple(PROPS),
        default=("layered_jacket_crop_top", "crossbody_bag"),
        help="Approved props to add to each selected full-body direction.",
    )
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset applied to the first seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seed variants.")
    parser.add_argument("--seed-step", type=int, default=1, help="Increment between seed variants.")
    parser.add_argument(
        "--output-prefix",
        default="p7-5-2-fullbody-face-prop-refinement",
        help="Filename prefix placed before view, timestamp, and seed suffixes.",
    )
    args = parser.parse_args()
    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")

    reference_paths = [FACE_IDENTITY, *(BODY_REFERENCES[view] for view in args.views)]
    reference_paths.extend(
        prop_reference_path(prop_id, view)
        for view in args.views
        for prop_id in args.props
    )
    if missing := [path.name for path in reference_paths if not path.is_file()]:
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
    face_image = Image.open(FACE_IDENTITY).convert("RGB")
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        for view in args.views:
            prompt = build_prompt(view, tuple(args.props))
            output = ROOT / f"{args.output_prefix}-{view}-{run_timestamp}-seed-{seed}-candidate.png"
            report = ROOT / f"{args.output_prefix}-{view}-{run_timestamp}-seed-{seed}-review.json"
            started = time.monotonic()
            prop_paths = [prop_reference_path(prop_id, view) for prop_id in args.props]
            prop_images = [Image.open(path).convert("RGB") for path in prop_paths]
            with Image.open(BODY_REFERENCES[view]) as body_source:
                image = pipe(
                    image=[face_image, body_source.convert("RGB"), *prop_images],
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
                        "references": {
                            "face_identity": FACE_IDENTITY.name,
                            "body_composition": BODY_REFERENCES[view].name,
                            "props": [path.name for path in prop_paths],
                        },
                        "model": MODEL_ID,
                        "image_size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                        "elapsed_seconds": elapsed,
                        "decision": "Review face identity, body-direction preservation, prop geometry, and strap continuity before replacing the approved full-body reference.",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            print(f"[{batch_index + 1}/{args.seed_count}] {view}: {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

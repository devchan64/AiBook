#!/usr/bin/env python3
"""Refine approved full-body references, then restore visible face identity."""

from __future__ import annotations

import argparse
from datetime import datetime
import gc
import json
from pathlib import Path
import time
from uuid import uuid4

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
BASE_SEED = 62377
FACE_IDENTITY_SEED = 62294
TIMESTAMP_FORMAT = "%Y%m%dT%H%M%S%f%z"
FACE_IDENTITY_BY_VIEW = {
    "front": ROOT / "p7-5-2-face-turnaround-codeformer-front-2x.png",
    "front_quarter": ROOT / "p7-5-2-face-turnaround-codeformer-front-quarter-2x.png",
    "profile": ROOT / "p7-5-2-face-turnaround-codeformer-profile-2x.png",
    # The rear panel anchors the back-of-head silhouette and neck line without introducing a face.
    "rear": ROOT / "p7-5-2-face-turnaround-codeformer-rear-2x.png",
}
FACE_FRONT_HAIR_DESCRIPTION = (
    "Deep petrol-teal, extremely voluminous jaw-length bob with medium-density hair."
)
# These four stable filenames are the only approved full-body composition inputs.
APPROVED_BODY_REFERENCES = {
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
FACE_FINAL_VIEW_RULES = {
    "front_quarter": (
        "For this three-quarter face, turn both pupils and the visible gaze toward the same side as the nose bridge "
        "and nose tip. Do not leave the eyes facing front while the nose is turned."
    ),
    "profile": (
        "For this profile forehead check, preserve the elongated forehead above the brow, a continuous unbroken hairline, "
        "and one controlled short fringe ending above the eyebrow. Do not expose a blank or receded forehead, split the "
        "fringe into extra bangs, or change the forehead-to-brow proportion."
    ),
}
LAYERED_OUTFIT_VIEW_RULES = {
    "profile": "Profile: keep the white cropped jacket as the outer layer over the gray crop top; show its collar, long sleeve, cropped hem, and side-back panel.",
    "rear": "Rear: use the supplied rear outfit reference as the construction anchor; keep its uninterrupted white jacket back panel, long sleeves, cropped hem, and a clear bare-skin midriff band above the trousers. No inner top is visible from the rear.",
}
BAG_VIEW_RULES = {
    "front": "Front: hang the bag side-on beside the wearer's outer-left trouser seam, its top at the waistband; show one continuous taut strap from the outer wearer's-right shoulder diagonally across the chest into the bag's upper inner attachment.",
    "front_quarter": "Front three-quarter: place the bag at the outer wearer's-left hip, its top at the waistband, below the ribs and clear of the front thigh.",
    "profile": "Profile: keep the bag at the outer wearer's-left hip with its top at the waistband, below the ribs, and keep its strap behind the jacket.",
    "rear": "Rear: retain long cuffed sleeves reaching the wrists. Show one continuous taut deep-navy canvas strap from the outer wearer's-right shoulder diagonally across the jacket back, exiting beyond the left waistband. At the outer left hip, show only a small deep-navy woven-fabric bag corner, mostly hidden behind the torso.",
}
COMPLETE_OUTFIT_VIEW_RULES = {
    "front": "Front: retain the bag side-on beside the wearer's outer-left trouser seam, its top aligned to the waistband, and one continuous taut strap from the outer wearer's-right shoulder diagonally across the chest into the bag's upper inner attachment.",
    "front_quarter": "Front three-quarter: retain the bag at the outer wearer's-left hip, its top aligned to the waistband, below the ribs and clear of the front thigh.",
    "profile": "Profile: render a visibly dominant white cropped utility-jacket body from collar to hem, including the side-back panel and one long cuffed sleeve. Show the charcoal-gray crop top only as a narrow inner layer at the open front. Keep the bag at the outer wearer's-left rearward hip, its top aligned to the waistband, with the strap behind the jacket.",
    "rear": "Rear: replace the upper garment with the supplied white cropped utility jacket: plain white back panel, long cuffed sleeves to the wrists, and bare-skin midriff below its hem; no gray inner top is visible. Show one continuous taut deep-navy canvas strap from the outer wearer's-right shoulder diagonally across the jacket back, exiting beyond the left waistband. At the outer left hip, show only a small deep-navy woven-fabric bag corner, mostly hidden behind the torso.",
}
IMAGE_WIDTH = 768
IMAGE_HEIGHT = 1152


def prompt_word_count(text: str) -> int:
    return len(text.split())


def resolve_body_references(assignments: list[str]) -> dict[str, Path]:
    """Return per-view composition inputs, defaulting to the approved stable set."""
    references = dict(APPROVED_BODY_REFERENCES)
    assigned_views: set[str] = set()
    for assignment in assignments:
        try:
            view, raw_path = assignment.split("=", maxsplit=1)
        except ValueError as exc:
            raise ValueError("--body-reference must use VIEW=PATH") from exc
        if view not in APPROVED_BODY_REFERENCES:
            raise ValueError(f"Unknown body-reference view: {view}")
        if view in assigned_views:
            raise ValueError(f"Duplicate body-reference view: {view}")
        path = Path(raw_path)
        references[view] = path if path.is_absolute() else ROOT / path
        assigned_views.add(view)
    return references


def unique_run_stem(prefix: str, view: str, run_id: str, seed: int) -> str:
    """Create an unused shared stem for PNG outputs and their review record."""
    base_stem = f"{prefix}-{view}-run-{run_id}-seed-{seed}"
    suffix = 1
    stem = base_stem
    while any(
        (ROOT / f"{stem}{extension}").exists()
        for extension in ("-candidate.png", "-outfit-stage.png", "-review.json")
    ):
        suffix += 1
        stem = f"{base_stem}-attempt-{suffix}"
    return stem


def prop_reference_paths(prop_id: str, view: str) -> tuple[Path, ...]:
    if prop_id == "complete_outfit":
        if view == "profile":
            # A side view needs both garment faces plus the approved front crop-length contract.
            return (
                COMPLETE_OUTFIT_REFERENCE_BY_VIEW["front"],
                COMPLETE_OUTFIT_REFERENCE_BY_VIEW["rear"],
                LAYERED_OUTFIT_REFERENCE_BY_VIEW["front"],
            )
        return (COMPLETE_OUTFIT_REFERENCE_BY_VIEW[view],)
    if prop_id == "layered_jacket_crop_top":
        return (LAYERED_OUTFIT_REFERENCE_BY_VIEW[view],)
    return (PROPS[prop_id]["path"],)


def build_outfit_prompt(view: str, prop_ids: tuple[str, ...]) -> str:
    if view == "profile" and "complete_outfit" in prop_ids:
        return (
            "Refine the supplied full-body reference into the same woman in a side-profile studio image. "
            "Preserve pose, hair-to-sole framing, dark teal trousers, and white low-top sneakers. "
            "Use the supplied front jacket-crop-top layer and front complete-outfit reference as the authoritative crop-length "
            "contract: the white jacket hem and charcoal-gray crop top end high above the trouser waistband, leaving the same "
            "narrow bare-midriff band seen in those front references. Do not lengthen either crop to the waistband, hip, or below "
            "the approved front cropped hem. From the supplied front and rear outfit references, render a white cropped utility "
            "jacket as the visible outer torso layer: jacket body from collar to cropped hem, side-back panel, and one long cuffed "
            "sleeve. Keep the charcoal-gray crop top as a narrow inner layer at the open front. Place the deep-navy bag at the "
            "outer left rearward hip with its strap behind the jacket. One person, complete limbs, no text or labels."
        )
    prop_instructions = " ".join(PROPS[prop_id]["instruction"] for prop_id in prop_ids)
    if "complete_outfit" in prop_ids:
        prop_instructions = PROPS["complete_outfit"]["instruction"]
    elif "layered_jacket_crop_top" in prop_ids and view == "front":
        prop_instructions = (
            "Add the supplied layered white cropped utility jacket worn open over the charcoal-gray crop top."
        )
    base_clothing = "dark teal trousers and white low-top sneakers"
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
        f"Keep the supplied full-body reference's upright pose, direction, hair-to-sole framing, and {base_clothing}. "
        f"{VIEW_RULES[view]} {prop_instructions} {' '.join(view_prop_rules)} "
        "One person, complete limbs, no text or labels."
    )


def build_identity_final_prompt(view: str) -> str:
    """Keep the outfit pass intact while applying the direction-matched identity input."""
    if view == "rear":
        return (
            "Use the supplied full-body image as the fixed composition, pose, clothing, bag, and full-body framing anchor. "
            "Restore only the back-of-head hair silhouette, nape hairline, hair color, and neck contour from the supplied "
            f"rear 2x identity reference. Keep the hair as {FACE_FRONT_HAIR_DESCRIPTION} "
            "Keep the rear view facing away; do not create a visible face, eyes, nose, or mouth. "
            "Keep the outfit, limbs, and camera unchanged. One person, no text or labels."
        )
    face_view_rule = FACE_FINAL_VIEW_RULES.get(view, "")
    return (
        "Use the supplied full-body image as the fixed composition, pose, clothing, bag, and full-body framing anchor. "
        "Restore only the visible face to match the supplied direction-matched identity reference: eyes, nose, skin tone, hairline, and "
        f"{FACE_FRONT_HAIR_DESCRIPTION} "
        f"{VIEW_RULES[view]} {face_view_rule} Keep the outfit, limbs, and camera unchanged. One person, no text or labels."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(APPROVED_BODY_REFERENCES),
        default=tuple(APPROVED_BODY_REFERENCES),
        help="Approved full-body directions to refine as separate PNGs.",
    )
    parser.add_argument(
        "--props",
        nargs="+",
        choices=tuple(PROPS),
        default=("complete_outfit",),
        help="Approved props to add to each selected full-body direction; defaults to the paired complete outfit references.",
    )
    parser.add_argument(
        "--body-reference",
        action="append",
        default=[],
        metavar="VIEW=PATH",
        help=(
            "Override one composition input with a PNG, for example "
            "--body-reference profile=p7-5-2-fullbody-profile-reference.png. "
            "Unspecified views use the approved stable references."
        ),
    )
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset applied to the first seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seed variants.")
    parser.add_argument("--seed-step", type=int, default=1, help="Increment between seed variants.")
    parser.add_argument(
        "--face-identity-seed",
        type=int,
        default=FACE_IDENTITY_SEED,
        help="Fixed seed for the final visible-face identity pass.",
    )
    parser.add_argument(
        "--output-prefix",
        default="p7-5-2-fullbody-face-prop-refinement",
        help="Filename prefix placed before view, run ID, and seed suffixes.",
    )
    parser.add_argument(
        "--run-id",
        help="Optional run identifier. An 8-character UUID fragment is generated when omitted.",
    )
    parser.add_argument(
        "--stage",
        choices=("all", "outfit", "face"),
        default="all",
        help="Run outfit only, face only from --intermediate, or both in one process.",
    )
    parser.add_argument(
        "--intermediate",
        type=Path,
        help="Outfit-stage PNG used by --stage face.",
    )
    args = parser.parse_args()
    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")
    if args.stage == "face" and args.intermediate is None:
        raise ValueError("--stage face requires --intermediate")
    body_references = resolve_body_references(args.body_reference)

    reference_paths = []
    if args.stage != "outfit":
        reference_paths.extend(FACE_IDENTITY_BY_VIEW[view] for view in args.views)
    if args.stage != "face":
        reference_paths.extend(body_references[view] for view in args.views)
        reference_paths.extend(
            path
            for view in args.views
            for prop_id in args.props
            for path in prop_reference_paths(prop_id, view)
        )
    if args.intermediate is not None:
        reference_paths.append(args.intermediate)
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
    run_id = args.run_id or uuid4().hex[:8]
    first_seed = BASE_SEED + args.seed_offset
    face_images = (
        {
            view: Image.open(FACE_IDENTITY_BY_VIEW[view]).convert("RGB")
            for view in args.views
        }
        if args.stage != "outfit"
        else {}
    )
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        for view in args.views:
            outfit_prompt = build_outfit_prompt(view, tuple(args.props))
            identity_prompt = build_identity_final_prompt(view)
            stem = unique_run_stem(args.output_prefix, view, run_id, seed)
            output = ROOT / f"{stem}-candidate.png"
            intermediate = ROOT / f"{stem}-outfit-stage.png"
            report = ROOT / f"{stem}-review.json"
            started = time.monotonic()
            prop_paths = [
                path
                for prop_id in args.props
                for path in prop_reference_paths(prop_id, view)
            ]
            if args.stage in ("all", "outfit"):
                prop_images = [Image.open(path).convert("RGB") for path in prop_paths]
                with Image.open(body_references[view]) as body_source:
                    outfit_image = pipe(
                        image=[body_source.convert("RGB"), *prop_images],
                        prompt=outfit_prompt,
                        width=IMAGE_WIDTH,
                        height=IMAGE_HEIGHT,
                        num_inference_steps=12,
                        guidance_scale=1.0,
                        generator=torch.Generator(device="cpu").manual_seed(seed),
                        max_sequence_length=256,
                    ).images[0]
                if args.stage == "outfit":
                    outfit_image.save(intermediate)
                    print(f"outfit-stage -> {intermediate}")
                    continue
            else:
                with Image.open(args.intermediate) as source:
                    outfit_image = source.convert("RGB")
            image = outfit_image
            if args.stage != "outfit":
                # The first pass is a full-resolution multi-reference edit on an 8GB GPU.
                # Release transient tensors before running the final face-only pass.
                gc.collect()
                torch.cuda.empty_cache()
                image = pipe(
                    image=[outfit_image, face_images[view]],
                    prompt=identity_prompt,
                    width=IMAGE_WIDTH,
                    height=IMAGE_HEIGHT,
                    num_inference_steps=12,
                    guidance_scale=1.0,
                    generator=torch.Generator(device="cpu").manual_seed(args.face_identity_seed),
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
                        "face_identity_seed": args.face_identity_seed,
                        "batch_index": batch_index,
                        "batch_size": args.seed_count,
                        "run_timestamp": run_timestamp,
                        "run_id": run_id,
                        "output_prefix": args.output_prefix,
                        "stages": {
                            "outfit": {
                                "prompt": outfit_prompt,
                                "prompt_word_count": prompt_word_count(outfit_prompt),
                            },
                            "identity_final": {
                                "prompt": identity_prompt,
                                "prompt_word_count": prompt_word_count(identity_prompt),
                                "seed": args.face_identity_seed,
                                "status": "generated_rear_head_identity" if view == "rear" else "generated_visible_face_identity",
                            },
                        },
                        "references": {
                            "identity_reference": FACE_IDENTITY_BY_VIEW[view].name,
                            "body_composition": body_references[view].name,
                            "props": [path.name for path in prop_paths],
                        },
                        "model": MODEL_ID,
                        "image_size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                        "elapsed_seconds": elapsed,
                        "decision": "Review outfit geometry before the final face pass, then review face identity, body direction, and strap continuity before replacing an approved full-body reference.",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            print(f"[{batch_index + 1}/{args.seed_count}] {view}: {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

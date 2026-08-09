#!/usr/bin/env python3
"""Refine approved full-body references in one face-sheet-guided pass."""

from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image
from p7_5_image_output_naming import candidate_stem, preview_callback


ROOT = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
SEED = 62294
STEPS = 3
IMAGE_WIDTH = 960
IMAGE_HEIGHT = 1440
STUDIO_BACKGROUND_RULE = "Use a plain white wall and a plain white studio floor."

# These six stable filenames are the only approved full-body composition inputs.
APPROVED_BODY_REFERENCES = {
    "front": ROOT / "p7-5-2-fullbody-front-reference.png",
    "front_quarter_left": ROOT / "p7-5-2-fullbody-front-quarter-left-reference.png",
    "front_quarter_right": ROOT / "p7-5-2-fullbody-front-quarter-right-reference.png",
    "profile_left": ROOT / "p7-5-2-fullbody-profile-left-reference.png",
    "profile_right": ROOT / "p7-5-2-fullbody-profile-right-reference.png",
    "rear": ROOT / "p7-5-2-fullbody-rear-reference.png",
}
LAYERED_OUTFIT_REFERENCE_BY_VIEW = {
    "front": ROOT / "p7-5-2-prop-reference-jacket-crop-top-front.png",
    "front_quarter_left": ROOT / "p7-5-2-prop-reference-jacket-crop-top-front.png",
    "front_quarter_right": ROOT / "p7-5-2-prop-reference-jacket-crop-top-front.png",
    "profile_left": ROOT / "p7-5-2-prop-reference-jacket-crop-top-front.png",
    "profile_right": ROOT / "p7-5-2-prop-reference-jacket-crop-top-front.png",
    "rear": ROOT / "p7-5-2-prop-reference-jacket-crop-top-rear.png",
}
COMPLETE_OUTFIT_REFERENCE_BY_VIEW = {
    "front": ROOT / "p7-5-2-prop-reference-complete-outfit-front-hip.png",
    "front_quarter_left": ROOT / "p7-5-2-prop-reference-complete-outfit-front-hip.png",
    "front_quarter_right": ROOT / "p7-5-2-prop-reference-complete-outfit-front-hip.png",
    "profile_left": ROOT / "p7-5-2-prop-reference-complete-outfit-front-hip.png",
    "profile_right": ROOT / "p7-5-2-prop-reference-complete-outfit-front-hip.png",
    "rear": ROOT / "p7-5-2-prop-reference-complete-outfit-rear-hip.png",
}
PROPS = {
    "layered_jacket_crop_top": {
        "instruction": "Add the supplied white cropped utility-jacket outfit layer.",
    },
    "crossbody_bag": {
        "path": ROOT / "p7-5-2-prop-reference-crossbody-bag.png",
        "instruction": "Add the approved deep-navy canvas crossbody bag and strap.",
    },
    "complete_outfit": {
        "instruction": "Apply the supplied complete outfit reference, including its jacket, crop top, trousers, and crossbody bag placement.",
    },
}
VIEW_RULES = {
    "front": "Keep a front view facing the camera.",
    "front_quarter_left": "Keep a left front three-quarter view with face, torso, pelvis, knees, and feet turned together.",
    "front_quarter_right": "Keep a right front three-quarter view with face, torso, pelvis, knees, and feet turned together.",
    "profile_left": "Keep a left-facing side profile with one near arm visible and the far arm hidden behind the torso.",
    "profile_right": "Keep a right-facing side profile with one near arm visible and the far arm hidden behind the torso.",
    "rear": "Keep a rear view facing away; do not show a frontal face.",
}
LAYERED_OUTFIT_VIEW_RULES = {
    "profile_left": "Profile: keep the white cropped jacket as the outer layer over the gray crop top; show its collar, long sleeve, cropped hem, and side-back panel.",
    "profile_right": "Profile: keep the white cropped jacket as the outer layer over the gray crop top; show its collar, long sleeve, cropped hem, and side-back panel.",
    "rear": "Rear: use the supplied rear outfit reference as the construction anchor; keep its uninterrupted white jacket back panel, long sleeves, cropped hem, and a clear bare-skin midriff band above the trousers. No inner top is visible from the rear.",
}
BAG_VIEW_RULES = {
    "front": "Front: hang the bag side-on beside the wearer's outer-left trouser seam, its top at the waistband; show one continuous taut strap from the outer wearer's-right shoulder diagonally across the chest into the bag's upper inner attachment.",
    "front_quarter_left": "Left front three-quarter: place the bag at the outer wearer's-left hip, its top at the waistband, below the ribs and clear of the front thigh. Show exactly one continuous taut deep-navy strap, fully visible on the exterior of the near-facing white jacket: start at the outer wearer's-right shoulder, cross the chest diagonally without a break or a second segment, and end at the bag's upper inner attachment. Keep the strap outside the jacket, never behind, inside, or detached from the bag.",
    "front_quarter_right": "Front three-quarter: place the bag at the outer wearer's-left hip, its top at the waistband, below the ribs and clear of the front thigh. Show one continuous taut deep-navy strap from the outer wearer's-right shoulder diagonally across the exterior of the white jacket into the bag's upper inner attachment; do not hide it behind or inside the jacket.",
    "profile_left": "Profile: keep the bag at the outer wearer's-left hip with its top at the waistband, below the ribs, and keep its strap behind the jacket.",
    "profile_right": "Profile: keep the bag at the outer wearer's-left hip with its top at the waistband, below the ribs, and keep its strap behind the jacket.",
    "rear": "Rear: retain long cuffed sleeves reaching the wrists. Show one continuous taut deep-navy canvas strap from the outer wearer's-right shoulder diagonally across the jacket back, exiting beyond the left waistband. At the outer left hip, show only a small deep-navy woven-fabric bag corner, mostly hidden behind the torso.",
}
COMPLETE_OUTFIT_VIEW_RULES = {
    "front": "Front: replace the visible charcoal top with the supplied very short white cropped utility jacket as the closed outer layer. Its white front panels cover the chest, with long cuffed sleeves reaching the wrists; the charcoal-gray crop top may appear only as a narrow band below the cropped hem. Retain the bag side-on beside the wearer's outer-left trouser seam, its top aligned to the waistband, and one continuous taut deep-navy strap from the outer wearer's-right shoulder diagonally across the white jacket into the bag's upper inner attachment.",
    "front_quarter_left": "Left front three-quarter: retain the bag at the outer wearer's-left hip, its top aligned to the waistband, below the ribs and clear of the front thigh. Show exactly one continuous taut deep-navy strap, fully visible on the exterior of the near-facing white jacket: start at the outer wearer's-right shoulder, cross the chest diagonally without a break or a second segment, and end at the bag's upper inner attachment. Keep the strap outside the jacket, never behind, inside, or detached from the bag.",
    "front_quarter_right": "Front three-quarter: retain the bag at the outer wearer's-left hip, its top aligned to the waistband, below the ribs and clear of the front thigh. Show one continuous taut deep-navy strap from the outer wearer's-right shoulder diagonally across the exterior of the white jacket into the bag's upper inner attachment; do not hide it behind or inside the jacket.",
    "profile_left": "Profile: render a visibly dominant white cropped utility-jacket body from collar to hem, including the side-back panel and one long cuffed sleeve. Show the charcoal-gray crop top only as a narrow inner layer at the open front. Keep the bag at the outer wearer's-left rearward hip, its top aligned to the waistband, with the strap behind the jacket.",
    "profile_right": "Profile: render a visibly dominant white cropped utility-jacket body from collar to hem, including the side-back panel and one long cuffed sleeve. Show the charcoal-gray crop top only as a narrow inner layer at the open front. Keep the bag at the outer wearer's-left rearward hip, its top aligned to the waistband, with the strap behind the jacket.",
    "rear": "Rear: replace the upper garment with the supplied white cropped utility jacket: plain white back panel, long cuffed sleeves to the wrists, and bare-skin midriff below its hem; no gray inner top is visible. Show one continuous taut deep-navy canvas strap from the outer wearer's-right shoulder diagonally across the jacket back, exiting beyond the left waistband. At the outer left hip, show only a small deep-navy woven-fabric bag corner, mostly hidden behind the torso.",
}


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


def prop_reference_paths(prop_id: str, view: str) -> tuple[Path, ...]:
    if prop_id == "complete_outfit":
        if view.startswith("profile_"):
            return (
                COMPLETE_OUTFIT_REFERENCE_BY_VIEW["front"],
                COMPLETE_OUTFIT_REFERENCE_BY_VIEW["rear"],
            )
        return (COMPLETE_OUTFIT_REFERENCE_BY_VIEW[view],)
    if prop_id == "layered_jacket_crop_top":
        return (LAYERED_OUTFIT_REFERENCE_BY_VIEW[view],)
    return (PROPS[prop_id]["path"],)


def build_prompt(view: str, prop_ids: tuple[str, ...]) -> str:
    if view == "front" and "complete_outfit" in prop_ids:
        return (
            "Use the supplied full-body image only for the front pose, full-body framing, teal trousers, and white sneakers. "
            "Use the supplied complete-outfit image as the clothing source. Replace the visible gray top with a closed white "
            "cropped utility jacket: white front panels cover the chest, long cuffed sleeves reach the wrists, and only a narrow "
            "gray crop-top band may show below the hem. Add one taut deep-navy crossbody strap from the wearer's right shoulder "
            f"across the jacket to a bag at the outer left hip. {STUDIO_BACKGROUND_RULE} "
            "One woman, complete limbs, no text or labels."
        )
    if view.startswith("profile_") and "complete_outfit" in prop_ids:
        return (
            "Refine the supplied full-body reference into the same woman in a side-profile studio image. "
            f"Preserve pose, hair-to-sole framing, dark teal trousers, and white low-top sneakers. "
            "From the supplied front and rear outfit references, render a white cropped utility jacket as the visible "
            "outer torso layer: jacket body from collar to cropped hem, side-back panel, and one long cuffed sleeve. "
            "Keep the charcoal-gray crop top as a narrow inner layer at the open front. Place the deep-navy bag at the "
            f"outer left rearward hip with its strap behind the jacket. {STUDIO_BACKGROUND_RULE} "
            "One person, complete limbs, no text or labels."
        )
    prop_instructions = " ".join(PROPS[prop_id]["instruction"] for prop_id in prop_ids)
    if "complete_outfit" in prop_ids:
        prop_instructions = PROPS["complete_outfit"]["instruction"]
    elif "layered_jacket_crop_top" in prop_ids and view == "front":
        prop_instructions = "Add the supplied layered white cropped utility jacket worn open over the charcoal-gray crop top."
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
        f"{VIEW_RULES[view]} {prop_instructions} {' '.join(view_prop_rules)} {STUDIO_BACKGROUND_RULE} "
        "One person, complete limbs, no text or labels."
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
        help="Approved props to add to each selected full-body direction; defaults to paired complete outfit references.",
    )
    parser.add_argument(
        "--body-reference",
        action="append",
        default=[],
        metavar="VIEW=PATH",
        help="Override one composition input; unspecified views use the approved stable references.",
    )
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset applied to the fixed seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seed variants.")
    parser.add_argument("--seed-step", type=int, default=1, help="Increment between seed variants.")
    parser.add_argument("--steps", type=int, default=STEPS, help="Denoising steps for the single refinement pass.")
    parser.add_argument("--prompt", help="Replace the single-pass refinement prompt for a controlled experiment.")
    parser.add_argument("--preview-every", type=int, default=0, help="Save a decoded preview every N steps; 0 disables previews.")
    parser.add_argument(
        "--output-prefix",
        default="p7-5-2-fullbody-face-prop-refinement",
        help="Filename prefix placed before the contract hash, seed, and steps suffixes.",
    )
    args = parser.parse_args()
    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")
    if args.steps < 1:
        raise ValueError("steps must be at least 1")
    if args.preview_every < 0:
        raise ValueError("preview-every must be zero or positive")

    body_references = resolve_body_references(args.body_reference)
    reference_paths = [body_references[view] for view in args.views]
    reference_paths.extend(path for view in args.views for prop_id in args.props for path in prop_reference_paths(prop_id, view))
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

    for batch_index in range(args.seed_count):
        seed = SEED + args.seed_offset + batch_index * args.seed_step
        for view in args.views:
            prompt = args.prompt or build_prompt(view, tuple(args.props))
            prop_paths = [path for prop_id in args.props for path in prop_reference_paths(prop_id, view)]
            stem = candidate_stem(
                f"{args.output_prefix}-{view}",
                seed=seed,
                steps=args.steps,
                contract={
                    "model": MODEL_ID,
                    "prompt": prompt,
                    "body_composition": body_references[view].name,
                    "props": [path.name for path in prop_paths],
                    "seed": seed,
                    "steps": args.steps,
                    "size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                },
            )
            output = ROOT / f"{stem}-candidate.png"
            report = ROOT / f"{stem}-review.json"
            started = time.monotonic()
            prop_images = [Image.open(path).convert("RGB") for path in prop_paths]
            with Image.open(body_references[view]) as body_source:
                image = pipe(
                    image=[body_source.convert("RGB"), *prop_images],
                    prompt=prompt,
                    width=IMAGE_WIDTH,
                    height=IMAGE_HEIGHT,
                    num_inference_steps=args.steps,
                    guidance_scale=1.0,
                    generator=torch.Generator(device="cpu").manual_seed(seed),
                    max_sequence_length=256,
                    callback_on_step_end=preview_callback(
                        pipe,
                        height=IMAGE_HEIGHT,
                        width=IMAGE_WIDTH,
                        every=args.preview_every,
                        directory=ROOT / "previews",
                        prefix=f"{stem}-single-stage",
                    ),
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
                        "steps": args.steps,
                        "seed_offset": args.seed_offset,
                        "seed_step": args.seed_step,
                        "batch_index": batch_index,
                        "batch_size": args.seed_count,
                        "output_prefix": args.output_prefix,
                        "stage": {
                            "status": "generated",
                            "prompt": prompt,
                            "prompt_word_count": prompt_word_count(prompt),
                            "body_composition": body_references[view].name,
                            "props": [path.name for path in prop_paths],
                        },
                        "model": MODEL_ID,
                        "image_size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                        "elapsed_seconds": elapsed,
                        "decision": "Review face identity, body direction, outfit geometry, and strap continuity before approval.",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            print(f"[{batch_index + 1}/{args.seed_count}] {view}: {elapsed:.2f}s -> {output}")
            gc.collect()
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate non-front full-body turnaround views from a supplied front full-body image."""

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
FIRST_STAGE_SEED = 62294
SECOND_STAGE_SEED = 62294
FIRST_STAGE_STEPS = 3
SECOND_STAGE_STEPS = 9
SECOND_STAGE_STEPS_BY_VIEW = {
    "front_quarter_left": SECOND_STAGE_STEPS,
    "front_quarter_right": SECOND_STAGE_STEPS,
    "profile_left": 12,
    "profile_right": 12,
    "rear": SECOND_STAGE_STEPS,
}
BODY_SEED_BY_VIEW = {
    "front_quarter_left": FIRST_STAGE_SEED,
    "front_quarter_right": FIRST_STAGE_SEED,
    "profile_left": FIRST_STAGE_SEED,
    "profile_right": FIRST_STAGE_SEED,
    "rear": FIRST_STAGE_SEED,
}
FACE_REFERENCE_BY_VIEW = {
    "front_quarter_left": ROOT / "p7-5-2-face-front-quarter-left-reference.png",
    "front_quarter_right": ROOT / "p7-5-2-face-front-quarter-right-reference.png",
    "profile_left": ROOT / "p7-5-2-face-profile-left-reference.png",
    "profile_right": ROOT / "p7-5-2-face-profile-right-reference.png",
    "rear": ROOT / "p7-5-2-face-rear-reference.png",
}
# A complete approved front view preserves the outfit relationship more reliably
# than independently referenced top, trousers, and shoes.
FULLBODY_REFERENCE = ROOT / "p7-5-2-fullbody-front-reference.png"
IMAGE_WIDTH = 960
IMAGE_HEIGHT = 1440
VIEW_RULES = {
    "front_quarter_left": "left front-quarter view, walking diagonally toward image left; gaze toward the left front-quarter",
    "front_quarter_right": "right front-quarter view, walking diagonally toward image right; gaze toward the right front-quarter",
    "profile_left": "strict side profile facing image left; nose, chest, hips, and toes point image left; near arm visible, far arm hidden, two legs and shoes separate",
    "profile_right": "strict side profile facing image right; nose, chest, hips, and toes point image right; near arm visible, far arm hidden, two legs and shoes separate",
    "rear": "rear view",
}
TURNAROUND_ORDER = (
    "front_quarter_left",
    "front_quarter_right",
    "profile_left",
    "profile_right",
    "rear",
)
def prompt_word_count(text: str) -> int:
    return len(text.split())


def build_body_prompt(view: str) -> str:
    return (
        "Use the supplied front full-body reference as the fixed source for the entire figure and its rotation. "
        f"Render the same full-body figure {VIEW_RULES[view]}. "
        "Preserve the full-body proportion, clothing silhouette, shoulder-width stance, and off-white studio background."
    )


def build_face_refinement_prompt(view: str) -> str:
    if view == "rear":
        return (
            "Use the supplied rear-head reference to preserve the character's hair identity in the body-stage image. "
            "Keep the completed rear view, with only the back of the head visible and no facial features. "
            "Keep the body pose, clothing, and background unchanged."
        )
    return (
        "Use the supplied face reference to restore the character's face identity in the body-stage image. "
        "Keep the completed body pose, view direction, clothing, and background unchanged."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(VIEW_RULES),
        default=TURNAROUND_ORDER,
        help="Non-front views to generate, in turnaround order.",
    )
    parser.add_argument(
        "--front-image",
        type=Path,
        required=True,
        help="Approved or reviewable front full-body PNG used as the fixed turnaround anchor.",
    )
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset applied to the first seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seed variants.")
    parser.add_argument("--seed-step", type=int, default=1, help="Increment between seed variants.")
    parser.add_argument("--body-steps", type=int, default=FIRST_STAGE_STEPS, help="Denoising steps for the first full-body pass.")
    parser.add_argument(
        "--face-steps",
        type=int,
        help="Override the direction-specific denoising steps for the second face-refinement pass.",
    )
    parser.add_argument(
        "--body-only",
        action="store_true",
        help="Run and save only the first full-body stage; skip face identity refinement.",
    )
    parser.add_argument(
        "--body-prompt",
        help="Replace the first-stage prompt for a controlled composition experiment.",
    )
    parser.add_argument(
        "--body-image",
        type=Path,
        help="Existing first-stage full-body PNG. When supplied, skip the first pass and run only face identity refinement.",
    )
    parser.add_argument(
        "--face-reference",
        action="append",
        default=[],
        type=Path,
        metavar="PNG",
        help="Additional approved PNG reference for the second face-refinement pass; may be repeated.",
    )
    parser.add_argument(
        "--face-prompt",
        help="Replace the second-stage face-refinement prompt for a controlled experiment.",
    )
    parser.add_argument("--preview-every", type=int, default=0, help="Save a decoded preview every N denoising steps; 0 disables previews.")
    parser.add_argument(
        "--output-prefix",
        default="p7-5-2-fullbody-turnaround",
        help="Filename prefix placed before the contract-hash, seed, and steps suffixes.",
    )
    args = parser.parse_args()
    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")
    if args.body_steps < 1 or (args.face_steps is not None and args.face_steps < 1):
        raise ValueError("body-steps and face-steps must both be at least 1")
    selected_views = tuple(view for view in TURNAROUND_ORDER if view in args.views)
    if not args.front_image.is_file():
        raise FileNotFoundError(args.front_image)
    if args.body_image is not None and not args.body_image.is_file():
        raise FileNotFoundError(args.body_image)
    extra_face_reference_paths = [
        path if path.is_absolute() else ROOT / path
        for path in args.face_reference
    ]
    reference_paths = [*(FACE_REFERENCE_BY_VIEW[view] for view in selected_views), FULLBODY_REFERENCE]
    reference_paths.append(args.front_image)
    if args.body_image is not None:
        reference_paths.append(args.body_image)
    reference_paths.extend(extra_face_reference_paths)
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

    fullbody_reference_image = Image.open(FULLBODY_REFERENCE).convert("RGB")
    face_images = {
        view: Image.open(FACE_REFERENCE_BY_VIEW[view]).convert("RGB")
        for view in selected_views
    }
    extra_face_reference_images = [
        Image.open(path).convert("RGB")
        for path in extra_face_reference_paths
    ]
    supplied_body_image = Image.open(args.body_image).convert("RGB") if args.body_image is not None else None
    for batch_index in range(args.seed_count):
        seed_offset = args.seed_offset + batch_index * args.seed_step
        front_anchor_path = args.front_image
        front_anchor_image = Image.open(args.front_image).convert("RGB")
        for view in selected_views:
            body_seed = BODY_SEED_BY_VIEW[view] + seed_offset
            face_steps = args.face_steps or SECOND_STAGE_STEPS_BY_VIEW[view]
            body_prompt = args.body_prompt or build_body_prompt(view)
            body_reference_paths = [front_anchor_path, FULLBODY_REFERENCE]
            body_reference_images = [front_anchor_image, fullbody_reference_image]
            face_refinement_prompt = None if args.body_only else (args.face_prompt or build_face_refinement_prompt(view))
            stem = candidate_stem(f"{args.output_prefix}-{view}", seed=body_seed, steps=args.body_steps if args.body_only else face_steps, contract={"model": MODEL_ID, "body_prompt": body_prompt, "face_refinement_prompt": face_refinement_prompt, "references": [path.name for path in body_reference_paths], "face_references": [FACE_REFERENCE_BY_VIEW[view].name, *(path.name for path in extra_face_reference_paths)], "body_image": args.body_image.name if args.body_image else None, "body_only": args.body_only, "body_seed": body_seed, "face_seed": None if args.body_only else SECOND_STAGE_SEED, "body_steps": args.body_steps, "face_steps": None if args.body_only else face_steps, "size": [IMAGE_WIDTH, IMAGE_HEIGHT]})
            stage_descriptor = f"stage-1-seed-{body_seed}-steps-{args.body_steps}"
            if not args.body_only:
                stage_descriptor += f"-stage-2-seed-{SECOND_STAGE_SEED}-steps-{face_steps}"
            body_output = ROOT / f"{stem}-{stage_descriptor}-stage-1.png"
            face_output = None if args.body_only else ROOT / f"{stem}-{stage_descriptor}-stage-2.png"
            output = body_output if args.body_only else ROOT / f"{stem}-{stage_descriptor}-final-candidate.png"
            report = ROOT / f"{stem}-review.json"
            started = time.monotonic()
            if supplied_body_image is None:
                body_image = pipe(
                    image=body_reference_images,
                    prompt=body_prompt,
                    width=IMAGE_WIDTH,
                    height=IMAGE_HEIGHT,
                    num_inference_steps=args.body_steps,
                    guidance_scale=1.0,
                    generator=torch.Generator(device="cpu").manual_seed(body_seed),
                    max_sequence_length=256,
                    callback_on_step_end=preview_callback(pipe, height=IMAGE_HEIGHT, width=IMAGE_WIDTH, every=args.preview_every, directory=ROOT / "previews", prefix=f"{stem}-{stage_descriptor}-stage-1"),
                ).images[0]
            else:
                body_image = supplied_body_image.copy()
            body_image.save(body_output)
            gc.collect()
            torch.cuda.empty_cache()
            if not args.body_only:
                image = pipe(
                    image=[body_image, face_images[view], *extra_face_reference_images],
                    prompt=face_refinement_prompt,
                    width=IMAGE_WIDTH,
                    height=IMAGE_HEIGHT,
                    num_inference_steps=face_steps,
                    guidance_scale=1.0,
                    generator=torch.Generator(device="cpu").manual_seed(SECOND_STAGE_SEED),
                    max_sequence_length=256,
                    callback_on_step_end=preview_callback(pipe, height=IMAGE_HEIGHT, width=IMAGE_WIDTH, every=args.preview_every, directory=ROOT / "previews", prefix=f"{stem}-{stage_descriptor}-stage-2"),
                ).images[0]
                image.save(face_output)
                image.save(output)
            elapsed = round(time.monotonic() - started, 2)
            report.write_text(
                json.dumps(
                    {
                        "status": "review_required",
                        "body_output": body_output.name,
                        "face_output": face_output.name if face_output else None,
                        "output": output.name,
                        "view": view,
                        "seed": body_seed,
                        "body_seed": body_seed,
                        "face_seed": None if args.body_only else SECOND_STAGE_SEED,
                        "body_steps": args.body_steps,
                        "face_steps": None if args.body_only else face_steps,
                        "seed_offset": args.seed_offset,
                        "seed_step": args.seed_step,
                        "batch_index": batch_index,
                        "batch_size": args.seed_count,
                        "output_prefix": args.output_prefix,
                        "stages": {
                            "body": {
                                "status": "generated" if supplied_body_image is None else "supplied",
                                "prompt": body_prompt,
                                "prompt_word_count": prompt_word_count(body_prompt),
                                "references": [path.name for path in body_reference_paths],
                                "face_reference": None,
                                "front_anchor": front_anchor_path.name,
                                "supplied_image": args.body_image.name if args.body_image else None,
                                "output": body_output.name,
                            },
                            "face_refinement": {
                                "status": "skipped" if args.body_only else "generated",
                                "prompt": face_refinement_prompt,
                                "prompt_word_count": prompt_word_count(face_refinement_prompt) if face_refinement_prompt else 0,
                                "seed": None if args.body_only else SECOND_STAGE_SEED,
                                "references": None if args.body_only else [FACE_REFERENCE_BY_VIEW[view].name, *(path.name for path in extra_face_reference_paths)],
                                "output": face_output.name if face_output else None,
                            },
                        },
                        "model": MODEL_ID,
                        "image_size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                        "elapsed_seconds": elapsed,
                        "decision": "Experiment only; review body proportion, outfit continuity, direction, and face identity before approval.",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            print(f"[{batch_index + 1}/{args.seed_count}] {view}: {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

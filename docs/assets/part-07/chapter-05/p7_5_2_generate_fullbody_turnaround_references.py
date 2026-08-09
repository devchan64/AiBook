#!/usr/bin/env python3
"""Generate each non-front full-body turnaround view in one reference-guided pass."""

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
STEPS = 6
FACE_SHEET_PANEL_SIZE = 768
# This generator deliberately uses PNG references, not the shared face-identity
# text contract. The face sheet supplies the approved front and target direction.
FACE_SHEET_BY_VIEW = {
    "front_quarter_left": (
        ("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),
        ("approved_left_front_quarter_face", ROOT / "p7-5-2-face-front-quarter-left-reference.png"),
        ("approved_left_profile_face", ROOT / "p7-5-2-face-profile-left-reference.png"),
    ),
    "profile_left": (
        ("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),
        ("approved_left_front_quarter_face", ROOT / "p7-5-2-face-front-quarter-left-reference.png"),
        ("approved_left_profile_face", ROOT / "p7-5-2-face-profile-left-reference.png"),
    ),
    "front_quarter_right": (
        ("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),
        ("approved_right_front_quarter_face", ROOT / "p7-5-2-face-front-quarter-right-reference.png"),
        ("approved_right_profile_face", ROOT / "p7-5-2-face-profile-right-reference.png"),
    ),
    "profile_right": (
        ("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),
        ("approved_right_front_quarter_face", ROOT / "p7-5-2-face-front-quarter-right-reference.png"),
        ("approved_right_profile_face", ROOT / "p7-5-2-face-profile-right-reference.png"),
    ),
    "rear": (
        ("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),
        ("approved_rear_face", ROOT / "p7-5-2-face-rear-reference.png"),
    ),
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
    "rear": "rear view, with only the back of the head visible and no facial features",
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


def square_panel(image: Image.Image) -> Image.Image:
    """Fit one approved face PNG into a same-sized white panel."""
    source = image.convert("RGB")
    source.thumbnail((FACE_SHEET_PANEL_SIZE, FACE_SHEET_PANEL_SIZE), Image.Resampling.LANCZOS)
    panel = Image.new("RGB", (FACE_SHEET_PANEL_SIZE, FACE_SHEET_PANEL_SIZE), "white")
    offset = ((FACE_SHEET_PANEL_SIZE - source.width) // 2, (FACE_SHEET_PANEL_SIZE - source.height) // 2)
    panel.paste(source, offset)
    return panel


def build_face_reference_sheet(face_images: tuple[Image.Image, ...]) -> Image.Image:
    """Place the ordered face references side-by-side for one-pass conditioning."""
    sheet = Image.new("RGB", (FACE_SHEET_PANEL_SIZE * len(face_images), FACE_SHEET_PANEL_SIZE), "white")
    for index, face_image in enumerate(face_images):
        sheet.paste(square_panel(face_image), (FACE_SHEET_PANEL_SIZE * index, 0))
    return sheet


def build_prompt(view: str) -> str:
    return (
        "Use the supplied front full-body reference as the fixed source for the entire figure and its rotation. "
        "Use the supplied ordered face sheet to preserve the same face and hair across the front and target-direction panels. "
        f"Render the same full-body figure {VIEW_RULES[view]}. "
        "Preserve the full-body proportion, clothing silhouette, shoulder-width stance, and off-white studio background. "
        "One person, complete limbs, no text or labels."
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
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset applied to the fixed seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seed variants.")
    parser.add_argument("--seed-step", type=int, default=1, help="Increment between seed variants.")
    parser.add_argument("--steps", type=int, default=STEPS, help="Denoising steps for the single turnaround pass.")
    parser.add_argument("--prompt", help="Replace the one-pass turnaround prompt for a controlled experiment.")
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
    if args.steps < 1:
        raise ValueError("steps must be at least 1")
    if args.preview_every < 0:
        raise ValueError("preview-every must be zero or positive")
    selected_views = tuple(view for view in TURNAROUND_ORDER if view in args.views)
    reference_paths = [args.front_image, FULLBODY_REFERENCE]
    reference_paths.extend(path for view in selected_views for _, path in FACE_SHEET_BY_VIEW[view])
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
        path: Image.open(path).convert("RGB")
        for path in {path for view in selected_views for _, path in FACE_SHEET_BY_VIEW[view]}
    }
    face_sheets = {
        view: build_face_reference_sheet(tuple(face_images[path] for _, path in FACE_SHEET_BY_VIEW[view]))
        for view in selected_views
    }
    front_anchor_image = Image.open(args.front_image).convert("RGB")
    for batch_index in range(args.seed_count):
        seed = SEED + args.seed_offset + batch_index * args.seed_step
        for view in selected_views:
            prompt = args.prompt or build_prompt(view)
            face_sheet_labels = [label for label, _ in FACE_SHEET_BY_VIEW[view]]
            face_sheet_sources = [path.name for _, path in FACE_SHEET_BY_VIEW[view]]
            stem = candidate_stem(
                f"{args.output_prefix}-{view}",
                seed=seed,
                steps=args.steps,
                contract={
                    "model": MODEL_ID,
                    "prompt": prompt,
                    "references": [args.front_image.name, FULLBODY_REFERENCE.name],
                    "face_sheet_sources": face_sheet_sources,
                    "seed": seed,
                    "steps": args.steps,
                    "size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                },
            )
            output = ROOT / f"{stem}-candidate.png"
            report = ROOT / f"{stem}-review.json"
            started = time.monotonic()
            image = pipe(
                image=[front_anchor_image, fullbody_reference_image, face_sheets[view]],
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
                            "references": [args.front_image.name, FULLBODY_REFERENCE.name],
                            "face_reference_sheet": {
                                "panel_order": face_sheet_labels,
                                "sources": face_sheet_sources,
                                "size": [FACE_SHEET_PANEL_SIZE * len(face_sheet_sources), FACE_SHEET_PANEL_SIZE],
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
            gc.collect()
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate a front-anchored full-body turnaround from face and outfit references."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image
from p7_5_image_output_naming import candidate_stem, preview_callback


ROOT = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
BASE_SEED = 62294
FACE_IDENTITY_CONTRACT_PATH = ROOT / "p7-5-2-face-identity-contract.json"
FACE_IDENTITY_CONTRACT = json.loads(FACE_IDENTITY_CONTRACT_PATH.read_text(encoding="utf-8"))
FACE_IDENTITY_BY_VIEW = {
    "front": ROOT / "p7-5-2-face-front-reference.png",
    "front_quarter_left": ROOT / "p7-5-2-face-front-quarter-left-reference.png",
    "front_quarter_right": ROOT / "p7-5-2-face-front-quarter-right-reference.png",
    "profile_left": ROOT / "p7-5-2-face-profile-left-reference.png",
    "profile_right": ROOT / "p7-5-2-face-profile-right-reference.png",
    "rear": ROOT / "p7-5-2-face-rear-reference.png",
}
OUTFIT_REFERENCES = [
    ROOT / "p7-5-2-outfit-crop-top-waist-reference.png",
    ROOT / "p7-5-2-prop-reference-trousers.png",
    ROOT / "p7-5-2-prop-reference-shoes.png",
]
IMAGE_WIDTH = 768
IMAGE_HEIGHT = 1152
VIEW_RULES = {
    "front": "front view, facing the camera",
    "front_quarter_left": "left front three-quarter view, with face, chest, pelvis, knees, and feet turned together",
    "front_quarter_right": "right front three-quarter view, with face, chest, pelvis, knees, and feet turned together",
    "profile_left": (
        "true left side profile, with one near arm beside the torso and the far arm hidden; "
        "use a natural narrow standing stance with both shoes visibly separated along the horizontal axis, "
        "the near foot slightly forward and the far foot slightly back, so neither shoe or leg occludes the other; "
        "preserve the elongated forehead above the brow, a continuous unbroken hairline, and the deep viewer-right side "
        "part with one full short fringe sweeping across the viewer-left forehead and ending above the eyebrow; do not "
        "expose a blank, receded, or chopped-off forehead, split the fringe into extra bangs, or insert gaps in the hairline"
    ),
    "profile_right": (
        "true right side profile, with one near arm beside the torso and the far arm hidden; "
        "use a natural narrow standing stance with both shoes visibly separated along the horizontal axis, "
        "the near foot slightly forward and the far foot slightly back, so neither shoe or leg occludes the other; "
        "preserve the elongated forehead above the brow, a continuous unbroken hairline, and the deep viewer-right side "
        "part with one full short fringe sweeping across the viewer-left forehead and ending above the eyebrow; do not "
        "expose a blank, receded, or chopped-off forehead, split the fringe into extra bangs, or insert gaps in the hairline"
    ),
    "rear": "rear view, facing away from the camera",
}
TURNAROUND_ORDER = (
    "front",
    "front_quarter_left",
    "front_quarter_right",
    "profile_left",
    "profile_right",
    "rear",
)
OUTFIT_RULE = (
    "Keep the charcoal-gray micro-crop crew-neck top, bare-midriff gap, deep teal-blue wide-leg trousers, "
    "and white lace-up low-top sneakers from the outfit references."
)
BODY_PROPORTION_RULE = (
    "Use a realistic adult female fashion-turnaround proportion: an approximately seven-and-a-half-head-tall figure, "
    "with a naturally sized head, shoulders about two and a half head-widths across, a compact torso, a clear pelvis, "
    "and long straight legs. Place the knees near the lower half of the figure and the ankles directly above the shoes; "
    "keep both arms naturally proportional from shoulder to wrist and both hands near mid-thigh."
)


def prompt_word_count(text: str) -> int:
    return len(text.split())


def build_body_prompt(view: str, *, front_anchored: bool) -> str:
    identity_rule = (
        FACE_IDENTITY_CONTRACT["rear_hair_identity"]
        if view == "rear"
        else FACE_IDENTITY_CONTRACT["identity_description"]
    )
    front_anchor_rule = (
        "Use the supplied front full-body image as the fixed character, outfit, body-proportion, "
        "and hair-to-sole continuity anchor; rotate that same person only to the requested direction. "
        if front_anchored
        else ""
    )
    return (
        "Full-body character turnaround reference of one woman on an off-white studio background. "
        f"{front_anchor_rule}"
        "Use the supplied direction-matched face identity reference as the fixed face anchor while "
        "constructing the full body: "
        f"{identity_rule} "
        f"{OUTFIT_RULE} {BODY_PROPORTION_RULE} {VIEW_RULES[view]}. "
        "One neutral upright standing figure, fully visible from hair to shoe soles, centered in the frame. "
        "No crop, no duplicate body, no other person, no text, and no labels."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(VIEW_RULES),
        default=TURNAROUND_ORDER,
        help="Views to generate. A complete turnaround is always ordered from front to rear.",
    )
    parser.add_argument(
        "--front-image",
        type=Path,
        help="Approved or reviewable front full-body PNG used to anchor individually generated non-front views.",
    )
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset applied to the first seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seed variants.")
    parser.add_argument("--seed-step", type=int, default=1, help="Increment between seed variants.")
    parser.add_argument("--steps", type=int, default=3, help="Denoising steps for the unified full-body generation pass.")
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
    selected_views = tuple(view for view in TURNAROUND_ORDER if view in args.views)
    needs_front_anchor = any(view != "front" for view in selected_views)
    if "front" not in selected_views and needs_front_anchor and args.front_image is None:
        raise ValueError("--front-image is required when generating non-front views without front")
    if args.front_image is not None and not args.front_image.is_file():
        raise FileNotFoundError(args.front_image)
    reference_paths = [*(FACE_IDENTITY_BY_VIEW[view] for view in selected_views), *OUTFIT_REFERENCES]
    if args.front_image is not None:
        reference_paths.append(args.front_image)
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

    first_seed = BASE_SEED + args.seed_offset
    outfit_images = [Image.open(path).convert("RGB") for path in OUTFIT_REFERENCES]
    face_images = {
        view: Image.open(FACE_IDENTITY_BY_VIEW[view]).convert("RGB")
        for view in selected_views
    }
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        generated_front_image = None
        generated_front_path = None
        if "front" not in selected_views:
            generated_front_path = args.front_image
            generated_front_image = Image.open(args.front_image).convert("RGB")
        for view in selected_views:
            front_anchored = view != "front"
            body_prompt = build_body_prompt(view, front_anchored=front_anchored)
            body_reference_paths = [FACE_IDENTITY_BY_VIEW[view], *OUTFIT_REFERENCES]
            body_reference_images = [face_images[view], *outfit_images]
            if front_anchored:
                assert generated_front_image is not None and generated_front_path is not None
                body_reference_paths.insert(0, generated_front_path)
                body_reference_images.insert(0, generated_front_image)
            stem = candidate_stem(f"{args.output_prefix}-{view}", seed=seed, steps=args.steps, contract={"model": MODEL_ID, "prompt": body_prompt, "references": [path.name for path in body_reference_paths], "size": [IMAGE_WIDTH, IMAGE_HEIGHT], "steps": args.steps})
            output = ROOT / f"{stem}-candidate.png"
            report = ROOT / f"{stem}-review.json"
            started = time.monotonic()
            body_image = pipe(
                image=body_reference_images,
                prompt=body_prompt,
                width=IMAGE_WIDTH,
                height=IMAGE_HEIGHT,
                num_inference_steps=args.steps,
                guidance_scale=1.0,
                generator=torch.Generator(device="cpu").manual_seed(seed),
                max_sequence_length=256,
                callback_on_step_end=preview_callback(pipe, height=IMAGE_HEIGHT, width=IMAGE_WIDTH, every=args.preview_every, directory=ROOT / "previews", prefix=f"{stem}-body"),
            ).images[0]
            body_image.save(output)
            if view == "front":
                generated_front_path = output
                generated_front_image = body_image
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
                        "stages": {
                            "unified_fullbody": {
                                "prompt": body_prompt,
                                "prompt_word_count": prompt_word_count(body_prompt),
                                "references": [path.name for path in body_reference_paths],
                                "face_identity_reference": FACE_IDENTITY_BY_VIEW[view].name,
                                "face_identity_contract": FACE_IDENTITY_CONTRACT_PATH.name,
                                "front_anchor": generated_front_path.name if front_anchored else None,
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

#!/usr/bin/env python3
"""Generate individual full-body turnaround candidates from face and outfit references."""

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
BASE_SEED = 62294
FACE_IDENTITY_SEED = 62294
FACE_IDENTITY_CONTRACT_PATH = ROOT / "p7-5-2-face-identity-contract.json"
FACE_IDENTITY_CONTRACT = json.loads(FACE_IDENTITY_CONTRACT_PATH.read_text(encoding="utf-8"))
FACE_IDENTITY_BY_VIEW = {
    view: ROOT / "p7-5-2-face-turnaround-reference.png"
    for view in ("front", "front_quarter", "profile", "rear")
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
    "front_quarter": "front three-quarter view, with face, chest, pelvis, knees, and feet turned together",
    "profile": (
        "true side profile, with one near arm beside the torso and the far arm hidden; "
        "use a natural narrow standing stance with both shoes visibly separated along the horizontal axis, "
        "the near foot slightly forward and the far foot slightly back, so neither shoe or leg occludes the other; "
        "preserve the elongated forehead above the brow, a continuous unbroken hairline, and the deep viewer-right side "
        "part with one full short fringe sweeping across the viewer-left forehead and ending above the eyebrow; do not "
        "expose a blank, receded, or chopped-off forehead, split the fringe into extra bangs, or insert gaps in the hairline"
    ),
    "rear": "rear view, facing away from the camera",
}
OUTFIT_RULE = (
    "Keep the charcoal-gray micro-crop crew-neck top, bare-midriff gap, deep teal-blue wide-leg trousers, "
    "and white lace-up low-top sneakers from the outfit references."
)


def prompt_word_count(text: str) -> int:
    return len(text.split())


def build_body_prompt(view: str) -> str:
    return (
        "Full-body character turnaround reference of one woman on an off-white studio background. "
        "Use the supplied direction-matched 2x face identity reference as the preliminary face anchor while "
        "constructing the full body. "
        f"{OUTFIT_RULE} {VIEW_RULES[view]}. "
        "One neutral upright standing figure, fully visible from hair to shoe soles, centered in the frame. "
        "No crop, no duplicate body, no other person, no text, and no labels."
    )


def build_face_identity_prompt(view: str) -> str:
    return (
        "Use the supplied full-body image as the fixed composition, pose, direction, clothing, and hair-to-sole framing anchor. "
        "Restore only the direction-matched face identity from the supplied 2x identity reference: "
        f"{FACE_IDENTITY_CONTRACT['identity_description']} "
        f"{VIEW_RULES[view]} Keep the outfit, limbs, body proportion, and camera unchanged. "
        "One person, no text, and no labels."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(VIEW_RULES),
        default=("front", "front_quarter", "profile", "rear"),
        help="Individual views to generate; each view is written as a separate PNG.",
    )
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset applied to the first seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seed variants.")
    parser.add_argument("--seed-step", type=int, default=1, help="Increment between seed variants.")
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
    reference_paths = [
        *(FACE_IDENTITY_BY_VIEW[view] for view in args.views),
        *OUTFIT_REFERENCES,
    ]
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
        for view in args.views
    }
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        for view in args.views:
            body_prompt = build_body_prompt(view)
            face_identity_prompt = build_face_identity_prompt(view)
            body_reference_paths = [FACE_IDENTITY_BY_VIEW[view], *OUTFIT_REFERENCES]
            body_reference_images = [face_images[view], *outfit_images]
            stem = candidate_stem(f"{args.output_prefix}-{view}", seed=seed, steps=12, contract={"model": MODEL_ID, "body_prompt": body_prompt, "face_prompt": face_identity_prompt, "body_references": [path.name for path in body_reference_paths], "face_identity_seed": FACE_IDENTITY_SEED, "size": [IMAGE_WIDTH, IMAGE_HEIGHT]})
            output = ROOT / f"{stem}-candidate.png"
            report = ROOT / f"{stem}-review.json"
            started = time.monotonic()
            body_image = pipe(
                image=body_reference_images,
                prompt=body_prompt,
                width=IMAGE_WIDTH,
                height=IMAGE_HEIGHT,
                num_inference_steps=12,
                guidance_scale=1.0,
                generator=torch.Generator(device="cpu").manual_seed(seed),
                max_sequence_length=256,
                callback_on_step_end=preview_callback(pipe, height=IMAGE_HEIGHT, width=IMAGE_WIDTH, every=args.preview_every, directory=ROOT / "previews", prefix=f"{stem}-body"),
            ).images[0]
            gc.collect()
            torch.cuda.empty_cache()
            image = pipe(
                image=[body_image, face_images[view]],
                prompt=face_identity_prompt,
                width=IMAGE_WIDTH,
                height=IMAGE_HEIGHT,
                num_inference_steps=12,
                guidance_scale=1.0,
                generator=torch.Generator(device="cpu").manual_seed(FACE_IDENTITY_SEED),
                max_sequence_length=256,
                callback_on_step_end=preview_callback(pipe, height=IMAGE_HEIGHT, width=IMAGE_WIDTH, every=args.preview_every, directory=ROOT / "previews", prefix=f"{stem}-face"),
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
                        "output_prefix": args.output_prefix,
                        "face_identity_seed": FACE_IDENTITY_SEED,
                        "stages": {
                            "body": {
                                "prompt": body_prompt,
                                "prompt_word_count": prompt_word_count(body_prompt),
                                "references": [path.name for path in body_reference_paths],
                            },
                            "face_identity": {
                                "prompt": face_identity_prompt,
                                "prompt_word_count": prompt_word_count(face_identity_prompt),
                                "seed": FACE_IDENTITY_SEED,
                                "reference": FACE_IDENTITY_BY_VIEW[view].name,
                                "contract": FACE_IDENTITY_CONTRACT_PATH.name,
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

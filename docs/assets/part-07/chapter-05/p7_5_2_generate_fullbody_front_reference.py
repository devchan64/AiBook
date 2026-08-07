#!/usr/bin/env python3
"""Generate a two-stage front full-body proportion reference for the turnaround pipeline."""

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
FACE_REFERENCE = ROOT / "p7-5-2-face-front-reference.png"
FACE_IDENTITY_CONTRACT_PATH = ROOT / "p7-5-2-face-identity-contract.json"
FACE_IDENTITY_CONTRACT = json.loads(FACE_IDENTITY_CONTRACT_PATH.read_text(encoding="utf-8"))
OUTFIT_REFERENCES = [
    ROOT / "p7-5-2-outfit-crop-top-waist-reference.png",
    ROOT / "p7-5-2-prop-reference-trousers.png",
    ROOT / "p7-5-2-prop-reference-shoes.png",
]
IMAGE_WIDTH = 768
IMAGE_HEIGHT = 1152
OUTFIT_RULE = (
    "Keep the charcoal-gray micro-crop crew-neck top, bare-midriff gap, deep teal-blue wide-leg trousers, "
    "and white lace-up low-top sneakers from the outfit references."
)
FRONT_PROPORTION_RULE = (
    "Tall adult fashion figure, close to eight heads high: a small proportional head, compact torso, high waist, and long legs."
)


def prompt_word_count(text: str) -> int:
    return len(text.split())


def build_body_prompt() -> str:
    return (
        "Front full-body character proportion reference of one woman on an off-white studio background. "
        f"{OUTFIT_RULE} {FRONT_PROPORTION_RULE} "
        "Neutral upright standing figure, fully visible from hair to shoe soles, centered in the frame. "
        "No crop, no duplicate body, no other person, no text, and no labels."
    )


def build_face_identity_prompt() -> str:
    return (
        "Use the supplied full-body image as the fixed pose, outfit, body-proportion, and hair-to-sole framing anchor. "
        "Use the supplied front face image as a strong identity reference. "
        f"Restore this identity in front view: {FACE_IDENTITY_CONTRACT['identity_description']} "
        "Refine the face and hair only; keep the body, hands, legs, shoes, outfit, background, camera, and framing unchanged. "
        "One person, no text, and no labels."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-offset", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=1)
    parser.add_argument("--seed-step", type=int, default=1)
    parser.add_argument("--body-steps", type=int, default=3, help="First body-proportion stage steps.")
    parser.add_argument("--face-steps", type=int, default=6, help="Second face-identity stage steps.")
    parser.add_argument("--preview-every", type=int, default=0)
    parser.add_argument("--output-prefix", default="p7-5-2-fullbody-front")
    args = parser.parse_args()
    if args.seed_count < 1 or args.seed_step == 0:
        raise ValueError("seed-count must be positive and seed-step must not be zero")
    if args.body_steps < 1 or args.face_steps < 1:
        raise ValueError("body-steps and face-steps must both be at least 1")
    reference_paths = [FACE_REFERENCE, *OUTFIT_REFERENCES]
    if missing := [path.name for path in reference_paths if not path.is_file()]:
        raise FileNotFoundError(", ".join(missing))
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache"
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    face_image = Image.open(FACE_REFERENCE).convert("RGB")
    outfit_images = [Image.open(path).convert("RGB") for path in OUTFIT_REFERENCES]
    body_prompt = build_body_prompt()
    face_prompt = build_face_identity_prompt()

    for batch_index in range(args.seed_count):
        seed = BASE_SEED + args.seed_offset + batch_index * args.seed_step
        stem = candidate_stem(
            args.output_prefix,
            seed=seed,
            steps=args.face_steps,
            contract={
                "model": MODEL_ID,
                "body_prompt": body_prompt,
                "face_prompt": face_prompt,
                "references": [path.name for path in reference_paths],
                "body_steps": args.body_steps,
                "face_steps": args.face_steps,
                "size": [IMAGE_WIDTH, IMAGE_HEIGHT],
            },
        )
        body_output = ROOT / f"{stem}-body-stage-steps-{args.body_steps}.png"
        output = ROOT / f"{stem}-candidate.png"
        report = ROOT / f"{stem}-review.json"
        started = time.monotonic()
        body_image = pipe(
            image=[face_image, *outfit_images],
            prompt=body_prompt,
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT,
            num_inference_steps=args.body_steps,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(seed),
            max_sequence_length=256,
            callback_on_step_end=preview_callback(pipe, height=IMAGE_HEIGHT, width=IMAGE_WIDTH, every=args.preview_every, directory=ROOT / "previews", prefix=f"{stem}-body"),
        ).images[0]
        body_image.save(body_output)
        gc.collect()
        torch.cuda.empty_cache()
        image = pipe(
            image=[body_image, face_image],
            prompt=face_prompt,
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT,
            num_inference_steps=args.face_steps,
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
                    "body_output": body_output.name,
                    "output": output.name,
                    "seed": seed,
                    "body_steps": args.body_steps,
                    "face_steps": args.face_steps,
                    "stages": {
                        "body": {"prompt": body_prompt, "prompt_word_count": prompt_word_count(body_prompt), "references": [path.name for path in reference_paths]},
                        "face_identity": {"prompt": face_prompt, "prompt_word_count": prompt_word_count(face_prompt), "seed": FACE_IDENTITY_SEED, "reference": FACE_REFERENCE.name, "contract": FACE_IDENTITY_CONTRACT_PATH.name},
                    },
                    "model": MODEL_ID,
                    "image_size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                    "elapsed_seconds": elapsed,
                    "decision": "Experiment only; review body proportion and face identity before approval.",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"[{batch_index + 1}/{args.seed_count}] front: {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Test a review-only basketball-jump frame from character and outfit references.

The run intentionally changes pose, camera, and scene together. It must not
replace any character-reference PNG without a separate human review.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image
from p7_5_image_output_naming import candidate_stem


ROOT = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
BASE_SEED = 62382
IMAGE_SIZE = (768, 1152)
REFERENCE_INPUTS = (
    ("face_identity", ROOT / "p7-5-2-face-turnaround-codeformer-front-2x.png"),
    ("fullbody_front", ROOT / "p7-5-2-fullbody-front-reference.png"),
    ("fullbody_front_quarter", ROOT / "p7-5-2-fullbody-front-quarter-reference.png"),
    ("fullbody_profile", ROOT / "p7-5-2-fullbody-profile-reference.png"),
    ("fullbody_rear", ROOT / "p7-5-2-fullbody-rear-reference.png"),
)
BASKETBALL_JUMP_PROMPT = (
    "Same woman from the supplied references, full body, with the deep petrol-teal jaw-length bob retained; no ponytail, "
    "long hair, or hair accessory. Airborne alley-oop dunk at the apex of the jump: her body is clearly suspended above "
    "the court with a visible gap beneath both shoes and neither foot touching the ground. Her fully visible right hand grips "
    "exactly one basketball high above her head toward one hoop, with the ball separated from her hair and fingers. Her left arm balances, left knee "
    "leads forward, right leg trails behind, and both legs and shoes are fully visible. Low front-left camera, modest Dutch "
    "tilt, diagonal frame. One woman, one ball, one hoop, no text, border, or panels."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset added to the fixed base seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seeds to generate.")
    parser.add_argument("--steps", type=int, default=12, help="Denoising steps; lower values trade detail for speed.")
    parser.add_argument(
        "--output-prefix",
        default="p7-5-2-dynamic-basketball-jump",
        help="Prefix placed before the contract hash, seed, and steps in candidate filenames.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.steps < 1 or args.seed_count < 1:
        raise ValueError("--steps and --seed-count must be at least 1")
    missing = [path.name for _, path in REFERENCE_INPUTS if not path.is_file()]
    if missing:
        raise FileNotFoundError(", ".join(missing))
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this local GPU example")

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    images = [Image.open(path).convert("RGB") for _, path in REFERENCE_INPUTS]
    for batch_index in range(args.seed_count):
        seed = BASE_SEED + args.seed_offset + batch_index
        stem = candidate_stem(args.output_prefix, seed=seed, steps=args.steps, contract={"model": MODEL_ID, "prompt": BASKETBALL_JUMP_PROMPT, "inputs": [path.name for _, path in REFERENCE_INPUTS], "size": IMAGE_SIZE})
        output = ROOT / f"{stem}-candidate.png"
        report = ROOT / f"{stem}-review.json"
        started = time.monotonic()
        result = pipe(
            image=images,
            prompt=BASKETBALL_JUMP_PROMPT,
            width=IMAGE_SIZE[0],
            height=IMAGE_SIZE[1],
            num_inference_steps=args.steps,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(seed),
            max_sequence_length=256,
        ).images[0]
        result.save(output)
        elapsed = round(time.monotonic() - started, 2)
        report.write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "output": output.name,
                    "prompt": BASKETBALL_JUMP_PROMPT,
                    "prompt_word_count": len(BASKETBALL_JUMP_PROMPT.split()),
                    "seed": seed,
                    "batch_index": batch_index + 1,
                    "seed_count": args.seed_count,
                    "steps": args.steps,
                    "model": MODEL_ID,
                    "image_size": list(IMAGE_SIZE),
                    "inputs": [{"role": role, "file": path.name} for role, path in REFERENCE_INPUTS],
                    "elapsed_seconds": elapsed,
                    "decision": "Review face, outfit, bag strap, limb count, ball position, ball-rim separation, and camera before using any result.",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"{batch_index + 1}/{args.seed_count}: {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

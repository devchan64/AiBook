#!/usr/bin/env python3
"""Generate one or more chin-cropped Mira front-face candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from p7_5_image_output_naming import candidate_stem, preview_callback


ROOT = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
FACE_IDENTITY_CONTRACT_PATH = ROOT / "p7-5-2-face-identity-contract.json"
FACE_IDENTITY_CONTRACT = json.loads(FACE_IDENTITY_CONTRACT_PATH.read_text(encoding="utf-8"))
PROMPT = " ".join(
    (
        FACE_IDENTITY_CONTRACT["front_portrait_context"],
        FACE_IDENTITY_CONTRACT["identity_description"],
        FACE_IDENTITY_CONTRACT["front_portrait_suffix"],
    )
)


def prompt_word_count(text: str) -> int:
    return len(text.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed-offset",
        type=int,
        default=0,
        help="Offset applied to the first face-with-hair seed.",
    )
    parser.add_argument(
        "--seed-count",
        type=int,
        default=1,
        help="Number of consecutive seed variants to generate.",
    )
    parser.add_argument(
        "--seed-step",
        type=int,
        default=1,
        help="Increment between consecutive seed variants.",
    )
    parser.add_argument(
        "--output-prefix",
        help="Filename prefix placed before the contract-hash, seed, and steps suffixes.",
    )
    parser.add_argument("--steps", type=int, default=6, help="Number of FLUX denoising steps.")
    parser.add_argument("--preview-every", type=int, default=0, help="Save a decoded preview every N denoising steps; 0 disables previews.")
    args = parser.parse_args()
    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")
    if args.steps < 1:
        raise ValueError("steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    first_seed = 62294 + args.seed_offset
    prefix = args.output_prefix or "p7-5-2-face-front-with-hair-v3"
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        stem = candidate_stem(
            prefix,
            seed=seed,
            steps=args.steps,
            contract={"model": MODEL_ID, "prompt": PROMPT, "size": [768, 768], "steps": args.steps},
        )
        output = ROOT / f"{stem}-candidate.png"
        report = ROOT / f"{stem}-review.json"
        started = time.monotonic()
        image = pipe(
            prompt=PROMPT,
            width=768,
            height=768,
            num_inference_steps=args.steps,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(seed),
            max_sequence_length=256,
            callback_on_step_end=preview_callback(pipe, height=768, width=768, every=args.preview_every, directory=ROOT / "previews", prefix=stem),
        ).images[0]
        image.save(output)
        elapsed = round(time.monotonic() - started, 2)
        report.write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "seed_offset": args.seed_offset,
                    "seed_step": args.seed_step,
                    "batch_index": batch_index,
                    "batch_size": args.seed_count,
                    "output_prefix": prefix,
                    "output": output.name,
                    "seed": seed,
                    "steps": args.steps,
                    "prompt": PROMPT,
                    "prompt_word_count": prompt_word_count(PROMPT),
                    "references": [],
                    "model": MODEL_ID,
                    "image_size": [768, 768],
                    "elapsed_seconds": elapsed,
                    "decision": "Candidate only; human review is required before it becomes a front-face or geometry reference.",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"[{batch_index + 1}/{args.seed_count}] {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

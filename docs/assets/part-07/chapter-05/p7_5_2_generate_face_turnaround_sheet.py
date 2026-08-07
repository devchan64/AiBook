#!/usr/bin/env python3
"""Generate one or more face turnaround sheets from the frontal reference."""

from __future__ import annotations

import argparse
import gc
from hashlib import sha256
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path(__file__).resolve().parent
FRONT = ROOT / "p7-5-2-face-front-reference.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
FACE_IDENTITY_CONTRACT_PATH = ROOT / "p7-5-2-face-identity-contract.json"
FACE_IDENTITY_CONTRACT = json.loads(FACE_IDENTITY_CONTRACT_PATH.read_text(encoding="utf-8"))
BASE_SEED = 62294
HEAD_INPUT_BOTTOM = 720
SHEET_SIZE = 1024
VIEW_RULES = {
    "front": "front view at 0 degrees, with the nose centered and both eyes equally visible",
    "front_quarter": "45-degree front-quarter view, with the near eye fully visible and the far eye half visible",
    "profile": "90-degree profile view, with one near eye visible in side view and the far eye hidden",
    "rear": (
        "strict 180-degree rear view, facing directly away from the camera: show only the back of the bob haircut, "
        "back of head, ears if exposed, and nape; no face, eye, eyebrow, nose, lips, cheek, or side-profile outline"
    ),
}
TURNAROUND_FIDELITY_RULE = (
    "Keep visible radial iris texture, a consistent iris diameter and pupil-to-iris ratio in every panel, "
    "allowing only perspective foreshortening. Keep the gaze direction aligned with the nose direction in every visible face."
)


def prompt_word_count(text: str) -> int:
    return len(text.split())


def output_contract_hash(
    turnaround_prompt: str, identity_fix_prompt: str, views: tuple[str, ...], seed: int
) -> str:
    """Return a stable short hash for the seed and generation contract in an output name."""
    contract = json.dumps(
        {
            "model": MODEL_ID,
            "seed": seed,
            "views": views,
            "turnaround_prompt": turnaround_prompt,
            "identity_fix_prompt": identity_fix_prompt,
            "image_size": [SHEET_SIZE, SHEET_SIZE],
            "steps": 12,
            "guidance_scale": 1.0,
            "identity_contract": FACE_IDENTITY_CONTRACT_PATH.name,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256(contract.encode("utf-8")).hexdigest()[:10]


def build_prompt(views: tuple[str, ...]) -> str:
    layout = "2 by 2" if len(views) == 4 else f"{len(views)}-panel"
    positions = {
        1: ("single panel",),
        2: ("left panel", "right panel"),
        3: ("top-left", "top-right", "bottom-center"),
        4: ("top-left", "top-right", "bottom-left", "bottom-right"),
    }[len(views)]
    view_list = "; ".join(
        f"{position}: {VIEW_RULES[view]}" for position, view in zip(positions, views, strict=True)
    )
    return (
        f"{layout} face turnaround of the same woman from the reference image. "
        f"Fixed panel directions: {view_list}. Use one distinct view per panel; never duplicate a front, three-quarter, "
        "profile, or rear view in another panel. The rear panel must remain a face-hidden back view. "
        f"{FACE_IDENTITY_CONTRACT['identity_description']} {TURNAROUND_FIDELITY_RULE}"
    )


def build_identity_fix_prompt(views: tuple[str, ...]) -> str:
    """Fix face identity without changing the first-stage panel layout or rotations."""
    layout = "2 by 2" if len(views) == 4 else f"{len(views)}-panel"
    positions = {
        1: ("single panel",),
        2: ("left panel", "right panel"),
        3: ("top-left", "top-right", "bottom-center"),
        4: ("top-left", "top-right", "bottom-left", "bottom-right"),
    }[len(views)]
    view_list = "; ".join(
        f"{position}: {VIEW_RULES[view]}" for position, view in zip(positions, views, strict=True)
    )
    return (
        f"Use the first supplied {layout} turnaround sheet as the fixed panel layout, crop, and head rotation. "
        "Use the second supplied frontal face image only as the identity anchor for the same woman. "
        f"Keep fixed panel directions: {view_list}. Do not duplicate or exchange panel directions. "
        f"Restore the same visible-face identity: {FACE_IDENTITY_CONTRACT['identity_description']} "
        f"{TURNAROUND_FIDELITY_RULE} For a rear panel, preserve only {FACE_IDENTITY_CONTRACT['rear_hair_identity']} "
        "and do not reveal a face. Keep the background and all panel boundaries unchanged."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(VIEW_RULES),
        default=("front", "profile"),
        help="Face views to include in reading order; defaults to front and profile for review.",
    )
    parser.add_argument(
        "--seed-offset",
        type=int,
        default=0,
        help="Offset applied to the first turnaround-sheet seed.",
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
        default="p7-5-2-face-turnaround-sheet",
        help="Filename prefix placed before the contract-hash, seed, and steps suffixes.",
    )
    parser.add_argument(
        "--stage",
        choices=("all", "turnaround", "identity"),
        default="all",
        help="Run the turnaround layout stage, identity-fix stage from --intermediate, or both stages.",
    )
    parser.add_argument(
        "--intermediate",
        type=Path,
        help="First-stage turnaround PNG required by --stage identity.",
    )
    args = parser.parse_args()
    if len(args.views) > 4:
        raise ValueError("A turnaround sheet accepts at most four views")
    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")
    if args.stage == "identity" and args.intermediate is None:
        raise ValueError("--stage identity requires --intermediate")
    if not FRONT.is_file():
        raise FileNotFoundError(FRONT.name)
    if args.intermediate is not None and not args.intermediate.is_file():
        raise FileNotFoundError(args.intermediate.name)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    source = Image.open(FRONT).convert("RGB")
    anchor = source.crop((0, 0, source.width, HEAD_INPUT_BOTTOM))
    prompt = build_prompt(tuple(args.views))
    first_seed = BASE_SEED + args.seed_offset
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        contract_hash = output_contract_hash(prompt, tuple(args.views), seed)
        stem = f"{args.output_prefix}-hash-{contract_hash}-seed-{seed}-steps-12"
        output = ROOT / f"{stem}-candidate.png"
        report = ROOT / f"{stem}-review.json"
        started = time.monotonic()
        sheet = pipe(
            image=anchor,
            prompt=prompt,
            width=SHEET_SIZE,
            height=SHEET_SIZE,
            num_inference_steps=12,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(seed),
            max_sequence_length=256,
        ).images[0]
        sheet.save(output)
        elapsed = round(time.monotonic() - started, 2)
        report.write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "output": output.name,
                    "seed": seed,
                    "contract_hash": contract_hash,
                    "seed_offset": args.seed_offset,
                    "seed_step": args.seed_step,
                    "batch_index": batch_index,
                    "batch_size": args.seed_count,
                    "output_prefix": args.output_prefix,
                    "prompt": prompt,
                    "prompt_word_count": prompt_word_count(prompt),
                    "references": [FRONT.name],
                    "identity_contract": FACE_IDENTITY_CONTRACT_PATH.name,
                    "input_transform": f"Cropped the frontal anchor at y={HEAD_INPUT_BOTTOM} before inference.",
                    "sheet_layout": args.views,
                    "style_reference": None,
                    "model": MODEL_ID,
                    "image_size": [SHEET_SIZE, SHEET_SIZE],
                    "elapsed_seconds": elapsed,
                    "decision": "Candidate only; review each view for layout, direction, and identity consistency.",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"[{batch_index + 1}/{args.seed_count}] {elapsed:.2f}s -> {output}")


if __name__ == "__main__":
    main()

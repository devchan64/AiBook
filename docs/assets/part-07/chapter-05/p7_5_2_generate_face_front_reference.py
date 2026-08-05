#!/usr/bin/env python3
"""Generate a chin-cropped Mira front-face candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
OUTPUT = ROOT / "p7-5-2-face-front-chin-crop-v4-candidate.png"
BALD_OUTPUT = ROOT / "p7-5-2-face-front-bald-geometry-v1-candidate.png"
BALD_DETAIL_OUTPUT = ROOT / "p7-5-2-face-front-bald-detail-match-v1-candidate.png"
HAIR_OUTPUT = ROOT / "p7-5-2-face-front-hair-match-v1-candidate.png"
HAIR_REFERENCE = ROOT / "p7-5-2-face-front-v2.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"

PROMPT = """Original adult webtoon woman, strict front head-only portrait on off-white paper. The image contains the full hair mass, face, jaw, and chin only; its lower edge ends directly beneath the chin. Oval face with warm light-peach skin, broad low-set cheekbones, visibly soft cheek fullness, and a smooth taper into a soft jaw. High straight nose bridge and a defined nose tip; calm neutral expression. Equal almond cat eyes with subtly upturned outer corners, two-color irises of chestnut brown and amber blended in a subtle radial wave pattern, dark limbal rings, and centered black pupils. Deep teal-blue hair in a rounded jaw-length bob: a deep viewer-right side part, one broad fringe sweeping across to the viewer-left forehead, and tapered side locks at the jaw."""
BALD_PROMPT = """Strict frontal geometry of a completely bald, hairless fifteen-year-old female with Western facial features on off-white. Very fair pale-peach skin. Egg-shaped skull, rounded crown, compact oval face, soft cheeks, and short rounded chin. Slim nose bridge and small rounded tip. Very large symmetric almond eyes with centered pupils; chestnut-brown and orange-amber irises. Crop below the chin."""
BALD_DETAIL_PROMPT = """Strict frontal, completely bald fifteen-year-old female face with East Asian facial features on off-white. Preserve the bald reference's skull, face outline, camera, and crop; use the face reference only for feature placement. Smooth very fair pale-peach skin. Retain the geometry. Slim nose bridge, small rounded tip, and very large near-symmetric almond eyes. Remove all visible double-eyelid creases. Crop below the chin."""
HAIR_PROMPT = """Add the deep teal jaw-length bob from the hair reference to the bald frontal geometry. Preserve face outline, eye line, nose, jaw, and camera. Keep the viewer-right part, broad viewer-left fringe, and tapered jaw locks. Crop directly below the chin."""


def prompt_word_count(text: str) -> int:
    return len(text.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--stages",
        nargs="+",
        choices=("character", "bald_geometry", "bald_detail_match", "hair_match"),
        default=("character",),
        help="Run the character, bald geometry, bald-detail match, or hair-match stage.",
    )
    parser.add_argument(
        "--seed-offset",
        type=int,
        default=0,
        help="Add the same offset to every selected stage's base seed.",
    )
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    if "character" in args.stages and len(args.stages) != 1:
        raise ValueError("character cannot be combined with bald_geometry or hair_match")
    dependent_stages = {"bald_detail_match", "hair_match"}
    if dependent_stages.intersection(args.stages) and "bald_geometry" not in args.stages and not BALD_OUTPUT.is_file():
        raise FileNotFoundError(f"Run bald_geometry first: {BALD_OUTPUT.name}")
    report = ROOT / f"p7-5-2-face-front-{'-'.join(args.stages)}-v1-review.json"

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    stage_specs = {
        "character": (OUTPUT, PROMPT, 62282, []),
        "bald_geometry": (BALD_OUTPUT, BALD_PROMPT, 62294, []),
        "bald_detail_match": (BALD_DETAIL_OUTPUT, BALD_DETAIL_PROMPT, 62295, [BALD_OUTPUT, HAIR_REFERENCE]),
        "hair_match": (HAIR_OUTPUT, HAIR_PROMPT, 62291, [BALD_OUTPUT, HAIR_REFERENCE]),
    }
    runs = []
    for stage in args.stages:
        output, prompt, base_seed, references = stage_specs[stage]
        seed = base_seed + args.seed_offset
        if missing := [path.name for path in references if not path.is_file()]:
            raise FileNotFoundError(", ".join(missing))
        started = time.monotonic()
        request = {"prompt": prompt}
        if references:
            request["image"] = [Image.open(path).convert("RGB") for path in references]
        image = pipe(
            **request,
            width=768,
            height=768,
            num_inference_steps=12,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(seed),
            max_sequence_length=256,
        ).images[0]
        image.save(output)
        elapsed = round(time.monotonic() - started, 2)
        runs.append({
            "stage": stage,
            "output": output.name,
            "seed": seed,
            "prompt": prompt,
            "prompt_word_count": prompt_word_count(prompt),
            "references": [path.name for path in references],
            "elapsed_seconds": elapsed,
        })
        print(f"{stage}: {elapsed:.2f}s -> {output}")
    report.write_text(
        json.dumps(
            {
                "status": "review_required",
                "requested_stages": args.stages,
                "seed_offset": args.seed_offset,
                "runs": runs,
                "model": MODEL_ID,
                "image_size": [768, 768],
                "decision": "Candidate only; human review is required before it becomes a front-face or geometry reference.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

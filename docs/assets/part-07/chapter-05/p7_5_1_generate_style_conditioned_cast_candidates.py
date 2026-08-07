#!/usr/bin/env python3
"""Generate review-only character-style candidates from approved P7-5.1 background references.

Each output tests a scene composition. Outputs are independent composition
candidates, not a turnaround or identity proof.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ASSET_DIR = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
BASE_SEED = 62510
TIMESTAMP_FORMAT = "%Y%m%dT%H%M%S%f%z"
COMMON_STYLE_CONTRACT = (
    "Create an edge-to-edge Korean webtoon scene. Do not draw an outer rectangular outline or surround the scene with a dark border. "
    "Use a transparent watercolor-and-ink medium: sparse thin charcoal contour and structure lines contain visible wet-on-wet blooms, uneven pigment pooling, granulating translucent washes, and layered translucent edges. "
    "Make material texture and lighting visibly varied: distinct translucent pigment pools on lit planes, cool shadow planes, and small reflected-light accents remain separately readable, never one uniform teal or gray wash. "
    "Use natural medium-chroma pigment, never neon, fluorescent, opaque, airbrushed, digitally flat, densely hatched, crosshatched, stippled, ink-wash, sumi-e, photorealistic, screentoned, or thick comic outlined. "
)
CAST_PROMPTS = {
    "young_woman_solo": {
        "age_and_gender": "22-year-old Korean woman",
        "prompt": "Depict a 22-year-old Korean woman.",
    },
    "young_man_solo": {
        "age_and_gender": "29-year-old Korean man",
        "prompt": "Depict a 29-year-old Korean man.",
    },
    "adult_pair": {
        "age_and_gender": "27-year-old Korean woman and 34-year-old Korean man",
        "prompt": "Depict a 27-year-old Korean woman and a 34-year-old Korean man.",
    },
    "mixed_age_trio": {
        "age_and_gender": "19-year-old Korean woman, 46-year-old Korean man, and 67-year-old Korean woman",
        "prompt": "Depict a 19-year-old Korean woman, a 46-year-old Korean man, and a 67-year-old Korean woman.",
    },
}
COMPOSITIONS = {
    "street": {
        "size": (768, 1152),
        "prompt": (
            "Urban street with buildings, sidewalks, and an open roadway. Keep the scene edge-to-edge and the subject readable."
        ),
    },
    "cafe": {
        "size": (768, 1152),
        "prompt": (
            "Cafe table scene with windows, floorboards, and a readable person-to-table relationship."
        ),
    },
    "rooftop": {
        "size": (768, 1152),
        "prompt": (
            "Rooftop terrace with open sky, low walls, and a clear usable floor area."
        ),
    },
    "park": {
        "size": (768, 1152),
        "prompt": (
            "Park pond with a path, low railing, foliage, and a readable water edge."
        ),
    },
    "atrium": {
        "size": (768, 1152),
        "prompt": (
            "Indoor atrium with stairs, tile floor, railings, and open walking space; do not make a character turnaround."
        ),
    },
}
STYLE_REFERENCE_BY_COMPOSITION = {
    "street": "p7-5-1-style-downtown-clear-day-wide-local-gpu-v1.png",
    "cafe": "p7-5-1-style-night-lit-reading-room-oblique-local-gpu-v1.png",
    "rooftop": "p7-5-1-style-rooftop-rainy-night-overhead-local-gpu-v1.png",
    "park": "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png",
    "atrium": "p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png",
}
APPROVED_STYLE_REFERENCES = tuple(sorted(set(STYLE_REFERENCE_BY_COMPOSITION.values())))


def prompt_word_count(text: str) -> int:
    return len(text.split())


def build_prompt(cast_id: str, composition_id: str) -> str:
    return f"{COMMON_STYLE_CONTRACT}{CAST_PROMPTS[cast_id]['prompt']} {COMPOSITIONS[composition_id]['prompt']}"


def style_reference_path(composition_id: str, override: str | None) -> Path:
    reference = ASSET_DIR / (override or STYLE_REFERENCE_BY_COMPOSITION[composition_id])
    if not reference.is_file():
        raise FileNotFoundError(reference)
    return reference


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cast", choices=tuple(CAST_PROMPTS), default="young_woman_solo", help="Cast prompt ID with fixed gender and age information.")
    parser.add_argument("--compositions", nargs="+", choices=tuple(COMPOSITIONS), default=("street",), help="Scene-composition conditions to generate as separate review candidates.")
    parser.add_argument("--seed-offset", type=int, default=0)
    parser.add_argument("--seed-count", type=int, default=1)
    parser.add_argument("--seed-step", type=int, default=1)
    parser.add_argument("--steps", type=int, default=50, help="Diffusion iterations per candidate; defaults to the P7-5.1 baseline of 50.")
    parser.add_argument(
        "--style-reference",
        choices=APPROVED_STYLE_REFERENCES,
        help="Approved local-GPU background PNG to use for every requested composition instead of its default matched reference.",
    )
    parser.add_argument("--output-prefix", default="p7-5-1-style-conditioned-cast")
    args = parser.parse_args()

    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")
    if args.steps < 1:
        raise ValueError("steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    pipe = Flux2KleinPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR)
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    timestamp = datetime.now().astimezone().strftime(TIMESTAMP_FORMAT)
    runs = []
    for batch_index in range(args.seed_count):
        seed = BASE_SEED + args.seed_offset + batch_index * args.seed_step
        for composition_id in args.compositions:
            width, height = COMPOSITIONS[composition_id]["size"]
            prompt = build_prompt(args.cast, composition_id)
            style_reference = style_reference_path(composition_id, args.style_reference)
            output = ASSET_DIR / f"{args.output_prefix}-{args.cast}-{composition_id}-{timestamp}-seed-{seed}-candidate.png"
            started = time.monotonic()
            image = pipe(
                image=Image.open(style_reference).convert("RGB"),
                prompt=prompt,
                width=width,
                height=height,
                num_inference_steps=args.steps,
                guidance_scale=4.0,
                generator=torch.Generator(device="cpu").manual_seed(seed),
                max_sequence_length=256,
            ).images[0]
            image.save(output)
            runs.append(
                {
                    "cast": args.cast,
                    "age_and_gender": CAST_PROMPTS[args.cast]["age_and_gender"],
                    "composition": composition_id,
                    "style_reference": style_reference.name,
                    "output": output.name,
                    "seed": seed,
                    "prompt": prompt,
                    "prompt_word_count": prompt_word_count(prompt),
                    "image_size": [width, height],
                    "elapsed_seconds": round(time.monotonic() - started, 2),
                    "status": "review_required",
                }
            )
            torch.cuda.empty_cache()
            print(f"[{batch_index + 1}/{args.seed_count}] {args.cast}/{composition_id} -> {output}")

    report = ASSET_DIR / f"{args.output_prefix}-{args.cast}-{timestamp}-review.json"
    report.write_text(json.dumps({
        "status": "review_required",
        "purpose": "Character-style candidates that test an approved P7-5.1 background image reference and text style contract across scene compositions, genders, and ages.",
        "model": {"id": MODEL_ID, "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload"},
        "style_input": "one_approved_background_png_plus_p7_5_1_text_contract",
        "requested_cast": args.cast,
        "cast": CAST_PROMPTS[args.cast],
        "requested_compositions": args.compositions,
        "composition_prompts": {item: COMPOSITIONS[item]["prompt"] for item in args.compositions},
        "input_policy": "Supply one individual approved local-GPU background PNG as image input for each run. By default it is matched to the requested composition; --style-reference can override that choice for a controlled comparison. The prompt carries the P7-5.1 text style contract, and each output remains an independent composition candidate, not an identity-preserving turnaround.",
        "steps": args.steps,
        "guidance_scale": 4.0,
        "runs": runs,
        "review_checklist": [
            "The cast keeps the P7-5.1 text contract's thin charcoal line role and translucent watercolor layers.",
            "The approved background reference transfers line, pigment, and lighting treatment without making the cast scene a duplicate of the reference location.",
            "The output remains an edge-to-edge single scene without an outer rectangular outline, panel divisions, or a dark border.",
        ],
        "decision": "Candidate only; a person must confirm the P7-5.1 style contract before any output can be used as a cast-style reference.",
    }, indent=2), encoding="utf-8")
    print(f"review record -> {report}")


if __name__ == "__main__":
    main()

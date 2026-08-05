#!/usr/bin/env python3
"""Generate selected prompt-only candidates for Mira's prop references."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
DEFAULT_REPORT = ROOT / "p7-5-2-prop-generation-candidate-review.json"
PROPS = {
    "jacket": {
        "id": "jacket",
        "seed": 62280,
        "output": "p7-5-2-no-style-prop-jacket-candidate.png",
        "size": (768, 1024),
        "prompt": "One isolated white cropped utility jacket in a clean front product view on a plain off-white background. Its short straight body ends at the natural waist: the hem sits immediately below the pocket bottoms, with no lower torso extension. Wide collar, two flap chest pockets, simple front buttons, long sleeves with cuffs, a narrow hem band, and clean seams. Clean product illustration. No person, hanger, text, logo, or other object.",
    },
    "trousers": {
        "id": "trousers",
        "seed": 62281,
        "output": "p7-5-2-no-style-prop-trousers-candidate.png",
        "size": (768, 1024),
        "prompt": "One isolated pair of deep teal blue high-waisted wide-leg trousers in a clean front view on a plain off-white background. Use one blue-dominant dark teal base color, neither green turquoise nor gray. Belt loops, center fly, crisp vertical seams, straight wide legs, and hems above the shoe collar. Clean product illustration. No person, hanger, text, logo, or other object.",
    },
    "shoes": {
        "id": "shoes",
        "seed": 62282,
        "output": "p7-5-2-no-style-prop-shoes-candidate.png",
        "size": (768, 768),
        "prompt": "One matching pair of plain white low-top lace-up sneakers, arranged in a clean three-quarter product view on a plain off-white background. Rounded toe caps, white laces, white rubber soles, and minimal stitching. Clean product illustration. No person, text, logo, or other object.",
    },
    "crossbody_bag": {
        "id": "crossbody_bag",
        "seed": 62283,
        "output": "p7-5-2-no-style-prop-crossbody-bag-candidate.png",
        "size": (768, 768),
        "prompt": "One isolated compact deep-navy woven-canvas crossbody bag in a clean three-quarter front view on a plain off-white background. Small horizontal rounded flap, visible textile weave, stitched seams, reinforced strap tabs, charcoal adjustable canvas strap, and one small silver clasp. Clean product illustration. No leather, person, text, logo, or other object.",
    },
    "gray_cropped_top": {
        "id": "gray_cropped_top",
        "seed": 64929,
        "output": "p7-5-2-no-style-prop-gray-cropped-top-candidate.png",
        "size": (768, 1024),
        "prompt": "Front apparel detail from shoulders through upper hips on a featureless neutral fashion torso against an off-white background. A charcoal-gray regular-fit micro-crop crew-neck T-shirt follows the upper torso with moderate ease: natural shoulder seams at the shoulders, standard short sleeves, clean vertical side seams, and a straight hem. Its hem ends high across the upper abdomen, sixteen centimeters above the navel. Deep teal-blue high-waisted wide-leg trousers have a waistband positioned at the navel. A clear sixteen-centimeter horizontal band of bare midriff visibly separates the cropped hem from the waistband. The short crop length and clean regular fit are the focus. Clean product illustration; no face, hands, text, logo, or other clothing.",
    },
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=tuple(PROPS),
        default=tuple(PROPS),
        help="Prop IDs to generate. Omit to generate jacket, trousers, shoes, crossbody_bag, and gray_cropped_top.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
        help="Candidate review JSON path.",
    )
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    runs = []
    for prop_id in args.targets:
        prop = PROPS[prop_id]
        started = time.monotonic()
        width, height = prop["size"]
        image = pipe(
            prompt=prop["prompt"],
            width=width,
            height=height,
            num_inference_steps=12,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(prop["seed"]),
            max_sequence_length=256,
        ).images[0]
        output = ROOT / prop["output"]
        image.save(output)
        elapsed = round(time.monotonic() - started, 2)
        runs.append(
            {
                "id": prop["id"],
                "output": output.name,
                "prompt": prop["prompt"],
                "seed": prop["seed"],
                "elapsed_seconds": elapsed,
            }
        )
        print(f"{prop['id']}: {elapsed:.2f}s -> {output}")

    args.report.write_text(
        json.dumps(
            {
                "status": "review_required",
                "purpose": "Generate selected prompt-only prop-reference candidates without a style-image or style prompt input.",
                "input_policy": "prompt only; no style, face, character, or existing prop image input",
                "requested_targets": args.targets,
                "model": {"id": MODEL_ID, "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload"},
                "runs": runs,
                "decision": "Pending human review; no candidate replaces the approved prop master until individually approved."
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

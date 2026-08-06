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

JACKET_COMMON_CONTRACT = (
    "One isolated very short white cropped utility jacket in a clean {view} product view "
    "on a plain off-white background. Its body panel ends at the high waist just below "
    "the ribcage, well above the hips; the cropped body is visibly much shorter than the "
    "long sleeves. Wide collar, long sleeves with cuffs, clean side seams, and a short "
    "straight hem. Clean product illustration. No person, hanger, text, logo, bag, or "
    "other object."
)

JACKET_VIEW_CONTRACTS = {
    "front": (
        "Show two flap chest pockets, simple front buttons, a narrow hem band, and clean "
        "front seams."
    ),
    "rear": (
        "Show one uninterrupted plain white back panel, shoulder seams, a centered "
        "center-back seam, and no pockets or buttons."
    ),
}

LAYERED_OUTFIT_COMMON_CONTRACT = (
    "One isolated torso-only apparel layering reference on a plain off-white background. "
    "Show a very short white cropped utility jacket worn open over a charcoal-gray micro-crop "
    "crew-neck top on a neutral headless torso form. The jacket body ends at the high waist just "
    "below the ribcage, well above the hips, and is visibly much shorter than its long cuffed sleeves. "
    "Keep the jacket and crop top as two clearly separate, correctly layered garments. Clean product "
    "illustration. No head, hands, legs, bag, hanger, text, logo, or other object."
)

LAYERED_OUTFIT_VIEW_CONTRACTS = {
    "front": (
        "Use a front view. Show the open jacket's wide collar, two flap chest pockets, simple front "
        "buttons, and narrow hem band; show the gray crop top through the open front and below the jacket hem."
    ),
}

REAR_JACKET_MIDRIFF_CONTRACT = (
    "One isolated torso-only rear apparel reference on a plain off-white background. Show a very short white "
    "cropped utility jacket on a neutral headless torso form. The uninterrupted white back panel has a wide collar, "
    "shoulder seams, a centered back seam, long cuffed sleeves, and a short hem at the high waist. Directly below "
    "the jacket hem, show a clear bare-skin midriff band; no inner shirt or gray fabric is visible from the rear. "
    "Clean product illustration. No head, hands, legs, bag, hanger, text, logo, or other object."
)

COMPLETE_OUTFIT_FRONT_HIP_CONTRACT = (
    "Front apparel-and-bag wearing reference from shoulders through hips on a neutral headless torso, plain "
    "off-white background. Show a very short white cropped utility jacket open over a charcoal-gray micro-crop "
    "crew-neck top, deep teal-blue high-waisted wide-leg trousers, and a compact deep-navy woven-canvas crossbody "
    "bag. The top ends at the upper abdomen, sixteen centimeters above the navel-height trouser waistband, leaving "
    "a clear bare-skin midriff band. Hang the bag side-on beside the wearer's outer left trouser seam (viewer right), "
    "with its top aligned to the waistband. Show one continuous taut strap from the outer wearer's-right shoulder "
    "(viewer left), diagonally across the chest, into the bag's upper inner attachment. Keep distinct garment layers "
    "and correct overlap. Clean "
    "product illustration. No head, hands, legs, text, logo, hanger, or other object."
)

COMPLETE_OUTFIT_REAR_HIP_CONTRACT = (
    "Rear apparel-and-strap wearing reference from shoulders through hips on a neutral headless torso, plain off-white "
    "background. Show a very short white cropped utility jacket with long cuffed sleeves reaching the wrists, deep "
    "teal-blue high-waisted wide-leg trousers, and one deep-navy canvas crossbody strap. Keep a plain white jacket "
    "back panel and a bare-skin midriff band below its short hem, with no inner shirt visible. Show one continuous taut "
    "deep-navy canvas strap from the outer wearer's-right shoulder (viewer right), diagonally across the jacket back, "
    "exiting beyond the left waistband. At the outer left hip, show only a small deep-navy woven-fabric bag corner, "
    "mostly hidden behind the torso. "
    "Keep distinct layers and correct overlap. Clean product illustration. No "
    "head, hands, legs, text, logo, hanger, or other object."
)


def jacket_prompt(view: str) -> str:
    """Keep the garment silhouette shared while isolating view-only construction details."""
    return f"{JACKET_COMMON_CONTRACT.format(view=view)} {JACKET_VIEW_CONTRACTS[view]}"


def layered_outfit_prompt(view: str) -> str:
    """Describe the jacket and crop top together so the body-panel layer is not inferred later."""
    if view == "rear":
        return REAR_JACKET_MIDRIFF_CONTRACT
    return f"{LAYERED_OUTFIT_COMMON_CONTRACT} {LAYERED_OUTFIT_VIEW_CONTRACTS[view]}"


PROPS = {
    "jacket": {
        "id": "jacket",
        "seed": 62280,
        "output": "p7-5-2-no-style-prop-jacket-candidate.png",
        "size": (768, 1024),
        "prompt": jacket_prompt("front"),
    },
    "jacket_rear": {
        "id": "jacket_rear",
        "seed": 62284,
        "output": "p7-5-2-no-style-prop-jacket-rear-candidate.png",
        "size": (768, 1024),
        "prompt": jacket_prompt("rear"),
    },
    "jacket_crop_top_front": {
        "id": "jacket_crop_top_front",
        "seed": 62285,
        "output": "p7-5-2-no-style-prop-jacket-crop-top-front-candidate.png",
        "size": (768, 1024),
        "prompt": layered_outfit_prompt("front"),
    },
    "jacket_crop_top_rear": {
        "id": "jacket_crop_top_rear",
        "seed": 62286,
        "output": "p7-5-2-no-style-prop-jacket-crop-top-rear-candidate.png",
        "size": (768, 1024),
        "prompt": layered_outfit_prompt("rear"),
    },
    "complete_outfit_front_hip": {
        "id": "complete_outfit_front_hip",
        "seed": 62287,
        "output": "p7-5-2-no-style-prop-complete-outfit-front-hip-candidate.png",
        "size": (768, 1152),
        "prompt": COMPLETE_OUTFIT_FRONT_HIP_CONTRACT,
    },
    "complete_outfit_rear_hip": {
        "id": "complete_outfit_rear_hip",
        "seed": 62288,
        "output": "p7-5-2-no-style-prop-complete-outfit-rear-hip-candidate.png",
        "size": (768, 1152),
        "prompt": COMPLETE_OUTFIT_REAR_HIP_CONTRACT,
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
    "crop_top_waist_relation": {
        "id": "crop_top_waist_relation",
        "seed": 64929,
        "output": "p7-5-2-no-style-prop-gray-cropped-top-candidate.png",
        "size": (768, 1024),
        "prompt": "Front apparel detail from shoulders through upper hips on a featureless neutral fashion torso against an off-white background. A charcoal-gray regular-fit micro-crop crew-neck T-shirt follows the upper torso with moderate ease: natural shoulder seams at the shoulders, standard short sleeves, clean vertical side seams, and a straight hem. Its hem ends high across the upper abdomen, sixteen centimeters above the navel. Deep teal-blue high-waisted wide-leg trousers have a waistband positioned at the navel. A clear sixteen-centimeter horizontal band of bare midriff visibly separates the cropped hem from the waistband. The short crop length and clean regular fit are the focus. Clean product illustration; no face, hands, text, logo, or other clothing.",
    },
}


def prompt_word_count(text: str) -> int:
    return len(text.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=tuple(PROPS),
        default=tuple(PROPS),
        help=(
            "Reference IDs to generate. Omit to generate every individual, layered, and complete outfit reference."
        ),
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
                "prompt_word_count": prompt_word_count(prop["prompt"]),
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

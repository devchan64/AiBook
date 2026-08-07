#!/usr/bin/env python3
"""Generate selected no-style candidates for Mira's prop references."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image
from p7_5_image_output_naming import candidate_stem, preview_callback


ROOT = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
PROP_SEED = 62294
DEFAULT_REPORT = ROOT / "p7-5-2-prop-generation-candidate-review.json"
CROP_TOP_WAIST_REFERENCE = ROOT / "p7-5-2-outfit-crop-top-waist-reference.png"

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
    "Front apparel-and-bag reference from shoulders through hips, on a neutral headless torso and off-white background. "
    "Wear a very short white cropped utility jacket as the closed outer layer; its white front panels cover the chest. "
    "Show a charcoal-gray micro-crop only below the jacket hem, with a bare midriff band above deep teal-blue high-waisted "
    "wide-leg trousers. Place one compact deep-navy woven-canvas crossbody bag at the wearer's outer-left hip (viewer right). "
    "Its strap is the exact same deep navy as the bag. Show exactly one taut diagonal strap: it starts only at the wearer's "
    "right shoulder (viewer left), crosses white jacket shoulder, collar, lapel, and front panel, then joins the bag. Keep "
    "the jacket front panel directly beneath the strap white and closed. Never show the strap on the gray top, in the open "
    "center, behind the jacket, from the viewer-right shoulder, or as a loose navy patch, second strap, or shoulder pad on "
    "the viewer-right shoulder. Clean product "
    "illustration; no head, text, logo, hanger, or extra object."
)

COMPLETE_OUTFIT_REAR_HIP_CONTRACT = (
    "Rear apparel-and-strap wearing reference from shoulders through hips on a neutral headless torso, plain off-white "
    "background. Show a very short white cropped utility jacket with long cuffed sleeves reaching the wrists, deep "
    "teal-blue wide-leg trousers with a clearly high waist: the full waistband sits at the navel, well above the hips, "
    "and stays visible, plus one deep-navy woven-canvas crossbody strap matching the bag body exactly. Keep a plain white jacket back panel and a bare-skin "
    "midriff band below its short hem, with no inner shirt visible. Show one continuous taut "
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
        "seed": PROP_SEED,
        "output": "p7-5-2-no-style-prop-jacket-candidate.png",
        "size": (768, 1024),
        "prompt": jacket_prompt("front"),
    },
    "jacket_rear": {
        "id": "jacket_rear",
        "seed": PROP_SEED,
        "output": "p7-5-2-no-style-prop-jacket-rear-candidate.png",
        "size": (768, 1024),
        "prompt": jacket_prompt("rear"),
    },
    "jacket_crop_top_front": {
        "id": "jacket_crop_top_front",
        "seed": PROP_SEED,
        "output": "p7-5-2-no-style-prop-jacket-crop-top-front-candidate.png",
        "size": (768, 1024),
        "references": (CROP_TOP_WAIST_REFERENCE,),
        "prompt": (
            f"{layered_outfit_prompt('front')} Use the supplied crop-top-to-waistband reference as the authoritative "
            "length contract for the gray crop top: keep its high hem and exposed midriff band; do not lengthen it to "
            "the trouser waistband, navel, hips, or below the upper abdomen."
        ),
    },
    "jacket_crop_top_rear": {
        "id": "jacket_crop_top_rear",
        "seed": PROP_SEED,
        "output": "p7-5-2-no-style-prop-jacket-crop-top-rear-candidate.png",
        "size": (768, 1024),
        "prompt": layered_outfit_prompt("rear"),
    },
    "complete_outfit_front_hip": {
        "id": "complete_outfit_front_hip",
        "seed": PROP_SEED,
        "output": "p7-5-2-no-style-prop-complete-outfit-front-hip-candidate.png",
        "size": (768, 1152),
        "references": (
            CROP_TOP_WAIST_REFERENCE,
        ),
        "prompt": (
            f"{COMPLETE_OUTFIT_FRONT_HIP_CONTRACT} Use the supplied crop-top-to-waistband reference as the authoritative "
            "gray crop-top length contract. Keep its high hem and exposed midriff band; do not lengthen it to the trouser "
            "waistband, navel, hips, or below the upper abdomen."
        ),
    },
    "complete_outfit_rear_hip": {
        "id": "complete_outfit_rear_hip",
        "seed": PROP_SEED,
        "output": "p7-5-2-no-style-prop-complete-outfit-rear-hip-candidate.png",
        "size": (768, 1152),
        "prompt": COMPLETE_OUTFIT_REAR_HIP_CONTRACT,
    },
    "trousers": {
        "id": "trousers",
        "seed": PROP_SEED,
        "output": "p7-5-2-no-style-prop-trousers-candidate.png",
        "size": (768, 1024),
        "prompt": "One isolated pair of deep teal blue high-waisted wide-leg trousers in a clean front view on a plain off-white background. Use one blue-dominant dark teal base color, neither green turquoise nor gray. Belt loops, center fly, crisp vertical seams, straight wide legs, and hems above the shoe collar. Clean product illustration. No person, hanger, text, logo, or other object.",
    },
    "shoes": {
        "id": "shoes",
        "seed": PROP_SEED,
        "output": "p7-5-2-no-style-prop-shoes-candidate.png",
        "size": (768, 768),
        "prompt": "One matching pair of plain white low-top lace-up sneakers, arranged in a clean three-quarter product view on a plain off-white background. Rounded toe caps, white laces, white rubber soles, and minimal stitching. Clean product illustration. No person, text, logo, or other object.",
    },
    "crossbody_bag": {
        "id": "crossbody_bag",
        "seed": PROP_SEED,
        "output": "p7-5-2-no-style-prop-crossbody-bag-candidate.png",
        "size": (768, 768),
        "prompt": "One isolated compact deep-navy woven-canvas crossbody bag in a clean three-quarter front view on a plain off-white background. Small horizontal rounded flap, visible textile weave, stitched seams, reinforced strap tabs, a deep-navy woven-canvas adjustable strap exactly matching the bag body's color and fabric, and one small silver clasp. No charcoal, black, gray, or differently colored strap. Clean product illustration. No leather, person, text, logo, or other object.",
    },
    "crop_top_waist_relation": {
        "id": "crop_top_waist_relation",
        "seed": PROP_SEED,
        "output": "p7-5-2-no-style-prop-gray-cropped-top-candidate.png",
        "size": (768, 1024),
        "prompt": "Front apparel detail from shoulders through upper hips on a featureless neutral fashion torso against an off-white background. A charcoal-gray regular-fit ultra-short micro-crop crew-neck T-shirt follows the upper torso with moderate ease: natural shoulder seams at the shoulders, standard short sleeves, clean vertical side seams, and a straight hem. Its hem ends immediately below the lower ribcage, twenty centimeters above the navel-height trouser waistband. Deep teal-blue high-waisted wide-leg trousers have a waistband positioned at the navel. A clear twenty-centimeter horizontal band of bare midriff visibly separates the cropped hem from the waistband. Treat this ultra-short crop hem and wide bare-midriff band as mandatory geometry: do not lengthen the crop top to the waistband, navel, hips, upper abdomen, or below the lower ribcage, and do not reduce or remove the exposed band. The ultra-short crop length and clean regular fit are the focus. Clean product illustration; no face, hands, text, logo, or other clothing.",
    },
}

# Generate reusable individual masters first so later layered and complete-outfit
# candidates can consume the PNGs created in this same invocation.
GENERATION_ORDER = (
    "shoes",
    "crossbody_bag",
    "trousers",
    "jacket",
    "jacket_rear",
    "crop_top_waist_relation",
    "jacket_crop_top_front",
    "jacket_crop_top_rear",
    "complete_outfit_front_hip",
    "complete_outfit_rear_hip",
)
GENERATED_REFERENCE_DEPENDENCIES = {
    "jacket_crop_top_front": ("jacket",),
    "jacket_crop_top_rear": ("jacket_rear",),
    "complete_outfit_front_hip": ("crossbody_bag", "trousers", "jacket"),
    "complete_outfit_rear_hip": ("crossbody_bag", "trousers", "jacket_rear"),
}


def prompt_word_count(text: str) -> int:
    return len(text.split())


def load_reference_images(paths: tuple[Path, ...]) -> list[Image.Image]:
    """Load the stable and same-run generated inputs for a prop candidate."""
    images = []
    for path in paths:
        with Image.open(path) as source:
            images.append(source.convert("RGB"))
    return images


def resolve_generation_targets(
    requested_targets: tuple[str, ...], provided_prerequisites: set[str]
) -> tuple[str, ...]:
    """Expand selected targets with prerequisites and return the fixed dependency order."""
    selected = set(requested_targets)
    pending = list(requested_targets)
    while pending:
        prop_id = pending.pop()
        for dependency in GENERATED_REFERENCE_DEPENDENCIES.get(prop_id, ()):
            if dependency not in selected and dependency not in provided_prerequisites:
                selected.add(dependency)
                pending.append(dependency)
    return tuple(prop_id for prop_id in GENERATION_ORDER if prop_id in selected)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=tuple(PROPS),
        default=GENERATION_ORDER,
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
    parser.add_argument(
        "--prop-reference",
        action="append",
        type=Path,
        default=[],
        metavar="PATH",
        help="Additional PNG input applied to each explicitly requested target, not its generated prerequisites.",
    )
    parser.add_argument(
        "--prerequisite-reference",
        action="append",
        default=[],
        metavar="ID=PATH",
        help="Use an existing prerequisite PNG instead of regenerating that prop, for example crossbody_bag=bag.png.",
    )
    parser.add_argument("--steps", type=int, default=3, help="Number of FLUX denoising steps for every selected prop.")
    parser.add_argument("--preview-every", type=int, default=0, help="Save a decoded preview every N denoising steps; 0 disables previews.")
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("steps must be at least 1")
    requested_target_ids = set(args.targets)
    prerequisite_references: dict[str, Path] = {}
    for assignment in args.prerequisite_reference:
        try:
            prop_id, raw_path = assignment.split("=", maxsplit=1)
        except ValueError as exc:
            raise ValueError("--prerequisite-reference must use ID=PATH") from exc
        if prop_id not in PROPS:
            raise ValueError(f"Unknown prerequisite prop ID: {prop_id}")
        if prop_id in prerequisite_references:
            raise ValueError(f"Duplicate prerequisite prop ID: {prop_id}")
        path = Path(raw_path)
        prerequisite_references[prop_id] = path if path.is_absolute() else ROOT / path
    targets = resolve_generation_targets(tuple(args.targets), set(prerequisite_references))
    extra_prop_references = tuple(
        path if path.is_absolute() else ROOT / path
        for path in args.prop_reference
    )

    missing = [
        path.name
        for prop_id in targets
        for path in PROPS[prop_id].get("references", ())
        if not path.is_file()
    ]
    missing.extend(path.name for path in extra_prop_references if not path.is_file())
    missing.extend(path.name for path in prerequisite_references.values() if not path.is_file())
    if missing:
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

    runs = []
    generated_outputs: dict[str, Path] = dict(prerequisite_references)
    for prop_id in targets:
        prop = PROPS[prop_id]
        started = time.monotonic()
        width, height = prop["size"]
        generated_reference_paths = tuple(
            generated_outputs[dependency]
            for dependency in GENERATED_REFERENCE_DEPENDENCIES.get(prop_id, ())
        )
        explicit_prop_references = extra_prop_references if prop_id in requested_target_ids else ()
        reference_paths = (*prop.get("references", ()), *generated_reference_paths, *explicit_prop_references)
        output_stem = candidate_stem(
            Path(prop["output"]).stem,
            seed=prop["seed"],
            steps=args.steps,
            contract={
                "model": MODEL_ID,
                "prompt": prop["prompt"],
                "references": [path.name for path in reference_paths],
                "size": prop["size"],
                "steps": args.steps,
            },
        )
        generation_inputs = {
            "prompt": prop["prompt"],
            "width": width,
            "height": height,
            "num_inference_steps": args.steps,
            "guidance_scale": 1.0,
            "generator": torch.Generator(device="cpu").manual_seed(prop["seed"]),
            "max_sequence_length": 256,
        }
        if reference_paths:
            generation_inputs["image"] = load_reference_images(reference_paths)
        generation_inputs["callback_on_step_end"] = preview_callback(
            pipe,
            height=height,
            width=width,
            every=args.preview_every,
            directory=ROOT / "previews",
            prefix=output_stem,
        )
        image = pipe(**generation_inputs).images[0]
        output = ROOT / f"{output_stem}.png"
        image.save(output)
        generated_outputs[prop_id] = output
        elapsed = round(time.monotonic() - started, 2)
        runs.append(
            {
                "id": prop["id"],
                "output": output.name,
                "prompt": prop["prompt"],
                "prompt_word_count": prompt_word_count(prop["prompt"]),
                "seed": prop["seed"],
                "steps": args.steps,
                "references": [path.name for path in reference_paths],
                "elapsed_seconds": elapsed,
            }
        )
        print(f"{prop['id']}: {elapsed:.2f}s -> {output}")

    args.report.write_text(
        json.dumps(
            {
                "status": "review_required",
                "purpose": "Generate selected no-style prop-reference candidates.",
                "input_policy": "No style, face, or character input. The front layered and complete-outfit targets may use the approved crop-top-to-waistband reference.",
                "requested_targets": args.targets,
                "generation_order": targets,
                "additional_prop_references": [path.name for path in extra_prop_references],
                "prerequisite_references": {
                    prop_id: path.name for prop_id, path in prerequisite_references.items()
                },
                "steps": args.steps,
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

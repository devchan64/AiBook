"""Run P7-5.3 Scene A/B/C with a structure guide and Qwen Edit."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import torch
from diffusers import QwenImageEditPlusPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel

# This executable is a retained Part 7 asset; shared local-run helpers remain
# in .tmp because they describe the local runtime rather than book content.
ROOT = Path(__file__).resolve().parents[4]
TMP_HELPERS = ROOT / ".tmp"
if str(TMP_HELPERS) not in sys.path:
    sys.path.insert(0, str(TMP_HELPERS))

from p7_5_4_qwen_experiment_utils import asset_record, runtime_record, sha256


OUT = ROOT / "docs" / "assets" / "part-07" / "chapter-05" / "p7-5-4-qwen-edit-grid-output"
SUBJECT = ROOT / "docs/assets/part-07/chapter-05/p7-5-2-face-front-reference.png"
# The approved front full-body reference already shows the inner shirt, bag,
# strap, trousers, and shoes.  Do not default to the older hip crop, which
# cannot establish those full-outfit relationships.
OUTFIT = ROOT / "docs/assets/part-07/chapter-05/p7-5-2-fullbody-front-refined-reference.png"
STORYBOARD = {
    scene: {
        "storyboard-depth": ROOT / f"docs/assets/part-07/chapter-05/p7-5-3-scene-{scene}-approved-storyboard-depth.png",
        "storyboard-rgb": ROOT / f"docs/assets/part-07/chapter-05/p7-5-3-scene-{scene}-approved-storyboard-rgb.png",
    }
    for scene in ("a", "b", "c")
}
IDENTITY_CONTRACT = ROOT / "docs/assets/part-07/chapter-05/p7-5-2-character-identity-contract.json"

# Do not duplicate character wording per scene.  The approved reference sheet,
# not a long textual restatement, is the identity and outfit source of truth.
# The contract is retained in the run record for traceability.
COMMON_CHARACTER_PROMPT = (
    "Use image 1 only as the exact face and hair identity reference. "
    "Preserve the visible face shape, both equal orange-amber irises, and the petrol-teal jaw-length bob from image 1. "
    "Do not copy image 1's background or camera."
)
COMMON_STYLE_PROMPT = (
    "Use image 3 only as the approved P7-5.1 rendering reference: off-white paper, sparse charcoal contours, "
    "transparent wet-on-wet washes, pigment pooling, granulation, and translucent edges. Do not copy image 3's "
    "scene, subject, pose, or camera; never photorealistic."
)
COMMON_OUTFIT_PROMPT = (
    "Use image 3 only as the exact complete outfit reference for image 1: preserve the white cropped jacket over the gray inner top, "
    "wide-leg petrol-teal trousers, white low-top sneakers, navy crossbody bag, and its strap outside the jacket. "
    "Do not copy image 3's pose, camera, or background."
)
COMMON_OUTFIT_STYLE_PROMPT = (
    "Use image 3's left panel only as image 1's exact complete outfit reference: preserve the white cropped jacket over the gray inner top, "
    "wide-leg petrol-teal trousers, white low-top sneakers, navy crossbody bag, and its strap outside the jacket. "
    "Use image 3's right panel only for the approved rendering: off-white paper, sparse charcoal contours, transparent wet-on-wet washes, "
    "pigment pooling, granulation, and translucent edges. Do not copy either panel's pose, camera, background, or scene; never photorealistic."
)
SCENE_STRUCTURE_PROMPTS = {
    "a": (
        "Use image 2 only for a wide low-angle view from near the canyon floor looking slightly upward through a broad pale sandstone canyon "
        "with visible spaced walls, one full-body airborne split leap facing right, and clear ground around her."
    ),
    "b": (
        "Use image 2 only for a very wide, gently elevated establishing view over a vast pale sandstone plain, low horizon, "
        "small distant rocks, centered uncropped full-body airborne split leap facing right, and ample empty ground."
    ),
    "c": (
        "Use image 2 only for a vertical overhead view, full-body airborne split leap facing right with both arms extended sideways, "
        "legs split, a detached full-body cast shadow, and loose gravel ground."
    ),
}

PROMPTS = {
    "a": (
        "Keep image 1's wide low-angle camera from near the canyon floor, broad pale sandstone canyon, visible spaced canyon walls, "
        "full-body airborne split leap, and clear ground around the dancer. Depict image 2's woman with her "
        "petrol-teal jaw-length bob and both amber irises in that composition. Use image 3 only as the exact outfit "
        "reference: white cropped jacket, wide-leg petrol-teal trousers, white low-top sneakers, navy crossbody bag, "
        "and the bag strap outside the jacket. Illustrated watercolor on off-white paper, sparse charcoal contours, "
        "transparent wet-on-wet washes, pigment pooling, granulation, and translucent edges; never photorealistic."
    ),
    "b": (
        "Keep image 1's very wide elevated establishing camera, vast pale sandstone plain, low horizon, small distant rocks, "
        "full-body airborne split leap, centered uncropped dancer, and ample empty ground around her. Depict image 2's woman "
        "with her petrol-teal jaw-length bob and both amber irises in that composition. Use image 3 only as the exact outfit "
        "reference: white cropped jacket, wide-leg petrol-teal trousers, white low-top sneakers, navy crossbody bag, and the bag "
        "strap outside the jacket. Illustrated watercolor on off-white paper, sparse charcoal contours, transparent wet-on-wet "
        "washes, pigment pooling, granulation, and translucent edges; never photorealistic."
    ),
    "c": (
        "Keep image 1's vertical overhead camera, full-body airborne split leap with both arms extended sideways, "
        "legs split, detached cast shadow, and loose gravel ground. Depict image 2's woman with her petrol-teal "
        "jaw-length bob and both amber irises in that composition. Use image 3 only as the exact outfit reference: "
        "white cropped jacket, wide-leg petrol-teal trousers, white low-top sneakers, navy crossbody bag, and the bag "
        "strap outside the jacket. Illustrated watercolor on off-white paper, sparse charcoal contours, transparent "
        "wet-on-wet washes, pigment pooling, granulation, and translucent edges; never photorealistic."
    ),
}

CHARACTER_FIRST_PROMPTS = {
    scene: f"{COMMON_CHARACTER_PROMPT} {SCENE_STRUCTURE_PROMPTS[scene]}"
    for scene in ("a", "b", "c")
}


def pipeline() -> QwenImageEditPlusPipeline:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(
        "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
    )
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        "Qwen/Qwen-Image-Edit-2509", transformer=transformer, torch_dtype=torch.bfloat16
    )
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipe._exclude_from_cpu_offload.append("transformer")
    pipe.enable_sequential_cpu_offload()
    return pipe


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", choices=("a", "b", "c"), required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--height", type=int, default=1024, help="Output height; must be compatible with the Qwen latent grid.")
    parser.add_argument("--width", type=int, default=1024, help="Output width; must be compatible with the Qwen latent grid.")
    parser.add_argument("--guide", type=Path, help="Explicit structure image; overrides --structure-source.")
    parser.add_argument(
        "--structure-source", choices=("controlnet-rgb", "storyboard-depth", "storyboard-rgb"),
        default="storyboard-depth",
        help="Structure reference role. Defaults to the approved storyboard depth; storyboard-* passes the approved source directly as an Edit reference, not native ControlNet.",
    )
    parser.add_argument("--subject", type=Path, help="Optional replacement for the single-view face reference.")
    parser.add_argument("--style-reference", type=Path, help="Approved P7-5.1 style image; uses the third Qwen image slot.")
    parser.add_argument("--outfit-style-reference", type=Path, help="A two-panel third image: left=outfit, right=approved rendering style.")
    parser.add_argument("--repair-source", type=Path, help="Completed scene to preserve while repairing only the character appearance.")
    parser.add_argument("--repair-outfit-reference", type=Path, help="Complete outfit reference for --repair-source; defaults to the approved full-body reference.")
    parser.add_argument("--repair-style-reference", type=Path, help="Approved rendering reference for --repair-source.")
    parser.add_argument("--route", help="Optional output route label; use when a controlled variant would otherwise overwrite an earlier result.")
    parser.add_argument("--no-outfit", action="store_true", help="Use a complete character sheet and omit the separate outfit input; image 3 remains available for --style-reference.")
    parser.add_argument("--character-first", action="store_true", help="Put the character reference before the structure guide.")
    args = parser.parse_args()
    if args.height <= 0 or args.width <= 0 or args.height % 16 or args.width % 16:
        raise ValueError("--height and --width must be positive multiples of 16")
    if args.guide:
        guide = args.guide.resolve()
        structure_source = "explicit-guide"
    elif args.structure_source == "controlnet-rgb":
        guide = ROOT / ".tmp/p7-5-4-qwen-edit-p753-structure-guide" / f"scene-{args.scene}-identity-free-watercolor-structure-guide.png"
        structure_source = args.structure_source
    else:
        guide = STORYBOARD[args.scene][args.structure_source]
        structure_source = args.structure_source
    if not guide.is_file():
        raise FileNotFoundError(guide)
    subject = args.subject.resolve() if args.subject else SUBJECT
    if not subject.is_file():
        raise FileNotFoundError(subject)
    style = args.style_reference.resolve() if args.style_reference else None
    outfit_style = args.outfit_style_reference.resolve() if args.outfit_style_reference else None
    repair_source = args.repair_source.resolve() if args.repair_source else None
    repair_outfit = args.repair_outfit_reference.resolve() if args.repair_outfit_reference else OUTFIT
    repair_style = args.repair_style_reference.resolve() if args.repair_style_reference else None
    if style and not style.is_file():
        raise FileNotFoundError(style)
    if outfit_style and not outfit_style.is_file():
        raise FileNotFoundError(outfit_style)
    if repair_source and not repair_source.is_file():
        raise FileNotFoundError(repair_source)
    if args.repair_source and not repair_outfit.is_file():
        raise FileNotFoundError(repair_outfit)
    if repair_style and not repair_style.is_file():
        raise FileNotFoundError(repair_style)
    if style and outfit_style:
        raise ValueError("--style-reference and --outfit-style-reference are mutually exclusive")
    if style and (not args.no_outfit or not args.character_first):
        raise ValueError("--style-reference requires --no-outfit and --character-first: image 1=character, image 2=structure, image 3=style")
    if outfit_style and (args.no_outfit or not args.character_first):
        raise ValueError("--outfit-style-reference requires --character-first without --no-outfit")
    if repair_source and not repair_style:
        raise ValueError("--repair-source requires --repair-style-reference: image 1=locked base, image 2=outfit, image 3=style")
    started = time.monotonic()
    prompt = PROMPTS[args.scene] if not args.no_outfit else (
        "Keep image 1's wide low-angle camera from near the canyon floor, broad pale sandstone canyon, visible spaced canyon walls, full-body airborne split leap, and clear ground around the dancer. Depict image 2's exact same woman, outfit, bag and strap in that composition. Illustrated watercolor on off-white paper, sparse charcoal contours, transparent wet-on-wet washes, pigment pooling, granulation, and translucent edges; never photorealistic."
    )
    inputs = (guide, subject) if args.no_outfit else (guide, subject, OUTFIT)
    if args.character_first:
        inputs = (subject, guide) if args.no_outfit else (subject, guide, OUTFIT)
        prompt = CHARACTER_FIRST_PROMPTS[args.scene]
        if not args.no_outfit:
            prompt += f" {COMMON_OUTFIT_PROMPT}"
    if style:
        inputs = (subject, guide, style)
        prompt += f" {COMMON_STYLE_PROMPT}"
    if outfit_style:
        inputs = (subject, guide, outfit_style)
        prompt = f"{CHARACTER_FIRST_PROMPTS[args.scene]} {COMMON_OUTFIT_STYLE_PROMPT}"
    if repair_source:
        inputs = (repair_source, repair_outfit, repair_style)
        prompt = (
            "Use image 1 as the locked base image. Preserve its exact low-angle canyon composition, airborne split pose, "
            "camera, background, face, hair, and all unmentioned pixels. Modify only the existing character's clothing and accessories. "
            "Use image 2 as the exact complete outfit reference: white cropped jacket over a gray inner top, visibly wide-leg petrol-teal trousers "
            "through both legs, white low-top sneakers, navy crossbody bag, and the bag strap outside the jacket. "
            "Use image 3 only for off-white paper, sparse charcoal contours, transparent wet-on-wet washes, pigment pooling, granulation, "
            "and translucent edges. Never photorealistic; do not add objects or alter the canyon."
        )
    result = pipeline()(
        image=[load_image(str(path)).convert("RGB") for path in inputs],
        prompt=prompt, generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0, negative_prompt=" ", num_inference_steps=args.steps, guidance_scale=1.0,
        height=args.height, width=args.width,
    ).images[0]
    OUT.mkdir(parents=True, exist_ok=True)
    route = args.route or ("controlnet-guide-face-sheet" if args.subject else ("controlnet-guide-edit" if args.guide else "b2"))
    stem = f"scene-{args.scene}-{route}-seed-{args.seed}-steps-{args.steps}"
    output = OUT / f"{stem}.png"
    result.save(output)
    record = {
        "status": "completed", "experiment_id": f"p7-5-4-qwen-scene-{args.scene}-{route}",
        "scene": args.scene.upper(), "model": "Qwen-Image-Edit-2509 with Nunchaku FP4 r128",
        "runtime": runtime_record(), "inputs": {"structure_reference": asset_record(guide), "subject": asset_record(subject), "identity_contract": asset_record(IDENTITY_CONTRACT), "outfit": asset_record(OUTFIT) if not args.no_outfit else None, "style_reference": asset_record(style) if style else None, "outfit_style_reference": asset_record(outfit_style) if outfit_style else None, "repair_source": asset_record(repair_source) if repair_source else None, "repair_outfit_reference": asset_record(repair_outfit) if repair_source else None, "repair_style_reference": asset_record(repair_style) if repair_style else None},
        "structure_source": structure_source,
        "seed": args.seed, "steps": args.steps, "height": args.height, "width": args.width,
        "true_cfg_scale": 4.0, "guidance_scale": 1.0,
        "negative_prompt": " ", "prompt": prompt, "prompt_word_count": len(prompt.split()), "output": str(output),
        "output_sha256": sha256(output), "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    (OUT / f"{stem}-run.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    review = {"status": "human_review_pending", "experiment_id": record["experiment_id"], "scene": args.scene.upper(), "seed": args.seed, "output": asset_record(output), "contracts": {"structure": "pending", "identity": "pending", "outfit": "pending", "style": "pending"}, "failure_observations": [], "decision": "Do not promote before human review."}
    (OUT / f"{stem}-human-review.json").write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n")
    print(output)


if __name__ == "__main__":
    main()

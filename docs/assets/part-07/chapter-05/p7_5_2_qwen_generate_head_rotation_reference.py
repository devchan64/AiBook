#!/usr/bin/env python3
"""Generate review-only Qwen Edit candidates for rotated head references.

The approved frontal head is always the only identity input.  A separately
approved structure map can be supplied with ``--structure-guide`` for an
explicit ablation; it is never synthesized by this script.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path

import torch
from diffusers import QwenImageEditPlusPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
PLAN = ASSETS / "p7-5-2-qwen-edit-transition-plan.json"
IDENTITY_CONTRACT = ASSETS / "p7-5-2-character-identity-contract.json"
STYLE_CONTRACT = ASSETS / "p7-5-2-character-reference-style-prompt-contract.json"
ILLUSTRATION_CONTRACT = ASSETS / "p7-5-2-character-reference-illustration-prompt-contract.json"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
FRONT_HEAD_REFERENCE = ASSETS / "p7-5-2-face-front-qwen-role-separated-reference.png"
# Candidate filenames identify their generator and run; do not create a
# separate candidate directory.
OUTPUT_DIR = ASSETS
DEFAULT_STEPS = 30
SIZE = (768, 768)
TARGET_SIZES = {
    "torso_front": (768, 1152),
    "torso_quarter_right": (768, 1152),
    "upperbody_profile_right": (768, 1024),
    "torso_profile_right": (768, 1152),
}
ROTATIONS = {
    "profile_left": (
        "Turn Image 1 into a left profile head portrait. The face points image left. Head and shoulders only, plain background."
    ),
    "profile_right": (
        "Turn Image 1 into a right profile head portrait. The face points image right. Head and shoulders only, plain background."
    ),
    "upperbody_profile_right": (
        "Image 1 supplies only the same woman's identity and rendering. Redraw her in a strict right-facing upper-body profile: nose, lips, chest, and shoulders point image right. "
        "Frame from the hair crown to below the waist, with the complete head, neck, both shoulders, upper torso, and one relaxed arm visible. "
        "Keep the compact oval face, high straight nose, amber iris, petrol-teal bob, cool blue-gray studio background, and one person. No text, panel, collage, bag, or scene."
    ),
    "torso_front": (
        "Image 1 supplies only the same woman's identity and rendering. Redraw her in a strict frontal torso view: face, chest, waist, and hips face the camera. "
        "Frame from hair crown to hips. Show the complete head, compact neck, both shoulders, ribcage, waist, hips, and both arms; one arm hangs naturally beside the torso. "
        "She wears an ultra-short white cropped utility jacket with long sleeves over a gray crop top, with a small bare midriff. Keep the compact oval face, high straight nose, amber iris, petrol-teal bob, cool blue-gray studio background, and one person. "
        "No text, panel, collage, bag, or scene."
    ),
    "torso_quarter_right": (
        "Image 1 supplies only the same woman's identity and rendering. Redraw her at yaw +45 degrees in a clear right front-quarter torso view: nose, lips, chest, waist, and hips point image right. "
        "Frame from hair crown to hips. Show the complete head, compact neck, both shoulders, ribcage, waist, hips, and both arms; one arm hangs naturally beside the torso. "
        "She wears an ultra-short white cropped utility jacket with long sleeves over a gray crop top, with a small bare midriff. Keep the compact oval face, high straight nose, amber iris, petrol-teal bob, cool blue-gray studio background, and one person. "
        "No text, panel, collage, bag, or scene."
    ),
    "torso_profile_right": (
        "Image 1 supplies only the same woman's identity and rendering. Redraw her in a strict right-facing torso profile: nose, lips, chest, waist, and hips point image right. "
        "Frame from hair crown to hips. Show the complete head, compact neck, both shoulders, ribcage, waist, hips, and both arms; one arm hangs naturally beside the torso. "
        "She wears an ultra-short white cropped utility jacket with long sleeves over a gray crop top, with a small bare midriff. Keep the compact oval face, high straight nose, amber iris, petrol-teal bob, cool blue-gray studio background, and one person. "
        "No text, panel, collage, bag, or scene."
    ),
    "quarter_left": (
        "Image 1 supplies only the same woman's identity and rendering: compact oval face, high straight nose, amber irises, line work, "
        "contrast, shading, and the exact petrol-teal/image-left plus near-black/image-right bob with high crown, loose S-waves, and inward-curled ends. "
        "Do not copy Image 1's frontal camera pose or facial symmetry. Redraw her at yaw -45 degrees, a clear left front-quarter: nose and lips point "
        "image left; the near image-right eye, cheek, and jaw are wider; the far image-left eye is narrower behind the nose bridge. Both eyes remain visible. "
        "Never output a frontal face. Crown-to-collarbone crop, cool blue-gray studio background, no body, outfit, bag, text, panel, or scene."
    ),
}
MINIMAL_ROTATIONS = {
    "profile_left": "Turn Image 1 into a left profile head portrait. The face points image left. Head and shoulders only, plain background.",
    "profile_right": "Turn Image 1 into a right profile head portrait. The face points image right. Head and shoulders only, plain background.",
    "upperbody_profile_right": "Turn Image 1 into a strict right-facing upper-body profile from hair crown to below the waist. Show the complete head, neck, shoulders, upper torso, and one relaxed arm. Plain background.",
    "torso_front": "Turn Image 1 into a strict frontal torso view from hair crown to hips. Show the complete head, neck, shoulders, torso, hips, and both arms. Plain background.",
    "torso_quarter_right": "Turn Image 1 into a clear right front-quarter torso view at yaw +45 degrees from hair crown to hips. Show the complete head, neck, shoulders, torso, hips, and both arms. Plain background.",
    "torso_profile_right": "Turn Image 1 into a strict right-facing upper-body profile from hair crown to hips. Show the complete head, neck, shoulders, torso, hips, and both arms. Plain background.",
    "quarter_left": "Turn Image 1 into a left front-quarter head portrait at yaw -45 degrees. The face points image left. Head and shoulders only, plain background.",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def asset_record(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": sha256(path)}


def runtime_record() -> dict[str, object]:
    packages: dict[str, str] = {}
    for name in ("nunchaku", "diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = "not-installed"
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": packages,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def load_pipeline() -> QwenImageEditPlusPipeline:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        transformer=transformer,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    pipe._exclude_from_cpu_offload.append("transformer")
    pipe.enable_sequential_cpu_offload()
    return pipe


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=tuple(ROTATIONS), default="quarter_left")
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=tuple(ROTATIONS),
        help="Generate these targets sequentially with one loaded pipeline; overrides --target.",
    )
    parser.add_argument("--minimal-prompt", action="store_true", help="Use only a rotation instruction; do not add a shared style prompt.")
    parser.add_argument("--pitch", type=int, default=0, help="Camera pitch in degrees; negative is high-angle and positive is low-angle.")
    parser.add_argument("--structure-guide", type=Path, help="Optional human-approved structural input; no guide is generated automatically.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--run-label", default="head-rotation")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    if missing := [path for path in (PLAN, IDENTITY_CONTRACT, STYLE_CONTRACT, ILLUSTRATION_CONTRACT, FRONT_HEAD_REFERENCE) if not path.is_file()]:
        raise FileNotFoundError("missing P7-5.2 asset: " + ", ".join(map(str, missing)))

    structure_guide = None
    if args.structure_guide:
        structure_guide = args.structure_guide if args.structure_guide.is_absolute() else ASSETS / args.structure_guide
        if not structure_guide.is_file():
            raise FileNotFoundError(structure_guide)
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    inputs = [FRONT_HEAD_REFERENCE] + ([structure_guide] if structure_guide else [])
    targets = args.targets or [args.target]
    pipeline = load_pipeline()
    loaded_inputs = [load_image(str(path)).convert("RGB") for path in inputs]
    outputs = []
    for sequence_index, target in enumerate(targets, start=1):
        prompt = MINIMAL_ROTATIONS[target] if args.minimal_prompt else ROTATIONS[target]
        if args.pitch:
            pitch_instruction = "High-angle view: the camera is above the face, looking down." if args.pitch < 0 else "Low-angle view: the camera is below the face, looking up."
            prompt += f" Camera pitch {args.pitch} degrees: {pitch_instruction}"
        if structure_guide:
            prompt += " Image 2 is a human-approved structure map: use only its requested orientation and never render its lines, dots, colours, or background."
        stem = f"p7-5-2-qwen-head-rotation-{target}-pitch-{args.pitch:+03d}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
        output = output_dir / f"{stem}.png"
        run_record = output_dir / f"{stem}-run.json"
        started = time.monotonic()
        image = pipeline(
            prompt=prompt,
            image=loaded_inputs,
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=4.0,
            guidance_scale=1.0,
            negative_prompt=" ",
            num_inference_steps=args.steps,
            width=TARGET_SIZES.get(target, SIZE)[0],
            height=TARGET_SIZES.get(target, SIZE)[1],
        ).images[0]
        image.save(output)
        record = {
            "status": "review_required",
            "experiment_id": f"p7-5-2-qwen-head-rotation-{target}",
            "model": MODEL_ID,
            "transformer": TRANSFORMER_ID,
            "runtime": runtime_record(),
            "transition_plan": asset_record(PLAN),
            "identity_contract": asset_record(IDENTITY_CONTRACT),
            "style_prompt_contract": asset_record(STYLE_CONTRACT),
            "illustration_prompt_contract": asset_record(ILLUSTRATION_CONTRACT),
            "prompt_contracts_applied": {"watercolor_style": False, "illustration": False},
            "inputs": [asset_record(path) for path in inputs],
            "input_roles": ["approved_front_head_identity"] + (["approved_structure_guide"] if structure_guide else []),
            "target": target,
            "sequence": {"index": sequence_index, "targets": targets},
            "pitch_degrees": args.pitch,
            "minimal_prompt": args.minimal_prompt,
            "seed": args.seed,
            "steps": args.steps,
            "size": list(TARGET_SIZES.get(target, SIZE)),
            "true_cfg_scale": 4.0,
            "guidance_scale": 1.0,
            "negative_prompt": " ",
            "prompt": prompt,
            "prompt_word_count": len(prompt.split()),
            "output": asset_record(output),
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "decision": "Candidate only; do not replace an approved head reference before human review.",
        }
        run_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        outputs.append({"output": str(output), "run_record": str(run_record)})
    print(json.dumps({"outputs": outputs}, ensure_ascii=False))


if __name__ == "__main__":
    main()

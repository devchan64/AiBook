#!/usr/bin/env python3
"""Generate review-only Qwen Edit candidates for five approved head rotations.

The approved frontal head is the only identity input.  Each target has one
fixed, human-approved FACE_70 shoulder OpenPose guide in this file.
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
HEAD_ROTATION_TARGETS = ("profile_left", "quarter_left", "front", "quarter_right", "profile_right")
OPENPOSE_GUIDES = {
    "profile_left": ASSETS / "p7-5-2-openpose-shoulders-five-yaw-face70-fixed-body18-v1-yaw-90_pitch+00.png",
    "quarter_left": ASSETS / "p7-5-2-openpose-shoulders-five-yaw-face70-fixed-body18-v1-yaw-45_pitch+00.png",
    "front": ASSETS / "p7-5-2-openpose-shoulders-five-yaw-face70-fixed-body18-v1-yaw+00_pitch+00.png",
    "quarter_right": ASSETS / "p7-5-2-openpose-shoulders-five-yaw-face70-fixed-body18-v1-yaw+45_pitch+00.png",
    "profile_right": ASSETS / "p7-5-2-openpose-shoulders-five-yaw-face70-fixed-body18-v1-yaw+90_pitch+00.png",
}
IDENTITY_PRESERVATION = "Preserve Image 1's character identity and illustration rendering."
ORIENTATION_EDIT = "Change only the head-and-shoulder orientation using Image 2."
RENDERING_PRESERVATION = "Keep Image 1's plain cool blue-gray background and rendering; do not render Image 2."
EXCLUSIONS = "Do not add a body, outfit, bag, text, panel, collage, or scene."


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def asset_record(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": sha256(path)}


def build_prompt() -> str:
    """Preserve Image 1 while using Image 2 only for the structural edit."""
    return " ".join((IDENTITY_PRESERVATION, ORIENTATION_EDIT, RENDERING_PRESERVATION, EXCLUSIONS))


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
    # This process already keeps the quantized transformer on CPU between
    # blocks.  Pinned CPU pages raised swap pressure enough for systemd-oomd
    # to end a sequential five-view run before its first output, so favour
    # pageable memory over a marginal transfer-speed gain here.
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
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
    parser.add_argument("--target", choices=HEAD_ROTATION_TARGETS, default="quarter_left")
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=HEAD_ROTATION_TARGETS,
        help="Generate these targets sequentially with one loaded pipeline; overrides --target.",
    )
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--run-label", default="head-rotation")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    if missing := [path for path in (PLAN, IDENTITY_CONTRACT, STYLE_CONTRACT, ILLUSTRATION_CONTRACT, FRONT_HEAD_REFERENCE, *OPENPOSE_GUIDES.values()) if not path.is_file()]:
        raise FileNotFoundError("missing P7-5.2 asset: " + ", ".join(map(str, missing)))

    targets = list(args.targets or [args.target])
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    pipeline = load_pipeline()
    outputs = []
    for sequence_index, target in enumerate(targets, start=1):
        target_structure_guide = OPENPOSE_GUIDES[target]
        inputs = [FRONT_HEAD_REFERENCE, target_structure_guide]
        prompt = build_prompt()
        stem = f"p7-5-2-qwen-head-rotation-{target}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
        output = output_dir / f"{stem}.png"
        run_record = output_dir / f"{stem}-run.json"
        started = time.monotonic()
        image = pipeline(
            prompt=prompt,
            image=[load_image(str(path)).convert("RGB") for path in inputs],
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=4.0,
            guidance_scale=1.0,
            num_inference_steps=args.steps,
            width=SIZE[0],
            height=SIZE[1],
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
            "input_roles": ["approved_front_head_identity", "approved_face70_orientation_structure"],
            "prompt_roles": {
                "image_1": "preserve character identity and illustration rendering",
                "image_2": "change head-and-shoulder orientation only",
                "rendering": "preserve Image 1; do not render Image 2",
            },
            "target": target,
            "sequence": {"index": sequence_index, "targets": targets},
            "seed": args.seed,
            "steps": args.steps,
            "size": list(SIZE),
            "true_cfg_scale": 4.0,
            "guidance_scale": 1.0,
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

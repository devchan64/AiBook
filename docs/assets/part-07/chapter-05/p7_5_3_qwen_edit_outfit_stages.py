#!/usr/bin/env python3
"""Generate the three front-facing outfit construction stages for P7-5.3."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import torch
from diffusers import QwenImageEditPlusPipeline
from huggingface_hub import snapshot_download
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
HF_HUB_CACHE = ASSETS.parents[3] / ".tmp" / "download" / "huggingface" / "hub"
IDENTITY_CONTRACT = ASSETS / "p7-5-2-character-identity-contract.json"
STYLE_CONTRACT = ASSETS / "p7-5-2-face-style-prompt-contract.json"
ILLUSTRATION_CONTRACT = ASSETS / "p7-5-2-face-illustration-prompt-contract.json"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
TRANSFORMER_REPOSITORY = "nunchaku-tech/nunchaku-qwen-image-edit-2509"
TRANSFORMER_FILENAME = "svdq-fp4_r128-qwen-image-edit-2509.safetensors"
OUTPUT_DIR = ASSETS
DEFAULT_STEPS = 30
QWEN_FACE_REFERENCE = "p7-5-2-qwen-face-head-front-1024-reference-v1-seed-62294-steps-10-size-1024.png"
FRONT_TORSO_REFERENCE = "p7-5-2-qwen-torso-yaw-front-cfg4-front-1024-v4-seed-62294-steps-8.png"
STAGE2_BODY_ONLY_OPENPOSE = "p7-5-3-openpose-fullbody-stage2-open-arms-short-long-legs-v7-yaw+00_pitch+00.png"


OUTFIT_STAGE_TARGETS: dict[str, dict[str, object]] = {
    "outfit_stage1_face_openpose": {
        "inputs": (QWEN_FACE_REFERENCE, STAGE2_BODY_ONLY_OPENPOSE),
        "input_roles": ["frontal_head_identity_hair_1024", "stage_2_calibrated_front_body_only_openpose"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 30,
        "size": (960, 1440),
        "negative_prompt": "OpenPose lines, dots, labels, text, panel, collage, extra person",
        "prompt": (
            "Photorealistic front full-body woman with a clearly narrow, defined waist. Image 1: exact face and hair identity. Image 2: strict-front skeleton; do not render it. "
            "Wear only a slim charcoal-gray micro crop T-shirt whose hem ends immediately below the bust, leaving a wide bare midriff above deep-teal high-waisted feminine full-length wide-leg trousers that reach the tops of white low-top sneakers. "
            "Both arms and complete hands are visible. Warm off-white background."
        ),
    },
    "outfit_stage2_jacket_face": {
        "inputs": (
            "p7-5-3-qwen-edit-prompt-style-outfit_stage1_face_openpose-long-trousers-defined-waist-v4-seed-62294-steps-30.png",
            QWEN_FACE_REFERENCE,
        ),
        "input_roles": ["stage_1_outfit_fullbody", "frontal_head_identity_hair_1024"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 30,
        "size": (960, 1440),
        "negative_prompt": "OpenPose lines, dots, labels, text, panel, collage, extra person",
        "prompt": (
            "Front full-body woman. Image 1: retain the stage-1 crop top, wide trousers, sneakers, and proportions. "
            "Image 2: retain face and hair. Add an unzipped white cropped riding jacket: its front panels are visibly apart and never meet; a flat folded-down pointed shirt collar, white lining, and wrist-length sleeves cover shoulders and upper arms. Both hands are fully visible below the sleeve cuffs. The gray crop top is visible from neckline to hem above the bare midriff; no inner sleeves. Warm off-white background."
        ),
    },
    "outfit_stage3_headless": {
        "inputs": (
            "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30.png",
        ),
        "input_roles": ["stage_2_outfit_fullbody"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 20,
        "size": (1024, 1536),
        "negative_prompt": "face, hair, head, text, panel, collage, extra person",
        "prompt": (
            "Front full-body outfit reference. A plain cool-gray background begins directly above the neck with no silhouette. "
            "Preserve the neck, shirt collar, jacket collar, shoulders, exact jacket, crop top, trousers, hands, and sneakers."
        ),
    },
    "outfit_stage3_faceless_bald": {
        "inputs": (
            "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30.png",
        ),
        "input_roles": ["stage_2_outfit_fullbody"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 20,
        "size": (1024, 1536),
        "negative_prompt": "hair, eyes, eyebrows, eyelashes, nose, mouth, facial features, text, panel, collage, extra person",
        "prompt": (
            "Front full-body faceless bald woman outfit reference. Preserve a smooth bald head silhouette and a blank face with no facial features. "
            "Preserve the neck, shirt collar, jacket collar, shoulders, exact white cropped jacket, gray crop top, trousers, hands, and sneakers. Plain cool-gray background."
        ),
    },
    "outfit_stage3_torso_face_hair_style": {
        "inputs": (
            "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-relaxed-arms-v3-seed-62294-steps-30.png",
            FRONT_TORSO_REFERENCE,
        ),
        "input_roles": ["stage_2_outfit_fullbody", "frontal_torso_face_hair_style"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 30,
        "size": (1024, 1536),
        "negative_prompt": "text, panel, collage, extra person",
        "prompt": (
            "Front full-body woman. Image 1 preserves the exact white cropped jacket, gray crop top, trousers, hands, and sneakers. "
            "Image 2 replaces the face and hair and defines the line work, color, and shading. Plain cool-gray background."
        ),
    },
    "outfit_stage3_4_headless_torso_face_hair_style": {
        "inputs": (
            "p7-5-3-qwen-edit-prompt-style-outfit_stage3_faceless_bald-long-trousers-folded-collar-v2-seed-62294-steps-20.png",
            FRONT_TORSO_REFERENCE,
            STAGE2_BODY_ONLY_OPENPOSE,
        ),
        "input_roles": ["stage_3_faceless_bald_outfit", "frontal_torso_face_hair_style", "front_body_only_openpose_v7"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 30,
        "size": (1024, 1536),
        "negative_prompt": "text, panel, collage, extra person",
        "prompt": (
            "Front full-body woman. Image 1 preserves the exact white cropped jacket, gray crop top, trousers, hands, and sneakers. "
            "Image 2 defines the face, hair, line work, color, and shading. Image 3 defines the full-body proportion, arm and hand placement; do not render it. Plain cool-gray background."
        ),
    },
    "outfit_stage3_stage2_openpose": {
        "inputs": (
            "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-relaxed-arms-v3-seed-62294-steps-30.png",
            STAGE2_BODY_ONLY_OPENPOSE,
        ),
        "input_roles": ["stage_2_outfit_fullbody", "stage_2_calibrated_front_body_only_openpose"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 30,
        "size": (1024, 1536),
        "negative_prompt": "face, hair, facial features, OpenPose lines, dots, labels, text, panel, collage, extra person",
        "prompt": (
            "Front full-body faceless bald woman outfit reference. Image 1 preserves the white cropped jacket, gray crop top, trousers, hands, and sneakers. "
            "Image 2 defines the standing body proportion, lowered arms, hands, and feet; do not render it. Plain cool-gray background."
        ),
    },
    "outfit_stage4_stage2_openpose_torso": {
        "inputs": (
            "p7-5-3-qwen-edit-prompt-style-outfit_stage3_stage2_openpose-stage2-openpose-v1-seed-62294-steps-30.png",
            FRONT_TORSO_REFERENCE,
            STAGE2_BODY_ONLY_OPENPOSE,
        ),
        "input_roles": ["stage_3_body_aligned_faceless_outfit", "frontal_torso_face_hair_style", "stage_2_calibrated_front_body_only_openpose"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 30,
        "size": (1024, 1536),
        "negative_prompt": "OpenPose lines, dots, labels, text, panel, collage, extra person",
        "prompt": (
            "Front full-body woman. Image 1 preserves the outfit, hands, and shoes. Image 2 defines face, hair, line work, color, and shading. "
            "Image 3 defines standing body proportion and relaxed arms; do not render it. Plain cool-gray background."
        ),
    },
}

# Stages 3 and 4 are retired.  Keep only the two active, reproducible outfit
# stages exposed through the CLI while their older configuration remains as
# local implementation history until the broader manuscript history is pruned.
OUTFIT_STAGE_TARGETS = {
    name: OUTFIT_STAGE_TARGETS[name]
    for name in ("outfit_stage1_face_openpose", "outfit_stage2_jacket_face")
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
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def load_pipeline() -> QwenImageEditPlusPipeline:
    transformer_path = Path(snapshot_download(TRANSFORMER_REPOSITORY, cache_dir=HF_HUB_CACHE, local_files_only=True)) / TRANSFORMER_FILENAME
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(transformer_path)
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        model_path,
        transformer=transformer,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    pipe._exclude_from_cpu_offload.append("transformer")
    pipe.enable_sequential_cpu_offload()
    return pipe


def parse_size(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", maxsplit=1)
        width, height = int(width_text), int(height_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("--size must use WIDTHxHEIGHT, for example 1152x1728") from error
    if width < 16 or height < 16 or width % 16 or height % 16:
        raise argparse.ArgumentTypeError("--size values must be positive multiples of 16")
    return width, height


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=tuple(OUTFIT_STAGE_TARGETS), help="One outfit stage to generate.")
    parser.add_argument("--targets", nargs="+", choices=tuple(OUTFIT_STAGE_TARGETS), help="Generate stages sequentially.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--size", type=parse_size)
    parser.add_argument("--run-label", default="v2-natural-eyes")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if bool(args.target) == bool(args.targets):
        parser.error("provide exactly one of --target or --targets")
    if args.targets:
        for target_id in args.targets:
            command = [sys.executable, str(Path(__file__).resolve()), "--target", target_id, "--seed", str(args.seed), "--run-label", args.run_label, "--output-dir", str(args.output_dir)]
            if args.steps is not None:
                command.extend(("--steps", str(args.steps)))
            subprocess.run(command, check=True)
        return
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = OUTFIT_STAGE_TARGETS[args.target]
    steps = args.steps if args.steps is not None else target.get("default_steps", DEFAULT_STEPS)
    if not isinstance(steps, int) or steps < 1:
        raise ValueError("--steps must be at least 1")
    inputs = [ASSETS / name for name in target["inputs"]]
    if missing := [str(path) for path in inputs if not path.is_file()]:
        raise FileNotFoundError("missing input asset(s): " + ", ".join(missing))
    if not IDENTITY_CONTRACT.is_file() or not STYLE_CONTRACT.is_file() or not ILLUSTRATION_CONTRACT.is_file():
        raise FileNotFoundError("missing P7-5.2 identity, style, or illustration contract")
    style_prompt = json.loads(STYLE_CONTRACT.read_text(encoding="utf-8"))["portrait_style_prompt"]
    illustration_prompt = json.loads(ILLUSTRATION_CONTRACT.read_text(encoding="utf-8"))["front_face_illustration_prompt"]
    prompt_parts = []
    if target.get("append_style_prompt", True):
        prompt_parts.append(style_prompt)
    if target.get("append_illustration_prompt", False):
        prompt_parts.append(illustration_prompt)
    prompt_parts.append(target["prompt"])
    prompt = " ".join(prompt_parts)

    width, height = args.size or target["size"]
    stem = f"p7-5-3-qwen-edit-prompt-style-{args.target}-{args.run_label}-seed-{args.seed}-steps-{steps}"
    output = args.output_dir / f"{stem}.png"
    result_record = args.output_dir / f"{stem}-result.json"
    started = time.monotonic()
    pipeline = load_pipeline()
    generation = {
        "prompt": prompt,
        "generator": torch.Generator("cpu").manual_seed(args.seed),
        "true_cfg_scale": 4.0,
        "negative_prompt": target.get("negative_prompt", " "),
        "num_inference_steps": steps,
        "guidance_scale": 1.0,
        "width": width,
        "height": height,
        "image": [load_image(str(path)).convert("RGB") for path in inputs],
    }
    result = pipeline(**generation).images[0]
    result.save(output)
    record = {
        "status": "generated",
        "experiment_id": f"p7-5-3-qwen-edit-{args.target}",
        "model": MODEL_ID,
        "transformer": TRANSFORMER_ID,
        "runtime": runtime_record(),
        "identity_contract": asset_record(IDENTITY_CONTRACT),
        "style_prompt_contract": asset_record(STYLE_CONTRACT),
        "illustration_prompt_contract": asset_record(ILLUSTRATION_CONTRACT),
        "prompt_contracts_applied": {
            "watercolor_style": target.get("append_style_prompt", True),
            "illustration": target.get("append_illustration_prompt", False),
        },
        "target": args.target,
        "run_label": args.run_label,
        "inputs": [asset_record(path) for path in inputs],
        "input_roles": target["input_roles"],
        "seed": args.seed,
        "steps": steps,
        "size": [width, height],
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "negative_prompt": generation["negative_prompt"],
        "prompt": prompt,
        "prompt_word_count": len(prompt.split()),
        "output": asset_record(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "Generated staged front outfit reference; compare the stated inputs and outfit change.",
    }
    result_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result_record": str(result_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

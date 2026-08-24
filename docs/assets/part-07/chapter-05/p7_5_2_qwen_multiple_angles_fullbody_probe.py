#!/usr/bin/env python3
"""Test full-body yaw views from the P7-5.2 stage-2 outfit reference.

This experiment uses one completed front outfit image as the subject source and
the dx8152 Multiple-angles LoRA as the sole camera-transform owner.  It does
not mix OpenPose or separate face/torso images into the camera test.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import platform
import sys
import time
from pathlib import Path

import torch
from diffusers import FlowMatchEulerDiscreteScheduler, QwenImageEditPlusPipeline
from diffusers.utils import load_image
from huggingface_hub import snapshot_download
from nunchaku import NunchakuQwenImageTransformer2DModel

sys.path.insert(0, "/tmp")
from nunchaku_lora_qwen import apply_lora  # noqa: E402


ASSETS = Path(__file__).resolve().parent
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = (
    "nunchaku-tech/nunchaku-qwen-image-edit-2509/lightning-251115/"
    "svdq-fp4_r128-qwen-image-edit-2509-lightning-8steps-251115.safetensors"
)
ANGLE_LORA_REPO = "dx8152/Qwen-Edit-2509-Multiple-angles"
ANGLE_LORA_FILE = "镜头转换.safetensors"
DEFAULT_REFERENCE = ASSETS / "p7-5-2-qwen-edit-prompt-style-outfit_stage2_jacket_face-stage2-open-jacket-visible-hands-v1-seed-62294-steps-30.png"
DEFAULT_SIZE = (960, 1440)
YAW_PROMPTS = {
    "yaw_minus_90": "将镜头向左旋转90度。",
    "yaw_minus_45": "将镜头向左旋转45度。",
    "yaw_plus_45": "将镜头向右旋转45度。",
    "yaw_plus_90": "将镜头向右旋转90度。",
}
YAW_DEGREES = {"yaw_minus_90": -90, "yaw_minus_45": -45, "yaw_plus_45": 45, "yaw_plus_90": 90}
SCHEDULER_CONFIG = {
    "base_image_seq_len": 256,
    "base_shift": math.log(3),
    "invert_sigmas": False,
    "max_image_seq_len": 8192,
    "max_shift": math.log(3),
    "num_train_timesteps": 1000,
    "shift": 1.0,
    "shift_terminal": None,
    "stochastic_sampling": False,
    "time_shift_type": "exponential",
    "use_beta_sigmas": False,
    "use_dynamic_shifting": True,
    "use_exponential_sigmas": False,
    "use_karras_sigmas": False,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def asset_record(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": sha256(path)}


def parse_size(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", maxsplit=1)
        width, height = int(width_text), int(height_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("--size must be WIDTHxHEIGHT") from error
    if width < 16 or height < 16 or width % 16 or height % 16:
        raise argparse.ArgumentTypeError("--size values must be positive multiples of 16")
    return width, height


def load_pipeline(angle_lora: Path, strength: float) -> tuple[QwenImageEditPlusPipeline, int]:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    applied_modules = apply_lora(transformer, angle_lora, strength=strength)
    if applied_modules == 0:
        raise RuntimeError("The Multiple-angles LoRA did not match the transformer")
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        transformer=transformer,
        scheduler=FlowMatchEulerDiscreteScheduler.from_config(SCHEDULER_CONFIG),
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline, applied_modules


def runtime_record() -> dict[str, object]:
    packages = {}
    for package in ("nunchaku", "diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": packages,
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", nargs="+", choices=tuple(YAW_PROMPTS), default=("yaw_minus_45",))
    parser.add_argument("--reference-image", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--size", type=parse_size, default=DEFAULT_SIZE)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--angle-lora-strength", type=float, default=1.0)
    parser.add_argument("--run-label", default="stage2-fullbody-multiple-angles-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if args.steps < 1 or args.angle_lora_strength <= 0:
        raise ValueError("--steps and --angle-lora-strength must be positive")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    reference = args.reference_image if args.reference_image.is_absolute() else ASSETS / args.reference_image
    if not reference.is_file():
        raise FileNotFoundError(reference)
    lora_dir = Path(snapshot_download(ANGLE_LORA_REPO, local_files_only=True))
    lora = lora_dir / ANGLE_LORA_FILE
    if not lora.is_file():
        raise FileNotFoundError(lora)
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    pipeline, applied_modules = load_pipeline(lora, args.angle_lora_strength)
    outputs = []
    for index, target in enumerate(args.targets, start=1):
        prompt = YAW_PROMPTS[target]
        stem = f"p7-5-2-qwen-multiple-angles-{target}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
        output = output_dir / f"{stem}.png"
        result_path = output_dir / f"{stem}-result.json"
        started = time.monotonic()
        image = pipeline(
            prompt=prompt,
            image=[load_image(str(reference)).convert("RGB")],
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=4.0,
            guidance_scale=1.0,
            negative_prompt=" ",
            num_inference_steps=args.steps,
            width=args.size[0],
            height=args.size[1],
        ).images[0]
        image.save(output)
        record = {
            "status": "generated",
            "experiment_id": "p7-5-2-qwen-multiple-angles-fullbody",
            "model": MODEL_ID,
            "transformer": TRANSFORMER_ID,
            "runtime": runtime_record(),
            "inputs": [asset_record(reference)],
            "input_roles": ["stage_2_open_jacket_front_outfit"],
            "camera_transform_owner": "dx8152 Multiple-angles LoRA",
            "angle_lora": {"repository": ANGLE_LORA_REPO, "weight": asset_record(lora)},
            "angle_lora_applied_modules": applied_modules,
            "angle_lora_strength": args.angle_lora_strength,
            "target": target,
            "yaw_degrees": YAW_DEGREES[target],
            "prompt": prompt,
            "prompt_language": "chinese",
            "openpose_used": False,
            "seed": args.seed,
            "steps": args.steps,
            "size": list(args.size),
            "true_cfg_scale": 4.0,
            "output": asset_record(output),
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "sequence": {"index": index, "total": len(args.targets), "targets": args.targets},
        }
        result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        outputs.append({"output": str(output), "result_record": str(result_path)})
    print(json.dumps({"outputs": outputs}, ensure_ascii=False))


if __name__ == "__main__":
    main()

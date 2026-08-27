#!/usr/bin/env python3
"""Generate a pose-transfer character with Qwen Image Edit 2509 via Diffusers."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
import time
from pathlib import Path

import torch
from diffusers import QwenImageEditPlusPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
DEFAULT_POSE = ASSETS / "p7-5-3-character-pose-cutout-white-scene-a-white-v2.png"
DEFAULT_CHARACTER = ASSETS / "p7-5-2-qwen-outfit-stage2-yaw_plus_90-multiple-angle-v1-seed-62294-steps-8.png"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def asset_record(path: Path, role: str) -> dict[str, str]:
    return {"path": str(path), "sha256": sha256(path), "role": role}


def parse_size(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", maxsplit=1)
        width, height = int(width_text), int(height_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("--size must use WIDTHxHEIGHT") from error
    if width < 16 or height < 16 or width % 16 or height % 16:
        raise argparse.ArgumentTypeError("--size values must be positive multiples of 16")
    return width, height


def load_pipeline() -> QwenImageEditPlusPipeline:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        transformer=transformer,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline


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
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "packages": packages,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pose", type=Path, default=DEFAULT_POSE)
    parser.add_argument("--character", type=Path, default=DEFAULT_CHARACTER)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--size", type=parse_size, default=(1024, 1024))
    parser.add_argument("--run-label", default="plus90-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    pose, character = args.pose.resolve(), args.character.resolve()
    if args.steps < 1:
        parser.error("--steps must be positive")
    for path in (pose, character):
        if not path.is_file():
            raise FileNotFoundError(path)
    prompt = "Replace the woman in Picture 1 with the woman in Picture 2, preserving the pose."
    width, height = args.size
    stem = f"p7-5-3-qwen-2509-pose-transfer-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output_dir = args.output_dir.resolve()
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    if args.dry_run:
        print(json.dumps({"pose": str(pose), "character": str(character), "prompt": prompt, "size": [width, height], "output": str(output)}, ensure_ascii=False))
        return
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    started = time.monotonic()
    pipeline = load_pipeline()
    image = pipeline(
        prompt=prompt,
        image=[load_image(str(pose)).convert("RGB"), load_image(str(character)).convert("RGB")],
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        negative_prompt=" ",
        num_inference_steps=args.steps,
        guidance_scale=1.0,
        width=width,
        height=height,
    ).images[0]
    output_dir.mkdir(parents=True, exist_ok=True)
    image.save(output)
    record = {
        "status": "generated",
        "stage": "pose_transfer",
        "model": MODEL_ID,
        "transformer": TRANSFORMER_ID,
        "runtime": runtime_record(),
        "inputs": [asset_record(pose, "Picture 1: pose and framing"), asset_record(character, "Picture 2: character identity and outfit")],
        "prompt": prompt,
        "seed": args.seed,
        "steps": args.steps,
        "size": [width, height],
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "output": asset_record(output, "generated output"),
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

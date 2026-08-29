#!/usr/bin/env python3
"""Generate a single dynamic alley-oop full-body reference for P7-5.3."""

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
from huggingface_hub import snapshot_download
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
HF_HUB_CACHE = ASSETS.parents[3] / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
TRANSFORMER_REPOSITORY = "nunchaku-tech/nunchaku-qwen-image-edit-2509"
TRANSFORMER_FILENAME = "svdq-fp4_r128-qwen-image-edit-2509.safetensors"
OUTFIT_REFERENCE = ASSETS / "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30.png"
TORSO_REFERENCE = ASSETS / "p7-5-7-qwen-torso-yaw-front-cfg4-front-1024-v4-seed-62294-steps-8.png"


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
    transformer_path = Path(snapshot_download(TRANSFORMER_REPOSITORY, cache_dir=HF_HUB_CACHE, local_files_only=True)) / TRANSFORMER_FILENAME
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(transformer_path)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        model_path,
        transformer=transformer,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--size", type=parse_size, default=(1024, 1536))
    parser.add_argument("--run-label", default="v1")
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    for path in (OUTFIT_REFERENCE, TORSO_REFERENCE):
        if not path.is_file():
            raise FileNotFoundError(f"missing input asset: {path}")

    prompt = (
        "Full-body woman. Image 1 defines her outfit and proportions. Image 2 defines her face, hair, line work, color, and shading. "
        "Airborne alley-oop dunk at the jump apex on an indoor basketball court: one basketball in her raised right hand toward one hoop, left arm balancing, left knee forward, right leg trailing, both shoes visible above the court. Low front-left dynamic camera."
    )
    width, height = args.size
    stem = f"p7-5-3-qwen-edit-fullbody-alley-oop-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output = ASSETS / f"{stem}.png"
    result_record = ASSETS / f"{stem}-result.json"
    started = time.monotonic()
    pipeline = load_pipeline()
    generation = {
        "prompt": prompt,
        "generator": torch.Generator("cpu").manual_seed(args.seed),
        "true_cfg_scale": 4.0,
        "negative_prompt": "text, panel, collage, extra person, extra ball, extra hoop",
        "num_inference_steps": args.steps,
        "guidance_scale": 1.0,
        "width": width,
        "height": height,
        "image": [load_image(str(OUTFIT_REFERENCE)).convert("RGB"), load_image(str(TORSO_REFERENCE)).convert("RGB")],
    }
    image = pipeline(**generation).images[0]
    image.save(output)
    result_record.write_text(
        json.dumps(
            {
                "status": "generated",
                "experiment_id": "p7-5-3-qwen-edit-fullbody-alley-oop",
                "model": MODEL_ID,
                "transformer": TRANSFORMER_ID,
                "runtime": runtime_record(),
                "inputs": [asset_record(OUTFIT_REFERENCE), asset_record(TORSO_REFERENCE)],
                "input_roles": ["stage_2_fullbody_outfit", "frontal_torso_face_hair_style"],
                "seed": args.seed,
                "steps": args.steps,
                "size": [width, height],
                "true_cfg_scale": 4.0,
                "guidance_scale": 1.0,
                "negative_prompt": generation["negative_prompt"],
                "prompt": prompt,
                "prompt_word_count": len(prompt.split()),
                "output": asset_record(output),
                "elapsed_seconds": round(time.monotonic() - started, 2),
                "decision": "Generate a dynamic alley-oop full-body pose from the current outfit and torso references.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output), "result_record": str(result_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

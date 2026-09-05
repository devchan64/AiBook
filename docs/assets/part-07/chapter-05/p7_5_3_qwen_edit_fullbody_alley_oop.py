#!/usr/bin/env python3
"""Generate a single dynamic alley-oop full-body reference for P7-5.3.

The stage-2 outfit and the frontal torso are the two image references.  This
script uses the official Qwen Image Edit 2511 BF16 pipeline directly, without
requiring a ComfyUI server.
"""

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

ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
OUTFIT_REFERENCE = ASSETS / (
    "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-"
    "bf16-2511-stage1-v9-jacket-v4-seed-62294-steps-10.png"
)
TORSO_REFERENCE = ASSETS / "p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-size-1280x1280-seed-62294-steps-30.png"
DEFAULT_SEED = 62294
DEFAULT_STEPS = 20
DEFAULT_SIZE = (1024, 1536)
DEFAULT_RUN_LABEL = "2511-v1"


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
    for name in ("diffusers", "torch", "transformers", "accelerate"):
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
    if width < 32 or height < 32 or width % 32 or height % 32:
        raise argparse.ArgumentTypeError("--size values must be positive multiples of 32")
    return width, height


def load_pipeline():
    """Load 2511 locally and retain inactive modules in CPU memory."""
    from diffusers import DiffusionPipeline

    pipeline = DiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=True,
    )
    pipeline.enable_sequential_cpu_offload()
    return pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--size", type=parse_size, default=DEFAULT_SIZE)
    parser.add_argument("--run-label", default=DEFAULT_RUN_LABEL)
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("--steps must be at least 1")
    from diffusers.utils import load_image

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
    stem = (
        f"p7-5-3-qwen-edit-2511-fullbody-alley-oop-{args.run_label}-"
        f"size-{width}x{height}-seed-{args.seed}-steps-{args.steps}"
    )
    output = ASSETS / f"{stem}.png"
    result_record = ASSETS / f"{stem}-result.json"
    started = time.monotonic()
    pipeline = load_pipeline()
    generation = {
        "prompt": prompt,
        "generator": torch.Generator(device="cuda").manual_seed(args.seed),
        "true_cfg_scale": 4.0,
        "negative_prompt": "text, panel, collage, extra person, extra ball, extra hoop",
        "num_inference_steps": args.steps,
        "guidance_scale": 1.0,
        "width": width,
        "height": height,
        "image": [load_image(str(OUTFIT_REFERENCE)).convert("RGB"), load_image(str(TORSO_REFERENCE)).convert("RGB")],
    }
    with torch.inference_mode():
        image = pipeline(**generation).images[0]
    image.save(output)
    result_record.write_text(
        json.dumps(
            {
                "status": "generated",
                "experiment_id": "p7-5-3-qwen-edit-fullbody-alley-oop",
                "runtime": runtime_record(),
                "execution_mode": "direct Diffusers; sequential CPU offload; no ComfyUI server",
                "model": {"repository": MODEL_ID, "dtype": "bfloat16", "device_placement": "sequential_cpu_offload"},
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

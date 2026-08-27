#!/usr/bin/env python3
"""Harmonize lighting and rendering style of a composited Scene A character image."""

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
DEFAULT_INPUT = ASSETS / "p7-5-3-character-background-composite-scene-a-v1.png"
PROMPT = (
    "Make Picture 1 a cohesive editorial illustration. Preserve the woman, her split-leap pose, "
    "white cropped jacket, dark teal pants, white shoes, coastline, and composition. "
    "Use the same clean illustrated rendering on the coastline and woman, with soft clear daylight "
    "from the upper left and consistent subtle shadows."
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def package_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in ("nunchaku", "diffusers", "torch", "transformers", "accelerate"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = "not-installed"
    return versions


def load_pipeline() -> QwenImageEditPlusPipeline:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, transformer=transformer, torch_dtype=torch.bfloat16, local_files_only=True
    )
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--run-label", default="scene-a-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    source = args.input.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    if args.steps < 1:
        parser.error("--steps must be positive")
    output_dir = args.output_dir.resolve()
    stem = f"p7-5-3-qwen-2509-harmonized-composite-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output, result = output_dir / f"{stem}.png", output_dir / f"{stem}-result.json"
    if args.dry_run:
        print(json.dumps({"input": str(source), "prompt": PROMPT, "output": str(output)}, ensure_ascii=False))
        return
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    started = time.monotonic()
    pipeline = load_pipeline()
    image = pipeline(
        prompt=PROMPT,
        image=[load_image(str(source)).convert("RGB")],
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        negative_prompt=" ",
        num_inference_steps=args.steps,
        guidance_scale=1.0,
        width=1024,
        height=1024,
    ).images[0]
    output_dir.mkdir(parents=True, exist_ok=True)
    image.save(output)
    result.write_text(
        json.dumps(
            {
                "status": "generated",
                "stage": "lighting_style_harmonization",
                "model": MODEL_ID,
                "transformer": TRANSFORMER_ID,
                "runtime": {
                    "python": sys.version.split()[0],
                    "platform": platform.platform(),
                    "cuda_device": torch.cuda.get_device_name(0),
                    "packages": package_versions(),
                },
                "input": {"path": str(source), "sha256": sha256(source)},
                "prompt": PROMPT,
                "seed": args.seed,
                "steps": args.steps,
                "true_cfg_scale": 4.0,
                "guidance_scale": 1.0,
                "output": {"path": str(output), "sha256": sha256(output)},
                "elapsed_seconds": round(time.monotonic() - started, 2),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

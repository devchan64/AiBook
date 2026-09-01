#!/usr/bin/env python3
"""Remove the character from Camera A and produce one background plate.

This is a single-image Qwen Image Edit 2511 edit.  It intentionally uses a
short positive instruction: Camera A supplies the composition and the model
only fills the former character region with the surrounding coastal scene.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import time
from pathlib import Path

from PIL import Image


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
DEFAULT_CAMERA = ASSETS / "p7-5-3-qwen-2511-camera-front-left-quarter-view-eye-level-shot-medium-shot-official-direct-seed-5420-steps-20.png"
DEFAULT_PROMPT = "Remove the woman from Picture 1. Preserve the coastal cliff, sky, sea, rocks, grass, and composition."


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--camera", type=Path, default=DEFAULT_CAMERA, help="Camera A image containing the character.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--run-label", default="camera-a-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32:
        parser.error("--steps must be positive and --size must be a positive multiple of 32")

    camera = args.camera.resolve()
    if not camera.is_file():
        raise FileNotFoundError(camera)
    output_dir = args.output_dir.resolve()
    stem = f"p7-5-4-qwen-2511-camera-a-background-{args.run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    output, result = output_dir / f"{stem}.png", output_dir / f"{stem}-result.json"
    if args.dry_run:
        print(json.dumps({"camera": str(camera), "prompt": args.prompt, "output": str(output), "result": str(result)}, ensure_ascii=False))
        return

    import torch
    from diffusers import QwenImageEditPlusPipeline

    source = Image.open(camera).convert("RGB").resize((args.size, args.size), Image.Resampling.LANCZOS)
    started = time.monotonic()
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR, local_files_only=True
    )
    pipeline.enable_sequential_cpu_offload()
    try:
        image = pipeline(
            image=[source], prompt=args.prompt, width=args.size, height=args.size,
            generator=torch.Generator("cpu").manual_seed(args.seed), true_cfg_scale=4.0,
            guidance_scale=1.0, negative_prompt=" ", num_inference_steps=args.steps,
        ).images[0].convert("RGB")
    finally:
        del pipeline
        torch.cuda.empty_cache()

    output_dir.mkdir(parents=True, exist_ok=True)
    image.save(output)
    result.write_text(json.dumps({
        "status": "generated", "stage": "camera_a_character_removal", "model": MODEL_ID,
        "input": {"path": str(camera), "sha256": sha256(camera), "role": "Camera A composition source"},
        "prompt": args.prompt, "seed": args.seed, "steps": args.steps, "true_cfg_scale": 4.0,
        "output": {"path": str(output), "sha256": sha256(output)},
        "runtime": {name: importlib.metadata.version(name) for name in ("diffusers", "torch", "transformers", "accelerate")},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

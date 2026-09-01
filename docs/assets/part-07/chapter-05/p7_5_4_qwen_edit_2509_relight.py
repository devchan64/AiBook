#!/usr/bin/env python3
"""Relight one composited scene with the dx8152 Qwen-Image-Edit-2509 LoRA.

The experiment keeps a single image input.  It tests relighting separately
from pose, clothing, and background replacement, so any added cast-shadow
change is attributable to the LoRA rather than a multi-image edit.
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


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
HUB_CACHE = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
TRANSFORMER_DIR = PROJECT_ROOT / ".tmp" / "download" / "model-qwen-image-edit-2509" / "transformer"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
LORA_ID = "dx8152/Qwen-Image-Edit-2509-Relight"
LORA_DIR = PROJECT_ROOT / ".tmp" / "download" / "weight-dx8152-qwen-image-edit-2509-relight"
LORA_FILENAME = "Qwen-Edit-Relight.safetensors"
DEFAULT_IMAGE = ASSETS / "p7-5-4-qwen-2511-pose-identity-official-camera-scene-a-tryon-camera-replace-v1-size-1280x1280-seed-62294-steps-20.png"
PROMPT = "重新照明, soft sunlight from the upper right."


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def runtime_record() -> dict[str, object]:
    packages = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {"python": sys.version.split()[0], "platform": platform.platform(), "packages": packages}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--lora-scale", type=float, default=1.0)
    parser.add_argument("--true-cfg-scale", type=float, default=4.0)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32:
        parser.error("--steps must be positive and --size must be a multiple of 32")
    if args.lora_scale < 0 or args.true_cfg_scale <= 0:
        parser.error("--lora-scale must be non-negative and --true-cfg-scale must be positive")

    source = args.image.resolve()
    for path in (source, LORA_DIR / LORA_FILENAME, TRANSFORMER_DIR / "config.json"):
        if not path.is_file():
            raise FileNotFoundError(path)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"p7-5-4-qwen-2509-relight-camera-a-{args.run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    output_path = output_dir / f"{stem}.png"
    result_path = output_dir / f"{stem}-result.json"

    import torch
    from diffusers import QwenImageEditPlusPipeline, QwenImageTransformer2DModel
    from diffusers.utils import load_image
    from huggingface_hub import snapshot_download

    started = time.monotonic()
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HUB_CACHE, local_files_only=True))
    transformer = QwenImageTransformer2DModel.from_pretrained(TRANSFORMER_DIR, torch_dtype=torch.bfloat16, local_files_only=True)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(model_path, transformer=transformer, torch_dtype=torch.bfloat16, local_files_only=True)
    pipeline.enable_sequential_cpu_offload()
    pipeline.load_lora_weights(LORA_DIR, weight_name=LORA_FILENAME, adapter_name="dx8152_relight", local_files_only=True)
    pipeline.set_adapters(["dx8152_relight"], adapter_weights=[args.lora_scale])
    try:
        image = pipeline(
            image=load_image(str(source)), prompt=PROMPT,
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=args.true_cfg_scale, negative_prompt=" ", guidance_scale=1.0,
            num_inference_steps=args.steps, width=args.size, height=args.size,
        ).images[0]
    finally:
        pipeline.delete_adapters("dx8152_relight")
    image.save(output_path)
    result_path.write_text(json.dumps({
        "status": "generated", "stage": "relight", "execution_mode": "direct Diffusers; Qwen Image Edit 2509; no ComfyUI",
        "runtime": runtime_record(), "model": MODEL_ID,
        "lora": {"repository": LORA_ID, "weight": LORA_FILENAME, "adapter": "dx8152_relight", "trigger": "重新照明"},
        "input": {"path": str(source), "sha256": sha256(source)},
        "prompt": PROMPT, "seed": args.seed, "steps": args.steps, "lora_scale": args.lora_scale,
        "true_cfg_scale": args.true_cfg_scale, "guidance_scale": 1.0, "generation_canvas": [args.size, args.size],
        "output": {"path": str(output_path), "sha256": sha256(output_path)},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output_path), "result": str(result_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

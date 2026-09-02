#!/usr/bin/env python3
"""Probe Xabsurd Clothing Extractor for shoes and other outfit accessories.

This isolates the extractor stage.  It takes one full-body outfit image and
produces a 1280×1280 white-background product image, so the result can show
whether separate footwear survives removal of the wearer.
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
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
LORA_ID = "Xabsurd/Clothing-Extractor"
LORA_DIR = PROJECT_ROOT / ".tmp" / "download" / "weight-xabsurd-clothing-extractor"
LORA_FILENAME = "qwen-image-edit-2511-白底图-v1-e50.safetensors"
PROMPT = "生成图中人物全身衣物和一双鞋子的商品白底图，去除背景和人物，只保留服装与鞋子"
DEFAULT_REFERENCE = ASSETS / "p7-5-3-qwen-outfit-stage2-yaw_minus_45-multiple-angle-v1-seed-62294-steps-8.png"
SIZE = (1280, 1280)


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
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--run-label", default="shoe-gear-probe-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    reference = args.reference.resolve()
    if args.steps < 1:
        parser.error("--steps must be positive")
    for path in (reference, LORA_DIR / LORA_FILENAME):
        if not path.is_file():
            raise FileNotFoundError(path)

    output_dir = args.output_dir.resolve()
    stem = (
        f"p7-5-4-qwen-2511-xabsurd-clothing-extractor-{args.run_label}"
        f"-size-{SIZE[0]}x{SIZE[1]}-seed-{args.seed}-steps-{args.steps}"
    )
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    plan = {
        "model": MODEL_ID,
        "lora": f"{LORA_ID}/{LORA_FILENAME}",
        "reference": str(reference),
        "prompt": PROMPT,
        "output": str(output),
        "result": str(result),
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    import torch
    from diffusers import DiffusionPipeline
    from diffusers.utils import load_image
    from huggingface_hub import snapshot_download

    started = time.monotonic()
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HUB_CACHE, local_files_only=True))
    pipeline = DiffusionPipeline.from_pretrained(
        model_path, torch_dtype=torch.bfloat16, local_files_only=True
    )
    pipeline.enable_sequential_cpu_offload()
    pipeline.load_lora_weights(
        LORA_DIR, weight_name=LORA_FILENAME, adapter_name="clothingextractor",
        local_files_only=True,
    )
    image = pipeline(
        image=load_image(str(reference)),
        prompt=PROMPT,
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        negative_prompt=" ",
        guidance_scale=1.0,
        num_inference_steps=args.steps,
        width=SIZE[0],
        height=SIZE[1],
    ).images[0]
    pipeline.delete_adapters("clothingextractor")
    image.save(output)
    record = {
        "status": "generated",
        "stage": "clothing_gear_extraction_probe",
        "purpose": "Check whether footwear and separate accessories survive extraction.",
        "execution_mode": "direct Diffusers; Qwen Image Edit 2511; no ComfyUI",
        "runtime": runtime_record(),
        "model": {"repository": MODEL_ID, "device_placement": "sequential CPU offload"},
        "lora": {"repository": LORA_ID, "weight": LORA_FILENAME, "adapter": "clothingextractor"},
        "input": {"path": str(reference), "sha256": sha256(reference)},
        "prompt": PROMPT,
        "seed": args.seed,
        "steps": args.steps,
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "output": {"path": str(output), "sha256": sha256(output)},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

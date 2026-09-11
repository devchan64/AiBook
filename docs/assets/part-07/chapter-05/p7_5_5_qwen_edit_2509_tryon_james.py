#!/usr/bin/env python3
"""Apply JamesDigitalOcean's Qwen Image Edit clothing Try-On LoRA.

This follows the publisher's two-image contract: Picture 1 is the extracted
outfit and Picture 2 is the person who will receive that outfit.
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
LORA_ID = "JamesDigitalOcean/Qwen_Image_Edit_Try_On_Clothes"
LORA_DIR = PROJECT_ROOT / ".tmp" / "download" / "weight-jamesdigitalocean-qwen-edit-try-on-clothes"
LORA_FILENAME = "qwen_image_edit_tryon.safetensors"
PROMPT = "tryon_clothes dress the clothing onto the person"
DEFAULT_GARMENT = ASSETS / "p7-5-5-qwen-2511-xabsurd-clothing-extractor-shoe-gear-v2-size-1280x1280-seed-62294-steps-10.png"
DEFAULT_PERSON = ASSETS / "p7-5-5-qwen-2511-pose-identity-official-camera-scene-b-shadow-side-profile-v2-size-1280x1280-seed-62294-steps-20.png"


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
    parser.add_argument("--garment", type=Path, default=DEFAULT_GARMENT)
    parser.add_argument("--person", type=Path, default=DEFAULT_PERSON)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--lora-scale", type=float, default=1.0)
    parser.add_argument("--true-cfg-scale", type=float, default=4.0)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--run-label", default="scene-b-direct-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32:
        parser.error("--steps must be positive and --size must be a multiple of 32")
    if args.lora_scale < 0 or args.true_cfg_scale <= 0:
        parser.error("LoRA scale must be non-negative and true CFG scale must be positive")

    garment, person = args.garment.resolve(), args.person.resolve()
    required = (garment, person, LORA_DIR / LORA_FILENAME, TRANSFORMER_DIR / "config.json")
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"p7-5-5-qwen-2509-tryon-james-{args.run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
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
    pipeline.load_lora_weights(LORA_DIR, weight_name=LORA_FILENAME, adapter_name="tryonclothes", local_files_only=True)
    pipeline.set_adapters(["tryonclothes"], adapter_weights=[args.lora_scale])
    try:
        image = pipeline(
            image=[load_image(str(garment)), load_image(str(person))], prompt=PROMPT,
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=args.true_cfg_scale, negative_prompt=" ", guidance_scale=1.0,
            num_inference_steps=args.steps, width=args.size, height=args.size,
        ).images[0].convert("RGB")
    finally:
        pipeline.delete_adapters("tryonclothes")
        del pipeline
        torch.cuda.empty_cache()
    image.save(output_path)
    result_path.write_text(json.dumps({
        "status": "generated", "stage": "tryon_james_direct",
        "execution_mode": "direct Diffusers; Qwen Image Edit 2509; no ComfyUI",
        "runtime": runtime_record(), "model": MODEL_ID,
        "lora": {"repository": LORA_ID, "weight": LORA_FILENAME, "adapter": "tryonclothes"},
        "inputs": [
            {"role": "extracted clothing (Picture 1)", "path": str(garment), "sha256": sha256(garment)},
            {"role": "person receiving clothing (Picture 2)", "path": str(person), "sha256": sha256(person)},
        ],
        "prompt": PROMPT, "seed": args.seed, "steps": args.steps,
        "lora_scale": args.lora_scale, "true_cfg_scale": args.true_cfg_scale,
        "guidance_scale": 1.0, "generation_canvas": [args.size, args.size],
        "output": {"path": str(output_path), "sha256": sha256(output_path)},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output_path), "result": str(result_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

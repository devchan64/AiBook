#!/usr/bin/env python3
"""Neutralize lighting in one image or a character-free background plate.

The Studio DeLight model card identifies Qwen Image Edit 2511 as its base and
also states compatibility with 2509.  This runner deliberately uses the
Qwen Image Edit 2509 direct-Diffusers path, one input image, and the model
card's short trigger prompt.  It does not add a separate Lightning LoRA.
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
RESTORATION_ID = "dx8152/Qwen-Image-Edit-2509-Light_restoration"
RESTORATION_DIR = PROJECT_ROOT / ".tmp" / "download" / "weight-dx8152-qwen-image-edit-2509-light-restoration"
RESTORATION_FILE = "移除光影V2.safetensors"
STUDIO_DELIGHT_ID = "prithivMLmods/QIE-2511-Studio-DeLight"
STUDIO_DELIGHT_DIR = PROJECT_ROOT / ".tmp" / "download" / "weight-prithivmlmods-qie-2511-studio-delight"
STUDIO_DELIGHT_FILE = "QIE-2511-Studio-DeLight-5000.safetensors"
PROMPT = "Neutral uniform lighting Preserve identity and composition"
DEFAULT_IMAGE = ASSETS / "p7-5-4-qwen-2511-camera-a-background-camera-a-v1-size-1280x1280-seed-62294-steps-10.png"
ASSET_PRESETS: dict[str, Path | None] = {
    "character-a": ASSETS / "p7-5-4-qwen-2511-pose-identity-official-camera-scene-a-shadow-stage2-outfit-v1-size-1280x1280-seed-62294-steps-30.png",
    "character-b": ASSETS / "p7-5-4-qwen-2511-pose-identity-official-camera-scene-b-shadow-stage2-outfit-v1-size-1280x1280-seed-62294-steps-30.png",
    "character-c": ASSETS / "p7-5-4-qwen-2511-cutout-shadow-scene-c-low-angle-closeup-v1-size-1280x1280-seed-62294-steps-10.png",
    "background-a": ASSETS / "p7-5-4-qwen-2511-camera-a-background-camera-a-v1-size-1280x1280-seed-62294-steps-10.png",
    "background-b": ASSETS / "p7-5-4-qwen-2511-camera-b-background-camera-b-v1-size-1280x1280-seed-62294-steps-10.png",
    "background-c": ASSETS / "p7-5-4-qwen-2511-camera-c-background-camera-c-v1-size-1280x1280-seed-62294-steps-10.png",
}


def sha256(path: Path) -> str:
    """Return a digest for result.json reproducibility records."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def runtime_record() -> dict[str, object]:
    """Report direct runtime versions, without relying on a server workflow."""
    packages: dict[str, str] = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {"python": sys.version.split()[0], "platform": platform.platform(), "packages": packages}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, default=DEFAULT_IMAGE, help="One image or a character-free background plate to de-light; used when --asset is omitted.")
    parser.add_argument(
        "--asset",
        choices=tuple(ASSET_PRESETS),
        help="Choose one of the prepared character-a|b|c or background-a|b|c inputs.",
    )
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1280, help="Square output edge.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--delight-weight", type=Path, default=STUDIO_DELIGHT_DIR / STUDIO_DELIGHT_FILE,
                        help="Local Studio DeLight LoRA file.")
    parser.add_argument("--prompt", default=PROMPT, help="Studio DeLight trigger prompt recorded in result.json.")
    parser.add_argument("--delight-scale", type=float, default=1.0)
    parser.add_argument("--run-label", help="Optional output label; defaults to the selected --asset or camera-a-background-v1.")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.steps <= 0 or args.size < 32 or args.size % 32 or args.delight_scale <= 0:
        parser.error("--steps and --delight-scale must be positive; --size must be a positive multiple of 32")
    preset_source = ASSET_PRESETS.get(args.asset) if args.asset else None
    source = (preset_source or args.image).resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    delight_weight = args.delight_weight.resolve()
    if not delight_weight.is_file():
        raise FileNotFoundError(delight_weight)
    output_dir = args.output_dir.resolve()
    run_label = args.run_label or args.asset or "camera-a-background-v1"
    stem = f"p7-5-4-qwen-2509-studio-delight-{run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    plan = {
        "model": MODEL_ID,
        "asset_preset": args.asset,
        "input": str(source),
        "prompt": args.prompt,
        "lora": {"repository": STUDIO_DELIGHT_ID, "weight": str(delight_weight), "scale": args.delight_scale},
        "true_cfg_scale": 4.0,
        "output": str(output),
        "result": str(result),
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    for required in (TRANSFORMER_DIR / "config.json", delight_weight):
        if not required.is_file():
            raise FileNotFoundError(required)

    import torch
    from diffusers import QwenImageEditPlusPipeline, QwenImageTransformer2DModel
    from diffusers.utils import load_image
    from huggingface_hub import snapshot_download

    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HUB_CACHE, local_files_only=True))
    transformer = QwenImageTransformer2DModel.from_pretrained(TRANSFORMER_DIR, torch_dtype=torch.bfloat16, local_files_only=True)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        model_path,
        transformer=transformer,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    pipeline.enable_attention_slicing("max")
    pipeline.enable_sequential_cpu_offload()
    pipeline.load_lora_weights(delight_weight.parent, weight_name=delight_weight.name, adapter_name="studio_delight", local_files_only=True)
    pipeline.set_adapters(["studio_delight"], adapter_weights=[args.delight_scale])
    try:
        image = pipeline(
            image=load_image(str(source)),
            prompt=args.prompt,
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=4.0,
            negative_prompt=" ",
            num_inference_steps=args.steps,
            width=args.size,
            height=args.size,
        ).images[0]
        image.save(output)
    finally:
        pipeline.delete_adapters(["studio_delight"])
        del pipeline
        torch.cuda.empty_cache()

    record = {
        "status": "generated",
        "stage": "studio_delight",
        "execution_mode": "direct Diffusers; Qwen Image Edit 2509; Studio DeLight LoRA; no ComfyUI",
        "runtime": runtime_record(),
        "model": {"repository": MODEL_ID, "dtype": "bfloat16", "device_placement": "sequential_cpu_offload"},
        "input": {
            "role": args.asset or "custom image or character-free background plate",
            "path": str(source),
            "sha256": sha256(source),
        },
        "prompt": args.prompt,
        "lora": {"repository": STUDIO_DELIGHT_ID, "weight": delight_weight.name, "adapter": "studio_delight", "scale": args.delight_scale},
        "seed": args.seed,
        "steps": args.steps,
        "true_cfg_scale": 4.0,
        "output": {"path": str(output), "sha256": sha256(output), "width": image.width, "height": image.height},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

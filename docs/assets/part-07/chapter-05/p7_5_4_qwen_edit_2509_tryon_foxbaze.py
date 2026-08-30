#!/usr/bin/env python3
"""Test FoxBaze Try-On Alpha with a subject-first, garment-second image order.

The model card defines a top subject image followed by bottom-row garment
images.  This one-garment probe keeps that order while using an identity-ready
split-leap subject.  Eight steps are deliberately below the card's 30-step
recommendation so it can be compared with the other two LoRAs.
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
LORA_ID = "FoxBaze/Try_On_Qwen_Edit_Lora_Alpha"
LORA_DIR = PROJECT_ROOT / ".tmp" / "download" / "weight-foxbaze-try-on-qwen-edit-alpha"
LORA_FILENAME = "Try_On_Qwen_Edit_Lora.safetensors"
BASE_PROMPT = "Style the woman in the top of the image, with every article of clothing on the bottom."
DEFAULT_PERSON = ASSETS / "p7-5-4-qwen-2511-pose-identity-official-camera-scene-a-direct-1280-steps50-v1-size-1280x1280-seed-62294-steps-50.png"
# 1024×1024 is one of the model card's supported Qwen resolutions.
SIZE = (1024, 1024)


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
    parser.add_argument("--person", type=Path, default=DEFAULT_PERSON, help="Subject image: first/top input.")
    parser.add_argument("--garment", type=Path, required=True, help="White-background garment image: second/bottom input.")
    parser.add_argument("--steps", type=int, default=8, help="Eight-step cross-LoRA comparison; card recommends 30.")
    parser.add_argument("--pose-suffix", default="", help="Optional short pose instruction appended after the required try-on prompt.")
    parser.add_argument("--lora-scale", type=float, default=1.0)
    parser.add_argument("--true-cfg-scale", type=float, default=2.5, help="Model-card CFG recommendation.")
    parser.add_argument("--seed", type=int, default=62295)
    parser.add_argument("--run-label", default="tryon-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    person = args.person.resolve()
    garment = args.garment.resolve()
    prompt = " ".join(part for part in (BASE_PROMPT, args.pose_suffix.strip()) if part)
    if args.steps < 1:
        parser.error("--steps must be positive")
    if args.lora_scale < 0 or args.true_cfg_scale <= 0:
        parser.error("LoRA scale must be non-negative and true CFG scale must be positive")
    output_dir = args.output_dir.resolve()
    stem = f"p7-5-4-qwen-2509-tryon-foxbaze-{args.run_label}-size-{SIZE[0]}x{SIZE[1]}-seed-{args.seed}-steps-{args.steps}"
    output_path = output_dir / f"{stem}.png"
    result_path = output_dir / f"{stem}-result.json"
    plan = {
        "model": MODEL_ID, "image_order": [str(person), str(garment)], "prompt": prompt,
        "steps": args.steps, "lora_scale": args.lora_scale, "true_cfg_scale": args.true_cfg_scale,
        "output": str(output_path), "result": str(result_path),
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    required = (
        person, garment, LORA_DIR / LORA_FILENAME, TRANSFORMER_DIR / "config.json",
        TRANSFORMER_DIR / "diffusion_pytorch_model.safetensors.index.json",
    )
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)

    import torch
    from diffusers import QwenImageEditPlusPipeline, QwenImageTransformer2DModel
    from diffusers.utils import load_image
    from huggingface_hub import snapshot_download

    started = time.monotonic()
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HUB_CACHE, local_files_only=True))
    transformer = QwenImageTransformer2DModel.from_pretrained(
        TRANSFORMER_DIR, torch_dtype=torch.bfloat16, local_files_only=True,
    )
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        model_path, transformer=transformer, torch_dtype=torch.bfloat16, local_files_only=True,
    )
    pipeline.enable_sequential_cpu_offload()
    pipeline.load_lora_weights(LORA_DIR, weight_name=LORA_FILENAME, adapter_name="foxbaze_tryon", local_files_only=True)
    pipeline.set_adapters(["foxbaze_tryon"], adapter_weights=[args.lora_scale])
    image = pipeline(
        image=[load_image(str(person)), load_image(str(garment))], prompt=prompt,
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=args.true_cfg_scale, negative_prompt=" ", guidance_scale=1.0,
        num_inference_steps=args.steps, width=SIZE[0], height=SIZE[1],
    ).images[0]
    pipeline.delete_adapters("foxbaze_tryon")
    image.save(output_path)
    result_path.write_text(json.dumps({
        "status": "generated", "stage": "subject_first_multi_reference_tryon",
        "execution_mode": "direct Diffusers; Qwen Image Edit 2509 compatibility probe; no ComfyUI",
        "runtime": runtime_record(), "model": MODEL_ID,
        "lora": {"repository": LORA_ID, "weight": LORA_FILENAME, "adapter": "foxbaze_tryon"},
        "inputs": [
            {"role": "subject (first/top input)", "path": str(person), "sha256": sha256(person)},
            {"role": "garment (second/bottom input)", "path": str(garment), "sha256": sha256(garment)},
        ],
        "image_order": [str(person), str(garment)], "prompt": prompt,
        "seed": args.seed, "steps": args.steps, "lora_scale": args.lora_scale,
        "true_cfg_scale": args.true_cfg_scale, "guidance_scale": 1.0,
        "output": {"path": str(output_path), "sha256": sha256(output_path)},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output_path), "result": str(result_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

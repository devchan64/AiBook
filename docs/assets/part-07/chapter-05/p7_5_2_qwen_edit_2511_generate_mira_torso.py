#!/usr/bin/env python3
"""Generate one frontal Mira torso portrait from her face reference.

The inference call intentionally matches the P7-5.4 camera generator: the
official Qwen-Image-Edit-2511 BF16 checkpoint, one Multiple-Angles LoRA at its
default strength, a single RGB image input, a CUDA generator, and no extra
CFG, negative-prompt, Lightning, or scheduler override.
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
ROOT = ASSETS.parents[3]
CACHE_DIR = ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
LORA_ID = "fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA"
LORA_FILENAME = "qwen-image-edit-2511-multiple-angles-lora.safetensors"
DEFAULT_FACE = ASSETS / (
    "p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-"
    "seed-62294-steps-30-size-1280.png"
)
DEFAULT_IDENTITY_CONTRACT = ASSETS / "p7-5-2-mira-identity-contract.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def runtime_record() -> dict[str, object]:
    packages: dict[str, str] = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {"python": sys.version.split()[0], "platform": platform.platform(), "packages": packages}


def load_outfit_identity(contract_path: Path) -> tuple[dict[str, object], str]:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    outfit = contract.get("outfit_identity_description")
    if not isinstance(outfit, str) or not outfit.strip():
        raise ValueError(f"outfit_identity_description is required: {contract_path}")
    return contract, outfit.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--face", type=Path, default=DEFAULT_FACE, help="Frontal Mira face reference.")
    parser.add_argument("--identity-contract", type=Path, default=DEFAULT_IDENTITY_CONTRACT)
    parser.add_argument("--prompt", help="Override the prompt; omit to append the contract's outfit identity.")
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--run-label", default="p7-5-4-direct-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32:
        parser.error("--steps must be positive; --size must be a multiple of 32 and at least 32")
    face = args.face.resolve()
    if not face.is_file():
        raise FileNotFoundError(face)
    contract_path = args.identity_contract.resolve()
    if not contract_path.is_file():
        raise FileNotFoundError(contract_path)
    contract, outfit_identity = load_outfit_identity(contract_path)
    outfit_clause = outfit_identity.removeprefix("She wears ")
    prompt = args.prompt or f"<sks> front view eye-level shot medium shot, {outfit_clause}"
    output_dir = args.output_dir.resolve()
    stem = (
        f"p7-5-2-qwen-2511-mira-torso-front-{args.run_label}-"
        f"size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    )
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    plan = {
        "execution_mode": "direct Diffusers; P7-5.4 camera-compatible call; no ComfyUI server",
        "model": MODEL_ID,
        "angle_lora": {"repository": LORA_ID, "weight": LORA_FILENAME, "strength": "model-card default"},
        "input": {"role": "Mira frontal face reference", "path": str(face), "sha256": sha256(face)},
        "identity_contract": {
            "path": str(contract_path),
            "sha256": sha256(contract_path),
            "contract_id": contract.get("contract_id"),
            "outfit_identity_description": outfit_identity,
        },
        "prompt": prompt,
        "size": [args.size, args.size],
        "steps": args.steps,
        "seed": args.seed,
        "output": str(output),
        "result": str(result),
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    import torch
    from diffusers import DiffusionPipeline
    from diffusers.utils import load_image

    started = time.monotonic()
    pipe = DiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipe.load_lora_weights(
        LORA_ID,
        weight_name=LORA_FILENAME,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipe.enable_sequential_cpu_offload()
    face_image = load_image(str(face)).convert("RGB").resize((args.size, args.size))
    image = pipe(
        image=face_image,
        prompt=prompt,
        generator=torch.Generator(device="cuda").manual_seed(args.seed),
        num_inference_steps=args.steps,
    ).images[0]
    output_dir.mkdir(parents=True, exist_ok=True)
    image.save(output)
    record = {
        "status": "generated",
        "experiment_id": "p7-5-2-mira-face-to-torso",
        "stage": "face_to_torso",
        "execution_mode": plan["execution_mode"],
        "runtime": runtime_record(),
        "model": {"repository": MODEL_ID, "dtype": "bfloat16", "device_placement": "sequential_cpu_offload"},
        "angle_lora": plan["angle_lora"],
        "inputs": [plan["input"]],
        "identity_contract": plan["identity_contract"],
        "prompt": prompt,
        "prompt_format": "<sks> [azimuth] [elevation] [distance], torso garment",
        "seed": args.seed,
        "steps": args.steps,
        "size": [image.width, image.height],
        "output": {"path": str(output), "sha256": sha256(output)},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

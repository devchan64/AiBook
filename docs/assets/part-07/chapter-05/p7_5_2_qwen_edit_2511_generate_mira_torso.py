#!/usr/bin/env python3
"""Generate one frontal Mira torso portrait from her face reference.

This uses the direct Qwen-Image-Edit-2511 BF16 path: one RGB face input, a
CUDA generator, and no camera-angle, Lightning, CFG, negative-prompt, or
scheduler override. Camera control is reserved for the later multiview stage.
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


def load_inner_top_identity(contract_path: Path) -> tuple[dict[str, object], str]:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    top = contract.get("inner_top_identity")
    if not isinstance(top, dict):
        raise ValueError(f"inner_top_identity is required: {contract_path}")
    color = top.get("color")
    if not isinstance(color, dict) or not isinstance(color.get("name"), str):
        raise ValueError(f"inner_top_identity.color.name is required: {contract_path}")
    required = ("fit", "garment", "neckline", "sleeves", "hem")
    if any(not isinstance(top.get(field), str) or not top[field].strip() for field in required):
        raise ValueError(f"inner_top_identity is incomplete: {contract_path}")
    description = (
        f"{top['fit']} {color['name']} {top['garment']} with a {top['neckline']} neckline "
        f"and {top['sleeves']} sleeves, ending {top['hem']}"
    )
    return contract, description


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--face", type=Path, default=DEFAULT_FACE, help="Frontal Mira face reference.")
    parser.add_argument("--identity-contract", type=Path, default=DEFAULT_IDENTITY_CONTRACT)
    parser.add_argument("--prompt", help="Override the prompt; omit to append the contract's inner-top identity.")
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
    contract, inner_top_identity = load_inner_top_identity(contract_path)
    prompt = args.prompt or f"Frontal upper-body portrait, {inner_top_identity}, warm off-white background"
    output_dir = args.output_dir.resolve()
    stem = (
        f"p7-5-2-qwen-2511-mira-torso-front-{args.run_label}-"
        f"size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    )
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    plan = {
        "execution_mode": "direct Diffusers; Qwen-Image-Edit-2511; no camera LoRA or ComfyUI server",
        "model": MODEL_ID,
        "input": {"role": "Mira frontal face reference", "path": str(face), "sha256": sha256(face)},
        "identity_contract": {
            "path": str(contract_path),
            "sha256": sha256(contract_path),
            "contract_id": contract.get("contract_id"),
            "outfit_identity_description": contract.get("outfit_identity_description"),
            "used_inner_top_identity_description": inner_top_identity,
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
        "inputs": [plan["input"]],
        "identity_contract": plan["identity_contract"],
        "prompt": prompt,
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

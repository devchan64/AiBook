#!/usr/bin/env python3
"""Generate Mira's frontal head reference with BF16 Qwen-Image.

This direct Diffusers runner uses the official Qwen/Qwen-Image checkpoint
with sequential CPU offload. It starts no ComfyUI server, opens no port, and
reads the character and illustration contracts before composing the prompt.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import time
from pathlib import Path

import torch
from diffusers import QwenImagePipeline
from huggingface_hub import snapshot_download

from p7_5_image_output_naming import candidate_stem


ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parents[3]
HF_HUB_CACHE = ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image"
IDENTITY_CONTRACT = ASSETS / "p7-5-2-mira-identity-contract.json"
DEFAULT_SIZE = 1280
DEFAULT_STEPS = 30
DEFAULT_CFG = 4.0
FRONTAL_HEAD_PROMPT = (
    "Strict frontal head-and-neck studio reference of Mira, an adult Korean woman. "
    "Complete hair crown visible with clear empty margin above it; no hair cropped by any edge. "
    "Face centered and facing the camera; both eyes and ears visible. "
    "Plain warm off-white background. No text, accessories, panel, collage, or background scene."
)


def require(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(f"Missing required artifact: {path}")
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def asset_record(path: Path) -> dict[str, object]:
    return {"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size}


def gpu_memory() -> str:
    completed = subprocess.run(
        ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,memory.free", "--format=csv,noheader"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip() if completed.returncode == 0 else "unavailable"


def runtime_record() -> dict[str, object]:
    packages: dict[str, str] = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {
        "execution_mode": "direct Diffusers; no ComfyUI server, port, or HTTP API",
        "offload": "sequential_cpu_offload",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "packages": packages,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--cfg", type=float, default=DEFAULT_CFG)
    parser.add_argument("--run-label", default="front-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.steps < 1 or args.size < 256 or args.size % 16:
        parser.error("--steps must be positive; --size must be at least 256 and divisible by 16")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for BF16 Qwen-Image generation")

    identity_path = require(IDENTITY_CONTRACT)
    identity = json.loads(identity_path.read_text(encoding="utf-8"))
    prompt = " ".join((
        identity["rendering_contract"]["front_face_illustration_prompt"],
        identity["identity_description"],
        FRONTAL_HEAD_PROMPT,
    ))
    stem = candidate_stem(
        f"p7-5-2-mira-head-qwen-image-bf16-{args.run_label}",
        seed=args.seed,
        steps=args.steps,
        contract={"identity": identity["contract_id"], "size": args.size, "cfg": args.cfg},
    )
    output_dir = args.output_dir.resolve()
    output = output_dir / f"{stem}-size-{args.size}.png"
    result = output.with_name(f"{output.stem}-result.json")
    if args.dry_run:
        print(json.dumps({"model": MODEL_ID, "prompt": prompt, "output": str(output)}, ensure_ascii=False, indent=2))
        return

    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    record: dict[str, object] = {
        "experiment_id": "p7-5-2-mira-head-bf16-t2i",
        "purpose": "Mira frontal-head text-to-image reference; no reference-image input",
        "model": MODEL_ID,
        "dtype": "bfloat16",
        "runtime": runtime_record(),
        "gpu_memory_before": gpu_memory(),
        "identity_contract": asset_record(identity_path),
        "rendering_contract": {
            "source": "identity_contract.rendering_contract",
            "components": ["front_face_illustration_prompt"],
        },
        "inputs": [],
        "input_roles": [],
        "prompt": prompt,
        "seed": args.seed,
        "steps": args.steps,
        "size": [args.size, args.size],
        "true_cfg_scale": args.cfg,
        "guidance_scale": 1.0,
        "negative_prompt": " ",
    }
    try:
        pipeline = QwenImagePipeline.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            local_files_only=True,
        )
        pipeline.enable_sequential_cpu_offload()
        image = pipeline(
            prompt=prompt,
            negative_prompt=" ",
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=args.cfg,
            guidance_scale=1.0,
            num_inference_steps=args.steps,
            width=args.size,
            height=args.size,
        ).images[0]
        image.save(output)
        record.update({"status": "generated", "output": asset_record(output)})
    except Exception as error:
        record.update({"status": "failed", "error_type": type(error).__name__, "error": str(error)})
    finally:
        record.update({"gpu_memory_after": gpu_memory(), "elapsed_seconds": round(time.monotonic() - started, 2)})
        result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        torch.cuda.empty_cache()
    print(json.dumps({"output": str(output), "result": str(result), "status": record["status"]}, ensure_ascii=False))
    if record["status"] != "generated":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

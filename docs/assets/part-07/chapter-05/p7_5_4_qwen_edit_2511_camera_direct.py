#!/usr/bin/env python3
"""Run Qwen-Image-Edit-2511 Multiple-Angles LoRA directly with Diffusers.

This follows the official Multiple-Angles LoRA model-card path: load the
official Qwen/Qwen-Image-Edit-2511 checkpoint and only the fal Multiple-Angles
LoRA.  It deliberately does not use a GGUF transformer, ComfyUI, or a
Lightning LoRA.  The card's direct CUDA placement is available, while
sequential CPU offload makes the same official weights feasible on 8GB VRAM.

The installed Diffusers 0.37 API uses ``torch_dtype`` (not the card's newer
``dtype`` spelling) and does not accept ``device_map='cuda'``.  The direct CUDA
mode therefore calls ``pipe.to('cuda')`` after loading; sequential offload
keeps the pipeline on CPU and moves modules as they are used.
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
CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
LORA_ID = "fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA"
LORA_FILENAME = "qwen-image-edit-2511-multiple-angles-lora.safetensors"
AZIMUTHS = (
    "front view", "front-right quarter view", "right side view", "rear-right quarter view",
    "rear view", "rear-left quarter view", "left side view", "front-left quarter view",
)
ELEVATIONS = ("low-angle shot", "eye-level shot", "elevated shot", "high-angle shot")
DISTANCES = ("close-up", "medium shot", "wide shot")
CAMERA_PRESETS = {
    "a": ("front-left quarter view", "eye-level shot", "medium shot"),
    "b": ("front-right quarter view", "high-angle shot", "medium shot"),
    "c": ("front-left quarter view", "low-angle shot", "close-up"),
}
SCENE_REFERENCES = {
    "a": "p7-5-4-qwen-image-q4ks-style-contract-scene-a-v1_00001_.png",
    "b": "p7-5-4-qwen-image-q4ks-style-contract-scene-b-v1_00001_.png",
    "c": "p7-5-4-qwen-image-q4ks-style-contract-scene-c-v1_00001_.png",
}


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


def prompt_for(camera: tuple[str, str, str]) -> str:
    return f"<sks> {camera[0]} {camera[1]} {camera[2]}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, help="Explicit source image. Overrides the scene source associated with --camera.")
    parser.add_argument("--camera", choices=tuple(CAMERA_PRESETS), help="Named camera preset with its matching scene input; overrides the three camera fields.")
    parser.add_argument("--azimuth", choices=AZIMUTHS, default="front view")
    parser.add_argument("--elevation", choices=ELEVATIONS, default="eye-level shot")
    parser.add_argument("--distance", choices=DISTANCES, default="medium shot")
    parser.add_argument("--seed", type=int, default=5420)
    parser.add_argument("--steps", type=int, default=20, help="Inference steps (default: 20).")
    parser.add_argument("--run-label", default="official-direct")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--offload", choices=("none", "sequential"), default="sequential", help="'none' reproduces the model-card CUDA placement; 'sequential' keeps the official weights but uses CPU offload for 8GB VRAM.")
    parser.add_argument("--allow-download", action="store_true", help="Permit Hugging Face downloads. The default is local-files-only.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.reference is not None:
        reference = args.reference.resolve()
    elif args.camera is not None:
        reference = ASSETS / SCENE_REFERENCES[args.camera]
    else:
        parser.error("provide --camera to use its matching scene input, or provide --reference with explicit camera fields")
    if not reference.is_file():
        raise FileNotFoundError(reference)
    if args.steps < 1:
        parser.error("--steps must be positive")
    camera = CAMERA_PRESETS[args.camera] if args.camera else (args.azimuth, args.elevation, args.distance)
    prompt = prompt_for(camera)
    camera_slug = "-".join(camera).replace(" ", "-")
    steps_label = str(args.steps)
    stem = f"p7-5-3-qwen-2511-camera-{camera_slug}-{args.run_label}-seed-{args.seed}-steps-{steps_label}"
    output = args.output_dir.resolve() / f"{stem}.png"
    result = args.output_dir.resolve() / f"{stem}-result.json"
    plan = {
        "execution_mode": "direct Diffusers; official model-card path; no ComfyUI or GGUF",
        "model": MODEL_ID,
        "lora": LORA_ID,
        "device_placement": "pipe.to(cuda)" if args.offload == "none" else "sequential_cpu_offload",
        "offload": args.offload,
        "local_files_only": not args.allow_download,
        "input": str(reference),
        "camera": {"azimuth": camera[0], "elevation": camera[1], "distance": camera[2]},
        "prompt": prompt,
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
    load_args = {
        "torch_dtype": torch.bfloat16,
        "cache_dir": CACHE_DIR,
        "local_files_only": not args.allow_download,
    }
    pipe = DiffusionPipeline.from_pretrained(MODEL_ID, **load_args)
    pipe.load_lora_weights(
        LORA_ID,
        weight_name=LORA_FILENAME,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    if args.offload == "sequential":
        pipe.enable_sequential_cpu_offload()
    else:
        pipe.to("cuda")
    generation_args = {"image": load_image(str(reference)), "prompt": prompt}
    generation_args["generator"] = torch.Generator(device="cuda").manual_seed(args.seed)
    generation_args["num_inference_steps"] = args.steps
    image = pipe(**generation_args).images[0]
    args.output_dir.resolve().mkdir(parents=True, exist_ok=True)
    image.save(output)
    record = {
        "status": "generated",
        "experiment_id": "p7-5-3-qwen-2511-camera-official-direct",
        "stage": "camera_angle",
        "execution_mode": plan["execution_mode"],
        "runtime": runtime_record(),
        "model": {"repository": MODEL_ID, "dtype": "bfloat16", "device_placement": plan["device_placement"], "offload": args.offload},
        "lora": {"repository": LORA_ID, "weight": LORA_FILENAME, "strength": "model-card default"},
        "input": {"path": str(reference), "sha256": sha256(reference)},
        "camera_preset": args.camera,
        "camera": plan["camera"],
        "prompt": prompt,
        "prompt_format": "<sks> [azimuth] [elevation] [distance]",
        "seed": args.seed,
        "steps": args.steps,
        "output": {"path": str(output), "sha256": sha256(output)},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

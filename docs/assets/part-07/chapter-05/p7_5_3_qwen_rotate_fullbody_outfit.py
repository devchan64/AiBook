#!/usr/bin/env python3
"""Generate P7-5.3 full-body outfit yaw views with Qwen Edit 2511.

The stage-2 outfit is the only image input. The fal Multiple-Angles LoRA
applies a single camera-view transformation; OpenPose and a separate face
reference are deliberately excluded from this rotation path.
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
ANGLE_LORA_ID = "fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA"
ANGLE_LORA_FILENAME = "qwen-image-edit-2511-multiple-angles-lora.safetensors"
DEFAULT_REFERENCE = ASSETS / (
    "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-"
    "long-trousers-folded-collar-v3-seed-62294-steps-30.png"
)
YAW_CAMERA_VIEWS = {
    "yaw_minus_90": ("left side view", -90),
    "yaw_minus_45": ("front-left quarter view", -45),
    "yaw_plus_45": ("front-right quarter view", 45),
    "yaw_plus_90": ("right side view", 90),
}
ELEVATION = "eye-level shot"
DISTANCE = "wide shot"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def asset_record(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": sha256(path)}


def runtime_record() -> dict[str, object]:
    packages: dict[str, str] = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {"python": sys.version.split()[0], "platform": platform.platform(), "packages": packages}


def prompt_for(azimuth: str) -> str:
    """Use the Multiple-Angles LoRA's documented camera-token format."""
    return f"<sks> {azimuth} {ELEVATION} {DISTANCE}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", nargs="+", choices=tuple(YAW_CAMERA_VIEWS), default=tuple(YAW_CAMERA_VIEWS))
    parser.add_argument("--reference-image", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--run-label", default="qwen-edit-2511-multiple-angles-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--offload", choices=("none", "sequential"), default="sequential")
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("--steps must be positive")

    reference = args.reference_image if args.reference_image.is_absolute() else ASSETS / args.reference_image
    if not reference.is_file():
        raise FileNotFoundError(reference)
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    local_files_only = not args.allow_download
    plans = []
    for target in args.targets:
        azimuth, yaw_degrees = YAW_CAMERA_VIEWS[target]
        stem = f"p7-5-3-qwen-outfit-stage2-{target}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
        plans.append({
            "target": target,
            "model": MODEL_ID,
            "angle_lora": ANGLE_LORA_ID,
            "reference": str(reference),
            "camera": {"azimuth": azimuth, "elevation": ELEVATION, "distance": DISTANCE, "yaw_degrees": yaw_degrees},
            "prompt": prompt_for(azimuth),
            "output": str(output_dir / f"{stem}.png"),
            "result": str(output_dir / f"{stem}-result.json"),
            "offload": args.offload,
            "local_files_only": local_files_only,
        })
    if args.dry_run:
        print(json.dumps({"plans": plans}, ensure_ascii=False, indent=2))
        return

    import torch
    from diffusers import DiffusionPipeline
    from diffusers.utils import load_image

    pipe = DiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=local_files_only,
    )
    pipe.load_lora_weights(
        ANGLE_LORA_ID,
        weight_name=ANGLE_LORA_FILENAME,
        cache_dir=CACHE_DIR,
        local_files_only=local_files_only,
    )
    if args.offload == "sequential":
        pipe.enable_sequential_cpu_offload()
        device_placement = "sequential_cpu_offload"
    else:
        pipe.to("cuda")
        device_placement = "pipe.to(cuda)"

    output_dir.mkdir(parents=True, exist_ok=True)
    reference_image = load_image(str(reference)).convert("RGB")
    outputs = []
    for index, plan in enumerate(plans, start=1):
        output = Path(plan["output"])
        result_path = Path(plan["result"])
        started = time.monotonic()
        image = pipe(
            image=reference_image,
            prompt=plan["prompt"],
            generator=torch.Generator(device="cuda").manual_seed(args.seed),
            num_inference_steps=args.steps,
        ).images[0]
        image.save(output)
        record = {
            "status": "generated",
            "experiment_id": "p7-5-3-qwen-outfit-yaw-2511",
            "runtime": runtime_record(),
            "model": {"repository": MODEL_ID, "dtype": "bfloat16", "device_placement": device_placement},
            "angle_lora": {"repository": ANGLE_LORA_ID, "weight": ANGLE_LORA_FILENAME, "strength": "model-card default"},
            "inputs": [asset_record(reference)],
            "input_roles": ["outfit-stage2_reference"],
            "openpose_used": False,
            "target": plan["target"],
            "camera": plan["camera"],
            "prompt": plan["prompt"],
            "prompt_format": "<sks> [azimuth] [elevation] [distance]",
            "seed": args.seed,
            "steps": args.steps,
            "output": asset_record(output),
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "sequence": {"index": index, "total": len(plans), "targets": args.targets},
        }
        result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        outputs.append({"output": str(output), "result_record": str(result_path)})
    print(json.dumps({"outputs": outputs}, ensure_ascii=False))


if __name__ == "__main__":
    main()

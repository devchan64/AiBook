#!/usr/bin/env python3
"""Generate P7-5.3 full-body outfit yaw views with Qwen Image Edit 2511.

The current stage-2 outfit is the only image input.  The fal
Multiple-Angles LoRA receives only its documented camera-token prompt, in the
order ``<sks> [azimuth] [elevation] [distance]``.  The LightX2V four-step
Lightning LoRA supplies the sampling profile.  OpenPose and a separate face
reference are deliberately excluded so they cannot compete with the single
camera transformation.
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
LIGHTNING_ID = "lightx2v/Qwen-Image-Edit-2511-Lightning"
LIGHTNING_FILENAME = "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors"
LIGHTNING_DIR = PROJECT_ROOT / ".tmp" / "download" / "weight-lightx2v-qwen-image-edit-2511-lightning-4steps"
DEFAULT_REFERENCE = ASSETS / (
    "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-"
    "bf16-2511-stage1-v9-jacket-v4-seed-62294-steps-10.png"
)
YAW_CAMERA_VIEWS = {
    "yaw_minus_90": ("left side view", -90),
    "yaw_minus_45": ("front-left quarter view", -45),
    "yaw_plus_45": ("front-right quarter view", 45),
    "yaw_plus_90": ("right side view", 90),
}
ELEVATION = "eye-level shot"
DISTANCE = "medium shot"
DEFAULT_STEPS = 4
DEFAULT_LORA_SCALE = 0.9
DEFAULT_WIDTH = 960
DEFAULT_HEIGHT = 1440
ADAPTER_NAME = "multiple_angles"
LIGHTNING_ADAPTER_NAME = "lightning4"


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
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS, help="Lightning 4-step profile; only 4 is supported.")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH, help="Output width in pixels (default: 960).")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT, help="Output height in pixels (default: 1440).")
    parser.add_argument(
        "--lora-scale",
        type=float,
        default=DEFAULT_LORA_SCALE,
        help="Multiple-Angles LoRA strength (the model card recommends 0.8–1.0; default: 0.9).",
    )
    parser.add_argument("--run-label", default="qwen-edit-2511-multiple-angles-lightning4-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--offload", choices=("none", "sequential"), default="sequential")
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.steps != DEFAULT_STEPS:
        parser.error("the Lightning 4-step profile requires --steps 4")
    if args.width < 32 or args.height < 32 or args.width % 32 or args.height % 32:
        parser.error("--width and --height must be multiples of 32 and at least 32")
    if not 0.8 <= args.lora_scale <= 1.0:
        parser.error("--lora-scale must be within the model-card recommended range 0.8–1.0")

    reference = args.reference_image if args.reference_image.is_absolute() else ASSETS / args.reference_image
    if not reference.is_file():
        raise FileNotFoundError(reference)
    lightning_weight = LIGHTNING_DIR / LIGHTNING_FILENAME
    if not lightning_weight.is_file():
        raise FileNotFoundError(lightning_weight)
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
            "lightning_lora": LIGHTNING_ID,
            "reference": str(reference),
            "camera": {"azimuth": azimuth, "elevation": ELEVATION, "distance": DISTANCE, "yaw_degrees": yaw_degrees},
            "prompt": prompt_for(azimuth),
            "output": str(output_dir / f"{stem}.png"),
            "result": str(output_dir / f"{stem}-result.json"),
            "offload": args.offload,
            "lora_scale": args.lora_scale,
            "steps": args.steps,
            "sampling": {
                "profile": "lightning4",
                "steps": args.steps,
                "true_cfg_scale": 1.0,
                "negative_prompt": None,
                "guidance_scale": 1.0,
            },
            "local_files_only": local_files_only,
            "size": [args.width, args.height],
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
        adapter_name=ADAPTER_NAME,
        cache_dir=CACHE_DIR,
        local_files_only=local_files_only,
    )
    pipe.load_lora_weights(
        str(LIGHTNING_DIR),
        weight_name=LIGHTNING_FILENAME,
        adapter_name=LIGHTNING_ADAPTER_NAME,
        local_files_only=True,
    )
    pipe.set_adapters(
        [ADAPTER_NAME, LIGHTNING_ADAPTER_NAME],
        adapter_weights=[args.lora_scale, 1.0],
    )
    if args.offload == "sequential":
        pipe.enable_sequential_cpu_offload()
        device_placement = "sequential_cpu_offload"
    else:
        pipe.to("cuda")
        device_placement = "pipe.to(cuda)"

    output_dir.mkdir(parents=True, exist_ok=True)
    reference_image = load_image(str(reference)).convert("RGB").resize((args.width, args.height))
    shared_input = {
        "role": "Picture 1: stage-2 full-body outfit reference",
        **asset_record(reference),
        "normalized_size": [args.width, args.height],
    }
    outputs = []
    batch_started = time.monotonic()
    for index, plan in enumerate(plans, start=1):
        output = Path(plan["output"])
        result_path = Path(plan["result"])
        started = time.monotonic()
        with torch.inference_mode():
            image = pipe(
                image=reference_image,
                prompt=plan["prompt"],
                generator=torch.Generator(device="cuda").manual_seed(args.seed),
                num_inference_steps=args.steps,
                height=args.height,
                width=args.width,
                true_cfg_scale=1.0,
                negative_prompt=None,
                guidance_scale=1.0,
                num_images_per_prompt=1,
            ).images[0]
        image.save(output)
        record = {
            "status": "generated",
            "experiment_id": "p7-5-3-qwen-outfit-yaw-2511",
            "runtime": runtime_record(),
            "model": {"repository": MODEL_ID, "dtype": "bfloat16", "device_placement": device_placement},
            "angle_lora": {
                "repository": ANGLE_LORA_ID,
                "weight": ANGLE_LORA_FILENAME,
                "adapter_name": ADAPTER_NAME,
                "strength": args.lora_scale,
                "recommended_range": [0.8, 1.0],
            },
            "lightning_lora": {
                "repository": LIGHTNING_ID,
                "weight": LIGHTNING_FILENAME,
                "adapter_name": LIGHTNING_ADAPTER_NAME,
                "strength": 1.0,
            },
            "sampling": {
                "profile": "lightning4",
                "steps": args.steps,
                "true_cfg_scale": 1.0,
                "negative_prompt": None,
                "guidance_scale": 1.0,
            },
            "inputs": [shared_input],
            "openpose_used": False,
            "target": plan["target"],
            "camera": plan["camera"],
            "prompt": plan["prompt"],
            "prompt_format": "<sks> [azimuth] [elevation] [distance]",
            "seed": args.seed,
            "steps": args.steps,
            "size": [image.width, image.height],
            "output": {**asset_record(output), "width": image.width, "height": image.height},
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "sequence": {"index": index, "total": len(plans), "targets": args.targets},
        }
        result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        outputs.append({"target": plan["target"], "output": str(output), "result_record": str(result_path)})
        print(json.dumps(outputs[-1], ensure_ascii=False), flush=True)
    batch_result = output_dir / (
        f"p7-5-3-qwen-outfit-stage2-yaw-batch-{args.run_label}-"
        f"size-{args.width}x{args.height}-seed-{args.seed}-steps-{args.steps}-result.json"
    )
    batch_result.write_text(
        json.dumps(
            {
                "status": "generated",
                "experiment_id": "p7-5-3-qwen-outfit-yaw-2511",
                "execution_mode": "direct Diffusers; sequential CPU offload by default; no ComfyUI server or HTTP API",
                "reference": shared_input,
                "sampling": {"profile": "lightning4", "steps": args.steps, "true_cfg_scale": 1.0, "negative_prompt": None, "guidance_scale": 1.0},
                "expected_count": len(plans),
                "outputs": outputs,
                "elapsed_seconds": round(time.monotonic() - batch_started, 2),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"batch_result": str(batch_result), "count": len(outputs)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate Mira torso-reference camera variants with the 2511 angle workflow.

The only image input is the generated Mira frontal torso reference. It carries
the approved face, clothing, and shoulder geometry into every camera variant.
The batch combines five horizontal yaw labels with three vertical camera
labels, producing 15 variants. It uses ``elevated shot`` rather than a high
angle: the vertical labels are low, eye-level, and elevated.

This runner uses the official Qwen-Image-Edit-2511 BF16 pipeline with the
Multiple-Angles LoRA in direct Diffusers. It starts no ComfyUI server or HTTP
API.
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
DEFAULT_TORSO = ASSETS / (
    "p7-5-2-qwen-2511-mira-torso-front-p7-5-4-direct-v1-"
    "size-320x320-seed-62294-steps-20.png"
)
YAW_VIEWS = {
    "minus-90": {"degrees": -90, "prompt": "left side view"},
    "minus-45": {"degrees": -45, "prompt": "front-left quarter view"},
    "zero": {"degrees": 0, "prompt": "front view"},
    "plus-45": {"degrees": 45, "prompt": "front-right quarter view"},
    "plus-90": {"degrees": 90, "prompt": "right side view"},
}
VERTICAL_VIEWS = {
    "low": {"prompt": "low-angle shot"},
    "level": {"prompt": "eye-level shot"},
    "elevated": {"prompt": "elevated shot"},
}
DEFAULT_DISTANCE = "medium shot"


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


def prompt_for(yaw: str, vertical: str) -> str:
    return f"<sks> {YAW_VIEWS[yaw]['prompt']} {VERTICAL_VIEWS[vertical]['prompt']} {DEFAULT_DISTANCE}"


def selected_values(values: dict[str, object], selection: str) -> tuple[str, ...]:
    if selection == "all":
        return tuple(values)
    return (selection,)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--torso", type=Path, default=DEFAULT_TORSO, help="Mira frontal torso reference, used as the only image input.")
    parser.add_argument("--yaw", choices=("all", *YAW_VIEWS), default="all")
    parser.add_argument("--vertical", choices=("all", *VERTICAL_VIEWS), default="all")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        metavar="VERTICAL:YAW",
        help="Skip a completed pair, for example --exclude elevated:minus-45. Repeat as needed.",
    )
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=30, help="Standard Qwen sampling steps.")
    parser.add_argument("--size", type=int, default=320, help="Square reference and output size for this probe.")
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32:
        parser.error("--steps must be positive; --size must be a multiple of 32 and at least 32")
    torso = args.torso.resolve()
    if not torso.is_file():
        raise FileNotFoundError(torso)
    yaws = selected_values(YAW_VIEWS, args.yaw)
    verticals = selected_values(VERTICAL_VIEWS, args.vertical)
    excluded: set[tuple[str, str]] = set()
    for value in args.exclude:
        try:
            vertical, yaw = value.split(":", maxsplit=1)
        except ValueError as error:
            parser.error(f"--exclude must use VERTICAL:YAW, got {value!r}")
        if vertical not in VERTICAL_VIEWS or yaw not in YAW_VIEWS:
            parser.error(f"--exclude uses an unknown pair: {value!r}")
        excluded.add((vertical, yaw))
    output_dir = args.output_dir.resolve()
    jobs = [(yaw, vertical) for vertical in verticals for yaw in yaws if (vertical, yaw) not in excluded]
    if not jobs:
        parser.error("the selected grid contains no jobs after exclusions")
    plan = {
        "model": MODEL_ID,
        "angle_lora": {"repository": LORA_ID, "weight": LORA_FILENAME, "adapter_weight": "model-card default"},
        "sampling": {"steps": args.steps, "scheduler": "FlowMatchEulerDiscreteScheduler", "dynamic_shift": True},
        "execution_mode": "direct Diffusers; sequential CPU offload; no ComfyUI server or HTTP API",
        "input": {"role": "Picture 1: Mira frontal torso reference", "path": str(torso), "sha256": sha256(torso)},
        "prompt_format": "<sks> [azimuth] [elevation] [distance]",
        "vertical_labels": VERTICAL_VIEWS,
        "excluded": [{"vertical": vertical, "yaw": yaw} for vertical, yaw in sorted(excluded)],
        "jobs": [
            {"yaw": yaw, "vertical": vertical, "prompt": prompt_for(yaw, vertical)}
            for yaw, vertical in jobs
        ],
        "expected_count": len(jobs),
        "size": [args.size, args.size],
        "steps": args.steps,
        "seed": args.seed,
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    import torch
    from diffusers import DiffusionPipeline
    from diffusers.utils import load_image

    started = time.monotonic()
    output_dir.mkdir(parents=True, exist_ok=True)
    pipeline = DiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipeline.load_lora_weights(
        LORA_ID,
        weight_name=LORA_FILENAME,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipeline.enable_sequential_cpu_offload()
    reference = load_image(str(torso)).convert("RGB").resize((args.size, args.size))
    shared_input = {"role": "Picture 1: Mira frontal torso reference", "path": str(torso), "sha256": sha256(torso)}
    results: list[dict[str, object]] = []
    for yaw, vertical in jobs:
        prompt = prompt_for(yaw, vertical)
        stem = (
            f"p7-5-2-qwen-2511-mira-torso-multiview-vertical-{vertical}-yaw-{yaw}-"
            f"{args.run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
        )
        output = output_dir / f"{stem}.png"
        result = output_dir / f"{stem}-result.json"
        with torch.inference_mode():
            image = pipeline(
                image=reference,
                prompt=prompt,
                generator=torch.Generator(device="cuda").manual_seed(args.seed),
                num_inference_steps=args.steps,
            ).images[0]
        image.save(output)
        record = {
            "status": "generated",
            "experiment_id": "p7-5-2-mira-torso-multiview",
            "stage": "torso_multiview_camera",
            "execution_mode": "direct Diffusers; QwenImageEditPlusPipeline; no ComfyUI server",
            "runtime": runtime_record(),
            "model": {"repository": MODEL_ID, "dtype": "bfloat16", "device_placement": "sequential_cpu_offload"},
            "angle_lora": {"repository": LORA_ID, "weight": LORA_FILENAME, "strength": "model-card default", "prompt_format": "<sks> [azimuth] [elevation] [distance]"},
            "sampling": {"steps": args.steps, "scheduler": "FlowMatchEulerDiscreteScheduler", "dynamic_shift": True, "execution": "direct Diffusers; no ComfyUI server"},
            "inputs": [shared_input],
            "camera": {
                "yaw_degrees": YAW_VIEWS[yaw]["degrees"],
                "azimuth": YAW_VIEWS[yaw]["prompt"],
                "vertical": vertical,
                "elevation": VERTICAL_VIEWS[vertical]["prompt"],
                "distance": DEFAULT_DISTANCE,
            },
            "prompt": prompt,
            "seed": args.seed,
            "steps": args.steps,
            "size": [image.width, image.height],
            "output": {"path": str(output), "sha256": sha256(output), "width": image.width, "height": image.height},
            "elapsed_seconds": round(time.monotonic() - started, 2),
        }
        result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        results.append({"yaw": yaw, "vertical": vertical, "output": str(output), "result": str(result)})
        print(json.dumps(results[-1], ensure_ascii=False), flush=True)
    batch_result = output_dir / (
        f"p7-5-2-qwen-2511-mira-torso-multiview-{args.run_label}-"
        f"size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}-batch-result.json"
    )
    batch_result.write_text(
        json.dumps({**plan, "status": "generated", "outputs": results, "elapsed_seconds": round(time.monotonic() - started, 2)}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"batch_result": str(batch_result), "count": len(results)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

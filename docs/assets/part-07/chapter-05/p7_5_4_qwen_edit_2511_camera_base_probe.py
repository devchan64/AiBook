#!/usr/bin/env python3
"""Probe base Qwen-Image-Edit-2511 viewpoint editing without camera LoRAs.

Picture 1 is the complete Scene A storyboard. The prompt changes only its
viewpoint while preserving the scene's subject, action, clothing, setting, and
lighting. This script intentionally loads no Multiple-Angles, Lightning, or
other LoRA so its output isolates the base model's native viewpoint editing.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
DEFAULT_REFERENCE = ASSETS / (
    "p7-5-4-qwen-2511-mira-reference-scene-a-v7-size-1280x1280-seed-5420-steps-20.png"
)
DEFAULT_PROMPT = (
    "Change the camera viewpoint of Picture 1 to a front-left quarter view at eye level. "
    "Preserve Mira, her running action, clothing, the crowd of runners, the city street, and the lighting."
)
DEFAULT_SIZE = 1280
DEFAULT_STEPS = 20
DEFAULT_TRUE_CFG_SCALE = 4.0
DEFAULT_GUIDANCE_SCALE = 1.0
DEFAULT_NEGATIVE_PROMPT = " "
DEFAULT_SEED = 62294
DEFAULT_RUN_LABEL = "base-viewpoint-v1"


def sha256(path: Path) -> str:
    """Return the SHA-256 digest recorded for one image artifact."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_version(name: str) -> str | None:
    """Return an installed package version when available."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def parse_args() -> argparse.Namespace:
    """Parse a reproducible single-reference base-model camera experiment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--true-cfg-scale", type=float, default=DEFAULT_TRUE_CFG_SCALE)
    parser.add_argument("--run-label", default=DEFAULT_RUN_LABEL)
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.reference.is_file():
        parser.error(f"Missing Scene A reference: {args.reference}")
    if args.size < 32 or args.size % 32:
        parser.error("--size must be a positive multiple of 32")
    if args.steps < 1 or args.true_cfg_scale <= 0:
        parser.error("--steps and --true-cfg-scale must be positive")
    return args


def runtime_record() -> dict[str, object]:
    """Record the direct Diffusers environment used for the probe."""
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            name: package_version(name)
            for name in ("diffusers", "torch", "transformers", "accelerate")
        },
    }


def main() -> None:
    """Generate one base-model-only Scene A viewpoint-edit experiment."""
    args = parse_args()
    stem = (
        "p7-5-4-qwen-2511-camera-base-scene-a-front-left-quarter-eye-level-"
        f"{args.run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    )
    output = args.output_dir.resolve() / f"{stem}.png"
    result_path = output.with_name(f"{output.stem}-result.json")
    if args.dry_run:
        print(json.dumps({
            "status": "planned",
            "model": MODEL_ID,
            "camera_lora_used": False,
            "reference": str(args.reference.resolve()),
            "prompt": args.prompt,
            "sampling": {
                "steps": args.steps,
                "true_cfg_scale": args.true_cfg_scale,
                "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
                "guidance_scale": DEFAULT_GUIDANCE_SCALE,
            },
            "output": str(output),
        }, ensure_ascii=False, indent=2))
        return
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite prior output: {output}")

    import torch
    from diffusers import QwenImageEditPlusPipeline
    from diffusers.utils import load_image

    output.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipeline.enable_attention_slicing("max")
    pipeline.enable_sequential_cpu_offload()
    with torch.inference_mode():
        image = pipeline(
            image=load_image(str(args.reference)).convert("RGB").resize((args.size, args.size)),
            prompt=args.prompt,
            negative_prompt=DEFAULT_NEGATIVE_PROMPT,
            width=args.size,
            height=args.size,
            num_inference_steps=args.steps,
            true_cfg_scale=args.true_cfg_scale,
            guidance_scale=DEFAULT_GUIDANCE_SCALE,
            num_images_per_prompt=1,
            generator=torch.Generator(device="cuda").manual_seed(args.seed),
        ).images[0]
    image.save(output)
    result_path.write_text(json.dumps({
        "status": "generated",
        "stage": "base_model_viewpoint_edit_probe",
        "execution_mode": "direct Diffusers; BF16; sequential CPU offload; no ComfyUI server",
        "runtime": runtime_record(),
        "model": {
            "repository": MODEL_ID,
            "dtype": "bfloat16",
            "device_placement": "sequential_cpu_offload",
        },
        "camera_lora_used": False,
        "inputs": [{
            "role": "Picture 1: Scene A storyboard reference",
            "path": str(args.reference.resolve()),
            "sha256": sha256(args.reference),
        }],
        "prompt": args.prompt,
        "sampling": {
            "steps": args.steps,
            "true_cfg_scale": args.true_cfg_scale,
            "negative_prompt": DEFAULT_NEGATIVE_PROMPT,
            "guidance_scale": DEFAULT_GUIDANCE_SCALE,
        },
        "seed": args.seed,
        "size": [args.size, args.size],
        "output": {
            "path": str(output),
            "sha256": sha256(output),
            "width": image.width,
            "height": image.height,
        },
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

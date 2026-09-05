#!/usr/bin/env python3
"""Generate a Scene A camera view with Qwen Edit 2511 Multiple-Angles LoRA.

The camera vocabulary and prompt order follow ComfyUI-qwenmultiangle exactly:
``<sks> {azimuth} {elevation} {distance}``. Picture 1 is the complete Scene A
storyboard. The Three.js viewport from that repository is a prompt-authoring
UI, so this direct Diffusers runner retains its useful contract without
starting a ComfyUI server.
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
ANGLE_LORA_ID = "fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA"
ANGLE_LORA_FILENAME = "qwen-image-edit-2511-multiple-angles-lora.safetensors"
ANGLE_ADAPTER_NAME = "multiple_angles"
DEFAULT_LORA_STRENGTH = 0.9
LIGHTNING_ID = "lightx2v/Qwen-Image-Edit-2511-Lightning"
LIGHTNING_FILENAME = "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors"
LIGHTNING_DIR = PROJECT_ROOT / ".tmp" / "download" / "weight-lightx2v-qwen-image-edit-2511-lightning-4steps"
LIGHTNING_ADAPTER_NAME = "lightning4"
LIGHTNING_LORA_STRENGTH = 1.0
DEFAULT_REFERENCE = ASSETS / (
    "p7-5-4-qwen-2511-mira-reference-scene-a-v7-size-1280x1280-seed-5420-steps-20.png"
)
AZIMUTHS = (
    "front view",
    "front-right quarter view",
    "right side view",
    "back-right quarter view",
    "back view",
    "back-left quarter view",
    "left side view",
    "front-left quarter view",
)
ELEVATIONS = ("low-angle shot", "eye-level shot", "elevated shot", "high-angle shot")
DISTANCES = ("wide shot", "medium shot", "close-up")
DEFAULT_AZIMUTH = "front-left quarter view"
DEFAULT_ELEVATION = "eye-level shot"
DEFAULT_DISTANCE = "medium shot"
DEFAULT_SIZE = 1280
DEFAULT_STEPS = 4
DEFAULT_TRUE_CFG_SCALE = 1.0
DEFAULT_GUIDANCE_SCALE = 1.0
DEFAULT_NEGATIVE_PROMPT = None
DEFAULT_SEED = 62294
DEFAULT_RUN_LABEL = "multiangle-lightning4-v1"


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


def prompt_for(camera: tuple[str, str, str]) -> str:
    """Emit the exact Qwen Multiangle Camera prompt string."""
    return "<sks> " + " ".join(camera)


def parse_args() -> argparse.Namespace:
    """Parse one reproducible Scene A camera transformation request."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--azimuth", choices=AZIMUTHS, default=DEFAULT_AZIMUTH)
    parser.add_argument("--elevation", choices=ELEVATIONS, default=DEFAULT_ELEVATION)
    parser.add_argument("--distance", choices=DISTANCES, default=DEFAULT_DISTANCE)
    parser.add_argument("--lora-strength", type=float, default=DEFAULT_LORA_STRENGTH)
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
    if args.steps != DEFAULT_STEPS:
        parser.error("--steps must be 4 for the Lightning sampling profile")
    if args.true_cfg_scale <= 0:
        parser.error("--true-cfg-scale must be positive")
    if not 0.8 <= args.lora_strength <= 1.0:
        parser.error("--lora-strength must be within the model-card range 0.8–1.0")
    if not (LIGHTNING_DIR / LIGHTNING_FILENAME).is_file():
        parser.error(f"Missing Lightning LoRA: {LIGHTNING_DIR / LIGHTNING_FILENAME}")
    return args


def runtime_record() -> dict[str, object]:
    """Record the direct Diffusers environment used for the camera view."""
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            name: package_version(name)
            for name in ("diffusers", "torch", "transformers", "accelerate")
        },
    }


def main() -> None:
    """Generate one LoRA-conditioned Scene A camera transformation."""
    args = parse_args()
    camera = (args.azimuth, args.elevation, args.distance)
    prompt = prompt_for(camera)
    slug = "-".join(camera).replace(" ", "-")
    stem = (
        f"p7-5-4-qwen-2511-camera-scene-a-{slug}-{args.run_label}"
        f"-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    )
    output = args.output_dir.resolve() / f"{stem}.png"
    result_path = output.with_name(f"{output.stem}-result.json")
    if args.dry_run:
        print(json.dumps({
            "status": "planned",
            "model": MODEL_ID,
            "angle_lora": {
                "repository": ANGLE_LORA_ID,
                "weight": ANGLE_LORA_FILENAME,
                "adapter_name": ANGLE_ADAPTER_NAME,
                "strength": args.lora_strength,
            },
            "lightning_lora": {
                "repository": LIGHTNING_ID,
                "weight": LIGHTNING_FILENAME,
                "adapter_name": LIGHTNING_ADAPTER_NAME,
                "strength": LIGHTNING_LORA_STRENGTH,
            },
            "camera": {"azimuth": camera[0], "elevation": camera[1], "distance": camera[2]},
            "prompt": prompt,
            "reference": str(args.reference.resolve()),
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
    pipeline.load_lora_weights(
        ANGLE_LORA_ID,
        weight_name=ANGLE_LORA_FILENAME,
        adapter_name=ANGLE_ADAPTER_NAME,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipeline.load_lora_weights(
        str(LIGHTNING_DIR),
        weight_name=LIGHTNING_FILENAME,
        adapter_name=LIGHTNING_ADAPTER_NAME,
        local_files_only=True,
    )
    pipeline.set_adapters(
        [ANGLE_ADAPTER_NAME, LIGHTNING_ADAPTER_NAME],
        adapter_weights=[args.lora_strength, LIGHTNING_LORA_STRENGTH],
    )
    pipeline.enable_attention_slicing("max")
    pipeline.enable_sequential_cpu_offload()
    with torch.inference_mode():
        image = pipeline(
            image=load_image(str(args.reference)).convert("RGB").resize((args.size, args.size)),
            prompt=prompt,
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
        "stage": "multiangle_lora_camera_transform",
        "execution_mode": "direct Diffusers; BF16; sequential CPU offload; no ComfyUI server",
        "runtime": runtime_record(),
        "model": {
            "repository": MODEL_ID,
            "dtype": "bfloat16",
            "device_placement": "sequential_cpu_offload",
        },
        "angle_lora": {
            "repository": ANGLE_LORA_ID,
            "weight": ANGLE_LORA_FILENAME,
            "adapter_name": ANGLE_ADAPTER_NAME,
            "strength": args.lora_strength,
            "prompt_format": "<sks> [azimuth] [elevation] [distance]",
        },
        "lightning_lora": {
            "repository": LIGHTNING_ID,
            "weight": LIGHTNING_FILENAME,
            "adapter_name": LIGHTNING_ADAPTER_NAME,
            "strength": LIGHTNING_LORA_STRENGTH,
        },
        "text_encoder": {
            "architecture": "Qwen2.5-VL bundled with Qwen-Image-Edit-2511",
            "comfyui_equivalent": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
        },
        "inputs": [{
            "role": "Picture 1: Scene A storyboard reference",
            "path": str(args.reference.resolve()),
            "sha256": sha256(args.reference),
        }],
        "camera": {"azimuth": camera[0], "elevation": camera[1], "distance": camera[2]},
        "prompt": prompt,
        "sampling": {
            "profile": "lightning4",
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

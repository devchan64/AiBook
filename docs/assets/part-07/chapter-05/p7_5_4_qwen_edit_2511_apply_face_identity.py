#!/usr/bin/env python3
"""Refine one transferred P7-5.4 scene with a frontal face identity reference.

The official Qwen-Image-Edit-2511 card presents character consistency as an
edit from an input portrait.  This runner deliberately uses only two images:
Picture 1 is the already composed scene and Picture 2 is the frontal portrait.
It does not add an outfit, pose, camera, lighting, or third reference because
those would make a face-identity result hard to attribute.
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

from PIL import Image


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
DEFAULT_SCENE = ASSETS / (
    "p7-5-4-qwen-2509-relight-camera-a-delight-multireference-v1-"
    "size-1280x1280-seed-62294-steps-10.png"
)
DEFAULT_FACE = ASSETS / "p7-5-2-qwen-face-head-front-1024-reference-v1-seed-62294-steps-10-size-1024.png"

# Keep the edit instruction short.  The portrait is the identity source; the
# first image already carries the desired pose, outfit, camera and background.
BASE_PROMPT = (
    "Replace the woman's face and hairstyle in Picture 1 with the woman in Picture 2. "
    "Preserve Picture 1's pose, outfit, scene, lighting, and composition."
)


def sha256(path: Path) -> str:
    """Return the input or output file digest recorded in result.json."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def runtime_record() -> dict[str, object]:
    packages: dict[str, str] = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
    }


def square_canvas(path: Path, size: int) -> Image.Image:
    """Pad a reference to a square canvas instead of stretching its face."""
    with Image.open(path) as source:
        source = source.convert("RGBA")
        source.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - source.width) // 2, (size - source.height) // 2)
        canvas.alpha_composite(source, offset)
    return canvas.convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene-id", choices=("a", "b", "c"), default="a", help="Label used only in output filenames and result metadata.")
    parser.add_argument("--scene", type=Path, default=DEFAULT_SCENE, help="Picture 1: transferred scene to preserve.")
    parser.add_argument("--face", type=Path, default=DEFAULT_FACE, help="Picture 2: character face and hair identity reference.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1280, help="Square output edge; must be a multiple of 32.")
    parser.add_argument("--run-label", default="relight-multireference-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.steps < 1:
        parser.error("--steps must be positive")
    if args.size < 32 or args.size % 32:
        parser.error("--size must be a multiple of 32")
    scene = args.scene.resolve()
    face = args.face.resolve()
    for path in (scene, face):
        if not path.is_file():
            raise FileNotFoundError(path)
    output_dir = args.output_dir.resolve()
    stem = (
        f"p7-5-4-qwen-2511-face-identity-scene-{args.scene_id}-"
        f"{args.run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    )
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    plan = {
        "model": MODEL_ID,
        "reference_order": "scene-face",
        "prompt": BASE_PROMPT,
        "scene": str(scene),
        "scene_id": args.scene_id,
        "face": str(face),
        "output": str(output),
        "result": str(result),
        "size": [args.size, args.size],
        "seed": args.seed,
        "steps": args.steps,
        "true_cfg_scale": 4.0,
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    import torch
    from diffusers import QwenImageEditPlusPipeline

    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipeline.enable_sequential_cpu_offload()
    image = pipeline(
        image=[square_canvas(scene, args.size), square_canvas(face, args.size)],
        prompt=BASE_PROMPT,
        height=args.size,
        width=args.size,
        generator=torch.manual_seed(args.seed),
        true_cfg_scale=4.0,
        negative_prompt=" ",
        num_inference_steps=args.steps,
        guidance_scale=1.0,
        num_images_per_prompt=1,
    ).images[0]
    image.save(output)
    record = {
        "status": "generated",
        "stage": "face_hair_identity_refinement",
        "execution_mode": "direct Diffusers; official QwenImageEditPlusPipeline; no ComfyUI or GGUF",
        "runtime": runtime_record(),
        "model": {"repository": MODEL_ID, "dtype": "bfloat16", "device_placement": "sequential_cpu_offload"},
        "inputs": [
            {"role": "Picture 1: transferred scene, pose, outfit and composition", "path": str(scene), "sha256": sha256(scene)},
            {"role": "Picture 2: face and hair identity", "path": str(face), "sha256": sha256(face)},
        ],
        "reference_order": "scene-face",
        "scene_id": args.scene_id,
        "prompt": BASE_PROMPT,
        "seed": args.seed,
        "steps": args.steps,
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "output": {"path": str(output), "width": image.width, "height": image.height, "sha256": sha256(output)},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

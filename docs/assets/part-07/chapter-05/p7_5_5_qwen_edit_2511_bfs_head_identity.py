#!/usr/bin/env python3
"""Test BFS Head V5 as a face-and-hair-only identity pass on one P7-5.4 scene.

Picture 1 is the finished scene to preserve; Picture 2 is the frontal face
reference.  This order and prompt are the BFS Head V5 model-card contract.
The run deliberately adds no outfit, pose, camera, or lighting reference.
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
LORA_REF = "weight:mr2along-bfs-head-v5-2511"
LORA_DIR = PROJECT_ROOT / ".tmp" / "download" / LORA_REF.replace(":", "-")
LORA_FILE = "bfs_head_v5_2511_original.safetensors"
SCENE_SOURCES = {
    "a": ASSETS / "p7-5-5-qwen-2511-pose-identity-official-camera-scene-a-shadow-stage2-outfit-v2-size-1280x1280-seed-62294-steps-30.png",
    "b": ASSETS / "p7-5-5-qwen-2509-studio-delight-character-b-size-1280x1280-seed-62294-steps-10.png",
    "c": ASSETS / "p7-5-5-qwen-2509-studio-delight-character-c-shadow-stage2-outfit-no-closeup-v3-size-1280x1280-seed-62294-steps-10.png",
}
DEFAULT_FACE = ASSETS / "p7-5-2-qwen-torso-yaw-quarter-left-cfg4-yaw-1024-v4-seed-62294-steps-8.png"
PROMPT = (
    "head_swap: start with Picture 1 as the base image, keeping its lighting, "
    "environment, and background. remove the head from Picture 1 completely and "
    "replace it with the head from Picture 2, strictly preserving the hair, eye "
    "color, and nose structure of Picture 2. copy the eye direction, head rotation, "
    "and micro-expressions from Picture 1. high quality, sharp details, 4k"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def square_canvas(path: Path, size: int) -> Image.Image:
    with Image.open(path) as source:
        source = source.convert("RGBA")
        source.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        canvas.alpha_composite(source, ((size - source.width) // 2, (size - source.height) // 2))
    return canvas.convert("RGB")


def runtime_record() -> dict[str, object]:
    packages = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {"python": sys.version.split()[0], "platform": platform.platform(), "packages": packages}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene-id", choices=tuple(SCENE_SOURCES), default="c", help="Select the matching A/B/C DeLight character source.")
    parser.add_argument("--scene", type=Path, help="Override the DeLight character selected by --scene-id.")
    parser.add_argument("--face", type=Path, default=DEFAULT_FACE)
    parser.add_argument("--steps", type=int, default=10, help="Inference steps (default: 10; the 30-step comparison added no material identity gain).")
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--run-label", help="Output label; defaults to the selected Scene ID and 45-degree reference.")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32:
        parser.error("--steps must be positive and --size must be a positive multiple of 32")
    scene = (args.scene or SCENE_SOURCES[args.scene_id]).resolve()
    face = args.face.resolve()
    run_label = args.run_label or f"delight-character-cutout-{args.scene_id}-quarter-left-v1"
    lora_path = LORA_DIR / LORA_FILE
    for path in (scene, face):
        if not path.is_file():
            raise FileNotFoundError(path)
    output_dir = args.output_dir.resolve()
    stem = f"p7-5-5-qwen-2511-bfs-head-v5-{run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    output, result = output_dir / f"{stem}.png", output_dir / f"{stem}-result.json"
    plan = {"model": MODEL_ID, "scene_id": args.scene_id, "lora": str(lora_path), "reference_order": "scene-face", "prompt": PROMPT, "output": str(output), "result": str(result)}
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    if not lora_path.is_file():
        raise FileNotFoundError(lora_path)

    import torch
    from diffusers import QwenImageEditPlusPipeline

    started = time.monotonic()
    pipeline = QwenImageEditPlusPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR, local_files_only=True)
    pipeline.load_lora_weights(lora_path.parent, weight_name=lora_path.name, adapter_name="bfs_head_v5", local_files_only=True)
    pipeline.set_adapters("bfs_head_v5", adapter_weights=1.0)
    pipeline.enable_sequential_cpu_offload()
    image = pipeline(image=[square_canvas(scene, args.size), square_canvas(face, args.size)], prompt=PROMPT, height=args.size, width=args.size, generator=torch.manual_seed(args.seed), true_cfg_scale=4.0, negative_prompt=" ", num_inference_steps=args.steps, guidance_scale=1.0, num_images_per_prompt=1).images[0]
    output_dir.mkdir(parents=True, exist_ok=True)
    image.save(output)
    record = {
        "status": "generated", "stage": "bfs_head_v5_face_hair_identity", "execution_mode": "direct Diffusers; QwenImageEditPlusPipeline; sequential CPU offload",
        "runtime": runtime_record(), "model": {"repository": MODEL_ID, "dtype": "bfloat16"},
        "lora": {"repository": "mr2along/BFS", "revision": "d9ffba9012dfa1b299a4294572791c3275ae6ae4", "file": LORA_FILE, "sha256": sha256(lora_path), "weight": 1.0},
        "inputs": [{"role": "Picture 1: scene to preserve", "path": str(scene), "sha256": sha256(scene)}, {"role": "Picture 2: face and hair identity", "path": str(face), "sha256": sha256(face)}],
        "reference_order": "scene-face", "scene_id": args.scene_id, "run_label": run_label, "prompt": PROMPT, "seed": args.seed, "steps": args.steps, "true_cfg_scale": 4.0, "guidance_scale": 1.0,
        "output": {"path": str(output), "width": image.width, "height": image.height, "sha256": sha256(output)}, "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

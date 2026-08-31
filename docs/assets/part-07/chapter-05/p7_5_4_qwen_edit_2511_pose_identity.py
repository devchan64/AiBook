#!/usr/bin/env python3
"""Apply the character reference to the P7-5.4 A/B/C pose cutouts.

This follows the official Qwen-Image-Edit-2511 multi-image Diffusers example.
Picture 1 supplies pose and framing; Picture 2 supplies character identity and
outfit. Camera control was completed before these cutouts, so this runner uses
no camera LoRA, GGUF transformer, ComfyUI graph, or latent override.
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
DEFAULT_CHARACTER = ASSETS / "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30.png"
POSES = {
    "a": ASSETS / "p7-5-3-character-pose-cutout-white-official-camera-scene-a-v5.png",
    "b": ASSETS / "p7-5-4-character-pose-cutout-white-official-camera-scene-b-v6.png",
    "c": ASSETS / "p7-5-4-character-pose-cutout-white-official-camera-scene-c-v5.png",
}
# Baseline prompt validated by the P7-5.4 Qwen-Image-Edit-2509 pose-transfer run.
# Keep this exact wording as the common prompt for A/B/C identity-transfer tests.
BASE_PROMPT = "Replace the woman in Picture 1 with the woman in Picture 2, preserving the pose."


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
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
    }


def square_canvas(path: Path, size: int) -> Image.Image:
    """Return an RGB, white-backed square canvas without distorting the input."""
    with Image.open(path) as source:
        source = source.convert("RGBA")
        source.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - source.width) // 2, (size - source.height) // 2)
        canvas.alpha_composite(source, offset)
    return canvas.convert("RGB")


def load_outfit_identity(contract_path: Path) -> str:
    """Read the shared, concise outfit instruction used for character transfer."""
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    description = contract.get("outfit_identity_description")
    if not isinstance(description, str) or not description.strip():
        raise ValueError(f"Missing outfit_identity_description: {contract_path}")
    return description.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenes", nargs="+", choices=tuple(POSES), default=("a", "b", "c"))
    parser.add_argument("--character", type=Path, default=DEFAULT_CHARACTER)
    parser.add_argument("--identity-contract", type=Path, help="Optional JSON containing outfit_identity_description.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--size", type=int, default=1280, help="Square input/output canvas edge in pixels.")
    parser.add_argument("--run-label", default="direct-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.steps < 1:
        parser.error("--steps must be positive")
    if args.size < 32 or args.size % 32:
        parser.error("--size must be a multiple of 32")
    character = args.character.resolve()
    if not character.is_file():
        raise FileNotFoundError(character)
    identity_contract = args.identity_contract.resolve() if args.identity_contract else None
    if identity_contract is not None and not identity_contract.is_file():
        raise FileNotFoundError(identity_contract)
    outfit_identity = load_outfit_identity(identity_contract) if identity_contract else None
    prompt = f"{BASE_PROMPT} {outfit_identity}" if outfit_identity else BASE_PROMPT
    output_dir = args.output_dir.resolve()
    plans = []
    for scene in dict.fromkeys(args.scenes):
        pose = POSES[scene].resolve()
        if not pose.is_file():
            raise FileNotFoundError(pose)
        stem = f"p7-5-4-qwen-2511-pose-identity-official-camera-scene-{scene}-{args.run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
        plans.append({
            "scene": scene,
            "pose": pose,
            "pose_sha256": sha256(pose),
            "output": output_dir / f"{stem}.png",
            "result": output_dir / f"{stem}-result.json",
        })
    if args.dry_run:
        print(json.dumps({
            "execution_mode": "direct Diffusers; no ComfyUI or GGUF",
            "model": MODEL_ID,
            "base_prompt": BASE_PROMPT,
            "outfit_identity": outfit_identity,
            "prompt": prompt,
            "size": [args.size, args.size],
            "reference_order": "Picture 1 pose/framing, Picture 2 character identity/outfit",
            "plans": [{"scene": plan["scene"], "pose": str(plan["pose"]), "output": str(plan["output"]), "result": str(plan["result"])} for plan in plans],
        }, ensure_ascii=False, indent=2))
        return

    import torch
    from diffusers import QwenImageEditPlusPipeline

    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipeline.enable_sequential_cpu_offload()
    output_dir.mkdir(parents=True, exist_ok=True)
    character_sha256 = sha256(character)
    identity_contract_sha256 = sha256(identity_contract) if identity_contract else None
    character_image = square_canvas(character, args.size)
    for plan in plans:
        started = time.monotonic()
        image = pipeline(
            image=[square_canvas(plan["pose"], args.size), character_image],
            prompt=prompt,
            height=args.size,
            width=args.size,
            generator=torch.manual_seed(args.seed),
            true_cfg_scale=4.0,
            negative_prompt=" ",
            num_inference_steps=args.steps,
            guidance_scale=1.0,
            num_images_per_prompt=1,
        ).images[0]
        image.save(plan["output"])
        record = {
            "status": "generated",
            "stage": "pose_cutout_identity_transfer",
            "execution_mode": "direct Diffusers; official QwenImageEditPlusPipeline; no ComfyUI or GGUF",
            "runtime": runtime_record(),
            "model": {"repository": MODEL_ID, "dtype": "bfloat16", "device_placement": "sequential_cpu_offload"},
            "inputs": [
                {"role": "Picture 1: pose and framing", "path": str(plan["pose"]), "sha256": plan["pose_sha256"]},
                {"role": "Picture 2: character identity and outfit", "path": str(character), "sha256": character_sha256},
            ],
            "reference_order": "pose-character",
            "identity_contract": (
                {"path": str(identity_contract), "sha256": identity_contract_sha256}
                if identity_contract else None
            ),
            "camera": "not used; fixed by the input cutout",
            "generation_canvas": {"width": args.size, "height": args.size, "background": "white"},
            "base_prompt": BASE_PROMPT,
            "outfit_identity": outfit_identity,
            "prompt": prompt,
            "seed": args.seed,
            "steps": args.steps,
            "true_cfg_scale": 4.0,
            "guidance_scale": 1.0,
            "output": {
                "path": str(plan["output"]),
                "width": image.width,
                "height": image.height,
                "sha256": sha256(plan["output"]),
            },
            "elapsed_seconds": round(time.monotonic() - started, 2),
        }
        plan["result"].write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"scene": plan["scene"], "output": str(plan["output"]), "result": str(plan["result"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()

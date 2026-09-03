#!/usr/bin/env python3
"""Generate one frontal Mira torso reference from two Qwen-Image-Edit-2511 inputs.

Picture 1 supplies Mira's current front-face identity.  Picture 2 supplies
only the established head-and-chest framing.  Keeping those roles separate
avoids asking one reference to carry both identity and composition.

The runner calls Diffusers directly.  It does not start a ComfyUI server.
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
DEFAULT_HEAD = ASSETS / (
    "p7-5-2-mira-head-qwen-image-q4ks-comfy-direct-young-adult-v1-"
    "seed-62294-steps-30-size-1280.png"
)
DEFAULT_TORSO_FRAMING = ASSETS / (
    "p7-5-2-qwen-torso-yaw-front-cfg4-front-1024-v4-"
    "seed-62294-steps-8.png"
)
DEFAULT_IDENTITY_CONTRACT = ASSETS / "p7-5-2-mira-identity-contract.json"

def sha256(path: Path) -> str:
    """Return a stable content digest for a result record."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def runtime_record() -> dict[str, object]:
    """Record the local package versions that affect image generation."""
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
    """Pad instead of stretching each reference before multi-image editing."""
    with Image.open(path) as source:
        source = source.convert("RGBA")
        source.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - source.width) // 2, (size - source.height) // 2)
        canvas.alpha_composite(source, offset)
    return canvas.convert("RGB")


def load_inner_top_identity(path: Path) -> str:
    """Read torso-visible clothing from the shared Mira identity contract."""
    contract = json.loads(path.read_text(encoding="utf-8"))
    value = contract.get("inner_top_identity_description")
    if not isinstance(value, str) or not value.strip():
        raise ValueError("identity contract needs inner_top_identity_description")
    return value.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--head", type=Path, default=DEFAULT_HEAD, help="Picture 1: Mira front-face identity.")
    parser.add_argument("--torso-framing", type=Path, default=DEFAULT_TORSO_FRAMING, help="Picture 2: existing frontal chest composition.")
    parser.add_argument("--identity-contract", type=Path, default=DEFAULT_IDENTITY_CONTRACT, help="Shared Mira identity JSON; supplies the inner-top description.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1280, help="Square output edge; must be a multiple of 32.")
    parser.add_argument("--run-label", default="front-identity-framing-gray-inner-top-multiref-v2")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.steps < 1:
        parser.error("--steps must be positive")
    if args.size < 32 or args.size % 32:
        parser.error("--size must be a multiple of 32")

    head = args.head.resolve()
    torso_framing = args.torso_framing.resolve()
    identity_contract = args.identity_contract.resolve()
    for path in (head, torso_framing, identity_contract):
        if not path.is_file():
            raise FileNotFoundError(path)
    inner_top_identity = load_inner_top_identity(identity_contract)
    prompt = (
        "Picture 1 is Mira's facial identity. Picture 2 is only the frontal "
        "head-and-upper-torso framing. Generate one frontal chest reference of "
        "Mira: preserve Picture 1's young adult face, amber eyes, and "
        "petrol-teal bob; use Picture 2 only for centered shoulders and "
        f"mid-chest framing. She wears {inner_top_identity} "
        "Plain warm off-white background."
    )
    output_dir = args.output_dir.resolve()
    stem = (
        f"p7-5-2-qwen-2511-mira-torso-{args.run_label}-"
        f"size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    )
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    plan = {
        "model": MODEL_ID,
        "reference_order": "mira-face_identity, torso-framing",
        "prompt": prompt,
        "head": str(head),
        "torso_framing": str(torso_framing),
        "identity_contract": str(identity_contract),
        "inner_top_identity_description": inner_top_identity,
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
        image=[square_canvas(head, args.size), square_canvas(torso_framing, args.size)],
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
    image.save(output)
    record = {
        "status": "generated",
        "stage": "mira_torso_multireference_generation",
        "execution_mode": "direct Diffusers; QwenImageEditPlusPipeline; no ComfyUI server",
        "runtime": runtime_record(),
        "model": {
            "repository": MODEL_ID,
            "dtype": "bfloat16",
            "device_placement": "sequential_cpu_offload",
        },
        "inputs": [
            {
                "role": "Picture 1: Mira face and hair identity",
                "path": str(head),
                "sha256": sha256(head),
            },
            {
                "role": "Picture 2: frontal head-and-chest framing only",
                "path": str(torso_framing),
                "sha256": sha256(torso_framing),
            },
            {
                "role": "Mira identity contract: torso-visible inner top",
                "path": str(identity_contract),
                "sha256": sha256(identity_contract),
            },
        ],
        "reference_order": "mira-face_identity, torso-framing",
        "identity_contract": str(identity_contract),
        "inner_top_identity_description": inner_top_identity,
        "prompt": prompt,
        "seed": args.seed,
        "steps": args.steps,
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "output": {
            "path": str(output),
            "width": image.width,
            "height": image.height,
            "sha256": sha256(output),
        },
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

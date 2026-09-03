#!/usr/bin/env python3
"""Generate a frontal Mira head-and-shoulders reference with a gray inner top.

Picture 1 is the BF16-generated frontal Mira head.  The fitted neutral-gray
inner-top specification comes from the Mira identity contract rather than a
second image, so the result record distinguishes visual identity input from
garment text constraints.  This is a direct Diffusers runner; it starts no
ComfyUI server or HTTP API.
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
DEFAULT_HEAD = ASSETS / (
    "p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-"
    "seed-62294-steps-30-size-1280.png"
)
DEFAULT_IDENTITY = ASSETS / "p7-5-2-mira-identity-contract.json"


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


def prompt_for(identity: dict[str, object]) -> str:
    top = identity["inner_top_identity"]
    color = top["color"]
    return (
        "Expand Picture 1 into a strict frontal head-and-shoulders studio portrait of the same adult woman. "
        "Preserve her face, jaw-length petrol-teal bob, pale-peach skin, and amber-brown eyes. "
        "Show both shoulders and the upper chest. "
        f"She wears a fitted {color['name']} {top['garment']} with a {top['neckline']} neckline and {top['sleeves']} sleeves. "
        "Use a plain warm off-white background."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--head", type=Path, default=DEFAULT_HEAD)
    parser.add_argument("--identity", type=Path, default=DEFAULT_IDENTITY)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32:
        parser.error("--steps must be positive; --size must be a multiple of 32 and at least 32")

    head = args.head.resolve()
    identity_path = args.identity.resolve()
    if not head.is_file() or not identity_path.is_file():
        raise FileNotFoundError(head if not head.is_file() else identity_path)
    identity = json.loads(identity_path.read_text(encoding="utf-8"))
    prompt = prompt_for(identity)
    stem = (
        f"p7-5-2-qwen-2511-mira-front-shoulders-gray-inner-top-{args.run_label}-"
        f"size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    )
    output_dir = args.output_dir.resolve()
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    plan = {
        "model": MODEL_ID,
        "inputs": [
            {"role": "Picture 1: Mira frontal head identity", "path": str(head), "sha256": sha256(head)},
            {"role": "text contract: gray inner-top identity", "path": str(identity_path), "sha256": sha256(identity_path)},
        ],
        "prompt": prompt,
        "size": [args.size, args.size],
        "steps": args.steps,
        "seed": args.seed,
        "output": str(output),
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    import torch
    from diffusers import QwenImageEditPlusPipeline
    from diffusers.utils import load_image

    started = time.monotonic()
    output_dir.mkdir(parents=True, exist_ok=True)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipeline.enable_sequential_cpu_offload()
    image = pipeline(
        image=[load_image(str(head))],
        prompt=prompt,
        height=args.size,
        width=args.size,
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        guidance_scale=1.0,
        negative_prompt=" ",
        num_inference_steps=args.steps,
    ).images[0]
    image.save(output)
    record = {
        "status": "generated",
        "experiment_id": "p7-5-2-mira-front-shoulders-gray-inner-top",
        "stage": "front_shoulders_identity_expansion",
        "execution_mode": "direct Diffusers; QwenImageEditPlusPipeline; no ComfyUI server",
        "runtime": runtime_record(),
        "model": {"repository": MODEL_ID, "dtype": "bfloat16", "device_placement": "sequential_cpu_offload"},
        "inputs": plan["inputs"],
        "prompt": prompt,
        "identity_contract": {
            "character_name": identity["character_name"],
            "inner_top": identity["inner_top_identity"],
        },
        "seed": args.seed,
        "steps": args.steps,
        "size": [args.size, args.size],
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "output": {"path": str(output), "sha256": sha256(output), "width": image.width, "height": image.height},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

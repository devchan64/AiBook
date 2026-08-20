#!/usr/bin/env python3
"""Generate review-only Qwen text-to-image candidates for front outfit anchors.

This generator has no image input.  It is separate from the Qwen Edit pilot so
the apparel reference is not confused with an identity-preserving edit.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path

import torch
from diffusers import QwenImagePipeline
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
PLAN = ASSETS / "p7-5-2-qwen-edit-transition-plan.json"
IDENTITY_CONTRACT = ASSETS / "p7-5-2-character-identity-contract.json"
STYLE_CONTRACT = ASSETS / "p7-5-2-character-reference-style-prompt-contract.json"
ILLUSTRATION_CONTRACT = ASSETS / "p7-5-2-character-reference-illustration-prompt-contract.json"
MODEL_ID = "Qwen/Qwen-Image"
TRANSFORMER_ID = "/home/cbsim/.cache/huggingface/hub/models--nunchaku-tech--nunchaku-qwen-image/snapshots/4d9f4f667ea571ab172e0ee29ac2c27b82a41a6b/svdq-fp4_r128-qwen-image.safetensors"
# Candidate filenames identify their generator and run; do not create a
# separate candidate directory.
OUTPUT_DIR = ASSETS
DEFAULT_STEPS = 10
SIZE = (768, 1152)
TARGETS = {
    "front_hip": (
        "Create one isolated front apparel-and-bag reference from shoulders through hips on a neutral headless torso. "
        "Show a very short white cropped utility jacket as the closed outer layer: its front panels cover the chest, two flap chest pockets and "
        "long cuffed sleeves are visible, and its hem ends immediately below the bust. Only below that hem, show a charcoal-gray micro-crop "
        "inner top, then a clear bare-midriff band, then the navel-height waistband of deep-teal high-waisted wide-leg trousers. Place one compact "
        "deep-navy woven-canvas crossbody bag at the wearer's outer-left hip. Show exactly one taut matching navy strap from the wearer's right "
        "shoulder across the exterior of the white jacket to the bag. Plain off-white background; no head, hands, legs, text, logo, hanger, extra strap, or other object."
    ),
    "front_full_length": (
        "Front full-length women's outfit reference. White ultra-short utility jacket ending immediately below the bust, gray crop top, clear bare-midriff "
        "band, deep-teal high-waisted wide-leg trousers, white low-top sneakers, navy crossbody bag and one strap. Plain off-white background."
    ),
}


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
    for name in ("nunchaku", "diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = "not-installed"
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": packages,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def load_pipeline() -> QwenImagePipeline:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    pipe = QwenImagePipeline.from_pretrained(
        MODEL_ID,
        transformer=transformer,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    pipe._exclude_from_cpu_offload.append("transformer")
    pipe.enable_sequential_cpu_offload()
    return pipe


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=tuple(TARGETS), default="front_hip")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--run-label", default="front-outfit")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    if missing := [path for path in (PLAN, IDENTITY_CONTRACT, STYLE_CONTRACT, ILLUSTRATION_CONTRACT) if not path.is_file()]:
        raise FileNotFoundError("missing P7-5.2 contract: " + ", ".join(map(str, missing)))

    illustration_prompt = json.loads(ILLUSTRATION_CONTRACT.read_text(encoding="utf-8"))["illustration_prompt"]
    prompt = f"{illustration_prompt} {TARGETS[args.target]}"
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"p7-5-2-qwen-outfit-{args.target}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output = output_dir / f"{stem}.png"
    run_record = output_dir / f"{stem}-run.json"

    started = time.monotonic()
    pipeline = load_pipeline()
    image = pipeline(
        prompt=prompt,
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        guidance_scale=1.0,
        negative_prompt=" ",
        num_inference_steps=args.steps,
        width=SIZE[0],
        height=SIZE[1],
    ).images[0]
    image.save(output)
    record = {
        "status": "review_required",
        "experiment_id": f"p7-5-2-qwen-outfit-{args.target}",
        "model": MODEL_ID,
        "transformer": TRANSFORMER_ID,
        "runtime": runtime_record(),
        "transition_plan": asset_record(PLAN),
        "identity_contract": asset_record(IDENTITY_CONTRACT),
        "style_prompt_contract": asset_record(STYLE_CONTRACT),
        "illustration_prompt_contract": asset_record(ILLUSTRATION_CONTRACT),
        "prompt_contracts_applied": {"watercolor_style": False, "illustration": True},
        "inputs": [],
        "input_roles": [],
        "target": args.target,
        "seed": args.seed,
        "steps": args.steps,
        "size": list(SIZE),
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "negative_prompt": " ",
        "prompt": prompt,
        "prompt_word_count": len(prompt.split()),
        "output": asset_record(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "Candidate only; do not replace an approved outfit reference before human review.",
    }
    run_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "run_record": str(run_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

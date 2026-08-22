#!/usr/bin/env python3
"""Generate front outfit references while preserving a supplied frontal head."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path

import torch
from diffusers import QwenImageEditPlusPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
IDENTITY_CONTRACT = ASSETS / "p7-5-7-face-identity-contract.json"
STYLE_CONTRACT = ASSETS / "p7-5-7-face-style-prompt-contract.json"
ILLUSTRATION_CONTRACT = ASSETS / "p7-5-7-face-illustration-prompt-contract.json"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
QWEN_FACE_REFERENCE = "p7-5-7-qwen-face-head-front-1024-reference-v1-seed-62294-steps-10-size-1024.png"
# Candidate filenames identify their generator and run; do not create a
# separate candidate directory.
OUTPUT_DIR = ASSETS
DEFAULT_STEPS = 10
SIZE = (960, 1440)
NEGATIVE_PROMPT = "duplicate bag, second strap, crossed straps, X-shaped straps, backpack, rolled sleeves, pushed-up sleeves, three-quarter sleeves, short sleeves, exposed wrists, vest pockets, text, panel, collage"
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
        "Image 1 is face identity and hair only; preserve the compact oval face, amber irises, asymmetric fringe, and petrol-teal jaw-length bob. "
        "Create one upright strict-front full-length adult woman with a fitted feminine silhouette. She wears an open-front white bolero jacket: a very short "
        "chest-length jacket with a standing neck collar, front panels ending immediately below the bust, and smooth long sleeves extending past the wrist bones to "
        "the heels of the hands. Under it "
        "is a plain charcoal-gray sleeveless underbust crop vest with no pockets. Leave the waist and navel visible above deep-teal high-waisted wide-leg trousers and white low-top sneakers. Add one compact navy "
        "crossbody bag at the wearer's outer-left hip, connected by one navy diagonal strap from the wearer's right shoulder. Plain warm off-white background."
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


def load_pipeline() -> QwenImageEditPlusPipeline:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    pipe = QwenImageEditPlusPipeline.from_pretrained(
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
    parser.add_argument("--target", choices=tuple(TARGETS), default="front_full_length")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--run-label", default="front-outfit")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    if missing := [path for path in (ASSETS / QWEN_FACE_REFERENCE, IDENTITY_CONTRACT, STYLE_CONTRACT, ILLUSTRATION_CONTRACT) if not path.is_file()]:
        raise FileNotFoundError("missing P7-5.7 face reference or prompt contract: " + ", ".join(map(str, missing)))

    illustration_prompt = json.loads(ILLUSTRATION_CONTRACT.read_text(encoding="utf-8"))["front_face_illustration_prompt"]
    prompt = f"{illustration_prompt} {TARGETS[args.target]}"
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"p7-5-2-qwen-outfit-{args.target}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output = output_dir / f"{stem}.png"
    result_record = output_dir / f"{stem}-result.json"

    started = time.monotonic()
    pipeline = load_pipeline()
    image = pipeline(
        prompt=prompt,
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        guidance_scale=1.0,
        negative_prompt=NEGATIVE_PROMPT,
        num_inference_steps=args.steps,
        width=SIZE[0],
        height=SIZE[1],
        image=[load_image(str(ASSETS / QWEN_FACE_REFERENCE)).convert("RGB")],
    ).images[0]
    image.save(output)
    record = {
        "status": "generated",
        "experiment_id": f"p7-5-2-qwen-outfit-{args.target}",
        "model": MODEL_ID,
        "transformer": TRANSFORMER_ID,
        "runtime": runtime_record(),
        "identity_contract": asset_record(IDENTITY_CONTRACT),
        "style_prompt_contract": asset_record(STYLE_CONTRACT),
        "illustration_prompt_contract": asset_record(ILLUSTRATION_CONTRACT),
        "prompt_contracts_applied": {"watercolor_style": False, "illustration": True},
        "inputs": [asset_record(ASSETS / QWEN_FACE_REFERENCE)],
        "input_roles": ["frontal_head_identity_and_hair"],
        "target": args.target,
        "seed": args.seed,
        "steps": args.steps,
        "size": list(SIZE),
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "negative_prompt": NEGATIVE_PROMPT,
        "prompt": prompt,
        "prompt_word_count": len(prompt.split()),
        "output": asset_record(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "Generated full-length outfit reference; compare face identity, outfit, bag, and framing with the stated input role.",
    }
    result_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result_record": str(result_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate front outfit references without a face-reference input."""

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
from nunchaku import NunchakuQwenImageTransformer2DModel
from PIL import Image


ASSETS = Path(__file__).resolve().parent
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
# Candidate filenames identify their generator and run; do not create a
# separate candidate directory.
OUTPUT_DIR = ASSETS
DEFAULT_STEPS = 10
SIZE = (960, 1440)
NEGATIVE_PROMPT = "rolled sleeves, pushed-up sleeves, three-quarter sleeves, exposed wrists, vest pockets, text, panel, collage"
BASE_OUTFIT_PROMPT = (
    "Photorealistic fashion catalog photograph. Front full-length women's outfit worn by an invisible woman: no head, hair, face, skin, or body. Charcoal-gray slim-fit micro crop T-shirt with "
    "short sleeves and round neck, hem at the underside of the bust. Wide midriff gap. Deep-teal feminine high-waisted wide-leg eight-tenths "
    "cropped trousers with generous width from hips to hems; hems clearly above "
    "the ankles with a gap before white low-top sneakers. No bag or strap. Warm off-white background."
)
JACKET_PROMPT = (
    "Photorealistic fashion catalog photograph. Use image 1 as the exact outfit base. Preserve its gray slim-fit micro crop T-shirt, midriff gap, deep-teal feminine wide-leg eight-tenths trousers, and white sneakers. "
    "Add only a feminine white cropped riding jacket with white lining, a pointed shirt collar, and long sleeves to the wrists. The invisible woman wears it: no head, hair, face, skin, or body. No bag or strap."
)


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
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--run-label", default="front-outfit")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"p7-5-2-qwen-outfit-front_full_length-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output = output_dir / f"{stem}.png"
    stage_one_output = output_dir / f"{stem}-stage-1-base.png"
    result_record = output_dir / f"{stem}-result.json"

    started = time.monotonic()
    pipeline = load_pipeline()
    stage_one = pipeline(
        prompt=BASE_OUTFIT_PROMPT,
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        guidance_scale=1.0,
        negative_prompt=NEGATIVE_PROMPT,
        num_inference_steps=args.steps,
        width=SIZE[0],
        height=SIZE[1],
        # Qwen Edit requires an image argument. This neutral canvas deliberately
        # contributes no face, hair, person, or outfit reference information.
        image=[Image.new("RGB", SIZE, "#f5f1e9")],
    ).images[0]
    stage_one.save(stage_one_output)
    image = pipeline(
        prompt=JACKET_PROMPT,
        generator=torch.Generator("cpu").manual_seed(args.seed + 1),
        true_cfg_scale=4.0,
        guidance_scale=1.0,
        negative_prompt=NEGATIVE_PROMPT,
        num_inference_steps=args.steps,
        width=SIZE[0],
        height=SIZE[1],
        image=[stage_one],
    ).images[0]
    image.save(output)
    record = {
        "status": "generated",
        "experiment_id": "p7-5-2-qwen-outfit-front_full_length",
        "model": MODEL_ID,
        "transformer": TRANSFORMER_ID,
        "runtime": runtime_record(),
        "inputs": [asset_record(stage_one_output)],
        "input_roles": ["stage_1_base_outfit"],
        "target": "front_full_length",
        "seed": args.seed,
        "steps": args.steps,
        "size": list(SIZE),
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "negative_prompt": NEGATIVE_PROMPT,
        "stages": [
            {"stage": 1, "prompt": BASE_OUTFIT_PROMPT, "output": asset_record(stage_one_output)},
            {"stage": 2, "prompt": JACKET_PROMPT, "input": asset_record(stage_one_output), "output": asset_record(output)},
        ],
        "prompt": JACKET_PROMPT,
        "prompt_word_count": len(BASE_OUTFIT_PROMPT.split()) + len(JACKET_PROMPT.split()),
        "output": asset_record(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "Generated the inner top, trousers, and sneakers first, then added the jacket without a face-reference input.",
    }
    result_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result_record": str(result_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

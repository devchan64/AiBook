#!/usr/bin/env python3
"""Run the P7-5.11 Qwen high-angle input-role comparison with new anchors.

The published P7-5.11 images preserve a historical comparison, but their
original face and outfit anchors were retired. This template requires explicit
replacement inputs: ``two-input`` passes a guide and a face, while
``role-separated`` adds an outfit-only third image. Every new output needs a
fresh result record and human review; it is not pixel-compared with the old
published images.
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

import torch
from diffusers import QwenImageEditPlusPipeline
from diffusers.utils import load_image
from huggingface_hub import snapshot_download
from nunchaku import NunchakuQwenImageTransformer2DModel


ROOT = Path(__file__).resolve().parents[4]
ASSETS = ROOT / "docs" / "assets" / "part-07" / "chapter-05"
HF_HUB_CACHE = ROOT / ".tmp" / "download" / "huggingface" / "hub"
DEFAULT_OUTPUT_DIR = ROOT / ".tmp" / "p7-5-11-qwen-edit-high-angle"
DEFAULT_GUIDE = ASSETS / "p7-5-11-experimental-animagine-high-angle-guide.png"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
TRANSFORMER_REPOSITORY = "nunchaku-tech/nunchaku-qwen-image-edit-2509"
TRANSFORMER_FILENAME = "svdq-fp4_r128-qwen-image-edit-2509.safetensors"
STEPS = 40

TWO_INPUT_PROMPT = (
    "Keep image 1's high-angle camera, framing, walking pose, tiled rooftop, and background. "
    "Replace only the person with the woman in image 2. Preserve her illustrated facial identity, "
    "petrol-teal jaw-length bob, and both amber irises."
)
ROLE_SEPARATED_PROMPT = (
    "Keep image 1's high-angle camera, framing, walking pose, tiled rooftop, and background. "
    "Replace only the person with the woman in image 2. Preserve her illustrated facial identity, "
    "petrol-teal jaw-length bob and both amber irises. Use image 3 only as the exact outfit reference: "
    "a white cropped jacket, wide-leg petrol-teal trousers, white low-top sneakers, and a navy crossbody bag, "
    "with the bag strap outside the jacket."
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
    packages = {}
    for name in ("nunchaku", "diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = "not-installed"
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def load_pipeline() -> QwenImageEditPlusPipeline:
    transformer_path = Path(snapshot_download(TRANSFORMER_REPOSITORY, cache_dir=HF_HUB_CACHE, local_files_only=True)) / TRANSFORMER_FILENAME
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(transformer_path)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(model_path, transformer=transformer, torch_dtype=torch.bfloat16, local_files_only=True)
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline


def configuration(condition: str, seed: int, guide: Path, face: Path, outfit: Path | None) -> tuple[list[Path], str, str]:
    if condition == "two-input":
        return [guide, face], TWO_INPUT_PROMPT, f"qwen-edit-2509-two-input-high-angle-seed-{seed}-steps-40.png"
    if outfit is None:
        raise ValueError("--outfit is required for --condition role-separated")
    return [guide, face, outfit], ROLE_SEPARATED_PROMPT, f"qwen-edit-2509-three-input-face-outfit-contract-seed-{seed}-steps-40.png"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", choices=("two-input", "role-separated"), required=True)
    parser.add_argument("--guide", type=Path, default=DEFAULT_GUIDE, help="Composition-only guide image; defaults to the retained historical guide.")
    parser.add_argument("--face", type=Path, required=True, help="Current front-face identity anchor.")
    parser.add_argument("--outfit", type=Path, help="Current complete-outfit anchor; required for role-separated.")
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--steps", type=int, default=STEPS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    if args.steps != STEPS:
        raise ValueError("this historical comparison fixes --steps at 40; make a separately labelled experiment for another value")

    inputs, prompt, filename = configuration(args.condition, args.seed, args.guide, args.face, args.outfit)
    if missing := [str(path) for path in inputs if not path.is_file()]:
        raise FileNotFoundError("missing input asset(s): " + ", ".join(missing))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    result = load_pipeline()(
        image=[load_image(str(path)).convert("RGB") for path in inputs],
        prompt=prompt,
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        negative_prompt=" ",
        num_inference_steps=args.steps,
        guidance_scale=1.0,
    ).images[0]
    output = args.output_dir / filename
    result.save(output)
    output_hash = sha256(output)
    record = {
        "status": "human_review_required",
        "experiment_id": f"p7-5-11-qwen-high-angle-{args.condition}",
        "model": "Qwen-Image-Edit-2509 with Nunchaku FP4 r128 per-layer CPU offload",
        "runtime": runtime_record(),
        "input_roles": {
            "composition": asset_record(args.guide),
            "face_identity": asset_record(args.face),
            "complete_outfit": asset_record(args.outfit) if args.condition == "role-separated" else None,
        },
        "seed": args.seed,
        "steps": args.steps,
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "negative_prompt": " ",
        "prompt": prompt,
        "output": asset_record(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "The historical P7-5.11 anchors were retired. Do not compare this result pixel-for-pixel with the published sheet or infer a pass without new human review.",
    }
    result_path = args.output_dir / f"{output.stem}-result.json"
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result_record": str(result_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

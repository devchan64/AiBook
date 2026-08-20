#!/usr/bin/env python3
"""Generate review-only Qwen text-to-image candidates for the frontal head anchor.

This is intentionally separate from ``p7_5_2_qwen_edit_reference_pilot.py``:
it has no image input and must not silently become an image-edit experiment.
The generated PNG and its run JSON remain candidates until human approval.
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
OUTPUT_DIR = ASSETS / "p7-5-2-qwen-head-candidates"
DEFAULT_STEPS = 10
SIZE = (768, 768)
FRONT_HEAD_PROMPT = (
    "Strict frontal head-and-neck studio reference of one young East Asian woman in her early twenties, face centered and facing the camera "
    "with both eyes and ears visible: compact oval face, a defined high nose bridge, and a refined straight nose line; high-volume petrol-teal "
    "jaw-length bob with asymmetric fringe, loose S-waves, inward-curled ends, and side locks wider than the neck. Long slender gently upturned "
    "eyes; equal orange-amber irises with distinct centered round dark pupils, separate from eyelids and eyeliner. Show ears and neck. "
    "No text, accessory, panel, collage, or background scene."
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
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--run-label", default="front-head")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    if missing := [path for path in (PLAN, IDENTITY_CONTRACT, STYLE_CONTRACT, ILLUSTRATION_CONTRACT) if not path.is_file()]:
        raise FileNotFoundError("missing P7-5.2 contract: " + ", ".join(map(str, missing)))

    illustration_prompt = json.loads(ILLUSTRATION_CONTRACT.read_text(encoding="utf-8"))["illustration_prompt"]
    prompt = f"{illustration_prompt} {FRONT_HEAD_PROMPT}"
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"p7-5-2-qwen-head-front-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
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
        "experiment_id": "p7-5-2-qwen-head-front",
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
        "decision": "Candidate only; do not replace the approved frontal head reference before human review.",
    }
    run_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "run_record": str(run_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

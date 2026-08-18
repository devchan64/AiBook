#!/usr/bin/env python3
"""Generate a review-only Qwen ControlNet head-turn candidate.

This probe intentionally separates OpenPose structural control from identity
editing.  It uses QwenImageControlNetPipeline and its `control_image` input;
it does not pass the OpenPose map as a Qwen Edit reference image and does not
use any FLUX output.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import platform
import sys
import time
from pathlib import Path

import torch
from diffusers import QwenImageControlNetModel, QwenImageControlNetPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
STYLE_CONTRACT = ASSETS / "p7-5-2-character-reference-style-prompt-contract.json"
OUTPUT_DIR = ASSETS / "p7-5-2-qwen-controlnet-candidates"
BASE_MODEL = "Qwen/Qwen-Image"
CONTROLNET_MODEL = "InstantX/Qwen-Image-ControlNet-Union"
NUNCHAKU_TRANSFORMER = Path(
    "/home/cbsim/.cache/huggingface/hub/models--nunchaku-tech--nunchaku-qwen-image/"
    "snapshots/4d9f4f667ea571ab172e0ee29ac2c27b82a41a6b/svdq-fp4_r128-qwen-image.safetensors"
)
DEFAULT_SEED = 119435
DEFAULT_STEPS = 30


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def record_asset(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": sha256(path)}


def runtime_record() -> dict[str, object]:
    packages: dict[str, str] = {}
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


def make_openpose_guide(target: str, path: Path) -> None:
    """Render the target geometry with controlnet_aux's standard OpenPose renderer."""
    source = ASSETS / "p7_5_2_qwen_edit_reference_pilot.py"
    spec = importlib.util.spec_from_file_location("p7_5_2_openpose_guide_source", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("P7-5.2 OpenPose guide source is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.save_openpose_guide(target, path)


def load_pipeline() -> QwenImageControlNetPipeline:
    if not NUNCHAKU_TRANSFORMER.is_file():
        raise FileNotFoundError(NUNCHAKU_TRANSFORMER)
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(str(NUNCHAKU_TRANSFORMER))
    controlnet = QwenImageControlNetModel.from_pretrained(
        CONTROLNET_MODEL, torch_dtype=torch.bfloat16, local_files_only=True
    )
    pipe = QwenImageControlNetPipeline.from_pretrained(
        BASE_MODEL,
        transformer=transformer,
        controlnet=controlnet,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipe._exclude_from_cpu_offload.append("transformer")
    pipe.enable_sequential_cpu_offload()
    return pipe


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--control-scale", type=float, default=1.0)
    parser.add_argument(
        "--map-target",
        choices=("face_front_quarter_left", "face_front_quarter_right"),
        default="face_front_quarter_right",
        help="OpenPose geometry to test independently from the fixed right-facing text prompt.",
    )
    parser.add_argument("--run-label", default="v1-openpose-controlnet-right-quarter")
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not 0.0 <= args.control_scale <= 2.0:
        raise ValueError("--control-scale must be between 0.0 and 2.0")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    guide = ASSETS / "p7-5-2-qwen-edit-candidates" / "p7-5-2-openpose-fullbody-quarter-left-45deg-guide.png"
    if not guide.is_file():
        raise FileNotFoundError(guide)
    style = json.loads(STYLE_CONTRACT.read_text(encoding="utf-8"))["portrait_style_prompt"]
    prompt = (
        "One young East Asian adult woman, full body from hair crown to shoe soles, in a true 45-degree left-facing front-quarter view. "
        "Her nose, torso, and feet point toward image left. Wear a short white cropped utility jacket with sleeves down to the wrists, "
        "gray inner crop top, visible midriff gap, high-waisted deep-teal wide-leg trousers, white low-top sneakers, and a navy crossbody bag "
        "with its strap outside the jacket. Petrol-teal jaw-length bob, orange-amber irises, plain warm off-white studio background. "
        f"{style}"
    )
    stem = (
        f"p7-5-2-qwen-controlnet-fullbody-quarter-left-{args.run_label}-"
        f"seed-{args.seed}-steps-{args.steps}"
    )
    output = OUTPUT_DIR / f"{stem}.png"
    run_record = OUTPUT_DIR / f"{stem}-run.json"
    started = time.monotonic()
    result = load_pipeline()(
        prompt=prompt,
        negative_prompt=" ",
        control_image=load_image(str(guide)).convert("RGB"),
        controlnet_conditioning_scale=args.control_scale,
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        num_inference_steps=args.steps,
        width=960,
        height=1440,
    ).images[0]
    result.save(output)
    record = {
        "status": "review_required",
        "experiment_id": "p7-5-2-qwen-controlnet-fullbody-quarter-left",
        "decision": "Candidate only; do not replace a stable P7-5.2 reference before human review.",
        "model": BASE_MODEL,
        "controlnet": CONTROLNET_MODEL,
        "transformer": str(NUNCHAKU_TRANSFORMER),
        "runtime": runtime_record(),
        "style_contract": record_asset(STYLE_CONTRACT),
        "control_image": record_asset(guide),
        "control_role": "standard_openpose_fullbody_45_degree_left_quarter_geometry",
        "map_target": "fullbody_quarter_left_45deg",
        "seed": args.seed,
        "steps": args.steps,
        "controlnet_conditioning_scale": args.control_scale,
        "true_cfg_scale": 4.0,
        "size": [960, 1440],
        "prompt": prompt,
        "prompt_word_count": len(prompt.split()),
        "output": record_asset(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    run_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "run_record": str(run_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

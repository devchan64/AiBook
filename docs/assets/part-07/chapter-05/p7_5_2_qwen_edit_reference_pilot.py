#!/usr/bin/env python3
"""Create review-only Qwen Edit candidates for the P7-5.2 front anchors.

The approved P7-5.2 Flux PNGs remain immutable inputs during this pilot.  This
script writes a separate candidate PNG and run record; it never changes a
stable reference, manifest, or approval status.
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
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
PLAN = ASSETS / "p7-5-2-qwen-edit-transition-plan.json"
IDENTITY_CONTRACT = ASSETS / "p7-5-2-character-identity-contract.json"
STYLE_CONTRACT = ASSETS / "p7-5-1-style-prompt-contract.json"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
OUTPUT_DIR = ASSETS / "p7-5-2-qwen-edit-candidates"
DEFAULT_STEPS = 20
QWEN_FACE_REFERENCE = "p7-5-2-face-front-qwen-prompt-style-reference.png"

TARGETS = {
    "face_front": {
        "inputs": ("p7-5-2-face-front-reference.png",),
        "size": (768, 768),
        "prompt": (
            "Use image 1 only as the exact front-face identity reference. Preserve its compact oval face, "
            "petrol-teal jaw-length bob, and long slender almond eyes with gently upturned outer corners, moderately narrow "
            "eyelid openings, and equal orange-amber irises. "
            "Create one clean strict frontal head-and-neck "
            "studio reference. No text, panel, collage, accessory, or background scene."
        ),
    },
    "fullbody_front_refined": {
        "inputs": (
            "p7-5-2-fullbody-front-refined-reference.png",
            QWEN_FACE_REFERENCE,
        ),
        "size": (960, 1440),
        "prompt": (
            "Use image 1 only as the exact front full-body composition and complete outfit reference. "
            "Use image 2 only as the exact face and hair identity reference. Keep hair-to-sole framing, upright pose, "
            "white cropped jacket over a gray inner top, bare midriff, high-waisted wide-leg deep-teal trousers, "
            "white low-top sneakers, navy crossbody bag, and its strap outside the jacket. One woman on an off-white "
            "studio background; complete limbs, no text, labels, panel, collage, or extra person."
        ),
    },
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
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def load_pipeline() -> QwenImageEditPlusPipeline:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    pipe = QwenImageEditPlusPipeline.from_pretrained(MODEL_ID, transformer=transformer, torch_dtype=torch.bfloat16)
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipe._exclude_from_cpu_offload.append("transformer")
    pipe.enable_sequential_cpu_offload()
    return pipe


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=tuple(TARGETS), required=True)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--run-label", default="v2-natural-eyes", help="Suffix that separates controlled reruns.")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    target = TARGETS[args.target]
    inputs = [ASSETS / name for name in target["inputs"]]
    if missing := [str(path) for path in inputs if not path.is_file()]:
        raise FileNotFoundError("missing input asset(s): " + ", ".join(missing))
    if not PLAN.is_file() or not IDENTITY_CONTRACT.is_file() or not STYLE_CONTRACT.is_file():
        raise FileNotFoundError("missing P7-5.2 Qwen transition plan, identity contract, or style contract")
    style_prompt = json.loads(STYLE_CONTRACT.read_text(encoding="utf-8"))["common_contract"]
    prompt = f"{target['prompt']} {style_prompt}"

    width, height = target["size"]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"p7-5-2-qwen-edit-prompt-style-{args.target}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output = args.output_dir / f"{stem}.png"
    run_record = args.output_dir / f"{stem}-run.json"
    started = time.monotonic()
    result = load_pipeline()(
        image=[load_image(str(path)).convert("RGB") for path in inputs],
        prompt=prompt,
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        negative_prompt=" ",
        num_inference_steps=args.steps,
        guidance_scale=1.0,
        width=width,
        height=height,
    ).images[0]
    result.save(output)
    record = {
        "status": "review_required",
        "experiment_id": f"p7-5-2-qwen-edit-{args.target}",
        "model": MODEL_ID,
        "transformer": TRANSFORMER_ID,
        "runtime": runtime_record(),
        "transition_plan": asset_record(PLAN),
        "identity_contract": asset_record(IDENTITY_CONTRACT),
        "style_prompt_contract": asset_record(STYLE_CONTRACT),
        "target": args.target,
        "run_label": args.run_label,
        "inputs": [asset_record(path) for path in inputs],
        "input_roles": ["face_identity"] if args.target == "face_front" else ["body_and_complete_outfit", "face_identity"],
        "seed": args.seed,
        "steps": args.steps,
        "size": [width, height],
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "negative_prompt": " ",
        "prompt": prompt,
        "prompt_word_count": len(prompt.split()),
        "output": asset_record(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "Candidate only; do not replace a stable P7-5.2 reference before human review.",
    }
    run_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "run_record": str(run_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

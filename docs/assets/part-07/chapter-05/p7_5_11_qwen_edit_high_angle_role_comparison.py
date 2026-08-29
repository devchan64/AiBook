#!/usr/bin/env python3
"""Reproduce the P7-5.11 high-angle Qwen input-role comparison.

The ``two-input`` condition generated
``p7-5-11-qwen-edit-two-input-outfit-loss.png``: composition plus face identity
leave the complete outfit unconstrained. The ``role-separated`` condition
generated the approved seed 62294/62295 pair by adding a third, outfit-only
reference. Outputs are candidates and require human review before reuse.
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
GUIDE = ASSETS / "p7-5-11-experimental-animagine-high-angle-guide.png"
FACE = ASSETS / "p7-5-3-face-front-reference.png"
OUTFIT = ASSETS / "p7-5-3-prop-reference-complete-outfit-front-hip.png"
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

# These hashes identify the historical source outputs copied into the published
# assets. A rerun can differ if the model, package versions, or runtime change.
EXPECTED_SHA256 = {
    ("two-input", 62294): "e9f03f9f308867d79a8c1c37b538190a776ef4a45a38e2c707040ebe9ac264a8",
    ("role-separated", 62294): "7f2d535032420271b9fcb5e561f20d0a9ce88fd0ab819ae73ad35d36ef7a0a1f",
    ("role-separated", 62295): "e09ffb940d1aae6ebe0751cf4d7a1b1810d1dc1b065294e1b8a4ea3c13eaf08d",
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


def configuration(condition: str, seed: int) -> tuple[list[Path], str, str]:
    if condition == "two-input":
        if seed != 62294:
            raise ValueError("the published two-input comparison used seed 62294")
        return [GUIDE, FACE], TWO_INPUT_PROMPT, "qwen-edit-2509-two-input-high-angle-seed-62294-steps-40.png"
    return [GUIDE, FACE, OUTFIT], ROLE_SEPARATED_PROMPT, f"qwen-edit-2509-three-input-face-outfit-contract-seed-{seed}-steps-40.png"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--condition", choices=("two-input", "role-separated"), required=True)
    parser.add_argument("--seed", type=int, required=True, help="62294 for either condition; 62295 also reproduces the approved role-separated pair.")
    parser.add_argument("--steps", type=int, default=STEPS)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    if args.steps != STEPS:
        raise ValueError("this historical comparison fixes --steps at 40; make a separately labelled experiment for another value")

    inputs, prompt, filename = configuration(args.condition, args.seed)
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
    expected_hash = EXPECTED_SHA256.get((args.condition, args.seed))
    record = {
        "status": "human_review_required",
        "experiment_id": f"p7-5-11-qwen-high-angle-{args.condition}",
        "model": "Qwen-Image-Edit-2509 with Nunchaku FP4 r128 per-layer CPU offload",
        "runtime": runtime_record(),
        "input_roles": {"composition": asset_record(GUIDE), "face_identity": asset_record(FACE), "complete_outfit": asset_record(OUTFIT) if args.condition == "role-separated" else None},
        "seed": args.seed,
        "steps": args.steps,
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "negative_prompt": " ",
        "prompt": prompt,
        "output": asset_record(output),
        "historical_output_sha256": expected_hash,
        "matches_historical_output": output_hash == expected_hash if expected_hash else None,
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "Do not replace the published reference or infer a pass without new human review.",
    }
    result_path = args.output_dir / f"{output.stem}-result.json"
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result_record": str(result_path), "matches_historical_output": record["matches_historical_output"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

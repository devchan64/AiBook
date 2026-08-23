#!/usr/bin/env python3
"""Generate five front-plane character-sheet turnaround references for P7-5.2.

The script deliberately keeps camera direction, outfit, and OpenPose in
separate inputs.  High/low chest references remain recorded for later pitch
experiments and are not mixed into this five-yaw baseline.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import torch
from diffusers import QwenImageEditPlusPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
OUTPUT_DIR = ASSETS
DEFAULT_STEPS = 30
DEFAULT_SIZE = (1024, 1536)
TRUE_CFG_SCALE = 4.0
STAGE3_OUTFIT = "p7-5-2-qwen-edit-prompt-style-outfit_stage3_crossbody_bag_face-stage3-crossbody-bag-v1-seed-62294-steps-30.png"
OPENPOSE_PREFIX = "p7-5-2-openpose-fullbody-hand-on-waist-pitch0"
FRONT_TORSO_DETAIL = "p7-5-7-qwen-torso-yaw-front-cfg4-front-1024-v4-seed-62294-steps-8.png"

# The relation-map generator keeps the right wrist at the waist.  The lowered
# left arm has an inward elbow and an outward wrist so its hand remains outside
# the bag silhouette in every full-body target.

# The complete supplied camera-reference library is kept explicit so pitch
# experiments can reuse the same controlled source set without rediscovery.
CAMERA_REFERENCE_LIBRARY = {
    "pitch_high": "p7-5-7-qwen-torso-pitch-high-angle-chest-reference-v1-seed-62294-steps-8.png",
    "pitch_low": "p7-5-7-qwen-torso-pitch-low-angle-chest-reference-v1-seed-62294-steps-8.png",
    "yaw_minus_90": "p7-5-7-qwen-torso-yaw-profile-left-chest-front-yaw-v1-seed-62294-steps-8.png",
    "yaw_minus_45": "p7-5-7-qwen-torso-yaw-quarter-left-cfg4-yaw-1024-v4-seed-62294-steps-8.png",
    "yaw_plus_45": "p7-5-7-qwen-torso-yaw-quarter-right-chest-front-yaw-v1-seed-62294-steps-8.png",
    "yaw_plus_90": "p7-5-7-qwen-torso-yaw-profile-right-chest-front-yaw-v1-seed-62294-steps-8.png",
    "yaw_minus_45_pitch_high": "p7-5-7-qwen-torso-yaw-quarter-left-chest-high-angle-yaw-v2-seed-62294-steps-8.png",
    "yaw_minus_45_pitch_low": "p7-5-7-qwen-torso-yaw-quarter-left-chest-low-angle-yaw-v2-seed-62294-steps-8.png",
    "yaw_plus_45_pitch_high": "p7-5-7-qwen-torso-yaw-quarter-right-chest-high-angle-yaw-v2-seed-62294-steps-8.png",
    "yaw_plus_45_pitch_low": "p7-5-7-qwen-torso-yaw-quarter-right-chest-low-angle-yaw-v2-seed-62294-steps-8.png",
}


def openpose(yaw: int) -> str:
    return f"{OPENPOSE_PREFIX}-yaw{yaw:+03d}_pitch+00.png"


def turnaround_target(yaw: int, view: str, camera_key: str | None) -> dict[str, object]:
    if yaw == 0:
        return {
            "inputs": (openpose(0), STAGE3_OUTFIT, FRONT_TORSO_DETAIL),
            "input_roles": ["front_fullbody_openpose", "complete_front_outfit", "front_torso_face_detail"],
            "prompt": "Render the full body of Image 2's woman in Image 1's hand-on-waist keypoint pose with natural bent elbows. Use Image 3 for her face, hair, and upper-torso detail.",
        }
    return {
        "inputs": (CAMERA_REFERENCE_LIBRARY[camera_key], STAGE3_OUTFIT, openpose(yaw)),
        "input_roles": ["yaw_camera_head_torso", "complete_front_outfit", "yaw_fullbody_openpose"],
        "prompt": (
            f"Render the full body of Image 2's woman at Image 1's {view} camera angle, "
            "in Image 3's hand-on-waist keypoint pose with natural bent elbows, against a plain "
            "light-gray studio background."
        ),
    }


TARGETS = {
    "yaw_minus_90": turnaround_target(-90, "left profile", "yaw_minus_90"),
    "yaw_minus_45": turnaround_target(-45, "left three-quarter", "yaw_minus_45"),
    "yaw_front": turnaround_target(0, "front", None),
    "yaw_plus_45": turnaround_target(45, "right three-quarter", "yaw_plus_45"),
    "yaw_plus_90": turnaround_target(90, "right profile", "yaw_plus_90"),
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
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        transformer=transformer,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline


def parse_size(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", maxsplit=1)
        width, height = int(width_text), int(height_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("--size must use WIDTHxHEIGHT, for example 1024x1536") from error
    if width < 16 or height < 16 or width % 16 or height % 16:
        raise argparse.ArgumentTypeError("--size values must be positive multiples of 16")
    return width, height


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=tuple(TARGETS), help="One yaw direction to generate.")
    parser.add_argument("--targets", nargs="+", choices=tuple(TARGETS), help="Generate yaw directions sequentially.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--size", type=parse_size, default=DEFAULT_SIZE)
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if bool(args.target) == bool(args.targets):
        parser.error("provide exactly one of --target or --targets")
    if args.targets:
        for target_id in args.targets:
            subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve()),
                    "--target",
                    target_id,
                    "--seed",
                    str(args.seed),
                    "--steps",
                    str(args.steps),
                    "--size",
                    f"{args.size[0]}x{args.size[1]}",
                    "--run-label",
                    args.run_label,
                    "--output-dir",
                    str(args.output_dir),
                ],
                check=True,
            )
        return
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    target = TARGETS[args.target]
    inputs = [ASSETS / name for name in target["inputs"]]
    if missing := [str(path) for path in inputs if not path.is_file()]:
        raise FileNotFoundError("missing input asset(s): " + ", ".join(missing))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    width, height = args.size
    stem = f"p7-5-2-qwen-character-sheet-{args.target}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output = args.output_dir / f"{stem}.png"
    result_record = args.output_dir / f"{stem}-result.json"
    started = time.monotonic()
    pipeline = load_pipeline()
    generation = {
        "prompt": target["prompt"],
        "generator": torch.Generator("cpu").manual_seed(args.seed),
        "true_cfg_scale": TRUE_CFG_SCALE,
        "negative_prompt": " ",
        "num_inference_steps": args.steps,
        "guidance_scale": 1.0,
        "num_images_per_prompt": 1,
        "max_sequence_length": 1024,
        "width": width,
        "height": height,
        "image": [load_image(str(path)).convert("RGB") for path in inputs],
    }
    result = pipeline(**generation).images[0]
    result.save(output)
    record = {
        "status": "generated",
        "experiment_id": "p7-5-2-qwen-character-sheet-turnaround",
        "model": MODEL_ID,
        "transformer": TRANSFORMER_ID,
        "runtime": runtime_record(),
        "target": args.target,
        "run_label": args.run_label,
        "inputs": [asset_record(path) for path in inputs],
        "input_roles": target["input_roles"],
        "camera_reference_library": {key: asset_record(ASSETS / name) for key, name in CAMERA_REFERENCE_LIBRARY.items()},
        "seed": args.seed,
        "steps": args.steps,
        "size": [width, height],
        "prompt": target["prompt"],
        "prompt_word_count": len(target["prompt"].split()),
        "true_cfg_scale": TRUE_CFG_SCALE,
        "negative_prompt": generation["negative_prompt"],
        "output": asset_record(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "Generated one character-sheet yaw reference; compare camera direction, outfit retention, and OpenPose silhouette.",
    }
    result_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result_record": str(result_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

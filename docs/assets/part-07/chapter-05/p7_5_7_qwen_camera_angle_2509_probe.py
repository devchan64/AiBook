#!/usr/bin/env python3
"""Create a review-only Qwen Edit 2509 camera-angle candidate.

This probe intentionally does not use OpenPose.  The dx8152 multiple-angle
LoRA owns the camera transform, while the approved frontal head is the only
image reference and therefore owns identity and illustration appearance.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import math
import platform
import sys
import time
from pathlib import Path

import torch
from diffusers import FlowMatchEulerDiscreteScheduler, QwenImageEditPlusPipeline
from diffusers.utils import load_image
from huggingface_hub import snapshot_download
from nunchaku import NunchakuQwenImageTransformer2DModel

# Review the third-party Nunchaku adapter implementation in /tmp before it is
# adopted into a maintained repository module.  Generic PEFT injection cannot
# target Nunchaku's AWQW4A16Linear blocks.
sys.path.insert(0, "/tmp")
from nunchaku_lora_qwen import apply_lora  # noqa: E402


ASSETS = Path(__file__).resolve().parent
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = (
    "nunchaku-tech/nunchaku-qwen-image-edit-2509/lightning-251115/"
    "svdq-fp4_r128-qwen-image-edit-2509-lightning-8steps-251115.safetensors"
)
ANGLE_LORA_REPO = "dx8152/Qwen-Edit-2509-Multiple-angles"
ANGLE_LORA_FILE = "镜头转换.safetensors"
FRONT_HEAD_REFERENCE = ASSETS / "p7-5-7-face-front-qwen-reference.png"
SIZE = (768, 768)
LIGHTNING_SCHEDULER_CONFIG = {
    "base_image_seq_len": 256,
    "base_shift": math.log(3),
    "invert_sigmas": False,
    "max_image_seq_len": 8192,
    "max_shift": math.log(3),
    "num_train_timesteps": 1000,
    "shift": 1.0,
    "shift_terminal": None,
    "stochastic_sampling": False,
    "time_shift_type": "exponential",
    "use_beta_sigmas": False,
    "use_dynamic_shifting": True,
    "use_exponential_sigmas": False,
    "use_karras_sigmas": False,
}
CAMERA_PROMPTS = {
    "quarter_right": "将镜头向右旋转45度。",
    "quarter_left": "将镜头向左旋转45度。",
    "profile_right": "将镜头向右旋转90度。",
    "profile_left": "将镜头向左旋转90度。",
    "front": "保持正面镜头。",
}
CAMERA_YAW_DEGREES = {
    "profile_left": -90,
    "quarter_left": -45,
    "quarter_right": 45,
    "profile_right": 90,
    "front": 0,
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
    for name in ("nunchaku", "diffusers", "torch", "transformers", "accelerate", "peft"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = "not-installed"
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": packages,
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def build_camera_prompt(target: str, pitch_degrees: int) -> str:
    """Compose the LoRA's Chinese camera command without identity text."""
    parts = [CAMERA_PROMPTS[target]]
    if pitch_degrees < 0:
        parts.append(f"将镜头向下旋转{abs(pitch_degrees)}度。")
    elif pitch_degrees > 0:
        parts.append(f"将镜头向上旋转{pitch_degrees}度。")
    return "".join(parts)


def load_pipeline(angle_lora: Path) -> tuple[QwenImageEditPlusPipeline, int]:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    # Standard PEFT injection cannot target Nunchaku's AWQW4A16Linear blocks.
    # This loader merges rank-decomposed weights into Nunchaku low-rank slots.
    applied_modules = apply_lora(transformer, angle_lora, strength=1.0)
    if applied_modules == 0:
        raise RuntimeError("The multiple-angle LoRA did not match any Nunchaku transformer modules")
    # Create the ping-pong offload buffers after the LoRA rank expansion.  The
    # manager clones its first transformer block, so doing this earlier locks
    # its buffers to the original rank-128 tensor shapes.
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        transformer=transformer,
        scheduler=FlowMatchEulerDiscreteScheduler.from_config(LIGHTNING_SCHEDULER_CONFIG),
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    pipe._exclude_from_cpu_offload.append("transformer")
    pipe.enable_sequential_cpu_offload()
    return pipe, applied_modules


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=tuple(CAMERA_PROMPTS), default="quarter_right")
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=tuple(CAMERA_PROMPTS),
        help="Generate these camera yaws sequentially with one loaded pipeline; overrides --target.",
    )
    parser.add_argument("--pitch-degrees", type=int, default=0)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--run-label", default="dx8152-camera-angle-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    if not FRONT_HEAD_REFERENCE.is_file():
        raise FileNotFoundError(FRONT_HEAD_REFERENCE)

    angle_lora_dir = Path(snapshot_download(ANGLE_LORA_REPO, local_files_only=True))
    angle_lora = angle_lora_dir / ANGLE_LORA_FILE
    if not angle_lora.is_file():
        raise FileNotFoundError(angle_lora)
    targets = list(args.targets or [args.target])
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    pipeline, applied_modules = load_pipeline(angle_lora)
    results = []
    for sequence_index, target in enumerate(targets, start=1):
        prompt = build_camera_prompt(target, args.pitch_degrees)
        stem = f"p7-5-7-qwen-head-{target}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
        output = output_dir / f"{stem}.png"
        run_record = output_dir / f"{stem}-run.json"
        started = time.monotonic()
        image = pipeline(
            prompt=prompt,
            image=[load_image(str(FRONT_HEAD_REFERENCE)).convert("RGB")],
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=1.0,
            guidance_scale=1.0,
            num_inference_steps=args.steps,
            width=SIZE[0],
            height=SIZE[1],
        ).images[0]
        image.save(output)
        record = {
            "status": "review_required",
            "experiment_id": "p7-5-7-qwen-camera-angle-2509",
            "model": MODEL_ID,
            "transformer": TRANSFORMER_ID,
            "angle_lora": {"repository": ANGLE_LORA_REPO, "weight": asset_record(angle_lora)},
            "runtime": runtime_record(),
            "inputs": [asset_record(FRONT_HEAD_REFERENCE)],
            "input_roles": ["approved_front_head_identity_and_illustration"],
            "openpose_used": False,
            "camera_transform_owner": "dx8152 multiple-angle LoRA",
            "angle_lora_applied_modules": applied_modules,
            "target": target,
            "yaw_degrees": CAMERA_YAW_DEGREES[target],
            "pitch_degrees": args.pitch_degrees,
            "sequence": {"index": sequence_index, "targets": targets},
            "seed": args.seed,
            "steps": args.steps,
            "size": list(SIZE),
            "true_cfg_scale": 1.0,
            "guidance_scale": 1.0,
            "prompt": prompt,
            "prompt_word_count": len(prompt.split()),
            "output": asset_record(output),
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "decision": "Candidate only; human review must confirm identity, hair, rendering, and camera direction.",
        }
        run_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        results.append({"output": str(output), "run_record": str(run_record)})
    print(json.dumps({"outputs": results}, ensure_ascii=False))


if __name__ == "__main__":
    main()

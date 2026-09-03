#!/usr/bin/env python3
"""Create a Qwen Edit 2509 camera-angle result.

This probe intentionally does not use OpenPose.  The dx8152 multiple-angle
LoRA owns the camera transform, while the supplied frontal reference is the
only image input and therefore owns identity and illustration appearance.
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
HF_HUB_CACHE = ASSETS.parents[3] / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = (
    "nunchaku-tech/nunchaku-qwen-image-edit-2509/lightning-251115/"
    "svdq-fp4_r128-qwen-image-edit-2509-lightning-8steps-251115.safetensors"
)
TRANSFORMER_REPOSITORY = "nunchaku-tech/nunchaku-qwen-image-edit-2509"
TRANSFORMER_FILENAME = (
    "lightning-251115/"
    "svdq-fp4_r128-qwen-image-edit-2509-lightning-8steps-251115.safetensors"
)
ANGLE_LORA_REPO = "dx8152/Qwen-Edit-2509-Multiple-angles"
ANGLE_LORA_FILE = "镜头转换.safetensors"
DEFAULT_REFERENCE_IMAGE = ASSETS / "p7-5-2-qwen-2511-mira-torso-front-identity-framing-neutral-gray-v3-size-1280x1280-seed-62294-steps-10.png"
SIZE = (1024, 1024)
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
YAW_PROMPTS = {
    "quarter_right": "将镜头向右旋转45度。",
    "quarter_left": "将镜头向左旋转45度。",
    "profile_right": "将镜头向右旋转90度。",
    "profile_left": "将镜头向左旋转90度。",
}
FRONT_PROMPT = "保持正面镜头。"
CAMERA_YAW_DEGREES = {
    "profile_left": -90,
    "quarter_left": -45,
    "quarter_right": 45,
    "profile_right": 90,
    "front": 0,
}
# Keep camera degrees of freedom separate.  The dx8152 model card lists
# translation, yaw rotation, viewpoint, and lens changes as independent
# commands; composing them in one "pitch" phrase made results ambiguous.
CAMERA_TRANSLATION_PROMPTS = {
    "none": "",
    "forward": "将镜头向前移动。",
    "left": "将镜头向左移动。",
    "right": "将镜头向右移动。",
    "up": "将镜头向上移动。",
    "down": "将镜头向下移动。",
}
PITCH_PROMPTS = {
    "high_angle": "将镜头转为俯视。",
    "level": "",
    "low_angle": "将镜头转为仰视。",
}
LENS_PROMPTS = {
    "none": "",
    "wide": "将镜头转为广角镜头。",
    "close_up": "将镜头转为特写镜头。",
}
CAMERA_PROMPT_SOURCE = "https://huggingface.co/dx8152/Qwen-Edit-2509-Multiple-angles"


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


def camera_prompt_components(axis: str, value: str) -> dict[str, str]:
    """Return exactly one camera-control command for a result."""
    commands = {"yaw": "", "pitch": "", "translation": "", "lens": ""}
    if axis == "yaw":
        commands["yaw"] = FRONT_PROMPT if value == "front" else YAW_PROMPTS[value]
    elif axis == "pitch":
        commands["pitch"] = PITCH_PROMPTS[value]
    elif axis == "translation":
        commands["translation"] = CAMERA_TRANSLATION_PROMPTS[value]
    elif axis == "lens":
        commands["lens"] = LENS_PROMPTS[value]
    else:
        raise ValueError(f"Unsupported camera axis: {axis}")
    return commands


def build_camera_prompt(axis: str, value: str) -> str:
    """Compose exactly one camera-control command."""
    return camera_prompt_components(axis, value)[axis]


def load_pipeline(angle_lora: Path, angle_lora_strength: float) -> tuple[QwenImageEditPlusPipeline, int]:
    transformer_path = Path(
        snapshot_download(TRANSFORMER_REPOSITORY, cache_dir=HF_HUB_CACHE, local_files_only=True)
    ) / TRANSFORMER_FILENAME
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(transformer_path)
    # Standard PEFT injection cannot target Nunchaku's AWQW4A16Linear blocks.
    # This loader merges rank-decomposed weights into Nunchaku low-rank slots.
    applied_modules = apply_lora(transformer, angle_lora, strength=angle_lora_strength)
    if applied_modules == 0:
        raise RuntimeError("The multiple-angle LoRA did not match any Nunchaku transformer modules")
    # Create the ping-pong offload buffers after the LoRA rank expansion.  The
    # manager clones its first transformer block, so doing this earlier locks
    # its buffers to the original rank-128 tensor shapes.
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        model_path,
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
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=tuple(CAMERA_YAW_DEGREES),
        default=tuple(CAMERA_YAW_DEGREES),
        help="Yaw targets to generate sequentially (default: all five).",
    )
    parser.add_argument(
        "--camera-views",
        nargs="+",
        choices=("high_angle", "level", "low_angle"),
        default=("high_angle", "level", "low_angle"),
        help="Pitch views to generate for every yaw (default: all three).",
    )
    parser.add_argument(
        "--axis",
        choices=("yaw", "pitch", "translation", "lens"),
        default="yaw",
        help="The single camera-control axis to apply (default: yaw).",
    )
    parser.add_argument(
        "--translation",
        choices=tuple(key for key in CAMERA_TRANSLATION_PROMPTS if key != "none"),
        default="forward",
        help="Translation value, used only with --axis translation.",
    )
    parser.add_argument(
        "--lens",
        choices=tuple(key for key in LENS_PROMPTS if key != "none"),
        default="wide",
        help="Lens value, used only with --axis lens.",
    )
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument(
        "--angle-lora-strength",
        type=float,
        default=1.0,
        help="Multiple-angle LoRA strength (default: 1.0).",
    )
    parser.add_argument("--run-label", default="dx8152-camera-angle-v1")
    parser.add_argument(
        "--reference-image",
        type=Path,
        default=DEFAULT_REFERENCE_IMAGE,
        help="Frontal image that owns the subject identity and rendering.",
    )
    parser.add_argument(
        "--subject-region",
        choices=("head", "torso"),
        default="torso",
        help="Subject framing represented by --reference-image; used in output filenames.",
    )
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if args.angle_lora_strength <= 0:
        raise ValueError("--angle-lora-strength must be positive")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    reference_image = args.reference_image
    if not reference_image.is_absolute():
        reference_image = ASSETS / reference_image
    if not reference_image.is_file():
        raise FileNotFoundError(reference_image)

    angle_lora_dir = Path(snapshot_download(ANGLE_LORA_REPO, cache_dir=HF_HUB_CACHE, local_files_only=True))
    angle_lora = angle_lora_dir / ANGLE_LORA_FILE
    if not angle_lora.is_file():
        raise FileNotFoundError(angle_lora)
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    pipeline, applied_modules = load_pipeline(angle_lora, args.angle_lora_strength)
    results = []
    if args.axis == "yaw":
        sequence_values = list(args.targets)
    elif args.axis == "pitch":
        sequence_values = list(args.camera_views)
    elif args.axis == "translation":
        sequence_values = [args.translation]
    else:
        sequence_values = [args.lens]
    for sequence_index, value in enumerate(sequence_values, start=1):
        prompt_components = camera_prompt_components(args.axis, value)
        # Keep yaw, pitch, translation, and lens experiments separate.  In a
        # yaw+pitch run, the multiple-angle LoRA rotated the entire frame
        # instead of producing a stable combined viewpoint, so compound
        # camera commands are intentionally unsupported in this generator.
        prompt = build_camera_prompt(args.axis, value)
        camera_suffix = f"{args.axis}-{value.replace('_', '-')}"
        stem = (
            f"p7-5-2-qwen-{args.subject_region}-{camera_suffix}-"
            f"{args.run_label}-seed-{args.seed}-steps-{args.steps}"
        )
        output = output_dir / f"{stem}.png"
        result_record = output_dir / f"{stem}-result.json"
        started = time.monotonic()
        image = pipeline(
            prompt=prompt,
            image=[load_image(str(reference_image)).convert("RGB")],
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
            "status": "generated",
            "experiment_id": "p7-5-2-qwen-camera-angle-2509",
            "model": MODEL_ID,
            "transformer": TRANSFORMER_ID,
            "angle_lora": {"repository": ANGLE_LORA_REPO, "weight": asset_record(angle_lora)},
            "runtime": runtime_record(),
            "inputs": [asset_record(reference_image)],
            "input_roles": ["reference_identity_and_illustration"],
            "openpose_used": False,
            "camera_transform_owner": "dx8152 multiple-angle LoRA",
            "camera_prompt_source": CAMERA_PROMPT_SOURCE,
            "angle_lora_applied_modules": applied_modules,
            "angle_lora_strength": args.angle_lora_strength,
            "axis": args.axis,
            "axis_value": value,
            "yaw_degrees": CAMERA_YAW_DEGREES[value] if args.axis == "yaw" else 0,
            "prompt_language": "chinese",
            "sequence": {
                "index": sequence_index,
                "total": len(sequence_values),
                "axis": args.axis,
                "values": sequence_values,
            },
            "seed": args.seed,
            "steps": args.steps,
            "size": list(SIZE),
            "true_cfg_scale": 4.0,
            "guidance_scale": 1.0,
            "negative_prompt": " ",
            "prompt": prompt,
            "prompt_components": prompt_components,
            "prompt_word_count": len(prompt.split()),
            "prompt_character_count": len(prompt),
            "output": asset_record(output),
            "elapsed_seconds": round(time.monotonic() - started, 2),
        }
        result_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        results.append({"output": str(output), "result_record": str(result_record)})
    print(json.dumps({"outputs": results}, ensure_ascii=False))


if __name__ == "__main__":
    main()

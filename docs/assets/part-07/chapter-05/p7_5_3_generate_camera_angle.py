#!/usr/bin/env python3
"""Create one P7-5.3 storyboard camera-angle variant with Qwen Image Edit.

The input is a completed scene PNG.  This program changes exactly one camera
axis per run: yaw *or* pitch.  Keeping axes separate makes the condition and
the resulting image comparable; combined yaw-plus-pitch prompts proved
ambiguous in the Multiple Angles LoRA experiment.
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


ASSETS = Path(__file__).resolve().parent
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = (
    "nunchaku-tech/nunchaku-qwen-image-edit-2509/lightning-251115/"
    "svdq-fp4_r128-qwen-image-edit-2509-lightning-8steps-251115.safetensors"
)
ANGLE_LORA_REPO = "dx8152/Qwen-Edit-2509-Multiple-angles"
ANGLE_LORA_FILE = "镜头转换.safetensors"
CAMERA_PROMPT_SOURCE = "https://huggingface.co/dx8152/Qwen-Edit-2509-Multiple-angles"
DEFAULT_REFERENCE = ASSETS / "p7-5-3-qwen-storyboard-scene-a-549191-seed-5420-steps-20.png"
DEFAULT_SIZE = 1024
SCHEDULER_CONFIG = {
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
    "front": "保持正面镜头。",
    "quarter_left": "将镜头向左旋转45度。",
    "quarter_right": "将镜头向右旋转45度。",
    "profile_left": "将镜头向左旋转90度。",
    "profile_right": "将镜头向右旋转90度。",
}
PITCH_PROMPTS = {
    "high_angle": "将镜头转为俯视。",
    "low_angle": "将镜头转为仰视。",
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
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def camera_prompt(axis: str, view: str) -> str:
    prompts = YAW_PROMPTS if axis == "yaw" else PITCH_PROMPTS
    return prompts[view]


def load_pipeline(angle_lora: Path) -> tuple[QwenImageEditPlusPipeline, int]:
    # The maintained adapter handles Nunchaku's AWQW4A16Linear modules.
    if "/tmp" not in sys.path:
        sys.path.insert(0, "/tmp")
    from nunchaku_lora_qwen import apply_lora

    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    applied_modules = apply_lora(transformer, angle_lora, strength=1.0)
    if not applied_modules:
        raise RuntimeError("Multiple Angles LoRA did not match the Nunchaku transformer")
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        transformer=transformer,
        scheduler=FlowMatchEulerDiscreteScheduler.from_config(SCHEDULER_CONFIG),
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline, applied_modules


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE, help="Stage 1 scene PNG.")
    parser.add_argument("--axis", choices=("yaw", "pitch"), required=True, help="One camera axis only.")
    parser.add_argument("--view", required=True, help="Yaw: front/quarter_left/quarter_right/profile_left/profile_right; pitch: high_angle/low_angle.")
    parser.add_argument("--seed", type=int, default=5420)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    allowed_views = YAW_PROMPTS if args.axis == "yaw" else PITCH_PROMPTS
    if args.view not in allowed_views:
        parser.error(f"--view must be one of: {', '.join(allowed_views)}")
    if args.steps < 1 or args.size < 256 or args.size % 16:
        parser.error("--steps must be positive and --size must be at least 256 and divisible by 16")
    reference = args.reference.resolve()
    if not reference.is_file():
        raise FileNotFoundError(reference)
    stem = f"p7-5-3-qwen-camera-{args.axis}-{args.view.replace('_', '-')}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output_dir = args.output_dir.resolve()
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    prompt = camera_prompt(args.axis, args.view)
    if args.dry_run:
        print(json.dumps({"input": str(reference), "prompt": prompt, "output": str(output), "result": str(result)}, ensure_ascii=False))
        return
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    angle_lora_dir = Path(snapshot_download(ANGLE_LORA_REPO, local_files_only=True))
    angle_lora = angle_lora_dir / ANGLE_LORA_FILE
    if not angle_lora.is_file():
        raise FileNotFoundError(angle_lora)
    output_dir.mkdir(parents=True, exist_ok=True)
    pipeline, applied_modules = load_pipeline(angle_lora)
    try:
        started = time.monotonic()
        image = pipeline(
            prompt=prompt,
            image=[load_image(str(reference)).convert("RGB")],
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=4.0,
            guidance_scale=1.0,
            negative_prompt=" ",
            num_inference_steps=args.steps,
            width=args.size,
            height=args.size,
        ).images[0]
        image.save(output)
        result.write_text(
            json.dumps(
                {
                    "status": "generated",
                    "experiment_id": "p7-5-3-qwen-camera-angle",
                    "stage": "camera_angle",
                    "model": MODEL_ID,
                    "transformer": TRANSFORMER_ID,
                    "angle_lora": {"repository": ANGLE_LORA_REPO, "weight": asset_record(angle_lora), "applied_modules": applied_modules},
                    "camera_prompt_source": CAMERA_PROMPT_SOURCE,
                    "input": asset_record(reference),
                    "input_role": "stage_1_scene",
                    "axis": args.axis,
                    "view": args.view,
                    "prompt_language": "chinese",
                    "prompt": prompt,
                    "seed": args.seed,
                    "steps": args.steps,
                    "size": [args.size, args.size],
                    "true_cfg_scale": 4.0,
                    "guidance_scale": 1.0,
                    "output": asset_record(output),
                    "next_input_role": "stage_3_camera_angle_reference",
                    "runtime": runtime_record(),
                    "elapsed_seconds": round(time.monotonic() - started, 2),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))
    finally:
        del pipeline
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

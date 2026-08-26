#!/usr/bin/env python3
"""Generate a Qwen RGB storyboard and its relative-depth guide for P7-5.3."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import secrets
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import torch
from diffusers import FlowMatchEulerDiscreteScheduler, QwenImageEditPlusPipeline, QwenImagePipeline
from diffusers.utils import load_image
from huggingface_hub import snapshot_download
from nunchaku import NunchakuQwenImageTransformer2DModel
from PIL import Image


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
DEPTH_ANYTHING_MODEL = PROJECT_ROOT / ".tmp/p7-5-3-depth-anything-v2-small"
MODEL_ID = "Qwen/Qwen-Image"
TRANSFORMER_ID = "/home/cbsim/.cache/huggingface/hub/models--nunchaku-tech--nunchaku-qwen-image/snapshots/4d9f4f667ea571ab172e0ee29ac2c27b82a41a6b/svdq-fp4_r128-qwen-image.safetensors"
EDIT_MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
EDIT_TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/lightning-251115/svdq-fp4_r128-qwen-image-edit-2509-lightning-8steps-251115.safetensors"
ANGLE_LORA_REPO = "dx8152/Qwen-Edit-2509-Multiple-angles"
ANGLE_LORA_FILE = "镜头转换.safetensors"


@dataclass(frozen=True)
class Defaults:
    steps: int = 20
    width: int = 1024
    height: int = 1024


DEFAULTS = Defaults()
ILLUSTRATION_PROMPT = "Illustrated character scene with clean charcoal contours and transparent watercolor color blocks."
DEFAULT_POSE_DESCRIPTION = (
    "One full-body adult woman is airborne in a natural forward jump: upright torso, one knee lifted forward, "
    "the other leg extended back, and both arms open naturally for balance."
)
SCENES = {
    "A": {
        "seed": 5420,
        "description": "해안 절벽 산책로 야외 장면",
        "backdrop": "Outdoor coastal cliffside path with rugged dark rocks, a distant blue ocean horizon, wind-blown grass, and clear open sky.",
    },
    "B": {
        "seed": 5421,
        "description": "야생화 초원 야외 장면",
        "backdrop": "Outdoor wildflower meadow with tall grass, scattered yellow flowers, a distant low mountain ridge, and broad open daylight sky.",
    },
    "C": {
        "seed": 5422,
        "description": "도심 공원 야외 장면",
        "backdrop": "Outdoor tree-lined city park plaza with pale stone paving, broadleaf trees, soft afternoon light, and a distant contemporary sculpture.",
    },
}
PITCH_VIEWS = {"high_angle": "保持场景和人物不变，将镜头转为俯视。", "low_angle": "保持场景和人物不变，将镜头转为仰视。"}
YAW_VIEWS = {"front": "保持场景和人物不变，保持正面镜头。", "quarter_left": "保持场景和人物不变，将镜头向左旋转45度。", "quarter_right": "保持场景和人物不变，将镜头向右旋转45度。"}
# Official Multiple Angles LoRA wording for a wide-angle lens.
# Camera axes are deliberately separate image-edit stages.  Never combine pitch
# and yaw in one prompt; the yaw stage receives the pitch PNG as its input.
SCENE_CAMERA_PLAN = {
    "A": {"pitch": "low_angle", "yaw": "front", "seed": 5420},
    "B": {"pitch": "high_angle", "yaw": "quarter_left", "seed": 5421},
    "C": {"pitch": "low_angle", "yaw": "quarter_right", "seed": 5422},
}
SCHEDULER_CONFIG = {"base_image_seq_len": 256, "base_shift": 1.0986122886681098, "invert_sigmas": False, "max_image_seq_len": 8192, "max_shift": 1.0986122886681098, "num_train_timesteps": 1000, "shift": 1.0, "shift_terminal": None, "stochastic_sampling": False, "time_shift_type": "exponential", "use_beta_sigmas": False, "use_dynamic_shifting": True, "use_exponential_sigmas": False, "use_karras_sigmas": False}


def scene_prompt(scene_id: str, pose_description: str) -> str:
    return f"{SCENES[scene_id]['backdrop']} {pose_description} Short bob haircut, dark sleeveless leotard and tights."


def asset_record(path: Path) -> dict[str, str]:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"path": str(path), "sha256": digest}


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
    pipeline = QwenImagePipeline.from_pretrained(
        MODEL_ID, transformer=transformer, torch_dtype=torch.bfloat16, local_files_only=True
    )
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline


def load_camera_pipeline() -> tuple[QwenImageEditPlusPipeline, Path, int]:
    """Load the Qwen Edit camera LoRA only for pitch/yaw stages."""
    if "/tmp" not in sys.path:
        sys.path.insert(0, "/tmp")
    from nunchaku_lora_qwen import apply_lora

    lora_dir = Path(snapshot_download(ANGLE_LORA_REPO, local_files_only=True))
    lora_path = lora_dir / ANGLE_LORA_FILE
    if not lora_path.is_file():
        raise FileNotFoundError(lora_path)
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(EDIT_TRANSFORMER_ID)
    applied_modules = apply_lora(transformer, lora_path, strength=1.0)
    if not applied_modules:
        raise RuntimeError("multiple-angle LoRA did not match the Qwen Edit transformer")
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        EDIT_MODEL_ID,
        transformer=transformer,
        scheduler=FlowMatchEulerDiscreteScheduler.from_config(SCHEDULER_CONFIG),
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline, lora_path, applied_modules


def relative_depth(image: Image.Image) -> Image.Image:
    """Estimate relative depth; do not substitute a synthetic guide if this fails."""
    from transformers import AutoImageProcessor, AutoModelForDepthEstimation

    if not DEPTH_ANYTHING_MODEL.is_dir():
        raise FileNotFoundError(f"Depth Anything V2 Small is missing: {DEPTH_ANYTHING_MODEL}")
    processor = AutoImageProcessor.from_pretrained(DEPTH_ANYTHING_MODEL, local_files_only=True, use_fast=False)
    model = AutoModelForDepthEstimation.from_pretrained(
        DEPTH_ANYTHING_MODEL, local_files_only=True, dtype=torch.float16
    ).to("cuda").eval()
    inputs = {name: value.to("cuda") for name, value in processor(images=image, return_tensors="pt").items()}
    with torch.inference_mode():
        depth = model(**inputs).predicted_depth
    depth = torch.nn.functional.interpolate(depth.unsqueeze(1), size=(image.height, image.width), mode="bicubic", align_corners=False)
    values = depth.squeeze().float().cpu()
    minimum, maximum = values.min(), values.max()
    if maximum <= minimum:
        raise RuntimeError("depth estimator returned a constant map")
    normalized = ((values - minimum) / (maximum - minimum) * 255).to(torch.uint8).numpy()
    del model
    torch.cuda.empty_cache()
    return Image.fromarray(normalized).convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("scene", "pitch", "yaw"), default="scene", help="scene makes RGB/depth; pitch and yaw edit one input PNG.")
    parser.add_argument("--scene", choices=tuple(SCENES), help="Scene ID. Required for every stage.")
    parser.add_argument("--scenes", nargs="+", choices=tuple(SCENES), help="Generate independent Stage 1 scenes sequentially.")
    parser.add_argument("--reference", type=Path, help="Stage 2/3 input PNG. Pitch receives Stage 1; yaw receives Stage 2.")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--runs", type=int, default=1)
    parser.add_argument("--pose-description", default=DEFAULT_POSE_DESCRIPTION, help="Character pose, independent from scene background and camera.")
    parser.add_argument("--illustration", action="store_true", help="Add the concise illustration rendering contract to a Stage 1 scene.")
    parser.add_argument("--steps", type=int, help="Default: 20 for Stage 1, 8 for pitch/yaw camera edits.")
    parser.add_argument("--size", type=int, default=DEFAULTS.width)
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.steps is None:
        args.steps = DEFAULTS.steps if args.stage == "scene" else 8
    if args.stage == "scene" and bool(args.scene) == bool(args.scenes):
        parser.error("Stage 1 requires exactly one of --scene or --scenes")
    if args.stage != "scene" and (not args.scene or args.scenes or not args.reference):
        parser.error("pitch/yaw requires --scene and --reference; --scenes is Stage 1 only")
    if args.runs < 1 or args.steps < 1:
        parser.error("--runs and --steps must be at least 1")
    if args.size < 256 or args.size % 16:
        parser.error("--size must be at least 256 and divisible by 16")
    if not torch.cuda.is_available() and not args.dry_run:
        raise RuntimeError("CUDA is required")

    if args.scenes:
        for scene_id in args.scenes:
            command = [sys.executable, str(Path(__file__).resolve()), "--stage", "scene", "--scene", scene_id, "--runs", str(args.runs), "--steps", str(args.steps), "--size", str(args.size), "--output-dir", str(args.output_dir), "--pose-description", args.pose_description]
            if args.illustration:
                command.append("--illustration")
            if args.seed is not None:
                command.extend(("--seed", str(args.seed)))
            if args.dry_run:
                command.append("--dry-run")
            subprocess.run(command, check=True)
        return

    if args.stage != "scene":
        reference = args.reference.resolve()
        if not reference.is_file():
            raise FileNotFoundError(reference)
        plan = SCENE_CAMERA_PLAN[args.scene]
        view = plan[args.stage]
        seed = args.seed if args.seed is not None else plan["seed"]
        stem = f"p7-5-3-qwen-storyboard-{args.stage}_{view}-{args.stage}-scene-{args.scene.lower()}-seed-{seed}-steps-{args.steps}"
        if args.dry_run:
            print(json.dumps({"output": f"{stem}.png", "result": f"{stem}-result.json"}))
            return
        args.output_dir.mkdir(parents=True, exist_ok=True)
        pipeline, lora_path, applied_modules = load_camera_pipeline()
        try:
            started = time.monotonic()
            prompt = (PITCH_VIEWS if args.stage == "pitch" else YAW_VIEWS)[view]
            output = args.output_dir / f"{stem}.png"
            result_path = args.output_dir / f"{stem}-result.json"
            image = pipeline(
                prompt=prompt,
                image=[load_image(str(reference)).convert("RGB")],
                generator=torch.Generator("cpu").manual_seed(seed),
                true_cfg_scale=4.0,
                guidance_scale=1.0,
                negative_prompt=" ",
                num_inference_steps=args.steps,
                width=args.size,
                height=args.size,
            ).images[0]
            image.save(output)
            result_path.write_text(
                json.dumps(
                    {
                        "status": "generated",
                        "experiment_id": "p7-5-3-qwen-storyboard",
                        "model": EDIT_MODEL_ID,
                        "transformer": EDIT_TRANSFORMER_ID,
                        "angle_lora": {"repository": ANGLE_LORA_REPO, "weight": asset_record(lora_path), "applied_modules": applied_modules},
                        "inputs": [asset_record(reference)],
                        "input_roles": [f"stage_{'1' if args.stage == 'pitch' else '2'}_reference"],
                        "scene_id": args.scene,
                        "stage": args.stage,
                        "axis": args.stage,
                        "view": view,
                        "seed": seed,
                        "steps": args.steps,
                        "size": [args.size, args.size],
                        "true_cfg_scale": 4.0,
                        "guidance_scale": 1.0,
                        "prompt_language": "chinese",
                        "prompt": prompt,
                        "output": asset_record(output),
                        "elapsed_seconds": round(time.monotonic() - started, 2),
                    },
                    ensure_ascii=False,
                    indent=2,
                ) + "\n",
                encoding="utf-8",
            )
            print(json.dumps({"output": str(output), "result": str(result_path)}, ensure_ascii=False))
        finally:
            del pipeline
            torch.cuda.empty_cache()
        return

    scene = SCENES[args.scene]
    start_seed = args.seed if args.seed is not None else scene["seed"]
    prompt = scene_prompt(args.scene, args.pose_description)
    if args.illustration:
        prompt = f"{prompt} {ILLUSTRATION_PROMPT}"
    execution_code = f"{secrets.randbelow(1_000_000):06d}"
    stems = [f"p7-5-3-qwen-storyboard-scene-{args.scene.lower()}-{execution_code}-seed-{start_seed + index}-steps-{args.steps}" for index in range(args.runs)]
    if args.dry_run:
        for stem in stems:
            print(json.dumps({"rgb": f"{stem}.png", "depth": f"{stem}-depth.png", "result": f"{stem}-result.json"}))
        return

    args.output_dir.mkdir(parents=True, exist_ok=True)
    pipeline = load_pipeline()
    try:
        for index, stem in enumerate(stems):
            seed = start_seed + index
            started = time.monotonic()
            rgb = pipeline(
                prompt=prompt,
                generator=torch.Generator("cpu").manual_seed(seed),
                true_cfg_scale=4.0,
                guidance_scale=1.0,
                negative_prompt="text, panel, collage, extra person",
                num_inference_steps=args.steps,
                width=args.size,
                height=args.size,
            ).images[0]
            rgb_path = args.output_dir / f"{stem}.png"
            depth_path = args.output_dir / f"{stem}-depth.png"
            result_path = args.output_dir / f"{stem}-result.json"
            rgb.save(rgb_path)
            try:
                relative_depth(rgb).save(depth_path)
            except Exception:
                rgb_path.unlink(missing_ok=True)
                raise
            result_path.write_text(
                json.dumps(
                    {
                        "status": "generated",
                        "experiment_id": "p7-5-3-qwen-storyboard",
                        "model": MODEL_ID,
                        "transformer": TRANSFORMER_ID,
                        "runtime": runtime_record(),
                        "scene_id": args.scene,
                        "scene_description": scene["description"],
                        "pose_description": args.pose_description,
                        "seed": seed,
                        "steps": args.steps,
                        "size": [args.size, args.size],
                        "true_cfg_scale": 4.0,
                        "guidance_scale": 1.0,
                        "prompt": prompt,
                        "prompt_word_count": len(prompt.split()),
                        "outputs": {"rgb": asset_record(rgb_path), "relative_depth": asset_record(depth_path)},
                        "elapsed_seconds": round(time.monotonic() - started, 2),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            print(json.dumps({"rgb": str(rgb_path), "depth": str(depth_path), "result": str(result_path)}, ensure_ascii=False))
    finally:
        del pipeline
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

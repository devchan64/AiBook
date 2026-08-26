#!/usr/bin/env python3
"""Use Qwen Edit to combine one P7-5.3 structure guide with character references."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path

import torch
from diffusers import QwenImageEditPlusPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
DEFAULT_OUTFIT = ASSETS / "p7-5-2-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30.png"
DEFAULT_TORSO = ASSETS / "p7-5-7-qwen-torso-yaw-front-cfg4-front-1024-v4-seed-62294-steps-8.png"
DEFAULT_STYLE_CONTRACT = ASSETS / "p7-5-1-style-prompt-contract.json"
DEFAULT_CHARACTER_FEATURES = ASSETS / "p7-5-3-character-features.json"


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


def load_pipeline() -> QwenImageEditPlusPipeline:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, transformer=transformer, torch_dtype=torch.bfloat16, local_files_only=True
    )
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage",
        choices=(
            "storyboard_a",
            "background_plate",
            "character_plate",
            "rgb_character",
            "rgb_character_detail",
            "outfit",
            "outfit_detail",
            "face",
            "shoes",
            "style",
        ),
        default="outfit",
    )
    parser.add_argument("--guide", type=Path, help="Unmodified relative-depth guide for the first outfit stage")
    parser.add_argument("--reference", type=Path, help="The immediately preceding stage PNG")
    parser.add_argument("--detail-references", type=Path, nargs="+", help="One or two rotated outfit-detail reference PNGs")
    parser.add_argument("--guide-type", choices=("rgb", "depth"), default="depth")
    parser.add_argument("--outfit", type=Path, default=DEFAULT_OUTFIT)
    parser.add_argument("--torso", type=Path, default=DEFAULT_TORSO)
    parser.add_argument(
        "--character-features",
        type=Path,
        default=DEFAULT_CHARACTER_FEATURES,
        help="Stage-1 character identity prompt JSON",
    )
    parser.add_argument("--style-contract", type=Path, default=DEFAULT_STYLE_CONTRACT, help="Stage 2 character-scene style JSON")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1024)
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("--steps must be at least 1")
    if args.size < 256 or args.size % 16:
        parser.error("--size must be at least 256 and divisible by 16")
    if args.stage in ("rgb_character", "outfit") and not args.guide:
        parser.error("rgb_character and outfit stages require --guide")
    if args.stage not in ("rgb_character", "outfit") and not args.reference:
        parser.error("this stage requires --reference")
    if args.stage == "rgb_character_detail" and not args.detail_references:
        parser.error("rgb_character_detail requires --detail-references")
    if args.detail_references and len(args.detail_references) > 2:
        parser.error("at most two --detail-references are supported with the current image")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    if args.stage == "storyboard_a":
        character = args.reference.resolve()
        character_features = args.character_features.resolve()
        for path in (character, character_features):
            if not path.is_file():
                raise FileNotFoundError(path)
        character_features_data = json.loads(character_features.read_text(encoding="utf-8"))
        character_features_prompt = character_features_data["stage1_character_features"]
        outfit_features_prompt = character_features_data["stage1_outfit_features"]
        pose_description = character_features_data["stage1_pose_description"]
        input_paths = (character,)
        input_roles = ["character reference: full-body plus-90-degree outfit view"]
        prompt = (
            "Image 1 woman airborne on an outdoor coastal cliffside path with rugged dark rocks, "
            "a distant blue ocean horizon, wind-blown grass, and clear open sky. "
            f"{pose_description} "
            f"{character_features_prompt} "
            f"{outfit_features_prompt} "
            "Illustrated character scene with clean charcoal contours and transparent watercolor color blocks."
        )
        character_features_record = asset_record(character_features)
        style_record = None
        stem = f"p7-5-3-qwen-storyboard-scene-a-character-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    elif args.stage == "background_plate":
        reference = args.reference.resolve()
        if not reference.is_file():
            raise FileNotFoundError(reference)
        input_paths = (reference,)
        input_roles = ["stage-1 storyboard: background source"]
        prompt = "Remove the person from Image 1."
        character_features_record = None
        style_record = None
        stem = f"p7-5-3-qwen-storyboard-background-plate-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    elif args.stage == "character_plate":
        reference = args.reference.resolve()
        if not reference.is_file():
            raise FileNotFoundError(reference)
        input_paths = (reference,)
        input_roles = ["stage-1 storyboard: character source"]
        prompt = "The full-body airborne woman from Image 1 isolated on a plain warm off-white background."
        character_features_record = None
        style_record = None
        stem = f"p7-5-3-qwen-storyboard-character-plate-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    elif args.stage == "rgb_character":
        rgb, outfit = (path.resolve() for path in (args.guide, args.outfit))
        for path in (rgb, outfit):
            if not path.is_file():
                raise FileNotFoundError(path)
        input_paths = (rgb, outfit)
        input_roles = [
            "original RGB storyboard: scene, camera, and jumping pose",
            "character outfit stage 2 reference",
        ]
        prompt = "The woman in Image 1 is the character in Image 2."
        character_features_record = None
        style_record = None
        stem = f"p7-5-3-qwen-scene-rgb-character-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    elif args.stage == "rgb_character_detail":
        current = args.reference.resolve()
        details = tuple(path.resolve() for path in args.detail_references)
        input_paths = (current, *details)
        for path in input_paths:
            if not path.is_file():
                raise FileNotFoundError(path)
        input_roles = ["current RGB character storyboard"] + ["rotated outfit-detail reference"] * len(details)
        references = " and ".join(f"Image {index}" for index in range(2, len(input_paths) + 1))
        prompt = f"The woman in Image 1 has the outfit details of {references}."
        character_features_record = None
        style_record = None
        stem = f"p7-5-3-qwen-scene-rgb-character-detail-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    elif args.stage == "outfit":
        guide, outfit = (path.resolve() for path in (args.guide, args.outfit))
        # Qwen Edit gives the first image stronger identity preservation.  Keep
        # the complete outfit first; use the depth map only to steer pose/camera.
        input_paths = (outfit, guide)
        for path in input_paths:
            if not path.is_file():
                raise FileNotFoundError(path)
        structure_role = "camera, framing, pose, and relative depth" if args.guide_type == "depth" else "camera, framing, pose, background, lighting, and shadows"
        input_roles = ["full-body outfit and proportions", structure_role]
        prompt = "Image 1: white cropped jacket with a folded collar, gray crop top, teal wide-leg trousers, white sneakers. Image 2: jumping pose, camera, background. One woman wears the Image 1 outfit."
        character_features_record = None
        style_record = None
        stem = f"p7-5-3-qwen-scene-outfit-{args.guide_type}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    elif args.stage == "outfit_detail":
        reference, outfit = (path.resolve() for path in (args.reference, args.outfit))
        input_paths = (reference, outfit)
        for path in input_paths:
            if not path.is_file():
                raise FileNotFoundError(path)
        input_roles = ["first outfit-stage image", "outfit detail reference"]
        prompt = "Image 1 unchanged. Image 2: white cropped jacket, folded collar, gray crop top, teal wide-leg trousers, white sneakers."
        character_features_record = None
        style_record = None
        stem = f"p7-5-3-qwen-scene-outfit-detail-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    elif args.stage == "face":
        reference, torso = (path.resolve() for path in (args.reference, args.torso))
        input_paths = (reference, torso)
        for path in input_paths:
            if not path.is_file():
                raise FileNotFoundError(path)
        input_roles = ["storyboard image: composition and airborne character scale", "profile face and hairstyle reference"]
        prompt = "The small airborne woman in Image 1 keeps the scene composition and scale; her face and hair use Image 2 facial identity and hairstyle."
        character_features_record = None
        style_record = None
        stem = f"p7-5-3-qwen-scene-face-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    elif args.stage == "shoes":
        reference, outfit = (path.resolve() for path in (args.reference, args.outfit))
        input_paths = (reference, outfit)
        for path in input_paths:
            if not path.is_file():
                raise FileNotFoundError(path)
        input_roles = ["face-stage image", "outfit shoe reference"]
        prompt = "Image 1 unchanged. Image 2: white sneakers only."
        character_features_record = None
        style_record = None
        stem = f"p7-5-3-qwen-scene-shoes-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    else:
        reference, style_contract = (path.resolve() for path in (args.reference, args.style_contract))
        for path in (reference, style_contract):
            if not path.is_file():
                raise FileNotFoundError(path)
        style_prompt = json.loads(style_contract.read_text(encoding="utf-8"))["character_scene_style_prompt"]
        input_paths = (reference,)
        input_roles = ["character-stage composition, face, outfit, and background"]
        prompt = f"Image 1 unchanged except rendering. {style_prompt}"
        character_features_record = None
        style_record = asset_record(style_contract)
        stem = f"p7-5-3-qwen-scene-style-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / f"{stem}.png"
    result_path = args.output_dir / f"{stem}-result.json"
    started = time.monotonic()
    pipeline = load_pipeline()
    try:
        image = pipeline(
            image=[load_image(str(path)).convert("RGB") for path in input_paths],
            prompt=prompt,
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=4.0,
            guidance_scale=1.0,
            negative_prompt="text, panel, collage, extra person",
            num_inference_steps=args.steps,
            width=args.size,
            height=args.size,
        ).images[0]
        image.save(output)
        result_path.write_text(
            json.dumps(
                {
                    "status": "generated",
                    "experiment_id": f"p7-5-3-qwen-scene-{args.stage}",
                    "model": MODEL_ID,
                    "transformer": TRANSFORMER_ID,
                    "runtime": runtime_record(),
                    "inputs": [asset_record(path) for path in input_paths],
                    "input_roles": input_roles,
                    "stage": args.stage,
                    "plate_type": (
                        "background_without_character"
                        if args.stage == "background_plate"
                        else "character_on_plain_background"
                        if args.stage == "character_plate"
                        else None
                    ),
                    "character_features_contract": character_features_record,
                    "character_features_key": "stage1_character_features" if args.stage == "storyboard_a" else None,
                    "outfit_features_key": "stage1_outfit_features" if args.stage == "storyboard_a" else None,
                    "pose_description_key": "stage1_pose_description" if args.stage == "storyboard_a" else None,
                    "style_prompt_contract": style_record,
                    "style_prompt_key": "character_scene_style_prompt" if style_record else None,
                    "guide_type": args.guide_type if args.stage == "outfit" else None,
                    "seed": args.seed,
                    "steps": args.steps,
                    "size": [args.size, args.size],
                    "true_cfg_scale": 4.0,
                    "guidance_scale": 1.0,
                    "negative_prompt": "text, panel, collage, extra person",
                    "prompt": prompt,
                    "prompt_word_count": len(prompt.split()),
                    "output": asset_record(output),
                    "elapsed_seconds": round(time.monotonic() - started, 2),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(json.dumps({"output": str(output), "result": str(result_path)}, ensure_ascii=False))
    finally:
        del pipeline
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

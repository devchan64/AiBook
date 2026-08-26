#!/usr/bin/env python3
"""Generate P7-5.2 full-body references from selected outfit, torso, and OpenPose inputs."""

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
HEADLESS_OUTFIT_REFERENCES = {
    "yaw_front": "p7-5-2-qwen-edit-prompt-style-outfit_stage3_faceless_bald-faceless-bald-v1-seed-62294-steps-20.png",
    "yaw_minus_45": "p7-5-2-qwen-faceless-bald-outfit-yaw_minus_45-yaw-v1-seed-62294-steps-8.png",
    "yaw_minus_90": "p7-5-2-qwen-faceless-bald-outfit-yaw_minus_90-yaw-v1-seed-62294-steps-8.png",
    "yaw_plus_45": "p7-5-2-qwen-faceless-bald-outfit-yaw_plus_45-yaw-v1-seed-62294-steps-8.png",
    "yaw_plus_90": "p7-5-2-qwen-faceless-bald-outfit-yaw_plus_90-yaw-v1-seed-62294-steps-8.png",
}
BACKGROUND_DESCRIPTION = "Plain cool-gray background."
DEFAULT_SIZE = (1024, 1536)
DEFAULT_STEPS = 30
YAW_DEGREES = {
    "yaw_front": 0,
    "yaw_minus_45": -45,
    "yaw_minus_90": -90,
    "yaw_plus_45": 45,
    "yaw_plus_90": 90,
}
TORSO_REFERENCES = {
    "yaw_front": "p7-5-7-qwen-torso-yaw-front-cfg4-front-1024-v4-seed-62294-steps-8.png",
    "yaw_minus_45": "p7-5-7-qwen-torso-yaw-quarter-left-cfg4-yaw-1024-v4-seed-62294-steps-8.png",
    "yaw_minus_90": "p7-5-7-qwen-torso-yaw-profile-left-cfg4-yaw-1024-v4-seed-62294-steps-8.png",
    "yaw_plus_45": "p7-5-7-qwen-torso-yaw-quarter-right-cfg4-yaw-1024-v4-seed-62294-steps-8.png",
    "yaw_plus_90": "p7-5-7-qwen-torso-yaw-profile-right-cfg4-yaw-1024-v4-seed-62294-steps-8.png",
}
OPENPOSE_REFERENCES = {
    "yaw_front": "p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw+00_pitch+00.png",
    # The relation-map projection uses the inverse screen direction of the
    # 5.7 camera yaw.  Pair each torso with its screen-direction match.
    "yaw_minus_45": "p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw+45_pitch+00.png",
    "yaw_minus_90": "p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw+90_pitch+00.png",
    "yaw_plus_45": "p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw-45_pitch+00.png",
    "yaw_plus_90": "p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw-90_pitch+00.png",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def asset_record(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": sha256(path)}


def parse_size(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", maxsplit=1)
        width, height = int(width_text), int(height_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("--size must be WIDTHxHEIGHT") from error
    if width < 16 or height < 16 or width % 16 or height % 16:
        raise argparse.ArgumentTypeError("--size values must be positive multiples of 16")
    return width, height


def runtime_record() -> dict[str, object]:
    packages = {}
    for package in ("nunchaku", "diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": packages,
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
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    return pipeline


def target_spec(target: str, input_order: str) -> tuple[tuple[str, ...], list[str], str]:
    direction = {
        "yaw_front": "facing forward",
        "yaw_minus_45": "facing three-quarter right",
        "yaw_minus_90": "facing right",
        "yaw_plus_45": "facing three-quarter left, front torso visible",
        "yaw_plus_90": "facing left",
    }[target]
    if input_order == "openpose_outfit_torso":
        return (
            (OPENPOSE_REFERENCES[target], HEADLESS_OUTFIT_REFERENCES[target], TORSO_REFERENCES[target]),
            ["matched_yaw_fullbody_openpose", "matched_yaw_headless_outfit", "matched_yaw_torso_face_hair_style"],
            f"Full-body woman {direction}. Image 1 pose. Image 2 outfit. Image 3 face, hair, and style.",
        )
    if input_order == "openpose_torso_outfit":
        return (
            (OPENPOSE_REFERENCES[target], TORSO_REFERENCES[target], HEADLESS_OUTFIT_REFERENCES[target]),
            ["matched_yaw_fullbody_openpose", "matched_yaw_torso_face_hair_style", "matched_yaw_headless_outfit"],
            f"Full-body woman {direction}. Image 1 pose. Image 2 face, hair, and style. Image 3 outfit.",
        )
    if input_order == "torso_outfit":
        return (
            (TORSO_REFERENCES[target], HEADLESS_OUTFIT_REFERENCES[target]),
            ["matched_yaw_torso_face_hair_style", "matched_yaw_faceless_bald_outfit"],
            f"Full-body woman {direction}. Image 1 face, hair, and style. Image 2 outfit, hands, shoes, and body proportions.",
        )
    if input_order == "outfit_torso":
        return (
            (HEADLESS_OUTFIT_REFERENCES[target], TORSO_REFERENCES[target]),
            ["matched_yaw_faceless_bald_outfit", "matched_yaw_torso_face_hair_style"],
            f"Full-body woman {direction}. Image 1 outfit, hands, shoes, and body proportions. Image 2 face, hair, and style.",
        )
    return (
        (TORSO_REFERENCES[target], OPENPOSE_REFERENCES[target], HEADLESS_OUTFIT_REFERENCES[target]),
        ["matched_yaw_torso_face_hair_style", "matched_yaw_fullbody_openpose", "matched_yaw_headless_outfit"],
        f"Full-body woman {direction}. Image 1 face, hair, and style. Image 2 pose. Image 3 outfit.",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", nargs="+", choices=tuple(YAW_DEGREES), default=("yaw_front",))
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--size", type=parse_size, default=DEFAULT_SIZE)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--run-label", default="matched-torso-face-refine-v1")
    parser.add_argument(
        "--input-order",
        choices=("openpose_outfit_torso", "openpose_torso_outfit", "torso_openpose_outfit", "torso_outfit", "outfit_torso"),
        default="openpose_outfit_torso",
    )
    parser.add_argument(
        "--openpose-reference",
        type=Path,
        help="Override the OpenPose input for a one-off comparison run.",
    )
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    pipeline = load_pipeline()
    outputs = []
    for index, target in enumerate(args.targets, start=1):
        input_names, input_roles, prompt = target_spec(target, args.input_order)
        inputs = [ASSETS / name for name in input_names]
        if args.openpose_reference:
            if "matched_yaw_fullbody_openpose" not in input_roles:
                raise ValueError("--openpose-reference requires an input order with OpenPose")
            override = args.openpose_reference
            if not override.is_absolute():
                override = ASSETS / override
            inputs[input_roles.index("matched_yaw_fullbody_openpose")] = override
        if missing := [str(path) for path in inputs if not path.is_file()]:
            raise FileNotFoundError("missing input asset(s): " + ", ".join(missing))
        stem = f"p7-5-2-qwen-fullbody-reference-{target}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
        output = output_dir / f"{stem}.png"
        result_path = output_dir / f"{stem}-result.json"
        started = time.monotonic()
        image = pipeline(
            prompt=prompt,
            image=[load_image(str(path)).convert("RGB") for path in inputs],
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=4.0,
            guidance_scale=1.0,
            negative_prompt=" ",
            num_inference_steps=args.steps,
            width=args.size[0],
            height=args.size[1],
        ).images[0]
        image.save(output)
        record = {
            "status": "generated",
            "experiment_id": "p7-5-2-qwen-fullbody-reference-refine",
            "model": MODEL_ID,
            "transformer": TRANSFORMER_ID,
            "runtime": runtime_record(),
            "target": target,
            "yaw_degrees": YAW_DEGREES[target],
            "inputs": [asset_record(path) for path in inputs],
            "input_roles": input_roles,
            "background_description": BACKGROUND_DESCRIPTION,
            "seed": args.seed,
            "steps": args.steps,
            "size": list(args.size),
            "true_cfg_scale": 4.0,
            "negative_prompt": " ",
            "prompt": prompt,
            "output": asset_record(output),
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "sequence": {"index": index, "total": len(args.targets), "targets": args.targets},
        }
        result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        outputs.append({"output": str(output), "result_record": str(result_path)})
    print(json.dumps({"outputs": outputs}, ensure_ascii=False))


if __name__ == "__main__":
    main()

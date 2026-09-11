#!/usr/bin/env python3
"""Generate the three front-facing outfit construction stages for P7-5.3."""

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
from huggingface_hub import snapshot_download
from diffusers.utils import load_image


ASSETS = Path(__file__).resolve().parent
HF_HUB_CACHE = ASSETS.parents[3] / ".tmp" / "download" / "huggingface" / "hub"
IDENTITY_CONTRACT = ASSETS / "p7-5-2-mira-identity-contract.json"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
OUTPUT_DIR = ASSETS
DEFAULT_STEPS = 10
QWEN_FACE_REFERENCE = "p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png"
SHOE_REFERENCE = "p7-5-3-qwen-image-2512-white-sneakers-v1-size-1280x1280-seed-62294-steps-10.png"
# 960×1440 BODY_18 map: 90% overall figure height with 7 px-radius joints.
STAGE2_BODY_ONLY_OPENPOSE = "p7-5-3-openpose-fullbody-stage2-open-arms-short-long-legs-v7-yaw+00_pitch+00.png"


OUTFIT_STAGE_TARGETS: dict[str, dict[str, object]] = {
    "outfit_stage1_face_openpose": {
        "inputs": (STAGE2_BODY_ONLY_OPENPOSE, QWEN_FACE_REFERENCE),
        "input_roles": ["stage_2_calibrated_front_body_only_openpose", "frontal_head_identity_hair_1280"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 10,
        "size": (960, 1440),
        "negative_prompt": "OpenPose lines, dots, labels, text, panel, collage, extra person",
        "prompt": (
            "Picture 1 defines the strict front full-body pose and framing; do not render its lines. "
            "Picture 2 defines Mira's identity. "
            "Front full-body illustrated woman with both arms and hands visible, in a charcoal-gray micro crop tee, deep-teal high-waisted wide-leg trousers, with bare feet and no shoes."
        ),
    },
    "outfit_stage2_shoes": {
        "inputs": (SHOE_REFERENCE,),
        "predecessor": "outfit_stage1_face_openpose",
        "input_roles": ["stage_1_barefoot_fullbody", "white_sneakers_reference"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 10,
        "size": (960, 1440),
        "negative_prompt": "text, panel, collage, extra person",
        "prompt": (
            "Put the shoes from Picture 2 on both feet of the woman in Picture 1. "
            "Preserve the shoe design and colors from Picture 2. "
            "Keep the face, hair, clothing, pose, proportions, and background of Picture 1 unchanged."
        ),
    },
    "outfit_stage3_jacket_face": {
        "inputs": (QWEN_FACE_REFERENCE,),
        "predecessor": "outfit_stage2_shoes",
        "input_roles": ["stage_2_outfit_with_shoes", "frontal_head_identity_hair_1280"],
        "append_style_prompt": False,
        "append_illustration_prompt": False,
        "default_steps": 10,
        "size": (960, 1440),
        "negative_prompt": "OpenPose lines, dots, labels, text, panel, collage, extra person",
        "prompt": (
            "Front full-body woman. Image 1: retain the stage-2 crop top, wide trousers, sneakers, and proportions. "
            "Image 2: retain face and hair. Add an unzipped white cropped riding jacket: its front panels are visibly apart and never meet; a flat folded-down pointed shirt collar, white lining, and wrist-length sleeves cover shoulders and upper arms. Both hands are fully visible below the sleeve cuffs. The gray crop top is visible from neckline to hem above the bare midriff; no inner sleeves. Warm off-white background."
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
    for name in ("diffusers", "torch", "transformers", "accelerate"):
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
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    # Keep the official BF16 modules on CPU except for the module being used.
    # This avoids the FP4 Nunchaku transformer path and fits the 8 GB GPU run.
    pipe.enable_attention_slicing("max")
    pipe.enable_sequential_cpu_offload()
    return pipe


def parse_size(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", maxsplit=1)
        width, height = int(width_text), int(height_text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("--size must use WIDTHxHEIGHT, for example 1152x1728") from error
    if width < 16 or height < 16 or width % 16 or height % 16:
        raise argparse.ArgumentTypeError("--size values must be positive multiples of 16")
    return width, height


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=tuple(OUTFIT_STAGE_TARGETS), help="One outfit stage to generate.")
    parser.add_argument("--targets", nargs="+", choices=tuple(OUTFIT_STAGE_TARGETS), help="Generate stages sequentially.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--size", type=parse_size)
    parser.add_argument("--run-label", default="three-stage-v1")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--input", type=Path, help="Override the predecessor image for stage 2 or 3.")
    args = parser.parse_args()
    if args.input and (args.targets or args.target == "outfit_stage1_face_openpose"):
        parser.error("--input requires a single stage 2 or stage 3 target")
    if bool(args.target) == bool(args.targets):
        parser.error("provide exactly one of --target or --targets")
    if args.targets:
        for target_id in args.targets:
            command = [sys.executable, str(Path(__file__).resolve()), "--target", target_id, "--seed", str(args.seed), "--run-label", args.run_label, "--output-dir", str(args.output_dir)]
            if args.steps is not None:
                command.extend(("--steps", str(args.steps)))
            if args.size:
                command.extend(("--size", f"{args.size[0]}x{args.size[1]}"))
            subprocess.run(command, check=True)
        return
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = OUTFIT_STAGE_TARGETS[args.target]
    steps = args.steps if args.steps is not None else target.get("default_steps", DEFAULT_STEPS)
    if not isinstance(steps, int) or steps < 1:
        raise ValueError("--steps must be at least 1")
    inputs = [ASSETS / name for name in target["inputs"]]
    if predecessor := target.get("predecessor"):
        previous = args.input or (args.output_dir / (
            f"p7-5-3-qwen-edit-prompt-style-{predecessor}-{args.run_label}"
            f"-seed-{args.seed}-steps-{steps}.png"))
        inputs.insert(0, previous.resolve())
    if missing := [str(path) for path in inputs if not path.is_file()]:
        raise FileNotFoundError("missing input asset(s): " + ", ".join(missing))
    if not IDENTITY_CONTRACT.is_file():
        raise FileNotFoundError("missing Mira identity contract")
    identity = json.loads(IDENTITY_CONTRACT.read_text(encoding="utf-8"))
    rendering = identity["rendering_contract"]
    style_prompt = rendering["portrait_style_prompt"]
    illustration_prompt = rendering["front_face_illustration_prompt"]
    prompt_parts = []
    if target.get("append_style_prompt", True):
        prompt_parts.append(style_prompt)
    if target.get("append_illustration_prompt", False):
        prompt_parts.append(illustration_prompt)
    prompt_parts.append(target["prompt"])
    prompt = " ".join(prompt_parts)

    width, height = args.size or target["size"]
    stem = f"p7-5-3-qwen-edit-prompt-style-{args.target}-{args.run_label}-seed-{args.seed}-steps-{steps}"
    output = args.output_dir / f"{stem}.png"
    result_record = args.output_dir / f"{stem}-result.json"
    for path in (output, result_record):
        if path.exists():
            raise FileExistsError(path)
    started = time.monotonic()
    pipeline = load_pipeline()
    generation = {
        "prompt": prompt,
        "generator": torch.Generator("cpu").manual_seed(args.seed),
        "true_cfg_scale": 4.0,
        "negative_prompt": target.get("negative_prompt", " "),
        "num_inference_steps": steps,
        "guidance_scale": 1.0,
        "width": width,
        "height": height,
        "image": [load_image(str(path)).convert("RGB") for path in inputs],
    }
    result = pipeline(**generation).images[0]
    result.save(output)
    record = {
        "status": "generated",
        "experiment_id": f"p7-5-3-qwen-edit-{args.target}",
        "model": MODEL_ID,
        "dtype": "bfloat16",
        "transformer": "official_bf16",
        "offload_mode": "sequential_cpu_offload",
        "runtime": runtime_record(),
        "identity_contract": asset_record(IDENTITY_CONTRACT),
        "rendering_contract": {
            "source": "identity_contract.rendering_contract",
            "components": ["portrait_style_prompt", "front_face_illustration_prompt"],
        },
        "prompt_contracts_applied": {
            "watercolor_style": target.get("append_style_prompt", True),
            "illustration": target.get("append_illustration_prompt", False),
        },
        "target": args.target,
        "run_label": args.run_label,
        "inputs": [asset_record(path) for path in inputs],
        "input_roles": target["input_roles"],
        "seed": args.seed,
        "steps": steps,
        "size": [width, height],
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "negative_prompt": generation["negative_prompt"],
        "prompt": prompt,
        "prompt_word_count": len(prompt.split()),
        "output": asset_record(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "Generated staged front outfit reference; compare the stated inputs and outfit change.",
    }
    result_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result_record": str(result_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

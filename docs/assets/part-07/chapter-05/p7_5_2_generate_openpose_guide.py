#!/usr/bin/env python3
"""Create a neutral source image, then extract one configurable OpenPose guide.

Stage 1 makes an anonymous seven-head front-standing source with local Qwen
Image.  Stage 2 runs ``controlnet_aux`` OpenPose on that source.  Face and
hand landmark maps are opt-in so the default guide remains body-only.

Examples:
  # Make a new anonymous source and a body-only guide (the default).
  .venv/bin/python p7_5_2_generate_openpose_guide.py --stage all

  # Extract a Full map from an existing source without regenerating it.
  .venv/bin/python p7_5_2_generate_openpose_guide.py --stage openpose \
    --source-output p7-5-2-openpose-source-woman-seven-heads-v1.png \
    --include-face --include-hands --guide-output p7-5-2-openpose-source-woman-seven-heads-v1-full-guide.png
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import sysconfig
import time
import types
from pathlib import Path

import torch
from diffusers import QwenImagePipeline
from nunchaku import NunchakuQwenImageTransformer2DModel
from PIL import Image


ASSETS = Path(__file__).resolve().parent
ANNOTATORS = Path(
    "/home/cbsim/.cache/huggingface/hub/models--lllyasviel--Annotators/"
    "snapshots/982e7edaec38759d914a963c48c4726685de7d96"
)
MODEL_ID = "Qwen/Qwen-Image"
TRANSFORMER_ID = (
    "/home/cbsim/.cache/huggingface/hub/models--nunchaku-tech--nunchaku-qwen-image/"
    "snapshots/4d9f4f667ea571ab172e0ee29ac2c27b82a41a6b/"
    "svdq-fp4_r128-qwen-image.safetensors"
)
DEFAULT_SOURCE = ASSETS / "p7-5-2-openpose-source-woman-seven-heads-v2.png"
SOURCE_PROMPT = (
    "One anonymous adult woman, strict frontal full-body standing pose, centered and fully visible from hair crown to shoe soles. "
    "Natural approximately seven-head figure proportion, relaxed arms beside the torso, both feet parallel, neutral off-white studio background. "
    "Plain fitted long-sleeve top, straight trousers, simple flat shoes, no bag, no accessory, no text, no other person, no scene."
)


def detector_class():
    """Load only controlnet_aux OpenPose without importing optional extras."""
    root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    parent = types.ModuleType("p7_5_2_openpose_aux")
    parent.__path__ = [str(root)]
    sys.modules[parent.__name__] = parent
    directory = root / "open_pose"
    spec = importlib.util.spec_from_file_location(
        "p7_5_2_openpose_aux.open_pose",
        directory / "__init__.py",
        submodule_search_locations=[str(directory)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("controlnet_aux OpenPose implementation is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.OpenposeDetector


def guide_default_path(source: Path, include_face: bool, include_hands: bool) -> Path:
    suffix = "full" if include_face and include_hands else "body-face" if include_face else "body-hand" if include_hands else "body"
    return source.with_name(f"{source.stem}-{suffix}-guide.png")


def prevent_overwrite(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists; choose a new output name or pass --overwrite")


def generate_source(*, output: Path, seed: int, steps: int, width: int, height: int) -> dict[str, object]:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for --stage source or --stage all")
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=4)
    pipeline = QwenImagePipeline.from_pretrained(
        MODEL_ID,
        transformer=transformer,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    pipeline._exclude_from_cpu_offload.append("transformer")
    pipeline.enable_sequential_cpu_offload()
    started = time.monotonic()
    image = pipeline(
        prompt=SOURCE_PROMPT,
        width=width,
        height=height,
        num_inference_steps=steps,
        true_cfg_scale=4.0,
        guidance_scale=1.0,
        negative_prompt=" ",
        generator=torch.Generator("cpu").manual_seed(seed),
    ).images[0]
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    del pipeline
    torch.cuda.empty_cache()
    return {
        "model": MODEL_ID,
        "transformer": TRANSFORMER_ID,
        "seed": seed,
        "steps": steps,
        "size": [width, height],
        "prompt": SOURCE_PROMPT,
        "prompt_word_count": len(SOURCE_PROMPT.split()),
        "output": output.name,
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }


def extract_openpose(*, source_path: Path, output: Path, include_face: bool, include_hands: bool) -> dict[str, object]:
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    if not ANNOTATORS.is_dir():
        raise FileNotFoundError(ANNOTATORS)
    source = Image.open(source_path).convert("RGB")
    detector = detector_class().from_pretrained(ANNOTATORS, local_files_only=True)
    started = time.monotonic()
    guide = detector(
        source,
        detect_resolution=1024,
        image_resolution=1024,
        include_body=True,
        include_hand=include_hands,
        include_face=include_face,
        output_type="pil",
    ).convert("RGB")
    if guide.size != source.size:
        guide = guide.resize(source.size, Image.Resampling.NEAREST)
    output.parent.mkdir(parents=True, exist_ok=True)
    guide.save(output)
    return {
        "detector": "controlnet_aux OpenposeDetector from lllyasviel/Annotators",
        "source": source_path.name,
        "output": output.name,
        "include_body": True,
        "include_face": include_face,
        "include_hands": include_hands,
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("all", "source", "openpose"), default="all")
    parser.add_argument("--source-output", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--guide-output", type=Path)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1536)
    parser.add_argument("--include-face", action="store_true", help="Include the detailed OpenPose face landmark map.")
    parser.add_argument("--include-hands", action="store_true", help="Include OpenPose hand landmark maps.")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if args.width < 16 or args.height < 16 or args.width % 16 or args.height % 16:
        raise ValueError("--width and --height must be positive multiples of 16")

    source_path = args.source_output if args.source_output.is_absolute() else ASSETS / args.source_output
    output = args.guide_output or guide_default_path(source_path, args.include_face, args.include_hands)
    output = output if output.is_absolute() else ASSETS / output
    record_path = output.with_name(f"{output.stem}-run.json")
    if args.stage in {"all", "source"}:
        prevent_overwrite(source_path, args.overwrite)
    if args.stage in {"all", "openpose"}:
        prevent_overwrite(output, args.overwrite)
        prevent_overwrite(record_path, args.overwrite)

    record: dict[str, object] = {
        "status": "review_required",
        "pipeline": Path(__file__).name,
        "stage": args.stage,
    }
    if args.stage in {"all", "source"}:
        record["source_generation"] = generate_source(
            output=source_path,
            seed=args.seed,
            steps=args.steps,
            width=args.width,
            height=args.height,
        )
    if args.stage in {"all", "openpose"}:
        record["openpose_extraction"] = extract_openpose(
            source_path=source_path,
            output=output,
            include_face=args.include_face,
            include_hands=args.include_hands,
        )
        record["decision"] = "Review the guide before using it as a structural input or approving it."
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

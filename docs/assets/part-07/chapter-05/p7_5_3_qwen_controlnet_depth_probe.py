#!/usr/bin/env python3
"""Probe genuine Qwen ControlNet depth conditioning without image-reference fusion."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path

import torch
from diffusers import QwenImageControlNetModel, QwenImageControlNetPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
MODEL_ID = "Qwen/Qwen-Image"
TRANSFORMER_ID = (
    "/home/cbsim/.cache/huggingface/hub/models--nunchaku-tech--nunchaku-qwen-image/"
    "snapshots/4d9f4f667ea571ab172e0ee29ac2c27b82a41a6b/svdq-fp4_r128-qwen-image.safetensors"
)
CONTROLNET_ID = "InstantX/Qwen-Image-ControlNet-Union"
DEFAULT_DEPTH = ASSETS / "p7-5-3-qwen-storyboard-scene-a-549191-seed-5420-steps-20-depth.png"
PROMPT = (
    "A woman wearing a white cropped jacket with a folded collar, a gray crop top, "
    "teal wide-leg trousers, and white sneakers, leaping over a coastal cliff path."
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=Path, default=DEFAULT_DEPTH)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1024)
    parser.add_argument("--control-scale", type=float, default=0.8)
    parser.add_argument("--run-label", default="v1")
    args = parser.parse_args()
    if args.steps < 1 or args.size < 256 or args.size % 16:
        parser.error("steps must be positive and size must be a multiple of 16")
    depth = args.depth.resolve()
    if not depth.is_file():
        raise FileNotFoundError(depth)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    output_stem = f"p7-5-3-qwen-controlnet-depth-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output = ASSETS / f"{output_stem}.png"
    result = ASSETS / f"{output_stem}-result.json"
    started = time.monotonic()
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    controlnet = QwenImageControlNetModel.from_pretrained(
        CONTROLNET_ID, torch_dtype=torch.bfloat16, local_files_only=True
    )
    pipe = QwenImageControlNetPipeline.from_pretrained(
        MODEL_ID,
        transformer=transformer,
        controlnet=controlnet,
        torch_dtype=torch.bfloat16,
        local_files_only=True,
    )
    pipe._exclude_from_cpu_offload.append("transformer")
    pipe.enable_sequential_cpu_offload()
    try:
        image = pipe(
            prompt=PROMPT,
            negative_prompt=" ",
            control_image=load_image(str(depth)).convert("RGB"),
            controlnet_conditioning_scale=args.control_scale,
            true_cfg_scale=4.0,
            guidance_scale=1.0,
            num_inference_steps=args.steps,
            width=args.size,
            height=args.size,
            generator=torch.Generator("cpu").manual_seed(args.seed),
        ).images[0]
        image.save(output)
        result.write_text(
            json.dumps(
                {
                    "status": "generated",
                    "experiment_id": "p7-5-3-qwen-controlnet-depth",
                    "model": MODEL_ID,
                    "transformer": TRANSFORMER_ID,
                    "controlnet": CONTROLNET_ID,
                    "control_image": {"path": str(depth), "sha256": sha256(depth)},
                    "prompt": PROMPT,
                    "seed": args.seed,
                    "steps": args.steps,
                    "size": [args.size, args.size],
                    "true_cfg_scale": 4.0,
                    "controlnet_conditioning_scale": args.control_scale,
                    "output": {"path": str(output), "sha256": sha256(output)},
                    "elapsed_seconds": round(time.monotonic() - started, 2),
                    "runtime": {
                        "python": platform.python_version(),
                        "diffusers": importlib.metadata.version("diffusers"),
                        "torch": importlib.metadata.version("torch"),
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))
    finally:
        del pipe
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

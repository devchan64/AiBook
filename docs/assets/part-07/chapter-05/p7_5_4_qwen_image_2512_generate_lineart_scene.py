#!/usr/bin/env python3
"""Generate a Qwen-Image-2512 line-art scene from text alone.

This pure text-to-image generator deliberately does not supply Mira or a
prior scene image. The runner uses direct Diffusers with BF16 sequential CPU
offload and does not start a server.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path


ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parents[3]
CACHE_DIR = ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-2512"
DEFAULT_SIZE = 640
DEFAULT_STEPS = 20
DEFAULT_SEED = 5420
DEFAULT_RUN_LABEL = "worm-eye-front-running-v15"
SCENE_A_PROMPT = (
    "Korean webtoon line art: worm's-eye view of a woman running toward the camera on a city street. "
    "Ground-level camera looking up; an open sky fills the upper background. Face and chest visible, "
    "with the sole of her raised leading shoe visible."
)


def sha256(path: Path) -> str:
    """Return the SHA-256 digest stored with the generated asset."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_version(name: str) -> str | None:
    """Return an installed package version when available."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def prompt_word_count(prompt: str) -> int:
    """Count whitespace-delimited prompt words for the result record."""
    return len(prompt.split())


def parse_args() -> argparse.Namespace:
    """Parse the reproducible text-to-image line-art scene request."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", default=SCENE_A_PROMPT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--run-label", default=DEFAULT_RUN_LABEL)
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    args = parser.parse_args()
    if args.size < 32 or args.size % 32:
        parser.error("--size must be a positive multiple of 32")
    if args.steps < 1:
        parser.error("--steps must be positive")
    return args


def generate(args: argparse.Namespace):
    """Generate the requested line-art scene through the direct T2I pipeline."""
    import torch
    from diffusers import QwenImagePipeline

    pipeline = QwenImagePipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipeline.enable_attention_slicing("max")
    pipeline.enable_sequential_cpu_offload()
    started = time.monotonic()
    image = pipeline(
        prompt=args.prompt,
        negative_prompt=" ",
        width=args.size,
        height=args.size,
        num_inference_steps=args.steps,
        true_cfg_scale=4.0,
        generator=torch.Generator(device="cpu").manual_seed(args.seed),
    ).images[0]
    return image, time.monotonic() - started


def main() -> None:
    """Create one line-art Scene A image and its result record."""
    args = parse_args()
    stem = (
        f"p7-5-4-qwen-image-2512-scene-a-{args.run_label}"
        f"-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    )
    output = args.output_dir.resolve() / f"{stem}.png"
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite prior output: {output}")
    image, elapsed_seconds = generate(args)
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output)
    result = {
        "status": "generated",
        "stage": "lineart_scene_text_to_image",
        "execution_mode": "direct Diffusers; BF16; sequential CPU offload; no server",
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "packages": {
                name: package_version(name)
                for name in ("diffusers", "torch", "transformers", "accelerate")
            },
        },
        "model": {
            "repository": MODEL_ID,
            "dtype": "bfloat16",
            "device_placement": "sequential_cpu_offload",
        },
        "inputs": [],
        "prompt": args.prompt,
        "prompt_word_count": prompt_word_count(args.prompt),
        "seed": args.seed,
        "steps": args.steps,
        "true_cfg_scale": 4.0,
        "size": [args.size, args.size],
        "output": {
            "path": str(output),
            "sha256": sha256(output),
            "width": args.size,
            "height": args.size,
        },
        "elapsed_seconds": round(elapsed_seconds, 2),
    }
    result_path = output.with_name(f"{output.stem}-result.json")
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

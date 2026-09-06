#!/usr/bin/env python3
"""Enrich a P7-5.4 line-art storyboard scene with Qwen-Image-Edit-2511.

Picture 1 fixes composition, action, and the background relationship. Picture
2 is Mira's full-body outfit image and supplies only visual style: linework,
restrained palette, and outfit silhouette. This stage adds secondary people
and environmental objects without replacing Picture 1's geometry. It uses
direct Diffusers BF16 with sequential CPU offload and starts no ComfyUI server.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path

from PIL import Image


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"

DEFAULT_REFERENCE = ASSETS / (
    "p7-5-4-qwen-image-2512-scene-a-worm-eye-front-running-v15-"
    "size-640x640-seed-5420-steps-5.png"
)
DEFAULT_MIRA_OUTFIT_STYLE = ASSETS / (
    "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-"
    "folded-collar-v3-seed-62294-steps-30.png"
)
DEFAULT_PROMPT = (
    "Picture 1 defines the composition. Preserve its central woman, frontal running pose, low street-level view, "
    "and background geometry. Use Picture 2 as the visual-style reference for clean delicate linework, restrained "
    "color treatment, and the woman's outfit silhouette. Add surrounding runners, sidewalk pedestrians, storefront "
    "signs, street lamps, and distant buildings."
)
DEFAULT_SIZE = 1280
DEFAULT_STEPS = 20
DEFAULT_TRUE_CFG_SCALE = 4.0
DEFAULT_GUIDANCE_SCALE = 1.0
DEFAULT_SEED = 5420
DEFAULT_RUN_LABEL = "surroundings-v1"


def sha256(path: Path) -> str:
    """Return a file digest for the reproducibility record."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_version(name: str) -> str | None:
    """Return an installed package version when it is available."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def prompt_word_count(prompt: str) -> int:
    """Count whitespace-delimited prompt words for the result record."""
    return len(prompt.split())


def load_square_reference(path: Path, size: int) -> Image.Image:
    """Load the line-art reference at the requested square edit resolution."""
    with Image.open(path) as source:
        return source.convert("RGB").resize((size, size), Image.Resampling.LANCZOS)


def load_centered_style_reference(path: Path, size: int) -> Image.Image:
    """Center the full-body outfit image on white without changing its proportions."""
    with Image.open(path) as source:
        reference = source.convert("RGBA")
        reference.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - reference.width) // 2, (size - reference.height) // 2)
        canvas.alpha_composite(reference, offset)
    return canvas.convert("RGB")


def parse_args() -> argparse.Namespace:
    """Parse a reproducible Scene A surroundings-enrichment request."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--mira-outfit-style", type=Path, default=DEFAULT_MIRA_OUTFIT_STYLE)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--true-cfg-scale", type=float, default=DEFAULT_TRUE_CFG_SCALE)
    parser.add_argument("--run-label", default=DEFAULT_RUN_LABEL)
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.reference.is_file():
        parser.error(f"Missing line-art reference: {args.reference}")
    if not args.mira_outfit_style.is_file():
        parser.error(f"Missing Mira outfit style reference: {args.mira_outfit_style}")
    if args.size < 32 or args.size % 32:
        parser.error("--size must be a positive multiple of 32")
    if args.steps < 1:
        parser.error("--steps must be positive")
    if args.true_cfg_scale <= 0:
        parser.error("--true-cfg-scale must be positive")
    return args


def output_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    """Build collision-safe PNG and result JSON paths."""
    stem = (
        "p7-5-4-qwen-2511-lineart-scene-a-"
        f"{args.run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    )
    output = args.output_dir.resolve() / f"{stem}.png"
    return output, output.with_name(f"{output.stem}-result.json")


def runtime_record() -> dict[str, object]:
    """Record the direct generation environment."""
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            name: package_version(name)
            for name in ("diffusers", "torch", "transformers", "accelerate")
        },
    }


def generate(args: argparse.Namespace) -> tuple[Image.Image, float]:
    """Edit the line-art composition while adding Scene A surroundings."""
    import torch
    from diffusers import QwenImageEditPlusPipeline

    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    pipeline.enable_attention_slicing("max")
    pipeline.enable_sequential_cpu_offload()
    started = time.monotonic()
    with torch.inference_mode():
        image = pipeline(
            image=[
                load_square_reference(args.reference, args.size),
                load_centered_style_reference(args.mira_outfit_style, args.size),
            ],
            prompt=args.prompt,
            negative_prompt=" ",
            width=args.size,
            height=args.size,
            num_inference_steps=args.steps,
            true_cfg_scale=args.true_cfg_scale,
            guidance_scale=DEFAULT_GUIDANCE_SCALE,
            generator=torch.Generator(device="cuda").manual_seed(args.seed),
        ).images[0]
    return image, time.monotonic() - started


def main() -> None:
    """Generate one 1280-pixel Scene A surroundings enrichment and its record."""
    args = parse_args()
    output, result_path = output_paths(args)
    plan = {
        "status": "planned",
        "stage": "lineart_scene_surroundings_enrichment",
        "execution_mode": "direct Diffusers; BF16; sequential CPU offload; no ComfyUI server",
        "model": MODEL_ID,
        "inputs": [
            str(args.reference.resolve()),
            str(args.mira_outfit_style.resolve()),
        ],
        "prompt": args.prompt,
        "prompt_word_count": prompt_word_count(args.prompt),
        "seed": args.seed,
        "steps": args.steps,
        "size": [args.size, args.size],
        "output": str(output),
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    if output.exists() or result_path.exists():
        raise FileExistsError(f"Refusing to overwrite prior output: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    image, elapsed_seconds = generate(args)
    image.save(output)
    result = {
        **plan,
        "status": "generated",
        "runtime": runtime_record(),
        "model": {
            "repository": MODEL_ID,
            "dtype": "bfloat16",
            "device_placement": "sequential_cpu_offload",
        },
        "inputs": [
            {
                "role": "Picture 1: fixed line-art composition, pose, and background geometry",
                "path": str(args.reference.resolve()),
                "sha256": sha256(args.reference),
            },
            {
                "role": "Picture 2: Mira full-body outfit visual-style reference",
                "path": str(args.mira_outfit_style.resolve()),
                "sha256": sha256(args.mira_outfit_style),
            },
        ],
        "reference_order": "lineart-composition, mira-outfit-style",
        "reference_roles": {
            "Picture 1": "composition, pose, and background geometry",
            "Picture 2": "linework, restrained palette, and outfit silhouette",
        },
        "edit_scope": "surrounding people and environmental objects only",
        "true_cfg_scale": args.true_cfg_scale,
        "guidance_scale": DEFAULT_GUIDANCE_SCALE,
        "output": {
            "path": str(output),
            "sha256": sha256(output),
            "width": image.width,
            "height": image.height,
        },
        "elapsed_seconds": round(elapsed_seconds, 2),
    }
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

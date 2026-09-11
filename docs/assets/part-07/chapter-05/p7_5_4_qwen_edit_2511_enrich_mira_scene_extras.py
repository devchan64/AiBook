#!/usr/bin/env python3
"""Add scene-specific extras to a fixed Mira-applied P7-5.4 scene.

Picture 1 is already a finished Mira scene.  The short prompt adds only the
scene's supporting subjects: pedestrians in A, woodland animals in B, or birds
in C.  The runner calls Qwen-Image-Edit-2511 directly through Diffusers with
BF16 sequential CPU offload onto the local CUDA GPU; it starts no ComfyUI server.
Scene C starts from the bird-free Mira scene to avoid retaining malformed birds.
Run its revised prompt with --scenes c (default label: extras-v5).
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
ROOT = ASSETS.parents[3]
CACHE_DIR = ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
DEFAULT_SIZE = 1280
DEFAULT_STEPS = 20
DEFAULT_TRUE_CFG_SCALE = 4.0
DEFAULT_SEEDS = {"a": 5420, "b": 5421, "c": 5422}
DEFAULT_RUN_LABEL = "extras-v4"
SCENE_RUN_LABELS = {"c": "extras-v5"}
MIRA_SCENES = {
    scene: ASSETS / (
        f"p7-5-4-qwen-2511-lineart-scene-{scene}-mira-identity-v1-"
        f"size-1280x1280-seed-{seed}-steps-20.png"
    )
    for scene, seed in DEFAULT_SEEDS.items()
}
EXTRA_PROMPTS = {
    "a": (
        "Add several pedestrians and several people running in casual clothing to Image 1."
    ),
    "b": (
        "Add two small animals to Image 1: one rabbit sitting on the clearing floor "
        "beside the lower-left ferns; and one squirrel standing on the ground at the base "
        "of the right tree."
    ),
    "c": (
        "Add three small birds to Image 1: one perched on top of the existing square "
        "railing post to the right of the male reader; one perched on the existing "
        "upper wooden rail near the right edge; and one sitting on the foreground "
        "rock at the lower left, beside Mira."
    ),
}


def sha256(path: Path) -> str:
    """Return the digest stored in the output record."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_file(path: Path, label: str) -> Path:
    """Return an input file, or make a missing dependency explicit."""
    resolved = path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"Missing {label}: {resolved}")
    return resolved


def square_canvas(path: Path, size: int) -> Image.Image:
    """Fit one fixed scene to the requested square canvas."""
    with Image.open(path) as source:
        image = source.convert("RGBA")
        image.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - image.width) // 2, (size - image.height) // 2)
        canvas.alpha_composite(image, offset)
    return canvas.convert("RGB")


def package_version(name: str) -> str | None:
    """Read an installed package version without assuming it is installed."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def parse_args() -> argparse.Namespace:
    """Parse one or more independent extra-subject generation requests."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenes", nargs="+", choices=tuple(MIRA_SCENES), default=("a",))
    parser.add_argument("--scene-image", type=Path, help="Override Picture 1; requires exactly one scene.")
    parser.add_argument("--prompt", help="Override the short scene-specific prompt.")
    parser.add_argument("--seed", type=int, help="Defaults to the selected scene seed.")
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--true-cfg-scale", type=float, default=DEFAULT_TRUE_CFG_SCALE)
    parser.add_argument("--run-label", help="Output label; defaults to extras-v5 for C, extras-v4 otherwise.")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.scene_image is not None and len(args.scenes) != 1:
        parser.error("--scene-image requires exactly one selected scene")
    if args.size < 32 or args.size % 32:
        parser.error("--size must be a positive multiple of 32")
    if args.steps < 1:
        parser.error("--steps must be positive")
    if args.true_cfg_scale <= 0:
        parser.error("--true-cfg-scale must be positive")
    return args


def build_plan(args: argparse.Namespace, scene: str) -> dict[str, object]:
    """Build a single-reference edit plan with an unambiguous subject role."""
    source = require_file(args.scene_image or MIRA_SCENES[scene], "Picture 1 Mira-applied scene")
    seed = args.seed if args.seed is not None else DEFAULT_SEEDS[scene]
    prompt = args.prompt or EXTRA_PROMPTS[scene]
    run_label = args.run_label or SCENE_RUN_LABELS.get(scene, DEFAULT_RUN_LABEL)
    stem = (
        f"p7-5-4-qwen-2511-lineart-scene-{scene}-{run_label}"
        f"-size-{args.size}x{args.size}-seed-{seed}-steps-{args.steps}"
    )
    output = args.output_dir.resolve() / f"{stem}.png"
    return {
        "scene": scene,
        "source": source,
        "prompt": prompt,
        "seed": seed,
        "steps": args.steps,
        "size": args.size,
        "true_cfg_scale": args.true_cfg_scale,
        "output": output,
        "result": output.with_name(f"{output.stem}-result.json"),
    }


def load_pipeline(*, allow_download: bool):
    """Load one reusable direct-Diffusers image-edit pipeline."""
    import torch
    from diffusers import QwenImageEditPlusPipeline

    if not torch.cuda.is_available():
        raise RuntimeError("A local CUDA GPU is required for Qwen image editing.")

    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not allow_download,
    )
    pipeline.enable_attention_slicing("max")
    pipeline.enable_sequential_cpu_offload()
    return pipeline, torch


def generate(plan: dict[str, object], *, pipeline, torch) -> tuple[Image.Image, float]:
    """Add the one requested supporting-subject group to Picture 1."""
    started = time.monotonic()
    size = int(plan["size"])
    image = pipeline(
        image=[square_canvas(plan["source"], size)],
        prompt=str(plan["prompt"]),
        negative_prompt=" ",
        width=size,
        height=size,
        num_inference_steps=int(plan["steps"]),
        true_cfg_scale=float(plan["true_cfg_scale"]),
        guidance_scale=1.0,
        generator=torch.Generator(device="cuda").manual_seed(int(plan["seed"])),
    ).images[0]
    return image, time.monotonic() - started


def write_result(plan: dict[str, object], elapsed_seconds: float) -> None:
    """Persist reproducible input, prompt, sampling, and output metadata."""
    output = plan["output"]
    result = {
        "status": "generated",
        "stage": "scene_extras_enrichment",
        "scene": plan["scene"],
        "execution_mode": "direct Diffusers; BF16; sequential CPU offload; no ComfyUI server",
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "packages": {name: package_version(name) for name in ("diffusers", "torch", "transformers", "accelerate")},
        },
        "model": {
            "repository": MODEL_ID,
            "dtype": "bfloat16",
            "device_placement": "sequential_cpu_offload",
        },
        "inputs": [{
            "role": "Picture 1: fixed Mira scene; preserve composition and lead character",
            "path": str(plan["source"]),
            "sha256": sha256(plan["source"]),
        }],
        "prompt": plan["prompt"],
        "prompt_word_count": len(str(plan["prompt"]).split()),
        "seed": plan["seed"],
        "steps": plan["steps"],
        "true_cfg_scale": plan["true_cfg_scale"],
        "guidance_scale": 1.0,
        "size": [plan["size"], plan["size"]],
        "output": {
            "path": str(output),
            "sha256": sha256(output),
            "width": plan["size"],
            "height": plan["size"],
        },
        "elapsed_seconds": round(elapsed_seconds, 2),
    }
    plan["result"].write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    """Generate extras for requested scenes, loading the model only once."""
    args = parse_args()
    plans = [build_plan(args, scene) for scene in dict.fromkeys(args.scenes)]
    if args.dry_run:
        printable = [{key: str(value) if isinstance(value, Path) else value for key, value in plan.items()} for plan in plans]
        print(json.dumps({"status": "planned", "model": MODEL_ID, "plans": printable}, ensure_ascii=False, indent=2))
        return
    for plan in plans:
        if plan["output"].exists() or plan["result"].exists():
            raise FileExistsError(f"Refusing to overwrite output: {plan['output']}")
    pipeline, torch = load_pipeline(allow_download=args.allow_download)
    for plan in plans:
        plan["output"].parent.mkdir(parents=True, exist_ok=True)
        image, elapsed_seconds = generate(plan, pipeline=pipeline, torch=torch)
        image.save(plan["output"])
        write_result(plan, elapsed_seconds)
        print(json.dumps({"scene": plan["scene"], "output": str(plan["output"]), "result": str(plan["result"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()

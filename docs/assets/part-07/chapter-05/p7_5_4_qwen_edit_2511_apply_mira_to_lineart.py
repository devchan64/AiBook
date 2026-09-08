#!/usr/bin/env python3
"""Apply Mira's visual identity to one fixed P7-5.4 line-art scene.

Picture 1 fixes the scene composition. Picture 2 supplies Mira's face, hair,
outfit, linework, and restrained color treatment. This direct Diffusers runner
uses Qwen-Image-Edit-2511 with BF16 sequential CPU offload and starts no server.
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
DEFAULT_RUN_LABEL = "mira-identity-v1"
DEFAULT_MIRA_REFERENCE = ASSETS / (
    'p7-5-3-qwen-edit-prompt-style-outfit_stage3_jacket_face-three-stage-v1-seed-62294-steps-10.png'
)
DEFAULT_IDENTITY_CONTRACT = ASSETS / "p7-5-2-mira-identity-contract.json"
LINEART_BY_SCENE = {
    scene: ASSETS / (
        f"p7-5-4-qwen-image-2512-scene-{scene}-lineart-v1-size-1280x1280-"
        f"seed-{seed}-steps-20.png"
    )
    for scene, seed in DEFAULT_SEEDS.items()
}
SCENE_PROMPTS = {
    "a": (
        "Replace the central running woman in Picture 1 with Mira from Picture 2. "
        "Preserve Picture 1's composition, running pose, low camera view, city street, and other runners."
    ),
    "b": (
        "Replace the leaping woman in Picture 1 with Mira from Picture 2. "
        "Preserve Picture 1's composition, grand jeté pose, side view, forest clearing, and sunset."
    ),
    "c": (
        "Replace the woman reading on the left in Picture 1 with Mira from Picture 2. "
        "Preserve Picture 1's composition, seated pose, second reader, books, hillside railing, and city skyline."
    ),
}
MIRA_REFERENCE_PROMPT = (
    "Use Picture 2 for Mira's face, hair, outfit, clean linework, and restrained color treatment."
)


def sha256(path: Path) -> str:
    """Return the digest written to the reproducibility record."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_file(path: Path, label: str) -> Path:
    """Return a resolved file or identify the missing input clearly."""
    resolved = path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"Missing {label}: {resolved}")
    return resolved


def square_canvas(path: Path, size: int) -> Image.Image:
    """Place a reference on a white square without changing its aspect ratio."""
    with Image.open(path) as source:
        reference = source.convert("RGBA")
        reference.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - reference.width) // 2, (size - reference.height) // 2)
        canvas.alpha_composite(reference, offset)
    return canvas.convert("RGB")


def package_version(name: str) -> str | None:
    """Return an installed package version when present."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def prompt_word_count(prompt: str) -> int:
    """Count the words stored in the generated result record."""
    return len(prompt.split())


def parse_args() -> argparse.Namespace:
    """Parse one or more reproducible line-art identity-transfer requests."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenes", nargs="+", choices=tuple(LINEART_BY_SCENE), default=("a",))
    parser.add_argument("--lineart", type=Path, help="Override Picture 1; requires exactly one selected scene.")
    parser.add_argument("--mira-reference", type=Path, default=DEFAULT_MIRA_REFERENCE)
    parser.add_argument("--identity-contract", type=Path, default=DEFAULT_IDENTITY_CONTRACT)
    parser.add_argument("--prompt", help="Override the full short edit prompt.")
    parser.add_argument("--seed", type=int, help="Defaults to the selected scene seed.")
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE)
    parser.add_argument("--true-cfg-scale", type=float, default=DEFAULT_TRUE_CFG_SCALE)
    parser.add_argument("--run-label", default=DEFAULT_RUN_LABEL)
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.size < 32 or args.size % 32:
        parser.error("--size must be a positive multiple of 32")
    if args.steps < 1:
        parser.error("--steps must be positive")
    if args.true_cfg_scale <= 0:
        parser.error("--true-cfg-scale must be positive")
    if args.lineart is not None and len(args.scenes) != 1:
        parser.error("--lineart requires exactly one selected scene")
    return args


def build_plan(args: argparse.Namespace, scene: str) -> dict[str, object]:
    """Build the two-picture reference contract and output locations."""
    lineart = require_file(args.lineart or LINEART_BY_SCENE[scene], "Picture 1 line-art scene")
    mira = require_file(args.mira_reference, "Picture 2 Mira reference")
    contract = require_file(args.identity_contract, "Mira identity contract")
    seed = args.seed if args.seed is not None else DEFAULT_SEEDS[scene]
    prompt = args.prompt or f"{SCENE_PROMPTS[scene]} {MIRA_REFERENCE_PROMPT}"
    stem = (
        f"p7-5-4-qwen-2511-lineart-scene-{scene}-{args.run_label}"
        f"-size-{args.size}x{args.size}-seed-{seed}-steps-{args.steps}"
    )
    output = args.output_dir.resolve() / f"{stem}.png"
    return {
        "scene": scene,
        "lineart": lineart,
        "mira": mira,
        "contract": contract,
        "prompt": prompt,
        "seed": seed,
        "steps": args.steps,
        "size": args.size,
        "true_cfg_scale": args.true_cfg_scale,
        "output": output,
        "result": output.with_name(f"{output.stem}-result.json"),
    }


def load_pipeline(*, allow_download: bool):
    """Load the direct image-edit pipeline once for a sequential scene run."""
    import torch
    from diffusers import QwenImageEditPlusPipeline

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
    """Run one two-reference edit through the already-loaded pipeline."""
    started = time.monotonic()
    size = int(plan["size"])
    image = pipeline(
        image=[square_canvas(plan["lineart"], size), square_canvas(plan["mira"], size)],
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
    """Write the paired input roles and exact sampling settings."""
    output = plan["output"]
    result = {
        "status": "generated",
        "stage": "lineart_mira_identity_style_transfer",
        "scene": plan["scene"],
        "execution_mode": "direct Diffusers; BF16; sequential CPU offload; no ComfyUI server",
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
        "inputs": [
            {"role": "Picture 1: fixed line-art composition", "path": str(plan["lineart"]), "sha256": sha256(plan["lineart"])},
            {"role": "Picture 2: Mira identity and visual-style reference", "path": str(plan["mira"]), "sha256": sha256(plan["mira"])},
        ],
        "identity_contract": {
            "path": str(plan["contract"]),
            "sha256": sha256(plan["contract"]),
            "role": "metadata only; identity wording is not appended to the prompt",
        },
        "reference_order": "lineart-composition, mira-identity-style",
        "prompt": plan["prompt"],
        "prompt_word_count": prompt_word_count(str(plan["prompt"])),
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
    """Create one or more Mira-applied scenes or print their exact contracts."""
    args = parse_args()
    plans = [build_plan(args, scene) for scene in dict.fromkeys(args.scenes)]
    if args.dry_run:
        printable_plans = [
            {key: str(value) if isinstance(value, Path) else value for key, value in plan.items()}
            for plan in plans
        ]
        print(json.dumps({"status": "planned", "model": MODEL_ID, "plans": printable_plans}, ensure_ascii=False, indent=2))
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

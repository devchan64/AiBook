#!/usr/bin/env python3
"""Generate one Mira storyboard scene with Qwen-Image-Edit-2511.

Picture 1 is Mira's full-body outfit reference. Scene layout, pose, setting,
and composition are defined only by each scene prompt; no prior scene image or
separate face image is used as an input. The runner uses direct Diffusers BF16
with sequential CPU offload and never starts a ComfyUI server.
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

DEFAULT_MIRA_FULLBODY = ASSETS / (
    "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-"
    "folded-collar-v3-seed-62294-steps-30.png"
)
DEFAULT_SIZE = 1280
DEFAULT_STEPS = 20
DEFAULT_TRUE_CFG_SCALE = 4.0
DEFAULT_RUN_LABEL = "v7"
MIRA_LINEWORK_REFERENCE_PROMPT = (
    "Render the central protagonist with the clean, delicate linework, soft facial rendering, "
    "and restrained color treatment of Mira in Picture 1."
)
SCENE_SEEDS = {"a": 5420, "b": 5421, "c": 5422}

# Do not add Mira identity or outfit descriptions here. The image references,
# rather than tokens, define the protagonist's appearance.
SCENE_PROMPTS = {
    "a": (
        "Create one central female protagonist running frontally toward the viewer through a city street, "
        "with a crowd of runners behind her. Use the woman in Picture 1."
    ),
    "b": (
        "Create one central female protagonist performing a grand jeté in a wide side view on a beach at sunset, "
        "with her reflection on the wet shore. Use the woman in Picture 1."
    ),
    "c": (
        "Create a two-person scene on a hillside overlook: the woman in Picture 1 reads on the left, "
        "beside a second person with books, a stone railing, and a city skyline."
    ),
}


def sha256(path: Path) -> str:
    """Return the SHA-256 digest recorded for every input and output."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_file(path: Path, label: str) -> Path:
    """Resolve and validate a required input artifact."""
    resolved = path.resolve()
    if not resolved.is_file():
        raise FileNotFoundError(f"Missing {label}: {resolved}")
    return resolved


def square_canvas(path: Path, size: int) -> Image.Image:
    """Center a reference on a white square without changing its proportions."""
    with Image.open(path) as source:
        reference = source.convert("RGBA")
        reference.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - reference.width) // 2, (size - reference.height) // 2)
        canvas.alpha_composite(reference, offset)
    return canvas.convert("RGB")


def package_version(name: str) -> str | None:
    """Return an installed package version when it is available."""
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def runtime_record() -> dict[str, object]:
    """Record the direct generation runtime."""
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            name: package_version(name)
            for name in ("diffusers", "torch", "transformers", "accelerate")
        },
    }


def parse_args() -> argparse.Namespace:
    """Parse a reproducible image-guided storyboard request."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", choices=tuple(SCENE_PROMPTS), default="a")
    parser.add_argument("--mira-fullbody", type=Path, default=DEFAULT_MIRA_FULLBODY)
    parser.add_argument("--prompt", help="One-off scene-only prompt override; no identity text is added.")
    parser.add_argument("--seed", type=int, help="Defaults to the selected scene's recorded seed.")
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
    return args


def build_plan(args: argparse.Namespace) -> dict[str, object]:
    """Build the scene-text plus one-reference Mira identity contract."""
    seed = args.seed if args.seed is not None else SCENE_SEEDS[args.scene]
    scene_prompt = args.prompt or SCENE_PROMPTS[args.scene]
    stem = (
        f"p7-5-4-qwen-2511-mira-reference-scene-{args.scene}-{args.run_label}"
        f"-size-{args.size}x{args.size}-seed-{seed}-steps-{args.steps}"
    )
    return {
        "scene": args.scene,
        "fullbody": require_file(args.mira_fullbody, "Mira full-body reference"),
        "scene_prompt": scene_prompt,
        "mira_linework_reference_prompt": MIRA_LINEWORK_REFERENCE_PROMPT,
        "prompt": f"{scene_prompt} {MIRA_LINEWORK_REFERENCE_PROMPT}",
        "seed": seed,
        "steps": args.steps,
        "size": args.size,
        "true_cfg_scale": args.true_cfg_scale,
        "output": args.output_dir.resolve() / f"{stem}.png",
    }


def generate(plan: dict[str, object], *, allow_download: bool) -> tuple[Image.Image, float]:
    """Generate the scene from text plus Mira's full-body reference and CPU offload."""
    import torch
    from diffusers import QwenImageEditPlusPipeline

    started = time.monotonic()
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not allow_download,
    )
    pipeline.enable_attention_slicing("max")
    pipeline.enable_sequential_cpu_offload()
    size = int(plan["size"])
    image = pipeline(
        image=[
            square_canvas(plan["fullbody"], size),
        ],
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


def write_result(plan: dict[str, object], output: Path, elapsed_seconds: float) -> Path:
    """Write a reproducible record next to the generated scene PNG."""
    result_path = output.with_name(f"{output.stem}-result.json")
    result = {
        "status": "generated",
        "stage": "storyboard_scene_image_guided",
        "scene": plan["scene"],
        "execution_mode": "direct Diffusers; BF16; sequential CPU offload; no ComfyUI server",
        "runtime": runtime_record(),
        "model": {
            "repository": MODEL_ID,
            "dtype": "bfloat16",
            "device_placement": "sequential_cpu_offload",
        },
        "inputs": [
            {
                "role": "Picture 1: Mira full-body outfit reference",
                "path": str(plan["fullbody"]),
                "sha256": sha256(plan["fullbody"]),
            },
        ],
        "reference_order": "mira-fullbody-outfit",
        "scene_prompt": plan["scene_prompt"],
        "mira_linework_reference_prompt": plan["mira_linework_reference_prompt"],
        "prompt": plan["prompt"],
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
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result_path


def main() -> None:
    """Generate one image-guided scene or print its exact input contract."""
    args = parse_args()
    plan = build_plan(args)
    if args.dry_run:
        printable_plan = {key: str(value) if isinstance(value, Path) else value for key, value in plan.items()}
        print(json.dumps({
            "status": "planned",
            "execution_mode": "direct Diffusers; BF16; sequential CPU offload; no ComfyUI server",
            "model": MODEL_ID,
            "reference_order": "Picture 1 Mira outfit",
            **printable_plan,
        }, ensure_ascii=False, indent=2))
        return

    output = plan["output"]
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite prior output: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    image, elapsed_seconds = generate(plan, allow_download=args.allow_download)
    image.save(output)
    result_path = write_result(plan, output, elapsed_seconds)
    print(json.dumps({"output": str(output), "result": str(result_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

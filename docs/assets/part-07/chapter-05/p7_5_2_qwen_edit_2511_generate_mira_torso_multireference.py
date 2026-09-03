#!/usr/bin/env python3
"""Generate a Mira torso reference or its 1280px multi-angle variants.

The ``torso-reference`` stage takes Mira's face as Picture 1 and the current
frontal torso composition as Picture 2.  It produces the frontal torso basis.
The ``multi-angle`` stage then takes that torso as Picture 1 and Mira's face
as Picture 2. It loads the Multiple-Angles LoRA and gives that adapter only
its ``<sks> [azimuth] [elevation] [distance]`` camera contract.

The runner calls Diffusers directly.  It does not start a ComfyUI server.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
import time
from pathlib import Path

from PIL import Image


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
ANGLE_LORA_ID = "fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA"
ANGLE_LORA_FILENAME = "qwen-image-edit-2511-multiple-angles-lora.safetensors"
DEFAULT_HEAD = ASSETS / (
    "p7-5-2-mira-head-qwen-image-q4ks-comfy-direct-young-adult-v1-"
    "seed-62294-steps-30-size-1280.png"
)
DEFAULT_TORSO = ASSETS / (
    "p7-5-2-qwen-2511-mira-torso-front-identity-framing-neutral-gray-v3-"
    "size-1280x1280-seed-62294-steps-10.png"
)
DEFAULT_TORSO_FRAMING = DEFAULT_TORSO
DEFAULT_IDENTITY_CONTRACT = ASSETS / "p7-5-2-mira-identity-contract.json"
VIEWS = {
    "front": "front view",
    "front-left-quarter": "front-left quarter view",
    "left-profile": "left side profile view",
    "front-right-quarter": "front-right quarter view",
    "right-profile": "right side profile view",
}
CAMERA_ELEVATIONS = ("low-angle shot", "eye-level shot", "elevated shot", "high-angle shot")
CAMERA_DISTANCES = ("close-up", "medium shot", "wide shot")

def sha256(path: Path) -> str:
    """Return a stable content digest for a result record."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def runtime_record() -> dict[str, object]:
    """Record the local package versions that affect image generation."""
    packages: dict[str, str] = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
    }


def square_canvas(path: Path, size: int) -> Image.Image:
    """Pad instead of stretching each reference before multi-image editing."""
    with Image.open(path) as source:
        source = source.convert("RGBA")
        source.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - source.width) // 2, (size - source.height) // 2)
        canvas.alpha_composite(source, offset)
    return canvas.convert("RGB")


def load_inner_top_identity(path: Path) -> str:
    """Read torso-visible clothing from the shared Mira identity contract."""
    contract = json.loads(path.read_text(encoding="utf-8"))
    value = contract.get("inner_top_identity")
    if not isinstance(value, dict):
        raise ValueError("identity contract needs inner_top_identity")
    color = value.get("color")
    if not isinstance(color, dict):
        raise ValueError("inner_top_identity needs a color object")
    fields = ("garment", "fit", "neckline", "sleeves", "hem")
    if any(not isinstance(value.get(field), str) or not value[field].strip() for field in fields):
        raise ValueError("inner_top_identity is missing a garment, fit, neckline, sleeves, or hem")
    color_name = color.get("name")
    if not isinstance(color_name, str) or not color_name.strip():
        raise ValueError("inner_top_identity color needs a name")
    return (
        f"a {value['fit'].strip()} {color_name.strip()} {value['garment'].strip()} "
        f"with a {value['neckline'].strip()} neckline and {value['sleeves'].strip()} sleeves, "
        f"ending {value['hem'].strip()}."
    )


def torso_reference_prompt(inner_top_identity: str) -> str:
    """Make a frontal torso from face identity and framing-only references."""
    return (
        "Picture 1 is Mira's face identity. Picture 2 is only frontal "
        "head-and-upper-torso framing. Generate one frontal torso reference of Mira. "
        f"Preserve her amber eyes, petrol-teal bob, and {inner_top_identity} "
        "Plain warm off-white background."
    )


def multiview_prompt(view: str, elevation: str, distance: str, use_angle_lora: bool) -> str:
    """Use LoRA tokens only when the Multiple-Angles adapter is loaded."""
    if use_angle_lora:
        return f"<sks> {VIEWS[view]} {elevation} {distance}"
    return f"{elevation} {VIEWS[view]}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("torso-reference", "multi-angle"), default="torso-reference")
    parser.add_argument("--head", type=Path, default=DEFAULT_HEAD, help="Mira front-face identity reference.")
    parser.add_argument("--torso", type=Path, default=DEFAULT_TORSO, help="Frontal torso used as Picture 1 only for --stage multi-angle.")
    parser.add_argument("--torso-framing", type=Path, default=DEFAULT_TORSO_FRAMING, help="Frontal torso composition used as Picture 2 only for --stage torso-reference.")
    parser.add_argument("--identity-contract", type=Path, default=DEFAULT_IDENTITY_CONTRACT, help="Shared Mira identity JSON; supplies the inner-top description.")
    parser.add_argument("--view", choices=tuple(VIEWS), default="front-left-quarter", help="Camera yaw / azimuth for --stage multi-angle.")
    parser.add_argument("--elevation", choices=CAMERA_ELEVATIONS, default="eye-level shot", help="Camera pitch for --stage multi-angle.")
    parser.add_argument("--distance", choices=CAMERA_DISTANCES, default="medium shot", help="Camera distance for --stage multi-angle.")
    parser.add_argument(
        "--no-angle-lora",
        action="store_true",
        help="Do not load the Multiple-Angles LoRA; use the minimal plain-text camera prompt instead.",
    )
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1280, help="Square output edge; must be a multiple of 32.")
    parser.add_argument("--run-label", help="Optional filename suffix. The stage-specific default is used when omitted.")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--allow-download", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.steps < 1:
        parser.error("--steps must be positive")
    if args.size < 32 or args.size % 32:
        parser.error("--size must be a multiple of 32")

    head = args.head.resolve()
    torso = args.torso.resolve()
    torso_framing = args.torso_framing.resolve()
    identity_contract = args.identity_contract.resolve()
    required_paths = (head, torso_framing, identity_contract) if args.stage == "torso-reference" else (torso, head, identity_contract)
    for path in required_paths:
        if not path.is_file():
            raise FileNotFoundError(path)
    inner_top_identity = load_inner_top_identity(identity_contract)
    if args.stage == "torso-reference":
        prompt = torso_reference_prompt(inner_top_identity)
        reference_order = "mira-face_identity, torso-framing"
        image_inputs = [square_canvas(head, args.size), square_canvas(torso_framing, args.size)]
        image_records = [
            {"role": "Picture 1: Mira face and hair identity", "path": str(head), "sha256": sha256(head)},
            {"role": "Picture 2: frontal head-and-chest framing only", "path": str(torso_framing), "sha256": sha256(torso_framing)},
        ]
        view = "front"
        view_prompt = VIEWS[view]
        run_label = args.run_label or "identity-framing-neutral-gray-v3"
    else:
        prompt = multiview_prompt(args.view, args.elevation, args.distance, not args.no_angle_lora)
        reference_order = "torso-inner_top, mira-face_identity"
        image_inputs = [square_canvas(torso, args.size), square_canvas(head, args.size)]
        image_records = [
            {"role": "Picture 1: frontal torso and inner top", "path": str(torso), "sha256": sha256(torso)},
            {"role": "Picture 2: Mira face and hair identity", "path": str(head), "sha256": sha256(head)},
        ]
        view = args.view
        view_prompt = VIEWS[view]
        run_label = args.run_label or "multiview-v1"
    output_dir = args.output_dir.resolve()
    stem = (
        f"p7-5-2-qwen-2511-mira-torso-{view}-{run_label}-"
        f"size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    )
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    plan = {
        "model": MODEL_ID,
        "stage": args.stage,
        "reference_order": reference_order,
        "prompt": prompt,
        "view": view,
        "view_prompt": view_prompt,
        "camera": {
            "azimuth": VIEWS[view],
            "elevation": args.elevation if args.stage == "multi-angle" else None,
            "distance": args.distance if args.stage == "multi-angle" else None,
        },
        "head": str(head),
        "torso": str(torso),
        "torso_framing": str(torso_framing),
        "identity_contract": str(identity_contract),
        "inner_top_identity_description": inner_top_identity,
        "output": str(output),
        "result": str(result),
        "size": [args.size, args.size],
        "seed": args.seed,
        "steps": args.steps,
        "true_cfg_scale": 4.0,
        "angle_lora": (
            {"repository": ANGLE_LORA_ID, "weight": ANGLE_LORA_FILENAME}
            if args.stage == "multi-angle" and not args.no_angle_lora
            else None
        ),
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    import torch
    from diffusers import QwenImageEditPlusPipeline

    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=CACHE_DIR,
        local_files_only=not args.allow_download,
    )
    if args.stage == "multi-angle" and not args.no_angle_lora:
        pipeline.load_lora_weights(
            ANGLE_LORA_ID,
            weight_name=ANGLE_LORA_FILENAME,
            cache_dir=CACHE_DIR,
            local_files_only=not args.allow_download,
        )
    pipeline.enable_sequential_cpu_offload()
    image = pipeline(
        image=image_inputs,
        prompt=prompt,
        height=args.size,
        width=args.size,
        generator=torch.manual_seed(args.seed),
        true_cfg_scale=4.0,
        negative_prompt=" ",
        num_inference_steps=args.steps,
        guidance_scale=1.0,
        num_images_per_prompt=1,
    ).images[0]
    image.save(output)
    record = {
        "status": "generated",
        "stage": "mira_torso_reference_generation" if args.stage == "torso-reference" else "mira_torso_multiview_generation",
        "execution_mode": "direct Diffusers; QwenImageEditPlusPipeline; no ComfyUI server",
        "runtime": runtime_record(),
        "model": {
            "repository": MODEL_ID,
            "dtype": "bfloat16",
            "device_placement": "sequential_cpu_offload",
        },
        "angle_lora": (
            {
                "repository": ANGLE_LORA_ID,
                "weight": ANGLE_LORA_FILENAME,
                "strength": "model-card default",
                "prompt_format": "<sks> [azimuth] [elevation] [distance]",
            }
            if args.stage == "multi-angle" and not args.no_angle_lora
            else None
        ),
        "inputs": [
            *image_records,
            {
                "role": "Mira identity contract: torso-visible inner top",
                "path": str(identity_contract),
                "sha256": sha256(identity_contract),
            },
        ],
        "reference_order": reference_order,
        "view": view,
        "view_prompt": view_prompt,
        "camera": {
            "azimuth": VIEWS[view],
            "elevation": args.elevation if args.stage == "multi-angle" else None,
            "distance": args.distance if args.stage == "multi-angle" else None,
        },
        "identity_contract": str(identity_contract),
        "inner_top_identity_description": inner_top_identity,
        "prompt": prompt,
        "seed": args.seed,
        "steps": args.steps,
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "output": {
            "path": str(output),
            "width": image.width,
            "height": image.height,
            "sha256": sha256(output),
        },
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

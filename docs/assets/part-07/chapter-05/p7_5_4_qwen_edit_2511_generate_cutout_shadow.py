#!/usr/bin/env python3
"""Generate a cast shadow for one A/B/C white-background character cutout.

Qwen creates only the shadow.  The original character pixels are composited
back with the supplied person mask, so the experiment cannot alter the pose,
face, or outfit while sampling the shadow.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import time
from pathlib import Path

from PIL import Image, ImageFilter


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
CUTOUTS = {
    "a": ASSETS / "p7-5-3-character-pose-cutout-white-official-camera-scene-a-v6.png",
    "b": ASSETS / "p7-5-3-character-pose-cutout-white-official-camera-scene-b-v7.png",
    "c": ASSETS / "p7-5-4-character-pose-cutout-white-official-camera-scene-c-v6-size-1280x1280.png",
}
PERSON_MASKS = {
    "a": ASSETS / "p7-5-3-sam2-person-mask-official-camera-scene-a-v6.png",
    "b": ASSETS / "p7-5-4-sam2-person-mask-official-camera-scene-b-v7.png",
    "c": ASSETS / "p7-5-4-sam2-person-mask-official-camera-scene-c-v8.png",
}
DEFAULT_PROMPT = (
    "Picture 1 is a woman airborne above a white floor. Add one soft gray cast "
    "shadow on the floor directly below her. Keep the white background clean. "
    "No additional people, objects, scenery, text, or changes to the woman."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", choices=tuple(CUTOUTS), default="a", help="Select the matching A/B/C cutout and SAM2 person mask.")
    parser.add_argument("--cutout", type=Path, help="Override the selected scene cutout.")
    parser.add_argument("--person-mask", type=Path, help="Override the selected scene mask; white=character pixels restored after Qwen sampling.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--protect-pixels", type=int, default=40, help="Expand the original character mask by this many pixels before restoring it.")
    parser.add_argument("--qwen-candidate", type=Path, help="Reuse a saved Qwen shadow candidate for compositing-only validation.")
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32 or args.protect_pixels < 0:
        parser.error("--steps must be positive, --size a multiple of 32, and --protect-pixels non-negative")
    cutout_path = (args.cutout or CUTOUTS[args.scene]).resolve()
    mask_path = (args.person_mask or PERSON_MASKS[args.scene]).resolve()
    if not cutout_path.is_file() or not mask_path.is_file():
        raise FileNotFoundError("--cutout and --person-mask must exist")

    cutout = Image.open(cutout_path).convert("RGB").resize((args.size, args.size), Image.Resampling.LANCZOS)
    person_mask = Image.open(mask_path).convert("L").resize((args.size, args.size), Image.Resampling.NEAREST)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"p7-5-4-qwen-2511-cutout-shadow-scene-{args.scene}-{args.run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    qwen_shadow, protect_mask_path = output_dir / f"{stem}-qwen.png", output_dir / f"{stem}-protect-mask.png"
    output, result = output_dir / f"{stem}.png", output_dir / f"{stem}-result.json"
    candidate = args.qwen_candidate.resolve() if args.qwen_candidate else None
    if candidate is not None and not candidate.is_file():
        raise FileNotFoundError(candidate)

    started = time.monotonic()
    if candidate is None:
        import torch
        from diffusers import QwenImageEditPlusPipeline

        pipeline = QwenImageEditPlusPipeline.from_pretrained(
            MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR, local_files_only=True
        )
        pipeline.enable_attention_slicing("max")
        pipeline.enable_sequential_cpu_offload()
        try:
            shadowed = pipeline(
                image=[cutout], prompt=args.prompt, height=args.size, width=args.size,
                generator=torch.Generator("cpu").manual_seed(args.seed), true_cfg_scale=4.0,
                guidance_scale=1.0, negative_prompt=" ", num_inference_steps=args.steps,
                num_images_per_prompt=1,
            ).images[0].convert("RGB")
        finally:
            del pipeline
            torch.cuda.empty_cache()
        shadowed.save(qwen_shadow)
    else:
        shadowed = Image.open(candidate).convert("RGB").resize((args.size, args.size), Image.Resampling.LANCZOS)
        qwen_shadow = candidate

    # Qwen can extend limbs outside the exact segmentation boundary.  Restoring
    # a white buffer around the original person removes those residual pixels
    # while leaving the detached floor shadow available outside the buffer.
    kernel = args.protect_pixels * 2 + 1
    protect_mask = person_mask.filter(ImageFilter.MaxFilter(kernel)) if kernel > 1 else person_mask
    protect_mask.save(protect_mask_path)
    Image.composite(cutout, shadowed, protect_mask).save(output)
    result.write_text(
        json.dumps(
            {
                "status": "generated", "stage": "qwen_cutout_cast_shadow", "scene": args.scene, "model": MODEL_ID,
                "inputs": {
                    "cutout": {"path": str(cutout_path), "sha256": sha256(cutout_path), "role": "Picture 1"},
                    "person_mask": {"path": str(mask_path), "sha256": sha256(mask_path), "semantics": "white=hard-restored source character"},
                },
                "prompt": args.prompt, "seed": args.seed, "steps": args.steps, "true_cfg_scale": 4.0,
                "outputs": {
                    "qwen_shadow_candidate": {"path": str(qwen_shadow), "sha256": sha256(qwen_shadow), "reused": candidate is not None},
                    "expanded_character_protection_mask": {"path": str(protect_mask_path), "sha256": sha256(protect_mask_path), "pixels": args.protect_pixels},
                    "character_restored_shadow_cutout": {"path": str(output), "sha256": sha256(output)},
                },
                "runtime": {name: importlib.metadata.version(name) for name in ("diffusers", "torch", "transformers", "accelerate")},
                "elapsed_seconds": round(time.monotonic() - started, 2),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

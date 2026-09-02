#!/usr/bin/env python3
"""Generate a cast shadow for one A/B/C white-background character cutout.

Qwen creates only the shadow.  The original character pixels are composited
back with the supplied person mask, so the experiment cannot alter the pose,
face, or outfit while sampling the shadow.  Scene C may also receive its
source scene as Picture 2 to preserve the scene's body-to-shadow separation.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import time
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
CUTOUTS = {
    "a": ASSETS / "p7-5-3-character-pose-cutout-white-official-camera-scene-a-v6.png",
    "b": ASSETS / "p7-5-3-character-pose-cutout-white-official-camera-scene-b-v7.png",
    "c": ASSETS / "p7-5-4-character-pose-cutout-white-official-camera-scene-c-no-closeup-v9-size-1280x1280.png",
}
PERSON_MASKS = {
    "a": ASSETS / "p7-5-3-sam2-person-mask-official-camera-scene-a-v6.png",
    "b": ASSETS / "p7-5-4-sam2-person-mask-official-camera-scene-b-v7.png",
    "c": ASSETS / "p7-5-4-sam2-person-mask-official-camera-scene-c-no-closeup-v9.png",
}
SCENE_REFERENCES: dict[str, Path] = {
    "c": ASSETS / "p7-5-3-qwen-2511-camera-front-left-quarter-view-low-angle-shot-no-closeup-v7-seed-5420-steps-20.png",
}
DEFAULT_PROMPT = (
    "Picture 1 is a woman airborne above a white floor. Add one soft gray cast "
    "shadow on the floor directly below her. Keep the white background clean. "
    "No additional people, objects, scenery, text, or changes to the woman."
)
SCENE_REFERENCE_PROMPT = (
    "Picture 1 is a woman airborne above a white floor. Picture 2 is the source "
    "scene. Add one soft gray cast shadow on the white floor directly below the woman. "
    "Match only the vertical separation between the woman and her floor shadow in Picture 2. "
    "Keep the white background clean. No additional people, objects, scenery, text, "
    "or changes to the woman."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", choices=tuple(CUTOUTS), default="a", help="Select the matching A/B/C cutout and SAM2 person mask.")
    parser.add_argument("--cutout", type=Path, help="Override the selected scene cutout.")
    parser.add_argument("--person-mask", type=Path, help="Override the selected scene mask; white=character pixels restored after Qwen sampling.")
    parser.add_argument("--scene-reference", type=Path, help="Optional Picture 2 source scene used only to match body-to-shadow separation.")
    parser.add_argument("--prompt", help="Override the scene-aware shadow prompt.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--protect-pixels", type=int, default=40, help="Expand the original character mask by this many pixels before restoring it.")
    parser.add_argument("--shadow-min-y", type=int, help="Keep only sampled shadow pixels at or below this y coordinate; Scene C defaults to 900 when its source scene is used.")
    parser.add_argument("--qwen-candidate", type=Path, help="Reuse a saved Qwen shadow candidate for compositing-only validation.")
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    protect_pixels = args.protect_pixels
    if args.steps < 1 or args.size < 32 or args.size % 32 or protect_pixels < 0:
        parser.error("--steps must be positive, --size a multiple of 32, and --protect-pixels non-negative")
    cutout_path = (args.cutout or CUTOUTS[args.scene]).resolve()
    mask_path = (args.person_mask or PERSON_MASKS[args.scene]).resolve()
    if not cutout_path.is_file() or not mask_path.is_file():
        raise FileNotFoundError("--cutout and --person-mask must exist")
    scene_reference_path = (args.scene_reference or SCENE_REFERENCES.get(args.scene))
    scene_reference_path = scene_reference_path.resolve() if scene_reference_path else None
    if scene_reference_path is not None and not scene_reference_path.is_file():
        raise FileNotFoundError(scene_reference_path)
    prompt = args.prompt or (SCENE_REFERENCE_PROMPT if scene_reference_path else DEFAULT_PROMPT)
    shadow_min_y = args.shadow_min_y if args.shadow_min_y is not None else (900 if args.scene == "c" and scene_reference_path else None)
    if shadow_min_y is not None and not 0 <= shadow_min_y < args.size:
        parser.error("--shadow-min-y must be within the output canvas")

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
            reference_images = [cutout]
            if scene_reference_path is not None:
                reference_images.append(
                    Image.open(scene_reference_path).convert("RGB").resize((args.size, args.size), Image.Resampling.LANCZOS)
                )
            shadowed = pipeline(
                image=reference_images, prompt=prompt, height=args.size, width=args.size,
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
    kernel = protect_pixels * 2 + 1
    protect_mask = person_mask.filter(ImageFilter.MaxFilter(kernel)) if kernel > 1 else person_mask
    protect_mask.save(protect_mask_path)
    if shadow_min_y is None:
        output_image = Image.composite(cutout, shadowed, protect_mask)
    else:
        # Picture 2 can make Qwen redraw limbs outside the person mask.  For C,
        # retain only the detached lower-floor shadow and restore all character
        # pixels directly from the original cutout.
        output_image = cutout.copy()
        shadow_alpha = ImageOps.invert(shadowed.convert("L")).point(
            lambda value: min(255, max(0, (value - 10) * 8))
        )
        shadow_alpha.paste(0, (0, 0, args.size, shadow_min_y))
        output_image.paste(shadowed, mask=shadow_alpha)
    output_image.save(output)
    result.write_text(
        json.dumps(
            {
                "status": "generated", "stage": "qwen_cutout_cast_shadow", "scene": args.scene, "model": MODEL_ID,
                "inputs": {
                    "cutout": {"path": str(cutout_path), "sha256": sha256(cutout_path), "role": "Picture 1"},
                    "person_mask": {"path": str(mask_path), "sha256": sha256(mask_path), "semantics": "white=hard-restored source character"},
                    "scene_reference": (
                        {"path": str(scene_reference_path), "sha256": sha256(scene_reference_path), "role": "Picture 2: body-to-shadow separation only"}
                        if scene_reference_path is not None else None
                    ),
                },
                "prompt": prompt, "seed": args.seed, "steps": args.steps, "true_cfg_scale": 4.0,
                "outputs": {
                    "qwen_shadow_candidate": {"path": str(qwen_shadow), "sha256": sha256(qwen_shadow), "reused": candidate is not None},
                    "expanded_character_protection_mask": {"path": str(protect_mask_path), "sha256": sha256(protect_mask_path), "pixels": protect_pixels},
                    "shadow_min_y": shadow_min_y,
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

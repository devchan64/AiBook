#!/usr/bin/env python3
"""Composite DeLight background and character with Qwen Edit 2511 references.

Picture 1 is the character-free coastal plate.  Picture 2 is the DeLight
character.  This intentionally does not provide a mask: Qwen receives the
two image roles directly and creates one integrated scene.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import time
from pathlib import Path

from PIL import Image


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
MODEL_ID = "Qwen/Qwen-Image-Edit-2511"
SCENE_CONFIG = {
    "a": {"background": "p7-5-4-qwen-2509-studio-delight-camera-a-background-v1-size-1280x1280-seed-62294-steps-10.png", "character": "p7-5-4-qwen-2511-bfs-head-v5-delight-character-cutout-a-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png", "place": "coastal"},
    "b": {"background": "p7-5-4-qwen-2509-studio-delight-background-b-size-1280x1280-seed-62294-steps-10.png", "character": "p7-5-4-qwen-2511-bfs-head-v5-delight-character-cutout-b-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png", "place": "wildflower meadow"},
    "c": {"background": "p7-5-4-qwen-2509-studio-delight-background-c-size-1280x1280-seed-62294-steps-10.png", "character": "p7-5-4-qwen-2511-bfs-head-v5-delight-character-cutout-c-quarter-left-v1-size-1280x1280-seed-62294-steps-10.png", "place": "city park"},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def square(path: Path, size: int) -> Image.Image:
    """Use equal RGB canvases without distorting the two references."""
    with Image.open(path) as source:
        source = source.convert("RGB")
        if source.size != (size, size):
            source = source.resize((size, size), Image.Resampling.LANCZOS)
        return source.copy()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene-id", choices=tuple(SCENE_CONFIG), default="c")
    parser.add_argument("--background", type=Path, help="Override the Scene's character-free DeLight background.")
    parser.add_argument("--character", type=Path, help="Override the Scene's BFS-refined DeLight character.")
    parser.add_argument("--prompt", help="Override the scene-aware positive integration prompt.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--run-label", help="Defaults to the selected Scene's BFS 45-degree integration label.")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32:
        parser.error("--steps must be positive and --size must be a positive multiple of 32")
    config = SCENE_CONFIG[args.scene_id]
    background = (args.background or ASSETS / config["background"]).resolve()
    character = (args.character or ASSETS / config["character"]).resolve()
    prompt = args.prompt or f"Place the woman in Picture 2 into Picture 1. Preserve the {config['place']} background and composition of Picture 1. Preserve the split-leap pose, identity, and outfit of the woman in Picture 2."
    run_label = args.run_label or f"scene-{args.scene_id}-bfs-quarter-left-v1"
    for path in (background, character):
        if not path.is_file():
            raise FileNotFoundError(path)
    output_dir = args.output_dir.resolve()
    stem = f"p7-5-4-qwen-2511-delight-multireference-composite-{run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    output, result = output_dir / f"{stem}.png", output_dir / f"{stem}-result.json"
    if args.dry_run:
        print(json.dumps({"scene_id": args.scene_id, "background": str(background), "character": str(character), "prompt": prompt, "output": str(output), "result": str(result)}, ensure_ascii=False))
        return

    import torch
    from diffusers import QwenImageEditPlusPipeline

    started = time.monotonic()
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR, local_files_only=True
    )
    pipeline.enable_attention_slicing("max")
    pipeline.enable_sequential_cpu_offload()
    try:
        image = pipeline(
            image=[square(background, args.size), square(character, args.size)],
            prompt=prompt,
            width=args.size,
            height=args.size,
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=4.0,
            guidance_scale=1.0,
            negative_prompt=" ",
            num_inference_steps=args.steps,
        ).images[0].convert("RGB")
    finally:
        del pipeline
        torch.cuda.empty_cache()
    output_dir.mkdir(parents=True, exist_ok=True)
    image.save(output)
    result.write_text(
        json.dumps(
            {
                "status": "generated",
                "stage": "delight_multireference_composite",
                "execution_mode": "direct Diffusers; Qwen Image Edit 2511; no mask; no ComfyUI",
                "model": MODEL_ID,
                "inputs": [
                    {"role": "Picture 1: DeLight character-free background", "path": str(background), "sha256": sha256(background)},
                    {"role": "Picture 2: DeLight character identity, pose, and outfit", "path": str(character), "sha256": sha256(character)},
                ],
                "scene_id": args.scene_id,
                "prompt": prompt,
                "seed": args.seed,
                "steps": args.steps,
                "true_cfg_scale": 4.0,
                "output": {"path": str(output), "sha256": sha256(output), "width": image.width, "height": image.height},
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

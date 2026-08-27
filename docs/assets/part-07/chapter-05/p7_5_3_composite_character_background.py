#!/usr/bin/env python3
"""Composite a generated character over the Scene A background with a SAM2 mask."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageFilter


ASSETS = Path(__file__).resolve().parent
DEFAULT_CHARACTER = ASSETS / "p7-5-3-qwen-2509-pose-transfer-plus90-replace-v2-seed-62294-steps-10.png"
DEFAULT_MASK = ASSETS / "p7-5-3-sam2-person-mask-pose-transfer-plus90-replace-v2.png"
DEFAULT_BACKGROUND = ASSETS / "p7-5-3-lama-background-scene-a-v3.png"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def asset_record(path: Path, role: str) -> dict[str, str]:
    return {"path": str(path), "sha256": sha256(path), "role": role}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--character", type=Path, default=DEFAULT_CHARACTER)
    parser.add_argument("--mask", type=Path, default=DEFAULT_MASK, help="White=character; black=background.")
    parser.add_argument("--background", type=Path, default=DEFAULT_BACKGROUND)
    parser.add_argument("--feather", type=float, default=0.8, help="Alpha-edge blur in pixels; use 0 for a hard edge.")
    parser.add_argument("--run-label", default="scene-a-v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    character, mask, background = args.character.resolve(), args.mask.resolve(), args.background.resolve()
    if args.feather < 0:
        parser.error("--feather must be non-negative")
    for path in (character, mask, background):
        if not path.is_file():
            raise FileNotFoundError(path)

    character_image = Image.open(character).convert("RGBA")
    background_image = Image.open(background).convert("RGBA")
    alpha = Image.open(mask).convert("L")
    if background_image.size != character_image.size:
        background_image = background_image.resize(character_image.size, Image.Resampling.LANCZOS)
    if alpha.size != character_image.size:
        alpha = alpha.resize(character_image.size, Image.Resampling.NEAREST)
    if args.feather:
        alpha = alpha.filter(ImageFilter.GaussianBlur(args.feather))
    character_image.putalpha(alpha)
    composite = Image.alpha_composite(background_image, character_image).convert("RGB")

    stem = f"p7-5-3-character-background-composite-{args.run_label}"
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output, result = output_dir / f"{stem}.png", output_dir / f"{stem}-result.json"
    composite.save(output)
    result.write_text(
        json.dumps(
            {
                "status": "generated",
                "stage": "character_background_composite",
                "inputs": [
                    asset_record(character, "generated character"),
                    asset_record(mask, "SAM2 alpha mask; white=character"),
                    asset_record(background, "Scene A background plate"),
                ],
                "feather_pixels": args.feather,
                "output": asset_record(output, "alpha composite"),
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

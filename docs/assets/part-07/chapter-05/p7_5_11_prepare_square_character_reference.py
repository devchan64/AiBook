#!/usr/bin/env python3
"""Letterbox a vertical character reference for the P7-5.11 aspect-ratio ablation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ASSET_DIR = Path(__file__).resolve().parent
SOURCE = ASSET_DIR / "p7-5-2-fullbody-front-refined-reference.png"
OUTPUT = ASSET_DIR / "p7-5-11-character-fullbody-front-square-padded.png"
RECORD = ASSET_DIR / "p7-5-11-character-fullbody-front-square-padded.json"
CANVAS_SIZE = 1152
BACKGROUND = (247, 245, 239)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = Image.open(SOURCE).convert("RGB")
    scale = min(CANVAS_SIZE / source.width, CANVAS_SIZE / source.height)
    resized = source.resize(
        (round(source.width * scale), round(source.height * scale)), Image.Resampling.LANCZOS
    )
    canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), BACKGROUND)
    offset = ((CANVAS_SIZE - resized.width) // 2, (CANVAS_SIZE - resized.height) // 2)
    canvas.paste(resized, offset)
    canvas.save(OUTPUT)
    RECORD.write_text(
        json.dumps(
            {
                "purpose": "P7-5.11 Qwen A-scene aspect-ratio ablation input",
                "source": {"path": str(SOURCE), "size": list(source.size), "sha256": sha256(SOURCE)},
                "transform": {
                    "type": "fit_inside_with_horizontal_padding",
                    "canvas_size": [CANVAS_SIZE, CANVAS_SIZE],
                    "resized_size": list(resized.size),
                    "offset": list(offset),
                    "background_rgb": list(BACKGROUND),
                    "crop": "none",
                    "geometric_distortion": "none",
                },
                "output": {"path": str(OUTPUT), "size": list(canvas.size), "sha256": sha256(OUTPUT)},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()

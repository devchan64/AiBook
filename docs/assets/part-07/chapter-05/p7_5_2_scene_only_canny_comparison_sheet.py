#!/usr/bin/env python3
"""Assemble a same-adapter full-Canny versus scene-only-Canny comparison."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def panel(sheet: Image.Image, column: int) -> Image.Image:
    width = sheet.width // 3
    return sheet.crop((column * width, 24, (column + 1) * width, sheet.height))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("full_035", type=Path)
    parser.add_argument("full_075", type=Path)
    parser.add_argument("scene_only", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    full_035 = Image.open(args.full_035).convert("RGB")
    full_075 = Image.open(args.full_075).convert("RGB")
    scene = Image.open(args.scene_only).convert("RGB")
    width = full_035.width // 3
    height = full_035.height - 24
    scene_width = scene.width // 5
    if (scene_width, height) != panel(full_035, 0).size:
        raise ValueError("input sheets do not use the same panel dimensions")
    panels = (
        ("Full Canny", panel(full_035, 0)),
        ("Scene-only Canny", scene.crop((scene_width, 24, scene_width * 2, scene.height))),
        ("LoRA only", panel(full_035, 1)),
        ("Full Canny 0.35", panel(full_035, 2)),
        ("Scene-only 0.35", scene.crop((scene_width * 3, 24, scene_width * 4, scene.height))),
        ("Full Canny 0.75", panel(full_075, 2)),
        ("Scene-only 0.75", scene.crop((scene_width * 4, 24, scene_width * 5, scene.height))),
    )
    contact = Image.new("RGB", (width * len(panels), height + 24), "white")
    draw = ImageDraw.Draw(contact)
    for index, (label, image) in enumerate(panels):
        left = index * width
        draw.text((left + 6, 5), label, fill="black")
        contact.paste(image, (left, 24))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    contact.save(args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

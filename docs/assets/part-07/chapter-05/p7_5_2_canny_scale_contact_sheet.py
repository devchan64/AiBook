#!/usr/bin/env python3
"""Assemble one fixed-seed Canny-strength comparison contact sheet."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def panel(sheet: Image.Image, column: int) -> Image.Image:
    width = sheet.width // 3
    return sheet.crop((column * width, 24, (column + 1) * width, sheet.height))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scale_010", type=Path)
    parser.add_argument("scale_035", type=Path)
    parser.add_argument("scale_075", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    sheets = [Image.open(path).convert("RGB") for path in (args.scale_010, args.scale_035, args.scale_075)]
    control = panel(sheets[0], 0)
    baseline = panel(sheets[0], 1)
    conditioned = [panel(sheet, 2) for sheet in sheets]
    width, height = control.size
    contact = Image.new("RGB", (width * 5, height + 24), "white")
    draw = ImageDraw.Draw(contact)
    labels = ("Canny input", "LoRA only", "Canny 0.10", "Canny 0.35", "Canny 0.75")
    for index, (label, image) in enumerate(zip(labels, (control, baseline, *conditioned))):
        left = index * width
        draw.text((left + 6, 5), label, fill="black")
        contact.paste(image, (left, 24))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    contact.save(args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

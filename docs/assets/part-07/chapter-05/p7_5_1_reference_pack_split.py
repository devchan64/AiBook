#!/usr/bin/env python3
"""Inspect one reference image without cropping, splitting, or rewriting it."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--minimum-side", type=int, default=512)
    args = parser.parse_args()

    with Image.open(args.image) as image:
        width, height = image.size
        mode = image.mode

    if min(width, height) < args.minimum_side:
        raise ValueError(
            f"{args.image} is {width}x{height}; each side must be at least "
            f"{args.minimum_side}px"
        )
    if height <= width:
        raise ValueError("single-image character references must use portrait framing")

    print(f"file: {args.image}")
    print(f"size: {width}x{height}")
    print(f"mode: {mode}")
    print("PASS image dimensions only; human review must approve identity and bag details")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

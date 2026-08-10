#!/usr/bin/env python3
"""Create a coarse operator-defined jacket mask for a fixed preflight input.

This mask is intentionally limited to the upper-body jacket area. It is not a
production mask and must not be reused for a P7-5.3 panel with a different pose.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--mode",
        choices=("wide", "jacket-shell", "fitted-shell"),
        default="wide",
        help="wide is the original coarse preflight; jacket-shell preserves the inner crop top",
    )
    parser.add_argument(
        "--expand-px",
        type=int,
        default=0,
        help="dilate the editable jacket region after drawing it",
    )
    args = parser.parse_args()
    if args.expand_px < 0:
        raise ValueError("--expand-px must be zero or positive")
    source = Image.open(args.input).convert("RGB")
    width, height = source.size
    mask = Image.new("L", source.size, 0)
    draw = ImageDraw.Draw(mask)
    if args.mode == "wide":
        # Coarse torso-and-sleeves preflight; face, trousers, shoes, and floor remain black.
        draw.polygon(
            [(int(width * x), int(height * y)) for x, y in ((0.27, 0.225), (0.73, 0.225), (0.70, 0.405), (0.64, 0.425), (0.36, 0.425), (0.30, 0.405))],
            fill=255,
        )
        for points in (
            ((0.27, 0.24), (0.18, 0.28), (0.17, 0.45), (0.25, 0.49), (0.33, 0.40)),
            ((0.73, 0.24), (0.82, 0.28), (0.83, 0.45), (0.75, 0.49), (0.67, 0.40)),
        ):
            draw.polygon([(int(width * x), int(height * y)) for x, y in points], fill=255)
    elif args.mode == "jacket-shell":
        # Target jacket shell: left/right panels and long sleeves are editable,
        # while the center charcoal crop top remains black and must be preserved.
        panels = (
            ((0.31, 0.205), (0.47, 0.195), (0.50, 0.245), (0.47, 0.370), (0.40, 0.385), (0.34, 0.345), (0.30, 0.270)),
            ((0.69, 0.205), (0.53, 0.195), (0.50, 0.245), (0.53, 0.370), (0.60, 0.385), (0.66, 0.345), (0.70, 0.270)),
            ((0.32, 0.215), (0.27, 0.250), (0.29, 0.380), (0.285, 0.515), (0.32, 0.550), (0.37, 0.515), (0.375, 0.365)),
            ((0.68, 0.215), (0.73, 0.250), (0.71, 0.380), (0.715, 0.515), (0.68, 0.550), (0.63, 0.515), (0.625, 0.365)),
        )
        for points in panels:
            draw.polygon([(int(width * x), int(height * y)) for x, y in points], fill=255)
    else:
        # Hand-traced target shell for this fixed front reference. The dense
        # contours follow its visible shoulders, arms, wrists, crop-top opening,
        # and high jacket hem instead of approximating the upper body as a box.
        panels = (
            (
                (0.357, 0.202), (0.400, 0.194), (0.443, 0.195), (0.468, 0.218),
                (0.488, 0.260), (0.484, 0.317), (0.476, 0.359), (0.467, 0.375),
                (0.430, 0.371), (0.394, 0.360), (0.365, 0.342), (0.347, 0.305),
                (0.338, 0.255),
            ),
            (
                (0.643, 0.202), (0.600, 0.194), (0.557, 0.195), (0.532, 0.218),
                (0.512, 0.260), (0.516, 0.317), (0.524, 0.359), (0.533, 0.375),
                (0.570, 0.371), (0.606, 0.360), (0.635, 0.342), (0.653, 0.305),
                (0.662, 0.255),
            ),
            (
                (0.348, 0.216), (0.319, 0.231), (0.303, 0.257), (0.309, 0.290),
                (0.324, 0.332), (0.324, 0.389), (0.316, 0.448), (0.306, 0.505),
                (0.306, 0.538), (0.321, 0.558), (0.342, 0.553), (0.358, 0.531),
                (0.370, 0.496), (0.375, 0.440), (0.375, 0.383), (0.386, 0.337),
            ),
            (
                (0.652, 0.216), (0.681, 0.231), (0.697, 0.257), (0.691, 0.290),
                (0.676, 0.332), (0.676, 0.389), (0.684, 0.448), (0.694, 0.505),
                (0.694, 0.538), (0.679, 0.558), (0.658, 0.553), (0.642, 0.531),
                (0.630, 0.496), (0.625, 0.440), (0.625, 0.383), (0.614, 0.337),
            ),
        )
        for points in panels:
            draw.polygon([(int(width * x), int(height * y)) for x, y in points], fill=255)
    if args.expand_px:
        mask = mask.filter(ImageFilter.MaxFilter(args.expand_px * 2 + 1))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    mask.save(args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

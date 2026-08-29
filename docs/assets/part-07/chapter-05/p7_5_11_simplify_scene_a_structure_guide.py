"""Create a low-detail, identity-free Scene A guide for Qwen Edit.

The approved depth map is a valid storyboard record, but it contains many
continuous canyon-depth gradients.  This derivative preserves only the
large-scale wall/ground separation and the approved airborne silhouette, so
the second Qwen image slot is less likely to compete with the character
reference for fine visual detail.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "docs/assets/part-07/chapter-05/p7-5-3-scene-a-approved-storyboard-depth.png"
OUTPUT = ROOT / "docs/assets/part-07/chapter-05/p7-5-11-scene-a-simplified-structure-guide.png"


def simplify(source: Image.Image, coarse_size: int, levels: int) -> Image.Image:
    """Keep broad depth regions while suppressing local texture cues."""
    gray = ImageOps.grayscale(source)
    coarse = gray.resize((coarse_size, coarse_size), Image.Resampling.BILINEAR)
    smooth = coarse.resize(gray.size, Image.Resampling.BICUBIC)
    step = 255 / (levels - 1)
    quantized = smooth.point(lambda value: round(value / step) * step)
    # Preserve only the central airborne figure.  A connected-component mask
    # avoids promoting the bright foreground walls and floor to the figure.
    values = np.asarray(gray)
    component_count, labels, stats, centers = cv2.connectedComponentsWithStats(
        (values > 150).astype(np.uint8), connectivity=8
    )
    figure = np.zeros(values.shape, dtype=bool)
    for label in range(1, component_count):
        x, y, width, height, area = stats[label]
        cx, cy = centers[label]
        if area >= 800 and 220 <= cx <= 850 and 250 <= cy <= 740 and x >= 200 and y >= 240:
            figure |= labels == label
    figure = cv2.morphologyEx(
        figure.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))
    ).astype(bool)
    # The depth map divides the head into shallow sub-regions; make it one
    # silhouette instead of asking the edit model to interpret facial depth.
    head = np.zeros(values.shape, dtype=np.uint8)
    cv2.ellipse(head, (550, 321), (43, 60), 0, 0, 360, 1, thickness=-1)
    figure |= head.astype(bool)
    return Image.fromarray(np.where(figure, 242, np.asarray(quantized)).astype(np.uint8)).convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coarse-size", type=int, default=48)
    parser.add_argument("--levels", type=int, default=5)
    args = parser.parse_args()
    if args.coarse_size < 8 or args.levels < 2:
        raise ValueError("--coarse-size must be >= 8 and --levels must be >= 2")
    source = Image.open(SOURCE).convert("RGB")
    result = simplify(source, args.coarse_size, args.levels)
    result.save(OUTPUT)
    OUTPUT.with_suffix(".json").write_text(
        json.dumps(
            {
                "source": str(SOURCE),
                "purpose": "low-detail, identity-free Qwen Edit structure guide",
                "coarse_size": args.coarse_size,
                "depth_levels": args.levels,
                "retained": ["canyon-wall masses", "ground perspective", "airborne split silhouette"],
                "removed": ["continuous local canyon-depth texture"],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()

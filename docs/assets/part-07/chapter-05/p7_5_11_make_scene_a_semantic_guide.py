"""Derive a neutral, illustrated Scene A guide from the approved depth map only.

This is intentionally not an RGB storyboard or a prior Qwen output.  It
retains the low-angle canyon masses, ground recession, and airborne split
silhouette while supplying the broad watercolor-like color and contour cues
that a raw depth map cannot express.
"""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "docs/assets/part-07/chapter-05/p7-5-3-scene-a-approved-storyboard-depth.png"
OUTPUT = ROOT / "docs/assets/part-07/chapter-05/p7-5-11-scene-a-depth-derived-semantic-guide.png"


def figure_mask(values: np.ndarray) -> np.ndarray:
    count, labels, stats, centers = cv2.connectedComponentsWithStats((values > 150).astype(np.uint8), connectivity=8)
    mask = np.zeros(values.shape, dtype=np.uint8)
    for label in range(1, count):
        x, y, width, height, area = stats[label]
        cx, cy = centers[label]
        if area >= 800 and 220 <= cx <= 850 and 250 <= cy <= 740 and x >= 200 and y >= 240:
            mask[labels == label] = 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
    cv2.ellipse(mask, (550, 321), (43, 60), 0, 0, 360, 255, thickness=-1)
    return mask


def main() -> None:
    source = Image.open(SOURCE).convert("L")
    values = np.asarray(source)
    coarse = np.asarray(source.resize((48, 48), Image.Resampling.BILINEAR).resize(source.size, Image.Resampling.BICUBIC))
    bins = np.digitize(coarse, bins=(52, 104, 156, 208))
    palette = np.array(
        [
            (117, 82, 66),   # distant shadowed canyon opening
            (166, 119, 92),
            (205, 156, 116),
            (232, 193, 150),
            (247, 232, 204), # near floor and sky paper
        ],
        dtype=np.uint8,
    )
    canvas = palette[bins]
    mask = figure_mask(values)
    canvas[mask > 0] = (222, 225, 220)  # deliberately identity- and outfit-neutral
    edges = cv2.Canny(coarse, 18, 48)
    edges = cv2.dilate(edges, np.ones((2, 2), dtype=np.uint8), iterations=1)
    canvas[edges > 0] = (105, 83, 72)
    # Reassert the neutral figure above background contours while retaining a thin outline.
    interior = cv2.erode(mask, np.ones((3, 3), dtype=np.uint8), iterations=1)
    canvas[interior > 0] = (222, 225, 220)
    outline = cv2.dilate(mask, np.ones((5, 5), dtype=np.uint8), iterations=1) & ~cv2.erode(mask, np.ones((5, 5), dtype=np.uint8), iterations=1)
    canvas[outline > 0] = (88, 77, 72)
    Image.fromarray(canvas, "RGB").save(OUTPUT)
    OUTPUT.with_suffix(".json").write_text(
        json.dumps(
            {
                "source": str(SOURCE),
                "derivation": "deterministic depth quantization, contour extraction, and neutral silhouette masking",
                "retained": ["low-angle canyon masses", "ground recession", "airborne split silhouette"],
                "excluded": ["storyboard RGB", "prior generated output", "character identity", "outfit identity"],
                "input_role": "Qwen image 1 semantic composition guide",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Make a review-only 10/20/30-step contact sheet for a fixed Qwen run."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


ASSETS = Path(__file__).resolve().parent
DEFAULT_CANDIDATES = ASSETS / "p7-5-2-qwen-edit-candidates"
STEPS = (10, 20, 30)
LABELS = {
    10: "10 steps · v93",
    20: "20 steps · v94",
    30: "30 steps · v95",
}


def candidate_path(candidates: Path, step: int) -> Path:
    label = "front" if step == 10 else f"{step}step"
    matches = sorted(
        candidates.glob(
            "p7-5-2-qwen-edit-prompt-style-fullbody_front_jacket_bag-"
            f"v{92 + step // 10}-compressed-body-only-openpose-{label}-seed-62294-steps-{step}.png"
        )
    )
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one {step}-step candidate, found {len(matches)}: {matches}")
    return matches[0]


def build_sheet(candidates: Path, output: Path) -> None:
    panel_width, panel_height = 320, 480
    header_height, gutter, margin = 52, 18, 24
    canvas = Image.new(
        "RGB",
        (margin * 2 + panel_width * 3 + gutter * 2, margin * 2 + header_height + panel_height),
        "#f7f5ef",
    )
    draw = ImageDraw.Draw(canvas)
    for index, step in enumerate(STEPS):
        source = Image.open(candidate_path(candidates, step)).convert("RGB")
        source.thumbnail((panel_width, panel_height), Image.Resampling.LANCZOS)
        left = margin + index * (panel_width + gutter)
        top = margin + header_height
        panel = Image.new("RGB", (panel_width, panel_height), "#ffffff")
        panel.paste(source, ((panel_width - source.width) // 2, (panel_height - source.height) // 2))
        canvas.paste(panel, (left, top))
        draw.text((left, margin + 16), LABELS[step], fill="#222222")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_CANDIDATES / "p7-5-2-qwen-edit-fullbody-front-step-comparison-v93-v95.png",
    )
    args = parser.parse_args()
    build_sheet(args.candidates, args.output)
    print(args.output)


if __name__ == "__main__":
    main()

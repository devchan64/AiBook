#!/usr/bin/env python3
"""Create a labeled contact sheet from manual-mask inpaint experiment folders."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    runs = sorted(path.parent for path in args.input_root.glob("*/run.json"))
    if len(runs) != 10:
        raise ValueError(f"expected 10 completed runs, found {len(runs)}")
    sample = Image.open(runs[0] / "inpaint-output.png").convert("RGB")
    width, height = sample.size
    header = 42
    columns = 5
    sheet = Image.new("RGB", (columns * width, 2 * (height + header)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, run_dir in enumerate(runs):
        report = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        x = (index % columns) * width
        y = (index // columns) * (height + header)
        label = (
            f"{run_dir.name}\n"
            f"s={report['strength']} cfg={report['guidance_scale']} ip={report['adapter_scale']}\n"
            f"expand={report['mask_expand_px']} pad={report['padding_mask_crop']} seed={report['seed']}"
        )
        draw.multiline_text((x + 4, y + 4), label, fill="black", spacing=2)
        sheet.paste(Image.open(run_dir / "inpaint-output.png").convert("RGB"), (x, y + header))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

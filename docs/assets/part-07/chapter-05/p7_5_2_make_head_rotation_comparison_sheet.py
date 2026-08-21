#!/usr/bin/env python3
"""Create a visual review sheet for the P7-5.2 five-yaw Qwen head experiments."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ASSETS = Path(__file__).resolve().parent
TARGETS = ("profile_left", "quarter_left", "front", "quarter_right", "profile_right")
TARGET_LABELS = ("Left profile", "Left quarter", "Front", "Right quarter", "Right profile")
OPENPOSE_GUIDES = {
    "profile_left": ASSETS / "p7-5-2-openpose-shoulders-five-yaw-face70-fixed-body18-v1-yaw-90_pitch+00.png",
    "quarter_left": ASSETS / "p7-5-2-openpose-shoulders-five-yaw-face70-fixed-body18-v1-yaw-45_pitch+00.png",
    "front": ASSETS / "p7-5-2-openpose-shoulders-five-yaw-face70-fixed-body18-v1-yaw+00_pitch+00.png",
    "quarter_right": ASSETS / "p7-5-2-openpose-shoulders-five-yaw-face70-fixed-body18-v1-yaw+45_pitch+00.png",
    "profile_right": ASSETS / "p7-5-2-openpose-shoulders-five-yaw-face70-fixed-body18-v1-yaw+90_pitch+00.png",
}
REFERENCE = ASSETS / "p7-5-2-face-front-qwen-role-separated-reference.png"
V4_LABEL = "shoulders-face70-five-yaw-v4-preserve-image1"
THUMBNAIL = 320
LABEL_WIDTH = 180
HEADER_HEIGHT = 64
PADDING = 16


def candidate(target: str, run_label: str) -> Path:
    return ASSETS / f"p7-5-2-qwen-head-rotation-{target}-{run_label}-seed-62294-steps-30.png"


def thumb(path: Path) -> Image.Image:
    with Image.open(path) as source:
        image = source.convert("RGB")
    image.thumbnail((THUMBNAIL, THUMBNAIL), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (THUMBNAIL, THUMBNAIL), "#1c2327")
    canvas.paste(image, ((THUMBNAIL - image.width) // 2, (THUMBNAIL - image.height) // 2))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ASSETS / "p7-5-2-qwen-head-rotation-v3-v4-comparison-sheet.png",
    )
    args = parser.parse_args()

    required = [REFERENCE, *OPENPOSE_GUIDES.values()]
    required.extend(candidate(target, V4_LABEL) for target in TARGETS)
    missing = [path for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing comparison input: " + ", ".join(map(str, missing)))

    font = ImageFont.load_default()
    width = LABEL_WIDTH + (len(TARGETS) + 1) * (THUMBNAIL + PADDING) + PADDING
    height = HEADER_HEIGHT + 2 * (THUMBNAIL + PADDING) + PADDING
    sheet = Image.new("RGB", (width, height), "#101518")
    draw = ImageDraw.Draw(sheet)
    draw.text((LABEL_WIDTH, 14), "Identity reference", fill="white", font=font)
    for index, label in enumerate(TARGET_LABELS):
        x = LABEL_WIDTH + (index + 1) * (THUMBNAIL + PADDING)
        draw.text((x, 14), label, fill="white", font=font)

    rows = (
        ("OpenPose", OPENPOSE_GUIDES),
        ("v4: preserve Image 1", {target: candidate(target, V4_LABEL) for target in TARGETS}),
    )
    for row_index, (label, images) in enumerate(rows):
        y = HEADER_HEIGHT + row_index * (THUMBNAIL + PADDING)
        draw.text((PADDING, y + 12), label, fill="white", font=font)
        if row_index == 0:
            sheet.paste(thumb(REFERENCE), (LABEL_WIDTH, y))
        for column_index, target in enumerate(TARGETS):
            x = LABEL_WIDTH + (column_index + 1) * (THUMBNAIL + PADDING)
            sheet.paste(thumb(images[target]), (x, y))

    output = args.output if args.output.is_absolute() else ASSETS / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    print(output)


if __name__ == "__main__":
    main()

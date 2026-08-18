#!/usr/bin/env python3
"""Render a review-only 45-degree left-quarter full-body OpenPose control guide."""

from pathlib import Path

import numpy as np
from PIL import Image

from p7_5_2_qwen_edit_reference_pilot import openpose_module


ASSETS = Path(__file__).resolve().parent
OUTPUT = ASSETS / "p7-5-2-qwen-edit-candidates" / "p7-5-2-openpose-fullbody-quarter-left-45deg-guide.png"
WIDTH, HEIGHT = 960, 1440


def main() -> None:
    module = openpose_module()

    def point(x: float, y: float):
        return module.Keypoint(x=x / WIDTH, y=y / HEIGHT)

    # BODY_18: a true 45-degree turn toward image left.  The nose and torso
    # center shift left, while the near image-right shoulder and hip remain
    # visibly wider than their far-side counterparts.
    coordinates = {
        0: (408, 210), 1: (448, 355),
        2: (568, 395), 3: (609, 623), 4: (618, 844),
        5: (378, 384), 6: (356, 611), 7: (351, 833),
        8: (528, 806), 9: (548, 1061), 10: (558, 1350),
        11: (418, 795), 12: (408, 1054), 13: (403, 1350),
        14: (385, 195), 15: (431, 195), 16: (365, 208), 17: (456, 208),
    }
    body = [point(*coordinates[index]) for index in range(18)]
    pose = module.PoseResult(
        body=module.BodyResult(keypoints=body, total_score=1.0, total_parts=18),
        left_hand=None,
        right_hand=None,
        face=None,
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rendered = module.draw_poses([pose], HEIGHT, WIDTH, draw_body=True, draw_hand=False, draw_face=False)
    Image.fromarray(np.ascontiguousarray(rendered)).save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()

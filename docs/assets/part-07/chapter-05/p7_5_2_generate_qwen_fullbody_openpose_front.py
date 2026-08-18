#!/usr/bin/env python3
"""Render a review-only strict-front full-body OpenPose control guide."""

from pathlib import Path

import numpy as np
from PIL import Image

from p7_5_2_qwen_edit_reference_pilot import openpose_module


ASSETS = Path(__file__).resolve().parent
OUTPUT = ASSETS / "p7-5-2-qwen-edit-candidates" / "p7-5-2-openpose-fullbody-front-guide.png"
WIDTH, HEIGHT = 960, 1440


def main() -> None:
    module = openpose_module()

    def point(x: float, y: float):
        return module.Keypoint(x=x / WIDTH, y=y / HEIGHT)

    # BODY_18: symmetrical strict-front standing pose, relaxed arms, and full
    # leg-to-ankle geometry. This map intentionally carries no RGB identity or
    # apparel information.
    coordinates = {
        0: (480, 205), 1: (480, 350),
        2: (625, 385), 3: (650, 620), 4: (655, 835),
        5: (335, 385), 6: (310, 620), 7: (305, 835),
        8: (565, 800), 9: (575, 1085), 10: (585, 1345),
        11: (395, 800), 12: (385, 1085), 13: (375, 1345),
        14: (440, 192), 15: (520, 192), 16: (420, 205), 17: (540, 205),
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

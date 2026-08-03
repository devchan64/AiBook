#!/usr/bin/env python3
"""Record 2D and estimated 3D landmarks without drawing a skeleton."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mediapipe as mp
from PIL import Image


NAME_TO_INDEX = {
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
    "left_heel": 29,
    "right_heel": 30,
    "left_foot_index": 31,
    "right_foot_index": 32,
}


def midpoint(first: float, second: float) -> float:
    return (first + second) / 2


def silhouette_bounds(image_path: Path) -> tuple[float, float]:
    """Find the top and bottom of a colored figure on the required pale backdrop."""
    with Image.open(image_path).convert("RGB") as image:
        width, height = image.size
        foreground_y = [
            y
            for y in range(height)
            for x in range(width)
            if min(image.getpixel((x, y))) < 245
        ]
    if not foreground_y:
        raise RuntimeError("no non-background pixels found for silhouette landmarks")
    return min(foreground_y) / height, max(foreground_y) / height


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--head-top-y", type=float, required=True)
    parser.add_argument("--chin-y", type=float, required=True)
    args = parser.parse_args()

    if not 0 <= args.head_top_y < args.chin_y <= 1:
        raise ValueError("head-top-y and chin-y must be normalized image y coordinates")

    base_options = mp.tasks.BaseOptions(model_asset_path=str(args.model))
    options = mp.tasks.vision.PoseLandmarkerOptions(
        base_options=base_options,
        running_mode=mp.tasks.vision.RunningMode.IMAGE,
        num_poses=1,
        min_pose_detection_confidence=0.6,
        min_pose_presence_confidence=0.6,
    )
    image = mp.Image.create_from_file(str(args.image))
    with mp.tasks.vision.PoseLandmarker.create_from_options(options) as detector:
        result = detector.detect(image)

    if not result.pose_landmarks:
        raise RuntimeError("no pose landmarks detected; do not infer proportions")

    image_points = result.pose_landmarks[0]
    world_points = result.pose_world_landmarks[0]
    points = {
        name: {
            "image": {
                "x": image_points[index].x,
                "y": image_points[index].y,
                "visibility": image_points[index].visibility,
            },
            "world_estimate_m": {
                "x": world_points[index].x,
                "y": world_points[index].y,
                "z": world_points[index].z,
                "visibility": world_points[index].visibility,
            },
        }
        for name, index in NAME_TO_INDEX.items()
    }

    shoulder_y = midpoint(points["left_shoulder"]["image"]["y"], points["right_shoulder"]["image"]["y"])
    hip_y = midpoint(points["left_hip"]["image"]["y"], points["right_hip"]["image"]["y"])
    sole_y = max(
        points["left_heel"]["image"]["y"],
        points["right_heel"]["image"]["y"],
        points["left_foot_index"]["image"]["y"],
        points["right_foot_index"]["image"]["y"],
    )
    head_height = args.chin_y - args.head_top_y
    body_height = sole_y - args.head_top_y
    leg_height = sole_y - hip_y
    torso_height = hip_y - shoulder_y
    silhouette_top_y, silhouette_bottom_y = silhouette_bounds(args.image)

    report = {
        "image": str(args.image),
        "method": "MediaPipe Pose Landmarker Full; no skeleton image is rendered",
        "manual_landmarks": {"head_top_y": args.head_top_y, "chin_y": args.chin_y},
        "silhouette_landmarks": {
            "top_y": silhouette_top_y,
            "bottom_y": silhouette_bottom_y,
        },
        "landmarks": points,
        "metrics": {
            "heads_tall_2d": body_height / head_height,
            "torso_to_leg_2d": torso_height / leg_height,
            "silhouette_to_shoulder_2d": (
                (silhouette_bottom_y - silhouette_top_y)
                / (shoulder_y - silhouette_top_y)
            ),
            "shoulder_depth_delta_3d_m": abs(
                points["left_shoulder"]["world_estimate_m"]["z"]
                - points["right_shoulder"]["world_estimate_m"]["z"]
            ),
            "hip_depth_delta_3d_m": abs(
                points["left_hip"]["world_estimate_m"]["z"]
                - points["right_hip"]["world_estimate_m"]["z"]
            ),
        },
        "limits": {
            "2d_metrics": "use for proportion comparison after human head-top and chin marking",
            "3d_metrics": "estimated world coordinates; use only as relative direction and asymmetry evidence, never as absolute body measurement",
        },
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"output: {args.output}")
    print(f"heads_tall_2d: {report['metrics']['heads_tall_2d']:.3f}")
    print(f"torso_to_leg_2d: {report['metrics']['torso_to_leg_2d']:.3f}")
    print(f"silhouette_to_shoulder_2d: {report['metrics']['silhouette_to_shoulder_2d']:.3f}")
    print("3d_landmarks: recorded as advisory only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

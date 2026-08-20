#!/usr/bin/env python3
"""Render deterministic face + body OpenPose relation maps.

This is deliberately not an OpenPose detector.  It defines one normalized
3D face/body template, rotates it through the 5 x 5 yaw/pitch grid visible in
the saved head-turnaround reference, and projects the same template into every
output.  The optional perspective mode preserves near/far limb foreshortening.
The PNGs use controlnet_aux's standard OpenPose
renderer; the JSON keeps both world and screen coordinates for ratio editing.

The template is a structural guide only.  It does not encode P7-5.2 identity,
hairstyle, clothing, or image style, and is not a substitute for a real 3D
face scan.

Examples:
  # Default 5×5 yaw/pitch grid.
  .venv/bin/python p7_5_2_generate_turnaround_relation_maps.py

  # Five full-body yaw directions at pitch 0, without face landmarks.
  .venv/bin/python p7_5_2_generate_turnaround_relation_maps.py \\
    --targets profile_left quarter_left front quarter_right profile_right \\
    --no-include-face
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ASSETS = Path(__file__).resolve().parent
DEFAULT_REFERENCE = ASSETS / "upscale_image_01.png"
DEFAULT_OUTPUT = ASSETS / "p7-5-2-openpose-turnaround-relations-v2-seven-heads"
WIDTH, HEIGHT = 768, 1152
# One seven-head unit is 150 px: crown-to-sole is therefore 1,050 px.
CENTER_X, SCALE = WIDTH / 2, 150
# Screen-space y coordinate occupied by the face pivot.  Keep this separate
# from the ground/body template so a generation experiment can reserve a
# larger lower-frame safety margin without changing body proportions.
# With a 150 px head unit, the nose pivot at y=120 leaves room for both the
# virtual crown (~42 px) and sole (~1,092 px) on the 768×1152 canvas.
DEFAULT_FRAME_ORIGIN_Y = 120
# The former perspective mapping had an effective horizontal FOV of about
# 45.8° (SCALE * default camera distance = 910 px focal length).  Use two
# thirds of that angle to make the perspective view deliberately narrower
# while keeping the setting explicit and reproducible.
DEFAULT_PERSPECTIVE_HORIZONTAL_FOV_DEGREES = 30.5
# Keep the seven-head full body framed at the former nominal size after
# narrowing the FOV. This is intentionally independent of the FOV constant,
# so experiments can separately change camera distance (perspective strength).
DEFAULT_PERSPECTIVE_CAMERA_DISTANCE = 10.8
YAWS = (-90, -45, 0, 45, 90)
# Positive pitch is a raised chin / camera looking upward; negative is down.
PITCHES = (55, 27, 0, -27, -55)
TARGET_YAWS = {
    "profile_left": -90,
    "quarter_left": -45,
    "front": 0,
    "quarter_right": 45,
    "profile_right": 90,
}

# A proportion profile is the domain model for a structural OpenPose guide.
# ``seven_head_standing`` is only the default profile, not the domain itself.
HUMAN_PROPORTION_PROFILES = {
    "seven_head_standing": {
        "head_face_height": 1.00,
        "face_width": 0.72,
        "upper_body_neck_base_to_crotch": 2.25,
        "leg_hip_to_sole": 3.55,
        "arm_shoulder_to_wrist": 2.15,
        "total_crown_to_sole": 7.00,
    },
}
DEFAULT_PROPORTION_PROFILE = "seven_head_standing"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def openpose_module():
    """Reuse the installed OpenPose renderer without top-level optional imports."""
    source = ASSETS / "p7_5_2_qwen_edit_reference_pilot.py"
    spec = importlib.util.spec_from_file_location("p7_5_2_relation_renderer_source", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("P7-5.2 OpenPose renderer source is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.openpose_module()


def rotate(point: tuple[float, float, float], yaw: float, pitch: float, pivot: tuple[float, float, float]) -> tuple[float, float, float]:
    """Rotate around a supplied structural pivot (y up, z toward camera)."""
    x, y, z = (point[0] - pivot[0], point[1] - pivot[1], point[2] - pivot[2])
    yaw_r = math.radians(yaw)
    pitch_r = math.radians(pitch)
    x, z = x * math.cos(yaw_r) + z * math.sin(yaw_r), -x * math.sin(yaw_r) + z * math.cos(yaw_r)
    y, z = y * math.cos(pitch_r) - z * math.sin(pitch_r), y * math.sin(pitch_r) + z * math.cos(pitch_r)
    return x + pivot[0], y + pivot[1], z + pivot[2]


def focal_length_for_horizontal_fov(horizontal_fov_degrees: float) -> float:
    """Return the pixel focal length implied by the output canvas and HFOV."""
    return WIDTH / (2.0 * math.tan(math.radians(horizontal_fov_degrees) / 2.0))


def project(point: tuple[float, float, float], yaw: float, pitch: float, projection: str, camera_distance: float, horizontal_fov_degrees: float, pivot: tuple[float, float, float], frame_origin_y: float) -> tuple[float, float]:
    x, y, z = rotate(point, yaw, pitch, pivot)
    # For perspective runs, the face remains the camera reference point so the
    # body foreshortens relative to the head rather than relative to the ground.
    if projection == "orthographic":
        focal_length = SCALE
        depth = 1.0
    else:
        focal_length = focal_length_for_horizontal_fov(horizontal_fov_degrees)
        depth = camera_distance - (z - pivot[2])
    return CENTER_X + focal_length * (x - pivot[0]) / depth, frame_origin_y - focal_length * (y - pivot[1]) / depth


def proportion_geometry(proportions: dict[str, float]) -> dict[str, float]:
    """Convert an editable human-proportion profile into shared body heights."""
    head = proportions["head_face_height"]
    upper_body = proportions["upper_body_neck_base_to_crotch"]
    leg = proportions["leg_hip_to_sole"]
    total = proportions["total_crown_to_sole"]
    if min(head, upper_body, leg, total, proportions["face_width"], proportions["arm_shoulder_to_wrist"]) <= 0:
        raise ValueError("Every human-proportion value must be positive")
    neck_to_chin = total - head - upper_body - leg
    if neck_to_chin < 0:
        raise ValueError("total_crown_to_sole is too short for the supplied head, torso, and leg lengths")
    hip_y = leg
    neck_y = hip_y + upper_body
    return {
        "head": head,
        "face_width": proportions["face_width"],
        "arm": proportions["arm_shoulder_to_wrist"],
        "sole_y": 0.0,
        "hip_y": hip_y,
        "neck_y": neck_y,
        "chin_y": neck_y + neck_to_chin,
        "crown_y": total,
    }


def body_template(proportions: dict[str, float]) -> list[tuple[float, float, float]]:
    """OpenPose BODY_18 order derived from one human-proportion profile."""
    geometry = proportion_geometry(proportions)
    head, face_width, arm = geometry["head"], geometry["face_width"], geometry["arm"]
    shoulder_y = geometry["neck_y"] - 0.04 * head
    elbow_y = shoulder_y - 0.46 * arm
    wrist_y = shoulder_y - arm
    shoulder_x = face_width
    arm_bend_x = 0.43 * face_width
    hip_x = 0.58 * face_width
    knee_x = 0.64 * face_width
    knee_y = geometry["hip_y"] * 0.50
    return [
        (0.00, geometry["chin_y"] + 0.48 * head, 0.52 * head),  # nose
        (0.00, geometry["neck_y"], 0.00),  # neck base
        (-shoulder_x, shoulder_y, 0.00), (-shoulder_x - arm_bend_x, elbow_y, 0.03), (-shoulder_x - arm_bend_x, wrist_y, 0.05),  # right arm
        (shoulder_x, shoulder_y, 0.00), (shoulder_x + arm_bend_x, elbow_y, 0.03), (shoulder_x + arm_bend_x, wrist_y, 0.05),      # left arm
        (-hip_x, geometry["hip_y"], 0.00), (-knee_x, knee_y, 0.02), (-knee_x, geometry["sole_y"], 0.10),  # right leg
        (hip_x, geometry["hip_y"], 0.00), (knee_x, knee_y, 0.02), (knee_x, geometry["sole_y"], 0.10),     # left leg
        (-0.24 * face_width, geometry["chin_y"] + 0.62 * head, 0.48 * head), (0.24 * face_width, geometry["chin_y"] + 0.62 * head, 0.48 * head),  # eyes
        (-0.53 * face_width, geometry["chin_y"] + 0.54 * head, 0.18 * head), (0.53 * face_width, geometry["chin_y"] + 0.54 * head, 0.18 * head),  # ears
    ]


def apply_body_pose(points: list[tuple[float, float, float]], pose: str, proportions: dict[str, float]) -> list[tuple[float, float, float]]:
    """Apply a deliberately visible pose ablation before view rotation."""
    if pose == "neutral":
        return points
    geometry = proportion_geometry(proportions)
    head = geometry["head"]
    posed = list(points)
    # BODY_18 indices 5, 6, 7 are the image-right arm before camera rotation.
    shoulder = posed[5]
    posed[6] = (shoulder[0] + 0.18 * head, geometry["neck_y"] + 0.65 * head, 0.18 * head)
    posed[7] = (shoulder[0] - 0.05 * head, geometry["neck_y"] + 1.35 * head, 0.32 * head)
    if pose == "raised-arm":
        return posed
    if pose not in {"asymmetric-lowered-arms", "hand-on-hip"}:
        raise ValueError(f"Unsupported body pose: {pose}")

    # Preserve the source upper-/lower-arm bone lengths while changing only
    # their 3D directions. Both wrists remain below their shoulders.
    posed = list(points)
    def distance(a, b):
        return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))
    def endpoint(start, direction, length):
        norm = math.sqrt(sum(value * value for value in direction))
        return tuple(start[i] + length * direction[i] / norm for i in range(3))
    right_upper, right_lower = distance(points[2], points[3]), distance(points[3], points[4])
    left_upper, left_lower = distance(points[5], points[6]), distance(points[6], points[7])
    # Camera-left arm: relaxed, slightly behind the torso.
    posed[3] = endpoint(points[2], (-0.18, -1.0, -0.18), right_upper)
    posed[4] = endpoint(posed[3], (0.08, -1.0, -0.10), right_lower)
    if pose == "hand-on-hip":
        # Camera-right hand finishes at the waist; the angled elbow makes this
        # a readable hand-on-hip pose without changing either bone length.
        posed[6] = endpoint(points[5], (1.15, -0.18, 0.30), left_upper)
        posed[7] = endpoint(posed[6], (-0.62, -0.78, 0.12), left_lower)
    else:
        # Camera-right arm: still lowered, but elbow and wrist advance toward camera.
        posed[6] = endpoint(points[5], (0.22, -1.0, 0.42), left_upper)
        posed[7] = endpoint(posed[6], (-0.12, -1.0, 0.35), left_lower)

    # Shift weight onto the camera-left leg.  The supporting leg stays nearly
    # vertical; the other knee relaxes inward and its foot steps slightly out.
    right_upper_leg, right_lower_leg = distance(points[8], points[9]), distance(points[9], points[10])
    left_upper_leg, left_lower_leg = distance(points[11], points[12]), distance(points[12], points[13])
    posed[8] = (points[8][0] - 0.08 * head, points[8][1], points[8][2])
    posed[11] = (points[11][0] - 0.08 * head, points[11][1] - 0.06 * head, points[11][2])
    posed[9] = endpoint(posed[8], (-0.03, -1.0, -0.04), right_upper_leg)
    posed[10] = endpoint(posed[9], (0.02, -1.0, 0.01), right_lower_leg)
    posed[12] = endpoint(posed[11], (0.22, -0.96, 0.12), left_upper_leg)
    posed[13] = endpoint(posed[12], (0.20, -0.98, 0.08), left_lower_leg)
    return posed


def arc(cx: float, cy: float, rx: float, ry: float, start: float, end: float, count: int, z: float) -> list[tuple[float, float, float]]:
    return [
        (cx + rx * math.cos(math.radians(angle)), cy + ry * math.sin(math.radians(angle)), z)
        for angle in np.linspace(start, end, count)
    ]


def face_template(proportions: dict[str, float]) -> tuple[list[tuple[float, float, float]], dict[str, list[int]]]:
    """Scale one 70-point canonical face by the selected human-proportion profile."""
    geometry = proportion_geometry(proportions)
    cx, cy = 0.0, 6.70
    jaw = [
        (0.36 * math.cos(math.radians(angle)), cy + 0.68 * math.sin(math.radians(angle)) - 0.02,
         0.14 + 0.20 * max(0.0, math.sin(math.radians(angle))))
        for angle in np.linspace(198, 342, 17)
    ]
    left_brow = arc(-0.17, 6.95, 0.13, 0.055, 198, 342, 5, 0.49)
    right_brow = arc(0.17, 6.95, 0.13, 0.055, 198, 342, 5, 0.49)
    nose_bridge = [(0.0, y, 0.53 + i * 0.035) for i, y in enumerate(np.linspace(6.90, 6.58, 4))]
    nose_base = [(-0.10, 6.54, 0.52), (-0.05, 6.49, 0.62), (0.0, 6.48, 0.67), (0.05, 6.49, 0.62), (0.10, 6.54, 0.52)]
    left_eye = arc(-0.17, 6.78, 0.115, 0.048, 0, 360, 6, 0.56)
    right_eye = arc(0.17, 6.78, 0.115, 0.048, 0, 360, 6, 0.56)
    outer_lip = arc(0.0, 6.27, 0.19, 0.075, 0, 360, 12, 0.57)
    inner_lip = arc(0.0, 6.27, 0.11, 0.032, 0, 360, 8, 0.585)
    irises = [(-0.17, 6.78, 0.575), (0.17, 6.78, 0.575)]
    points = jaw + left_brow + right_brow + nose_bridge + nose_base + left_eye + right_eye + outer_lip + inner_lip + irises
    # The canonical face has chin y=6, face width=.72, and face height=1.
    # Attach and scale it from the profile-derived chin instead of fixed pixels.
    points = [
        (
            x * geometry["face_width"] / 0.72,
            geometry["chin_y"] + (y - 6.00) * geometry["head"],
            z * geometry["head"],
        )
        for x, y, z in points
    ]
    groups = {
        "jaw": list(range(0, 17)), "left_brow": list(range(17, 22)), "right_brow": list(range(22, 27)),
        "nose_bridge": list(range(27, 31)), "nose_base": list(range(31, 36)), "left_eye": list(range(36, 42)),
        "right_eye": list(range(42, 48)), "outer_lip": list(range(48, 60)), "inner_lip": list(range(60, 68)),
        "iris_centres": [68, 69],
    }
    assert len(points) == 70
    return points, groups


def as_keypoint(renderer, xy: tuple[float, float]):
    x, y = xy
    return renderer.Keypoint(x=x / WIDTH, y=y / HEIGHT, score=1.0)


def serialise_points(points: list[tuple[float, float, float]], yaw: float, pitch: float, projection: str, camera_distance: float, horizontal_fov_degrees: float, pivot: tuple[float, float, float], frame_origin_y: float) -> list[dict[str, object]]:
    rows = []
    for index, world in enumerate(points):
        x, y = project(world, yaw, pitch, projection, camera_distance, horizontal_fov_degrees, pivot, frame_origin_y)
        rows.append({
            "index": index,
            "world_xyz": [round(value, 5) for value in world],
            "screen_xy": [round(x, 3), round(y, 3)],
            "normalized_xy": [round(x / WIDTH, 6), round(y / HEIGHT, 6)],
            "confidence": 1.0,
        })
    return rows


def render_map(renderer, body: list[dict[str, object]], face: list[dict[str, object]] | None) -> Image.Image:
    body_points = [renderer.Keypoint(x=row["normalized_xy"][0], y=row["normalized_xy"][1], score=1.0) for row in body]
    face_points = (
        [renderer.Keypoint(x=row["normalized_xy"][0], y=row["normalized_xy"][1], score=1.0) for row in face]
        if face is not None
        else None
    )
    pose = renderer.PoseResult(
        body=renderer.BodyResult(keypoints=body_points, total_score=1.0, total_parts=len(body_points)),
        left_hand=None,
        right_hand=None,
        face=face_points,
    )
    canvas = renderer.draw_poses([pose], HEIGHT, WIDTH, draw_body=True, draw_hand=False, draw_face=face is not None)
    return Image.fromarray(np.ascontiguousarray(canvas)).convert("RGB")


def contact_sheet(entries: list[tuple[str, Image.Image]], path: Path) -> None:
    tile_w, tile_h = 192, 288
    rows = math.ceil(len(entries) / 5)
    sheet = Image.new("RGB", (tile_w * 5, tile_h * rows), "black")
    draw = ImageDraw.Draw(sheet)
    for index, (label, image) in enumerate(entries):
        tile = image.resize((tile_w, tile_h), Image.Resampling.NEAREST)
        left, top = (index % 5) * tile_w, (index // 5) * tile_h
        sheet.paste(tile, (left, top))
        draw.text((left + 6, top + 6), label, fill="white")
    sheet.save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE, help="Head-turnaround reference used only for direction review")
    parser.add_argument(
        "--openpose-review",
        type=Path,
        help="Optional earlier detector review to retain as comparison evidence; it does not affect coordinates.",
    )
    parser.add_argument("--yaws", type=int, nargs="+", default=list(YAWS), help="Yaw angles to render in degrees")
    parser.add_argument("--pitches", type=int, nargs="+", default=list(PITCHES), help="Pitch angles to render in degrees")
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=tuple(TARGET_YAWS),
        help="Named full-body yaw targets to render sequentially at pitch 0; preserves the supplied order.",
    )
    parser.add_argument(
        "--proportion-profile",
        choices=sorted(HUMAN_PROPORTION_PROFILES),
        default=DEFAULT_PROPORTION_PROFILE,
        help="Named human-proportion profile that drives all body and face coordinates.",
    )
    parser.add_argument(
        "--output-range",
        choices=("all", "pitch0", "front"),
        help="Convenience range: all=5x5 grid, pitch0=five yaw views at pitch 0, front=one frontal view. Overrides --yaws/--pitches; incompatible with --targets.",
    )
    parser.add_argument(
        "--include-face",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Render and write the 70-point face map (use --no-include-face for a body-only guide).",
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--body-pose", choices=("neutral", "raised-arm", "asymmetric-lowered-arms", "hand-on-hip"), default="neutral")
    parser.add_argument(
        "--projection",
        choices=("orthographic", "perspective"),
        default="perspective",
        help="Projection model; perspective is the default so --horizontal-fov-degrees is applied.",
    )
    parser.add_argument("--camera-distance", type=float, default=DEFAULT_PERSPECTIVE_CAMERA_DISTANCE, help="Camera distance in template-head units for perspective projection.")
    parser.add_argument(
        "--frame-origin-y",
        type=float,
        default=DEFAULT_FRAME_ORIGIN_Y,
        help="Screen y coordinate for the face pivot; lower values move the complete skeleton upward.",
    )
    parser.add_argument(
        "--horizontal-fov-degrees",
        type=float,
        default=DEFAULT_PERSPECTIVE_HORIZONTAL_FOV_DEGREES,
        help="Horizontal field of view for perspective projection; default is two thirds of the former effective 45.8° FOV.",
    )
    args = parser.parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    reference = args.reference if args.reference.is_absolute() else ASSETS / args.reference
    detection_review = (
        args.openpose_review if args.openpose_review and args.openpose_review.is_absolute()
        else ASSETS / args.openpose_review if args.openpose_review
        else None
    )
    if not reference.is_file():
        raise FileNotFoundError(reference)
    if detection_review is not None and not detection_review.is_file():
        raise FileNotFoundError(detection_review)
    if args.camera_distance <= 1.0:
        raise ValueError("--camera-distance must be greater than 1.0")
    if not 1.0 < args.horizontal_fov_degrees < 179.0:
        raise ValueError("--horizontal-fov-degrees must be between 1 and 179")
    if not 0.0 <= args.frame_origin_y <= HEIGHT:
        raise ValueError(f"--frame-origin-y must be between 0 and {HEIGHT}")
    if args.targets and args.output_range:
        parser.error("--targets cannot be combined with --output-range")
    if args.targets:
        target_names = args.targets
        yaws, pitches = [TARGET_YAWS[target] for target in target_names], [0]
    elif args.output_range == "all":
        target_names = None
        yaws, pitches = list(YAWS), list(PITCHES)
    elif args.output_range == "pitch0":
        target_names = list(TARGET_YAWS)
        yaws, pitches = list(YAWS), [0]
    elif args.output_range == "front":
        target_names = ["front"]
        yaws, pitches = [0], [0]
    else:
        target_names = None
        yaws, pitches = args.yaws, args.pitches
    manifest = output_dir / "turnaround-relation-maps.json"
    if manifest.exists() and not args.overwrite:
        raise FileExistsError(f"{manifest} exists; pass --overwrite to replace this generated set")
    output_dir.mkdir(parents=True, exist_ok=True)

    renderer = openpose_module()
    proportions = HUMAN_PROPORTION_PROFILES[args.proportion_profile]
    body_world = apply_body_pose(body_template(proportions), args.body_pose, proportions)
    face_world, face_groups = face_template(proportions)
    geometry = proportion_geometry(proportions)
    face_pivot = (0.0, geometry["chin_y"] + 0.48 * geometry["head"], 0.52 * geometry["head"])
    views: list[dict[str, object]] = []
    previews: list[tuple[str, Image.Image]] = []
    for row, pitch in enumerate(pitches, start=1):
        for column, yaw in enumerate(yaws, start=1):
            target_name = target_names[column - 1] if target_names and len(pitches) == 1 else None
            body = serialise_points(body_world, yaw, pitch, args.projection, args.camera_distance, args.horizontal_fov_degrees, face_pivot, args.frame_origin_y)
            face = serialise_points(face_world, yaw, pitch, args.projection, args.camera_distance, args.horizontal_fov_degrees, face_pivot, args.frame_origin_y) if args.include_face else None
            label = f"yaw{yaw:+03d}_pitch{pitch:+03d}"
            png_name = f"p7-5-2-openpose-relation-{label}.png"
            json_name = f"p7-5-2-openpose-relation-{label}.json"
            image = render_map(renderer, body, face)
            image.save(output_dir / png_name)
            view = {
                "grid_position": {"row": row, "column": column},
                "target": target_name,
                "yaw_degrees": yaw,
                "pitch_degrees": pitch,
                "projection": {"type": args.projection, "canvas": [WIDTH, HEIGHT], "center_xy": [CENTER_X, args.frame_origin_y], "pixels_per_unit": SCALE, "camera_distance": args.camera_distance if args.projection == "perspective" else None, "horizontal_fov_degrees": args.horizontal_fov_degrees if args.projection == "perspective" else None, "focal_length_px": round(focal_length_for_horizontal_fov(args.horizontal_fov_degrees), 3) if args.projection == "perspective" else None},
                "body_openpose_18": body,
                "face_openpose_70": face,
                "face_point_groups": face_groups if args.include_face else {},
                "png": png_name,
            }
            (output_dir / json_name).write_text(json.dumps(view, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            views.append({**{key: view[key] for key in ("grid_position", "target", "yaw_degrees", "pitch_degrees", "png")}, "coordinates": json_name})
            previews.append((label, image))

    sheet_name = "p7-5-2-openpose-relation-contact-sheet.png"
    contact_sheet(previews, output_dir / sheet_name)
    manifest.write_text(
        json.dumps(
            {
                "status": "review_required",
                "purpose": "Deterministic common-coordinate face and full-body OpenPose relation maps for ratio adjustment.",
                "reference_direction_sheet": {"path": str(reference), "sha256": sha256(reference)},
                "prior_openpose_detection_review": (
                    {"path": str(detection_review), "sha256": sha256(detection_review)}
                    if detection_review is not None
                    else None
                ),
                "method": f"One normalized 3D structural template was yaw/pitch rotated and {args.projection} projected; no landmark detector was used for the generated coordinates.",
                "coordinate_system": {"world": "x right, y up, z toward camera; origin at ground centre", "screen": "x right, y down", "canvas": [WIDTH, HEIGHT], "frame_origin_y": args.frame_origin_y, "projection": args.projection, "camera_distance": args.camera_distance if args.projection == "perspective" else None, "horizontal_fov_degrees": args.horizontal_fov_degrees if args.projection == "perspective" else None, "focal_length_px": round(focal_length_for_horizontal_fov(args.horizontal_fov_degrees), 3) if args.projection == "perspective" else None},
                "human_proportion_profile": {"name": args.proportion_profile, "values": proportions},
                "body_pose": args.body_pose,
                "view_grid": {"columns": yaws, "rows": pitches, "meaning": "columns=yaw degrees, rows=pitch degrees"},
                "targets": target_names,
                "output_range": args.output_range or "custom",
                "openpose": {"body": "BODY_18", "face_included": args.include_face, "face": "70 points: 68 contour landmarks plus 2 iris centres" if args.include_face else None, "hands_included": False},
                "contact_sheet": sheet_name,
                "views": views,
                "limitations": [
                    "This is a proportion-editing template, not a detected pose or a character identity map.",
                    "Occlusion is not removed from the JSON: each point remains present so that the same indexed relation can be compared across rotations.",
                    "The supplied head-turnaround sheet is used for angle inspection only; it has no body data and does not calibrate this template to a scan."
                ],
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    print(output_dir / sheet_name)
    print(manifest)


if __name__ == "__main__":
    main()

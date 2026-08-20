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
    --targets profile_left quarter_left front quarter_right profile_right
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import math
import sys
import sysconfig
import types
import zlib
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ASSETS = Path(__file__).resolve().parent
DEFAULT_REFERENCE = ASSETS / "upscale_image_01.png"
# File names encode the run, so candidate output stays directly in the chapter
# asset root instead of creating a directory per candidate.
DEFAULT_OUTPUT = ASSETS
FULLBODY_WIDTH, FULLBODY_HEIGHT = 768, 1152
SHOULDERS_WIDTH, SHOULDERS_HEIGHT = 768, 768
WIDTH, HEIGHT = FULLBODY_WIDTH, FULLBODY_HEIGHT
# One seven-head unit is 150 px: crown-to-sole is therefore 1,050 px.
CENTER_X, SCALE = WIDTH / 2, 150
# Screen-space y coordinate occupied by the face pivot.  Keep this separate
# from the ground/body template so a generation experiment can reserve a
# larger lower-frame safety margin without changing body proportions.
# With a 150 px head unit, the nose pivot at y=120 leaves room for both the
# virtual crown (~42 px) and sole (~1,092 px) on the 768×1152 canvas.
DEFAULT_FRAME_ORIGIN_Y = 120
# Square head-and-shoulders maps centre the BODY_18 nose/eye/ear cluster. The
# shoulders then remain below the centre without cutting off the crop.
DEFAULT_SHOULDERS_FRAME_ORIGIN_Y = SHOULDERS_HEIGHT / 2
SHOULDERS_SCALE = 240
# The former perspective mapping had an effective horizontal FOV of about
# 45.8° (SCALE * default camera distance = 910 px focal length).  Use two
# thirds of that angle to make the perspective view deliberately narrower
# while keeping the setting explicit and reproducible.
DEFAULT_PERSPECTIVE_HORIZONTAL_FOV_DEGREES = 30.5
# Keep the seven-head full body framed at the former nominal size after
# narrowing the FOV. This is intentionally independent of the FOV constant,
# so experiments can separately change camera distance (perspective strength).
DEFAULT_PERSPECTIVE_CAMERA_DISTANCE = 10.8
DEFAULT_SHOULDERS_CAMERA_DISTANCE = 4.5
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
# Measured from p7-5-2-qwen-torso-profile-right-face70-source-v1.  These are
# FACE_70 points normalized around BODY_18 nose/eye/ear anchors, embedded here
# so relation-map generation never depends on a separate observation JSON.
PROFILE_RIGHT_FACE70_ANCHORS = {0: (0.0, 0.0), 14: (-0.469073, -0.469077), 15: (0.046912, -0.39403), 16: (-1.923205, -0.253306), 17: None}
PROFILE_RIGHT_FACE70_POINTS = (
    (-1.613614, -0.544135), (-1.613614, -0.178259), (-1.613614, 0.187629), (-1.510417, 0.562886), (-1.191445, 0.8068), (-0.975678, 0.928762), (-0.656706, 1.050725), (-0.337734, 1.172676), (-0.234537, 1.172676), (-0.337734, 1.050725), (-0.121959, 0.8068), (-0.018762, 0.684848), (0.084435, 0.440924), (0.084435, 0.431543), (0.084435, 0.187629), (0.093816, -0.046915), (-0.018762, -0.178259),
    (-0.863092, -0.788049), (-0.656706, -0.788049), (-0.440931, -0.788049), (-0.337734, -0.788049), (-0.121959, -0.666087), (-0.018762, -0.544135), (-0.018762, -0.666087), (-0.018762, -0.666087), (-0.018762, -0.666087), (-0.121959, -0.666087), (-0.121959, -0.30021), (-0.018762, -0.178259), (-0.009381, -0.046915), (0.093816, 0.187629), (-0.121959, 0.30958), (-0.018762, 0.318961), (-0.018762, 0.318961), (-0.018762, 0.318961), (-0.009381, 0.30958),
    (-0.656706, -0.422173), (-0.553509, -0.544135), (-0.440931, -0.422173), (-0.440931, -0.412792), (-0.544128, -0.30021), (-0.656706, -0.422173), (-0.121959, -0.30021), (-0.121959, -0.30021), (-0.121959, -0.30021), (-0.018762, -0.30021), (-0.121959, -0.290829), (-0.121959, -0.290829),
    (-0.337734, 0.675467), (-0.225156, 0.562886), (-0.121959, 0.553505), (-0.018762, 0.562886), (-0.018762, 0.553505), (-0.018762, 0.553505), (-0.121959, 0.562886), (-0.121959, 0.684848), (-0.018762, 0.684848), (-0.121959, 0.8068), (-0.121959, 0.8068), (-0.234537, 0.797419), (-0.234537, 0.684848), (-0.121959, 0.675467), (-0.018762, 0.562886), (-0.018762, 0.562886), (-0.121959, 0.562886), (-0.018762, 0.562886), (-0.018762, 0.675467), (-0.121959, 0.675467), (-0.544128, -0.422173), (-0.121959, -0.30021),
)
FACE70_GROUPS = {"jaw": list(range(0, 17)), "left_brow": list(range(17, 22)), "right_brow": list(range(22, 27)), "nose_bridge": list(range(27, 31)), "nose_base": list(range(31, 36)), "left_eye": list(range(36, 42)), "right_eye": list(range(42, 48)), "outer_lip": list(range(48, 60)), "inner_lip": list(range(60, 68)), "pupils": [68, 69]}


def decode_embedded_face70(value: str) -> dict[str, object]:
    """Decode compact source-code literals; no external observation file is read."""
    return json.loads(zlib.decompress(base64.b85decode(value)).decode("utf-8"))


FRONT_FACE70 = decode_embedded_face70("c$|e)%WmT^4Ez_Loj@eThx#jvBIu$y6xeMS-AlVg|9wfxcBI5W4hf90#NiBw{+gbqhp#Ec-_N(_Pq5R=>+|_zdPwv1`u6_&>DSA@^YiKBb9(rZj+`=x&glq}+2}FO{5_w}pZ<G#KiytPel|UR&lBWZ3dnmL*)k~y2WJzw$8qo*1rqD*Pb6TVm5+D$cvllrVXJ(oYWFn-9bwRADnwT4WQR_6<z+2UEmZV}yYk@Z?FoS2AV}bb1fA~C>8?5!tY(TS-y?$~7DUX|3{I}hx&HWzXafKU!>5F7;<W~F>8*l^NJ|u9F)o3nW1*B&$Trl()<9JzDzo1(pY;NA$vM;9dTAxyH6WjpgKnQ!Y9JCyLI(v6!P6LlV^<0z7QK-KmXM4q#u=5YFX-(c3FTlGp&}J4DKiI_k``I8Rg315O9*VQa||g9W3AUzwIsU~#vVH~hchki_>^ScBsI_&O{vD()c38SqENJkJv<rh8NtP#Lo)!I7tsn-ej+aQ=w?uNebq4^*1T6xvcMG-^TaD=AA+V@FUC=5Ks!5na0^fiSPfMSNtT0QmjoD7Qn<Rkf!*zGI)2$BDL9^6oLC(lJnuu^Ti(mLe06#>T(xplU^zM}m!g)2boj_DqYd<J_?4zL+|uidB{HOFi*GdKi-p*q+^IOWxa~;4ic5ml#9w(HtD$A|yu&unI}DTfRQiHzH^YK0Hu&eo%ry7o8kTdR?XXLKBe;Dkwu(L2Yu>JR{cJoPw#eJ>yFa(~y<2aW`1WHsjPJ6UOYk1Q{{wSn*a`")
QUARTER_RIGHT_FACE70 = decode_embedded_face70("c$|%t(TW=}3`PHCo~J>wWl7Gjln_#qhlMm-wiGs9_TOuHrXG1R-7O)(oXEPmlI^$QH0<97u%B<w=R4~0>2|)n4tp4f+w;r!)Ai~1<$Qd-5BsmMOC#)1F%uo^@1K|B<zBw0m*ZnBlvp^tj|0+UcBHNJq!2(&gHx99nZ}p0gPAFgWtEtex$312y|ifuW1>*?ilzVX6fp-)CPx%NCOO`a<4t=(K%>b?MwU<Q;Z87@kLf|yfT8Niu)qDfUd!@FiLx-tim7%X=8#iqTu(tFn_i_7liC~uCB_*>NikaEDI?}QK@?RsC>TPlk+91#1~v~FR3c8$0zw*b2N6@4p`}tO5JMK$36>5Z<rTE@q=SW7d1@(vvq)uVwdbO(2&7b*g@M^gT1Lndn?y=CSP7<lWf?P%QxfsW3ZUXfR}iiF)VZFmLT`IT6DCOyG-MK#H8qV;)fi*#dvn>djkwvR&*;nl7%p9(YlAdX8(Zl7d)Q7=gVQ3!&d^jH_ev}HcYA}|tPS07wgVucKk(KY0;tsTFm>l}6>DpzwfkjurWSZT=N9XG;@~p7rsW6a;4%}peTi)HKBupVP*Qy=+qqv3nZL$vB=%OOv>Hi^blu-#?s_%GDx71_{9DmryRTl^!&ak*&5h4F&#m{}wtLuwI{1;Fj|2aea#MUcNN(oKEuP`w{SSGPzjF")

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
    """Load the installed OpenPose renderer without top-level optional imports."""
    root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    package_name = "p7_5_2_relation_openpose_aux"
    parent = types.ModuleType(package_name)
    parent.__path__ = [str(root)]
    sys.modules[package_name] = parent
    directory = root / "open_pose"
    spec = importlib.util.spec_from_file_location(
        f"{package_name}.open_pose",
        directory / "__init__.py",
        submodule_search_locations=[str(directory)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("controlnet_aux OpenPose renderer is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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
    if pose != "hand-on-hip":
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
    # Camera-right hand finishes at the waist; the angled elbow makes this a
    # readable hand-on-hip pose without changing either bone length.
    posed[6] = endpoint(points[5], (1.15, -0.18, 0.30), left_upper)
    posed[7] = endpoint(posed[6], (-0.62, -0.78, 0.12), left_lower)

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


def serialise_points(points: list[tuple[float, float, float]], yaw: float, pitch: float, projection: str, camera_distance: float, horizontal_fov_degrees: float, pivot: tuple[float, float, float], frame_origin_y: float, visible_indices: set[int] | None = None) -> list[dict[str, object] | None]:
    rows = []
    for index, world in enumerate(points):
        if visible_indices is not None and index not in visible_indices:
            rows.append(None)
            continue
        x, y = project(world, yaw, pitch, projection, camera_distance, horizontal_fov_degrees, pivot, frame_origin_y)
        rows.append({
            "index": index,
            "world_xyz": [round(value, 5) for value in world],
            "screen_xy": [round(x, 3), round(y, 3)],
            "normalized_xy": [round(x / WIDTH, 6), round(y / HEIGHT, 6)],
            "confidence": 1.0,
        })
    return rows


def calibrate_profile_ear_depth(
    body_rows: list[dict[str, object] | None],
    body_world: list[tuple[float, float, float]],
    yaw: float,
    pitch: float,
    projection: str,
    camera_distance: float,
    horizontal_fov_degrees: float,
    pivot: tuple[float, float, float],
    frame_origin_y: float,
) -> None:
    """Correct only pitch-0 profile ear placement from the measured FACE_70 view.

    The actual Qwen right profile has a 205 px nose-to-visible-ear span for a
    209 px face height.  At ±90°, the generic 3D template's ear depth made
    that span too short and therefore reduced the similarity-fitted FACE_70.
    We re-project only both profile ears on the head centre plane.  Quarter
    views retain the unmodified 3D template, where this calibration is not
    supported by a profile measurement.
    """
    if abs(yaw) != 90 or pitch != 0:
        return
    for index in (16, 17):
        if body_rows[index] is None:
            continue
        x, y, _ = body_world[index]
        screen_x, screen_y = project(
            (x, y, 0.0), yaw, pitch, projection, camera_distance,
            horizontal_fov_degrees, pivot, frame_origin_y,
        )
        body_rows[index]["screen_xy"] = [round(screen_x, 3), round(screen_y, 3)]
        body_rows[index]["normalized_xy"] = [round(screen_x / WIDTH, 6), round(screen_y / HEIGHT, 6)]


def centre_rows_horizontally(rows: list[dict[str, object] | None], anchor_indices: set[int]) -> float:
    """Translate a crop so the projected anchor bounding box is centred."""
    anchors = [rows[index] for index in anchor_indices if rows[index] is not None]
    if not anchors:
        return 0.0
    xs = [row["screen_xy"][0] for row in anchors]
    offset = WIDTH / 2 - (min(xs) + max(xs)) / 2
    for row in rows:
        if row is None:
            continue
        x, y = row["screen_xy"]
        row["screen_xy"] = [round(x + offset, 3), y]
        row["normalized_xy"] = [round((x + offset) / WIDTH, 6), row["normalized_xy"][1]]
    return round(offset, 3)


def mirrored_face_index(index: int) -> int:
    if index < 17:
        return 16 - index
    if index < 22:
        return 26 - (index - 17)
    if index < 27:
        return 21 - (index - 22)
    if index < 31:
        return index
    if index < 36:
        return 35 - (index - 31)
    if index < 42:
        return 47 - (index - 36)
    if index < 48:
        return 41 - (index - 42)
    if index < 60:
        return 59 - (index - 48)
    if index < 68:
        return 67 - (index - 60)
    return 137 - index


def mirrored_body_index(index: int) -> int:
    """Return the BODY_18 source index that becomes ``index`` after reflection."""
    return (0, 1, 5, 6, 7, 2, 3, 4, 11, 12, 13, 8, 9, 10, 15, 14, 17, 16)[index]


def mirrored_body_anchors(anchors: dict[int, tuple[float, float] | None]) -> dict[int, tuple[float, float] | None]:
    """Reflect BODY_18 head anchors while preserving their left/right semantics."""
    return {
        index: None if (point := anchors.get(mirrored_body_index(index))) is None else (-point[0], point[1])
        for index in anchors
    }


def embedded_face_observations() -> dict[tuple[int, int], dict[str, object]]:
    """Return the embedded actual right profile and its declared mirror."""
    right = {
        "anchors": PROFILE_RIGHT_FACE70_ANCHORS,
        "points": PROFILE_RIGHT_FACE70_POINTS,
        "provenance": "measured_qwen_torso_profile_right_face70",
        "symmetry_assumption": False,
    }
    left = {
        "anchors": mirrored_body_anchors(PROFILE_RIGHT_FACE70_ANCHORS),
        "points": tuple(
            (-PROFILE_RIGHT_FACE70_POINTS[mirrored_face_index(index)][0], PROFILE_RIGHT_FACE70_POINTS[mirrored_face_index(index)][1])
            for index in range(70)
        ),
        "provenance": "horizontal_reflection_of_measured_qwen_torso_profile_right_face70",
        "symmetry_assumption": True,
    }
    front = {
        "anchors": {int(index): None if point is None else tuple(point["nose_eye_ear_normalized_xy"]) for index, point in FRONT_FACE70["a"].items()},
        "points": tuple(map(tuple, FRONT_FACE70["p"])),
        "provenance": "measured_fullbody_front_face70",
        "symmetry_assumption": False,
    }
    quarter_right = {
        "anchors": {int(index): None if point is None else tuple(point["nose_eye_ear_normalized_xy"]) for index, point in QUARTER_RIGHT_FACE70["a"].items()},
        "points": tuple(map(tuple, QUARTER_RIGHT_FACE70["p"])),
        "provenance": "measured_fullbody_quarter_right_face70",
        "symmetry_assumption": False,
    }
    quarter_left = {
        "anchors": mirrored_body_anchors(quarter_right["anchors"]),
        "points": tuple((-quarter_right["points"][mirrored_face_index(index)][0], quarter_right["points"][mirrored_face_index(index)][1]) for index in range(70)),
        "provenance": "horizontal_reflection_of_measured_fullbody_quarter_right_face70",
        "symmetry_assumption": True,
    }
    return {(90, 0): right, (-90, 0): left, (0, 0): front, (45, 0): quarter_right, (-45, 0): quarter_left}


def map_face_to_body_anchors(observation: dict[str, object], body: list[dict[str, object] | None]) -> list[dict[str, object]]:
    """Place FACE_70 via a ratio-preserving BODY_18 anchor similarity fit."""
    source_anchors = observation["anchors"]
    pairs = []
    for index, source in source_anchors.items():
        target = body[index]
        if source is None or target is None:
            continue
        sx, sy = source
        tx, ty = target["screen_xy"]
        pairs.append((float(sx), float(sy), float(tx), float(ty)))
    if len(pairs) < 3:
        raise ValueError("FACE_70 placement requires at least three visible BODY_18 nose/eye/ear anchors")
    source_points = np.array([[sx, sy] for sx, sy, _, _ in pairs], dtype=float)
    target_points = np.array([[tx, ty] for _, _, tx, ty in pairs], dtype=float)
    source_center = source_points.mean(axis=0)
    target_center = target_points.mean(axis=0)
    source_centered = source_points - source_center
    target_centered = target_points - target_center
    covariance = source_centered.T @ target_centered
    left, singular_values, right_t = np.linalg.svd(covariance)
    rotation = left @ right_t
    if np.linalg.det(rotation) < 0:
        left[:, -1] *= -1
        rotation = left @ right_t
    source_energy = float((source_centered**2).sum())
    if source_energy <= 0:
        raise ValueError("FACE_70 source anchors must not be coincident")
    scale = float(singular_values.sum() / source_energy)
    rows = []
    for index, (sx, sy) in enumerate(observation["points"]):
        x, y = scale * ((np.array([sx, sy]) - source_center) @ rotation) + target_center
        rows.append(
            {
                "index": index,
                "screen_xy": [round(x, 3), round(y, 3)],
                "normalized_xy": [round(x / WIDTH, 6), round(y / HEIGHT, 6)],
                "confidence": 1.0,
            }
        )
    return rows


BODY18_TO_FACE70_VISUAL_ANCHORS = {
    0: (30,),                 # BODY nose -> FACE nose tip
    14: tuple(range(36, 42)), # BODY right eye -> FACE eye contour centre
    15: tuple(range(42, 48)), # BODY left eye -> FACE eye contour centre
}
FACE70_TO_BODY18_ALIGNMENT_STRENGTH = 0.65


def move_face_toward_fixed_body_head_anchors(
    face: list[dict[str, object]], body: list[dict[str, object] | None],
) -> None:
    """Partially translate FACE_70 toward fixed BODY_18 nose/eye anchors.

    BODY_18 remains one shared structural model across every yaw.  The
    observed FACE_70 shape is therefore moved as a whole, rather than
    rewriting BODY_18 head joints separately for each direction.  A partial
    correction retains the small detector-model difference while avoiding the
    visibly detached eyes and nose.
    """
    offsets = []
    for body_index, face_indices in BODY18_TO_FACE70_VISUAL_ANCHORS.items():
        if body[body_index] is None:
            continue
        face_x = sum(face[index]["screen_xy"][0] for index in face_indices) / len(face_indices)
        face_y = sum(face[index]["screen_xy"][1] for index in face_indices) / len(face_indices)
        body_x, body_y = body[body_index]["screen_xy"]
        offsets.append((body_x - face_x, body_y - face_y))
    if not offsets:
        return
    dx = sum(offset[0] for offset in offsets) / len(offsets) * FACE70_TO_BODY18_ALIGNMENT_STRENGTH
    dy = sum(offset[1] for offset in offsets) / len(offsets) * FACE70_TO_BODY18_ALIGNMENT_STRENGTH
    for row in face:
        x, y = row["screen_xy"]
        row["screen_xy"] = [round(x + dx, 3), round(y + dy, 3)]
        row["normalized_xy"] = [round((x + dx) / WIDTH, 6), round((y + dy) / HEIGHT, 6)]


def render_map(renderer, body: list[dict[str, object] | None], face: list[dict[str, object]] | None) -> Image.Image:
    body_points = [
        renderer.Keypoint(x=row["normalized_xy"][0], y=row["normalized_xy"][1], score=1.0) if row is not None else None
        for row in body
    ]
    face_points = (
        [renderer.Keypoint(x=row["normalized_xy"][0], y=row["normalized_xy"][1], score=1.0) for row in face]
        if face is not None
        else None
    )
    pose = renderer.PoseResult(
        body=renderer.BodyResult(keypoints=body_points, total_score=1.0, total_parts=sum(point is not None for point in body_points)),
        left_hand=None,
        right_hand=None,
        face=face_points,
    )
    canvas = renderer.draw_poses([pose], HEIGHT, WIDTH, draw_body=True, draw_hand=False, draw_face=face is not None)
    return Image.fromarray(np.ascontiguousarray(canvas)).convert("RGB")


def contact_sheet(entries: list[tuple[str, Image.Image]], path: Path) -> None:
    tile_w = 192
    tile_h = 192 if WIDTH == HEIGHT else 288
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
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT, help="Output location; defaults to the chapter asset root.")
    parser.add_argument("--output-label", help="Filename label used when output files are written directly to the asset root.")
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
    parser.add_argument("--include-face", action="store_true", help="Render the embedded FACE_70 nose/eye/ear-normalized maps.")
    parser.add_argument("--frame", choices=("fullbody", "shoulders"), default="fullbody", help="Output framing: fullbody or a square BODY_18 eye-nose-ear-neck-shoulder structure.")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--body-pose", choices=("neutral", "raised-arm", "hand-on-hip"), default="hand-on-hip")
    parser.add_argument(
        "--projection",
        choices=("orthographic", "perspective"),
        default="perspective",
        help="Projection model; perspective is the default so --horizontal-fov-degrees is applied.",
    )
    parser.add_argument("--camera-distance", type=float, help="Camera distance in template-head units for perspective projection; defaults depend on --frame.")
    parser.add_argument(
        "--frame-origin-y",
        type=float,
        default=None,
        help="Screen y coordinate for the nose pivot; defaults depend on --frame.",
    )
    parser.add_argument(
        "--horizontal-fov-degrees",
        type=float,
        default=DEFAULT_PERSPECTIVE_HORIZONTAL_FOV_DEGREES,
        help="Horizontal field of view for perspective projection; default is two thirds of the former effective 45.8° FOV.",
    )
    args = parser.parse_args()
    global WIDTH, HEIGHT, CENTER_X, SCALE
    if args.frame == "shoulders":
        WIDTH, HEIGHT, CENTER_X, SCALE = SHOULDERS_WIDTH, SHOULDERS_HEIGHT, SHOULDERS_WIDTH / 2, SHOULDERS_SCALE
        default_frame_origin_y = DEFAULT_SHOULDERS_FRAME_ORIGIN_Y
        default_camera_distance = DEFAULT_SHOULDERS_CAMERA_DISTANCE
    else:
        WIDTH, HEIGHT, CENTER_X, SCALE = FULLBODY_WIDTH, FULLBODY_HEIGHT, FULLBODY_WIDTH / 2, 150
        default_frame_origin_y = DEFAULT_FRAME_ORIGIN_Y
        default_camera_distance = DEFAULT_PERSPECTIVE_CAMERA_DISTANCE
    frame_origin_y = args.frame_origin_y if args.frame_origin_y is not None else default_frame_origin_y
    camera_distance = args.camera_distance if args.camera_distance is not None else default_camera_distance
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
    if camera_distance <= 1.0:
        raise ValueError("--camera-distance must be greater than 1.0")
    if not 1.0 < args.horizontal_fov_degrees < 179.0:
        raise ValueError("--horizontal-fov-degrees must be between 1 and 179")
    if not 0.0 <= frame_origin_y <= HEIGHT:
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
    face_observations = embedded_face_observations() if args.include_face else {}
    if args.include_face:
        requested_views = [(yaw, pitch) for pitch in pitches for yaw in yaws]
        missing_embedded = [view for view in requested_views if view not in face_observations]
        if missing_embedded:
            raise ValueError(f"no embedded FACE_70 map for requested views: {missing_embedded}")
    if args.output_label:
        output_label = args.output_label
    elif target_names:
        output_label = f"{args.frame}-{'-'.join(target_names)}-{'face70-nose-eye-ear' if args.include_face else 'body-only'}"
    elif args.output_range:
        output_label = f"{args.frame}-{args.output_range}-body-only"
    else:
        output_label = f"{args.frame}-custom-yaw-pitch-body-only"
    prefix = f"p7-5-2-openpose-{output_label}"
    manifest = output_dir / f"{prefix}-manifest.json"
    if manifest.exists() and not args.overwrite:
        raise FileExistsError(f"{manifest} exists; pass --overwrite to replace this generated set")
    output_dir.mkdir(parents=True, exist_ok=True)

    renderer = openpose_module()
    proportions = HUMAN_PROPORTION_PROFILES[args.proportion_profile]
    body_world = apply_body_pose(body_template(proportions), args.body_pose, proportions)
    geometry = proportion_geometry(proportions)
    face_pivot = (0.0, geometry["chin_y"] + 0.48 * geometry["head"], 0.52 * geometry["head"])
    # Keep BODY_18's five head-direction points (nose, eyes, ears) plus neck
    # and shoulders.  This is still body-only OpenPose, not the disabled
    # 70-point face landmark map.
    visible_body_indices = {0, 1, 2, 5, 14, 15, 16, 17} if args.frame == "shoulders" else None
    head_anchor_indices = {0, 14, 15, 16, 17}
    views: list[dict[str, object]] = []
    previews: list[tuple[str, Image.Image]] = []
    for row, pitch in enumerate(pitches, start=1):
        for column, yaw in enumerate(yaws, start=1):
            target_name = target_names[column - 1] if target_names and len(pitches) == 1 else None
            body = serialise_points(body_world, yaw, pitch, args.projection, camera_distance, args.horizontal_fov_degrees, face_pivot, frame_origin_y, visible_body_indices)
            if args.include_face:
                calibrate_profile_ear_depth(
                    body, body_world, yaw, pitch, args.projection, camera_distance,
                    args.horizontal_fov_degrees, face_pivot, frame_origin_y,
                )
            horizontal_crop_offset = centre_rows_horizontally(body, head_anchor_indices) if args.frame == "shoulders" else 0.0
            observation = face_observations.get((yaw, pitch)) if args.include_face else None
            if args.include_face and observation is None:
                raise ValueError(f"no embedded FACE_70 map for yaw={yaw}, pitch={pitch}")
            face = map_face_to_body_anchors(observation, body) if observation is not None else None
            if face is not None:
                move_face_toward_fixed_body_head_anchors(face, body)
            label = f"yaw{yaw:+03d}_pitch{pitch:+03d}"
            png_name = f"{prefix}-{label}.png"
            json_name = f"{prefix}-{label}.json"
            image = render_map(renderer, body, face)
            image.save(output_dir / png_name)
            view = {
                "grid_position": {"row": row, "column": column},
                "target": target_name,
                "frame": args.frame,
                "horizontal_crop_offset_px": horizontal_crop_offset,
                "yaw_degrees": yaw,
                "pitch_degrees": pitch,
                "projection": {"type": args.projection, "canvas": [WIDTH, HEIGHT], "center_xy": [CENTER_X, frame_origin_y], "pixels_per_unit": SCALE, "camera_distance": camera_distance if args.projection == "perspective" else None, "horizontal_fov_degrees": args.horizontal_fov_degrees if args.projection == "perspective" else None, "focal_length_px": round(focal_length_for_horizontal_fov(args.horizontal_fov_degrees), 3) if args.projection == "perspective" else None},
                "body_openpose_18": body,
                "face_openpose_70": face,
                "face_point_groups": FACE70_GROUPS if observation is not None else {},
                "face_observation": {"source": "embedded_code_constant", "provenance": observation["provenance"], "symmetry_assumption": observation["symmetry_assumption"]} if observation is not None else None,
                "png": png_name,
            }
            (output_dir / json_name).write_text(json.dumps(view, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            views.append({**{key: view[key] for key in ("grid_position", "target", "yaw_degrees", "pitch_degrees", "png")}, "coordinates": json_name})
            previews.append((label, image))

    sheet_name = f"{prefix}-contact-sheet.png"
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
                "method": f"BODY_18 was generated from one normalized 3D template and {args.projection} projected. FACE_70 was {'mapped from embedded nose/eye/ear-normalized code constants' if args.include_face else 'not included'}.",
                "coordinate_system": {"world": "x right, y up, z toward camera; origin at ground centre", "screen": "x right, y down", "canvas": [WIDTH, HEIGHT], "frame_origin_y": frame_origin_y, "projection": args.projection, "camera_distance": camera_distance if args.projection == "perspective" else None, "horizontal_fov_degrees": args.horizontal_fov_degrees if args.projection == "perspective" else None, "focal_length_px": round(focal_length_for_horizontal_fov(args.horizontal_fov_degrees), 3) if args.projection == "perspective" else None},
                "human_proportion_profile": {"name": args.proportion_profile, "values": proportions},
                "body_pose": args.body_pose,
                "frame": args.frame,
                "output_label": output_label,
                "view_grid": {"columns": yaws, "rows": pitches, "meaning": "columns=yaw degrees, rows=pitch degrees"},
                "targets": target_names,
                "output_range": args.output_range or "custom",
                "openpose": {"body": "BODY_18", "visible_body_indices": sorted(visible_body_indices) if visible_body_indices is not None else list(range(18)), "face_included": args.include_face, "face": "FACE_70 mapped through BODY_18 nose/eye/ear anchors and partially translated toward fixed BODY_18 nose/eye anchors" if args.include_face else None, "face70_to_fixed_body18_blend_strength": FACE70_TO_BODY18_ALIGNMENT_STRENGTH if args.include_face else None, "hands_included": False},
                "contact_sheet": sheet_name,
                "views": views,
                "limitations": [
                    "This is a proportion-editing template, not a detected pose or a character identity map.",
                    "FACE_70 observations may include a declared horizontal-symmetry assumption; those views are not detector measurements.",
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

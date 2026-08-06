"""Render a teaching blockout as line-only and depth-plus-line structure maps."""

from __future__ import annotations

from math import cos, radians, sin
from pathlib import Path

from PIL import Image, ImageDraw


OUT = Path(__file__).parent
WIDTH, HEIGHT = 640, 960
YAW_DEGREES = 32
PITCH_DEGREES = -10

JOINTS = {
    "head": (0.0, 1.80, 0.02),
    "neck": (0.0, 1.57, 0.0),
    "chest": (0.0, 1.34, 0.0),
    "pelvis": (0.0, 0.92, 0.0),
    "left_shoulder": (-0.30, 1.50, 0.02),
    "left_elbow": (-0.50, 1.18, 0.13),
    "left_wrist": (-0.43, 0.93, 0.20),
    "right_shoulder": (0.30, 1.50, -0.02),
    "right_elbow": (0.50, 1.18, -0.13),
    "right_wrist": (0.43, 0.93, -0.20),
    "left_hip": (-0.18, 0.90, 0.03),
    "left_knee": (-0.20, 0.48, 0.14),
    "left_ankle": (-0.18, 0.06, 0.20),
    "right_hip": (0.18, 0.90, -0.03),
    "right_knee": (0.24, 0.48, -0.15),
    "right_ankle": (0.20, 0.06, -0.21),
}

BONES = [
    ("head", "neck"),
    ("neck", "chest"),
    ("chest", "pelvis"),
    ("neck", "left_shoulder"),
    ("left_shoulder", "left_elbow"),
    ("left_elbow", "left_wrist"),
    ("neck", "right_shoulder"),
    ("right_shoulder", "right_elbow"),
    ("right_elbow", "right_wrist"),
    ("pelvis", "left_hip"),
    ("left_hip", "left_knee"),
    ("left_knee", "left_ankle"),
    ("pelvis", "right_hip"),
    ("right_hip", "right_knee"),
    ("right_knee", "right_ankle"),
]


def rotate(point: tuple[float, float, float]) -> tuple[float, float, float]:
    """Rotate the blockout before orthographic projection."""
    x, y, z = point
    yaw = radians(YAW_DEGREES)
    pitch = radians(PITCH_DEGREES)
    x, z = x * cos(yaw) + z * sin(yaw), -x * sin(yaw) + z * cos(yaw)
    y, z = y * cos(pitch) - z * sin(pitch), y * sin(pitch) + z * cos(pitch)
    return x, y, z


def project(points: dict[str, tuple[float, float, float]]) -> dict[str, tuple[float, float, float]]:
    rotated = {name: rotate(point) for name, point in points.items()}
    xs = [point[0] for point in rotated.values()]
    ys = [point[1] for point in rotated.values()]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    scale = min((WIDTH - 160) / (max_x - min_x), (HEIGHT - 120) / (max_y - min_y))
    return {
        name: ((x - min_x) * scale + 80, HEIGHT - ((y - min_y) * scale + 60), z)
        for name, (x, y, z) in rotated.items()
    }


def depth_gray(depth: float, low: float, high: float) -> int:
    ratio = 0.5 if high == low else (depth - low) / (high - low)
    return round(70 + ratio * 160)


def render_line_only(points: dict[str, tuple[float, float, float]]) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    for start, end in BONES:
        draw.line((points[start][:2], points[end][:2]), fill=(25, 32, 38), width=10)
    for x, y, _ in points.values():
        draw.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(25, 32, 38))
    return image


def render_depth_plus_line(points: dict[str, tuple[float, float, float]]) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), (245, 246, 247))
    draw = ImageDraw.Draw(image)
    depths = [point[2] for point in points.values()]
    low, high = min(depths), max(depths)

    # Far bones first let nearer bones cover them, making the depth order visible.
    for start, end in sorted(BONES, key=lambda bone: (points[bone[0]][2] + points[bone[1]][2]) / 2):
        depth = (points[start][2] + points[end][2]) / 2
        gray = depth_gray(depth, low, high)
        draw.line((points[start][:2], points[end][:2]), fill=(gray, gray, gray), width=26)
    for x, y, depth in points.values():
        gray = depth_gray(depth, low, high)
        draw.ellipse((x - 15, y - 15, x + 15, y + 15), fill=(gray, gray, gray))
    for start, end in BONES:
        draw.line((points[start][:2], points[end][:2]), fill=(24, 30, 35), width=4)
    return image


def main() -> None:
    points = project(JOINTS)
    render_line_only(points).save(OUT / "p7-5-6-3d-line-only.png")
    render_depth_plus_line(points).save(OUT / "p7-5-6-3d-depth-plus-line.png")


if __name__ == "__main__":
    main()

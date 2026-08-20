#!/usr/bin/env python3
"""Extract review-only BODY_18 and FACE_70 OpenPose landmarks from one image.

This utility deliberately extracts what the detector sees in a generated
reference.  It does not construct, rotate, interpolate, or correct face
coordinates.  The resulting PNG and JSON are candidates until a human has
checked that the facial direction and jaw contour are usable.

Example:
  .venv/bin/python p7_5_2_extract_openpose_landmarks.py \
    --input p7-5-2-fullbody-quarter-left-reference.png \
    --output-label fullbody-quarter-left-candidate
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import sys
import sysconfig
import types
from pathlib import Path

import numpy as np
from PIL import Image


ASSETS = Path(__file__).resolve().parent
DEFAULT_INPUT = ASSETS / "p7-5-2-fullbody-quarter-left-reference.png"
DEFAULT_OUTPUT = ASSETS
ANNOTATOR_REPOSITORY = "lllyasviel/Annotators"
FACE_GROUPS = {
    "jaw": list(range(0, 17)),
    "left_brow": list(range(17, 22)),
    "right_brow": list(range(22, 27)),
    "nose_bridge": list(range(27, 31)),
    "nose_base": list(range(31, 36)),
    "left_eye": list(range(36, 42)),
    "right_eye": list(range(42, 48)),
    "outer_lip": list(range(48, 60)),
    "inner_lip": list(range(60, 68)),
    "pupils": [68, 69],
}


def mirrored_face_index(index: int) -> int:
    """Return the detector index that corresponds to ``index`` after x-flip."""
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
    if index < 70:
        return 137 - index
    raise IndexError(index)


def mirrored_body_index(index: int) -> int:
    """Return the BODY_18 detector index that corresponds after x-flip."""
    return (0, 1, 5, 6, 7, 2, 3, 4, 11, 12, 13, 8, 9, 10, 15, 14, 17, 16)[index]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_openpose_module():
    """Load only OpenPose, avoiding unrelated optional controlnet_aux imports."""
    root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    package_name = "p7_5_2_openpose_extract_aux"
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
        raise RuntimeError("controlnet_aux OpenPose detector is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def serialise_keypoints(keypoints, width: int, height: int, *, mirrored: bool = False, face: bool = False) -> list[dict[str, object] | None]:
    rows = []
    for index in range(len(keypoints or [])):
        source_index = mirrored_face_index(index) if mirrored and face else mirrored_body_index(index) if mirrored else index
        keypoint = keypoints[source_index]
        if keypoint is None or keypoint.x < 0 or keypoint.y < 0:
            rows.append(None)
            continue
        x = 1.0 - float(keypoint.x) if mirrored else float(keypoint.x)
        rows.append(
            {
                "index": index,
                "normalized_xy": [round(x, 6), round(float(keypoint.y), 6)],
                "pixel_xy": [round(x * width, 3), round(float(keypoint.y) * height, 3)],
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--output-label", default="fullbody-quarter-left-candidate")
    parser.add_argument(
        "--face-mirror-fallback",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Retry an incomplete FACE_70 detection on a horizontally mirrored image, then restore coordinates and landmark indices.",
    )
    args = parser.parse_args()

    source = args.input if args.input.is_absolute() else ASSETS / args.input
    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    if not source.is_file():
        raise FileNotFoundError(source)
    output_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(source).convert("RGB")
    width, height = image.size
    openpose = load_openpose_module()
    detector = openpose.OpenposeDetector.from_pretrained(ANNOTATOR_REPOSITORY, local_files_only=True)
    source_pixels = np.array(image)
    poses = detector.detect_poses(source_pixels, include_face=True)
    if len(poses) != 1:
        raise RuntimeError(f"expected exactly one person, found {len(poses)}")
    pose = poses[0]
    face70_available = pose.face is not None and len(pose.face) == 70
    direct_face_point_count = len(pose.face) if pose.face is not None else 0
    mirror_fallback_face_point_count = None
    detection_pass = "direct"
    mirrored = False
    if not face70_available and args.face_mirror_fallback:
        mirrored_poses = detector.detect_poses(np.ascontiguousarray(source_pixels[:, ::-1]), include_face=True)
        mirror_fallback_face_point_count = (
            len(mirrored_poses[0].face)
            if len(mirrored_poses) == 1 and mirrored_poses[0].face is not None
            else 0
        )
        if len(mirrored_poses) == 1 and mirrored_poses[0].face is not None and len(mirrored_poses[0].face) == 70:
            poses = mirrored_poses
            pose = poses[0]
            face70_available = True
            detection_pass = "horizontal_mirror_fallback"
            mirrored = True

    prefix = f"p7-5-2-openpose-extraction-{args.output_label}"

    output_png = output_dir / f"{prefix}.png"
    output_json = output_dir / f"{prefix}.json"
    canvas = openpose.draw_poses(poses, height, width, draw_body=True, draw_hand=False, draw_face=face70_available)
    if mirrored:
        canvas = np.ascontiguousarray(canvas[:, ::-1])
    Image.fromarray(canvas).save(output_png)

    record = {
        "status": "review_required" if face70_available else "face70_incomplete",
        "kind": "detector_extraction_not_synthetic_relation_map",
        "source": {"path": str(source), "sha256": sha256(source), "size": [width, height]},
        "detector": {
            "repository": ANNOTATOR_REPOSITORY,
            "local_files_only": True,
            "controlnet_aux_version": importlib.metadata.version("controlnet-aux"),
            "person_count": len(poses),
            "detection_pass": detection_pass,
            "horizontal_mirror_fallback_enabled": args.face_mirror_fallback,
            "direct_face_point_count": direct_face_point_count,
            "mirror_fallback_face_point_count": mirror_fallback_face_point_count,
            "face_point_count": len(pose.face) if pose.face is not None else 0,
            "face70_available": face70_available,
        },
        "body_openpose_18": serialise_keypoints(pose.body.keypoints, width, height, mirrored=mirrored),
        "face_openpose_70": serialise_keypoints(pose.face, width, height, mirrored=mirrored, face=True) if face70_available else None,
        "face_groups": FACE_GROUPS,
        "output": {"path": str(output_png), "sha256": sha256(output_png)},
        "decision": (
            "Candidate only. Approve the detected jaw and facial direction before using these coordinates as a reference map."
            if face70_available
            else "FACE_70 is incomplete. Do not use this view for face_template fitting; regenerate the source or use a detector that supports this profile."
        ),
    }
    output_json.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"png": str(output_png), "json": str(output_json)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

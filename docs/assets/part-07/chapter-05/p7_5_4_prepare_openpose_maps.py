#!/usr/bin/env python3
"""Save reusable OpenPose maps for the approved P7-5.2 full-body references."""

from __future__ import annotations

import importlib.util
import sys
import sysconfig
import types
from pathlib import Path

from PIL import Image


ASSETS = Path(__file__).resolve().parent
ANNOTATORS = Path(
    "/home/cbsim/.cache/huggingface/hub/models--lllyasviel--Annotators/"
    "snapshots/982e7edaec38759d914a963c48c4726685de7d96"
)
REFERENCES = {
    "front": "p7-5-2-fullbody-front-reference.png",
    "front-quarter-right": "p7-5-2-fullbody-front-quarter-right-reference.png",
    "profile-left": "p7-5-2-fullbody-profile-left-reference.png",
    "profile-right": "p7-5-2-fullbody-profile-right-reference.png",
    "rear": "p7-5-2-fullbody-rear-reference.png",
}


def detector_class():
    root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    parent = types.ModuleType("p7_5_4_openpose_assets_aux")
    parent.__path__ = [str(root)]
    sys.modules[parent.__name__] = parent
    directory = root / "open_pose"
    spec = importlib.util.spec_from_file_location(
        "p7_5_4_openpose_assets_aux.open_pose",
        directory / "__init__.py",
        submodule_search_locations=[str(directory)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("OpenPose implementation is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.OpenposeDetector


def main() -> int:
    detector = detector_class().from_pretrained(ANNOTATORS)
    for label, filename in REFERENCES.items():
        source = ASSETS / filename
        if not source.is_file():
            raise FileNotFoundError(source)
        output = ASSETS / f"p7-5-4-openpose-fullbody-{label}-reference.png"
        pose = detector(Image.open(source).convert("RGB"), hand_and_face=False).convert("RGB")
        if pose.size != Image.open(source).size:
            pose = pose.resize(Image.open(source).size, Image.Resampling.NEAREST)
        pose.save(output)
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Extract a body-only OpenPose map from an explicitly selected reference image."""

from __future__ import annotations

import argparse
import importlib.util
import sys
import sysconfig
import types
from pathlib import Path

from huggingface_hub import snapshot_download
from PIL import Image


ASSETS = Path(__file__).resolve().parent.parent
ANNOTATOR_REPOSITORY = "lllyasviel/Annotators"
HF_HUB_CACHE = ASSETS.parents[3] / ".tmp" / "download" / "huggingface" / "hub"
OUTPUT_DIR = Path(__file__).resolve().parent


def detector_class():
    root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    parent = types.ModuleType("p7_5_16_openpose_assets_aux")
    parent.__path__ = [str(root)]
    sys.modules[parent.__name__] = parent
    directory = root / "open_pose"
    spec = importlib.util.spec_from_file_location(
        "p7_5_16_openpose_assets_aux.open_pose",
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-image", type=Path, required=True)
    parser.add_argument("--output", type=Path,
                        default=OUTPUT_DIR / "p7-5-16-openpose-body-reference.png")
    args = parser.parse_args()
    source = args.reference_image.resolve()
    if not source.is_file():
        parser.error(f"Reference image does not exist: {source}")
    output = args.output.resolve()
    if output == source:
        parser.error("Output must differ from the reference image")
    annotator_path = Path(
        snapshot_download(ANNOTATOR_REPOSITORY, cache_dir=HF_HUB_CACHE, local_files_only=True)
    )
    detector = detector_class().from_pretrained(annotator_path, local_files_only=True)
    with Image.open(source) as opened:
        image = opened.convert("RGB")
    pose = detector(image, hand_and_face=False).convert("RGB")
    if pose.size != image.size:
        pose = pose.resize(image.size, Image.Resampling.NEAREST)
    output.parent.mkdir(parents=True, exist_ok=True)
    pose.save(output)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

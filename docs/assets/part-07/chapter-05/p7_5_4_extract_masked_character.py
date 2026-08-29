#!/usr/bin/env python3
"""Extract a transparent character cutout from a camera-angle scene and person mask."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


ASSETS = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", type=Path, required=True)
    parser.add_argument("--mask", type=Path, required=True, help="White=character, black=background.")
    parser.add_argument("--matte", choices=("transparent", "black", "white"), default="transparent", help="Opaque black/white mattes are for Qwen pose-reference images.")
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    scene, mask = args.scene.resolve(), args.mask.resolve()
    if not scene.is_file() or not mask.is_file():
        raise FileNotFoundError("--scene and --mask must exist")
    rgb = Image.open(scene).convert("RGB")
    alpha = Image.open(mask).convert("L")
    if rgb.size != alpha.size:
        alpha = alpha.resize(rgb.size, Image.Resampling.NEAREST)
    if args.matte == "transparent":
        cutout = rgb.convert("RGBA")
        cutout.putalpha(alpha)
    else:
        cutout = Image.composite(rgb, Image.new("RGB", rgb.size, args.matte), alpha)
    role = f"pose-cutout-{args.matte}" if args.matte in {"black", "white"} else "cutout"
    stem = f"p7-5-3-character-{role}-{args.run_label}"
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output, result = output_dir / f"{stem}.png", output_dir / f"{stem}-result.json"
    cutout.save(output)
    result.write_text(json.dumps({"status": "generated", "stage": "character_cutout", "scene": {"path": str(scene), "sha256": sha256(scene)}, "mask": {"path": str(mask), "sha256": sha256(mask), "semantics": "white=character; black=background"}, "matte": args.matte, "output": {"path": str(output), "sha256": sha256(output)}}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

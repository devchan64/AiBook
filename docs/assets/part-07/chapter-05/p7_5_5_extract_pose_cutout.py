#!/usr/bin/env python3
"""Extract one camera-frame character pose onto a white 1:1 canvas.

The source camera image determines the pose, framing, and perspective.  Its
matching SAM2 mask supplies the only editable boundary: white mask pixels are
copied from the source, and every other pixel is replaced with white.  This
creates a pose reference, not a transparent compositing asset.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from PIL import Image


ASSETS = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, type=Path, help="Camera-frame image containing one person.")
    parser.add_argument("--mask", required=True, type=Path, help="Matching SAM2 mask; white=person, black=background.")
    parser.add_argument("--scene", choices=("a", "b", "c"), required=True)
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--size", type=int, default=1280, help="Square output edge; must be a multiple of 32.")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if args.size < 32 or args.size % 32:
        parser.error("--size must be a positive multiple of 32")

    reference = args.reference.resolve()
    mask_path = args.mask.resolve()
    if not reference.is_file() or not mask_path.is_file():
        raise FileNotFoundError("--reference and --mask must exist")

    started = time.monotonic()
    with Image.open(reference) as source:
        image = source.convert("RGB").resize((args.size, args.size), Image.Resampling.LANCZOS)
    with Image.open(mask_path) as source:
        mask = source.convert("L").resize((args.size, args.size), Image.Resampling.NEAREST)
    white = Image.new("RGB", image.size, "white")
    cutout = Image.composite(image, white, mask)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = (
        f"p7-5-5-character-pose-cutout-white-official-camera-scene-{args.scene}-"
        f"{args.run_label}-size-{args.size}x{args.size}"
    )
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    cutout.save(output)
    result.write_text(
        json.dumps(
            {
                "status": "generated",
                "stage": "white_background_pose_cutout",
                "purpose": "Pose, framing, and perspective reference for later character identity transfer",
                "inputs": {
                    "camera_frame": {"path": str(reference), "sha256": sha256(reference)},
                    "person_mask": {
                        "path": str(mask_path),
                        "sha256": sha256(mask_path),
                        "semantics": "white=source character copied; black=white background",
                    },
                },
                "output": {"path": str(output), "sha256": sha256(output), "width": args.size, "height": args.size},
                "canvas": "opaque white; this is a pose reference, not an alpha compositing asset",
                "elapsed_seconds": round(time.monotonic() - started, 2),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Extract face-only OpenPose maps from a regular face-turnaround contact sheet.

The source sheet is not an identity reference or an approved pose guide. This
script separates its regular grid, detects only the OpenPose face landmarks in
each cell, and writes review candidates. Inspect every output before using it
as a structural condition: profile and steep-down views can have missing or
misplaced landmarks.

Example:
  .venv/bin/python p7_5_2_extract_face_turnaround_openpose.py \
    --source /path/to/face-turnaround.png --columns 5 --rows 3 \
    --annotators /path/to/models--lllyasviel--Annotators/snapshots/<revision>
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import sysconfig
import types
from pathlib import Path

from PIL import Image, ImageOps


ASSETS = Path(__file__).resolve().parent
ANNOTATORS = Path(
    "/home/cbsim/.cache/huggingface/hub/models--lllyasviel--Annotators/"
    "snapshots/982e7edaec38759d914a963c48c4726685de7d96"
)


def detector_class():
    """Load the OpenPose submodule without importing unrelated annotators."""
    root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    parent = types.ModuleType("p7_5_2_face_turnaround_openpose_aux")
    parent.__path__ = [str(root)]
    sys.modules[parent.__name__] = parent
    directory = root / "open_pose"
    spec = importlib.util.spec_from_file_location(
        "p7_5_2_face_turnaround_openpose_aux.open_pose",
        directory / "__init__.py",
        submodule_search_locations=[str(directory)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("controlnet_aux OpenPose implementation is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.OpenposeDetector


def grid_cell_bounds(image: Image.Image, row: int, column: int, rows: int, columns: int) -> tuple[int, int, int, int]:
    left = round(column * image.width / columns)
    right = round((column + 1) * image.width / columns)
    top = round(row * image.height / rows)
    bottom = round((row + 1) * image.height / rows)
    return left, top, right, bottom


def crop_visible_face(cell: Image.Image, *, background_threshold: int, padding: int) -> Image.Image:
    """Trim a near-white sheet background while retaining a configurable margin."""
    grayscale = ImageOps.grayscale(cell)
    foreground = grayscale.point(lambda value: 255 if value < background_threshold else 0)
    bounds = foreground.getbbox()
    if bounds is None:
        raise ValueError("No non-background pixels were found in a grid cell")
    left, top, right, bottom = bounds
    return cell.crop(
        (
            max(0, left - padding),
            max(0, top - padding),
            min(cell.width, right + padding),
            min(cell.height, bottom + padding),
        )
    )


def make_contact_sheet(images: list[Image.Image], *, columns: int, cell_size: int) -> Image.Image:
    rows = (len(images) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_size, rows * cell_size), "white")
    for index, image in enumerate(images):
        thumbnail = ImageOps.contain(image, (cell_size, cell_size), Image.Resampling.NEAREST)
        left = (index % columns) * cell_size + (cell_size - thumbnail.width) // 2
        top = (index // columns) * cell_size + (cell_size - thumbnail.height) // 2
        sheet.paste(thumbnail, (left, top))
    return sheet


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="5×3 face-turnaround contact sheet")
    parser.add_argument("--output-dir", type=Path, default=ASSETS / "p7-5-2-face-turnaround-openpose-candidates")
    parser.add_argument("--annotators", type=Path, default=ANNOTATORS, help="Local lllyasviel/Annotators snapshot")
    parser.add_argument("--columns", type=int, default=5)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--detect-resolution", type=int, default=512)
    parser.add_argument("--background-threshold", type=int, default=245)
    parser.add_argument("--padding", type=int, default=12)
    parser.add_argument("--contact-cell-size", type=int, default=256)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if args.columns < 1 or args.rows < 1:
        raise ValueError("--columns and --rows must be positive")
    if not 1 <= args.background_threshold <= 255:
        raise ValueError("--background-threshold must be between 1 and 255")
    if args.padding < 0 or args.detect_resolution < 16 or args.contact_cell_size < 16:
        raise ValueError("--padding must be non-negative; resolutions must be at least 16")
    if not args.source.is_file():
        raise FileNotFoundError(args.source)
    if not args.annotators.is_dir():
        raise FileNotFoundError(f"OpenPose annotator snapshot not found: {args.annotators}")

    output_dir = args.output_dir if args.output_dir.is_absolute() else ASSETS / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    record_path = output_dir / "face-openpose-extraction-review.json"
    contact_path = output_dir / "face-openpose-contact-sheet.png"
    if not args.overwrite and (record_path.exists() or contact_path.exists()):
        raise FileExistsError("Output already exists; choose a new --output-dir or pass --overwrite")

    source = Image.open(args.source).convert("RGB")
    detector = detector_class().from_pretrained(args.annotators, local_files_only=True)
    face_maps: list[Image.Image] = []
    records: list[dict[str, object]] = []
    for row in range(args.rows):
        for column in range(args.columns):
            cell = source.crop(grid_cell_bounds(source, row, column, args.rows, args.columns))
            face_crop = crop_visible_face(
                cell,
                background_threshold=args.background_threshold,
                padding=args.padding,
            ).convert("RGB")
            output_name = f"face-r{row + 1:02d}-c{column + 1:02d}-openpose.png"
            output_path = output_dir / output_name
            if output_path.exists() and not args.overwrite:
                raise FileExistsError(f"{output_path} already exists; pass --overwrite to replace it")
            face_map = detector(
                face_crop,
                detect_resolution=args.detect_resolution,
                image_resolution=max(face_crop.size),
                include_body=False,
                include_hand=False,
                include_face=True,
                output_type="pil",
            ).convert("RGB")
            if face_map.size != face_crop.size:
                face_map = face_map.resize(face_crop.size, Image.Resampling.NEAREST)
            face_map.save(output_path)
            face_maps.append(face_map)
            records.append(
                {
                    "grid_position": {"row": row + 1, "column": column + 1},
                    "output": output_name,
                    "crop_size": list(face_crop.size),
                    "status": "review_required",
                }
            )

    make_contact_sheet(face_maps, columns=args.columns, cell_size=args.contact_cell_size).save(contact_path)
    record_path.write_text(
        json.dumps(
            {
                "status": "review_required",
                "source": str(args.source),
                "detector": "controlnet_aux OpenposeDetector from lllyasviel/Annotators",
                "annotators": str(args.annotators),
                "grid": {"columns": args.columns, "rows": args.rows},
                "face_only": True,
                "body_included": False,
                "hands_included": False,
                "contact_sheet": contact_path.name,
                "outputs": records,
                "review_note": "Inspect all fifteen maps before using them as structural inputs; no map is an identity or style approval.",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(contact_path)
    print(record_path)


if __name__ == "__main__":
    main()

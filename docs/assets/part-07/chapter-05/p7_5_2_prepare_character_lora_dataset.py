#!/usr/bin/env python3
"""Prepare the approved P7-5.2 face and full-body references for a character LoRA.

This script does not generate a new image and does not train an adapter.  It
places links and tag captions for the six faces, six basic full-body views, and
six refined full-body views in a local training directory.  The 18 sources stay
in their stable approved locations; no duplicate PNG is added to the repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT.parents[3] / ".tmp" / "p7-5-2-character-lora-dataset"
VIEWS = ("front", "front_quarter_left", "front_quarter_right", "profile_left", "profile_right", "rear")
VIEW_TAGS = {
    "front": "front view",
    "front_quarter_left": "left three-quarter view",
    "front_quarter_right": "right three-quarter view",
    "profile_left": "left profile",
    "profile_right": "right profile",
    "rear": "back view",
}
CORE_IDENTITY = (
    "p7mira, 1girl, solo, adult Korean woman, very fair pale-peach skin, "
    "deep petrol-teal jaw-length bob, chestnut-brown and amber eyes, webtoon style, clean lineart"
)
BASE_OUTFIT = "charcoal gray crop top, bare midriff, deep teal wide-leg trousers, white low-top sneakers"
REFINED_OUTFIT = (
    "white cropped utility jacket, charcoal gray crop top, bare midriff, deep teal wide-leg trousers, "
    "white low-top sneakers, deep navy crossbody messenger bag"
)
CONTACT_SHEET_COLUMNS = 3
CONTACT_SHEET_CELL_SIZE = (240, 360)
CONTACT_SHEET_LABEL_HEIGHT = 26


@dataclass(frozen=True)
class Source:
    source_id: str
    asset: str
    source_type: str
    view: str
    caption: str


def source_catalog() -> tuple[Source, ...]:
    faces = tuple(
        Source(
            source_id=f"p7-5-2-character-lora-face-{view}",
            asset=f"p7-5-2-face-{view.replace('_', '-')}-reference.png",
            source_type="face_identity",
            view=view,
            caption=f"{CORE_IDENTITY}, face portrait, {VIEW_TAGS[view]}",
        )
        for view in VIEWS
    )
    basic_bodies = tuple(
        Source(
            source_id=f"p7-5-2-character-lora-body-{view}",
            asset=f"p7-5-2-fullbody-{view.replace('_', '-')}-reference.png",
            source_type="fullbody_basic",
            view=view,
            caption=f"{CORE_IDENTITY}, {BASE_OUTFIT}, full body, standing, {VIEW_TAGS[view]}",
        )
        for view in VIEWS
    )
    refined_bodies = tuple(
        Source(
            source_id=f"p7-5-2-character-lora-refined-{view}",
            asset=f"p7-5-2-fullbody-{view.replace('_', '-')}-refined-reference.png",
            source_type="fullbody_refined",
            view=view,
            caption=f"{CORE_IDENTITY}, {REFINED_OUTFIT}, full body, standing, {VIEW_TAGS[view]}",
        )
        for view in VIEWS
    )
    return faces + basic_bodies + refined_bodies


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Local directory for image links, captions, and manifest.")
    parser.add_argument("--plan-only", action="store_true", help="Validate and print the 18 source records without writing files.")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_sources() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for source in source_catalog():
        path = ROOT / source.asset
        if not path.is_file():
            raise FileNotFoundError(f"approved P7-5.2 source is missing: {path}")
        record = asdict(source)
        record["sha256"] = sha256(path)
        records.append(record)
    if len(records) != 18:
        raise ValueError("the character LoRA input must contain six faces plus twelve full-body sources")
    if len({record["sha256"] for record in records}) != len(records):
        raise ValueError("the character LoRA input contains duplicate image sources")
    return records


def link_or_validate(source: Path, destination: Path) -> None:
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() and destination.resolve() == source.resolve():
            return
        raise FileExistsError(f"refusing to replace existing dataset entry: {destination}")
    os.symlink(source, destination)


def write_contact_sheet(output: Path, records: list[dict[str, str]]) -> str:
    """Render a review image without changing any training source PNG."""
    cell_width, cell_height = CONTACT_SHEET_CELL_SIZE
    rows = (len(records) + CONTACT_SHEET_COLUMNS - 1) // CONTACT_SHEET_COLUMNS
    sheet = Image.new(
        "RGB",
        (CONTACT_SHEET_COLUMNS * cell_width, rows * (cell_height + CONTACT_SHEET_LABEL_HEIGHT)),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    for index, record in enumerate(records):
        source = ROOT / record["asset"]
        image = Image.open(source).convert("RGB")
        image.thumbnail(CONTACT_SHEET_CELL_SIZE, Image.Resampling.LANCZOS)
        column, row = index % CONTACT_SHEET_COLUMNS, index // CONTACT_SHEET_COLUMNS
        left, top = column * cell_width, row * (cell_height + CONTACT_SHEET_LABEL_HEIGHT)
        sheet.paste(image, (left + (cell_width - image.width) // 2, top + (cell_height - image.height) // 2))
        draw.text((left + 6, top + cell_height + 5), record["source_id"], fill="black")
    name = "character-lora-source-contact-sheet.png"
    sheet.save(output / name)
    return name


def write_dataset(output: Path, records: list[dict[str, str]]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for record in records:
        source = ROOT / record["asset"]
        image_name = f"{record['source_id']}.png"
        image_path = output / image_name
        link_or_validate(source, image_path)
        caption_path = output / f"{record['source_id']}.txt"
        caption_path.write_text(record["caption"] + "\n", encoding="utf-8")
        record["dataset_image"] = image_name
        record["dataset_caption"] = caption_path.name
    contact_sheet = write_contact_sheet(output, records)
    manifest = {
        "dataset_id": "p7-5-2-character-lora-approved-18",
        "status": "prepared_from_human_approved_sources",
        "purpose": "Additional identity and outfit data for a later character-LoRA experiment.",
        "input_rule": "Six face identity sources, six basic full-body sources, and six refined full-body sources. The data preparation step does not approve a LoRA or broaden pose, camera, or scene scope.",
        "image_link_mode": "symlink",
        "review_contact_sheet": contact_sheet,
        "counts": {"face_identity": 6, "fullbody_basic": 6, "fullbody_refined": 6, "total": 18},
        "sources": records,
    }
    (output / "dataset-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    records = resolve_sources()
    if args.plan_only:
        print(json.dumps({"status": "validated", "count": len(records), "sources": records}, ensure_ascii=False, indent=2))
        return 0
    write_dataset(args.output, records)
    print(
        json.dumps(
            {"status": "prepared", "output": str(args.output), "count": len(records), "review_contact_sheet": "character-lora-source-contact-sheet.png"},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

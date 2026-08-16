#!/usr/bin/env python3
"""Prepare approved identity anchors and P7-5.4 action images for character-LoRA training.

The approved PNG files stay in the documentation asset directory.  This tool
creates a local training directory containing symbolic links, one caption per
image, and a reproducible manifest.  It does not train an adapter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


ASSETS = Path(__file__).resolve().parent
DATASET_ASSETS = ASSETS / "p7-5-4-character-lora-54"
ACTION_ASSETS = DATASET_ASSETS / "actions"
DEFAULT_OUTPUT = ASSETS.parents[3] / ".tmp" / "p7-5-4-character-lora-identity-action-54"
APPROVED = {
    "approved_for_character_lora_candidate_pool",
    "approved_for_styled_character_lora_dataset",
}
ACTION_COUNT = 36
CORE_IDENTITY_COUNT = 18
EXPECTED_COUNT = ACTION_COUNT + CORE_IDENTITY_COUNT
SOURCE_MANIFEST = DATASET_ASSETS / "dataset-manifest.json"
IDENTITY = "p7mira, adult Korean woman, petrol-teal jaw-length bob, amber eyes, webtoon watercolor"
VIEWS = ("front", "front_quarter_left", "front_quarter_right", "profile_left", "profile_right", "rear")
VIEW_TAGS = {
    "front": "front view", "front_quarter_left": "left three-quarter view", "front_quarter_right": "right three-quarter view",
    "profile_left": "left profile", "profile_right": "right profile", "rear": "back view",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--plan-only", action="store_true")
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Write only the source manifest; do not create local training links or captions.",
    )
    parser.add_argument(
        "--manifest-output",
        type=Path,
        default=DATASET_ASSETS / "dataset-manifest.json",
        help="Path for the checked-in source manifest used by the manuscript.",
    )
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def core_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for view in VIEWS:
        records.append({"source_id": f"identity-face-{view}", "image": f"p7-5-2-face-{view.replace('_', '-')}-reference.png", "caption": f"{IDENTITY}, face portrait, {VIEW_TAGS[view]}", "view": view, "pose_family": "face_identity"})
        records.append({"source_id": f"identity-basic-{view}", "image": f"p7-5-2-fullbody-{view.replace('_', '-')}-reference.png", "caption": f"{IDENTITY}, full body, standing, charcoal crop top, teal wide-leg trousers, white sneakers, {VIEW_TAGS[view]}", "view": view, "pose_family": "turnaround_basic"})
        records.append({"source_id": f"identity-refined-{view}", "image": f"p7-5-2-fullbody-{view.replace('_', '-')}-refined-reference.png", "caption": f"{IDENTITY}, full body, white cropped jacket, charcoal crop top, teal wide-leg trousers, white sneakers, navy crossbody bag, {VIEW_TAGS[view]}", "view": view, "pose_family": "turnaround_refined"})
    for record in records:
        image_path = ASSETS / str(record["image"])
        if not image_path.is_file():
            raise FileNotFoundError(f"identity anchor missing: {image_path}")
        record["sha256"] = sha256(image_path)
        record["review"] = "approved P7-5.2 reference"
    return records


def approved_records() -> list[dict[str, object]]:
    source_manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    source_records = {
        str(record["source_id"]): record
        for record in source_manifest["sources"]
        if str(record["source_id"]).startswith(("pose-extra-", "sport-"))
    }
    records: list[dict[str, object]] = []
    for review_path in sorted(ACTION_ASSETS.glob("p7-5-4-character-lora-pose-stage2-*-reference-review.json")):
        review = json.loads(review_path.read_text(encoding="utf-8"))
        if review.get("status") not in APPROVED:
            continue
        image_path = review_path.parent / str(review["output"])
        if not image_path.is_file():
            raise FileNotFoundError(f"approved image missing: {image_path}")
        source_record = source_records.get(str(review["candidate_id"]))
        if source_record is None:
            raise ValueError(f"approved action missing from source manifest: {review['candidate_id']}")
        if source_record["image"] != image_path.relative_to(ASSETS).as_posix():
            raise ValueError(f"manifest image mismatch: {review['candidate_id']}")
        if source_record["review"] != review_path.relative_to(ASSETS).as_posix():
            raise ValueError(f"manifest review mismatch: {review['candidate_id']}")
        records.append(
            {
                "source_id": str(review["candidate_id"]),
                "image": image_path.relative_to(ASSETS).as_posix(),
                "review": review_path.relative_to(ASSETS).as_posix(),
                "caption": str(source_record["caption"]),
                "sha256": sha256(image_path),
                "view": str(source_record["view"]),
                "pose_family": str(source_record["pose_family"]),
            }
        )
    if len(records) != ACTION_COUNT:
        raise ValueError(f"expected {ACTION_COUNT} approved action images, found {len(records)}")
    return core_records() + records


def link(source: Path, destination: Path) -> None:
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() and destination.resolve() == source.resolve():
            return
        raise FileExistsError(f"refusing to replace dataset entry: {destination}")
    os.symlink(source, destination)


def manifest(records: list[dict[str, object]]) -> dict[str, object]:
    return {
        "dataset_id": "p7-5-4-character-lora-approved-identity-action-54",
        "status": "prepared_from_human_approved_sources",
        "purpose": "Character identity anchors plus style-conditioned full-body pose diversity for a later character-LoRA experiment.",
        "image_link_mode": "symlink_when_prepared_locally",
        "counts": {"identity_anchors": CORE_IDENTITY_COUNT, "approved_action_images": ACTION_COUNT, "total": EXPECTED_COUNT},
        "sources": records,
    }


def write_manifest(output: Path, records: list[dict[str, object]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest(records), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_dataset(output: Path, records: list[dict[str, object]]) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for index, record in enumerate(records, start=1):
        image = ASSETS / str(record["image"])
        stem = f"{index:02d}-{record['source_id']}"
        image_name = f"{stem}.png"
        link(image, output / image_name)
        caption_name = f"{stem}.txt"
        (output / caption_name).write_text(str(record["caption"]) + "\n", encoding="utf-8")
        record["dataset_image"] = image_name
        record["dataset_caption"] = caption_name
    write_manifest(output / "dataset-manifest.json", records)


def main() -> int:
    args = parse_args()
    records = approved_records()
    if args.plan_only:
        print(json.dumps({"status": "validated", "count": len(records), "sources": records}, ensure_ascii=False, indent=2))
        return 0
    if args.manifest_only:
        write_manifest(args.manifest_output, records)
        print(json.dumps({"status": "manifest_written", "count": len(records), "output": str(args.manifest_output)}, ensure_ascii=False))
        return 0
    write_dataset(args.output, records)
    print(json.dumps({"status": "prepared", "count": len(records), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

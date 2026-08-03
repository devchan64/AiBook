#!/usr/bin/env python3
"""Materialize the approved P7-5.1 train and held-out image sets without cropping."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


IDENTITY_CAPTION = (
    "p7mira, adult Korean webtoon woman, jaw-length teal-blue bob, "
    "small silver hair clip on right-side bangs, dark brown eyes, white cropped "
    "utility jacket, charcoal crew-neck shirt, high-waisted teal wide-leg trousers, "
    "white sneakers, one navy horizontal flap messenger bag at right hip, one "
    "continuous navy diagonal strap from left shoulder to bag, clean restrained "
    "webtoon line art, low-saturation flat colors"
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("manifest", type=Path)
    result.add_argument("output_dir", type=Path)
    result.add_argument(
        "--copy-images",
        action="store_true",
        help="Copy images instead of creating relative symbolic links.",
    )
    return result


def write_split(
    split_name: str,
    items: list[dict[str, str]],
    source_by_id: dict[str, dict[str, object]],
    assets_dir: Path,
    output_dir: Path,
    copy_images: bool,
) -> int:
    split_dir = output_dir / split_name
    split_dir.mkdir(parents=True, exist_ok=True)
    metadata_path = split_dir / "metadata.jsonl"
    rows: list[str] = []

    for item in items:
        source = source_by_id[item["source_id"]]
        source_path = assets_dir / item["file"]
        target_path = split_dir / item["file"]
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        if target_path.exists() or target_path.is_symlink():
            target_path.unlink()
        if copy_images:
            shutil.copy2(source_path, target_path)
        else:
            target_path.symlink_to(source_path.resolve())

        caption_parts = [IDENTITY_CAPTION]
        for key in ("scene", "camera", "action", "lighting"):
            value = source.get(key)
            if value:
                caption_parts.append(str(value).replace("_", " "))
        rows.append(
            json.dumps(
                {
                    "file_name": target_path.name,
                    "text": ", ".join(caption_parts),
                    "source_id": item["source_id"],
                    "split": split_name,
                },
                ensure_ascii=True,
            )
        )

    metadata_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return len(rows)


def main() -> int:
    args = parser().parse_args()
    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["character_reference_pack"]["approval_status"] != "approved":
        raise RuntimeError("reference pack is not approved")

    assets_dir = manifest_path.parent
    train_sources = {item["source_id"]: item for item in manifest["scene_reference_images"]}
    heldout_sources = {item["source_id"]: item for item in manifest["heldout_reference_images"]}
    train_items = manifest["dataset"]["train_items"]
    heldout_items = manifest["dataset"]["heldout_items"]

    train_ids = {item["source_id"] for item in train_items}
    heldout_ids = {item["source_id"] for item in heldout_items}
    if train_ids & heldout_ids:
        raise RuntimeError("train and held-out source IDs overlap")
    if len(train_items) < manifest["dataset"]["train_minimum"]:
        raise RuntimeError("train set is smaller than train_minimum")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    train_count = write_split(
        "train", train_items, train_sources, assets_dir, args.output_dir, args.copy_images
    )
    heldout_count = write_split(
        "heldout", heldout_items, heldout_sources, assets_dir, args.output_dir, args.copy_images
    )
    (args.output_dir / "dataset-summary.json").write_text(
        json.dumps(
            {
                "experiment_id": manifest["experiment_id"],
                "preprocessing": "source PNG only; no crop, panel split, or resize",
                "train_count": train_count,
                "heldout_count": heldout_count,
                "image_mode": "copy" if args.copy_images else "symlink",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"prepared train={train_count} heldout={heldout_count} at {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

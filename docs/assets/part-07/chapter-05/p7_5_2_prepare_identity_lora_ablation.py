#!/usr/bin/env python3
"""Create an identity-only LoRA dataset from approved full-body reference views."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


IDENTITY_CAPTION = (
    "p7mira, woman, teal bob, silver right hair clip, dark eyes, white cropped jacket, "
    "charcoal shirt, teal wide-leg trousers, white sneakers, navy flap crossbody bag at "
    "right hip, one diagonal strap, clean webtoon line art, low-saturation flat colors"
)


def write_link(source: Path, target: Path) -> None:
    if target.exists() or target.is_symlink():
        target.unlink()
    target.symlink_to(source.resolve())


def caption(item: dict[str, object]) -> str:
    camera = str(item.get("camera", "full body")).replace("_", " ")
    return ", ".join((IDENTITY_CAPTION, camera, "full body"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["character_reference_pack"]["approval_status"] != "approved":
        raise RuntimeError("the reference pack is not approved")
    assets_dir = manifest_path.parent
    train_dir = args.output_dir / "train"
    heldout_dir = args.output_dir / "heldout"
    train_dir.mkdir(parents=True, exist_ok=True)
    heldout_dir.mkdir(parents=True, exist_ok=True)

    references = [
        item for item in manifest["character_reference_pack"]["reference_images"]
        if item.get("status") != "rejected"
    ]
    if len(references) < 16:
        raise RuntimeError("identity-only ablation requires at least 16 approved full-body references")
    train_rows: list[dict[str, str]] = []
    for item in references:
        source = assets_dir / str(item["file"])
        if not source.is_file():
            raise FileNotFoundError(source)
        write_link(source, train_dir / source.name)
        train_rows.append({"file_name": source.name, "text": caption(item), "source_id": str(item["source_id"])})

    heldout_by_id = {item["source_id"]: item for item in manifest["heldout_reference_images"]}
    heldout_rows: list[dict[str, str]] = []
    for item in manifest["dataset"]["heldout_items"]:
        source = heldout_by_id[item["source_id"]]
        source_path = assets_dir / item["file"]
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        write_link(source_path, heldout_dir / source_path.name)
        heldout_rows.append({"file_name": source_path.name, "source_id": str(item["source_id"])})

    (train_dir / "metadata.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=True) for row in train_rows) + "\n", encoding="utf-8"
    )
    (heldout_dir / "metadata.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=True) for row in heldout_rows) + "\n", encoding="utf-8"
    )
    (args.output_dir / "dataset-summary.json").write_text(json.dumps({
        "experiment": "P7-5.1 identity-only LoRA data ablation",
        "train_role": "approved full-body character views only; no scene images, face crops, or hand-detail images",
        "heldout_role": "unchanged four scene-and-camera images from the baseline experiment",
        "preprocessing": "source PNG only; no crop, panel split, or resize",
        "train_count": len(train_rows),
        "heldout_count": len(heldout_rows),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"prepared identity-only train={len(train_rows)} heldout={len(heldout_rows)} at {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

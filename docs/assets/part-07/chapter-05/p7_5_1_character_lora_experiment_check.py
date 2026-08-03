#!/usr/bin/env python3
"""Validate the P7-5.1 character LoRA experiment before training."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    manifest_path = Path(__import__("sys").argv[1])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pack = manifest["character_reference_pack"]
    dataset = manifest["dataset"]
    messages: list[str] = []

    missing_views = sorted(set(pack["required_views"]) - set(pack["approved_views"]))
    if pack["rights_confirmation"] in {"", "pending", None}:
        messages.append("BLOCKED rights_confirmation is required")
    if pack["approval_status"] != "approved":
        messages.append("BLOCKED character_reference_pack is not approved")
    if missing_views:
        messages.append(f"BLOCKED missing approved views: {', '.join(missing_views)}")
    if len(dataset["train_items"]) < dataset["train_minimum"]:
        messages.append("BLOCKED train_items is below train_minimum")

    for item in pack.get("reference_images", []):
        if item["status"] == "rejected":
            continue
        if not (manifest_path.parent / item["file"]).is_file():
            messages.append(f"BLOCKED missing reference image: {item['file']}")
        report = item.get("landmark_report")
        if report and not (manifest_path.parent / report).is_file():
            messages.append(f"BLOCKED missing reference landmark report: {report}")

    landmark_contract = manifest.get("proportion_landmark_contract")
    if landmark_contract and not (
        manifest_path.parent / landmark_contract["canonical_report"]
    ).is_file():
        messages.append("BLOCKED canonical landmark report is missing")

    train_ids = {item["source_id"] for item in dataset["train_items"]}
    heldout_ids = {item["source_id"] for item in dataset["heldout_items"]}
    overlap = sorted(train_ids & heldout_ids)
    if overlap:
        messages.append(f"ERROR overlapping source_id: {', '.join(overlap)}")

    scene_plan = manifest.get("single_character_scene_adapter_plan")
    if scene_plan and scene_plan["status"] != "ready_for_joint_training":
        messages.append(
            "BLOCKED joint adapter scene pack has not passed per-panel identity review"
        )

    print(f"experiment: {manifest['experiment_id']}")
    print(f"phase: {manifest['phase']}")
    print(f"evaluation panels: {len(manifest['evaluation_panels'])}")
    print("\n".join(messages) if messages else "PASS ready for training")
    return 1 if any(message.startswith(("BLOCKED", "ERROR")) for message in messages) else 0


if __name__ == "__main__":
    raise SystemExit(main())

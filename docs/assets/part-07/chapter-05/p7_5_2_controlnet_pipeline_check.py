#!/usr/bin/env python3
"""Validate the asset and panel contract for the P7 ControlNet pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VALID_PHASES = {"asset_approval", "baseline", "identity_anchor", "repair", "continuity_review"}
VALID_STRATEGIES = {
    "pose-first": {"openpose"},
    "camera-background-first": {"depth", "lineart"},
    "object-first": {"lineart", "segmentation"},
    "face-first": {"lineart", "segmentation", "none"},
}
QUALITY_KEYS = {"identity", "structure", "style", "local_detail"}
QUALITY_RESULTS = {"pass", "fail", "pending"}


def missing(required: list[str], approved: list[str]) -> list[str]:
    return sorted(set(required) - set(approved))


def validate_assets(manifest: dict[str, Any]) -> list[str]:
    messages: list[str] = []
    for asset_name, asset in manifest["assets"].items():
        absent = missing(asset["required_views"] if asset_name == "character_sheet" else asset["required_items"],
                         asset["approved_views"] if asset_name == "character_sheet" else asset["approved_items"])
        if asset["status"] == "approved" and absent:
            messages.append(f"ERROR asset {asset_name}: approved but missing {', '.join(absent)}")
        elif absent:
            messages.append(f"BLOCKED asset {asset_name}: needs {', '.join(absent)}")
    return messages


def validate_reference_pack(manifest: dict[str, Any], phase: str) -> list[str]:
    pack = manifest.get("character_reference_pack")
    if not isinstance(pack, dict):
        return ["ERROR character_reference_pack is required"]
    messages: list[str] = []
    if not pack.get("revision"):
        messages.append("ERROR character_reference_pack: revision is required")
    if phase != "asset_approval":
        if pack.get("approval_status") != "approved":
            messages.append("ERROR character_reference_pack: must be approved before generation")
        if pack.get("rights_confirmation") in {None, "", "pending"}:
            messages.append("ERROR character_reference_pack: rights_confirmation is required before generation")
    return messages


def validate_panel(panel: dict[str, Any], phase: str) -> list[str]:
    messages: list[str] = []
    panel_id = panel.get("panel_id", "<missing>")
    strategy = panel.get("entry_strategy")
    control = panel.get("primary_control")
    if strategy not in VALID_STRATEGIES:
        messages.append(f"ERROR {panel_id}: unknown entry_strategy {strategy!r}")
    elif control not in VALID_STRATEGIES[strategy]:
        allowed = ", ".join(sorted(VALID_STRATEGIES[strategy]))
        messages.append(f"ERROR {panel_id}: {strategy} requires primary_control in {allowed}")
    if not panel.get("camera_intent"):
        messages.append(f"ERROR {panel_id}: camera_intent is required")
    if not panel.get("identity_anchor"):
        messages.append(f"ERROR {panel_id}: identity_anchor is required")
    if not isinstance(panel.get("repair_targets"), list) or not panel["repair_targets"]:
        messages.append(f"ERROR {panel_id}: at least one repair_targets item is required")

    quality = panel.get("quality", {})
    if phase in {"repair", "continuity_review"}:
        absent = QUALITY_KEYS - set(quality)
        if absent:
            messages.append(f"ERROR {panel_id}: missing quality results for {', '.join(sorted(absent))}")
        for key, result in quality.items():
            if key not in QUALITY_KEYS or result not in QUALITY_RESULTS:
                messages.append(f"ERROR {panel_id}: invalid quality result {key}={result!r}")
    return messages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    messages: list[str] = []
    if manifest.get("schema_version") != "p7-controlnet-webtoon/v1":
        messages.append("ERROR schema_version must be p7-controlnet-webtoon/v1")
    phase = manifest.get("phase")
    if phase not in VALID_PHASES:
        messages.append(f"ERROR unknown phase {phase!r}")
    else:
        messages.extend(validate_reference_pack(manifest, phase))
        messages.extend(validate_assets(manifest))
        for panel in manifest.get("panels", []):
            messages.extend(validate_panel(panel, phase))
        if phase != "asset_approval" and any(message.startswith("BLOCKED asset") for message in messages):
            messages.append("ERROR generation phases require approved character, style, and location sheets")

    reference_pack = manifest.get("character_reference_pack", {})
    report = [
        "P7 ControlNet webtoon pipeline check",
        f"project: {manifest.get('project_id', '<missing>')}",
        f"phase: {phase}",
        f"character_reference_pack: {reference_pack.get('revision', '<missing>')} ({reference_pack.get('approval_status', '<missing>')})",
        f"panels: {len(manifest.get('panels', []))}",
        *messages,
    ]
    if not messages:
        report.append("PASS configuration is ready for the declared phase")
    text = "\n".join(report) + "\n"
    print(text, end="")
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    return 1 if any(message.startswith("ERROR") for message in messages) else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Compose, but do not execute, the review-gated directional full-body workflow."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from p7_5_2_generate_fullbody_direction_references import VIEW_SPECS, stage_output


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
OUTPUT = ROOT / "p7-5-2-fullbody-direction-workflow.json"
def command(views: list[str]) -> list[str]:
    return [
        ".venv/bin/python",
        "docs/assets/part-07/chapter-05/p7_5_2_generate_fullbody_direction_references.py",
        "--views",
        *views,
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--views", nargs="+", choices=VIEW_SPECS, required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    face_inputs = {view: VIEW_SPECS[view][0].name for view in args.views}
    torso_outputs = {view: stage_output("torso", view).name for view in args.views}
    fullbody_outputs = {view: stage_output("fullbody", view).name for view in args.views}
    proportion_outputs = {view: stage_output("proportion", view).name for view in args.views}
    outfit_outputs = {view: stage_output("outfit", view).name for view in args.views}
    workflow = {
        "status": "plan_only",
        "requested_views": args.views,
        "stages": [
            {
                "id": "face_to_torso_to_fullbody_to_proportion_to_outfit_unified",
                "inputs": face_inputs,
                "intermediates": {
                    "torso": torso_outputs,
                    "fullbody": fullbody_outputs,
                    "proportion": proportion_outputs,
                },
                "outputs": outfit_outputs,
                "environment": {"PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"},
                "command": command(args.views),
                "gate": "Human review is required before any outfit-unified full-body output becomes a reference asset.",
            },
        ],
    }
    args.output.write_text(json.dumps(workflow, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Prepare a controlled CatVTON guidance A/B experiment without generating images.

The garment, source, mask, size, seed, and inference steps are fixed.  Only
guidance changes, so human review can attribute a difference in collar,
open-front layering, or symmetry to that one setting.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


CONDITIONS = (
    {"id": "guidance-2_5", "guidance": 2.5},
    {"id": "guidance-3_5", "guidance": 3.5},
)
GATES = {
    "preserve_outside_mask": "face, charcoal crop top, trousers, shoes, and background remain unchanged",
    "jacket_shape": "white cropped jacket has two long sleeves and an open front",
    "layering": "crop top stays visible through the open front; collar does not remain black or charcoal",
    "geometry": "left and right lapels, pockets, and cuffs are plausible and symmetric",
    "texture": "white fabric is coherent without a pasted boundary or repeated artifacts",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("mask", type=Path)
    parser.add_argument("garment", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--catvton-repo",
        type=Path,
        help="official CatVTON checkout; required only with --run",
    )
    parser.add_argument("--steps", type=int, default=50)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--run", action="store_true", help="execute the two prepared conditions")
    return parser.parse_args()


def build_command(args: argparse.Namespace, condition: dict[str, object]) -> list[str]:
    if args.catvton_repo is None:
        raise ValueError("--catvton-repo is required with --run")
    runner = Path(__file__).with_name("p7_5_4_catvton_manual_mask_probe.py")
    output = args.output / str(condition["id"])
    return [
        sys.executable,
        str(runner),
        str(args.source.resolve()),
        str(args.mask.resolve()),
        str(args.garment.resolve()),
        str(output.resolve()),
        "--steps",
        str(args.steps),
        "--guidance",
        str(condition["guidance"]),
        "--seed",
        str(args.seed),
    ]


def main() -> int:
    args = parse_args()
    missing = [str(path) for path in (args.source, args.mask, args.garment) if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing fixed input(s): " + ", ".join(missing))
    if args.steps <= 0:
        raise ValueError("--steps must be positive")
    if args.run and (args.catvton_repo is None or not args.catvton_repo.is_dir()):
        raise ValueError("--run requires an existing --catvton-repo checkout")

    args.output.mkdir(parents=True, exist_ok=True)
    plan = {
        "status": "prepared" if not args.run else "running",
        "experiment": "P7-5.4 CatVTON guidance A/B",
        "question": "Does guidance alone improve collar layering and jacket symmetry?",
        "fixed_inputs": {
            "source": str(args.source.resolve()),
            "operator_mask": str(args.mask.resolve()),
            "garment": str(args.garment.resolve()),
            "resolution": [768, 1024],
            "steps": args.steps,
            "seed": args.seed,
        },
        "variable": "guidance",
        "conditions": CONDITIONS,
        "human_review_gates": GATES,
        "decision_rule": "Choose neither if either candidate changes protected regions or fails a jacket gate; this does not approve a production asset.",
    }
    plan_path = args.output / "plan.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not args.run:
        print(f"Prepared {len(CONDITIONS)} conditions: {plan_path}")
        return 0

    for condition in CONDITIONS:
        command = build_command(args, condition)
        print("Running:", " ".join(command))
        subprocess.run(
            command,
            check=True,
            cwd=args.catvton_repo,
            env={**os.environ, "CATVTON_REPO": str(args.catvton_repo.resolve())},
        )
    plan["status"] = "generated_for_human_review"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

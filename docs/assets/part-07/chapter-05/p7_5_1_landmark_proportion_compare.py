#!/usr/bin/env python3
"""Compare landmark reports without rendering a pose skeleton."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


METRICS = ("silhouette_to_shoulder_2d", "torso_to_leg_2d")


def relative_difference(canonical: float, candidate: float) -> float:
    return abs(candidate - canonical) / canonical


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--maximum-relative-drift", type=float, default=0.04)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    canonical = json.loads(args.canonical.read_text(encoding="utf-8"))["metrics"]
    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))["metrics"]
    comparison = {
        metric: {
            "canonical": canonical[metric],
            "candidate": candidate[metric],
            "relative_drift": relative_difference(canonical[metric], candidate[metric]),
        }
        for metric in METRICS
    }
    failed = [
        metric
        for metric, values in comparison.items()
        if values["relative_drift"] > args.maximum_relative_drift
    ]
    report = {
        "method": "2D silhouette and pose-landmark proportion comparison; 3D values are intentionally excluded from the pass rule",
        "maximum_relative_drift": args.maximum_relative_drift,
        "metrics": comparison,
        "status": "rejected" if failed else "proportion_match",
        "failed_metrics": failed,
    }
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"output: {args.output}")
    print(f"status: {report['status']}")
    for metric, values in comparison.items():
        print(f"{metric}_drift: {values['relative_drift']:.3%}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

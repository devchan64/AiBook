#!/usr/bin/env python3
"""Prepare and inspect a local Kimodo text-to-keyframe right-walk probe.

This is a preflight for P7-5.6, not an approved animation pipeline.  Kimodo
creates a 3D SOMA joint sequence; this script records a small, reviewable set
of frames and their foot-contact labels before any pose-map or character
animation stage is attempted.

Run ``--dry-run`` first.  ``--run`` can download model weights through
Kimodo's own loader, so it is deliberately opt-in.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import numpy as np


ASSET_DIR = Path(__file__).parent
DEFAULT_OUTPUT_DIR = ASSET_DIR / "p7-5-6-kimodo-right-walk-output"
PROMPT = (
    "A person walks naturally to the right at a normal pace. "
    "They start by stepping forward with the left foot, keep the torso upright, "
    "swing each arm opposite to its leg, and complete one full walk cycle."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Run Kimodo generation after preflight.")
    parser.add_argument("--inspect", type=Path, help="Inspect an existing Kimodo NPZ instead of generating.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--model", default="Kimodo-SOMA-RP-v1.1")
    parser.add_argument("--duration", type=float, default=2.0, help="Seconds; keep the first probe short.")
    parser.add_argument("--samples", type=int, default=2, help="Compare two motion candidates, not one lucky sample.")
    parser.add_argument("--steps", type=int, default=50, help="Kimodo denoising steps.")
    parser.add_argument("--seed", type=int, default=20260808)
    parser.add_argument(
        "--review-frames",
        type=int,
        default=16,
        help="Evenly spaced frames recorded for gait review; the full motion remains in the NPZ.",
    )
    return parser.parse_args()


def kimodo_available() -> bool:
    return importlib.util.find_spec("kimodo") is not None


def build_command(args: argparse.Namespace, output_stem: Path) -> list[str]:
    return [
        sys.executable,
        "-m",
        "kimodo.scripts.generate",
        PROMPT,
        "--model",
        args.model,
        "--duration",
        str(args.duration),
        "--num_samples",
        str(args.samples),
        "--diffusion_steps",
        str(args.steps),
        "--seed",
        str(args.seed),
        "--output",
        str(output_stem),
    ]


def write_plan(args: argparse.Namespace, output_stem: Path) -> Path:
    args.output_dir.mkdir(parents=True, exist_ok=True)
    plan = {
        "section_id": "P7-5.6",
        "purpose": "text-to-keyframe right-walk preflight before DWPose conversion",
        "prompt": PROMPT,
        "model": args.model,
        "duration_seconds": args.duration,
        "num_samples": args.samples,
        "diffusion_steps": args.steps,
        "seed": args.seed,
        "review_frames": args.review_frames,
        "text_encoder_device": "cpu",
        "expected_output": f"{output_stem}.npz (or numbered NPZ files when samples > 1)",
        "review_gate": [
            "left/right foot-contact labels alternate plausibly",
            "root translation is consistently toward the right after camera projection",
            "no knee, ankle, or foot crosses impossibly before DWPose conversion",
            "only a human-approved candidate can become a P7-5.6 structure-map input",
        ],
    }
    plan_path = args.output_dir / "kimodo-run-plan.json"
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    return plan_path


def inspect_motion(npz_path: Path, output_dir: Path, review_frames: int) -> Path:
    with np.load(npz_path) as motion:
        required = {"posed_joints", "foot_contacts", "root_positions"}
        missing = sorted(required.difference(motion.files))
        if missing:
            raise ValueError(f"{npz_path} is missing Kimodo fields: {', '.join(missing)}")
        joints = motion["posed_joints"]
        contacts = motion["foot_contacts"]
        root = motion["root_positions"]

    if joints.ndim != 3 or joints.shape[2] != 3:
        raise ValueError(f"expected posed_joints [frames, joints, 3], got {joints.shape}")
    if contacts.shape != (joints.shape[0], 4):
        raise ValueError(f"expected foot_contacts [{joints.shape[0]}, 4], got {contacts.shape}")
    if root.shape != (joints.shape[0], 3):
        raise ValueError(f"expected root_positions [{joints.shape[0]}, 3], got {root.shape}")

    if review_frames < 2:
        raise ValueError("review_frames must be at least 2")
    frame_ids = np.unique(np.linspace(0, joints.shape[0] - 1, review_frames, dtype=int))
    report = {
        "source_npz": str(npz_path),
        "frames": int(joints.shape[0]),
        "joints_per_frame": int(joints.shape[1]),
        "keyframe_indices": frame_ids.tolist(),
        "keyframe_foot_contacts": contacts[frame_ids].astype(int).tolist(),
        "root_displacement": (root[-1] - root[0]).round(5).tolist(),
        "warning": (
            "Kimodo coordinate axes must be projected and visually checked before interpreting "
            "a displacement component as screen-right motion."
        ),
    }
    report_path = output_dir / f"{npz_path.stem}-inspection.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote inspection report: {report_path}")
    print(f"Review keyframes: {report['keyframe_indices']}")
    print(f"Foot contacts [left heel, left toe, right heel, right toe]: {report['keyframe_foot_contacts']}")
    return report_path


def main() -> int:
    args = parse_args()
    if args.duration <= 0 or args.samples < 1 or args.steps < 1 or args.review_frames < 2:
        raise ValueError("duration, samples, steps, and review_frames must be positive; review_frames needs at least 2")

    if args.inspect:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        inspect_motion(args.inspect, args.output_dir, args.review_frames)
        return 0

    output_stem = args.output_dir / "right-walk"
    plan_path = write_plan(args, output_stem)
    command = build_command(args, output_stem)
    print(f"Wrote Kimodo probe plan: {plan_path}")
    print("Text encoder is deliberately pinned to CPU for the 8 GB preflight.")
    print("Command:")
    print(" ".join(command))

    if not args.run:
        print("Dry run only. Re-run with --run after Kimodo and its model weights are approved and installed.")
        return 0
    if not kimodo_available():
        raise RuntimeError("Kimodo is not installed in this Python environment. Run without --run to inspect the plan.")
    if shutil.which("nvidia-smi") is None:
        raise RuntimeError("No NVIDIA GPU command was found; do not start this GPU preflight.")

    environment = {**os.environ, "TEXT_ENCODER_DEVICE": "cpu"}
    subprocess.run(command, check=True, env=environment)
    generated = sorted(args.output_dir.rglob("right-walk*.npz"))
    if not generated:
        raise FileNotFoundError("Kimodo completed without an NPZ in the expected output directory")
    for npz_path in generated:
        inspect_motion(npz_path, args.output_dir, args.review_frames)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Prepare a fixed-length MoMask walking-motion experiment without loading a model.

The generated files live in ``.tmp/`` by default: this preparation step records
the text-to-motion input and the 48-to-12 keyframe sampling rule, but it does
not download weights or claim that an 8 GB GPU has passed inference.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUTPUT_DIR = ROOT / ".tmp" / "p7-5-8-momask-walk-keyframes"


def evenly_spaced_indices(source_frames: int, keyframes: int) -> list[int]:
    if source_frames % keyframes:
        raise ValueError("--source-frames must be divisible by --keyframes")
    step = source_frames // keyframes
    return list(range(0, source_frames, step))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", default="A person walks forward")
    parser.add_argument("--source-frames", type=int, default=48)
    parser.add_argument("--keyframes", type=int, default=12)
    parser.add_argument("--fps", type=int, default=20)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    if args.source_frames < 4 or args.source_frames % 4:
        raise ValueError("MoMask source motion must contain a positive multiple of four poses")
    if args.keyframes < 2 or args.keyframes > args.source_frames:
        raise ValueError("--keyframes must be between 2 and --source-frames")
    if args.fps < 1:
        raise ValueError("--fps must be positive")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    momask_line = f"{args.prompt.strip().rstrip('#')}#{args.source_frames}"
    indices = evenly_spaced_indices(args.source_frames, args.keyframes)
    plan = {
        "status": "prepared_not_run",
        "section_id": "P7-5.8",
        "model_candidate": "centersymmetry/momask",
        "task": "text_to_3d_human_motion_then_openpose_keyframes",
        "momask_input": {"line": momask_line, "source_frames": args.source_frames, "fps": args.fps},
        "expected_motion_shape": [args.source_frames, 22, 3],
        "keyframe_sampling": {
            "keyframes": args.keyframes,
            "source_indices": indices,
            "method": "every_nth_frame",
        },
        "next_steps": [
            "run MoMask with batch size 1 on the local 8 GB GPU",
            "verify the generated joint array shape before projection",
            "map the 22-joint sequence to the repository's OpenPose body-only schema",
            "render and review the 12 2D keyframe guides before image generation",
        ],
        "hardware_claim": "No minimum VRAM claim; preparation only.",
    }
    (output_dir / "momask-input.txt").write_text(momask_line + "\n", encoding="utf-8")
    (output_dir / "experiment-plan.json").write_text(
        json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output_dir": str(output_dir), "source_indices": indices}, ensure_ascii=False))


if __name__ == "__main__":
    main()

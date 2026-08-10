#!/usr/bin/env python3
"""Run a fixed ten-condition jacket-inpaint search and make one review sheet.

Only the local edit contract changes: crop padding, edit-mask border, adapter
weight, denoise strength, or CFG.  The source, fitted-shell mask, isolated
jacket reference, resolution, prompt, negative prompt, and seed stay fixed.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROMPT = (
    "open white cropped utility jacket with long white cuffed sleeves, worn "
    "unfastened over the preserved charcoal-gray micro-crop top; preserve the "
    "teal bob, face, teal wide-leg trousers, white sneakers, pose, and studio"
)
NEGATIVE_PROMPT = (
    "closed jacket, buttoned jacket, gray jacket, short sleeves, changed face, "
    "changed hair, changed trousers, changed shoes, changed pose, cropped "
    "person, extra limbs, text, watermark"
)
CONDITIONS = (
    ("01-baseline", 0, None, 0.55, 0.75, 12.0),
    ("02-pad-32", 0, 32, 0.55, 0.75, 12.0),
    ("03-pad-96", 0, 96, 0.55, 0.75, 12.0),
    ("04-expand-4", 4, None, 0.55, 0.75, 12.0),
    ("05-expand-8", 8, None, 0.55, 0.75, 12.0),
    ("06-adapter-030", 0, None, 0.30, 0.75, 12.0),
    ("07-adapter-100", 0, None, 1.00, 0.75, 12.0),
    ("08-strength-060", 0, None, 0.55, 0.60, 12.0),
    ("09-strength-085", 0, None, 0.55, 0.85, 12.0),
    ("10-cfg-7", 0, None, 0.55, 0.75, 7.0),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("mask", type=Path)
    parser.add_argument("outfit_reference", type=Path)
    parser.add_argument("output_root", type=Path)
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    probe = script_dir / "p7_5_4_manual_mask_ipadapter_inpaint_probe.py"
    sheet = script_dir / "p7_5_4_make_inpaint_ablation_sheet.py"
    args.output_root.mkdir(parents=True, exist_ok=True)
    for name, expand, padding, adapter, strength, cfg in CONDITIONS:
        command = [
            sys.executable,
            str(probe),
            str(args.source),
            str(args.mask),
            str(args.outfit_reference),
            str(args.output_root / name),
            "--prompt",
            PROMPT,
            "--negative-prompt",
            NEGATIVE_PROMPT,
            "--steps",
            "30",
            "--strength",
            str(strength),
            "--guidance-scale",
            str(cfg),
            "--adapter-scale",
            str(adapter),
            "--seed",
            "62294",
            "--width",
            "512",
            "--height",
            "768",
            "--mask-expand-px",
            str(expand),
        ]
        if padding is not None:
            command.extend(("--padding-mask-crop", str(padding)))
        subprocess.run(command, check=True)
    subprocess.run(
        [sys.executable, str(sheet), str(args.output_root), str(args.output_root / "contact-sheet.png")],
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

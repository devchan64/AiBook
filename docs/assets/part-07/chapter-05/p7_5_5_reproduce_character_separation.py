#!/usr/bin/env python3
"""Reproduce four reviewed Grounding DINO/SAM2 character separations.

The recipe fixes source hashes, pixel-coordinate prompts and baseline images.
Segmentation runs on the local CUDA GPU; the cutout helper copies source pixels.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parents[3]
RECIPE = ASSETS / 'p7-5-5-character-separation-recipe-v1.json'
MASK_SCRIPT = ASSETS / 'p7_5_5_generate_person_mask.py'
CUTOUT_SCRIPT = ASSETS / 'p7_5_5_extract_pose_cutout.py'


def digest(path: Path) -> str:
    """Identify the exact input or source file used by a run."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pixels(path: Path, mode: str) -> np.ndarray:
    """Read pixels without depending on PNG compression or metadata."""
    with Image.open(path) as image:
        return np.array(image.convert(mode))


def main() -> None:
    """Plan, execute and verify the selected independent characters."""
    recipe = json.loads(RECIPE.read_text(encoding='utf-8'))
    targets = {row['target']: row for row in recipe['targets']}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--targets', nargs='+', choices=tuple(targets), default=list(targets))
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--run-label', default='reproduce-v1')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('--run-label must contain only letters, digits, underscores or hyphens')
    output_dir = args.output_dir.resolve()
    manifest = output_dir / f'p7-5-5-character-separation-{args.run_label}-result.json'
    plans = []
    all_outputs = [manifest]
    for key in dict.fromkeys(args.targets):
        row = targets[key]
        reference = ASSETS / row['reference']
        if digest(reference) != row['reference_sha256']:
            raise ValueError(f'Input differs from the reviewed recipe: {reference}')
        for filename in row['baseline'].values():
            if not (ASSETS / filename).is_file():
                raise FileNotFoundError(ASSETS / filename)
        mask_label = f"scene-{key}-{args.run_label}"
        mask_stem = f'p7-5-5-sam2-person-mask-{mask_label}'
        cut_stem = f'p7-5-5-character-cutout-scene-{key}-{args.run_label}'
        mask = output_dir / f'{mask_stem}.png'
        white = output_dir / f'{cut_stem}.png'
        rgba = output_dir / f'{cut_stem}-rgba.png'
        mask_command = [sys.executable, str(MASK_SCRIPT), '--reference', str(reference),
                        '--run-label', mask_label, '--output-dir', str(output_dir), *row['mask_args']]
        cutout_command = [sys.executable, str(CUTOUT_SCRIPT), '--reference', str(reference),
                          '--mask', str(mask), '--scene', row['scene'], '--character', row['character'],
                          '--run-label', args.run_label, '--output-dir', str(output_dir), '--transparent']
        paths = [mask, output_dir / f'{mask_stem}-overlay.png', output_dir / f'{mask_stem}-result.json',
                 white, rgba, output_dir / f'{cut_stem}-result.json']
        all_outputs.extend(paths)
        plans.append({'target': key, 'reference': str(reference), 'mask_command': mask_command,
                      'cutout_command': cutout_command, 'outputs': [str(path) for path in paths]})
    for path in all_outputs:
        if path.exists():
            raise FileExistsError(f'Refusing to overwrite: {path}')
    if args.dry_run:
        print(json.dumps({'status': 'planned', 'plans': plans}, ensure_ascii=False, indent=2))
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {'status': 'verified', 'recipe_sha256': digest(RECIPE),
              'source_sha256': {p.name: digest(p) for p in (Path(__file__), MASK_SCRIPT, CUTOUT_SCRIPT)},
              'characters': []}
    masks = {}
    for plan in plans:
        print(f"Starting {plan['target']}", flush=True)
        subprocess.run(plan['mask_command'], cwd=ROOT, check=True)
        subprocess.run(plan['cutout_command'], cwd=ROOT, check=True)
        paths = [Path(p) for p in plan['outputs']]
        source = pixels(Path(plan['reference']), 'RGB')
        mask = pixels(paths[0], 'L')
        white = pixels(paths[3], 'RGB')
        rgba = pixels(paths[4], 'RGBA')
        baseline = targets[plan['target']]['baseline']
        checks = {
            'size_1280': source.shape == (1280, 1280, 3) and mask.shape == (1280, 1280),
            'binary_mask': bool(np.isin(mask, [0, 255]).all()),
            'alpha_equals_mask': bool(np.array_equal(rgba[:, :, 3], mask)),
            'source_pixels_preserved': bool(np.array_equal(rgba[:, :, :3][mask > 0], source[mask > 0])
                                           and np.array_equal(white[mask > 0], source[mask > 0])),
            'background_white': bool((white[mask == 0] == 255).all()),
            'baseline_mask_equal': bool(np.array_equal(mask, pixels(ASSETS / baseline['mask'], 'L'))),
            'baseline_white_equal': bool(np.array_equal(white, pixels(ASSETS / baseline['white'], 'RGB'))),
            'baseline_rgba_equal': bool(np.array_equal(rgba, pixels(ASSETS / baseline['rgba'], 'RGBA'))),
        }
        masks[plan['target']] = mask > 0
        report['characters'].append({**plan, 'checks': checks,
                                     'output_sha256': {p.name: digest(p) for p in paths}})
        if not all(checks.values()):
            report['status'] = 'verification_failed'
    if 'c-mira' in masks and 'c-supporting' in masks:
        report['c_mask_overlap_pixels'] = int((masks['c-mira'] & masks['c-supporting']).sum())
    manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Result: {manifest}', flush=True)
    if report['status'] != 'verified':
        raise RuntimeError('Outputs differ from the baseline or violate pixel checks; inspect the result JSON.')


if __name__ == '__main__':
    main()

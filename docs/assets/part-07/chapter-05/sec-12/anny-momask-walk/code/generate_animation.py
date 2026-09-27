"""Saved HumanML22 joints -> the registered P7-5.11 ANNY rig.

Run with Python + numpy + PyYAML. Workers require Python with bpy 4.5.3,
numpy and PyYAML. This entry point does not run MoMask inference.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess

import numpy as np
import yaml


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--motion', type=Path, required=True)
    parser.add_argument('--rig', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--blender-python', type=Path, required=True)
    parser.add_argument('--fps', type=int, default=20)
    parser.add_argument('--render', action='store_true', help='Render four views using CUDA/Cycles')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.fps <= 0:
        parser.error('--fps must be positive')
    for path in (args.motion, args.rig, args.blender_python):
        if not path.is_file():
            parser.error(f'File not found: {path}')
    out = args.output_dir.resolve()
    if out.exists():
        parser.error('Output directory already exists; choose a new directory')
    code = Path(__file__).resolve().parent
    profile = yaml.safe_load((code / 'retarget-profile.yaml').read_text())
    with np.load(args.motion, allow_pickle=False) as bundle:
        joints = bundle['joints'].copy()
    if joints.ndim != 3 or joints.shape[1:] != (22, 3) or len(joints) < 2 or not np.isfinite(joints).all():
        parser.error('Expected finite joints with shape (T, 22, 3), T >= 2')
    record = dict(status='validated', frames=len(joints), source_fps=20,
                  playback_fps=args.fps, motion_sha256=sha(args.motion),
                  rig_sha256=sha(args.rig), contacts='zero placeholders, not inferred',
                  rig_objects=['AnnyAttributesRig', 'AnnyAttributesBody'], render=args.render)
    if args.dry_run:
        print(json.dumps(record, indent=2))
        return
    out.mkdir(parents=True)
    (out / 'inputs').mkdir()
    names = ['position_retarget.py', 'retarget_audit.py', 'retarget_loop.py',
             'run_stage.py', 'retarget-profile.yaml', 'MOMASK-TEMPLATE-LICENSE.txt']
    for name in names:
        shutil.copy2(code / name, out / name)
    motion = out / 'inputs/mannequin-motion.npz'
    np.savez_compressed(motion, joints=joints,
                        rest=np.asarray(profile['source_reference']['joint_positions']),
                        contacts=np.zeros((len(joints), 4), dtype=np.float32),
                        sample_indices=np.arange(len(joints)))
    (out / 'inputs/artifact.json').write_text(json.dumps({
        'files': {'mannequin-motion.npz': sha(motion)}, 'fps': args.fps,
        'source_motion': str(args.motion.resolve())}, indent=2))
    shutil.copy2(args.rig, out / 'inputs/anny-reference-fit-rig.blend')
    stages = ['retarget_loop.py']
    if args.render:
        source = (code / 'render_asset.py').read_text()
        source, count = re.subn(r'^OUTPUT_SAMPLE_FRAMES=.*$',
                               f'OUTPUT_SAMPLE_FRAMES={list(range(1, len(joints) + 1))}',
                               source, flags=re.MULTILINE)
        if count != 1:
            raise ValueError('Renderer frame configuration marker changed')
        (out / 'render_asset.py').write_text(source)
        stages.append('render_asset.py')
    record['code_sha256'] = {p.name: sha(p) for p in out.glob('*.py')}
    record['profile_sha256'] = sha(out / 'retarget-profile.yaml')
    record['entrypoint_sha256'] = sha(Path(__file__))
    record['status'] = 'running'
    try:
        for stage in stages:
            with (out / (stage + '.log')).open('w') as log:
                subprocess.run([str(args.blender_python.absolute()), str(out / 'run_stage.py'),
                                str(out / stage)], stdout=log, stderr=subprocess.STDOUT, check=True)
        record['status'] = 'generated_review_required'
        record['outputs'] = {name: sha(out / name) for name in
                             ('mannequin.blend', 'mannequin.glb', 'review-metrics.json')}
    except Exception:
        record['status'] = 'failed'
        raise
    finally:
        (out / 'generation-record.json').write_text(json.dumps(record, indent=2))
    print(json.dumps(record, indent=2))


if __name__ == '__main__':
    main()

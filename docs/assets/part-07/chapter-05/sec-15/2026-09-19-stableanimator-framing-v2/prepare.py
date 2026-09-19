"""Prepare a two-step framing comparison. Does not run image inference."""
from pathlib import Path
import hashlib
import importlib.util
import json
import numpy as np
from PIL import Image, ImageDraw

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[5]
PREVIOUS = BASE.parent / '2026-09-19-momask-stableanimator-v1'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    if (BASE / 'plan.json').exists():
        raise SystemExit('Prepared plan already exists; use a new experiment folder.')
    motion = PREVIOUS / 'momask-v2/run-10109.npz'
    reference = PREVIOUS / 'stableanimator-run-v1/reference-512.png'
    prior_plan = PREVIOUS / 'stableanimator-run-v1/plan.json'
    baseline = json.loads(prior_plan.read_text())
    j = np.load(motion)['joints'][36:68]
    indices = baseline['pose_mapping']
    scale = float(min(390 / np.ptp(j[:, :, 1]), 440 / np.ptp(j[:, :, 2])))
    floor = float(np.percentile(j[:, [7, 10, 8, 11], 1], 1))
    renderer = ROOT / '.tmp/download/sources/p7-5-15/StableAnimator/DWPose/dwpose_utils/util.py'
    spec = importlib.util.spec_from_file_location('poseutil', renderer)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    conditions = []
    for name, factor in [('centered-small', 1.0), ('centered-large', 2.0)]:
        folder = BASE / name / 'poses'
        folder.mkdir(parents=True, exist_ok=True)
        all_xy, hashes = [], {}
        for frame in range(32):
            xy = np.zeros((18, 2))
            subset = np.full((1, 18), -1.)
            for k, idx in enumerate(indices):
                if idx is not None:
                    # Track only horizontal root position; preserve vertical root motion.
                    xy[k] = [(256 + (j[frame, idx, 2] - j[frame, 0, 2]) * scale * factor) / 512,
                             (455 - (j[frame, idx, 1] - floor) * scale * factor) / 512]
                    subset[0, k] = k
            valid = xy[np.array(indices, dtype=object) != None]  # noqa: E711
            assert np.all(valid > 0) and np.all(valid < 1), 'Pose outside canvas'
            im = module.draw_bodypose(np.zeros((512, 512, 3), np.uint8), xy, subset)
            path = folder / f'frame_{frame}.png'
            Image.fromarray(im).save(path)
            hashes[path.name] = sha(path)
            all_xy.append(xy.tolist())
        conditions.append({'id': name, 'scale_factor': factor, 'pixels_per_meter': scale * factor,
                           'pose_normalized_xy': all_xy, 'pose_sha256': hashes})
    plan = {'experiment_id': 'P7-5.15-framing-v2', 'status': 'prepared_not_run', 'motion_review':'motion-review.json', 'execution_readiness':'Inputs verified; user did not observe the suspected foot alternation issue in continuous video. Ready for framing comparison; no image inference executed.',
            'source_motion': str(motion.relative_to(ROOT)), 'source_motion_sha256': sha(motion),
            'source_frames': list(range(36, 68)), 'reference': str(reference.relative_to(ROOT)),
            'reference_sha256': sha(reference), 'baseline_plan': str(prior_plan.relative_to(ROOT)),
            'baseline_result': str((PREVIOUS / 'stableanimator-run-v1/result.json').relative_to(ROOT)),
            'baseline_plan_sha256': sha(prior_plan), 'pose_renderer_sha256': sha(renderer),
            'pose_mapping': indices, 'floor_estimate_m': floor, 'floor_pixel_y': 455,
            'baseline_height_range_px': float(np.ptp(j[:, :, 1]) * scale),
            'comparisons': ['previous run vs centered-small: horizontal root tracking only',
                            'centered-small vs centered-large: scale only, 1x vs 2x'],
            'fixed': {'width':512, 'height':512, 'frames':32, 'steps':25, 'guidance':3,
                      'seed':23123134, 'tile_size':16, 'overlap':4, 'decode_chunk_size':1,
                      'noise_aug_strength':0.02, 'model_fps':7, 'cpu_threads':4,
                      'reference':'reuse previous preprocessed reference', 'face_hands':'omitted'},
            'primary_question': 'Does framing affect failure to preserve the reference character?',
            'review': {'primary_endpoint':'Reference character preservation across all 32 frames, before motion quality',
                       'identity_checks':['hair color and silhouette','visible facial features; mark unjudgeable where too small','clothing color, construction and silhouette','body proportions and full-body integrity','first deviation frame'],
                       'acceptance_rule':'Body loss, major clothing drift, or extra/fused limbs fails character preservation even if motion transfers.',
                       'all_output_frames':True, 'flight_candidate_output_frames':[8,16,22,23,29,30],
                       'criteria':['body and clothing preservation', 'leg overlap and separation',
                                   'pose following at the six candidate frames'],
                       'limits':['No observable ground plane in generated background.',
                                 'No new seed or character; exploratory, no general performance claim.',
                                 'Center tracking changes camera motion; no claim of stationary world camera.']},
            'conditions': conditions}
    (BASE / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    sheet = Image.new('RGB', (6 * 256, 3 * 280), 'white')
    draw = ImageDraw.Draw(sheet)
    for row, folder in enumerate([PREVIOUS / 'stableanimator-run-v1/poses',
                                 BASE / 'centered-small/poses', BASE / 'centered-large/poses']):
        for col, frame in enumerate([8,16,22,23,29,30]):
            x, y = col * 256, row * 280
            draw.text((x + 4, y + 4), f'{["baseline", "center 1x", "center 2x"][row]} / {frame}', fill='black')
            sheet.paste(Image.open(folder / f'frame_{frame}.png').resize((256,256)), (x,y+24))
    sheet.save(BASE / 'pose-comparison.jpg', quality=93)
    print('Prepared two conditions / 64 poses. No model inference executed.')

if __name__ == '__main__':
    main()

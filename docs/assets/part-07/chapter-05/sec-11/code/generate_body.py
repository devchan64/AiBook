"""ANNY 0.6.0 속성 JSON → 수치 신체 → Blender 리그. 기존 출력은 덮어쓰지 않는다."""
import argparse
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import traceback


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'중복 필드: {key}')
        result[key] = value
    return result


def read_attributes(path):
    import numpy as np
    data = json.loads(path.read_text(), object_pairs_hook=unique)
    expected = {'phenotype_kwargs', 'local_changes_kwargs', 'facial_actions',
                'pose_parameterization', 'pose_parameters'}
    if set(data) != expected or data['pose_parameterization'] != 'local-ref':
        raise ValueError('필드 또는 자세 표현 오류: local-ref 필요')
    for group, low, high in [('phenotype_kwargs', 0, 1),
                             ('local_changes_kwargs', -1, 1), ('facial_actions', 0, 1)]:
        if not isinstance(data[group], dict):
            raise ValueError(f'{group}: 사전 필요')
        for key, value in data[group].items():
            limit = 3 if group == 'local_changes_kwargs' and key in {
                'head-scale-horiz-incr', 'head-scale-vert-incr', 'head-scale-depth-incr'} else high
            if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= limit:
                raise ValueError(f'속성 범위 오류: {group}/{key}')
    if not isinstance(data['pose_parameters'], dict) or len(data['pose_parameters']) != 104:
        raise ValueError('anny 리그의 104본 자세 필요')
    for name, values in data['pose_parameters'].items():
        a = np.asarray(values, dtype=float)
        if (a.shape != (4, 4) or not np.isfinite(a).all()
                or not np.allclose(a[3], [0, 0, 0, 1])
                or not np.allclose(a[:3, :3].T @ a[:3, :3], np.eye(3), atol=1e-5)
                or not np.isclose(np.linalg.det(a[:3, :3]), 1, atol=1e-5)):
            raise ValueError(f'강체 변환 오류: {name}')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--attributes', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--cache-dir', type=Path, required=True)
    parser.add_argument('--blender-python', type=Path)
    parser.add_argument('--height', type=float, default=1.6)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    data = read_attributes(args.attributes)
    if not math.isfinite(args.height) or args.height <= 0:
        raise ValueError('높이는 양의 유한값이어야 한다')
    out = args.output_dir.resolve()
    if out.exists():
        raise FileExistsError(out)
    if args.dry_run:
        print('입력 구조·수치 검사 통과. 모델 라벨·CUDA·Blender 검사는 실제 실행 시 수행한다.')
        return
    if args.blender_python is None or not args.blender_python.is_file():
        raise ValueError('bpy 4.5.3을 사용할 Python 경로 필요')
    os.environ['ANNY_CACHE_DIR'] = str(args.cache_dir.resolve())
    import numpy as np
    import torch
    import anny
    if importlib.metadata.version('anny') != '0.6.0':
        raise RuntimeError('이 예제는 anny==0.6.0을 기준으로 한다')
    if not torch.cuda.is_available():
        raise RuntimeError('이 실행 경로는 CUDA가 필요하다')
    out.mkdir(parents=True)
    record = {'status': 'running', 'model': 'anny==0.6.0', 'input_sha256': digest(args.attributes),
              'runner_sha256': digest(__file__), 'height': args.height,
              'torch': torch.__version__, 'gpu': torch.cuda.get_device_name(0)}
    try:
        shutil.copy2(args.attributes, out / 'attributes.json')
        model = anny.Anny(rig='anny', topology='anny', local_changes='default',
                          facial_actions='all', skinning_method='lbs').to(device='cuda', dtype=torch.float32)
        for group, labels in [('phenotype_kwargs', model.phenotype_labels),
                              ('local_changes_kwargs', model.local_change_labels),
                              ('facial_actions', model.facial_action_labels)]:
            if set(data[group]) - set(labels):
                raise ValueError(f'알 수 없는 모델 속성: {group}')
        if set(data['pose_parameters']) != set(model.bone_labels):
            raise ValueError('모델 본 이름 불일치')
        pose = {k: torch.tensor(v, device='cuda', dtype=torch.float32)[None]
                for k, v in data['pose_parameters'].items()}
        with torch.inference_mode():
            result = model(**{**data, 'pose_parameters': pose})
        arrays = dict(vertices=result['vertices'][0].cpu().numpy(), faces=model.faces.cpu().numpy(),
                      bone_matrices=result['bone_poses'][0].cpu().numpy(),
                      bone_parents=np.array(model.bone_parents), bone_names=np.array(model.bone_labels),
                      weights=model.vertex_bone_weights.cpu().numpy(), indices=model.vertex_bone_indices.cpu().numpy())
        if not all(np.isfinite(v).all() for k, v in arrays.items() if k != 'bone_names'):
            raise ValueError('모델 출력에 비유한값 존재')
        np.savez(out / 'anny-rest-rig.npz', **arrays)
        del result, model, pose
        import gc
        gc.collect()
        torch.cuda.empty_cache()
        exporter = Path(__file__).with_name('export_blender.py')
        shutil.copy2(exporter, out / 'export_blender.py')
        with (out / 'blender.log').open('w') as log:
            subprocess.run([str(args.blender_python.resolve()), str(exporter.resolve()),
                            '--bundle', str(out / 'anny-rest-rig.npz'), '--output-dir', str(out),
                            '--height', str(args.height)], check=True, stdout=log, stderr=subprocess.STDOUT)
        record['status'] = 'generated_review_required'
        record['outputs'] = {f.name: digest(f) for f in out.iterdir() if f.is_file()}
    except Exception:
        record['status'] = 'failed'
        record['error'] = traceback.format_exc()
        raise
    finally:
        (out / 'result.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()

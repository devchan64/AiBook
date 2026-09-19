"""Validate prepared inputs; add --execute to run one condition on CUDA."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import time
import traceback

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[5]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('condition', choices=['centered-small', 'centered-large'])
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    plan = json.loads((BASE / 'plan.json').read_text())
    if plan['status'] == 'blocked_source_discarded':
        raise SystemExit('Source experiment discarded; new inputs and plan required.')
    condition = next(c for c in plan['conditions'] if c['id'] == args.condition)
    out = BASE / args.condition
    if (out / 'result.json').exists() or (out / 'output').exists():
        raise SystemExit('Existing output; do not overwrite an experiment.')
    for key in ['source_motion', 'reference', 'baseline_plan']:
        assert sha(ROOT / plan[key]) == plan[key + '_sha256'], key
    for name, digest in condition['pose_sha256'].items():
        assert sha(out / 'poses' / name) == digest, name
    prior = json.loads((ROOT / plan['baseline_result']).read_text())
    source = ROOT / '.tmp/download/sources/p7-5-15/StableAnimator'
    revision = subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
    assert revision == prior['source_revision'], 'Source revision changed'
    assert sha(source / 'DWPose/dwpose_utils/util.py') == plan['pose_renderer_sha256']
    argv = prior['argv'].copy()
    for option, value in {'--output_dir':str(out/'output'),
                          '--validation_control_folder':str(out/'poses'),
                          '--validation_image':str(ROOT/plan['reference'])}.items():
        argv[argv.index(option)+1] = value
    for option in ['--pretrained_model_name_or_path', '--posenet_model_name_or_path',
                   '--face_encoder_model_name_or_path', '--unet_model_name_or_path']:
        assert Path(argv[argv.index(option)+1]).exists(), option
    if not args.execute:
        print(json.dumps({'status':'inputs_validated_not_run','motion_status':plan['status'],'condition':args.condition,'argv':argv},indent=2))
        return
    if plan['status'] != 'prepared_not_run':
        raise SystemExit('Motion review unresolved; revise the experiment plan before image inference.')
    import torch
    assert torch.cuda.is_available(), 'CUDA required'
    torch.set_num_threads(4)
    os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
    sys.path.insert(0,str(source))
    os.chdir(source)
    sys.argv = argv
    torch.cuda.reset_peak_memory_stats()
    start = time.perf_counter()
    record = {'condition':args.condition, 'plan_sha256':sha(BASE/'plan.json'),
              'runner_sha256':sha(Path(__file__)), 'source_revision':revision, 'argv':argv,
              'torch':torch.__version__, 'gpu':torch.cuda.get_device_name(), 'status':'running'}
    try:
        runpy.run_path(str(source/'inference_basic.py'),run_name='__main__')
        record['status'] = 'generated_not_reviewed'
    except Exception:
        record.update(status='failed', traceback=traceback.format_exc())
        raise
    finally:
        record.update(seconds=time.perf_counter()-start,
                      peak_allocated_bytes=torch.cuda.max_memory_allocated(),
                      peak_reserved_bytes=torch.cuda.max_memory_reserved())
        (out/'result.json').write_text(json.dumps(record,indent=2)+'\n')

if __name__ == '__main__':
    main()

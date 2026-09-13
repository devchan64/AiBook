#!/usr/bin/env python3
"""Generate the ordered Mira supplement catalog, one image at a time."""
import argparse
import fcntl
import json
import re
import time
from pathlib import Path
from p7_5_2_qwen_edit_2511_generate_mira_torso import ASSETS, ROOT, CACHE_DIR, MODEL_ID, sha256, runtime_record


def write(path, data):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', type=Path, default=ASSETS / 'p7-5-11/datasets/p7-5-11-mira-supplement-spec.json')
    parser.add_argument('--output-dir', type=Path, default=ROOT / '.tmp/p7-5-11/supplements-v1')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text())
    assert spec['schema_version'] == 1 and spec['model_id'] == MODEL_ID
    cfg = spec['settings']
    assert cfg['extra_lora'] is None and cfg['size'] >= 32 and cfg['size'] % 32 == 0
    assert cfg['steps'] > 0 and cfg['true_cfg_scale'] >= 1
    ids = [x['id'] for x in spec['items']]
    assert len(ids) == len(set(ids)) and all(re.fullmatch(r'[a-z0-9-]+', x) for x in ids)
    assert [x['order'] for x in spec['items']] == list(range(1, len(ids)+1))
    for ref in spec['references'].values():
        assert sha256(ROOT / ref['path']) == ref['sha256'], 'Reference changed'
    for item in spec['items']:
        assert item['reference'] in spec['references'] and item['prompt'].strip()
    if args.dry_run:
        print(json.dumps({'model':MODEL_ID,'count':len(ids),'order':ids,'output_dir':str(args.output_dir)},indent=2))
        return
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    with (out / '.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        run(out, args.spec, spec)


def run(out, spec_path, spec):
    fingerprint = {'spec_sha256':sha256(spec_path),'code_sha256':sha256(Path(__file__)),
                   'helper_sha256':sha256(ASSETS / 'p7_5_2_qwen_edit_2511_generate_mira_torso.py')}
    state_path = out / 'generation-state.json'
    if state_path.exists():
        old = json.loads(state_path.read_text())
        assert old['fingerprint'] == fingerprint, 'Changed spec/code: use a new output directory'
    state = {'model_id':MODEL_ID,'fingerprint':fingerprint,'status':'preflight','completed':[], 'current':None}
    pending=[]
    for item in spec['items']:
        png=out/(item['id']+'.png'); record=out/(item['id']+'-result.json')
        if png.exists() or record.exists():
            assert png.exists() and record.exists(), f'Partial output: {item["id"]}; preserve it and use a new directory'
            data=json.loads(record.read_text())
            assert data['fingerprint']==fingerprint and data['output']['sha256']==sha256(png), 'Existing result mismatch'
            state['completed'].append(item['id'])
        else:
            pending.append(item)
    write(state_path,state)
    try:
        if not pending:
            state['status']='generated_pending_review'; return
        import torch
        from PIL import Image
        from diffusers import QwenImageEditPlusPipeline
        if not torch.cuda.is_available():
            raise RuntimeError('CUDA unavailable: no image generated; restore GPU/driver access and rerun the same command')
        cfg=spec['settings']; size=cfg['size']
        pipe=QwenImageEditPlusPipeline.from_pretrained(MODEL_ID,torch_dtype=torch.bfloat16,cache_dir=CACHE_DIR,local_files_only=True)
        pipe.enable_sequential_cpu_offload(); pipe.vae.enable_slicing()
        for item in pending:
            state['current']=item['id']; state['status']='generating'; write(state_path,state)
            print('Generating '+item['id'],flush=True)
            ref=spec['references'][item['reference']]
            with Image.open(ROOT/ref['path']) as opened:
                assert opened.width==opened.height
                image=opened.convert('RGB').resize((size,size),Image.Resampling.LANCZOS)
            started=time.monotonic()
            with torch.inference_mode():
                result=pipe(image=[image],prompt=item['prompt'],negative_prompt=' ',width=size,height=size,num_inference_steps=cfg['steps'],true_cfg_scale=cfg['true_cfg_scale'],guidance_scale=1.0,generator=torch.Generator(device='cuda').manual_seed(item['seed'])).images[0]
            assert result.size==(size,size)
            png=out/(item['id']+'.png'); result.save(png)
            write(out/(item['id']+'-result.json'),{'status':'generated_pending_review','model_id':MODEL_ID,'fingerprint':fingerprint,'design':item,'input':ref,'settings':cfg,'reference_preprocessing':'RGB Lanczos square resize to target size','runtime':runtime_record(),'gpu':torch.cuda.get_device_name(),'dtype':'bfloat16','device_placement':'sequential_cpu_offload','elapsed_seconds':round(time.monotonic()-started,2),'output':{'path':str(png),'sha256':sha256(png)}})
            state['completed'].append(item['id']); write(state_path,state)
        state['current']=None; state['status']='generated_pending_review'
    except Exception as error:
        state['status']='failed'; state['error']=str(error)
        raise
    finally:
        write(state_path,state)


if __name__=='__main__':
    main()

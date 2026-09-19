#!/usr/bin/env python3
"""Generate raw MoMask motions; keep upstream generation functions, omit BVH/IK.
Run from repository root. Requires official source and previously downloaded weights.
"""
import argparse, ast, hashlib, json, subprocess, sys, time
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[6]
SOURCE = ROOT / '.tmp/download/sources/p7-5-15/momask'
WEIGHTS = ROOT / '.tmp/download/artifacts/weight-p7-5-15-momask-humanml3d'
CLIP = ROOT / '.tmp/download/artifacts/weight-p7-5-15-momask-clip/ViT-B-32.pt'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--frames',type=int,default=48)
    ap.add_argument('--walk-prompt',default='A person walks forward.')
    ap.add_argument('--run-prompt',default='A person runs forward.')
    ap.add_argument('--seeds',type=int,nargs='+',default=[10107,10108,10109])
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    assert 4<=args.frames<=196 and args.frames%4==0
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    if (out/'result.json').exists():
        raise SystemExit('Existing experiment found; use a new output directory.')
    sys.path.insert(0,str(SOURCE))
    import numpy as np
    # Upstream quaternion module uses the removed alias; float has identical semantics.
    np.float = float
    import torch
    from models.vq.model import RVQVAE, LengthEstimator
    from models.mask_transformer.transformer import MaskTransformer, ResidualTransformer
    from utils.get_opt import get_opt
    from utils.fixseed import fixseed
    from utils.motion_process import recover_from_ric
    assert torch.cuda.is_available(), 'CUDA required for this experiment'
    torch.set_num_threads(4)
    device=torch.device('cuda:0')
    # Load unchanged upstream functions without importing the legacy BVH renderer.
    tree=ast.parse((SOURCE/'gen_t2m.py').read_text())
    module=ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[])
    scope=dict(torch=torch,pjoin=__import__('os').path.join,RVQVAE=RVQVAE,
               LengthEstimator=LengthEstimator,MaskTransformer=MaskTransformer,
               ResidualTransformer=ResidualTransformer,clip_version=str(CLIP))
    exec(compile(module,str(SOURCE/'gen_t2m.py'),'exec'),scope)
    staging=ROOT/'.tmp/experiments/p7-5-15/checkpoints';staging.mkdir(parents=True,exist_ok=True)
    if not (staging/'t2m').exists():(staging/'t2m').symlink_to(WEIGHTS,target_is_directory=True)
    name='t2m_nlayer8_nhead6_ld384_ff1024_cdp0.1_rvq6ns'
    resname='tres_nlayer8_ld384_ff1024_rvq6ns_cdp0.2_sw'
    opt=SimpleNamespace(name=name,device=device)
    mo=get_opt(str(WEIGHTS/name/'opt.txt'),device,checkpoints_dir=str(staging))
    vo=get_opt(str(WEIGHTS/mo.vq_name/'opt.txt'),device,checkpoints_dir=str(staging));vo.dim_pose=263
    ro=get_opt(str(WEIGHTS/resname/'opt.txt'),device,checkpoints_dir=str(staging))
    torch.cuda.reset_peak_memory_stats();start=time.perf_counter()
    vq,_=scope['load_vq_model'](vo)
    mo.num_tokens=vo.nb_code;mo.num_quantizers=vo.num_quantizers;mo.code_dim=vo.code_dim
    residual=scope['load_res_model'](ro,vo,opt)
    model=scope['load_trans_model'](mo,opt,'latest.tar')
    for m in [vq,residual,model]:m.eval().to(device)
    torch.cuda.synchronize();load_seconds=time.perf_counter()-start
    mean=np.load(WEIGHTS/mo.vq_name/'meta/mean.npy');std=np.load(WEIGHTS/mo.vq_name/'meta/std.npy')
    prompts={'walk':args.walk_prompt,'run':args.run_prompt}
    result={'section_id':'P7-5.15','status':'running','source_revision':subprocess.check_output(['git','-C',str(SOURCE),'rev-parse','HEAD'],text=True).strip(),'runner_sha256':sha(Path(__file__)), 'gpu':torch.cuda.get_device_name(), 'torch':torch.__version__, 'numpy':np.__version__,'fps':20,'frames':args.frames,'batch_size':1,'mask_steps':18,'mask_guidance':4,'residual_guidance':5,'temperature':1,'topk_filter_threshold':0.9,'postprocessing':'none: raw recover_from_ric, no BVH IK, no per-frame ground alignment','load_seconds':load_seconds,'weights':{str(p.relative_to(ROOT)):sha(p) for p in list(WEIGHTS.rglob('*.tar'))+[CLIP]},'samples':[]}
    for action,prompt in prompts.items():
        for seed in args.seeds:
            fixseed(seed);t=time.perf_counter()
            with torch.inference_mode():
                lengths=torch.tensor([args.frames//4],device=device)
                tokens=model.generate([prompt],lengths,timesteps=18,cond_scale=4,temperature=1,topk_filter_thres=.9,gsample=False)
                tokens=residual.generate(tokens,[prompt],lengths,temperature=1,cond_scale=5)
                raw=vq.forward_decoder(tokens).cpu().numpy()[0]*std+mean
                joints=recover_from_ric(torch.from_numpy(raw).float(),22).numpy()
            torch.cuda.synchronize()
            assert joints.shape==(args.frames,22,3) and np.isfinite(joints).all()
            path=out/f'{action}-{seed}.npz';np.savez_compressed(path,joints=joints,features=raw)
            result['samples'].append({'action':action,'prompt':prompt,'seed':seed,'file':path.name,'sha256':sha(path),'seconds':time.perf_counter()-t})
            (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print('COMPLETED',action,seed,flush=True)
    result.update(status='generated_not_visually_reviewed',peak_allocated_bytes=torch.cuda.max_memory_allocated(),peak_reserved_bytes=torch.cuda.max_memory_reserved())
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()

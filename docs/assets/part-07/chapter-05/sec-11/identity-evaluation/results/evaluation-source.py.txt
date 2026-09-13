#!/usr/bin/env python3
"""Evaluate identity from a neutral canvas: no face or hair in the model input."""
import argparse,json,time,fcntl,shutil
from pathlib import Path
from p7_5_2_qwen_edit_2511_generate_mira_torso import ROOT,ASSETS,CACHE_DIR,MODEL_ID,sha256,runtime_record
from p7_5_11_generate_supplements import write

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--dry-run',action='store_true');p.add_argument('--resume-from',type=Path);a=p.parse_args()
 spec=json.loads((ASSETS/'p7-5-11/datasets/identity-evaluation/spec.json').read_text())
 checkpoint=ROOT/'.tmp/p7-5-11/lora-v2-run100-retry1/checkpoints/mira_identity.safetensors'
 assert sha256(checkpoint)=='d76b96198d210ef27a9d97955315e4dfec8f688044d9a832520281a10698d0f3'
 assert spec['evaluation_type']=='identity_from_neutral_canvas' and spec['model']==MODEL_ID
 cases=spec['cases']
 from PIL import Image
 for case in cases:
  ref=case['reference'];assert sha256(ROOT/ref['path'])==ref['sha256']
  with Image.open(ROOT/ref['path']) as im:
   assert im.mode=='RGB' and im.size==(512,512) and im.getextrema()==((240,240),)*3, 'Identity evaluation requires a neutral canvas without facial information'
 plan={'model':MODEL_ID,'checkpoint':str(checkpoint),'checkpoint_sha256':sha256(checkpoint),'size':512,'steps':20,'cfg':4.0,'scales':[0,1],'cases':cases,'code_sha256':sha256(Path(__file__)),'runtime':runtime_record()}
 if a.dry_run:print(json.dumps(plan,ensure_ascii=False,indent=2));return
 out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
 with (out/'.lock').open('w') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  if (out/'plan.json').exists():assert json.loads((out/'plan.json').read_text())==plan
  if a.resume_from:
   assert a.resume_from.resolve()!=out
   prior=json.loads((a.resume_from/'plan.json').read_text())
   for field in ('model','checkpoint_sha256','size','steps','cfg','scales','cases'):assert prior[field]==plan[field],field
   write(out/'prior-plan.json',prior)
   for record in a.resume_from.glob('*-result.json'):
    data=json.loads(record.read_text());png=record.with_name(record.name.replace('-result.json','.png'))
    assert data['output_sha256']==sha256(png) and data['plan_sha256']==sha256(a.resume_from/'plan.json')
    for source in (record,png):
     target=out/source.name
     if target.exists():assert sha256(target)==sha256(source)
     else:shutil.copy2(source,target)
  write(out/'plan.json',plan)
  state={'status':'loading','completed':[],'current':None};write(out/'state.json',state)
  try:
   import torch
   from PIL import Image
   from diffusers import QwenImageEditPlusPipeline
   assert torch.cuda.is_available()
   pipe=QwenImageEditPlusPipeline.from_pretrained(MODEL_ID,torch_dtype=torch.bfloat16,cache_dir=CACHE_DIR,local_files_only=True)
   pipe.load_lora_weights(str(checkpoint.parent),weight_name=checkpoint.name,adapter_name='mira',local_files_only=True)
   assert 'mira' in pipe.get_active_adapters()
   pipe.enable_sequential_cpu_offload();pipe.vae.enable_slicing()
   for case in cases:
    with Image.open(ROOT/case['reference']['path']) as im:ref=im.convert('RGB').resize((512,512),Image.Resampling.LANCZOS)
    for scale in plan['scales']:
     key=case['id']+('-base' if scale==0 else '-lora');png=out/(key+'.png');record=out/(key+'-result.json')
     if png.exists() or record.exists():
      assert png.exists() and record.exists();assert json.loads(record.read_text())['output_sha256']==sha256(png)
      state['completed'].append(key);continue
     state.update(status='generating',current=key);write(out/'state.json',state);print(key,flush=True)
     with torch.inference_mode():
      if scale:pipe.enable_lora();pipe.set_adapters('mira',adapter_weights=scale)
      else:pipe.disable_lora()
     start=time.monotonic()
     with torch.inference_mode():
      result=pipe(image=[ref],prompt=case['prompt'],negative_prompt=' ',width=512,height=512,num_inference_steps=20,true_cfg_scale=4.0,guidance_scale=1.0,generator=torch.Generator(device='cuda').manual_seed(case['seed'])).images[0]
     result.save(png)
     write(record,{'case':case,'scale':scale,'checkpoint_sha256':plan['checkpoint_sha256'],'plan_sha256':sha256(out/'plan.json'),'output_sha256':sha256(png),'elapsed_seconds':round(time.monotonic()-start,2),'status':'pending_visual_review'})
     state['completed'].append(key);write(out/'state.json',state)
   state.update(status='generated_pending_visual_review',current=None)
  except BaseException as e:state.update(status='failed',error=str(e));raise
  finally:write(out/'state.json',state)
if __name__=='__main__':main()

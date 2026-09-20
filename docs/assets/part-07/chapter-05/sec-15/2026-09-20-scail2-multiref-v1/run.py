"""SCAIL-2 Q4_K_M inference through a pinned ComfyUI backend, no web server.
Reuses VACE's UMT5 prompt embeddings. All models are local and publicly accessible.
"""
from pathlib import Path
import sys,json,time,hashlib,traceback,importlib.util,subprocess,os,argparse
O=Path(__file__).resolve().parent;R=O.parents[5];S=R/'.tmp/download/sources/p7-5-15';COMFY=S/'ComfyUI-scail2'
ap=argparse.ArgumentParser();ap.add_argument('--attempt',default='multiref-dpo-q4-704');ap.add_argument('--frames',type=int,default=33);ap.add_argument('--steps',type=int,default=40);ap.add_argument('--shift',type=float,default=3.0);ap.add_argument('--dry-run',action='store_true');a=ap.parse_args()
if a.dry_run:
 print(json.dumps({'attempt':a.attempt,'steps':a.steps,'shift':a.shift,'frames':a.frames,'resolution':[704,704],'existing_output':(O/a.attempt).exists(),'new_runs':0 if (O/a.attempt).exists() else 1}));sys.exit(0)
sys.path.insert(0,str(R/'.tmp/experiments/p7-5-15/scail2-deps'))
sys.path.insert(0,str(COMFY))
import comfy.options
comfy.options.enable_args_parsing(False)
from comfy.cli_args import args
args.lowvram=True;args.disable_dynamic_vram=True;args.reserve_vram=1.2
import torch,numpy as np
from PIL import Image
import nodes,folder_paths,comfy.sd,comfy.utils,comfy.model_management as mm
from comfy_extras.nodes_scail import WanSCAILToVideo
from comfy_extras.nodes_model_advanced import ModelSamplingSD3
# Load GGUF as an isolated package; no custom-node directory mutation.
spec=importlib.util.spec_from_file_location('scail_gguf',S/'ComfyUI-GGUF/__init__.py',submodule_search_locations=[str(S/'ComfyUI-GGUF')]);mod=importlib.util.module_from_spec(spec);sys.modules['scail_gguf']=mod;spec.loader.exec_module(mod)
from scail_gguf.nodes import UnetLoaderGGUF
records=json.loads((O/'download-record.json').read_text())+json.loads((O/'reused-models.json').read_text());paths={r['repo']:R/r['snapshot'] for r in records}
weight=paths['vantagewithai/SCAIL-2-GGUF-ComfyUI']/'wan2.1_14B_SCAIL_2-Q4_K_M.gguf';vaep=paths['Comfy-Org/Wan_2.1_ComfyUI_repackaged']/'split_files/vae/wan_2.1_vae.safetensors'
folder_paths.add_model_folder_path('unet',str(weight.parent));folder_paths.add_model_folder_path('diffusion_models',str(weight.parent));folder_paths.add_model_folder_path('unet_gguf',str(weight.parent))
case=O/a.attempt;case.mkdir(exist_ok=False);torch.set_num_threads(4);torch.cuda.reset_peak_memory_stats();start=time.perf_counter()
pr={'cache_sha256':json.loads((O/'baseline-conditions.json').read_text())['prompt_cache_sha256']};cache=R/'.tmp/experiments/p7-5-15/vace-prompt.pt';assert hashlib.sha256(cache.read_bytes()).hexdigest()==pr['cache_sha256']
reference_paths=[O/'reference-native-704.png',O/'reference-closeup-704.png']
inputs=reference_paths+sorted((O/'poses').glob('*.png'))[:a.frames]
result={'status':'running','model':'SCAIL-2, community GGUF Q4_K_M','weights':records,'frames':a.frames,'steps':a.steps,'resolution':[704,704],'seed':23123134,'cfg':5.0,'sampling_shift':a.shift,'sampler':'uni_pc','scheduler':'simple','fps':20,'pose_strength':1.0,'prompt_record':'baseline-conditions.json (embeddings hash verified; original prompt text unavailable)','prompt_cache_sha256':pr['cache_sha256'],'gpu':torch.cuda.get_device_name(),'torch':torch.__version__,'source_revisions':{name:subprocess.check_output(['git','-C',str(S/name),'rev-parse','HEAD'],text=True).strip() for name in ['ComfyUI-scail2','ComfyUI-GGUF','SCAIL-Pose']},'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'inputs':{str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'limitations':['Q4 quantization; not original BF16 benchmark','Body motion from MoMask; geometric head proxies; no finger overlay','Legacy reference and cached text embeddings reused; original prompt text unavailable','No CLIP vision conditioning used']}
result['controlled_change']='Add one close-up reference from same original image with same identity mask; keep full-body reference, poses, seed, DPO and 704p sampling settings'
result['dpo_lora']=json.loads((O/'dpo-record.json').read_text())
result['dpo_strength']=1.0
baseline=json.loads((O/'baseline-conditions.json').read_text())
for key in ['frames','steps','resolution','seed','cfg','sampling_shift','fps','prompt_cache_sha256','source_revisions','dpo_strength','weights','sampler','scheduler']:
 assert result[key]==baseline[key],key
assert {k:v for k,v in result['inputs'].items() if k.startswith('poses/')}=={k:v for k,v in baseline['inputs'].items() if k.startswith('poses/')}
result['reference_preparation']=json.loads((O/'native-reference-preparation.json').read_text())
(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
try:
 with torch.inference_mode():
  vae=comfy.sd.VAE(sd=comfy.utils.load_torch_file(str(vaep)))
  result['vae_dtype_actual']=str(vae.vae_dtype);assert vae.vae_dtype==torch.bfloat16
  data=torch.load(cache,map_location='cpu',weights_only=True);positive=[[data['positive'],{}]];negative=[[data['negative'],{}]]
  reference=torch.from_numpy(np.stack([np.array(Image.open(p).convert('RGB')) for p in reference_paths]).astype(np.float32)/255)
  poses=torch.from_numpy(np.stack([np.array(Image.open(p).convert('RGB')) for p in inputs[2:]]).astype(np.float32)/255)
  refmask=torch.from_numpy(np.stack([np.array(Image.open(O/'reference-mask.png').resize((704,704),Image.Resampling.NEAREST)),np.array(Image.open(O/'reference-closeup-mask.png'))]).astype(np.float32)/255)
  posemask=torch.from_numpy(np.stack([np.array(Image.open(p)) for p in sorted((O/'pose-masks').glob('*.png'))[:a.frames]]).astype(np.float32)/255)
  result['mask_inputs']={str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/'reference-mask.png']+sorted((O/'pose-masks').glob('*.png'))}
  result['limitations'] += ['Experimental multi-reference; full-body baseline preserved for direct comparison', 'Reference segmentation uses color-background separation, not SAM3', 'Inherited low subject resolution and missing finger controls']
  assert result['mask_inputs']==baseline['mask_inputs']
  result['mask_inputs']['reference-closeup-mask.png']=hashlib.sha256((O/'reference-closeup-mask.png').read_bytes()).hexdigest()
  result['closeup_preparation']=json.loads((O/'closeup-preparation.json').read_text())
  print('ENCODE CONDITIONS',flush=True)
  cond=WanSCAILToVideo.execute(positive,negative,vae,704,704,a.frames,1,1.0,0.0,1.0,video_frame_offset=0,previous_frame_count=5,reference_image=reference,pose_video=poses,reference_image_mask=refmask,pose_video_mask=posemask)
  positive,negative,latent=cond[0],cond[1],cond[2]
  refs=positive[0][1]['reference_latents']
  assert len(refs)==2
  negative=[[ctx,{**meta,'reference_latents':refs}] for ctx,meta in negative]
  assert all(torch.equal(meta['reference_latents'][0],refs[0]) for _,meta in negative)
  result['cfg_reference_condition']='same encoded reference in positive and negative branches, matching official SCAIL'
  result['reference_latent_sha256']=hashlib.sha256(refs[0].float().cpu().numpy().tobytes()).hexdigest()
  mm.unload_all_models();mm.soft_empty_cache()
  print('LOAD SCAIL Q4',flush=True)
  model=UnetLoaderGGUF().load_unet(weight.name,dequant_dtype='bfloat16',patch_dtype='bfloat16',patch_on_device=False)[0]
  import comfy.lora
  dpo=result['dpo_lora'];lorap=R/dpo['converted_file']
  assert hashlib.sha256(lorap.read_bytes()).hexdigest()==dpo['converted_sha256']
  lora=comfy.utils.load_torch_file(str(lorap));keymap=comfy.lora.model_lora_keys_unet(model.model,{})
  expected=set()
  for key in lora:
   suffix=next((x for x in ['.lora_down.weight','.lora_up.weight','.diff_b'] if key.endswith(x)),None)
   assert suffix,key
   prefix=key[:-len(suffix)];assert prefix in keymap,key
   target=keymap[prefix]
   expected.add(target[:-len('.weight')]+'.bias' if suffix=='.diff_b' else target)
  patches=comfy.lora.load_lora(lora,keymap)
  assert set(patches)==expected,(len(patches),len(expected))
  model=model.clone();applied=model.add_patches(patches,1.0);assert set(applied)==expected
  result['dpo_applied_patches']=len(applied)
  result['dpo_tensor_count']=len(lora)
  (case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
  print('DPO APPLIED',len(applied),'patches',flush=True)
  model=ModelSamplingSD3().patch(model,a.shift)[0]
  print('SAMPLE',flush=True)
  samples=nodes.common_ksampler(model,23123134,a.steps,5.0,'uni_pc','simple',positive,negative,latent,denoise=1.0)[0]
  # Only final images and execution metadata retained.
  del model;mm.unload_all_models();mm.soft_empty_cache()
  print('DECODE',flush=True)
  imgs=vae.decode_tiled(samples['samples'],tile_x=256,tile_y=256,overlap=64,tile_t=16,overlap_t=4)
  if imgs.ndim==5: imgs=imgs.reshape(-1,*imgs.shape[-3:])
  import imageio.v2 as imageio
  arr=(imgs.cpu().numpy().clip(0,1)*255).round().astype(np.uint8);hashes=[]
  with imageio.get_writer(case/'animation.mp4',fps=20) as w:
   for i,x in enumerate(arr):
    p=case/f'frame_{i:03d}.png';Image.fromarray(x).save(p);w.append_data(x);hashes.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
  (case/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
  result['status']='generated_not_reviewed';result['output_frames']=len(arr)
except Exception:
 result['status']='execution_failed';result['error']=traceback.format_exc();print(result['error'],flush=True)
finally:
 result['seconds']=time.perf_counter()-start;result['peak_allocated_bytes']=torch.cuda.max_memory_allocated();result['peak_reserved_bytes']=torch.cuda.max_memory_reserved();(case/'result.json').write_text(json.dumps(result,indent=2)+'\n')
if result['status']=='execution_failed':sys.exit(1)

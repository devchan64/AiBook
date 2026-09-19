#!/usr/bin/env python3
"""Run the official basic inference script against local models and prepared inputs."""
from pathlib import Path
import os,sys,json,runpy,time,traceback,subprocess,hashlib,argparse
ap=argparse.ArgumentParser();ap.add_argument('--name',default='stableanimator-walk-v1');args=ap.parse_args()
root=Path(__file__).resolve().parents[6];src=root/'.tmp/download/sources/p7-5-15/StableAnimator';out=root/'docs/assets/part-07/chapter-05/sec-15/2026-09-19-momask-stableanimator-v1'/args.name
if (out/'result.json').exists():raise SystemExit('Existing result: use another experiment name')
import torch
torch.set_num_threads(4)
assert torch.cuda.is_available()
os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
sys.path.insert(0,str(src));os.chdir(src)
snap=(src/'checkpoints').resolve();torch.cuda.reset_peak_memory_stats();t=time.perf_counter()
sys.argv=['inference_basic.py','--pretrained_model_name_or_path',str(snap/'stable-video-diffusion-img2vid-xt'),'--output_dir',str(out/'output'),'--validation_control_folder',str(out/'poses'),'--validation_image',str(out/'reference-512.png'),'--width','512','--height','512','--guidance_scale','3','--num_inference_steps','25','--posenet_model_name_or_path',str(snap/'Animation/pose_net.pth'),'--face_encoder_model_name_or_path',str(snap/'Animation/face_encoder.pth'),'--unet_model_name_or_path',str(snap/'Animation/unet.pth'),'--tile_size','16','--overlap','4','--frames_overlap','4','--decode_chunk_size','1','--noise_aug_strength','0.02']
record={'section_id':'P7-5.15','source_revision':subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True).strip(),'argv':sys.argv,'gpu':torch.cuda.get_device_name(),'torch':torch.__version__,'status':'running'}
try:
 runpy.run_path(str(src/'inference_basic.py'),run_name='__main__');record['status']='generated_not_reviewed'
except Exception as e:
 record.update(status='failed',error=repr(e),traceback=traceback.format_exc());traceback.print_exc()
finally:
 record.update(seconds=time.perf_counter()-t,peak_allocated_bytes=torch.cuda.max_memory_allocated(),peak_reserved_bytes=torch.cuda.max_memory_reserved())
 (out/'result.json').write_text(json.dumps(record,indent=2)+'\n')
if record['status']=='failed':raise SystemExit(1)

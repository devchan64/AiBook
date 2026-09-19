from pathlib import Path
import json,sys,importlib.util,hashlib,argparse
import numpy as np
from PIL import Image
ap=argparse.ArgumentParser();ap.add_argument('--motion',default='momask-v1/walk-10107.npz');ap.add_argument('--start',type=int,default=0);ap.add_argument('--name',default='stableanimator-walk-v1');args=ap.parse_args()
root=Path.cwd();src=root/'.tmp/download/sources/p7-5-15/StableAnimator';out=root/'docs/assets/part-07/chapter-05/sec-15/2026-09-19-momask-stableanimator-v1'/args.name;out.mkdir(exist_ok=True)
record=json.loads((root/'.tmp/download/sources/p7-5-15/FrancisRing--StableAnimator.json').read_text());snap=root/'.tmp/download/huggingface/hub/models--FrancisRing--StableAnimator/snapshots'/record['revision']
for a,b in [(src/'models',snap/'models'),(src/'checkpoints',snap)]:
 if not a.exists():a.symlink_to(b,target_is_directory=True)
# facexlib uses its package-local weights folder by default; use explicit local root via wrapper below.
spec=importlib.util.spec_from_file_location('poseutil',src/'DWPose/dwpose_utils/util.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
j=np.load(root/'docs/assets/part-07/chapter-05/sec-15/2026-09-19-momask-stableanimator-v1'/args.motion)['joints'][args.start:args.start+32]
# HumanML3D -> OpenPose18: omit unavailable nose/eye/ear landmarks, keep neck and body.
indices=[None,12,17,19,21,16,18,20,2,5,8,1,4,7,None,None,None,None]
scale=min(390/(j[:,:,1].max()-j[:,:,1].min()),440/np.ptp(j[:,:,2]));cx=(j[:,:,2].max()+j[:,:,2].min())/2;floor=np.percentile(j[:,[7,10,8,11],1],1)
frames=out/'poses';frames.mkdir(exist_ok=True);coords=[]
for t in range(32):
 pts=np.zeros((18,2));subset=np.full((1,18),-1.)
 for k,idx in enumerate(indices):
  if idx is not None:pts[k]=[(256+(j[t,idx,2]-cx)*scale)/512,(455-(j[t,idx,1]-floor)*scale)/512];subset[0,k]=k
 canvas=m.draw_bodypose(np.zeros((512,512,3),np.uint8),pts,subset);Image.fromarray(canvas).save(frames/f'frame_{t}.png');coords.append(pts.tolist())
ref=root/'docs/assets/part-07/chapter-05/sec-03/p7-5-3-qwen-edit-prompt-style-outfit_stage3_jacket_face-three-stage-v1-seed-62294-steps-10.png'
im=Image.open(ref).convert('RGB');im.thumbnail((512,512));canvas=Image.new('RGB',(512,512),(255,253,229));canvas.paste(im,((512-im.width)//2,(512-im.height)//2));canvas.save(out/'reference-512.png')
(out/'plan.json').write_text(json.dumps({'source_motion':'../'+args.motion,'source_frames':list(range(args.start,args.start+32)),'reference':str(ref.relative_to(root)),'reference_sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'reference_preprocess':'aspect-preserving fit into 512 square; pale canvas padding','pose_mapping':indices,'camera':'fixed orthographic z/y, constant scale and floor for entire 32-frame clip','pose_normalized_xy':coords,'steps':25,'seed':23123134,'guidance':3,'status':'prepared','limitation':'body-only mapping without nose/face/hands; stylized frontal reference to side-motion is unvalidated'},indent=2)+'\n')
print(out)

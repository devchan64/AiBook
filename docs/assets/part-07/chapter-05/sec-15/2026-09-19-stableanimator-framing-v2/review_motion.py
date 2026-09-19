from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw
import imageio.v2 as imageio
base=Path(__file__).resolve().parent
if json.loads((base/'plan.json').read_text())['status'] == 'blocked_source_discarded':
 raise SystemExit('Source experiment discarded; historical review assets retained.')
j=np.load(base.parent/'2026-09-19-momask-stableanimator-v1/momask-v2/run-10109.npz')['joints'][36:68]
chains=[([0,1,4,7,10],'#2474d2'),([0,2,5,8,11],'#d64040'),([0,3,6,9,12,15],'#666666'),([9,13,16,18,20],'#2474d2'),([9,14,17,19,21],'#d64040')]
fig,axs=plt.subplots(4,8,figsize=(20,10))
for t,ax in enumerate(axs.flat):
 for ids,color in chains:
  ax.plot(j[t,ids,2]-j[t,0,2],j[t,ids,1],color=color,lw=2,marker='o',ms=2)
 for idx,label,color in [(7,'L','#2474d2'),(8,'R','#d64040')]:
  ax.text(j[t,idx,2]-j[t,0,2],j[t,idx,1]-.09,label,color=color,fontsize=9)
 ax.set(xlim=(-.95,.95),ylim=(-.2,1.75),title=f'{t} / source {t+36}',aspect='equal');ax.axis('off')
fig.suptitle('Consecutive raw motion: LEFT blue / RIGHT red; ankles labelled; toes included',fontsize=14)
fig.tight_layout();fig.savefig(base/'motion-continuous-32.jpg',dpi=120);plt.close(fig)
with imageio.get_writer(str(base/'poses-centered-large-20fps.mp4'),fps=20,codec='libx264') as writer:
 for t in range(32):writer.append_data(np.asarray(Image.open(base/'centered-large/poses'/f'frame_{t}.png').convert('RGB')))
z=j[:,7,2]-j[:,8,2];cross=(np.where(z[:-1]*z[1:]<0)[0]+1).tolist()
fig,axs=plt.subplots(2,1,figsize=(10,6))
for idx,label,color in [(7,'Left ankle','#2474d2'),(8,'Right ankle','#d64040')]:
 axs[0].plot(range(32),j[:,idx,2]-j[:,0,2],label=label,color=color)
 axs[1].plot(range(32),j[:,idx,1],label=label,color=color)
axs[0].set_ylabel('Forward relative to root (m)');axs[1].set_ylabel('Raw ankle height (m)');axs[1].set_xlabel('Output frame (source frame minus 36)');axs[0].legend()
for ax in axs:
 ax.grid(alpha=.2)
 for t in [13,20,26]:ax.axvline(t,color='gray',ls='--',alpha=.5)
fig.tight_layout();fig.savefig(base/'foot-trajectories.png',dpi=130);plt.close(fig)
(base/'motion-diagnostics.json').write_text(json.dumps({'status':'diagnostics_only','preview_limitation':'Original comparison selects six nonconsecutive flight-candidate frames, not a temporal sequence.','ankle_fore_aft_sign_change_frames':cross,'ignore_initial_near_zero_crossing':True,'main_crossings':[13,20,26],'main_crossing_source_frames':[49,56,62],'side_mapping':'HumanML3D left 1,4,7,10; right 2,5,8,11; same identity each frame','openpose_limitation':'body-only ankle endpoints, no toe joints or depth/occlusion labels','interpretation':'Numerical diagnostics only; current user review is recorded separately in motion-review.json.'},indent=2)+'\n')

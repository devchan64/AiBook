#!/usr/bin/env python3
"""Render fixed side views and foot-clearance diagnostics for raw HumanML3D joints."""
import argparse,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import imageio.v2 as imageio
CHAINS=[([0,2,5,8,11],'#d24b42'),([0,1,4,7,10],'#3478bf'),([0,3,6,9,12,15],'#525252'),([9,14,17,19,21],'#d24b42'),([9,13,16,18,20],'#3478bf')]
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('folder',type=Path);a=ap.parse_args();r=json.loads((a.folder/'result.json').read_text());summary=[]
 all_joints=[np.load(a.folder/s['file'])['joints'] for s in r['samples']]
 low=min(float(j[:,:,2].min()) for j in all_joints)-.25;high=max(float(j[:,:,2].max()) for j in all_joints)+.25
 shared_span=max(high-low,1.8);shared_center=(low+high)/2
 ylow=min(float(j[:,:,1].min()) for j in all_joints)-.15;yhigh=max(2.1,max(float(j[:,:,1].max()) for j in all_joints)+.15)
 for sample in r['samples']:
  name=Path(sample['file']).stem;j=np.load(a.folder/sample['file'])['joints'];n=len(j)
  # One floor estimate per clip, never per frame. Foot joints approximate sole clearance.
  floor=float(np.percentile(j[:,[7,10,8,11],1],1))
  left=np.min(j[:,[7,10],1],axis=1)-floor;right=np.min(j[:,[8,11],1],axis=1)-floor
  # HumanML3D locomotion points mainly along z. Preserve this fixed camera and all root motion.
  span=shared_span;center=shared_center
  def draw(ax,t):
   for chain,c in CHAINS:ax.plot(j[t,chain,2],j[t,chain,1],'-o',c=c,lw=1.6,ms=2)
   ax.axhline(floor,c='#888',lw=.7);ax.set(xlim=(center-span/2,center+span/2),ylim=(ylow,yhigh),aspect='equal');ax.axis('off');ax.set_title(f'{t:02d} / {t/20:.2f}s',fontsize=9)
  indices=np.linspace(0,n-1,12).round().astype(int)
  fig,axes=plt.subplots(2,6,figsize=(16,6))
  for ax,t in zip(axes.flat,indices):draw(ax,t)
  fig.suptitle(f'{name}: raw side view (red=right, blue=left); no IK',fontsize=14);fig.tight_layout();fig.savefig(a.folder/f'{name}-contact-sheet.png',dpi=120);plt.close(fig)
  frames=a.folder/f'{name}-frames';frames.mkdir(exist_ok=True)
  fig,ax=plt.subplots(figsize=(5.12,5.12),dpi=100)
  with imageio.get_writer(a.folder/f'{name}-side.mp4',fps=20,macro_block_size=1) as writer:
   for t in range(n):
    ax.clear();draw(ax,t);fig.canvas.draw();im=np.asarray(fig.canvas.buffer_rgba())[:,:,:3].copy();imageio.imwrite(frames/f'{t:03d}.png',im);writer.append_data(im)
  plt.close(fig)
  fig,ax=plt.subplots(figsize=(10,3));ts=np.arange(n)/20
  ax.plot(ts,left,label='left foot clearance');ax.plot(ts,right,label='right foot clearance');ax.axhline(.04,c='gray',ls='--',label='4 cm diagnostic threshold');ax.set(xlabel='time (s)',ylabel='height above estimated floor (m)',title=name);ax.legend();fig.tight_layout();fig.savefig(a.folder/f'{name}-clearance.png',dpi=120);plt.close(fig)
  delta=j[:,7,2]-j[:,8,2];sign=np.sign(delta[np.abs(delta)>.02]);alternations=int(np.count_nonzero(sign[1:]!=sign[:-1]))
  summary.append({'sample':name,'floor_estimate_m':floor,'ankle_fore_aft_sign_changes':alternations,'both_feet_above_threshold_frames':{str(h):np.flatnonzero((left>h)&(right>h)).tolist() for h in [.02,.04,.06]},'max_minimum_foot_clearance_m':float(np.minimum(left,right).max()),'pelvis_vertical_range_m':float(np.ptp(j[:,0,1]))})
 (a.folder/'diagnostics.json').write_text(json.dumps({'camera_bounds':{'z':[shared_center-shared_span/2,shared_center+shared_span/2],'y':[ylow,yhigh]},'method':'Common fixed world camera for every sample. Raw joints; floor=1st percentile of all four foot joint heights over entire clip. Threshold sensitivity only, not a physical contact ground truth. Fixed side projection z/y; no camera tracking.','samples':summary},indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()

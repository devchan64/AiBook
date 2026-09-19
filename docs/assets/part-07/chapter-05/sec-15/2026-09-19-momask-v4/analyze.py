"""Audit root reconstruction and screen raw motions. No corrections applied."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
BASE=Path(__file__).resolve().parent
rows=[]
fig,axes=plt.subplots(2,3,figsize=(12,7),sharex=True,sharey=True)
for ax,path in zip(axes.flat,sorted((BASE/'results').glob('*.npz'))):
 data=np.load(path);j=data['joints'];f=data['features'];root=j[:,0][:,[0,2]]
 angle=np.r_[0,np.cumsum(f[:-1,0])];v=np.vstack([np.zeros((1,2)),f[:-1,1:3]])
 c=np.cos(2*angle);s=np.sin(2*angle)
 independent=np.cumsum(np.column_stack([c*v[:,0]-s*v[:,1],s*v[:,0]+c*v[:,1]]),axis=0)
 error=float(np.max(np.abs(independent-root)));assert error<1e-5
 floor=float(np.percentile(j[:,[7,10,8,11],1],1));clear=np.min(j[:,[7,10,8,11],1],axis=1)-floor
 root_speed=np.linalg.norm(np.diff(root,axis=0),axis=1)*20
 feet={}
 for side,ankle,toe in [('left',7,10),('right',8,11)]:
  height=np.minimum(j[:,ankle,1],j[:,toe,1])-floor
  near=(height[:-1]<.025)&(height[1:]<.025)
  speed=np.linalg.norm(np.diff(j[:,toe][:,[0,2]],axis=0),axis=1)*20
  feet[side]={'near_floor_pair_count':int(near.sum()),'median_toe_horizontal_speed_m_s':float(np.median(speed[near])) if near.any() else None,'p90_toe_horizontal_speed_m_s':float(np.percentile(speed[near],90)) if near.any() else None}
  moving=near & (root_speed>.1)
  feet[side]['moving_near_floor_pairs']=int(moving.sum())
  feet[side]['moving_median_toe_speed_m_s']=float(np.median(speed[moving])) if moving.any() else None
 delta=j[:,7,2]-j[:,8,2];sign=np.sign(delta[np.abs(delta)>.02])
 net=float(np.linalg.norm(root[-1]-root[0]));pathlen=float(np.linalg.norm(np.diff(root,axis=0),axis=1).sum())
 row={'sample':path.stem,'root_speed_above_0_1_m_s_intervals':np.flatnonzero(root_speed>.1).tolist(),'initial_foot_clearance_m':float(clear[0]),'final_foot_clearance_m':float(clear[-1]),'both_feet_above_threshold_frames':{str(t):int((clear>t).sum()) for t in [.02,.04,.06]},'pelvis_vertical_range_m':float(np.ptp(j[:,0,1])),'root_net_displacement_m':net,'root_path_length_m':pathlen,'root_recovery_max_error_m':error,'ankle_fore_aft_sign_changes':int((sign[1:]!=sign[:-1]).sum()),'near_floor_toe_speed_proxy':feet,'passes_initial_height_and_travel_screen':bool(clear[0]<=.04 and net>=1)}
 rows.append(row);ax.plot(root[:,0],root[:,1]);ax.scatter(root[[0,-1],0],root[[0,-1],1],c=['green','red']);ax.set(title=path.stem,xlabel='world x (m)',ylabel='world z (m)',aspect='equal');ax.grid(alpha=.25)
fig.tight_layout();fig.savefig(BASE/'root-paths.png',dpi=130);plt.close(fig)
(BASE/'metrics.json').write_text(json.dumps({'method':'Clip-wide first-percentile foot floor. Near-floor proxy uses consecutive foot minima <2.5cm and measures toe horizontal speed; not true support contacts. Independent root velocity integration checks recovery consistency.','samples':rows},indent=2)+'\n')
print(json.dumps(rows,indent=2))

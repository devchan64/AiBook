"""Project saved HumanML22 joints to educational COCO18-style maps.

Dependencies: numpy, Pillow. No OpenPose inference; nose is a head proxy.
Camera: fixed orthographic view, fitted to the entire sequence, Y up.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw

NAMES = ['pelvis','left_hip','right_hip','spine1','left_knee','right_knee',
         'spine2','left_ankle','right_ankle','spine3','left_foot','right_foot',
         'neck','left_collar','right_collar','head','left_shoulder',
         'right_shoulder','left_elbow','right_elbow','left_wrist','right_wrist']
CHAINS = [[0,2,5,8,11],[0,1,4,7,10],[0,3,6,9,12,15],
          [9,14,17,19,21],[9,13,16,18,20]]
# OpenPose COCO18 slots 0..13; eyes/ears 14..17 are unavailable.
MAP = [15,12,17,19,21,16,18,20,2,5,8,1,4,7]
PAIRS = [(1,2),(1,5),(2,3),(3,4),(5,6),(6,7),(1,8),(8,9),
         (9,10),(1,11),(11,12),(12,13),(1,0)]
COLORS = [(255,0,0),(255,85,0),(255,170,0),(255,255,0),(170,255,0),
          (85,255,0),(0,255,0),(0,255,85),(0,255,170),(0,255,255),
          (0,170,255),(0,85,255),(0,0,255),(85,0,255)]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--motion',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--yaw',type=float,default=35,help='Orthographic camera yaw in degrees')
    args=ap.parse_args()
    with np.load(args.motion,allow_pickle=False) as data:
        joints=data['joints'].copy()
    if joints.ndim!=3 or joints.shape[1:]!=(22,3) or len(joints)==0 or not np.isfinite(joints).all():
        ap.error('Expected finite (T,22,3) joints')
    if not np.isfinite(args.yaw): ap.error('Yaw must be finite')
    args.output_dir.mkdir(parents=True,exist_ok=False)
    angle=np.deg2rad(args.yaw)
    xy=np.stack((joints[:,:,0]*np.cos(angle)-joints[:,:,2]*np.sin(angle),-joints[:,:,1]),axis=-1)
    low=xy.min(axis=(0,1));high=xy.max(axis=(0,1))
    extent=float((high-low).max())
    if extent<=0: raise ValueError('Degenerate motion')
    scale=440/extent
    xy=(xy-(low+high)/2)*scale+256
    records=[];frames=[]
    for index,points in enumerate(xy):
        pose=np.zeros((18,3));pose[:14,:2]=points[MAP];pose[:14,2]=1
        image=Image.new('RGB',(512,512),'black');draw=ImageDraw.Draw(image)
        for k,(a,b) in enumerate(PAIRS):
            draw.line([tuple(pose[a,:2]),tuple(pose[b,:2])],fill=COLORS[k],width=5)
        for k,(x,y,valid) in enumerate(pose[:14]):
            draw.ellipse((x-4,y-4,x+4,y+4),fill=COLORS[k])
        image.save(args.output_dir/f'pose-{index:04d}.png');frames.append(image)
        records.append({'frame':index,'people':[{'pose_keypoints_2d':pose.reshape(-1).tolist()}]})
    frames[0].save(args.output_dir/'pose-map-4fps.gif',save_all=True,
                   append_images=frames[1:],duration=250,loop=0)
    # Numbered input skeleton for joint-index inspection; same camera and frame.
    selected=min(29,len(xy)-1)
    image=Image.new('RGB',(512,512),'#18202d');draw=ImageDraw.Draw(image)
    for chain in CHAINS:
        draw.line([tuple(xy[selected,k]) for k in chain],fill='#9bbfe5',width=3)
    for k,(x,y) in enumerate(xy[selected]):
        draw.ellipse((x-3,y-3,x+3,y+3),fill='white')
        draw.text((x+5,y-9),str(k),fill='#ffe29a')
    image.save(args.output_dir/'humanml22-numbered.png')
    record={'source_sha256':hashlib.sha256(args.motion.read_bytes()).hexdigest(),
            'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'joint_names':NAMES,'coco18_to_humanml22':MAP+[None]*4,
            'camera':{'type':'orthographic','yaw_degrees':args.yaw,'sequence_center':((low+high)/2).tolist(),'pixels_per_unit':scale},
            'size':[512,512],'preview_fps':4,'frame_count':len(xy),'numbered_frame':selected,
            'limitations':['head substitutes nose','eyes and ears missing','no occlusion test',
                            'confidence 1 means synthetic availability, not detector confidence',
                            'illustrative line renderer, not a model-specific conditioning guarantee'],
            'frames':records}
    (args.output_dir/'pose-maps.json').write_text(json.dumps(record,indent=2)+'\n')


if __name__=='__main__':main()

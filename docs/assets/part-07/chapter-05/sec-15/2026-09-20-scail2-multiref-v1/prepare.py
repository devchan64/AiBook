from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_fill_holes
O=Path(__file__).resolve().parent;R=O.parents[5];B=O
r=json.loads((B/'native-reference-preparation.json').read_text());src=R/r['source']
assert hashlib.sha256(src.read_bytes()).hexdigest()==r['source_sha256']
box=[140,110,844,814]; im=Image.open(src).convert('RGB').crop(box);im.save(O/'reference-closeup-704.png')
a=np.array(im);fg=np.max(np.abs(a.astype(float)-np.array([255,253,231])),axis=-1)>35
lab,n=label(fg);counts=np.bincount(lab.ravel());counts[0]=0;fg=binary_fill_holes(lab==counts.argmax());m=np.full_like(a,255);m[fg]=[0,0,255];Image.fromarray(m).save(O/'reference-closeup-mask.png')
r={'source':r['source'],'source_sha256':r['source_sha256'],'crop':box,'resize':None,'output_size':[704,704],'identity_rgb':[0,0,255],'reference_order':['reference-native-704.png','reference-closeup-704.png'],'mask_method':'same largest component RGB-background separation as baseline, threshold 35 and hole filling','hashes':{n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in ['reference-closeup-704.png','reference-closeup-mask.png']}}
(O/'closeup-preparation.json').write_text(json.dumps(r,indent=2)+'\n')

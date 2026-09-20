from pathlib import Path
import json,hashlib,urllib.request,importlib.util,torch
from huggingface_hub import HfApi,hf_hub_download
from safetensors.torch import save_file
O=Path(__file__).resolve().parent;R=O.parents[5]
repo='zai-org/SCAIL-2';rev='150cc0ca4e98e50e60b9295dacde39442fdccab2'
assert HfApi(token=False).model_info(repo,revision=rev).gated is False
p=Path(hf_hub_download(repo,'model/bias-aware-dpo-lora.pt',revision=rev,token=False,cache_dir=R/'.tmp/download/huggingface/hub'))
source_rev='78fe19576bb06be96c2375e088574a262a300edb'
u=f'https://raw.githubusercontent.com/zai-org/SCAIL-2/{source_rev}/convert_lora.py'
source=R/'.tmp/download/sources/p7-5-15/scail2-convert-lora.py';source.write_bytes(urllib.request.urlopen(u).read())
spec=importlib.util.spec_from_file_location('convert_dpo',source);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
import numpy as np
with torch.serialization.safe_globals([np.ndarray,(np._core.multiarray._reconstruct,'numpy.core.multiarray._reconstruct'),np.dtype,type(np.dtype('uint32')),type(np.dtype('float64'))]):
 d=torch.load(p,map_location='cpu',weights_only=True)
print('Checkpoint keys',list(d)[:5],flush=True)
state=d.get('module',d.get('state_dict',d.get('model',d)));converted=mod.convert_state_dict(state)
out=R/'.tmp/download/artifacts/p7-5-15/scail2-bias-aware-dpo.safetensors';out.parent.mkdir(exist_ok=True,parents=True);save_file(converted,str(out))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as st:
  for b in iter(lambda:st.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
record={'repo':repo,'revision':rev,'gated':False,'source_file':str(p.relative_to(R)),'source_sha256':sha(p),'converted_file':str(out.relative_to(R)),'converted_sha256':sha(out),'converter_url':u,'converter_sha256':sha(source),'input_tensor_count':len(state),'output_tensor_count':len(converted),'keys':list(converted),'dtype':'unchanged'}
(O/'dpo-record.json').write_text(json.dumps(record,indent=2)+'\n');print('DPO READY',len(converted),flush=True)

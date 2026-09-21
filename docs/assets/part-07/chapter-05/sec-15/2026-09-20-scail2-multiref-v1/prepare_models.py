from pathlib import Path
import json,hashlib
from huggingface_hub import HfApi,snapshot_download
O=Path(__file__).resolve().parent;R=O.parents[5]
repo='vantagewithai/SCAIL-2-GGUF-ComfyUI';rev='8d99a4251592b5e834169bf9faeebeb36c553e07'
assert HfApi(token=False).model_info(repo,revision=rev).gated is False
p=Path(snapshot_download(repo,revision=rev,token=False,allow_patterns=['README.md','wan2.1_14B_SCAIL_2-Q4_K_M.gguf'],cache_dir=R/'.tmp/download/huggingface/hub'))
files=[]
for f in p.rglob('*'):
 if f.is_file():
  h=hashlib.sha256()
  with f.open('rb') as st:
   for b in iter(lambda:st.read(8*1024*1024),b''):h.update(b)
  files.append({'path':str(f.relative_to(p)),'bytes':f.stat().st_size,'sha256':h.hexdigest()})
(O/'download-record.json').write_text(json.dumps([{'repo':repo,'revision':rev,'gated':False,'snapshot':str(p.relative_to(R)),'files':files}],indent=2)+'\n')
print('DOWNLOAD COMPLETE',flush=True)

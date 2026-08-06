#!/usr/bin/env python3
"""Create one SD 1.5 depth-ControlNet storyboard probe for P7-5.3."""
from pathlib import Path
import json
import torch
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent / "p7-5-3-depth-storyboard-probe"
SD15 = Path("/home/cbsim/.cache/huggingface/hub/models--stable-diffusion-v1-5--stable-diffusion-v1-5/snapshots/451f4fe16113bff5a5d2269ed5ad43b0592e9a14")
DEPTH = Path(".tmp/p7-5-3-sd15-depth-controlnet")
PROMPT = "Korean webtoon storyboard, a woman on a rooftop terrace, distant buildings, thin charcoal contours, translucent watercolor washes"

def guide():
    image = Image.new("RGB", (512, 768), (235, 235, 235)); draw = ImageDraw.Draw(image)
    draw.rectangle((0, 430, 512, 768), fill=(115, 115, 115)); draw.rectangle((0, 360, 512, 430), fill=(165, 165, 165))
    draw.rectangle((205, 250, 300, 590), fill=(55, 55, 55)); draw.ellipse((205, 185, 300, 290), fill=(45, 45, 45))
    return image

def main():
    OUT.mkdir(exist_ok=True); control = guide(); control.save(OUT / "rooftop-depth-blockout.png")
    net = ControlNetModel.from_pretrained(DEPTH, torch_dtype=torch.float16)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(SD15, controlnet=net, torch_dtype=torch.float16, safety_checker=None).to("cuda")
    pipe.enable_attention_slicing(); pipe.set_progress_bar_config(disable=True); torch.cuda.reset_peak_memory_stats()
    common = dict(prompt=PROMPT, image=control, width=512, height=768, num_inference_steps=20, guidance_scale=7.0)
    off = pipe(**common, controlnet_conditioning_scale=0.0, generator=torch.Generator("cuda").manual_seed(5301)).images[0]
    on = pipe(**common, controlnet_conditioning_scale=1.0, generator=torch.Generator("cuda").manual_seed(5301)).images[0]
    off.save(OUT / "rooftop-depth-off.png"); on.save(OUT / "rooftop-depth-on.png")
    (OUT / "report.json").write_text(json.dumps({"status":"review_required","control":"depth","resolution":[512,768],"steps":20,"peak_vram_mib":round(torch.cuda.max_memory_allocated()/1024**2,1)}, indent=2))
if __name__ == "__main__": main()

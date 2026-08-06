#!/usr/bin/env python3
"""Compare a camera-composition Canny condition with an SDXL identity reference."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import torch
from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline
from PIL import Image, ImageDraw


ANIMAGINE = Path("/home/cbsim/.cache/huggingface/hub/models--cagliostrolab--animagine-xl-4.0/snapshots/2b7c1b397761bf5bd3cc42e5b39ec99314a75a96")
CONTROLNET = Path("/home/cbsim/.cache/huggingface/hub/models--diffusers--controlnet-canny-sdxl-1.0/snapshots/eb115a19a10d14909256db740ed109532ab1483c")
IP_ADAPTER = Path("/home/cbsim/.cache/huggingface/hub/models--h94--IP-Adapter/snapshots/018e402774aeeddd60609b4ecdb7e298259dc729")
PROMPT = "anime style, adult woman, teal bob, silver hair clip, white jacket, charcoal shirt, teal wide-leg trousers, white sneakers, navy crossbody bag, clean webtoon line art, cinema foyer at night, low side three-quarter full body, left hand picks up ticket"
NEGATIVE = "multiple people, cropped body, cut off feet, extra bag, broken strap, deformed hands, text, watermark"


def canny(image: Image.Image) -> Image.Image:
    array = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(array, 100, 200)
    return Image.fromarray(edges).convert("RGB")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path)
    parser.add_argument("reference_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    rows = [json.loads(line) for line in (args.dataset / "heldout" / "metadata.jsonl").read_text().splitlines()]
    row = next(item for item in rows if item["source_id"] == "mira-heldout-03")
    source = Image.open(args.dataset / "heldout" / row["file_name"]).convert("RGB").resize((512, 768))
    control = canny(source)
    reference = Image.open(args.reference_dir / "p7-5-2-mira-single-reference-01.png").convert("RGB")
    args.output.mkdir(parents=True, exist_ok=True)

    controlnet = ControlNetModel.from_pretrained(CONTROLNET, torch_dtype=torch.float16, variant="fp16")
    pipe = StableDiffusionXLControlNetPipeline.from_pretrained(ANIMAGINE, controlnet=controlnet, torch_dtype=torch.float16, use_safetensors=True)
    pipe.load_ip_adapter(str(IP_ADAPTER), subfolder="sdxl_models", weight_name="ip-adapter_sdxl.safetensors", image_encoder_folder="image_encoder")
    pipe.enable_sequential_cpu_offload()
    pipe.enable_vae_slicing()
    pipe.set_progress_bar_config(disable=True)
    common = dict(prompt=PROMPT, negative_prompt=NEGATIVE, image=control, ip_adapter_image=reference, width=512, height=768, num_inference_steps=15, guidance_scale=7.0)
    seed = 4703
    off = pipe(**common, controlnet_conditioning_scale=0.0, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]
    on = pipe(**common, controlnet_conditioning_scale=0.75, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]

    sheet = Image.new("RGB", (1536, 792), "white")
    draw = ImageDraw.Draw(sheet)
    for x, label, image in ((0, "Canny camera input", control), (512, "Canny off", off), (1024, "Canny on", on)):
        draw.text((x + 6, 5), label, fill="black")
        sheet.paste(image, (x, 24))
    output_path = args.output / "p7-5-4-sdxl-canny-camera-on-off.png"
    sheet.save(output_path)
    record = {
        "status": "generated_for_review",
        "base_model": "cagliostrolab/animagine-xl-4.0 (SDXL)",
        "controlnet": "diffusers/controlnet-canny-sdxl-1.0",
        "identity_adapter": "ip-adapter_sdxl.safetensors",
        "input": row["file_name"],
        "control_scales": [0.0, 0.75],
        "size": [512, 768],
        "steps": 15,
        "seed": seed,
        "result": output_path.name,
    }
    (args.output / "p7-5-4-sdxl-canny-camera-on-off.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

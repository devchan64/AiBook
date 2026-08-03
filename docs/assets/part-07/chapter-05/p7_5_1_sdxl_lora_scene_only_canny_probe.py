#!/usr/bin/env python3
"""Test scene-only Canny so character edges cannot override an identity LoRA."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import numpy as np
import torch
from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline
from PIL import Image, ImageDraw


PROMPT = (
    "p7mira, woman, teal bob, silver clip, white jacket, teal trousers, white sneakers, "
    "navy flap bag, diagonal strap, webtoon line art, cinema foyer at night, "
    "low side three-quarter full body, left hand picks up ticket"
)
NEGATIVE = "multiple people, cropped body, cut off feet, extra bag, broken strap, deformed hands, text, watermark, photorealistic"


def canny(image: Image.Image) -> Image.Image:
    gray = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    return Image.fromarray(cv2.Canny(gray, 100, 200)).convert("RGB")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("adapter", type=Path)
    parser.add_argument("controlnet", type=Path)
    parser.add_argument("heldout", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=768)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--guidance", type=float, default=7.0)
    parser.add_argument("--lora-scale", type=float, default=1.0)
    parser.add_argument("--control-scales", type=float, nargs="+", default=(0.0, 0.35, 0.75))
    parser.add_argument("--foreground-box", type=int, nargs=4, default=(110, 175, 430, 750))
    parser.add_argument("--seed", type=int, default=5203)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    if args.control_scales[0] != 0.0:
        raise ValueError("the first control scale must be 0.0 for the fixed baseline")

    source = Image.open(args.heldout).convert("RGB").resize((args.width, args.height))
    original_canny = canny(source)
    control = original_canny.copy()
    left, top, right, bottom = args.foreground_box
    ImageDraw.Draw(control).rectangle((left, top, right, bottom), fill="black")
    args.output.mkdir(parents=True, exist_ok=True)
    controlnet = ControlNetModel.from_pretrained(args.controlnet, torch_dtype=torch.float16, variant="fp16")
    pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
        args.model, controlnet=controlnet, torch_dtype=torch.float16, use_safetensors=True
    )
    pipe.load_lora_weights(args.adapter, weight_name="pytorch_lora_weights.safetensors", adapter_name="p7mira")
    pipe.set_adapters("p7mira", adapter_weights=args.lora_scale)
    pipe.enable_sequential_cpu_offload()
    pipe.vae.enable_slicing()
    pipe.set_progress_bar_config(disable=True)
    common = dict(
        prompt=PROMPT,
        negative_prompt=NEGATIVE,
        image=control,
        width=args.width,
        height=args.height,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance,
    )
    generated: list[tuple[float, Image.Image]] = []
    for scale in args.control_scales:
        image = pipe(
            **common,
            controlnet_conditioning_scale=scale,
            generator=torch.Generator(device="cuda").manual_seed(args.seed),
        ).images[0]
        generated.append((scale, image))
    sheet = Image.new("RGB", (args.width * (2 + len(generated)), args.height + 24), "white")
    draw = ImageDraw.Draw(sheet)
    panels = (("Original Canny", original_canny), ("Scene-only Canny", control), *[(f"Scene-only {scale:.2f} + LoRA", image) for scale, image in generated])
    for index, (label, image) in enumerate(panels):
        left = index * args.width
        draw.text((left + 6, 5), label, fill="black")
        sheet.paste(image, (left, 24))
    sheet_path = args.output / "p7-5-1-sdxl-lora-scene-only-canny-scale-sweep.png"
    sheet.save(sheet_path)
    record = {
        "status": "generated_for_review",
        "base_model": str(args.model),
        "identity_condition": "P7-5.1 SDXL base native-resolution identity-only LoRA",
        "controlnet": str(args.controlnet),
        "heldout": args.heldout.name,
        "foreground_box": list(args.foreground_box),
        "control_scales": list(args.control_scales),
        "lora_scale": args.lora_scale,
        "resolution": [args.width, args.height],
        "steps": args.steps,
        "guidance": args.guidance,
        "seed": args.seed,
        "result": sheet_path.name,
        "quality_status": "review_required",
    }
    (args.output / "p7-5-1-sdxl-lora-scene-only-canny-scale-sweep.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n"
    )
    print(sheet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

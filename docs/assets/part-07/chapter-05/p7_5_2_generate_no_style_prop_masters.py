#!/usr/bin/env python3
"""Generate prompt-only replacement candidates for Mira's prop masters."""

from __future__ import annotations

import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
REPORT = ROOT / "p7-5-2-no-style-prop-master-review.json"
PROPS = [
    {
        "id": "jacket",
        "output": "p7-5-2-no-style-prop-jacket-candidate.png",
        "size": (768, 1024),
        "prompt": "One isolated white cropped utility jacket in a clean front view on a plain off-white background. Wide collar, two flap chest pockets, simple front buttons, long sleeves with cuffs, clean seams, and a cropped hem. Clean product illustration. No person, hanger, text, logo, or other object.",
    },
    {
        "id": "trousers",
        "output": "p7-5-2-no-style-prop-trousers-candidate.png",
        "size": (768, 1024),
        "prompt": "One isolated pair of deep saturated petrol-blue-teal high-waisted wide-leg trousers in a clean front view on a plain off-white background. Belt loops, center fly, crisp vertical seams, straight wide legs, and hems above the shoe collar. Clean product illustration. No person, hanger, text, logo, or other object.",
    },
    {
        "id": "shoes",
        "output": "p7-5-2-no-style-prop-shoes-candidate.png",
        "size": (768, 768),
        "prompt": "One matching pair of plain white low-top lace-up sneakers, arranged in a clean three-quarter product view on a plain off-white background. Rounded toe caps, white laces, white rubber soles, and minimal stitching. Clean product illustration. No person, text, logo, or other object.",
    },
    {
        "id": "crossbody_bag",
        "output": "p7-5-2-no-style-prop-crossbody-bag-candidate.png",
        "size": (768, 768),
        "prompt": "One isolated compact deep-navy woven-canvas crossbody bag in a clean three-quarter front view on a plain off-white background. Small horizontal rounded flap, visible textile weave, stitched seams, reinforced strap tabs, charcoal adjustable canvas strap, and one small silver clasp. Clean product illustration. No leather, person, text, logo, or other object.",
    },
]


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    runs = []
    for index, prop in enumerate(PROPS):
        started = time.monotonic()
        width, height = prop["size"]
        image = pipe(
            prompt=prop["prompt"],
            width=width,
            height=height,
            num_inference_steps=12,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(62280 + index),
            max_sequence_length=256,
        ).images[0]
        output = ROOT / prop["output"]
        image.save(output)
        elapsed = round(time.monotonic() - started, 2)
        runs.append({"id": prop["id"], "output": output.name, "prompt": prop["prompt"], "elapsed_seconds": elapsed})
        print(f"{prop['id']}: {elapsed:.2f}s -> {output}")

    REPORT.write_text(
        json.dumps(
            {
                "status": "review_required",
                "purpose": "Generate replacement prop-master candidates without a style-image or style prompt input.",
                "input_policy": "prompt only; no style, face, character, or existing prop image input",
                "model": {"id": MODEL_ID, "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload"},
                "runs": runs,
                "decision": "Pending human review; no candidate replaces the approved prop master until individually approved."
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

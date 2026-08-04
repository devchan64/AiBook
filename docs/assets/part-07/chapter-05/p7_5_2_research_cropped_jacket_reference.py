#!/usr/bin/env python3
"""Generate a shorter cropped-jacket prop candidate for Mira's reference pack."""

from __future__ import annotations

import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
OUTPUT = ROOT / "p7-5-2-prop-reference-v3-cropped-jacket-candidate.png"
REPORT = ROOT / "p7-5-2-prop-reference-v3-cropped-jacket-candidate.json"
PROMPT = """One isolated white cropped utility jacket in a clean front product view on a plain off-white background. Its short straight body ends at the natural waist: the hem sits immediately below the pocket bottoms, with no lower torso extension. Wide collar, two flap chest pockets, simple front buttons, long sleeves with cuffs, a narrow hem band, and clean seams. Clean product illustration. No person, hanger, text, logo, or other object."""


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    started = time.monotonic()
    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    image = pipe(
        prompt=PROMPT,
        width=768,
        height=1024,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62310),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    REPORT.write_text(
        json.dumps(
            {
                "status": "review_required",
                "purpose": "Replace the jacket prop reference with a visibly shorter natural-waist cropped cut.",
                "input_policy": "prompt only; no style, face, character, or existing prop image input",
                "model": {"id": MODEL_ID, "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload"},
                "output": OUTPUT.name,
                "prompt": PROMPT,
                "elapsed_seconds": round(time.monotonic() - started, 2),
                "decision": "Pending human review; this does not replace the approved jacket reference until approved.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

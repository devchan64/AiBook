#!/usr/bin/env python3
"""Generate a front full-body candidate from the approved face and prop references."""

from __future__ import annotations

import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
REFERENCES = [
    ROOT / "p7-5-2-face-front-v2.png",
    ROOT / "p7-5-2-prop-reference-v2-jacket.png",
    ROOT / "p7-5-2-prop-reference-v2-trousers.png",
    ROOT / "p7-5-2-prop-reference-v2-shoes.png",
    ROOT / "p7-5-2-prop-reference-v2-crossbody-bag.png",
]
OUTPUT = ROOT / "p7-5-2-fullbody-front-reference-candidate.png"
REPORT = ROOT / "p7-5-2-fullbody-front-reference-review.json"
PROMPT = (
    "Full-body front reference of the same woman on an off-white studio background. "
    "Use the face and four prop references. Neutral standing pose, complete from hair to soles. "
    "No extra person, text, or border."
)
SEED = 62285


def main() -> None:
    if missing := [path.name for path in REFERENCES if not path.is_file()]:
        raise FileNotFoundError(", ".join(missing))
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    started = time.monotonic()
    image = pipe(
        image=[Image.open(path).convert("RGB") for path in REFERENCES],
        prompt=PROMPT,
        width=768,
        height=1280,
        num_inference_steps=12,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(SEED),
        max_sequence_length=256,
    ).images[0]
    image.save(OUTPUT)
    REPORT.write_text(
        json.dumps(
            {
                "status": "review_required",
                "references": [path.name for path in REFERENCES],
                "output": OUTPUT.name,
                "seed": SEED,
                "prompt": PROMPT,
                "model": MODEL_ID,
                "elapsed_seconds": round(time.monotonic() - started, 2),
                "decision": "Candidate only; human review is required before it becomes the front full-body reference.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

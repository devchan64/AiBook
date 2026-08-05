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
    ROOT / "p7-5-2-outfit-crop-top-waist-reference.png",
    ROOT / "p7-5-2-prop-reference-v2-trousers.png",
    ROOT / "p7-5-2-prop-reference-v2-shoes.png",
]
OUTPUT = ROOT / "p7-5-2-fullbody-front-reference-candidate.png"
REPORT = ROOT / "p7-5-2-fullbody-front-candidate-review.json"
PROMPT = (
    "Full-body strict front reference of the same woman on an off-white studio background, complete from hair to soles in a neutral upright standing pose. "
    "Use the frontal face reference for identity and its clean ink outlines, watercolor fills, and flat illustrated rendering. "
    "She is 165 cm tall, weighs 55 kg, and has approximately 7.5 head heights. "
    "Use the approved outfit relationship reference for a charcoal-gray regular-fit short-sleeve micro-crop crew-neck top, with its hem high across the upper abdomen and a clear bare midriff above the trousers. "
    "Use the approved clothing references for deep teal-blue high-waisted wide-leg trousers and a matching pair of plain white lace-up low-top sneakers."
)
SEED = 62285


def prompt_word_count(text: str) -> int:
    return len(text.split())


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
                "prompt_word_count": prompt_word_count(PROMPT),
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

#!/usr/bin/env python3
"""Generate head-and-neck rotation candidates from one approved frontal face."""

from __future__ import annotations

import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
FRONT = ROOT / "p7-5-2-face-front-v2.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
REPORT = ROOT / "p7-5-2-face-rotation-from-front-v2-review.json"
BASE_PROMPT = (
    "Head-and-neck reference portrait of the same adult Korean webtoon woman on an off-white background. "
    "Frame from the top of her deep teal jaw-length bob to the base of her neck, with no shoulders. "
    "Use the single frontal face reference for her warm light-peach skin, chestnut-and-amber eyes, "
    "and side-parted jaw-length bob. "
)
VIEWS = [
    ("left_front_quarter", "left-front-quarter", 62350,
     "Turn her head 50 degrees toward viewer-left; nose, lips, and chin point left, and the far eye is narrower."),
    ("right_front_quarter", "right-front-quarter", 62351,
     "Turn her head 50 degrees toward viewer-right; nose, lips, and chin point right, and the far eye is narrower."),
    ("profile_left", "profile-left", 62352,
     "Face viewer-left in strict profile with one visible eye, one ear, and a clear left-facing nose, lips, and chin."),
    ("profile_right", "profile-right", 62353,
     "Face viewer-right in strict profile with one visible eye, one ear, and a clear right-facing nose, lips, and chin."),
    ("rear_hair", "rear-hair", 62354,
     "Show the back of her head and neck: the bob silhouette, nape, and no visible face."),
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
    face = Image.open(FRONT).convert("RGB")
    runs = []
    for view_id, name, seed, direction in VIEWS:
        started = time.monotonic()
        prompt = f"{BASE_PROMPT}{direction} Calm neutral expression. No accessory, text, or border."
        output = ROOT / f"p7-5-2-face-rotation-v2-{name}-candidate.png"
        image = pipe(
            image=[face],
            prompt=prompt,
            width=768,
            height=768,
            num_inference_steps=12,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(seed),
            max_sequence_length=256,
        ).images[0]
        image.save(output)
        runs.append({
            "view_id": view_id,
            "output": output.name,
            "seed": seed,
            "prompt": prompt,
            "elapsed_seconds": round(time.monotonic() - started, 2),
        })

    REPORT.write_text(
        json.dumps(
            {
                "status": "review_required",
                "purpose": "Create compact-prompt directional face candidates from the approved frontal-face reference.",
                "input": FRONT.name,
                "model": MODEL_ID,
                "runs": runs,
                "decision": "Review each view before replacing a directional reference.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

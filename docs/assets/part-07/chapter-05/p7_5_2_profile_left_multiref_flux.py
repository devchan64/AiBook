"""Generate a Canny-free left-profile candidate from character and style references."""

from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
CHARACTER = ROOT / "p7-5-2-multireference-turnaround-v1-front.png"
STYLE = ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png"
OUT = Path("/tmp/p7-5-2-profile-left-no-canny")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    flux = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B", torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache"
    )
    flux.enable_sequential_cpu_offload()
    flux.set_progress_bar_config(disable=True)
    started = time.monotonic()
    image = flux(
        image=[Image.open(CHARACTER).convert("RGB"), Image.open(STYLE).convert("RGB")],
        prompt=(
            "Create exactly one original full-body Korean webtoon character illustration. Reference 1 defines the same woman: teal bob, silver hair clip, "
            "white cropped utility jacket, charcoal shirt, teal wide-leg trousers, and white sneakers. "
            "Reference 2 defines thin charcoal contours and transparent pale-blue muted-teal watercolor washes. "
            "Use a neutral standing pose with arms relaxed at the sides, two coherent legs, and both feet planted. "
            "Make a strict left side profile: nose, eyes, chin, gaze, shoulders, torso, hips, knees, and toes all face image-left. Show the complete body from head to soles. "
            "No bag, no strap, no front-facing face or torso, no three-quarter turn, no extra limbs, crop, text, watermark, frame, or photorealism."
        ),
        width=768,
        height=1152,
        num_inference_steps=8,
        guidance_scale=1.0,
        generator=torch.Generator(device="cpu").manual_seed(62021),
        max_sequence_length=256,
    ).images[0]
    image.save(OUT / "profile-left-flux-candidate.png")
    print(f"seconds={time.monotonic() - started:.2f}")
    print(OUT)


if __name__ == "__main__":
    main()

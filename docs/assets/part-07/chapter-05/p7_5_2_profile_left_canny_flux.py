"""Temporary left-profile Canny layout plus FLUX multi-reference candidate."""

from pathlib import Path
import time

import cv2
import numpy as np
import torch
from diffusers import Flux2KleinPipeline, StableDiffusionPipeline, UniPCMultistepScheduler
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
SD15 = Path("/home/cbsim/.cache/huggingface/hub/models--stable-diffusion-v1-5--stable-diffusion-v1-5/snapshots/451f4fe16113bff5a5d2269ed5ad43b0592e9a14")
CHARACTER = ROOT / "p7-5-2-multireference-turnaround-v1-front.png"
STYLE = ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png"
OUT = Path("/tmp/p7-5-2-profile-left-canny")


def foreground_canny(image: Image.Image) -> Image.Image:
    rgb = np.asarray(image)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    mask = np.zeros(rgb.shape[:2], np.uint8)
    bg = np.zeros((1, 65), np.float64)
    fg = np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, mask, (32, 20, rgb.shape[1] - 64, rgb.shape[0] - 40), bg, fg, 5, cv2.GC_INIT_WITH_RECT)
    foreground = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    contours, _ = cv2.findContours(foreground, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        touches = x <= 1 or y <= 1 or x + w >= rgb.shape[1] - 1 or y + h >= rgb.shape[0] - 1
        if not touches and cv2.contourArea(contour) >= rgb.shape[0] * rgb.shape[1] * 0.03:
            candidates.append((cv2.contourArea(contour), contour))
    if not candidates:
        raise RuntimeError("could not isolate one full-body profile figure")
    _, person = max(candidates, key=lambda row: row[0])
    person_mask = np.zeros(rgb.shape[:2], np.uint8)
    cv2.drawContours(person_mask, [person], -1, 255, thickness=cv2.FILLED)
    edges = cv2.Canny(cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY), 90, 190)
    edges = cv2.dilate(cv2.bitwise_and(edges, person_mask), np.ones((2, 2), np.uint8), iterations=1)
    cv2.drawContours(edges, [person], -1, 255, 2)
    return Image.fromarray(edges).convert("RGB")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    draft_pipe = StableDiffusionPipeline.from_pretrained(SD15, torch_dtype=torch.float16, safety_checker=None, requires_safety_checker=False).to("cuda")
    draft_pipe.scheduler = UniPCMultistepScheduler.from_config(draft_pipe.scheduler.config)
    draft_pipe.enable_attention_slicing()
    draft_pipe.set_progress_bar_config(disable=True)
    draft = draft_pipe(
        prompt=(
            "one adult woman, strict full-body left side profile, head to shoe soles visible, neutral planted standing, arms at sides, "
            "nose chin gaze shoulders torso hips knees and toes all point image-left, simple jacket trousers sneakers, blank studio background"
        ),
        negative_prompt="front view, three-quarter view, multiple people, crop, cut feet, extra limbs, duplicate body, text, watermark, frame",
        width=512,
        height=768,
        num_inference_steps=28,
        guidance_scale=7.0,
        generator=torch.Generator(device="cuda").manual_seed(62021),
    ).images[0]
    draft.save(OUT / "profile-left-draft.png")
    canny = foreground_canny(draft)
    canny.save(OUT / "profile-left-canny.png")
    del draft_pipe
    torch.cuda.empty_cache()

    flux = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B", torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache"
    )
    flux.enable_sequential_cpu_offload()
    flux.set_progress_bar_config(disable=True)
    started = time.monotonic()
    image = flux(
        image=[Image.open(CHARACTER).convert("RGB"), Image.open(STYLE).convert("RGB"), canny],
        prompt=(
            "Create exactly one original full-body Korean webtoon character illustration. Reference 1 defines the same woman: teal bob, silver hair clip, "
            "white cropped utility jacket, charcoal shirt, teal wide-leg trousers, and white sneakers. "
            "Reference 2 defines thin charcoal contours and transparent pale-blue muted-teal watercolor washes. "
            "Reference 3 is Canny layout only: follow its one-person full-body silhouette, arm placement, legs, and planted feet; do not copy black background or edge marks. "
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

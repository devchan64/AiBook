#!/usr/bin/env python3
"""Run the first 8 GB DiffEdit probe without adding a control or identity model.

The approved P7-5.2 front turnaround is a fixed probe input, not a P7-5.3
production cut. Change --steps or --mask-maps to inspect their effect on the
automatic mask, GPU peak, elapsed time, and changes outside the intended area.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import threading
import time
from pathlib import Path

import numpy as np
import torch
from diffusers import DDIMInverseScheduler, DDIMScheduler, StableDiffusionDiffEditPipeline, StableDiffusionPipeline
from PIL import Image, ImageDraw


ROOT = Path("/home/cbsim/ws/AiBook")
BASE_MODEL = Path(
    "/home/cbsim/.cache/huggingface/hub/models--stable-diffusion-v1-5--stable-diffusion-v1-5/"
    "snapshots/451f4fe16113bff5a5d2269ed5ad43b0592e9a14/v1-5-pruned-emaonly.safetensors"
)
SOURCE_IMAGE = ROOT / "docs/assets/part-07/chapter-05/p7-5-2-fullbody-front-reference.png"
SOURCE_PROMPT = (
    "one adult woman with a teal bob haircut, dark gray crop top, teal wide-leg trousers, white sneakers, "
    "standing front-facing in a plain studio"
)
TARGET_PROMPT = (
    "one adult woman with a teal bob haircut, cropped white jacket worn open over a dark gray crop top, "
    "teal wide-leg trousers, white sneakers, standing front-facing in a plain studio"
)
NEGATIVE_PROMPT = "multiple people, cropped body, cut off feet, extra arms, extra legs, text, watermark"
SEED = 5404
WIDTH = 512
HEIGHT = 768


def gpu_memory_mib() -> int | None:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        return int(result.stdout.splitlines()[0])
    except (IndexError, ValueError):
        return None


def to_mask_image(mask: Image.Image | np.ndarray) -> Image.Image:
    if isinstance(mask, Image.Image):
        return mask.convert("L")
    array = np.asarray(mask)
    if array.ndim == 4:
        array = array[0, 0]
    elif array.ndim == 3:
        array = array[0]
    if array.max() <= 1.0:
        array = array * 255
    return Image.fromarray(np.asarray(array, dtype=np.uint8)).convert("L")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--mask-maps", type=int, default=10)
    parser.add_argument("--mask-encode-strength", type=float, default=0.2)
    parser.add_argument("--mask-thresholding-ratio", type=float, default=8.0)
    parser.add_argument("--source-prompt", default=SOURCE_PROMPT)
    parser.add_argument("--target-prompt", default=TARGET_PROMPT)
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this 8 GB probe")
    if not BASE_MODEL.is_file():
        raise FileNotFoundError(BASE_MODEL)
    if not SOURCE_IMAGE.is_file():
        raise FileNotFoundError(SOURCE_IMAGE)

    args.output.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE_IMAGE).convert("RGB").resize((WIDTH, HEIGHT))
    before = gpu_memory_mib()
    peak = before or 0
    stop = threading.Event()

    def observe_peak() -> None:
        nonlocal peak
        while not stop.is_set():
            observed = gpu_memory_mib()
            if observed is not None:
                peak = max(peak, observed)
            time.sleep(0.2)

    observer = threading.Thread(target=observe_peak, daemon=True)
    observer.start()
    started = time.monotonic()
    try:
        base_pipe = StableDiffusionPipeline.from_single_file(BASE_MODEL, torch_dtype=torch.float16)
        scheduler = DDIMScheduler.from_config(base_pipe.scheduler.config)
        pipe = StableDiffusionDiffEditPipeline(
            vae=base_pipe.vae,
            text_encoder=base_pipe.text_encoder,
            tokenizer=base_pipe.tokenizer,
            unet=base_pipe.unet,
            scheduler=scheduler,
            safety_checker=base_pipe.safety_checker,
            feature_extractor=base_pipe.feature_extractor,
            inverse_scheduler=DDIMInverseScheduler.from_config(scheduler.config),
            requires_safety_checker=False,
        )
        pipe.enable_sequential_cpu_offload()
        pipe.enable_attention_slicing()
        pipe.set_progress_bar_config(disable=True)
        generator = torch.Generator(device="cuda").manual_seed(SEED)
        mask = pipe.generate_mask(
            image=source,
            source_prompt=args.source_prompt,
            target_prompt=args.target_prompt,
            num_maps_per_mask=args.mask_maps,
            mask_encode_strength=args.mask_encode_strength,
            mask_thresholding_ratio=args.mask_thresholding_ratio,
            num_inference_steps=args.steps,
            guidance_scale=7.5,
            generator=generator,
            output_type="np",
        )
        mask_preview = to_mask_image(mask).resize((WIDTH, HEIGHT), Image.Resampling.NEAREST)
        inverted = pipe.invert(
            image=source,
            prompt=args.source_prompt,
            num_inference_steps=args.steps,
            inpaint_strength=0.8,
            guidance_scale=7.5,
            generator=torch.Generator(device="cuda").manual_seed(SEED),
        ).latents
        edited = pipe(
            prompt=args.target_prompt,
            negative_prompt=NEGATIVE_PROMPT,
            mask_image=mask,
            image_latents=inverted,
            inpaint_strength=0.8,
            num_inference_steps=args.steps,
            guidance_scale=7.5,
            generator=torch.Generator(device="cuda").manual_seed(SEED),
        ).images[0]
        source.save(args.output / "source.png")
        mask_preview.save(args.output / "diffedit-mask.png")
        edited.save(args.output / "diffedit-output.png")
        sheet = Image.new("RGB", (WIDTH * 3, HEIGHT + 28), "white")
        labels = (("fixed source", source), ("DiffEdit automatic mask", mask_preview.convert("RGB")), ("DiffEdit output", edited))
        draw = ImageDraw.Draw(sheet)
        for index, (label, image) in enumerate(labels):
            x = index * WIDTH
            draw.text((x + 6, 6), label, fill="black")
            sheet.paste(image, (x, 28))
        sheet.save(args.output / "contact-sheet.png")
    finally:
        stop.set()
        observer.join(timeout=2)

    report = {
        "status": "generated_for_human_review",
        "purpose": "8 GB DiffEdit preflight; fixed P7-5.2 input, not a P7-5.3 production cut",
        "base_model": "stable-diffusion-v1-5/stable-diffusion-v1-5",
        "additional_condition_models": [],
        "source_image": str(SOURCE_IMAGE.relative_to(ROOT)),
        "source_prompt": args.source_prompt,
        "target_prompt": args.target_prompt,
        "resolution": [WIDTH, HEIGHT],
        "steps": args.steps,
        "mask_maps": args.mask_maps,
        "mask_encode_strength": args.mask_encode_strength,
        "mask_thresholding_ratio": args.mask_thresholding_ratio,
        "seed": SEED,
        "gpu_memory_before_mib": before,
        "gpu_memory_peak_mib": peak if peak else None,
        "elapsed_seconds": round(time.monotonic() - started, 1),
        "outputs": ["source.png", "diffedit-mask.png", "diffedit-output.png", "contact-sheet.png"],
        "review_questions": [
            "Does the automatic mask concentrate on the intended jacket area?",
            "Does the output preserve face, trousers, shoes, and the background outside the edit?",
            "Does the output add the requested cropped white jacket without new anatomy or boundary errors?",
        ],
    }
    (args.output / "run.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output / "contact-sheet.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

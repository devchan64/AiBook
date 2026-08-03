"""InvokeAI-free FLUX.2 Klein 4B single-reference preflight using Diffusers."""

import json
import os
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
CACHE_DIR = "/tmp/flux2-klein-diffusers-cache"
REFERENCE = Path(
    "/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05/"
    "p7-5-1-mira-single-reference-01.png"
)
OUTPUT_DIR = Path("/tmp/p7-5-1-diffusers-flux2-klein")
PROMPT = (
    "Create one polished full-body Korean webtoon panel of the exact same young woman in the reference image. "
    "Keep her teal bob haircut with one silver hair clip, white cropped utility jacket, teal wide-leg trousers, "
    "white sneakers, and the navy rectangular flap shoulder bag at her right hip with exactly one diagonal navy strap. "
    "She stands naturally at a quiet cinema ticket counter, holding one ticket in her left hand and looking at it. "
    "Show her complete body from head to shoes with correct human anatomy, expressive face, detailed hands, "
    "clean Korean webtoon line art, soft flat colors, and a readable cinema lobby background."
)


def gpu_memory_mib() -> int:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        check=False,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.splitlines()[0])


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    before = gpu_memory_mib()
    peak = before
    stop = threading.Event()

    def observe_peak() -> None:
        nonlocal peak
        while not stop.is_set():
            peak = max(peak, gpu_memory_mib())
            time.sleep(0.2)

    observer = threading.Thread(target=observe_peak, daemon=True)
    observer.start()
    started = time.monotonic()
    try:
        pipe = Flux2KleinPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.bfloat16,
            cache_dir=CACHE_DIR,
        )
        pipe.enable_sequential_cpu_offload()
        prompt = os.environ.get("PROMPT_OVERRIDE", PROMPT)
        image = pipe(
            image=Image.open(REFERENCE).convert("RGB"),
            prompt=prompt,
            width=512,
            height=768,
            num_inference_steps=4,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(320241),
            max_sequence_length=256,
        ).images[0]
        output = OUTPUT_DIR / os.environ.get(
            "OUTPUT_NAME", "p7-5-1-diffusers-flux2-klein-reference-preflight.png"
        )
        image.save(output)
        report = {
            "runtime": "diffusers-0.37.0",
            "model_id": MODEL_ID,
            "status": "completed",
            "elapsed_seconds": round(time.monotonic() - started, 1),
            "gpu_memory_before_mib": before,
            "gpu_memory_peak_mib": peak,
            "reference_image": str(REFERENCE),
            "output_image": str(output),
            "prompt": prompt,
        }
        report_name = os.environ.get("REPORT_NAME", "run.json")
        (OUTPUT_DIR / report_name).write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

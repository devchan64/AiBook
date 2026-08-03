"""Create a mirror-safe local character-and-style master without asymmetric details."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-local-mirror-safe-master")
PROMPT = (
    "Create exactly one original full-body adult Korean webtoon character reference illustration. "
    "A young woman stands naturally in a relaxed front three-quarter view, completely visible from the top of her head to both shoe soles. "
    "She has a symmetric deep teal-blue jaw-length bob haircut with a soft center part and no hair clips, jewelry, or asymmetric ornament, "
    "warm light skin, dark brown almond-shaped eyes, a white cropped utility jacket with matching left and right chest pockets over a charcoal crew-neck shirt, "
    "teal high-waisted wide-leg trousers, and plain white sneakers. She wears no bag, no backpack, no purse, no belt pouch, and holds no object. "
    "Clean contemporary Korean webtoon line art, thin charcoal outlines, low-saturation flat colors, subtle fold shadows, white studio background, "
    "no text, no logos, no watermark, no panels, anatomically correct hands and feet. Do not add another person, accessories, duplicate limbs, cropped body parts, "
    "thick comic outlines, screentones, or painterly texture."
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
        pipe = Flux2KleinPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR)
        pipe.enable_sequential_cpu_offload()
        image = pipe(
            prompt=PROMPT,
            width=768,
            height=1152,
            num_inference_steps=50,
            guidance_scale=4.0,
            generator=torch.Generator(device="cpu").manual_seed(410201),
            max_sequence_length=256,
        ).images[0]
        output = OUTPUT_DIR / "master.png"
        image.save(output)
        (OUTPUT_DIR / "run.json").write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "model_id": MODEL_ID,
                    "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload",
                    "purpose": "local text-to-image mirror-safe character-and-style master",
                    "prompt": PROMPT,
                    "size": [768, 1152],
                    "steps": 50,
                    "guidance_scale": 4.0,
                    "seed": 410201,
                    "elapsed_seconds": round(time.monotonic() - started, 1),
                    "gpu_memory_before_mib": before,
                    "gpu_memory_peak_mib": peak,
                    "output_image": str(output),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

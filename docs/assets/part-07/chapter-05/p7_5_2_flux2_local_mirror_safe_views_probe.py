"""Generate the non-mirrored views required for a mirror-safe local character pack."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image, ImageDraw


MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
CACHE_DIR = Path("/tmp/flux2-klein-diffusers-cache")
MASTER = Path("/tmp/p7-5-2-local-mirror-safe-master/master.png")
OUTPUT_DIR = Path("/tmp/p7-5-2-local-mirror-safe-views")
CONTRACT = (
    "Keep the exact same adult Korean woman in the reference: symmetric deep teal-blue jaw-length bob with a soft center part and no hair clips or asymmetric ornament, "
    "warm light skin, dark brown almond-shaped eyes, white cropped utility jacket with matching left and right chest pockets over a charcoal crew-neck shirt, "
    "teal high-waisted wide-leg trousers, and plain white sneakers. She wears no bag, no backpack, no purse, no belt pouch, no jewelry, and holds no object. "
    "Show the complete body from head to both shoe soles. Clean contemporary Korean webtoon line art, thin charcoal outlines, low-saturation flat colors, subtle fold shadows, "
    "white studio background, no text, no logos, no watermark, no panels."
)
CASES = [
    ("left-profile", "Show a genuine left-side profile standing view, not a front-facing pose.", 410211),
    ("rear-three-quarter", "Show a genuine rear three-quarter standing view, with the head turned slightly so one eye edge is visible.", 410212),
]


def gpu_memory_mib() -> int:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        check=False,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.splitlines()[0])


def main() -> None:
    if not MASTER.is_file():
        raise FileNotFoundError(MASTER)
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
        images = []
        results = []
        for case_id, view_prompt, seed in CASES:
            case_started = time.monotonic()
            prompt = f"Create one polished full-body character reference illustration. {view_prompt} {CONTRACT}"
            image = pipe(
                image=Image.open(MASTER).convert("RGB"),
                prompt=prompt,
                width=768,
                height=1152,
                num_inference_steps=4,
                guidance_scale=1.0,
                generator=torch.Generator(device="cpu").manual_seed(seed),
                max_sequence_length=256,
            ).images[0]
            output = OUTPUT_DIR / f"{case_id}.png"
            image.save(output)
            images.append((case_id, image))
            results.append({"case_id": case_id, "prompt": prompt, "output_image": str(output), "elapsed_seconds": round(time.monotonic() - case_started, 1)})
        sheet = Image.new("RGB", (1536, 1176), "white")
        draw = ImageDraw.Draw(sheet)
        for index, (case_id, image) in enumerate(images):
            x = index * 768
            draw.text((x + 8, 6), case_id, fill="black")
            sheet.paste(image, (x, 24))
        sheet.save(OUTPUT_DIR / "contact-sheet.png")
        (OUTPUT_DIR / "run.json").write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "model_id": MODEL_ID,
                    "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload",
                    "purpose": "profile and rear source views for a mirror-safe local character-and-style pack",
                    "master_image": str(MASTER),
                    "size": [768, 1152],
                    "steps": 4,
                    "guidance_scale": 1.0,
                    "elapsed_seconds": round(time.monotonic() - started, 1),
                    "gpu_memory_before_mib": before,
                    "gpu_memory_peak_mib": peak,
                    "results": results,
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

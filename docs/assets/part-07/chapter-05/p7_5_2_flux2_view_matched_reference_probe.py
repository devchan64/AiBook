"""Compare front and angle-matched references for one FLUX.2 Klein side-view cut."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image, ImageDraw


ROOT = Path("/home/cbsim/ws/AiBook")
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
CACHE_DIR = Path("/tmp/flux2-klein-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-2-flux2-view-matched-reference")
CASES = [
    ("front_reference", ROOT / "docs/assets/part-07/chapter-05/p7-5-2-mira-single-reference-01.png"),
    ("side_reference", ROOT / "docs/assets/part-07/chapter-05/p7-5-2-mira-single-reference-14-side-walk-pause.png"),
]
PROMPT = (
    "Create one polished full-body Korean webtoon panel of the exact same young woman in the reference image. "
    "Show a real left-side profile as she walks through a quiet cinema lobby, holding one plain ticket in her left hand. "
    "Keep her teal bob haircut and silver hair clip, white cropped utility jacket, charcoal shirt, teal wide-leg trousers, "
    "white sneakers, and exactly one navy horizontal flap shoulder bag at her right hip with one diagonal strap. "
    "Show her complete body and both shoes with natural anatomy, clean restrained webtoon line art, soft flat colors, and a readable lobby background."
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
    for _, reference in CASES:
        if not reference.is_file():
            raise FileNotFoundError(reference)
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
        images: list[tuple[str, Image.Image]] = []
        rows = []
        for index, (case_id, reference) in enumerate(CASES):
            case_started = time.monotonic()
            image = pipe(
                image=Image.open(reference).convert("RGB"),
                prompt=PROMPT,
                width=512,
                height=768,
                num_inference_steps=4,
                guidance_scale=1.0,
                generator=torch.Generator(device="cpu").manual_seed(320301),
                max_sequence_length=256,
            ).images[0]
            output = OUTPUT_DIR / f"{case_id}.png"
            image.save(output)
            images.append((case_id, image))
            rows.append({"case_id": case_id, "reference_image": str(reference), "output_image": str(output), "elapsed_seconds": round(time.monotonic() - case_started, 1)})
        sheet = Image.new("RGB", (1024, 792), "white")
        draw = ImageDraw.Draw(sheet)
        for index, (case_id, image) in enumerate(images):
            x = index * 512
            draw.text((x + 6, 5), case_id, fill="black")
            sheet.paste(image, (x, 24))
        sheet.save(OUTPUT_DIR / "contact-sheet.png")
        (OUTPUT_DIR / "run.json").write_text(json.dumps({
            "status": "review_required", "model_id": MODEL_ID, "runtime": "diffusers Flux2KleinPipeline sequential CPU offload",
            "purpose": "single variable comparison: front versus angle-matched reference on one side-view whole-shot contract",
            "prompt": PROMPT, "size": [512, 768], "steps": 4, "guidance_scale": 1.0, "seed": 320301,
            "elapsed_seconds": round(time.monotonic() - started, 1), "gpu_memory_before_mib": before, "gpu_memory_peak_mib": peak,
            "results": rows, "contact_sheet": "contact-sheet.png"
        }, indent=2), encoding="utf-8")
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

"""Compare character-only and style-plus-character references for one local cut scene."""

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
STYLE = ROOT / "docs/assets/part-07/chapter-05/p7-5-1-local-style-pack-v1-station-master.png"
CHARACTER = ROOT / "docs/assets/part-07/chapter-05/p7-5-1-local-style-conditioned-character-pack-v1-master.png"
OUTPUT_DIR = Path("/tmp/p7-5-1-style-character-cutscene-ablation")
PROMPT = (
    "Create one polished vertical Korean webtoon scene of the exact same adult Korean woman in the character reference, rendered in the visual style of the style reference. "
    "Show her complete body from the top of her head to both shoe soles, walking naturally from left to right in a quiet rainy residential lane with wet pavement, steps, trees, and softly blurred apartment facades. "
    "Use a medium-long camera view at eye level with a three-quarter side composition. Her gaze follows the walking direction. Keep her symmetric deep teal-blue jaw-length bob, warm light skin, dark brown almond-shaped eyes, "
    "white cropped utility jacket with matching left and right chest pockets over a charcoal crew-neck shirt, teal high-waisted wide-leg trousers, and plain white sneakers. "
    "She wears no bag, no backpack, no purse, no belt pouch, no jewelry, and holds no object. Keep thin charcoal outlines, low-saturation teal, warm gray, off-white, and charcoal palette, soft flat color blocks, subtle single-edge shadows, and restrained material detail. "
    "No other person, readable signs, text, logos, watermark, panels, photorealism, painterly texture, screentones, thick comic outlines, gradients, or neon."
)
CASES = [
    ("character-only", [CHARACTER]),
    ("style-plus-character", [STYLE, CHARACTER]),
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
    for _, references in CASES:
        for reference in references:
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
        images = []
        results = []
        for case_id, references in CASES:
            case_started = time.monotonic()
            image = pipe(
                image=[Image.open(reference).convert("RGB") for reference in references],
                prompt=PROMPT,
                width=768,
                height=1152,
                num_inference_steps=4,
                guidance_scale=1.0,
                generator=torch.Generator(device="cpu").manual_seed(420301),
                max_sequence_length=256,
            ).images[0]
            output = OUTPUT_DIR / f"{case_id}.png"
            image.save(output)
            images.append((case_id, image))
            results.append({
                "case_id": case_id,
                "references": [str(reference) for reference in references],
                "output_image": str(output),
                "elapsed_seconds": round(time.monotonic() - case_started, 1),
            })
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
                    "purpose": "single-variable comparison of character-only versus style-plus-character cut-scene conditioning",
                    "prompt": PROMPT,
                    "size": [768, 1152],
                    "steps": 4,
                    "guidance_scale": 1.0,
                    "seed": 420301,
                    "elapsed_seconds": round(time.monotonic() - started, 1),
                    "gpu_memory_before_mib": before,
                    "gpu_memory_peak_mib": peak,
                    "results": results,
                    "contact_sheet": "contact-sheet.png",
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

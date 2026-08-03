"""Generate a frame-free high-angle local watercolor style candidate."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-style-high-angle-probe")
PROMPT = (
    "Create a full-bleed vertical background painting for a Korean webtoon: an empty indoor atrium at dawn viewed from a high camera above the upper landing, looking steeply downward across stair flights, tiled floor, benches, and plants. "
    "The camera is high angle and downward-looking, not eye level, not centered one-point perspective, and not a frontal hallway view. The image fills every edge of the canvas. "
    "There is no page border, no black rectangle at the edge, no panel frame, no white margin, no inset illustration, no text, no signs, no people, no animals, and no vehicles. "
    "Use thin charcoal contour and structural perspective lines that remain visible above transparent watercolor washes: pale teal and indigo shadow, muted olive plants, warm apricot dawn light, and warm off-white surfaces. "
    "Use no hatching, no crosshatching, no stippling, no dense ink texture, no monochrome ink wash, no sumi-e, no calligraphy, no photorealism, no opaque airbrush, no screentones, no thick comic outlines, and no neon."
)


def gpu_memory_mib() -> int:
    result = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], check=False, capture_output=True, text=True)
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
        image = pipe(prompt=PROMPT, width=768, height=1152, num_inference_steps=50, guidance_scale=4.0, generator=torch.Generator(device="cpu").manual_seed(420601), max_sequence_length=256).images[0]
        output = OUTPUT_DIR / "high-angle.png"
        image.save(output)
        (OUTPUT_DIR / "run.json").write_text(json.dumps({"status": "review_required", "model_id": MODEL_ID, "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload", "purpose": "first frame-free, non-eye-level style-pack camera candidate", "prompt": PROMPT, "size": [768, 1152], "steps": 50, "guidance_scale": 4.0, "seed": 420601, "elapsed_seconds": round(time.monotonic() - started, 1), "gpu_memory_before_mib": before, "gpu_memory_peak_mib": peak, "output_image": str(output)}, indent=2), encoding="utf-8")
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

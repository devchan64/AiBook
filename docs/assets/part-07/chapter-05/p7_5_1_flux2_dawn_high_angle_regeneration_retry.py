"""Retry the dawn high-angle row with a composition that reaches all edges."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-dawn-high-angle-regeneration-retry")
PROMPT = (
    "Create a full-bleed vertical Korean webtoon background of an empty indoor atrium at early dawn, viewed almost straight downward from directly above an upper landing. "
    "Pale tiled floor, a diagonal stair flight, one bench, and a few planters continue naturally past all four image edges so there is no centered picture, border, page, panel, or blank margin. "
    "The camera is a genuine high-angle downward view, never eye level, frontal, or a hallway. Use cool off-white surfaces, subdued teal shadows, and only a small soft apricot dawn reflection near one window. "
    "Use thin charcoal contour and structure lines over transparent watercolor washes with wet-on-wet bleeding, uneven pigment pooling, and layered translucent edges. No text, signs, logos, people, animals, vehicles, black rectangle, hatching, crosshatching, stippling, dense ink texture, opaque paint, airbrush, neon, or sunset sky."
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
        image = pipe(prompt=PROMPT, width=768, height=1152, num_inference_steps=50, guidance_scale=3.5, generator=torch.Generator(device="cpu").manual_seed(420648), max_sequence_length=256).images[0]
        output = OUTPUT_DIR / "dawn-high-angle-medium-chroma.png"
        image.save(output)
        (OUTPUT_DIR / "run.json").write_text(json.dumps({"status": "review_required", "model_id": MODEL_ID, "scene_id": "indoor-dawn-high-angle-medium-chroma-retry", "seed": 420648, "size": [768, 1152], "steps": 50, "guidance_scale": 3.5, "elapsed_seconds": round(time.monotonic() - started, 1), "gpu_memory_before_mib": before, "gpu_memory_peak_mib": peak, "output_image": str(output)}, indent=2), encoding="utf-8")
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

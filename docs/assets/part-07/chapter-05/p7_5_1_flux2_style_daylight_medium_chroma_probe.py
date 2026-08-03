"""Generate a frame-free daylight sample with restrained color emphasis."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-style-daylight-medium-chroma")
PROMPT = (
    "Create a full-bleed vertical Korean webtoon background of an empty city park beside a clear daytime pond, viewed obliquely from a low stone path. "
    "A pale cool blue sky, medium teal water reflections, leaf-green trees, cool off-white paving, and a few muted blue-gray shadows establish clear midday. "
    "The path and pond recede diagonally rather than as a centered corridor. There are no buildings, shops, signs, letters, logos, people, animals, or vehicles. "
    "The scene reaches all four canvas edges: no page border, black rectangle, panel frame, white margin, or inset illustration. "
    "Use sparse thin charcoal contour and structure lines over transparent watercolor washes. Keep color naturally medium-chroma with wet-on-wet bleeding, uneven pigment pooling, and layered translucent edges. "
    "Never use apricot, vermilion, red, orange, pink, golden light, or sunset colors. Do not use neon, opaque paint, airbrush, flat digital fills, hatching, crosshatching, stippling, dense ink texture, ink wash, sumi-e, photorealism, screentones, or thick comic outlines."
)


def gpu_memory_mib() -> int:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], check=False, capture_output=True, text=True
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
            guidance_scale=3.5,
            generator=torch.Generator(device="cpu").manual_seed(420641),
            max_sequence_length=256,
        ).images[0]
        output = OUTPUT_DIR / "daylight-park-medium-chroma.png"
        image.save(output)
        (OUTPUT_DIR / "run.json").write_text(json.dumps({"status": "review_required", "model_id": MODEL_ID, "scene_id": "daylight-park-medium-chroma", "seed": 420641, "size": [768, 1152], "steps": 50, "guidance_scale": 3.5, "elapsed_seconds": round(time.monotonic() - started, 1), "gpu_memory_before_mib": before, "gpu_memory_peak_mib": peak, "output_image": str(output)}, indent=2), encoding="utf-8")
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

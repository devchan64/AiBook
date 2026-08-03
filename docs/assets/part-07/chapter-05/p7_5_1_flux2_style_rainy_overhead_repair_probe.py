"""Retry the rainy-night overhead matrix row with an exterior composition."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-style-rainy-overhead-repair")
PROMPT = (
    "Create a full-bleed vertical watercolor background of an empty Seoul rooftop plaza immediately after rainfall at night. "
    "View steeply downward from a high building terrace across broad wet paving, two large planters, a shallow puddle, and small pools of warm lamp reflection. "
    "The nearest roof edge enters from one side and the plaza recedes diagonally, never as a centered corridor. "
    "No falling rain streaks, no rails, no signs, and no people. The rain is visible only through wet surfaces and reflections under a deep indigo-black night sky. "
    "The painted scene reaches every canvas edge with no page border, black rectangle, panel frame, white margin, or inset illustration. "
    "Use sparse thin charcoal contour and structure lines over broad transparent watercolor washes in pale teal, muted olive, warm apricot, soft indigo, and warm off-white. "
    "Do not use text, logos, hatching, crosshatching, stippling, parallel shading lines, dense ink texture, ink wash, sumi-e, photorealism, airbrush, screentones, thick comic outlines, or neon."
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
            MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR
        )
        pipe.enable_sequential_cpu_offload()
        image = pipe(
            prompt=PROMPT,
            width=768,
            height=1152,
            num_inference_steps=50,
            guidance_scale=4.0,
            generator=torch.Generator(device="cpu").manual_seed(420631),
            max_sequence_length=256,
        ).images[0]
        output = OUTPUT_DIR / "seoul-rainy-night-overhead-repair.png"
        image.save(output)
        (OUTPUT_DIR / "run.json").write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "model_id": MODEL_ID,
                    "scene_id": "seoul-rainy-night-overhead-repair",
                    "seed": 420631,
                    "size": [768, 1152],
                    "steps": 50,
                    "guidance_scale": 4.0,
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

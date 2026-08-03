"""Retry a bright rainy platform with a clear but non-corridor rail cue."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-train-platform-bright-rail-retry")
PROMPT = (
    "Create a vertical Korean webtoon background of an empty commuter train platform just after rain at late night. View diagonally down from a near left canopy corner across wet platform paving. "
    "A bright cool-white canopy corner, two cropped columns, and one blank bench occupy the left. At the lower right, a short clear section of two steel rails and visible sleepers enters diagonally then exits the frame; "
    "it is unmistakably a railway track but not a long centered corridor. The platform edge and rails are side elements, not the central vanishing point. "
    "Cool-white canopy light makes the wet pale-cyan paving clearly visible. Two small warm lamps create only small gold reflections; broken teal and navy puddle reflections remain visible. "
    "The distance is rainy indigo night, not sunrise, daylight, or sunset. No wall, station building, timetable, route map, signboard, poster, train, text, readable symbols, logos, people, animals, or vehicles. "
    "All surfaces continue through the canvas edges as a full-bleed scene: no paper edge, white margin, page border, black edge rectangle, panel frame, or inset illustration. "
    "Use sparse thin charcoal contour and structure lines over transparent watercolor washes with wet-on-wet bleeding, uneven pigment pooling, and layered translucent edges. "
    "Use natural medium-chroma pigment, never neon, fluorescent, opaque, airbrushed, digitally flat, densely hatched, crosshatched, stippled, ink-wash, sumi-e, photorealistic, screentoned, or thick comic outlined."
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
            guidance_scale=3.5,
            generator=torch.Generator(device="cpu").manual_seed(420663),
            max_sequence_length=256,
        ).images[0]
        output = OUTPUT_DIR / "train-platform-rainy-night-bright-rail.png"
        image.save(output)
        (OUTPUT_DIR / "run.json").write_text(json.dumps({"status": "review_required", "model_id": MODEL_ID, "scene_id": "train-platform-rainy-night-bright-rail", "seed": 420663, "size": [768, 1152], "steps": 50, "guidance_scale": 3.5, "elapsed_seconds": round(time.monotonic() - started, 1), "gpu_memory_before_mib": before, "gpu_memory_peak_mib": peak, "output_image": str(output)}, indent=2), encoding="utf-8")
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

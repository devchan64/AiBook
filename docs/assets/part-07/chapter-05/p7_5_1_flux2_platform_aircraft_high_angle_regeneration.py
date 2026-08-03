"""Generate a rail platform and retry aircraft light and high-angle style references."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-platform-aircraft-high-angle-regeneration")
COMMON_CONTRACT = (
    "The scene fills all four canvas edges. No page border, black edge rectangle, panel frame, white margin, inset illustration, "
    "text, readable signs, logos, people, animals, or vehicles. Use sparse thin charcoal contour and structure lines over transparent "
    "watercolor washes with wet-on-wet bleeding, uneven pigment pooling, and layered translucent edges. Use natural medium-chroma pigment, "
    "never neon, fluorescent, opaque, airbrushed, digitally flat, densely hatched, crosshatched, stippled, ink-wash, sumi-e, photorealistic, "
    "screentoned, or thick comic outlined."
)
SCENES = [
    {
        "id": "train-platform-rainy-night-lit",
        "seed": 420657,
        "prompt": "Create a vertical Korean webtoon background of an empty open-air Seoul train platform immediately after rain at late night. View obliquely along the platform under a simple canopy; the platform edge, a few roof columns, blank benches, and only two subtle rail lines recede diagonally. Small warm platform lamps and a few cool-white station lights reflect as broken elongated highlights across the wet dark indigo pavement. Keep navy rain shadows dominant, with restrained teal puddle reflections. No train, no route map, no timetable, no readable sign, and no centered corridor. ",
    },
    {
        "id": "aircraft-night-interior-light-retry",
        "seed": 420658,
        "prompt": "Create a vertical Korean webtoon background inside an empty passenger aircraft at deep night. View diagonally from a rear window seat across an off-center short row of dark-navy seats, oval windows, ceiling panels, and one small portion of aisle. The window sky is indigo-black with faint stars. Add restrained warm tungsten reading lights at several seat and ceiling positions, plus soft cool-white cabin light on the armrests and window frames; these are small pools of light, not a bright cabin. Make navy upholstery, indigo windows, warm reading lights, and cool cabin reflections visibly distinct. This is night, never dusk, dawn, or sunset: no apricot, orange, red, pink, golden sky, labels, symbols, or panels. ",
    },
    {
        "id": "outdoor-courtyard-high-angle-framefree-retry",
        "seed": 420659,
        "prompt": "Create a vertical Korean webtoon background of an empty Seoul residential courtyard in clear early morning, viewed steeply downward from an upper balcony. Diagonal paved paths, a small tree, benches, planters, and low building roofs create varied depth and cross the canvas edges naturally. This is a genuine high-angle downward camera, never eye level, a frontal hallway, or centered one-point perspective. Use cool off-white paving, distinct teal-blue shadows, leaf-green foliage, and a tiny pale apricot reflection on one window only. No orange or red sky, broad warm wash, or sunset effect. ",
    },
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
    runs = []
    try:
        pipe = Flux2KleinPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR)
        pipe.enable_sequential_cpu_offload()
        for scene in SCENES:
            scene_started = time.monotonic()
            image = pipe(
                prompt=scene["prompt"] + COMMON_CONTRACT,
                width=768,
                height=1152,
                num_inference_steps=50,
                guidance_scale=3.5,
                generator=torch.Generator(device="cpu").manual_seed(scene["seed"]),
                max_sequence_length=256,
            ).images[0]
            output = OUTPUT_DIR / f"{scene['id']}.png"
            image.save(output)
            runs.append({"id": scene["id"], "seed": scene["seed"], "elapsed_seconds": round(time.monotonic() - scene_started, 1), "output_image": str(output)})
        (OUTPUT_DIR / "run.json").write_text(json.dumps({"status": "review_required", "model_id": MODEL_ID, "size": [768, 1152], "steps": 50, "guidance_scale": 3.5, "elapsed_seconds": round(time.monotonic() - started, 1), "gpu_memory_before_mib": before, "gpu_memory_peak_mib": peak, "runs": runs}, indent=2), encoding="utf-8")
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

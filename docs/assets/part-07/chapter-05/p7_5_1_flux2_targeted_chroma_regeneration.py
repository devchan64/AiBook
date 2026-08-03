"""Regenerate four accepted style references with time-specific medium chroma."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-targeted-chroma-regeneration")
COMMON_CONTRACT = (
    "The scene fills all four canvas edges. No page border, black edge rectangle, panel frame, "
    "white margin, inset illustration, text, readable signs, logos, people, animals, or vehicles. "
    "Use sparse thin charcoal contour and structure lines over transparent watercolor washes with "
    "wet-on-wet bleeding, uneven pigment pooling, and layered translucent edges. Use natural "
    "medium-chroma pigment, never neon, fluorescent, opaque, airbrushed, digitally flat, densely "
    "hatched, crosshatched, stippled, ink-wash, sumi-e, photorealistic, screentoned, or thick comic outlined."
)
SCENES = [
    {
        "id": "gangnam-clear-day-targeted-chroma",
        "seed": 420651,
        "prompt": "Create a vertical Korean webtoon background of an empty Seoul Gangnam business intersection in bright clear midday. View sideways from a shaded near-left sidewalk corner. Layer diagonal blue-teal glass towers behind leaf-green street trees, with cool off-white pavement and crisp pale-blue reflected daylight. This is a lateral city-corner composition, never a centered road corridor. Keep the daylight colors clear and separately readable: no orange, red, pink, golden light, or sunset sky. ",
    },
    {
        "id": "aircraft-deep-night-targeted-chroma",
        "seed": 420652,
        "prompt": "Create a vertical Korean webtoon background inside an empty passenger aircraft at deep night. View diagonally from beside the rear window seats toward a short off-center row of plain dark-navy seat backs and oval windows. Outside is a distinctly indigo-black sky with faint stars; only tiny restrained tungsten reading-light reflections touch a few seat edges. Make the dark navy cabin, indigo windows, and small warm lights clearly separate without brightening the entire cabin. This is night, never dusk, dawn, or sunset: no apricot, orange, red, pink, golden sky, labels, symbols, or panels. ",
    },
    {
        "id": "atrium-dawn-high-angle-targeted-chroma",
        "seed": 420653,
        "prompt": "Create a vertical Korean webtoon background of an empty indoor atrium at early dawn, viewed steeply downward from an upper landing across diagonal stair flights, cool off-white tiled floor, benches, and a few potted plants. This is a genuine high-angle downward camera, never eye level, a frontal hallway, or centered one-point perspective. Use distinct cool teal-blue shadows and pale neutral daylight, with only a tiny soft apricot dawn reflection on one window. No orange or red sky, broad warm wash, or sunset effect. ",
    },
    {
        "id": "venice-oblique-sunset-targeted-chroma",
        "seed": 420654,
        "prompt": "Create a vertical Korean webtoon background of an empty Venice canal at sunset, viewed obliquely from a stone bridge-side edge. The canal bends diagonally between pale warm ochre facades. Use clear medium teal water with small indigo shadows and only a narrow apricot sky opening, so the water, stone, and sunset signal remain separate. Keep the composition oblique, never a centered canal corridor. No boats, signs, text, people, broad orange, red, pink, or neon color fields. ",
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

"""Regenerate accepted style-pack rows with time-balanced medium chroma."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-time-balanced-style-pack-regeneration")
COMMON_CONTRACT = (
    "The scene fills all four canvas edges. No page border, black edge rectangle, panel frame, white margin, inset illustration, text, readable signs, logos, people, animals, or vehicles. "
    "Use sparse thin charcoal contour and structure lines over transparent watercolor washes with wet-on-wet bleeding, uneven pigment pooling, and layered translucent edges. "
    "Use natural medium-chroma pigment, never neon, fluorescent, opaque, airbrushed, digitally flat, densely hatched, crosshatched, stippled, ink-wash, sumi-e, photorealistic, screentoned, or thick comic outlined."
)
SCENES = [
    {
        "id": "indoor-dawn-high-angle-medium-chroma",
        "seed": 420642,
        "prompt": "Create a vertical Korean webtoon background of an empty indoor atrium at early dawn, viewed steeply downward from an upper landing across stair flights, tiled floor, benches, and a few potted plants. This is a genuine high-angle downward camera, never eye level, a frontal hallway, or centered one-point perspective. Use cool off-white surfaces, subdued teal shadows, and only a small soft apricot dawn reflection near one window. No orange or red sky, broad warm wash, or sunset effect. ",
    },
    {
        "id": "gangnam-day-lateral-medium-chroma",
        "seed": 420643,
        "prompt": "Create a vertical Korean webtoon background of an empty Seoul Gangnam business intersection in clear midday. View sideways across the broad crossing from a shaded sidewalk at the near left corner; teal glass facades overlap at diagonal angles, leaf-green street trees occupy the middle ground, and cool off-white paving crosses the lower third. This is a lateral city-corner composition, never a centered road corridor. No orange, red, pink, golden light, or sunset sky. ",
    },
    {
        "id": "outdoor-sunset-low-angle-medium-chroma",
        "seed": 420644,
        "prompt": "Create a vertical Korean webtoon background of an empty residential street at sunset, viewed from near curb height looking upward past a bicycle rack, blank house facades, tree branches, and a narrow sky. This is a genuine low-angle upward view with strong foreground-to-sky scale change, never eye level or a centered corridor. Use muted teal shadows, olive foliage, and a limited apricot sunset glow only at the sky edge; do not use broad vermilion, pink, red, or neon washes. ",
    },
    {
        "id": "venice-sunset-oblique-medium-chroma",
        "seed": 420645,
        "prompt": "Create a vertical Korean webtoon background of an empty Venice canal at sunset, viewed obliquely from a stone bridge-side edge. The canal bends diagonally between pale warm ochre facades; medium teal water has small indigo shadows, and only a narrow apricot sky opening indicates sunset. Keep the composition oblique, never a centered canal corridor. No boats, signs, text, people, broad orange, red, pink, or neon color fields. ",
    },
    {
        "id": "aircraft-night-oblique-medium-chroma",
        "seed": 420646,
        "prompt": "Create a vertical Korean webtoon background inside an empty passenger aircraft at deep night. View diagonally from beside the rear window seats toward a short row of plain blank dark-navy seat backs and oval windows. Outside is an indigo-black sky with faint stars; tiny tungsten reading-light reflections appear only on seat edges. Keep the aisle off-center. This is night, never dusk, dawn, or sunset: no apricot, orange, red, pink, golden sky, labels, symbols, or panels. ",
    },
    {
        "id": "rainy-night-overhead-medium-chroma",
        "seed": 420647,
        "prompt": "Create a vertical Korean webtoon background of an empty Seoul rooftop plaza immediately after rain at late night, viewed steeply downward from a high terrace. Broad wet paving, two large planters, and a shallow puddle form simple diagonal planes. Use indigo and navy night shadows, restrained teal wet reflections, and only a few small tungsten reflections in puddles. No rain streaks, rails, apricot, orange, red, pink, golden sky, or broad warm wash. This is a genuine overhead high-angle camera, never eye level. ",
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

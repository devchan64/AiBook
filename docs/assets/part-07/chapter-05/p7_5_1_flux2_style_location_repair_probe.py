"""Retry rejected local watercolor style locations with failure-specific prompts."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-style-location-repair")
STYLE_CONTRACT = (
    "Fill every canvas edge. No page border, black edge rectangle, panel frame, white margin, inset illustration, text, readable signs, logos, people, animals, or vehicles. "
    "Use sparse thin charcoal contour and structure lines over large transparent watercolor washes in pale teal, muted olive, warm apricot, soft indigo, and warm off-white. "
    "Do not use hatching, crosshatching, stippling, parallel shading lines, dense ink texture, ink wash, sumi-e, photorealism, airbrush, screentones, thick comic outlines, or neon."
)
SCENES = [
    {
        "id": "gangnam-day-oblique-repair",
        "seed": 420621,
        "prompt": "Create a vertical Korean webtoon background of an empty Seoul Gangnam business district in clear daytime. View a broad tree-lined boulevard obliquely from one sidewalk corner so the nearest glass facade enters from the left and the street recedes diagonally to the right. Show no storefront signs, billboards, letters, or logos; use only blank facades and unmarked street furniture. This is a wide lateral city view, never a centered one-point street canyon. ",
    },
    {
        "id": "zhangjiajie-low-angle-repair",
        "seed": 420622,
        "prompt": "Create a vertical Korean webtoon background of an empty stone path in Zhangjiajie National Forest Park, China, viewed close to the ground looking upward through sandstone pillars and hanging vegetation. Make a true low-angle upward view with large simple watercolor cliff planes and only a few clean contour lines around the pillar silhouettes. Do not draw repeated vertical texture marks or any shading lines on the rock faces. ",
    },
    {
        "id": "passenger-aircraft-night-oblique-repair",
        "seed": 420623,
        "prompt": "Create a vertical Korean webtoon background of an empty passenger aircraft cabin in deep night. View diagonally from beside the rear window seats toward a short row of unbranded seats and oval windows; outside is a nearly black indigo sky with faint stars. Keep the aisle out of the center and let dim warm reading lights reflect subtly on seat edges. This is a side-oblique cabin view, never a centered aisle perspective and never daylight. ",
    },
    {
        "id": "train-platform-rainy-night-overhead-repair",
        "seed": 420624,
        "prompt": "Create a vertical Korean webtoon background of an empty train platform in heavy rain at night, viewed diagonally from a high pedestrian bridge. Wet paving and rails reflect warm platform lamps and a deep indigo-black sky; the nearest canopy enters from one side and the tracks recede diagonally instead of forming a centered corridor. No readable signs, train cars, or people. The dark artificial night lighting must be unmistakable. ",
    },
]


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
    runs = []
    try:
        pipe = Flux2KleinPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR)
        pipe.enable_sequential_cpu_offload()
        for scene in SCENES:
            scene_started = time.monotonic()
            image = pipe(
                prompt=scene["prompt"] + STYLE_CONTRACT,
                width=768,
                height=1152,
                num_inference_steps=50,
                guidance_scale=4.0,
                generator=torch.Generator(device="cpu").manual_seed(scene["seed"]),
                max_sequence_length=256,
            ).images[0]
            output = OUTPUT_DIR / f"{scene['id']}.png"
            image.save(output)
            runs.append({"id": scene["id"], "seed": scene["seed"], "elapsed_seconds": round(time.monotonic() - scene_started, 1), "output_image": str(output)})
        (OUTPUT_DIR / "run.json").write_text(json.dumps({"status": "review_required", "model_id": MODEL_ID, "size": [768, 1152], "steps": 50, "guidance_scale": 4.0, "elapsed_seconds": round(time.monotonic() - started, 1), "gpu_memory_before_mib": before, "gpu_memory_peak_mib": peak, "runs": runs}, indent=2), encoding="utf-8")
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

"""Targeted retry for two rejected local watercolor style locations."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-style-targeted-repair")
STYLE_CONTRACT = (
    "Fill every canvas edge with the scene itself. No page border, black edge rectangle, panel frame, white margin, inset illustration, text, readable signs, logos, people, animals, or vehicles. "
    "Use sparse thin charcoal contour and structure lines over large transparent watercolor washes in pale teal, muted olive, warm apricot, soft indigo, and warm off-white. "
    "Do not use hatching, crosshatching, stippling, parallel shading lines, dense ink texture, ink wash, sumi-e, photorealism, airbrush, screentones, thick comic outlines, or neon."
)
SCENES = [
    {
        "id": "zhangjiajie-side-low-angle-repair",
        "seed": 420625,
        "prompt": "Create a vertical Korean webtoon background in Zhangjiajie National Forest Park, China. From a stone ledge near ground level, look upward diagonally across three broad sandstone pillars and hanging vegetation; the closest pillar enters from one side and the distant sky opens on the other side. Avoid a centered canyon corridor, symmetry, and any dark edge around the image. Paint each cliff as a single broad, simple transparent watercolor plane with only a few clean silhouette contours, never repeated rock marks or shading lines. ",
    },
    {
        "id": "passenger-aircraft-night-window-repair",
        "seed": 420626,
        "prompt": "Create a vertical Korean webtoon background inside an empty passenger aircraft at deep night. From the window-side rear seats, look diagonally across two plain dark-navy fabric seat backs toward oval windows. Every headrest and seat back is completely blank and unmarked: no labels, letters, symbols, logos, stitching patterns, screens, or printed panels. Outside the windows is a nearly black indigo star sky. Keep the aisle off-center, use dim warm reading lights only, and never show daylight. ",
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
        pipe = Flux2KleinPipeline.from_pretrained(
            MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR
        )
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
            runs.append(
                {
                    "id": scene["id"],
                    "seed": scene["seed"],
                    "elapsed_seconds": round(time.monotonic() - scene_started, 1),
                    "output_image": str(output),
                }
            )
        (OUTPUT_DIR / "run.json").write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "model_id": MODEL_ID,
                    "size": [768, 1152],
                    "steps": 50,
                    "guidance_scale": 4.0,
                    "elapsed_seconds": round(time.monotonic() - started, 1),
                    "gpu_memory_before_mib": before,
                    "gpu_memory_peak_mib": peak,
                    "runs": runs,
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

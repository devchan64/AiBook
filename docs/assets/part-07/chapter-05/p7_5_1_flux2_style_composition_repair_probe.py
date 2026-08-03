"""Change composition, rather than only negative wording, for style-pack failures."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-style-composition-repair")
STYLE_CONTRACT = (
    "The painted scene reaches all four canvas edges. There is no border, black rectangular outline, comic panel, page, inset image, white margin, text, sign, logo, person, animal, or vehicle. "
    "Use only sparse thin charcoal contour and structure lines over broad transparent watercolor washes in pale teal, muted olive, warm apricot, soft indigo, and warm off-white. "
    "No hatching, crosshatching, stippling, parallel shading lines, dense texture, ink wash, sumi-e, photorealism, airbrush, screentones, thick comic outlines, or neon."
)
SCENES = [
    {
        "id": "gangnam-side-intersection-repair",
        "seed": 420627,
        "prompt": "Vertical watercolor webtoon setting: an empty Seoul Gangnam business intersection in clear daytime, seen from a shaded sidewalk at the near left corner looking sideways across the broad crossing. The road runs horizontally through the lower third; three glass building facades overlap at diagonal angles, with the nearest facade large at left and a second facade turning away at right. This is a lateral street corner composition with no road corridor, no center vanishing point, no centered street, and no shop signage. ",
    },
    {
        "id": "passenger-aircraft-close-window-repair",
        "seed": 420628,
        "prompt": "Vertical watercolor webtoon setting: an empty passenger aircraft window-side at deep night. Fill the canvas with a close diagonal view of one plain blank navy seat back at lower right, three oval windows along the left wall, and the softly lit ceiling above. The nearest window opens directly to an indigo-black star sky. Seat surfaces are completely unmarked with no labels, letters, symbols, stitched patterns, screens, or panels. This is a wall-to-wall close interior view, not a framed illustration and not a centered aisle. ",
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
            runs.append({"id": scene["id"], "seed": scene["seed"], "elapsed_seconds": round(time.monotonic() - scene_started, 1), "output_image": str(output)})
        (OUTPUT_DIR / "run.json").write_text(json.dumps({"status": "review_required", "model_id": MODEL_ID, "size": [768, 1152], "steps": 50, "guidance_scale": 4.0, "elapsed_seconds": round(time.monotonic() - started, 1), "gpu_memory_before_mib": before, "gpu_memory_peak_mib": peak, "runs": runs}, indent=2), encoding="utf-8")
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

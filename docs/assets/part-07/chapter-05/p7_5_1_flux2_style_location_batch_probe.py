"""Generate location-diverse, frame-free local watercolor style candidates."""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
OUTPUT_DIR = Path("/tmp/p7-5-1-style-location-batch")
STYLE_CONTRACT = (
    "The image fills every edge of the canvas with no page border, no black rectangle at the edge, no panel frame, no white margin, no inset illustration, no text, no readable signs, no people, no animals, and no vehicles. "
    "Use thin charcoal contour and structural perspective lines that remain visible above transparent watercolor washes: pale teal shadows, muted olive foliage, warm apricot light, soft indigo shadow, and warm off-white surfaces. "
    "Use no hatching, no crosshatching, no stippling, no dense ink texture, no monochrome ink wash, no sumi-e, no calligraphy, no photorealism, no opaque airbrush, no screentones, no thick comic outlines, and no neon."
)
SCENES = [
    {
        "id": "gangnam-day-wide",
        "seed": 420611,
        "prompt": "Create a full-bleed vertical background painting for a Korean webtoon: an empty Seoul Gangnam business district boulevard in clear daytime, with tall glass office towers, broad sidewalks, ginkgo trees, and restrained Korean urban street furniture. Use a genuinely wide eye-level camera with a long lateral streetscape, not a centered one-point corridor, not a low angle, and not an aerial view. ",
    },
    {
        "id": "zhangjiajie-low-angle",
        "seed": 420612,
        "prompt": "Create a full-bleed vertical background painting for a Korean webtoon: an empty stone path in Zhangjiajie National Forest Park, China, viewed from a camera close to the path and looking upward at tall sandstone pillars, hanging vegetation, and misty sky. Use a genuine low-angle upward camera with strong foreground-to-cliff scale change, not eye level, not a centered hallway, and not an aerial view. ",
    },
    {
        "id": "venice-sunset-oblique",
        "seed": 420613,
        "prompt": "Create a full-bleed vertical background painting for a Korean webtoon: an empty Venice canal at sunset, seen obliquely from the side of a small stone bridge with diagonal water, weathered palazzi, mooring posts, and a distant narrow bend. Use a genuine oblique side-view camera, not a centered frontal canal, not eye-level corridor symmetry, and not a high aerial view. ",
    },
    {
        "id": "passenger-aircraft-night-oblique",
        "seed": 420614,
        "prompt": "Create a full-bleed vertical background painting for a Korean webtoon: an empty passenger aircraft cabin at night, viewed diagonally across the aisle toward rows of unbranded seats, overhead bins, oval windows with deep indigo sky, and dim warm reading lights. Use a genuine oblique side-view camera, not a centered aisle, not a frontal cabin symmetry, and not a wide exterior shot. ",
    },
    {
        "id": "train-platform-rainy-overhead",
        "seed": 420615,
        "prompt": "Create a full-bleed vertical background painting for a Korean webtoon: an empty train platform on a rainy night, seen from a high pedestrian bridge looking steeply down on wet platform paving, canopy edges, rails, puddle reflections, and distant signal lights without readable text. Use a genuine overhead high-angle camera, not eye level, not a centered platform corridor, and not a frontal elevation. ",
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
            MODEL_ID,
            torch_dtype=torch.bfloat16,
            cache_dir=CACHE_DIR,
        )
        pipe.enable_sequential_cpu_offload()
        for scene in SCENES:
            scene_started = time.monotonic()
            prompt = scene["prompt"] + STYLE_CONTRACT
            image = pipe(
                prompt=prompt,
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
                    "prompt": prompt,
                    "elapsed_seconds": round(time.monotonic() - scene_started, 1),
                    "output_image": str(output),
                }
            )
        (OUTPUT_DIR / "run.json").write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "model_id": MODEL_ID,
                    "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload",
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

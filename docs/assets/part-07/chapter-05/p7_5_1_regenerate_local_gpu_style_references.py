"""Regenerate the nine P7-5.1 style-reference rows on the local GPU only.

Outputs are review candidates. This script never marks an image approved.
"""

import json
import os
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline


ASSET_DIR = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
SIZE = (768, 1152)
STEPS = 50
GUIDANCE = 4.0
COMMON_CONTRACT = (
    "Create an edge-to-edge Korean webtoon background: at every image border the depicted architecture, ground, sky, or foliage "
    "continues naturally, as if the camera cuts through an ongoing real space. Do not draw an outer rectangular outline or surround "
    "the scene with a dark border. Use a transparent watercolor-and-ink medium inside the depicted architecture: sparse thin charcoal contour "
    "and structure lines contain visible wet-on-wet blooms, uneven pigment pooling, granulating translucent washes, "
    "and layered translucent edges. Make the material texture and lighting visibly varied: distinct translucent pigment pools on "
    "lit planes, cool shadow planes, and small reflected-light accents must remain separately readable, never one uniform teal or gray wash. "
    "Use natural medium-chroma pigment, never neon, fluorescent, opaque, airbrushed, "
    "digitally flat, densely hatched, crosshatched, stippled, ink-wash, sumi-e, photorealistic, screentoned, or thick comic outlined. "
    "Exclude readable signs, logos, people, animals, and vehicles."
)
SCENES = [
    {
        "id": "atrium-dawn-high-angle",
        "seed": 420713,
        "prompt": "Create a vertical Korean webtoon background of an empty indoor atrium at early dawn, viewed steeply downward from an upper landing across diagonal stair flights, cool off-white tiled floor, benches, and a few potted plants. The camera is inside a continuing atrium, with walls, stairs, window light, and floor tiles naturally cut by the image edges. This is a genuine high-angle downward camera, never eye level, a frontal hallway, or centered one-point perspective. Show a pale blue-gray dawn window, blue-teal shadows on the stair undersides, cool off-white tiles, and a narrow pale-cyan reflected stripe on the floor; add only one tiny muted apricot glint, never a broad peach window or sunset effect. Render detailed layered shadows: window-mullion shadows, thin railing shadows, stair-tread contact shadows, and small plant shadows cross the tiled floor at different blue-gray and teal values. Alternate darker stair undersides with lighter reflected stair edges. Make the watercolor unmistakably visible inside the tile planes, wall shadows, and stair risers: overlapping transparent blue-gray and teal glazes, soft wet-on-wet blooms that feather across adjacent tiles, granulating pigment speckles, irregular tide marks, and small darker pigment pools along tile joints and contact-shadow edges. Keep the ink structure crisp while the painted areas stay varied rather than smoothly airbrushed. ",
    },
    {
        "id": "courtyard-early-morning-high-angle",
        "seed": 420702,
        "prompt": "Create a vertical Korean webtoon background of an empty Seoul residential courtyard in clear early morning, viewed steeply downward from an upper balcony. Diagonal paved paths, a small tree, benches, planters, and low building roofs create varied depth and cross the canvas edges naturally. This is a genuine high-angle downward camera, never eye level, a frontal hallway, or centered one-point perspective. Separate cool off-white paving, blue-teal cast shadows, leaf-green foliage, pale-blue reflected sky light, and one tiny warm window glint with visibly varied watercolor pigment pools. ",
    },
    {
        "id": "downtown-clear-day-wide",
        "seed": 420703,
        "prompt": "Create a vertical Korean webtoon background of an empty Seoul business intersection in bright clear midday. View sideways from a shaded near-left sidewalk corner. Layer diagonal blue-teal glass towers behind leaf-green street trees, with cool off-white pavement and crisp pale-blue reflected daylight. Put pale-blue sky reflections in glass, deeper teal building shadows, green foliage shadows, and cool gray pavement highlights in separate watercolor pools. This is a lateral city-corner composition, never a centered road corridor. Keep daylight colors clear and separately readable: no orange, red, pink, golden light, or sunset sky. ",
    },
    {
        "id": "residential-sunset-low-angle",
        "seed": 420704,
        "prompt": "Create a vertical Korean webtoon background of an empty residential street at sunset, viewed from near curb height looking upward past a bicycle rack, blank house facades, tree branches, and a narrow sky. This is a genuine low-angle upward view with strong foreground-to-sky scale change, never eye level or a centered corridor. Separate cool teal shadowed pavement, olive foliage, blue-gray facade shadows, and a limited apricot rim light only at the narrow sky edge; add subtle warm reflected color only to upward-facing edges. Do not use broad vermilion, pink, red, or neon washes. ",
    },
    {
        "id": "aircraft-night-oblique",
        "seed": 420705,
        "prompt": "Create a vertical Korean webtoon background inside one physically plausible empty commercial aircraft cabin at deep night. Use a simple eye-level view from the rear of one standard economy row looking forward: one straight central aisle divides exactly three attached seats on the left and exactly three attached seats on the right, a clear 3+3 layout. Each side shows three equal seat backs touching across shared armrests; keep all six foreground seats visible as one uncomplicated row. Repeat only a few matching 3+3 rows farther ahead, with no complex diagonal composition, pods, single armchairs, extra aisles, or cropped seat groups. The entire top half of the frame is a continuous closed interior ceiling: dark navy opaque ceiling panels, overhead bins, and a central service strip span edge to edge with no gaps. Never show sky, stars, a skylight, glass roof, open roof, or exterior darkness above the seat backs. Exterior night is visible only as small indigo-black areas through evenly spaced oval windows on the side walls. Keep the cabin genuinely dim: navy upholstery and blue-gray walls are mostly in shadow; use only a few tiny, low-intensity cool-white reading lights and very small muted tungsten accents, never broad white, cream, or warm ceiling illumination. Show only one continuous cabin, never impossible stairs, intersecting seats, duplicated aisles, mismatched window heights, or broken aircraft geometry. Make the watercolor unmistakable inside the seats, ceiling, wall, and floor: layered transparent navy and blue-gray glazes, soft wet-on-wet blooms around the few lights, granulating pigment, irregular tide marks, and darker pigment pooling in seat seams and contact shadows. Keep thin charcoal structure lines crisp over the translucent washes, never smooth digital gradients or flat opaque coloring. This is night, never dusk, dawn, or sunset: no apricot, orange, red, pink, golden sky, labels, symbols, or panels. ",
    },
    {
        "id": "rooftop-rainy-night-overhead",
        "seed": 420706,
        "prompt": "Create a vertical Korean webtoon background of an empty Seoul rooftop plaza immediately after rain at late night, viewed steeply downward from a high terrace. Broad wet paving, two large planters, and a shallow puddle form simple diagonal planes. Make deep indigo shadow planes, navy wet pavement, cyan-blue puddle reflections, and a few small tungsten reflections visibly distinct; reflected colors should break and pool across wet surfaces. No rain streaks, rails, apricot, orange, red, pink, golden sky, or broad warm wash. This is a genuine overhead high-angle camera, never eye level. ",
    },
    {
        "id": "venice-sunset-oblique",
        "seed": 420707,
        "prompt": "Create a vertical Korean webtoon background of an empty Venice canal at sunset, viewed obliquely from a stone bridge-side edge. The canal bends diagonally between pale warm ochre facades. Separate clear medium teal water, small indigo water shadows, pale stone reflected light, and only a narrow apricot sky opening in visibly varied translucent pigment pools. Keep the composition oblique, never a centered canal corridor. No boats, signs, text, people, broad orange, red, pink, or neon color fields. ",
    },
    {
        "id": "park-clear-day-eye-level",
        "seed": 420708,
        "prompt": "Create a vertical Korean webtoon background of an empty city park pond in clear midday, viewed at a calm eye-level diagonal from a cool off-white path. Separate teal pond reflections, leaf-green foliage, pale-blue sky reflection, cool off-white path, and blue-green shade under trees in visibly varied watercolor pigment pools so the daylight is not flat. Keep the water edge diagonal and avoid a centered path corridor. No people, animals, signs, text, orange, red, pink, golden sky, or frame. ",
    },
    {
        "id": "train-platform-rainy-night-oblique",
        "seed": 420709,
        "prompt": "Create a vertical Korean webtoon background of an empty open-air Seoul train platform immediately after rain at late night. View obliquely along the platform under a simple canopy; the platform edge, a few roof columns, blank benches, and only two subtle rail lines recede diagonally. Separate dark indigo wet pavement, navy rain shadows, cool-white canopy light, local tungsten lamps, and cyan puddle reflections as broken colorful pools across the ground. No train, route map, timetable, readable sign, or centered corridor. ",
    },
]


def gpu_memory_mib() -> int:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        check=True,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.splitlines()[0])


def main() -> None:
    requested_scene = os.environ.get("P7_STYLE_SCENE")
    run_label = os.environ.get("P7_STYLE_RUN_LABEL", "v1")
    excluded_scenes = {item for item in os.environ.get("P7_STYLE_EXCLUDE", "").split(",") if item}
    scenes = [scene for scene in SCENES if scene["id"] == requested_scene] if requested_scene else SCENES
    scenes = [scene for scene in scenes if scene["id"] not in excluded_scenes]
    if requested_scene and not scenes:
        raise KeyError(f"Unknown P7_STYLE_SCENE: {requested_scene}")
    if not scenes:
        raise ValueError("No scenes selected for generation")
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
        for scene in scenes:
            scene_started = time.monotonic()
            image = pipe(
                prompt=scene["prompt"] + COMMON_CONTRACT,
                width=SIZE[0],
                height=SIZE[1],
                num_inference_steps=STEPS,
                guidance_scale=GUIDANCE,
                generator=torch.Generator(device="cpu").manual_seed(scene["seed"]),
                max_sequence_length=256,
            ).images[0]
            image_name = f"p7-5-1-style-{scene['id']}-local-gpu-{run_label}.png"
            image.save(ASSET_DIR / image_name)
            runs.append(
                {
                    "id": scene["id"],
                    "seed": scene["seed"],
                    "asset": image_name,
                    "elapsed_seconds": round(time.monotonic() - scene_started, 1),
                    "status": "review_required",
                }
            )
            torch.cuda.empty_cache()
    finally:
        stop.set()
        observer.join(timeout=2)

    record = {
        "status": "review_required",
        "model_id": MODEL_ID,
        "runtime": "local GPU via Diffusers Flux2KleinPipeline sequential CPU offload",
        "size": list(SIZE),
        "steps": STEPS,
        "guidance_scale": GUIDANCE,
        "elapsed_seconds": round(time.monotonic() - started, 1),
        "gpu_memory_before_mib": before,
        "gpu_memory_peak_mib": peak,
        "requested_scene": requested_scene,
        "excluded_scenes": sorted(excluded_scenes),
        "runs": runs,
    }
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()

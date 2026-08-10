"""Generate P7-5.1 style-reference review candidates on the local GPU.

Outputs are review candidates. This script never marks an image approved.
Set ``P7_STYLE_SCENE`` to regenerate one named existing or extension scene.
Set ``P7_STYLE_INCLUDE_EXISTING=1`` to regenerate all twenty rows; otherwise
the default remains the eleven extension rows.
"""

import json
import os
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from p7_5_image_output_naming import candidate_stem


ASSET_DIR = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-base-4B"
CACHE_DIR = Path("/tmp/flux2-klein-base-4b-diffusers-cache")
SIZE = (768, 1152)
STEPS = 12
GUIDANCE = 4.0
STYLE_PROMPT_PATH = ASSET_DIR / "p7-5-1-style-prompt-contract.json"
COMMON_CONTRACT = json.loads(STYLE_PROMPT_PATH.read_text(encoding="utf-8"))["common_contract"]
SCENES = [
    {
        "id": "atrium-dawn-high-angle",
        "generate_by_default": False,
        "seed": 420713,
        "prompt": "Vertical empty indoor atrium at early dawn, steep high-angle from an upper landing. Diagonal stair flights, tiled floor, benches, and plants cross the edges; avoid a frontal hallway. Cool off-white tiles, blue-gray window light, teal stair shadows, and one small muted apricot reflection. ",
    },
    {
        "id": "courtyard-early-morning-high-angle",
        "generate_by_default": False,
        "seed": 420702,
        "prompt": "Vertical empty Seoul residential courtyard in clear early morning, steep high-angle from a balcony. Diagonal paving, one tree, benches, planters, and low roofs cross the edges. Cool off-white paving, blue-teal shadows, leaf green, pale-blue sky reflection, and one tiny warm window glint. ",
    },
    {
        "id": "downtown-clear-day-wide",
        "generate_by_default": False,
        "seed": 420703,
        "prompt": "Vertical empty Seoul business intersection at clear midday, side view from a shaded sidewalk corner. Diagonal glass towers and street trees, cool off-white pavement; avoid a centered road corridor. Pale-blue glass reflections, teal building shadows, green foliage shadows, cool-gray highlights. ",
    },
    {
        "id": "residential-sunset-low-angle",
        "generate_by_default": False,
        "seed": 420704,
        "prompt": "Vertical empty residential street at sunset, low angle from curb height toward bicycle rack, house facades, branches, and narrow sky. Strong foreground-to-sky scale; avoid eye level and a centered corridor. Teal pavement shadow, olive foliage, blue-gray walls, narrow muted-apricot sky rim. ",
    },
    {
        "id": "night-lit-reading-room-oblique",
        "generate_by_default": False,
        "seed": 420705,
        "prompt": "Vertical empty window-side reading room at deep night, diagonal view from the left window wall. Wood table in lower-left foreground; window frames and floorboards run toward upper right. Indigo exterior, blue-gray room shadow, one small table lamp with a compact amber tabletop reflection. ",
    },
    {
        "id": "rooftop-rainy-night-overhead",
        "generate_by_default": False,
        "seed": 420706,
        "prompt": "Vertical empty Seoul rooftop plaza after rain at late night, steep overhead from a high terrace. Wet paving, two planters, and one shallow puddle form diagonal planes. Deep indigo shadow, navy pavement, cyan puddle reflections, and a few small tungsten reflections; no rain streaks or warm sky. ",
    },
    {
        "id": "venice-sunset-oblique",
        "generate_by_default": False,
        "seed": 420707,
        "prompt": "Vertical empty Venice canal at sunset, oblique view from a stone bridge edge. A diagonal canal bends between pale ochre facades; avoid a centered canal. Medium teal water, small indigo water shadows, pale stone reflection, and a narrow muted-apricot sky opening. ",
    },
    {
        "id": "park-clear-day-eye-level",
        "generate_by_default": False,
        "seed": 420708,
        "prompt": "Vertical empty city park pond at clear midday, calm eye-level diagonal from a cool off-white path. Diagonal water edge, teal pond reflection, leaf green, pale-blue sky reflection, and blue-green tree shade; avoid a centered path corridor. ",
    },
    {
        "id": "train-platform-rainy-night-oblique",
        "generate_by_default": False,
        "seed": 420709,
        "prompt": "Vertical empty open-air Seoul train platform after rain at late night, oblique view under a simple canopy. Platform edge, columns, blank benches, and two rail lines recede diagonally. Indigo wet pavement, navy shadows, cool-white canopy light, small tungsten pools, and cyan puddle reflections. ",
    },
    {
        "id": "gallery-midday-oblique", "generate_by_default": True, "seed": 420810,
        "prompt": "Vertical empty contemporary gallery at clear midday, oblique view from a near corner. Off-white walls, cool-gray floor, blank plinths, and ceiling tracks form diagonal planes crossing the edges. Pale-blue reflection, blue-gray shadow, and one muted-apricot accent; avoid artworks, visitors, labels, and a centered corridor. ",
    },
    {
        "id": "library-stairwell-day-high-angle", "generate_by_default": True, "seed": 420811,
        "prompt": "Vertical empty public-library stairwell in daylight, steep high-angle from an upper landing. Diagonal flights, railings, terrazzo treads, book-return shelves, and a tall frosted window cross the edges. Cool off-white treads, blue-teal shadows, muted wood, and pale-cyan reflections; avoid people, book titles, signs, and a frontal hallway. ",
    },
    {
        "id": "harbor-plaza-sunrise-high", "generate_by_default": True, "seed": 420812,
        "prompt": "Vertical empty harbor plaza at sunrise, high oblique view from a terrace. Angular paving, bollards, low seawall, distant water, and sparse planting cut through the edges. Blue-teal water, indigo shadow, cool off-white paving, and a narrow muted-apricot horizon; avoid boats, people, signs, broad orange light, and a centered waterfront. ",
    },
    {
        "id": "underpass-rainy-twilight", "generate_by_default": True, "seed": 420813,
        "prompt": "Vertical empty pedestrian underpass just after rain at blue twilight, diagonal view from its entrance into a gently bending passage. Concrete walls, wet tile, blank columns, and a narrow cool-sky opening cross the edges. Indigo wet shadows, blue-gray concrete, cyan puddles, and small warm safety lights; avoid people, graffiti, signs, trains, and a centered tunnel. ",
    },
    {
        "id": "hillside-alley-late-afternoon", "generate_by_default": True, "seed": 420814,
        "prompt": "Vertical empty hillside alley in late afternoon, eye-level view along a diagonal climbing path. Retaining walls, blank small-house facades, unmarked poles, steps, and foliage overlap at the edges. Teal pavement shadows, leaf-green foliage, blue-gray walls, and a narrow muted-apricot rim; avoid people, vehicles, signs, broad sunset orange, and a centered corridor. ",
    },
    {
        "id": "market-arcade-overcast", "generate_by_default": True, "seed": 420815,
        "prompt": "Vertical empty covered market arcade under soft overcast daylight, oblique view across shuttered blank stalls. Canopy ribs, damp cool-gray floor, unmarked crates, and side openings create diagonal depth at the edges. Cool off-white skylight, blue-teal shadow, muted olive, and faint cyan reflections; avoid shoppers, products, signs, logos, and a centered corridor. ",
    },
    {
        "id": "riverside-terrace-night", "generate_by_default": True, "seed": 420816,
        "prompt": "Vertical empty riverside terrace at night, oblique view beside a low stone planter. Broad promenade, river edge, blank benches, distant bridge silhouette, and sparse trees cross the edges. Navy pavement, indigo water, cyan-blue reflections, cool-white lights, and two muted tungsten pools; avoid people, boats, signs, neon, and a centered corridor. ",
    },
    {
        "id": "greenhouse-blue-hour", "generate_by_default": True, "seed": 420817,
        "prompt": "Vertical empty greenhouse conservatory at blue hour, quiet eye-level diagonal. Glass roof ribs, damp stone path, leafy plants, benches, and a distant glass door cross the edges. Pale-blue exterior light, blue-teal glass shadow, leaf green, cool off-white highlights, and tiny warm glints; avoid people, labels, signs, animals, and a centered aisle. ",
    },
    {
        "id": "ferry-deck-morning", "generate_by_default": True, "seed": 420818,
        "prompt": "Vertical empty open ferry deck in clear morning light, oblique view beside a blank bench toward railings and distant water. Deck planks, simple rail posts, unmarked life-ring housing, and horizon cross the edges. Cool off-white deck light, teal sea, pale-blue reflections, navy rail shadow, muted-apricot accent; avoid people, boats, text, logos, and a centered corridor. ",
    },
    {
        "id": "cinema-foyer-night", "generate_by_default": True, "seed": 420819,
        "prompt": "Vertical empty neighborhood cinema foyer at night, eye-level view from a side corner. Dark-indigo tiles, blank ticket counter planes, unlettered poster frames, ceiling lights, and glass reflections create an oblique composition at the edges. Deep navy shadow, cool-white light, cyan reflections, restrained amber pools; avoid people, film images, signs, logos, and a centered hallway. ",
    },
    {
        "id": "ceramics-studio-afternoon", "generate_by_default": True, "seed": 420820,
        "prompt": "Vertical empty ceramics studio in quiet afternoon light, diagonal view across a worktable. Pottery wheel, blank shelves, unmarked clay forms, tall windows, and cool concrete floor cross the edges. Pale-blue window light, blue-gray shadow, muted clay beige, leaf-green reflection, and a small apricot highlight; avoid people, lettering, logos, and a centered aisle. ",
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
    include_existing = os.environ.get("P7_STYLE_INCLUDE_EXISTING") == "1"
    excluded_scenes = {item for item in os.environ.get("P7_STYLE_EXCLUDE", "").split(",") if item}
    scenes = [scene for scene in SCENES if scene["id"] == requested_scene] if requested_scene else [
        scene for scene in SCENES if include_existing or scene["generate_by_default"]
    ]
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
            image_name = f"{candidate_stem(f'p7-5-1-style-{scene["id"]}-local-gpu-{run_label}', seed=scene['seed'], steps=STEPS, contract={'model': MODEL_ID, 'prompt': scene['prompt'] + COMMON_CONTRACT, 'size': SIZE, 'guidance': GUIDANCE})}.png"
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
        "include_existing": include_existing,
        "excluded_scenes": sorted(excluded_scenes),
        "runs": runs,
    }
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()

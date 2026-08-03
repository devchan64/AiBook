"""Generate one P7-5.2 full-body character master from an approved P7-5.1 original.

The model receives one approved original, not a tiled contact sheet. This is a
review-only P7-5.2 experiment and never changes P7-5.1 or P7-5.3 approval.
"""

import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ASSET_DIR = Path(__file__).parent
STYLE_LEDGER = ASSET_DIR / "p7-5-1-local-style-pack-review.json"
STYLE_SCENE_ID = "outdoor-day-wide"
OUTPUT = ASSET_DIR / "p7-5-2-style-pack-character-master-v1.png"
RUN = ASSET_DIR / "p7-5-2-style-pack-character-master-v1.json"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
CACHE_DIR = Path("/tmp/flux2-klein-diffusers-cache")
SIZE = (768, 1152)
STEPS = 8
GUIDANCE = 1.0
SEED = 420751
PROMPT = (
    "Create exactly one original full-body adult Korean webtoon character reference illustration, "
    "using the reference image only for its drawing-line and transparent-watercolor visual language. "
    "Mira stands naturally facing the camera, fully visible from the top of her head to both shoe soles, "
    "on a plain off-white studio background. She has a symmetric jaw-length deep teal-blue bob with a soft center part, "
    "warm light-peach skin, dark-brown almond-shaped eyes, a calm neutral expression, a white cropped utility jacket "
    "over a charcoal crew-neck shirt, teal high-waisted wide-leg trousers, and plain white sneakers. "
    "Use living thin charcoal drawing lines and restrained transparent watercolor washes, with clear flat local colors "
    "and soft single-edge fold shadows. Keep hair dark teal-blue with muted teal highlights and keep skin even warm light peach. "
    "No bag, backpack, purse, belt pouch, jewelry, handheld object, extra person, duplicate limbs, cropped body, outer frame line, "
    "panel border, text, logo, watermark, photorealism, screentones, heavy hatching, or dramatic scene lighting."
)


def gpu_memory_mib() -> int:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        check=False,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.splitlines()[0])


def approved_style_original() -> tuple[dict, Path]:
    ledger = json.loads(STYLE_LEDGER.read_text(encoding="utf-8"))
    for run in ledger["reviewed_runs"]:
        if run.get("scene_id") == STYLE_SCENE_ID and run.get("status") == "approved":
            source = ASSET_DIR / run["asset"]
            if not source.is_file():
                raise FileNotFoundError(source)
            return run, source
    raise LookupError(f"No approved P7-5.1 style original for {STYLE_SCENE_ID}")


def main() -> None:
    source_record, source = approved_style_original()
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
            image=Image.open(source).convert("RGB"),
            prompt=PROMPT,
            width=SIZE[0],
            height=SIZE[1],
            num_inference_steps=STEPS,
            guidance_scale=GUIDANCE,
            generator=torch.Generator(device="cpu").manual_seed(SEED),
            max_sequence_length=256,
        ).images[0]
        image.save(OUTPUT)
        RUN.write_text(
            json.dumps(
                {
                    "status": "review_required_not_character_pack_approved",
                    "purpose": "P7-5.2 style-pack-conditioned full-body character-master experiment",
                    "source_style_ledger": STYLE_LEDGER.name,
                    "source_style_run": source_record["run_id"],
                    "source_style_scene_id": STYLE_SCENE_ID,
                    "source_style_original": source.name,
                    "model": {
                        "id": MODEL_ID,
                        "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload",
                        "size": list(SIZE),
                        "steps": STEPS,
                        "guidance_scale": GUIDANCE,
                        "seed": SEED,
                    },
                    "prompt": PROMPT,
                    "output_image": OUTPUT.name,
                    "review_keys": [
                        "one complete body",
                        "face and hair color stability",
                        "clothing identity",
                        "line and watercolor style transfer",
                        "no frame, text, or unintended prop",
                    ],
                    "excluded_scope": ["turnaround expansion", "cutscene generation", "P7-5.3 approval"],
                    "elapsed_seconds": round(time.monotonic() - started, 1),
                    "gpu_memory_before_mib": before,
                    "gpu_memory_peak_mib": peak,
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

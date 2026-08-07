#!/usr/bin/env python3
"""Redraw an approved P7-5.3 storyboard as the approved P7-5.2 character."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import subprocess
import threading
from time import perf_counter, sleep

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ASSET_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = ASSET_DIR.parents[3]
DEFAULT_CACHE_DIR = PROJECT_ROOT / ".tmp" / "p7-5-3-flux2-klein-cache"
DEFAULT_OUTPUT_DIR = ASSET_DIR / "p7-5-3-flux2-storyboard-character-output"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
DEFAULT_STORYBOARD = ASSET_DIR / "p7-5-3-20260806-233009-animagine-run-03-seed-5413-storyboard.png"
DEFAULT_FACE = ASSET_DIR / "p7-5-2-face-turnaround-codeformer-front-2x.png"
DEFAULT_OUTFIT = ASSET_DIR / "p7-5-2-prop-reference-v2-complete-outfit-front-hip.png"
PROMPT = (
    "Redraw image 1 as one finished vertical Korean webtoon panel. Preserve its exact composition: "
    "one full-body dancer stands alone on an open flat floor in the center of a canyon; the left leg is lifted straight upward in front of the torso; "
    "the right leg is the only weight-bearing leg; both arms have the same open balancing gesture; the raised foot, supporting foot, all joints, and both hands are visible. "
    "The distant rock cliffs remain separated from the dancer. Replace the dancer with the exact adult Korean woman from images 2 and 3: "
    "a clean jaw-length teal-blue bob haircut with a smooth rounded silhouette, short blunt ends at the jaw, and a soft center part. "
    "She has dark brown eyes, a white cropped utility jacket over a charcoal crew-neck top, and teal high-waisted wide-leg trousers. "
    "The lifted left leg has loose teal trouser fabric with visible folds and a flared wide silhouette; a naturally visible ankle is allowed. "
    "Use plain white sneakers and exactly one navy rectangular flap crossbody bag at her right hip with one diagonal strap. "
    "Use clean restrained Korean webtoon line art, low-saturation flat colors, subtle fold shadows, readable face, correct anatomy, no text, and no watermark. "
    "Do not add people, duplicate limbs, extra bags, extra straps, cropped feet, floating body parts, exposed underwear, overlapping cliffs, or long hair."
)


def gpu_memory_mib() -> int | None:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        return int(result.stdout.strip())
    except ValueError:
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storyboard", type=Path, default=DEFAULT_STORYBOARD)
    parser.add_argument("--face-reference", type=Path, default=DEFAULT_FACE)
    parser.add_argument("--outfit-reference", type=Path, default=DEFAULT_OUTFIT)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--seed", type=int, default=5413)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=768)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_paths = {
        "storyboard": args.storyboard,
        "face": args.face_reference,
        "outfit": args.outfit_reference,
    }
    missing = [str(path) for path in input_paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing input files: " + ", ".join(missing))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = args.output_dir / f"{timestamp}-flux2-klein-4b-seed-{args.seed}.png"
    record_path = output_path.with_suffix(".json")
    before = gpu_memory_mib()
    peak = before or 0
    stop = threading.Event()

    def observe_peak() -> None:
        nonlocal peak
        while not stop.is_set():
            used = gpu_memory_mib()
            if used is not None:
                peak = max(peak, used)
            sleep(0.2)

    observer = threading.Thread(target=observe_peak, daemon=True)
    observer.start()
    started = perf_counter()
    try:
        pipe = Flux2KleinPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=args.cache_dir)
        pipe.enable_sequential_cpu_offload()
        references = [Image.open(path).convert("RGB") for path in input_paths.values()]
        image = pipe(
            image=references,
            prompt=PROMPT,
            width=args.width,
            height=args.height,
            num_inference_steps=args.steps,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(args.seed),
            max_sequence_length=256,
        ).images[0]
        image.save(output_path)
        record = {
            "status": "review_required",
            "model_id": MODEL_ID,
            "runtime": "Diffusers Flux2KleinPipeline sequential CPU offload",
            "inputs": {name: str(path) for name, path in input_paths.items()},
            "output_image": str(output_path),
            "prompt": PROMPT,
            "seed": args.seed,
            "size": [args.width, args.height],
            "steps": args.steps,
            "guidance_scale": 1.0,
            "elapsed_seconds": round(perf_counter() - started, 1),
            "gpu_memory_before_mib": before,
            "gpu_memory_peak_mib": peak,
        }
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(record, ensure_ascii=False, indent=2))
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

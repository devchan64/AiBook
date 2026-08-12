#!/usr/bin/env python3
"""Apply the approved P7-5.1 visual style to approved unstyled pose anchors.

This is Stage 2 of the character-LoRA data pipeline.  It receives an approved
Stage-1 pose PNG as the primary composition/identity input and one P7-5.1 style
reference as the rendering-only input.  It never changes or recreates poses.
"""

from __future__ import annotations

import argparse
import gc
import json
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image

from p7_5_image_output_naming import candidate_stem, preview_callback


ROOT = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
STYLE_REFERENCE = ROOT / "p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png"
DEFAULT_SEED = 62294
DEFAULT_STEPS = 6
IMAGE_SIZE = 1024


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", nargs="+", type=Path, required=True, help="Approved Stage-1 pose PNG paths.")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--preview-every", type=int, default=0)
    parser.add_argument("--output-prefix", default="p7-5-4-character-lora-pose-stage2")
    parser.add_argument("--plan-only", action="store_true")
    return parser.parse_args()


def source_path(path: Path) -> Path:
    if path.is_absolute() or path.is_file():
        return path
    return ROOT / path


def candidate_id(path: Path) -> str:
    return path.stem.removeprefix("p7-5-4-character-lora-pose-stage1-").removesuffix("-reference")


def build_prompt(source: Path) -> str:
    if "-rear-" in source.name:
        return (
            "Render the supplied full-body figure in restrained webtoon watercolor. "
            "Preserve the supplied figure's exact rear-facing pose, anatomy, clothing silhouette, and plain off-white studio background. "
            "Show a strict rear view with the back of the jaw-length bob, nape, shoulders, back, and back of the trousers facing the camera. "
            "Use the second supplied image only as the visual-style reference. One complete person with a clean rear silhouette."
        )
    return (
        "Render the supplied full-body figure in restrained webtoon watercolor. "
        "Preserve the supplied figure's exact pose, view, facial identity, anatomy, clothing silhouette, and plain off-white studio background. "
        "Preserve equal-sized orange-amber irises in both eyes. "
        "Use the second supplied image only as the visual-style reference. One person, no text or labels."
    )


def records(sources: list[Path], seed: int, steps: int) -> list[dict[str, object]]:
    if not STYLE_REFERENCE.is_file():
        raise FileNotFoundError(STYLE_REFERENCE)
    result: list[dict[str, object]] = []
    for source in sources:
        resolved = source_path(source)
        if not resolved.is_file():
            raise FileNotFoundError(resolved)
        if not resolved.name.startswith("p7-5-4-character-lora-pose-stage1-") or not resolved.name.endswith("-reference.png"):
            raise ValueError(f"Stage-2 inputs must be approved Stage-1 references: {resolved.name}")
        result.append(
            {
                "candidate_id": candidate_id(resolved),
                "stage": "style_stage_2",
                "source": resolved.name,
                "style_reference": STYLE_REFERENCE.name,
                "seed": seed,
                "steps": steps,
                "prompt": build_prompt(resolved),
            }
        )
    return result


def main() -> int:
    args = parse_args()
    if args.steps < 1 or args.preview_every < 0:
        raise ValueError("steps must be positive and preview-every must be zero or positive")
    entries = records(args.sources, args.seed, args.steps)
    if args.plan_only:
        print(json.dumps({"status": "validated", "count": len(entries), "candidates": entries}, ensure_ascii=False, indent=2))
        return 0
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache"
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    style_image = Image.open(STYLE_REFERENCE).convert("RGB")
    for entry in entries:
        stem = candidate_stem(
            f"{args.output_prefix}-{entry['candidate_id']}",
            seed=args.seed,
            steps=args.steps,
            contract={"model": MODEL_ID, **entry, "size": [IMAGE_SIZE, IMAGE_SIZE]},
        )
        output = ROOT / f"{stem}-candidate.png"
        review = ROOT / f"{stem}-review.json"
        started = time.monotonic()
        pose_image = Image.open(ROOT / str(entry["source"])).convert("RGB")
        image = pipe(
            image=[pose_image, style_image],
            prompt=str(entry["prompt"]),
            width=IMAGE_SIZE,
            height=IMAGE_SIZE,
            num_inference_steps=args.steps,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(args.seed),
            max_sequence_length=256,
            callback_on_step_end=preview_callback(
                pipe, height=IMAGE_SIZE, width=IMAGE_SIZE, every=args.preview_every,
                directory=ROOT / "previews", prefix=stem,
            ),
        ).images[0]
        image.save(output)
        payload = {
            "status": "review_required", "model": MODEL_ID, "image_size": [IMAGE_SIZE, IMAGE_SIZE],
            **entry, "output": output.name, "review": review.name,
            "elapsed_seconds": round(time.monotonic() - started, 2),
            "decision": "Stage-2 candidate only; require human approval before character-LoRA dataset inclusion.",
        }
        review.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{entry['candidate_id']}: {payload['elapsed_seconds']}s -> {output.name}", flush=True)
        gc.collect()
        torch.cuda.empty_cache()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

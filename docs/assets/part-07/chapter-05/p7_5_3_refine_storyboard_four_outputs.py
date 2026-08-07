#!/usr/bin/env python3
"""Test FLUX.2 character refinement with the four approved P7-5.3 storyboard outputs."""

from __future__ import annotations

import argparse
from datetime import datetime
import gc
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[3]
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
MODEL_CACHE = PROJECT_ROOT / ".tmp/p7-5-3-flux2-klein-cache"
BASE_SEED = 62377  # Keep P7-5.2 refinement's seed contract for the comparison.
IMAGE_WIDTH = 768
IMAGE_HEIGHT = 1152
STEPS = 12
GUIDANCE = 1.0
MAX_SEQUENCE_LENGTH = 256

STORYBOARD = ROOT / "p7-5-3-flux2-klein-storyboard-approved.png"
LINEART = ROOT / "p7-5-3-flux2-klein-storyboard-approved-guide-lineart.png"
CANNY = ROOT / "p7-5-3-flux2-klein-storyboard-approved-guide-canny.png"
DEPTH = ROOT / "p7-5-3-flux2-klein-storyboard-approved-guide-depth.png"
FACE_REFERENCE = ROOT / "p7-5-2-face-turnaround-codeformer-front-2x.png"
OUTFIT_FRONT = ROOT / "p7-5-2-prop-reference-v2-complete-outfit-front-hip.png"
OUTFIT_REAR = ROOT / "p7-5-2-prop-reference-v2-complete-outfit-rear-hip.png"


GUIDE_LABELS = {
    "storyboard": "the exact complete canyon storyboard panel",
    "lineart": "the storyboard lineart",
    "canny": "the storyboard Canny edges",
    "depth": "the storyboard relative-depth layout",
}


def background_prompt(guide_kind: str) -> str:
    if guide_kind == "depth":
        return (
            "Reference image 1 is the complete dressed dancer panel after the outfit stage. Preserve its dancer, clothing, bag, silhouette, raised left leg, planted right foot, arm order, and full-body framing. "
            "Reference image 2 is a relative-depth layout, not the final visible background. Use it only to correct the camera depth, narrow canyon walls, and floor recession. "
            "Render a complete natural-color pale sandstone-and-gravel canyon: tall craggy cliffs rise close at both sides and behind the dancer, with a narrow visible gap around her silhouette. "
            "The visible panel is the natural canyon scene with the dressed dancer, not a grayscale depth image. One person, complete limbs, no text or labels."
        )
    return (
        "Reference image 1 is the complete dressed dancer panel after the outfit stage. Preserve its dancer, clothing, bag, silhouette, raised leg, planted foot, arm placement, and full-body framing. "
        f"Reference image 2 is {GUIDE_LABELS[guide_kind]}; use it only to correct the canyon, camera, and spatial depth. "
        "Render a complete natural-color pale sandstone-and-gravel canyon with tall craggy cliffs and readable full-body anatomy. One person, complete limbs, no text or labels."
    )


def outfit_prompt(guide_kind: str) -> str:
    return (
        f"Reference image 1 is {GUIDE_LABELS[guide_kind]}. Use it to establish the camera, dancer silhouette, raised leg, planted foot, arm placement, spatial depth, and full-body framing. "
        "Reference images 2 and 3 define only a white cropped utility jacket over a charcoal-gray crop top, dark teal wide-leg trousers, and a navy crossbody bag. "
        "Render one adult dancer in that exact outfit and bag, with complete natural full-body anatomy, in a simple natural-color pale sandstone canyon. One person, complete limbs, no text or labels."
    )


def face_prompt() -> str:
    return (
        "Reference image 1 is the exact complete canyon panel after the background stage. Preserve its camera, canyon, dancer silhouette, raised leg, planted foot, arm placement, spatial depth, hair, clothing, and bag. "
        "Reference image 2 defines only the dancer's visible face identity from the frontal reference. "
        "Change only the visible face in reference image 1. Preserve its hair, clothing, bag, anatomy, limbs, lighting, and every other part of the panel. One person, no text or labels."
    )


def open_image(path: Path) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(path)
    return Image.open(path).convert("RGB")


def save(image: Image.Image, path: Path) -> Path:
    image.save(path)
    return path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="스토리보드 RGB·lineart·Canny·depth를 각각 단일 기준으로 비교하는 P7-5.3 캐릭터 정제 실험"
    )
    parser.add_argument("--storyboard", type=Path, default=STORYBOARD)
    parser.add_argument("--lineart", type=Path, default=LINEART)
    parser.add_argument("--canny", type=Path, default=CANNY)
    parser.add_argument("--depth", type=Path, default=DEPTH)
    parser.add_argument(
        "--guide-kinds",
        nargs="+",
        choices=tuple(GUIDE_LABELS),
        default=tuple(GUIDE_LABELS),
        help="같은 seed로 비교할 스토리보드 산출물 종류",
    )
    parser.add_argument("--seed", type=int, default=BASE_SEED)
    parser.add_argument("--stage", choices=("all", "background", "outfit", "face"), default="all")
    parser.add_argument("--intermediate", type=Path, help="background·face 단독 실행에 쓸 직전 단계 PNG")
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    parser.add_argument("--output-prefix", default="p7-5-3-four-output-character-refine")
    args = parser.parse_args()
    if args.stage in ("background", "face") and args.intermediate is None:
        raise ValueError("--stage background 또는 --stage face에는 --intermediate가 필요합니다.")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    guides = {
        "storyboard": open_image(args.storyboard),
        "lineart": open_image(args.lineart),
        "canny": open_image(args.canny),
        "depth": open_image(args.depth),
    }
    face_reference = open_image(FACE_REFERENCE)
    outfit_front = open_image(OUTFIT_FRONT)
    outfit_rear = open_image(OUTFIT_REAR)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=MODEL_CACHE,
        local_files_only=True,
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    timestamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%f%z")
    try:
        for guide_kind in args.guide_kinds:
            stem = f"{args.output_prefix}-{guide_kind}-{timestamp}-seed-{args.seed}"
            background_path = args.output_dir / f"{stem}-background-stage.png"
            outfit_path = args.output_dir / f"{stem}-outfit-stage.png"
            candidate_path = args.output_dir / f"{stem}-candidate.png"
            report_path = args.output_dir / f"{stem}-review.json"
            started = time.monotonic()
            if args.stage in ("all", "outfit"):
                outfit = pipe(
                    image=[guides[guide_kind], outfit_front, outfit_rear],
                    prompt=outfit_prompt(guide_kind),
                    width=IMAGE_WIDTH, height=IMAGE_HEIGHT, num_inference_steps=STEPS,
                    guidance_scale=GUIDANCE,
                    generator=torch.Generator(device="cpu").manual_seed(args.seed),
                    max_sequence_length=MAX_SEQUENCE_LENGTH,
                ).images[0]
                save(outfit, outfit_path)
                if args.stage == "outfit":
                    print(f"{guide_kind}: outfit-stage -> {outfit_path}")
                    continue
            else:
                outfit = open_image(args.intermediate)

            gc.collect()
            torch.cuda.empty_cache()
            if args.stage in ("all", "background"):
                background = pipe(
                    image=[outfit, guides[guide_kind]], prompt=background_prompt(guide_kind),
                    width=IMAGE_WIDTH,
                    height=IMAGE_HEIGHT,
                    num_inference_steps=STEPS,
                    guidance_scale=GUIDANCE,
                    generator=torch.Generator(device="cpu").manual_seed(args.seed + 1),
                    max_sequence_length=MAX_SEQUENCE_LENGTH,
                ).images[0]
                save(background, background_path)
                if args.stage == "background":
                    print(f"{guide_kind}: background-stage -> {background_path}")
                    continue
            else:
                background = open_image(args.intermediate)

            gc.collect()
            torch.cuda.empty_cache()
            candidate = pipe(
                image=[background, face_reference], prompt=face_prompt(),
                width=IMAGE_WIDTH,
                height=IMAGE_HEIGHT,
                num_inference_steps=STEPS,
                guidance_scale=GUIDANCE,
                generator=torch.Generator(device="cpu").manual_seed(args.seed + 2),
                max_sequence_length=MAX_SEQUENCE_LENGTH,
            ).images[0]
            save(candidate, candidate_path)
            elapsed = round(time.monotonic() - started, 2)
            report_path.write_text(
            json.dumps(
                {
                    "status": "review_required",
                    "output": candidate_path.name,
                    "guide_kind": guide_kind,
                    "seed": args.seed,
                    "image_size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                    "steps_per_stage": STEPS,
                    "elapsed_seconds": elapsed,
                    "model": MODEL_ID,
                    "guide_input": {"kind": guide_kind, "path": {"storyboard": args.storyboard, "lineart": args.lineart, "canny": args.canny, "depth": args.depth}[guide_kind].name},
                    "stages": {"outfit": outfit_prompt(guide_kind), "background": background_prompt(guide_kind), "face_final": face_prompt()},
                    "decision": "Review each guide's contribution to pose, canyon spacing, limb completeness, outfit geometry, and face identity before approval.",
                },
                indent=2,
            ),
            encoding="utf-8",
        )
            print(f"{guide_kind}: review candidate -> {candidate_path} ({elapsed:.2f}s)")
    finally:
        del pipe
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

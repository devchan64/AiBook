#!/usr/bin/env python3
"""Draw a P7-5.3 scene from an approved depth/RGB guide and one full-body reference."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image
from p7_5_image_output_naming import candidate_stem


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parents[3]
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
MODEL_CACHE = PROJECT_ROOT / ".tmp/p7-5-3-flux2-klein-cache"
BASE_SEED = 62944
DEFAULT_STEPS = 6
GUIDANCE = 1.0
MAX_SEQUENCE_LENGTH = 256

APPROVED_DEPTHS = {
    "A": ROOT / "p7-5-3-scene-a-approved-storyboard-depth.png",
    "B": ROOT / "p7-5-3-scene-b-approved-storyboard-depth.png",
    "C": ROOT / "p7-5-3-scene-c-approved-storyboard-depth.png",
}
APPROVED_RGB = {
    "A": ROOT / "p7-5-3-scene-a-approved-storyboard-rgb.png",
    "B": ROOT / "p7-5-3-scene-b-approved-storyboard-rgb.png",
    "C": ROOT / "p7-5-3-scene-c-approved-storyboard-rgb.png",
}
SCENE_BODY_REFERENCES = {
    "A": (ROOT / "p7-5-2-fullbody-front-quarter-left-refined-reference.png",),
    "B": (ROOT / "p7-5-2-fullbody-front-quarter-right-refined-reference.png",),
    "C": (ROOT / "p7-5-2-fullbody-front-reference.png",),
}
SCENE_DESCRIPTIONS = {
    "A": "a broad pale sandstone canyon with widely spaced craggy walls and a visible gravel floor",
    "B": "a vast open pale sandstone-and-gravel plain with a low horizon and small distant rocks, without nearby cliffs or walls",
    "C": "open pale sandstone gravel seen vertically from directly overhead, without a horizon, canyon, cliff, or wall",
}


def scene_prompt(scene_id: str, guide_type: str) -> str:
    guide_contract = (
        "Image 1 is a depth guide: render its single bright human silhouette as exactly one airborne woman, preserving its camera, scale, and limb pose. "
        if guide_type == "depth"
        else "Image 1 is the approved RGB storyboard: preserve its single airborne figure, camera, scale, limb pose, space, lighting, and shadows. "
    )
    return (
        guide_contract
        + "Image 2 supplies only her identity, short teal bob, white cropped jacket, gray crop top, wide dark trousers, white sneakers, and navy crossbody bag; do not copy its standing pose or background. "
        "Render her eyes, nose, and mouth clearly. Keep open air around both shoes, separated from the cliffs. Show part of the bag behind her hip. "
        f"Place her in {SCENE_DESCRIPTIONS[scene_id]}. Natural color."
    )


def open_image(path: Path) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(path)
    return Image.open(path).convert("RGB")


def write_review(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="승인 depth 또는 RGB와 방향별 전신 한 장을 참고해 P7-5.3 완성 RGB 장면을 그립니다."
    )
    parser.add_argument("--scene", choices=tuple(APPROVED_DEPTHS), default="A")
    parser.add_argument("--guide-type", choices=("depth", "rgb"), default="depth")
    guide_group = parser.add_mutually_exclusive_group()
    guide_group.add_argument("--guide", type=Path, help="선택한 guide 종류의 기본 승인 자산 대신 사용할 PNG")
    guide_group.add_argument("--depth", type=Path, help="기존 호환 옵션. 지정하면 --guide-type depth로 처리합니다.")
    parser.add_argument(
        "--body-references",
        type=Path,
        nargs="+",
        help="외형만 참고할 전신 PNG. 생략하면 장면 방향에 가까운 승인 리파인 전신 한 장을 사용합니다.",
    )
    parser.add_argument("--seed", type=int, default=BASE_SEED)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    parser.add_argument("--output-prefix", default="p7-5-3-storyboard-refine")
    args = parser.parse_args()
    guide_type = "depth" if args.depth else args.guide_type
    approved_guides = APPROVED_DEPTHS if guide_type == "depth" else APPROVED_RGB
    guide_path = args.depth or args.guide or approved_guides[args.scene]
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    guide_image = open_image(guide_path)
    body_reference_paths = tuple(args.body_references or SCENE_BODY_REFERENCES[args.scene])
    body_references = [open_image(path) for path in body_reference_paths]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    prompt = scene_prompt(args.scene, guide_type)
    stem_prefix = f"{args.output_prefix}-scene-{args.scene.lower()}"
    if guide_type == "rgb":
        stem_prefix = f"{args.output_prefix}-rgb-scene-{args.scene.lower()}"
    stem = candidate_stem(
        stem_prefix,
        seed=args.seed,
        steps=args.steps,
        contract={
            "model": MODEL_ID,
            "scene_id": args.scene,
            "guide_type": guide_type,
            "guide_input": guide_path.name,
            "body_reference_inputs": [path.name for path in body_reference_paths],
            "prompt": prompt,
            "steps": args.steps,
        },
    )
    scene_path = args.output_dir / f"{stem}-scene.png"
    report_path = args.output_dir / f"{stem}-review.json"

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=MODEL_CACHE,
        local_files_only=True,
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    try:
        started = time.monotonic()
        scene = pipe(
            image=[guide_image, *body_references],
            prompt=prompt,
            width=guide_image.width,
            height=guide_image.height,
            num_inference_steps=args.steps,
            guidance_scale=GUIDANCE,
            generator=torch.Generator(device="cpu").manual_seed(args.seed),
            max_sequence_length=MAX_SEQUENCE_LENGTH,
        ).images[0]
        scene.save(scene_path)
        elapsed = round(time.monotonic() - started, 2)
        write_review(
            report_path,
            {
                "status": "review_required",
                "output": scene_path.name,
                "model": MODEL_ID,
                "stage": "scene",
                "scene_id": args.scene,
                "seed": args.seed,
                "steps": args.steps,
                "image_size": [guide_image.width, guide_image.height],
                "guide_type": guide_type,
                "guide_input": guide_path.name,
                "depth_input": guide_path.name if guide_type == "depth" else None,
                "rgb_input": guide_path.name if guide_type == "rgb" else None,
                "body_reference_inputs": [path.name for path in body_reference_paths],
                "direct_face_reference": None,
                "direct_outfit_references": [],
                "prompt": prompt,
                "elapsed_seconds": elapsed,
                "decision": f"Review pose, camera, space, lighting, and shadows from the {guide_type} guide; identity and outfit from the full-body reference; and limb completeness.",
            },
        )
        print(f"scene {args.scene}: {guide_type} + full-body reference -> {scene_path} ({elapsed:.2f}s)")
    finally:
        del pipe
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Draw a P7-5.3 scene from approved depth and a refined character image."""

from __future__ import annotations

import argparse
import gc
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
BASE_SEED = 62944  # Keep P7-5.2 refinement's seed contract for the comparison.
IMAGE_WIDTH = 1152
IMAGE_HEIGHT = 1152
DEFAULT_STEPS = 3
GUIDANCE = 1.0
MAX_SEQUENCE_LENGTH = 256

STORYBOARD = ROOT / "p7-5-3-flux2-klein-storyboard-forward-leap-approved.png"
CANNY = ROOT / "p7-5-3-flux2-klein-storyboard-forward-leap-approved-guide-canny.png"
DEPTH = ROOT / "p7-5-3-flux2-klein-storyboard-forward-leap-approved-guide-depth.png"
APPROVED_DEPTHS = {
    "A": ROOT / "p7-5-3-scene-a-037414-seed-5420-s6-02-storyboard-depth.png",
    "B": ROOT / "p7-5-3-scene-b-088266-seed-5421-s6-02-storyboard-depth.png",
    "C": ROOT / "p7-5-3-scene-c-288128-seed-5422-s6-02-storyboard-depth.png",
}
CHARACTER_REFINE = ROOT / (
    "p7-5-3-refine-hypothesis-depth-character-depth-hash-eb58e6e519-"
    "seed-62377-steps-3-depth-character-stage.png"
)
FACE_REFERENCE = ROOT / "p7-5-2-face-front-reference.png"
OUTFIT_FRONT = ROOT / "p7-5-2-prop-reference-complete-outfit-front-hip.png"
OUTFIT_REAR = ROOT / "p7-5-2-prop-reference-complete-outfit-rear-hip.png"


GUIDE_LABELS = {
    "storyboard": "the exact complete canyon storyboard panel",
    "canny": "the storyboard Canny edges",
    "depth": "the storyboard relative-depth layout",
}

DEPTH_CHARACTER_HYPOTHESIS = (
    "A compact depth-only prompt can retain the airborne pose, approved identity, cropped wide-leg outfit, and plain background."
)

OUTFIT_DESCRIPTION = (
    "a white cropped utility jacket over a charcoal-gray crop top; deep teal high-waisted wide-leg trousers with the waistband at the navel, "
    "belt loops, a center fly, and roomy straight legs. Hems end 8 to 10 cm above the ankles. A navy crossbody bag sits at the left hip; "
    "one matching strap stays outside the jacket, from the right shoulder to the bag in front and from the right shoulder to beyond the left waistband at the back"
)

SCENE_DESCRIPTIONS = {
    "A": "a narrow pale sandstone canyon with tall craggy cliffs beside and behind the dancer and a visible gravel floor",
    "B": "a vast open pale sandstone-and-gravel plain with a low horizon and small distant rocks, without nearby cliffs or walls",
    "C": "open pale sandstone gravel seen vertically from directly overhead, without a horizon, canyon, cliff, or wall",
}


def scene_prompt(scene_id: str) -> str:
    return (
        "Reference image 1 is the approved relative-depth layout. Copy its camera, framing, dancer silhouette, limb count, pose, scale, and spatial depth. "
        "Reference image 2 is the approved refined character. Copy only her identity, dark teal bob, visible face, white cropped jacket, charcoal crop top, deep teal wide-leg trousers, navy crossbody bag, skin, and clothing details; do not copy its plain background or pose. "
        f"Draw one complete natural-color storyboard scene in {SCENE_DESCRIPTIONS[scene_id]}. "
        "The output must be a finished RGB scene, never a grayscale depth map. Exactly one full-body dancer, two arms, two legs, complete hands and feet, no text or labels."
    )


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
        f"Reference image 2 is {GUIDE_LABELS[guide_kind]}; use it only to correct the canyon and camera. "
        "Reference image 3 is a relative-depth layout; use it only to preserve the camera depth, canyon spacing, and floor recession. "
        "Render a complete natural-color pale sandstone-and-gravel canyon with tall craggy cliffs and readable full-body anatomy. One person, complete limbs, no text or labels."
    )


def outfit_prompt(guide_kind: str) -> str:
    if guide_kind == "depth":
        return (
            "Reference image 1 is a relative-depth layout. Use it only to establish the camera, dancer silhouette, spatial depth, and full-body framing. "
            f"Reference images 2 and 3 define only {OUTFIT_DESCRIPTION}. "
            "Render one adult dancer in that exact outfit and bag, with complete natural full-body anatomy, in a simple natural-color pale sandstone canyon. One person, complete limbs, no text or labels."
        )
    return (
        f"Reference image 1 is {GUIDE_LABELS[guide_kind]}. Use it to establish the camera, dancer silhouette, raised leg, planted foot, arm placement, spatial depth, and full-body framing. "
        "Reference image 2 is a relative-depth layout; use it only to preserve the camera depth and floor recession. "
        f"Reference images 3 and 4 define only {OUTFIT_DESCRIPTION}. "
        "Render one adult dancer in that exact outfit and bag, with complete natural full-body anatomy, in a simple natural-color pale sandstone canyon. One person, complete limbs, no text or labels."
    )


def depth_character_prompt() -> str:
    return (
        "Reference image 1 is a depth layout: copy only the airborne forward-leap silhouette and camera; ignore its background. "
        f"Reference images 2 and 3 define only {OUTFIT_DESCRIPTION}. "
        "Reference image 4 is the exact dancer: light warm skin, dark teal bob, amber eyes. Render her visible face, hands, and ankles; never a dark silhouette. "
        "One full-body dancer only, both feet airborne, on a flat pale-neutral background. No canyon, floor, scenery, shadows, text, or labels."
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


def write_review(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="승인 depth와 캐릭터 리파인 이미지를 참고해 P7-5.3 완성 장면 RGB를 그립니다."
    )
    parser.add_argument("--scene", choices=tuple(APPROVED_DEPTHS), default="A")
    parser.add_argument("--storyboard", type=Path, default=STORYBOARD)
    parser.add_argument("--canny", type=Path, default=CANNY)
    parser.add_argument("--depth", type=Path, help="생략하면 선택한 A/B/C씬의 승인 상대 depth를 사용합니다.")
    parser.add_argument(
        "--character-refine",
        type=Path,
        default=CHARACTER_REFINE,
        help="외형·얼굴·복장만 참고할 승인 캐릭터 리파인 PNG",
    )
    parser.add_argument(
        "--guide-kinds",
        nargs="+",
        choices=tuple(GUIDE_LABELS),
        default=("storyboard",),
        help="같은 seed로 비교할 스토리보드 산출물 종류",
    )
    parser.add_argument("--seed", type=int, default=BASE_SEED)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS, help="Denoising steps for each selected refinement stage.")
    parser.add_argument(
        "--stage",
        choices=("scene", "all", "depth-character", "background", "outfit", "face"),
        default="scene",
        help="기본 scene은 승인 depth와 캐릭터 리파인 이미지로 완성 RGB를 그립니다.",
    )
    parser.add_argument("--intermediate", type=Path, help="background·face 단독 실행에 쓸 직전 단계 PNG")
    parser.add_argument("--output-dir", type=Path, default=ROOT)
    parser.add_argument("--output-prefix", default="p7-5-3-storyboard-refine")
    args = parser.parse_args()
    args.depth = args.depth or APPROVED_DEPTHS[args.scene]
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if args.stage in ("background", "face") and args.intermediate is None:
        raise ValueError("--stage background 또는 --stage face에는 --intermediate가 필요합니다.")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    guide_paths = {
        "storyboard": args.storyboard,
        "canny": args.canny,
        "depth": args.depth,
    }
    run_guide_kinds = ("depth",) if args.stage in ("scene", "depth-character") else args.guide_kinds
    required_guides = set(run_guide_kinds)
    if any(guide_kind != "depth" for guide_kind in run_guide_kinds):
        required_guides.add("depth")
    guides = {guide_kind: open_image(guide_paths[guide_kind]) for guide_kind in required_guides}
    character_refine = open_image(args.character_refine) if args.stage == "scene" else None
    face_reference = open_image(FACE_REFERENCE) if args.stage != "scene" else None
    outfit_front = open_image(OUTFIT_FRONT) if args.stage != "scene" else None
    outfit_rear = open_image(OUTFIT_REAR) if args.stage != "scene" else None
    args.output_dir.mkdir(parents=True, exist_ok=True)

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir=MODEL_CACHE,
        local_files_only=True,
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    try:
        if args.stage == "scene":
            prompt = scene_prompt(args.scene)
            depth_image = guides["depth"]
            stem = candidate_stem(
                f"{args.output_prefix}-scene-{args.scene.lower()}",
                seed=args.seed,
                steps=args.steps,
                contract={
                    "model": MODEL_ID,
                    "stage": "scene",
                    "scene_id": args.scene,
                    "depth_input": args.depth.name,
                    "character_refine_input": args.character_refine.name,
                    "prompt": prompt,
                    "steps": args.steps,
                },
            )
            scene_path = args.output_dir / f"{stem}-scene.png"
            report_path = args.output_dir / f"{stem}-review.json"
            started = time.monotonic()
            scene = pipe(
                image=[depth_image, character_refine],
                prompt=prompt,
                width=depth_image.width,
                height=depth_image.height,
                num_inference_steps=args.steps,
                guidance_scale=GUIDANCE,
                generator=torch.Generator(device="cpu").manual_seed(args.seed),
                max_sequence_length=MAX_SEQUENCE_LENGTH,
            ).images[0]
            save(scene, scene_path)
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
                    "image_size": [depth_image.width, depth_image.height],
                    "depth_input": args.depth.name,
                    "character_refine_input": args.character_refine.name,
                    "prompt": prompt,
                    "elapsed_seconds": elapsed,
                    "decision": "Review camera and pose from depth, identity and outfit from character refine, limb completeness, and natural-color scene rendering.",
                },
            )
            print(f"scene {args.scene}: depth + character-refine -> {scene_path} ({elapsed:.2f}s)")
            return

        for guide_kind in run_guide_kinds:
            stem = candidate_stem(
                f"{args.output_prefix}-{guide_kind}",
                seed=args.seed,
                steps=args.steps,
                contract={
                    "model": MODEL_ID,
                    "guide_input": (
                        args.depth.name if args.stage == "depth-character" else guide_paths[guide_kind].name
                    ),
                    "depth_input": args.depth.name,
                    "face_input": FACE_REFERENCE.name if args.stage == "depth-character" else None,
                    "depth_character_prompt": depth_character_prompt(),
                    "outfit_prompt": outfit_prompt(guide_kind),
                    "background_prompt": background_prompt(guide_kind),
                    "face_prompt": face_prompt(),
                    "stage": args.stage,
                    "steps": args.steps,
                },
            )
            background_path = args.output_dir / f"{stem}-background-stage.png"
            depth_character_path = args.output_dir / f"{stem}-depth-character-stage.png"
            outfit_path = args.output_dir / f"{stem}-outfit-stage.png"
            candidate_path = args.output_dir / f"{stem}-candidate.png"
            report_path = args.output_dir / f"{stem}-review.json"
            started = time.monotonic()
            if args.stage == "depth-character":
                depth_character = pipe(
                    image=[guides["depth"], outfit_front, outfit_rear, face_reference],
                    prompt=depth_character_prompt(),
                    width=IMAGE_WIDTH,
                    height=IMAGE_HEIGHT,
                    num_inference_steps=args.steps,
                    guidance_scale=GUIDANCE,
                    generator=torch.Generator(device="cpu").manual_seed(args.seed),
                    max_sequence_length=MAX_SEQUENCE_LENGTH,
                ).images[0]
                save(depth_character, depth_character_path)
                elapsed = round(time.monotonic() - started, 2)
                write_review(
                    report_path,
                    {
                        "status": "review_required",
                        "output": depth_character_path.name,
                        "hypothesis": DEPTH_CHARACTER_HYPOTHESIS,
                        "seed": args.seed,
                        "steps": args.steps,
                        "depth_input": args.depth.name,
                        "face_input": FACE_REFERENCE.name,
                        "elapsed_seconds": elapsed,
                        "decision": "Review pose, visible identity, trouser width and hem height, strap path, and background removal.",
                    },
                )
                print(f"{guide_kind}: depth-character-stage -> {depth_character_path} ({elapsed:.2f}s)")
                continue

            if args.stage in ("all", "outfit"):
                outfit_inputs = [guides[guide_kind], outfit_front, outfit_rear]
                if guide_kind != "depth":
                    outfit_inputs.insert(1, guides["depth"])
                outfit = pipe(
                    image=outfit_inputs,
                    prompt=outfit_prompt(guide_kind),
                    width=IMAGE_WIDTH, height=IMAGE_HEIGHT, num_inference_steps=args.steps,
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
                background_inputs = [outfit, guides[guide_kind]]
                if guide_kind != "depth":
                    background_inputs.append(guides["depth"])
                background = pipe(
                    image=background_inputs, prompt=background_prompt(guide_kind),
                    width=IMAGE_WIDTH,
                    height=IMAGE_HEIGHT,
                    num_inference_steps=args.steps,
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
                num_inference_steps=args.steps,
                guidance_scale=GUIDANCE,
                generator=torch.Generator(device="cpu").manual_seed(args.seed + 2),
                max_sequence_length=MAX_SEQUENCE_LENGTH,
            ).images[0]
            save(candidate, candidate_path)
            elapsed = round(time.monotonic() - started, 2)
            write_review(
                report_path,
                {
                    "status": "review_required",
                    "output": candidate_path.name,
                    "guide_kind": guide_kind,
                    "seed": args.seed,
                    "image_size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                    "steps_per_stage": args.steps,
                    "elapsed_seconds": elapsed,
                    "model": MODEL_ID,
                    "guide_input": {"kind": guide_kind, "path": guide_paths[guide_kind].name},
                    "depth_input": args.depth.name,
                    "stages": {"outfit": outfit_prompt(guide_kind), "background": background_prompt(guide_kind), "face_final": face_prompt()},
                    "decision": "Review each guide's contribution to pose, canyon spacing, limb completeness, outfit geometry, and face identity before approval.",
                },
            )
            print(f"{guide_kind}: review candidate -> {candidate_path} ({elapsed:.2f}s)")
    finally:
        del pipe
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()

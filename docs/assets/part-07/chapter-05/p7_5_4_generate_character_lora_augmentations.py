#!/usr/bin/env python3
"""Generate unstyled character-pose candidates for the two-stage LoRA dataset.

Stage 1 follows the P7-5.2 full-body-turnaround method: an approved raw front
full-body anchor fixes the figure and clothing, while a directional sheet made
from approved raw face references fixes facial identity. The prompt asks only
for target pose and view. A separately reviewed Stage 2 applies the style.
Generated PNGs are never training inputs until a human separately approves
their review records.
"""

from __future__ import annotations

import argparse
import gc
import json
from dataclasses import asdict, dataclass
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image, ImageDraw
from p7_5_image_output_naming import candidate_stem, preview_callback


ROOT = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
BASE_SEED = 62294
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024
FACE_SHEET_PANEL_SIZE = 768
VIEWS = ("front", "front_quarter_left", "front_quarter_right", "profile_left", "profile_right", "rear")
VIEW_RULES = {
    "front": "front view facing the camera",
    "front_quarter_left": "left front-quarter view facing toward image left",
    "front_quarter_right": "right front-quarter view facing toward image right",
    "profile_left": "strict left side profile facing image left",
    "profile_right": "strict right side profile facing image right",
    "rear": "strict rear back-of-head view facing away from the camera",
}
RAW_FULLBODY_FRONT_REFERENCE = ROOT / "p7-5-2-fullbody-front-reference.png"
FACE_SHEET_BY_VIEW = {
    "front": (("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),),
    "front_quarter_left": (
        ("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),
        ("approved_left_front_quarter_face", ROOT / "p7-5-2-face-front-quarter-left-reference.png"),
        ("approved_left_profile_face", ROOT / "p7-5-2-face-profile-left-reference.png"),
    ),
    "front_quarter_right": (
        ("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),
        ("approved_right_front_quarter_face", ROOT / "p7-5-2-face-front-quarter-right-reference.png"),
        ("approved_right_profile_face", ROOT / "p7-5-2-face-profile-right-reference.png"),
    ),
    "profile_left": (
        ("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),
        ("approved_left_front_quarter_face", ROOT / "p7-5-2-face-front-quarter-left-reference.png"),
        ("approved_left_profile_face", ROOT / "p7-5-2-face-profile-left-reference.png"),
    ),
    "profile_right": (
        ("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),
        ("approved_right_front_quarter_face", ROOT / "p7-5-2-face-front-quarter-right-reference.png"),
        ("approved_right_profile_face", ROOT / "p7-5-2-face-profile-right-reference.png"),
    ),
    "rear": (
        ("approved_front_face", ROOT / "p7-5-2-face-front-reference.png"),
        ("approved_rear_face", ROOT / "p7-5-2-face-rear-reference.png"),
    ),
}
CONTACT_SHEET_CELL = (240, 360)
CONTACT_SHEET_LABEL_HEIGHT = 24


@dataclass(frozen=True)
class CandidateSpec:
    candidate_id: str
    view: str
    outfit_variant: str
    scene_id: str
    scene_rule: str
    pose_family: str
    pose_rule: str
    include_view_prompt: bool = True


def build_specs() -> tuple[CandidateSpec, ...]:
    sports_specs = (
        CandidateSpec(
            "sport-front-basketball-defense", "front", "basic", "basketball_court", "empty indoor court with a matte wood floor", "low_wide_defensive_pose", "Bend both knees deeply, hips at knee height, torso forward, arms spread wide with open hands.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-basketball-jump-shot", "front_quarter_left", "basic", "basketball_court", "empty indoor basketball court with a matte wood floor and a distant hoop", "basketball_jump_shot", "Jump vertically for a basketball jump shot; hold one basketball above the forehead with both hands, with both legs and shoes separately visible.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-tennis-forehand", "front_quarter_right", "basic", "tennis_court", "empty outdoor tennis court under clear daytime light", "one_hand_tennis_return", "With one hand, swing one tennis racket to return one ball toward image right; the other arm balances an athletic open stance.",
        ),
        CandidateSpec(
            "sport-profile_left-track-sprint", "profile_left", "basic", "running_track", "empty outdoor running track under clear daytime light", "track_sprint", "Sprint powerfully toward image left with a long running stride, opposite arm drive, and two separate shoes.",
        ),
        CandidateSpec(
            "sport-profile_right-soccer-pass", "profile_right", "basic", "soccer_field", "empty outdoor soccer practice field under clear daytime light", "soccer_pass", "Right-facing walking step: right foot planted ahead, left heel raised behind, weight on the right leg, and both arms swinging naturally in opposite directions.",
        ),
        CandidateSpec(
            "sport-rear-track-run", "rear", "basic", "running_track", "empty outdoor running track under clear daytime light", "rear_track_run", "Rear walking step: left foot planted, right foot lifted behind with the knee bent, weight on the left leg, and opposite elbows bent naturally.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-gymnastics-landing", "front_quarter_left", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "controlled_gymnastics_landing", "Controlled gymnastics landing: knees softly bent, arms raised in a V.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-boxing-jab", "front_quarter_left", "basic", "boxing_gym", "empty boxing gym with a clean practice ring and overhead daylight", "low_orthodox_boxing_jab", "Low orthodox boxing stance: both hands clenched into fists; throw one straight jab toward image left while the raised guard fist covers the face.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-volleyball-set", "front_quarter_right", "basic", "volleyball_court", "empty indoor volleyball court under even light", "high_angle_volleyball_set", "High-angle view: raise both hands to set one volleyball overhead in a low athletic stance.", include_view_prompt=False,
        ),
        CandidateSpec(
            "sport-profile_left-breaking-floor-pose", "profile_left", "basic", "breaking_floor", "empty breaking floor under even light", "high_angle_breaking_floor_pose", "Left-facing kneel: right knee on the ground, left foot planted forward, torso upright, and both hands resting on the raised left thigh.",
        ),
        CandidateSpec(
            "sport-profile_right-wrestling-shot", "profile_right", "basic", "wrestling_mat", "empty wrestling practice mat under even gym lighting", "wrestling_shot", "Right-facing deep lunge: right knee bent directly above the right ankle, left leg straight behind, left heel raised, torso upright, and hands on the right thigh.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-long-jump", "front_quarter_right", "basic", "athletics_runway", "empty athletics runway under even light", "long_jump_takeoff", "Long-jump takeoff: raised knee, trailing leg, balanced proportions.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-badminton-forehand", "front_quarter_right", "basic", "tennis_court", "empty indoor court under even light", "badminton_forehand", "Front-quarter side step toward image right: right foot planted sideways, left foot crossing behind, hips turned right, right hand on hip, left arm relaxed; empty hands.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-gymnastics-split-leap", "front_quarter_left", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_split_leap", "Perform a split leap toward image left with both legs extended in opposite directions and both arms lifted for balance.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-rugby-carry", "front_quarter_right", "basic", "rugby_field", "empty rugby field under even light", "rugby_carry", "Run toward image right carrying one rugby ball under one arm.",
        ),
        CandidateSpec(
            "sport-profile_left-gymnastics-arabesque", "profile_left", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_arabesque_left", "Left-facing knee lift: left foot planted, right knee lifted to hip height, torso upright, left hand on hip, and right arm relaxed down.",
        ),
        CandidateSpec(
            "sport-profile_right-gymnastics-lunge", "profile_right", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_lunge_right", "Right-facing seated squat: hips low, both feet flat and shoulder width apart, knees bent, torso upright, and both hands resting on the thighs.",
        ),
        CandidateSpec(
            "sport-rear-gymnastics-turn", "rear", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_turn_rear", "Rear weight shift: right foot planted, left toe touching the ground behind, hips shifted right, torso upright, and hands relaxed at the sides.",
        ),
    )
    extension_specs = (
        CandidateSpec(
            "sport-front_quarter_left-wrestling-stance", "front_quarter_left", "basic", "wrestling_mat", "empty wrestling mat under even light", "wrestling_stance", "Low wrestling stance, knees bent, open hands forward.",
        ),
        CandidateSpec(
            "sport-profile_right-gymnastics-floor-balance", "profile_right", "basic", "gymnastics_floor", "empty gymnastics floor under even light", "gymnastics_floor_balance_right", "Floor gymnastics balance on an empty floor: one leg back, arms wide, both white sneakers visible.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-track-acceleration", "front_quarter_left", "basic", "running_track", "empty running track under even light", "track_acceleration", "Sprint forward: one knee high, opposite arm forward.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-soccer-defensive-shuffle", "front_quarter_right", "basic", "soccer_field", "empty soccer field under even light", "soccer_defensive_shuffle", "Soccer defensive shuffle: knees bent, arms relaxed.",
        ),
        CandidateSpec(
            "sport-profile_left-track-start", "profile_left", "basic", "running_track", "empty outdoor running track under clear daytime light", "track_start", "Left-facing stride: left foot planted forward, right foot extended behind on its toe, left knee bent, torso leaning forward, and elbows bent in a running posture.",
        ),
        CandidateSpec(
            "sport-profile_right-boxing-duck", "profile_right", "basic", "boxing_gym", "empty boxing gym under even light", "boxing_duck", "Low side crouch toward image right: both feet grounded, knees bent, torso inclined forward, elbows bent, and both hands open beside the cheeks.",
        ),
        CandidateSpec(
            "sport-front-track-high-knees", "front", "basic", "running_track", "empty running track under even light", "track_high_knees", "High-knee running drill, one knee raised, opposite arm forward.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-volleyball-block", "front_quarter_left", "basic", "volleyball_court", "empty volleyball court under even light", "volleyball_block", "Volleyball block jump, both arms overhead.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-gymnastics-kneeling-presentation", "front_quarter_left", "basic", "gymnastics_floor", "empty gymnastics floor under even light", "gymnastics_kneeling_presentation", "Kneeling floor-gymnastics presentation, one knee down, arms open.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-gymnastics-presentation-lunge", "front_quarter_right", "basic", "gymnastics_floor", "empty gymnastics floor under even light", "gymnastics_presentation_lunge", "Front-quarter one-knee kneel: right knee on the ground, left foot planted forward, torso upright, right hand on hip, and left hand on the raised thigh.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-wrestling-single-leg", "front_quarter_left", "basic", "wrestling_mat", "empty wrestling practice mat under even gym lighting", "wrestling_single_leg_entry", "Practice a solo single-leg takedown entry toward image left with torso low, one knee bent, and both hands reaching forward.",
        ),
        CandidateSpec(
            "sport-rear-wrestling-bridge", "rear", "basic", "wrestling_mat", "empty wrestling practice mat under even gym lighting", "wrestling_bridge", "Rear wide side lunge: right knee bent, left leg straight sideways, both soles flat, torso upright, and hands resting on the right thigh.",
        ),
        CandidateSpec(
            "sport-front-gymnastics-squat", "front", "basic", "gymnastics_floor", "empty gymnastics floor under even light", "gymnastics_squat", "Gymnastics deep squat, arms forward, both white sneakers visible.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-judo-ready", "front_quarter_right", "basic", "wrestling_mat", "empty judo mat under even light", "judo_ready", "Judo ready stance, feet apart, knees softly bent, hands loose at the waist, both white sneakers visible.",
        ),
        CandidateSpec(
            "sport-profile_left-athletic-side-lunge", "profile_left", "basic", "wrestling_mat", "empty training mat under even light", "athletic_side_lunge", "Athletic side lunge toward image left, both feet grounded, knees bent, hands resting at the thighs, both white sneakers visible.",
        ),
        CandidateSpec(
            "sport-profile_right-gymnastics-leap", "profile_right", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_stag_leap", "Right-facing heel raise: left foot planted, right heel lifted behind with the knee bent, torso upright, left hand on hip, and right arm relaxed down.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-vertical-jump", "front_quarter_left", "basic", "gymnastics_floor", "empty training floor under even light", "vertical_jump", "Athletic vertical jump toward image left, arms raised, knees softly bent, both white sneakers visible.",
        ),
        CandidateSpec(
            "sport-rear-gymnastics-step-turn", "rear", "basic", "gymnastics_floor", "empty training floor under even light", "gymnastics_step_turn_rear", "Rear-view gymnastics step turn, feet staggered, one heel lifted, arms relaxed, both white sneakers visible.",
        ),
    )
    additional_pose_specs = (
        CandidateSpec("pose-extra-front-wide-squat", "front", "basic", "training_floor", "plain studio floor", "front_wide_squat", "Front wide squat: feet wider than shoulders, both soles flat, knees bent outward, hips low, torso upright, and hands resting on the thighs."),
        CandidateSpec("pose-extra-front-one-knee-kneel", "front", "basic", "training_floor", "plain studio floor", "front_one_knee_kneel", "Front one-knee kneel: right knee on the ground, left foot planted forward, torso upright, and both hands resting on the raised left thigh."),
        CandidateSpec("pose-extra-front-quarter-left-step", "front_quarter_left", "basic", "training_floor", "plain studio floor", "quarter_left_step", "Front-quarter left forward stride: left foot planted far ahead, right foot on its toe behind, left knee bent, torso leaning forward, and elbows bent naturally."),
        CandidateSpec("pose-extra-front-quarter-left-lunge", "front_quarter_left", "basic", "training_floor", "plain studio floor", "quarter_left_lunge", "Front-quarter left lunge: left knee bent above the ankle, right leg straight behind, both feet flat, torso upright, and hands on the left thigh."),
        CandidateSpec("pose-extra-front-quarter-right-knee-lift", "front_quarter_right", "basic", "training_floor", "plain studio floor", "quarter_right_knee_lift", "Front-quarter right knee lift: right foot planted, left knee raised to hip height, torso upright, right hand on hip, and left arm relaxed down."),
        CandidateSpec("pose-extra-front-quarter-right-side-step", "front_quarter_right", "basic", "training_floor", "plain studio floor", "quarter_right_side_step", "Front-quarter right side lunge: right knee bent deeply above the ankle, left leg straight sideways, both soles flat, torso upright, and hands on the right thigh."),
        CandidateSpec("pose-extra-profile-left-kneel", "profile_left", "basic", "training_floor", "plain studio floor", "profile_left_kneel", "Left-facing low kneel: left knee on the ground, right foot planted forward, hips lowered, torso upright, and both hands on the raised right thigh."),
        CandidateSpec("pose-extra-profile-left-weight-shift", "profile_left", "basic", "training_floor", "plain studio floor", "profile_left_weight_shift", "Left-facing knee lift: left foot planted, right knee raised to hip height, torso upright, left hand on hip, and right arm relaxed down."),
        CandidateSpec("pose-extra-profile-right-half-squat", "profile_right", "basic", "training_floor", "plain studio floor", "profile_right_half_squat", "Right-facing deep squat: feet wider than shoulders, both soles flat, hips low, knees bent outward, torso upright, and hands on the thighs."),
        CandidateSpec("pose-extra-profile-right-stride", "profile_right", "basic", "training_floor", "plain studio floor", "profile_right_stride", "Right-facing forward lunge: right knee bent directly above the ankle, left leg straight behind, left heel raised, torso upright, and hands on the right thigh."),
        CandidateSpec("pose-extra-rear-side-lunge", "rear", "basic", "training_floor", "plain studio floor", "rear_side_lunge", "Rear wide squat: feet wider than shoulders, both soles flat, hips low, knees bent outward, torso upright, and hands on the thighs."),
        CandidateSpec("pose-extra-rear-heel-lift", "rear", "basic", "training_floor", "plain studio floor", "rear_heel_lift", "Rear staggered lunge: left foot planted forward, right foot on its toe behind, left knee bent, torso upright, and hands resting on the left thigh."),
    )
    return sports_specs + extension_specs + additional_pose_specs


SPECS = build_specs()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", nargs="+", choices=tuple(spec.candidate_id for spec in SPECS), default=tuple(spec.candidate_id for spec in SPECS))
    parser.add_argument("--seed", type=int, default=BASE_SEED)
    parser.add_argument(
        "--seed-step",
        type=int,
        default=0,
        help="Seed increment between targets; 0 keeps every candidate on the approved identity seed.",
    )
    parser.add_argument("--steps", type=int, default=6)
    parser.add_argument("--preview-every", type=int, default=0)
    parser.add_argument("--front-image", type=Path, default=RAW_FULLBODY_FRONT_REFERENCE, help="Approved raw front full-body PNG used as the fixed pose anchor.")
    parser.add_argument("--output-prefix", default="p7-5-4-character-lora-pose-stage1")
    parser.add_argument("--plan-only", action="store_true", help="Validate the raw turnaround anchor and face-sheet inputs, then print the selected Stage-1 plan.")
    parser.add_argument(
        "--contact-sheet-images",
        nargs="+",
        type=Path,
        help="Create a 3-column review contact sheet from already generated candidate PNG paths; no GPU is used.",
    )
    return parser.parse_args()


def prompt_word_count(text: str) -> int:
    return len(text.split())


def square_panel(image: Image.Image) -> Image.Image:
    """Fit one approved face PNG into a common white panel."""
    source = image.convert("RGB")
    source.thumbnail((FACE_SHEET_PANEL_SIZE, FACE_SHEET_PANEL_SIZE), Image.Resampling.LANCZOS)
    panel = Image.new("RGB", (FACE_SHEET_PANEL_SIZE, FACE_SHEET_PANEL_SIZE), "white")
    panel.paste(source, ((FACE_SHEET_PANEL_SIZE - source.width) // 2, (FACE_SHEET_PANEL_SIZE - source.height) // 2))
    return panel


def build_face_reference_sheet(face_images: tuple[Image.Image, ...]) -> Image.Image:
    """Place 5.2 directional face anchors side-by-side, as in the turnaround generator."""
    sheet = Image.new("RGB", (FACE_SHEET_PANEL_SIZE * len(face_images), FACE_SHEET_PANEL_SIZE), "white")
    for index, face_image in enumerate(face_images):
        sheet.paste(square_panel(face_image), (FACE_SHEET_PANEL_SIZE * index, 0))
    return sheet


def build_prompt(spec: CandidateSpec) -> str:
    view_clause = f"{VIEW_RULES[spec.view]}, " if spec.include_view_prompt else ""
    return (
        "Use the supplied front full-body reference as the fixed source for the entire figure and pose change. "
        "Use the supplied ordered face sheet to preserve the same face and hair across its front and target-direction panels. "
        f"Render the same full-body figure, {view_clause}{spec.pose_rule} "
        "Preserve full-body proportion, clothing silhouette, and the plain off-white studio background. "
        "One person, complete limbs, no text or labels."
    )


def planned_records(targets: tuple[str, ...], seed: int, seed_step: int, steps: int, front_image: Path) -> list[dict[str, object]]:
    selected = [spec for spec in SPECS if spec.candidate_id in targets]
    records: list[dict[str, object]] = []
    for index, spec in enumerate(selected):
        face_sheet_sources = [path for _, path in FACE_SHEET_BY_VIEW[spec.view]]
        references = [front_image, RAW_FULLBODY_FRONT_REFERENCE, *face_sheet_sources]
        if missing := [path.name for path in references if not path.is_file()]:
            raise FileNotFoundError(", ".join(missing))
        prompt = build_prompt(spec)
        records.append(
            {
                **asdict(spec),
                "seed": seed + index * seed_step,
                "steps": steps,
                "stage": "pose_stage_1_unstyled",
                "front_anchor_reference": front_image.name,
                "fullbody_reference": RAW_FULLBODY_FRONT_REFERENCE.name,
                "face_sheet": {
                    "panel_order": [label for label, _ in FACE_SHEET_BY_VIEW[spec.view]],
                    "sources": [path.name for path in face_sheet_sources],
                    "size": [FACE_SHEET_PANEL_SIZE * len(face_sheet_sources), FACE_SHEET_PANEL_SIZE],
                },
                "prompt": prompt,
                "prompt_word_count": prompt_word_count(prompt),
            }
        )
    return records


def write_contact_sheet(paths: list[Path], output_prefix: str) -> Path:
    if not paths:
        raise ValueError("at least one candidate PNG is required for a contact sheet")
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(", ".join(missing))
    cell_width, cell_height = CONTACT_SHEET_CELL
    columns = 3
    rows = (len(paths) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_width, rows * (cell_height + CONTACT_SHEET_LABEL_HEIGHT)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, path in enumerate(paths):
        image = Image.open(path).convert("RGB")
        image.thumbnail(CONTACT_SHEET_CELL, Image.Resampling.LANCZOS)
        column, row = index % columns, index // columns
        left, top = column * cell_width, row * (cell_height + CONTACT_SHEET_LABEL_HEIGHT)
        sheet.paste(image, (left + (cell_width - image.width) // 2, top + (cell_height - image.height) // 2))
        candidate_id = path.name.split("-code-", maxsplit=1)[0].removeprefix(
            f"{output_prefix}-"
        )
        label = f"{index + 1:02d}"
        draw.text((left + 5, top + cell_height + 4), label, fill="black")
    output = ROOT / f"{output_prefix}-review-contact-sheet.png"
    sheet.save(output)
    return output


def main() -> int:
    args = parse_args()
    if args.contact_sheet_images:
        output = write_contact_sheet(args.contact_sheet_images, args.output_prefix)
        print(json.dumps({"status": "contact_sheet_created", "output": output.name, "count": len(args.contact_sheet_images)}, ensure_ascii=False))
        return 0
    if args.steps < 1 or args.preview_every < 0:
        raise ValueError("steps must be positive and preview-every must be zero or positive")
    records = planned_records(
        tuple(args.targets), args.seed, args.seed_step, args.steps, args.front_image
    )
    if args.plan_only:
        print(json.dumps({"status": "validated", "count": len(records), "candidates": records}, ensure_ascii=False, indent=2))
        return 0
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for candidate generation")

    pipe = Flux2KleinPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache")
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    front_anchor_image = Image.open(args.front_image).convert("RGB")
    fullbody_reference_image = Image.open(RAW_FULLBODY_FRONT_REFERENCE).convert("RGB")
    face_images = {
        path: Image.open(path).convert("RGB")
        for record in records
        for path in (ROOT / source for source in record["face_sheet"]["sources"])
    }
    face_sheets = {
        view: build_face_reference_sheet(
            tuple(face_images[path] for _, path in FACE_SHEET_BY_VIEW[view])
        )
        for view in {str(record["view"]) for record in records}
    }
    generated: list[dict[str, object]] = []
    for record in records:
        stem = candidate_stem(
            f"{args.output_prefix}-{record['candidate_id']}",
            seed=int(record["seed"]),
            steps=args.steps,
            contract={"model": MODEL_ID, **record, "size": [IMAGE_WIDTH, IMAGE_HEIGHT]},
        )
        output, review = ROOT / f"{stem}-candidate.png", ROOT / f"{stem}-review.json"
        started = time.monotonic()
        image = pipe(
            image=[
                front_anchor_image,
                fullbody_reference_image,
                face_sheets[str(record["view"])],
            ],
            prompt=str(record["prompt"]),
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT,
            num_inference_steps=args.steps,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(int(record["seed"])),
            max_sequence_length=256,
            callback_on_step_end=preview_callback(pipe, height=IMAGE_HEIGHT, width=IMAGE_WIDTH, every=args.preview_every, directory=ROOT / "previews", prefix=stem),
        ).images[0]
        image.save(output)
        result = {**record, "status": "review_required", "output": output.name, "review": review.name, "elapsed_seconds": round(time.monotonic() - started, 2)}
        review.write_text(
            json.dumps(
                {
                    "model": MODEL_ID,
                    "image_size": [IMAGE_WIDTH, IMAGE_HEIGHT],
                    **result,
                    "hard_fail_conditions": [
                        "The figure does not show exactly two arms, two hands, two legs, and two feet.",
                        "Any limb, hand, or foot is extra, missing, fused, duplicated, or cropped.",
                        "Any visible hand does not show five separate fingers including the thumb.",
                        "The pose, view, face identity, or clothing silhouette does not match the supplied Stage-1 references.",
                    ],
                    "decision": "Stage-1 candidate only; require human approval before Stage-2 style application and LoRA dataset inclusion.",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        generated.append(result)
        print(f"{record['candidate_id']}: {result['elapsed_seconds']}s -> {output.name}", flush=True)
        gc.collect()
        torch.cuda.empty_cache()
    print(json.dumps({"status": "generated", "count": len(generated), "outputs": [record["output"] for record in generated]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate style-conditioned sports-action candidates for character-LoRA data.

The six basic and six refined approved full-body references are direct LoRA
inputs and are never regenerated here. Each new candidate uses one directional
face plus a matching basic body for identity, proportion, and outfit
construction, and an approved P7-5.1 background image for the rendering style.
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
VIEWS = ("front", "front_quarter_left", "front_quarter_right", "profile_left", "profile_right", "rear")
VIEW_RULES = {
    "front": "front view facing the camera",
    "front_quarter_left": "left front-quarter view facing toward image left",
    "front_quarter_right": "right front-quarter view facing toward image right",
    "profile_left": "strict left side profile facing image left",
    "profile_right": "strict right side profile facing image right",
    "rear": "strict rear back-of-head view facing away from the camera",
}
FACE_REFERENCE_BY_VIEW = {
    view: ROOT / f"p7-5-2-face-{view.replace('_', '-')}-reference.png" for view in VIEWS
}
CHARACTER_IDENTITY_CONTRACT_PATH = ROOT / "p7-5-2-character-identity-contract.json"
CHARACTER_IDENTITY_CONTRACT = json.loads(
    CHARACTER_IDENTITY_CONTRACT_PATH.read_text(encoding="utf-8")
)
BASIC_BODY_BY_VIEW = {
    view: ROOT / f"p7-5-2-fullbody-{view.replace('_', '-')}-reference.png" for view in VIEWS
}
REFINED_BODY_BY_VIEW = {
    view: ROOT / f"p7-5-2-fullbody-{view.replace('_', '-')}-refined-reference.png" for view in VIEWS
}
STYLE_REFERENCE_BY_SCENE = {
    "basketball_court": ROOT / "p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png",
    "boxing_gym": ROOT / "p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png",
    "wrestling_mat": ROOT / "p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png",
    "gymnastics_floor": ROOT / "p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png",
    "tennis_court": ROOT / "p7-5-1-style-downtown-clear-day-wide-local-gpu-v1.png",
    "running_track": ROOT / "p7-5-1-style-downtown-clear-day-wide-local-gpu-v1.png",
    "soccer_field": ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png",
    "volleyball_court": ROOT / "p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png",
    "breaking_floor": ROOT / "p7-5-1-style-downtown-clear-day-wide-local-gpu-v1.png",
    "fencing_piste": ROOT / "p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png",
    "athletics_runway": ROOT / "p7-5-1-style-downtown-clear-day-wide-local-gpu-v1.png",
    "rugby_field": ROOT / "p7-5-1-style-downtown-clear-day-wide-local-gpu-v1.png",
}
BASE_OUTFIT = "charcoal-gray cropped crew-neck top, narrow bare-midriff gap, deep teal wide-leg trousers, and white low-top sneakers"
REFINED_OUTFIT = (
    "white cropped utility jacket over the charcoal-gray crop top, narrow bare-midriff gap, deep teal wide-leg trousers, "
    "white low-top sneakers, and one deep-navy crossbody messenger bag with its single strap outside the jacket"
)
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
            "sport-profile_right-soccer-pass", "profile_right", "basic", "soccer_field", "empty outdoor soccer practice field under clear daytime light", "soccer_pass", "Pass one soccer ball toward image right: plant one foot, swing the other leg forward, and keep both arms, hands, legs, feet, and the ball readable.",
        ),
        CandidateSpec(
            "sport-rear-track-run", "rear", "basic", "running_track", "empty outdoor running track under clear daytime light", "rear_track_run", "Rear running mid-stride: one foot lifted, the other planted, with strong opposite-arm drive.",
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
            "sport-profile_left-breaking-floor-pose", "profile_left", "basic", "breaking_floor", "empty breaking floor under even light", "high_angle_breaking_floor_pose", "High-angle view: hold a low breaking floor pose, one hand supporting and legs extended.", include_view_prompt=False,
        ),
        CandidateSpec(
            "sport-profile_right-wrestling-shot", "profile_right", "basic", "wrestling_mat", "empty wrestling practice mat under even gym lighting", "wrestling_shot", "Practice a solo double-leg wrestling shot toward image right: one knee deeply bent, torso low, both arms reaching forward.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-long-jump", "front_quarter_right", "basic", "athletics_runway", "empty athletics runway under even light", "long_jump_takeoff", "Long-jump takeoff: raised knee, trailing leg, balanced proportions.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-badminton-forehand", "front_quarter_right", "basic", "tennis_court", "empty indoor court under even light", "badminton_forehand", "Hit one shuttlecock with one badminton racket in a balanced forehand toward image right.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-gymnastics-split-leap", "front_quarter_left", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_split_leap", "Perform a split leap toward image left with both legs extended in opposite directions and both arms lifted for balance.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-rugby-carry", "front_quarter_right", "basic", "rugby_field", "empty rugby field under even light", "rugby_carry", "Run toward image right carrying one rugby ball under one arm.",
        ),
        CandidateSpec(
            "sport-profile_left-gymnastics-arabesque", "profile_left", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_arabesque_left", "Hold a floor-gymnastics arabesque toward image left: balance on one straight leg, extend the other leg behind, and extend both arms for balance.",
        ),
        CandidateSpec(
            "sport-profile_right-gymnastics-lunge", "profile_right", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_lunge_right", "Hold a deep gymnastics presentation lunge toward image right with one knee bent, rear leg straight, and both arms lifted overhead.",
        ),
        CandidateSpec(
            "sport-rear-gymnastics-turn", "rear", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_turn_rear", "Rear one-foot gymnastics pivot: raised knee, arms wide, white sneakers.",
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
            "sport-front_quarter_left-tennis-backhand", "front_quarter_left", "basic", "tennis_court", "empty outdoor tennis court under clear daytime light", "tennis_backhand", "Make a two-handed tennis backhand toward image left with a stable split stance, one racket, and both feet separately visible.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-tennis-serve", "front_quarter_right", "basic", "tennis_court", "empty outdoor tennis court under clear daytime light", "tennis_serve", "Perform a tennis serve preparation toward image right: toss one ball upward and raise one racket, keeping both arms and both feet readable.",
        ),
        CandidateSpec(
            "sport-profile_left-track-start", "profile_left", "basic", "running_track", "empty outdoor running track under clear daytime light", "track_start", "Hold a track sprint start toward image left with one knee forward, the rear foot braced, and both hands near the ground with both feet fully visible.",
        ),
        CandidateSpec(
            "sport-profile_right-track-hurdle", "profile_right", "basic", "running_track", "empty outdoor running track under clear daytime light", "track_hurdle", "Clear one low track hurdle toward image right with a lead leg extended, trail leg bent, and natural opposite-arm balance.",
        ),
        CandidateSpec(
            "sport-front-soccer-dribble", "front", "basic", "soccer_field", "empty outdoor soccer practice field under clear daytime light", "soccer_dribble", "Control one soccer ball in a front-facing dribble with a slight knee bend, one foot beside the ball, and both arms naturally balancing.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-soccer-volley", "front_quarter_left", "basic", "soccer_field", "empty outdoor soccer practice field under clear daytime light", "soccer_volley", "Strike one airborne soccer ball in a controlled volley toward image left, with one planted foot, one lifted leg, and both arms for balance.",
        ),
        CandidateSpec(
            "sport-front-boxing-dodge", "front", "basic", "boxing_gym", "empty boxing gym with a clean practice ring and overhead daylight", "boxing_dodge", "Hold a low solo boxing slip with both fists guarding, torso angled, knees bent, and two clearly separated feet.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-boxing-uppercut", "front_quarter_right", "basic", "boxing_gym", "empty boxing gym with a clean practice ring and overhead daylight", "boxing_uppercut", "Throw one compact solo boxing uppercut toward image right while the other hand protects the face and the stance stays grounded.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-wrestling-single-leg", "front_quarter_left", "basic", "wrestling_mat", "empty wrestling practice mat under even gym lighting", "wrestling_single_leg_entry", "Practice a solo single-leg takedown entry toward image left with torso low, one knee bent, and both hands reaching forward.",
        ),
        CandidateSpec(
            "sport-rear-wrestling-bridge", "rear", "basic", "wrestling_mat", "empty wrestling practice mat under even gym lighting", "wrestling_bridge", "Hold a solo wrestling bridge from the rear with shoulders and feet grounded, hips raised, and both arms visible for balance in a back-of-head view.",
        ),
        CandidateSpec(
            "sport-front-gymnastics-handstand", "front", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_handstand", "Hold a straight floor-gymnastics handstand facing the camera with both hands on the floor, both legs together overhead, and both shoes visible.",
        ),
        CandidateSpec(
            "sport-front_quarter_right-gymnastics-roundoff", "front_quarter_right", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_roundoff", "Perform a controlled floor-gymnastics roundoff toward image right with both hands approaching the floor and both legs clearly separated through the motion.",
        ),
        CandidateSpec(
            "sport-profile_left-gymnastics-balance", "profile_left", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_scale_balance", "Hold a floor-gymnastics scale balance toward image left: one supporting leg, the other extended behind, torso forward, and both arms extended for balance.",
        ),
        CandidateSpec(
            "sport-profile_right-gymnastics-leap", "profile_right", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_stag_leap", "Perform a controlled stag leap toward image right with one knee bent forward, the other leg extended behind, and both arms lifted for balance.",
        ),
        CandidateSpec(
            "sport-front_quarter_left-gymnastics-floor-pose", "front_quarter_left", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_floor_presentation", "Hold a kneeling floor-gymnastics presentation toward image left with one knee on the floor, the other foot planted, and both arms in a clean open line.",
        ),
        CandidateSpec(
            "sport-rear-gymnastics-finish", "rear", "basic", "gymnastics_floor", "empty gymnastics floor with a blue spring floor and bright indoor light", "gymnastics_finish_rear", "Hold a standing floor-gymnastics finish from the rear with both arms raised and feet apart in a back-of-head view.",
        ),
    )
    return sports_specs + extension_specs


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
    parser.add_argument("--output-prefix", default="p7-5-4-character-lora-augmentation")
    parser.add_argument("--plan-only", action="store_true", help="Validate approved identity, body, and style inputs and print the selected generation plan.")
    parser.add_argument(
        "--contact-sheet-images",
        nargs="+",
        type=Path,
        help="Create a 3-column review contact sheet from already generated candidate PNG paths; no GPU is used.",
    )
    return parser.parse_args()


def prompt_word_count(text: str) -> int:
    return len(text.split())


def body_reference(spec: CandidateSpec) -> Path:
    return BASIC_BODY_BY_VIEW[spec.view] if spec.outfit_variant == "basic" else REFINED_BODY_BY_VIEW[spec.view]


def build_prompt(spec: CandidateSpec) -> str:
    view_clause = f"{VIEW_RULES[spec.view]}, " if spec.include_view_prompt else ""
    return (
        f"Full-body woman, {view_clause}isolated on a plain off-white background. Webtoon watercolor. "
        f"{CHARACTER_IDENTITY_CONTRACT['lora_eye_identity_description']} "
        f"{CHARACTER_IDENTITY_CONTRACT['lora_hair_identity_description']} "
        f"{CHARACTER_IDENTITY_CONTRACT['lora_fullbody_proportion_description']} "
        f"{spec.pose_rule} "
        "Natural anatomy."
    )


def planned_records(targets: tuple[str, ...], seed: int, seed_step: int, steps: int) -> list[dict[str, object]]:
    selected = [spec for spec in SPECS if spec.candidate_id in targets]
    records: list[dict[str, object]] = []
    for index, spec in enumerate(selected):
        face, body, style = FACE_REFERENCE_BY_VIEW[spec.view], body_reference(spec), STYLE_REFERENCE_BY_SCENE[spec.scene_id]
        if missing := [path.name for path in (face, body, style) if not path.is_file()]:
            raise FileNotFoundError(", ".join(missing))
        prompt = build_prompt(spec)
        records.append(
            {
                **asdict(spec),
                "seed": seed + index * seed_step,
                "steps": steps,
                "face_reference": face.name,
                "character_identity_contract": CHARACTER_IDENTITY_CONTRACT_PATH.name,
                "body_reference": body.name,
                "style_reference": style.name,
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
        label = path.name.split("-code-", maxsplit=1)[0].removeprefix(f"{output_prefix}-")
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
    records = planned_records(tuple(args.targets), args.seed, args.seed_step, args.steps)
    if args.plan_only:
        print(json.dumps({"status": "validated", "count": len(records), "candidates": records}, ensure_ascii=False, indent=2))
        return 0
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for candidate generation")

    pipe = Flux2KleinPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache")
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    generated: list[dict[str, object]] = []
    for record in records:
        face_path = ROOT / str(record["face_reference"])
        body_path = ROOT / str(record["body_reference"])
        style_path = ROOT / str(record["style_reference"])
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
                Image.open(face_path).convert("RGB"),
                Image.open(body_path).convert("RGB"),
                Image.open(style_path).convert("RGB"),
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
                        "The rendering style does not match the approved P7-5.1 restrained-webtoon watercolor style contract.",
                        "The visible face does not match the shared face-identity contract, including its chestnut-brown and orange-amber iris rule.",
                    ],
                    "decision": "Candidate only; require human approval before LoRA dataset inclusion.",
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

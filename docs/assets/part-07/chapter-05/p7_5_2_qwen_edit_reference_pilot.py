#!/usr/bin/env python3
"""Create review-only Qwen Edit candidates for the P7-5.2 front anchors.

Approved P7-5.2 reference PNGs remain immutable during this pilot. This script
writes a separate candidate PNG and run record; it never changes a stable
reference, manifest, or approval status.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
import time
from pathlib import Path

import torch
from diffusers import QwenImageEditPlusPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel
from PIL import Image, ImageDraw


ASSETS = Path(__file__).resolve().parent
PLAN = ASSETS / "p7-5-2-qwen-edit-transition-plan.json"
IDENTITY_CONTRACT = ASSETS / "p7-5-2-character-identity-contract.json"
STYLE_CONTRACT = ASSETS / "p7-5-2-character-reference-style-prompt-contract.json"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
OUTPUT_DIR = ASSETS / "p7-5-2-qwen-edit-candidates"
DEFAULT_STEPS = 20
QWEN_FACE_REFERENCE = "p7-5-2-face-front-qwen-role-separated-reference.png"
OPENPOSE_GUIDES = {
    "face_front_quarter_left": "p7-5-2-openpose-face-quarter-left-declarative-guide.png",
    "face_front_quarter_right": "p7-5-2-openpose-face-quarter-right-declarative-guide.png",
    "face_profile_left": "p7-5-2-openpose-face-profile-left-declarative-guide.png",
    "face_profile_right": "p7-5-2-openpose-face-profile-right-declarative-guide.png",
    "face_rear": "p7-5-2-openpose-face-rear-declarative-guide.png",
}
HAIR_VOLUME_RULE = (
    "Preserve a high-volume crown and a wide rounded jaw-length bob silhouette: medium-density petrol-teal hair, "
    "large loose S-waves, pronounced inward C-curls at both ends, and tapered side locks that stay visibly wider than the neck."
)

TARGETS = {
    "face_front": {
        "inputs": ("p7-5-2-face-front-reference.png",),
        "size": (768, 768),
        "prompt": (
            "Use image 1 only as the exact front-face identity reference. Preserve its compact oval face, "
            "petrol-teal jaw-length bob, and long slender almond eyes with gently upturned outer corners, moderately narrow "
            "eyelid openings, and equal orange-amber irises. "
            f"{HAIR_VOLUME_RULE} Create one clean strict frontal head-and-neck "
            "studio reference. No text, panel, collage, accessory, or background scene."
        ),
    },
    "fullbody_front_refined": {
        "inputs": (
            "p7-5-2-fullbody-front-refined-reference.png",
            QWEN_FACE_REFERENCE,
        ),
        "size": (960, 1440),
        "prompt": (
            "Use image 1 only as the exact front full-body composition and complete outfit reference. "
            "Use image 2 only as the exact face and hair identity reference. Keep hair-to-sole framing, upright pose, "
            "white cropped jacket over a gray inner top, bare midriff, high-waisted wide-leg deep-teal trousers, "
            "white low-top sneakers, navy crossbody bag, and its strap outside the jacket. One woman on an off-white "
            "studio background; complete limbs, no text, labels, panel, collage, or extra person."
        ),
    },
}

FACE_DIRECTION_RULES = {
    "face_front_quarter_left": (
        "a true 45-degree front-quarter view turned toward the viewer's left: the near right eye and right cheek are visibly wider, "
        "the far left eye is narrower and partly hidden behind the nose bridge, the nose tip points left, and the far left ear is hidden by hair"
    ),
    "face_front_quarter_right": (
        "a true 45-degree front-quarter view turned toward the viewer's right: the near left eye and left cheek are visibly wider, "
        "the far right eye is narrower and partly hidden behind the nose bridge, the nose tip points right, and the far right ear is hidden by hair"
    ),
    "face_profile_left": (
        "a strict true left profile: nose tip and lips point left, exactly one right eye and eyebrow are visible, "
        "and the far left eye, eyebrow, cheek, and ear are fully hidden"
    ),
    "face_profile_right": (
        "a strict true right profile: nose tip and lips point right, exactly one left eye and eyebrow are visible, "
        "and the far right eye, eyebrow, cheek, and ear are fully hidden"
    ),
    "face_rear": (
        "a strict 180-degree rear view facing directly away from the camera; show only the back bob silhouette, nape, and ears if exposed, "
        "with no face, eye, eyebrow, nose, lips, cheek, or side-profile outline"
    ),
}

for target_id, direction in FACE_DIRECTION_RULES.items():
    visible_face_rule = (
        "Preserve the compact oval face, long slender almond eyes with gently upturned outer corners, equal orange-amber irises, "
        f"and petrol-teal jaw-length bob. {HAIR_VOLUME_RULE}"
        if target_id != "face_rear"
        else f"Preserve only the petrol-teal jaw-length bob silhouette, nape hairline, and hair color. {HAIR_VOLUME_RULE}"
    )
    TARGETS[target_id] = {
        "inputs": (QWEN_FACE_REFERENCE, OPENPOSE_GUIDES[target_id]),
        "size": (768, 768),
        "append_style_prompt": False,
        "prompt": (
            f"Use image 1 only as the exact character identity, including the compact oval face, orange-amber irises, petrol-teal hair, fringe, and high-volume jaw-length bob. "
            "Use image 2 only as a weak, non-rendered declarative OpenPose face-and-neck geometry cue; do not copy its lines, dots, colors, or background. "
            f"Create one clean head-and-neck studio reference in {direction}. "
            f"{visible_face_rule} Plain off-white background, one person, no text, panel, collage, accessory, or background scene."
        ),
    }

# A controlled identity-first ablation: the requested quarter turn is expressed
# in text only, with the approved Qwen front reference as the sole image input.
TARGETS["face_front_quarter_left"] = {
    "inputs": (QWEN_FACE_REFERENCE, OPENPOSE_GUIDES["face_front_quarter_left"]),
    "size": (768, 768),
    "append_style_prompt": False,
    "prompt": (
        "Use image 1 as the exact character identity: preserve the original face width, compact oval jawline, eye proportion, orange-amber irises, fringe, "
        "petrol-teal hair color, and high-volume jaw-length bob. Use image 2 only as a weak, non-rendered OpenPose face-and-neck geometry cue. Create a shallow 30-degree "
        "front-quarter view turned toward the viewer's left, never a profile: both eyes remain visible; the near right eye and cheek are only slightly wider; "
        "the nose points slightly left. Copy the original asymmetric side fringe, rounded crown, loose S-waves, pronounced inward C-curls at both jaw-length ends, "
        "and outer hair silhouette that remains wider than the neck. Do not make a smooth, straight, blunt bob; do not lengthen the hair or change the fringe. Do not copy image 2's lines, dots, "
        "or skeleton. Do not create a frontal view, a new person, text, accessory, scene, or panel."
    ),
}


def save_openpose_guide(target_id: str, path: Path) -> None:
    """Create a declarative BODY_18-style map with face direction but no RGB subject data."""
    canvas = Image.new("RGB", (768, 768), "#f7f3e9")
    draw = ImageDraw.Draw(canvas)

    # Body_18 neck/shoulder anchors keep the portrait upright and centered.
    neck = (385, 505)
    right_shoulder = (500, 555)
    left_shoulder = (300, 555)
    # These sparse anchors encode direction only; no source face pixels enter
    # the guide. Quarter maps keep both eyes, profile maps retain one eye, and
    # rear omits face points entirely.
    head = (360, 282)
    nose = (346, 350)
    near_eye = (374, 329)
    far_eye = (318, 333)
    near_ear = (407, 352)
    include_far_eye = True
    include_near_ear = True
    if target_id == "face_front_quarter_right":
        # This is a separately authored right-quarter map, not a horizontal
        # mirror of the left map. It encodes the near left eye/cheek, the
        # smaller far right eye, a rightward nose tip, and the near left ear.
        head = (408, 282)
        nose = (422, 350)
        near_eye = (394, 329)
        far_eye = (450, 333)
        near_ear = (361, 352)
    elif target_id == "face_profile_left":
        head, nose, near_eye, near_ear = (350, 282), (272, 352), (309, 329), (414, 352)
        include_far_eye = False
    elif target_id == "face_profile_right":
        head, nose, near_eye, near_ear = (418, 282), (496, 352), (459, 329), (354, 352)
        include_far_eye = False
    elif target_id == "face_rear":
        head, include_far_eye, include_near_ear = (385, 282), False, False

    def segment(start: tuple[int, int], end: tuple[int, int], color: tuple[int, int, int]) -> None:
        draw.line((start, end), fill=color, width=4)

    def joint(point: tuple[int, int], color: tuple[int, int, int], radius: int = 5) -> None:
        draw.ellipse((point[0] - radius, point[1] - radius, point[0] + radius, point[1] + radius), fill=color)

    muted = (103, 113, 132)
    segment(head, neck, muted)
    segment(neck, right_shoulder, muted)
    segment(neck, left_shoulder, muted)
    if target_id != "face_rear":
        segment(head, nose, muted)
        segment(nose, near_eye, muted)
        if include_far_eye:
            segment(nose, far_eye, muted)
        if include_near_ear:
            segment(nose, near_ear, muted)
    for point, color in (
        (head, muted), (neck, muted), (right_shoulder, muted), (left_shoulder, muted),
    ):
        joint(point, color)
    if target_id != "face_rear":
        joint(nose, muted)
        joint(near_eye, muted)
        if include_near_ear:
            joint(near_ear, muted)
        if include_far_eye:
            joint(far_eye, muted, radius=3)
    canvas.save(path)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def asset_record(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": sha256(path)}


def runtime_record() -> dict[str, object]:
    packages: dict[str, str] = {}
    for name in ("nunchaku", "diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = "not-installed"
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
    }


def load_pipeline() -> QwenImageEditPlusPipeline:
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(TRANSFORMER_ID)
    pipe = QwenImageEditPlusPipeline.from_pretrained(MODEL_ID, transformer=transformer, torch_dtype=torch.bfloat16)
    transformer.set_offload(True, use_pin_memory=False, num_blocks_on_gpu=1)
    pipe._exclude_from_cpu_offload.append("transformer")
    pipe.enable_sequential_cpu_offload()
    return pipe


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=tuple(TARGETS), required=True)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS)
    parser.add_argument("--run-label", default="v2-natural-eyes", help="Suffix that separates controlled reruns.")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    if args.target in FACE_DIRECTION_RULES:
        save_openpose_guide(args.target, ASSETS / OPENPOSE_GUIDES[args.target])
    target = TARGETS[args.target]
    inputs = [ASSETS / name for name in target["inputs"]]
    if missing := [str(path) for path in inputs if not path.is_file()]:
        raise FileNotFoundError("missing input asset(s): " + ", ".join(missing))
    if not PLAN.is_file() or not IDENTITY_CONTRACT.is_file() or not STYLE_CONTRACT.is_file():
        raise FileNotFoundError("missing P7-5.2 Qwen transition plan, identity contract, or style contract")
    style_prompt = json.loads(STYLE_CONTRACT.read_text(encoding="utf-8"))["portrait_style_prompt"]
    prompt = f"{target['prompt']} {style_prompt}" if target.get("append_style_prompt", True) else target["prompt"]

    width, height = target["size"]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"p7-5-2-qwen-edit-prompt-style-{args.target}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output = args.output_dir / f"{stem}.png"
    run_record = args.output_dir / f"{stem}-run.json"
    started = time.monotonic()
    result = load_pipeline()(
        image=[load_image(str(path)).convert("RGB") for path in inputs],
        prompt=prompt,
        generator=torch.Generator("cpu").manual_seed(args.seed),
        true_cfg_scale=4.0,
        negative_prompt=" ",
        num_inference_steps=args.steps,
        guidance_scale=1.0,
        width=width,
        height=height,
    ).images[0]
    result.save(output)
    record = {
        "status": "review_required",
        "experiment_id": f"p7-5-2-qwen-edit-{args.target}",
        "model": MODEL_ID,
        "transformer": TRANSFORMER_ID,
        "runtime": runtime_record(),
        "transition_plan": asset_record(PLAN),
        "identity_contract": asset_record(IDENTITY_CONTRACT),
        "style_prompt_contract": asset_record(STYLE_CONTRACT),
        "target": args.target,
        "run_label": args.run_label,
        "inputs": [asset_record(path) for path in inputs],
        "input_roles": (
            ["complete_head_identity", "declarative_openpose_face_geometry"]
            if args.target == "face_front_quarter_left"
            else
            ["face_identity"]
            if args.target == "face_front" or (args.target in FACE_DIRECTION_RULES and len(target["inputs"]) == 1)
            else ["face_identity", "declarative_openpose_face_geometry"]
            if args.target in FACE_DIRECTION_RULES
            else ["body_and_complete_outfit", "face_identity"]
        ),
        "seed": args.seed,
        "steps": args.steps,
        "size": [width, height],
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "negative_prompt": " ",
        "prompt": prompt,
        "prompt_word_count": len(prompt.split()),
        "output": asset_record(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "Candidate only; do not replace a stable P7-5.2 reference before human review.",
    }
    run_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "run_record": str(run_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

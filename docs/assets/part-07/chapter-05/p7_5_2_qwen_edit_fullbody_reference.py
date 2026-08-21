#!/usr/bin/env python3
"""Generate Qwen Edit full-body references for P7-5.2.

Each run writes a separately named PNG and result record; existing reference
assets are never overwritten.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import torch
from diffusers import QwenImageEditPlusPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel


ASSETS = Path(__file__).resolve().parent
PLAN = ASSETS / "p7-5-2-qwen-edit-transition-plan.json"
IDENTITY_CONTRACT = ASSETS / "p7-5-7-face-identity-contract.json"
STYLE_CONTRACT = ASSETS / "p7-5-7-face-style-prompt-contract.json"
ILLUSTRATION_CONTRACT = ASSETS / "p7-5-7-face-illustration-prompt-contract.json"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
# Candidate filenames carry target, label, seed, and step, so keep them in the
# chapter asset root rather than creating a directory per experiment.
OUTPUT_DIR = ASSETS
DEFAULT_STEPS = 30
# P7-5.7 produces the face-and-upper-torso reference before P7-5.2 uses it
# for full-body generation.  Keeping the shoulders and upper torso in this
# input gives the body editor a clearer neck-to-shoulder connection than a
# face-only crop.
QWEN_FACE_REFERENCE = "p7-5-7-qwen-face-torso-chest-v1-seed-62294-steps-10.png"
HAND_ON_WAIST_OPENPOSE = "p7-5-2-openpose-fullbody-hand-on-waist-pitch0-yaw+00_pitch+00.png"
HAND_ON_WAIST_OPENPOSE_PREFIX = "p7-5-2-openpose-fullbody-hand-on-waist-pitch0"
HAIR_VOLUME_RULE = (
    "Preserve a high-volume crown and a wide rounded jaw-length bob silhouette: medium-density petrol-teal hair, "
    "large loose S-waves, pronounced inward C-curls at both ends, and tapered side locks that stay visibly wider than the neck."
)

TARGETS = {
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
    "fullbody_front_jacket_bag": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            HAND_ON_WAIST_OPENPOSE,
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 5,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and "
            "high-volume petrol-teal bob. Image 2: body-only OpenPose for a centered strict-front full body with the image-right hand on the waist; do not render it. "
            "Preserve an ultra-short white cropped utility jacket, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, "
            "white low-top sneakers, and a navy crossbody bag from right shoulder to left hip. Hair crown to shoe soles, image-right elbow angled outward, image-left arm relaxed, compact neck, "
            "natural seven-head proportion, off-white background, one person, no text."
        ),
    },
    "fullbody_front_seven_head_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            HAND_ON_WAIST_OPENPOSE,
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 30,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and "
            "high-volume petrol-teal bob. Image 2: use only as the centered strict-front seven-head body-only OpenPose structural map with the image-right hand on the waist; do not render it. "
            "Create a full body from hair crown to white sneaker soles, with the image-right elbow angled outward, the image-left arm relaxed, and a natural compact neck. Preserve an ultra-short white cropped "
            "utility jacket with long cuffed sleeves, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, white low-top sneakers, "
            "and one navy crossbody bag from right shoulder to left hip. Plain warm off-white background, one person, no text, panel, collage, or scene."
        ),
    },
    "fullbody_front_seven_head_qwen_outfit_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            HAND_ON_WAIST_OPENPOSE,
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 30,
        "size": (960, 1440),
        "prompt": (
            "Image 1 is face and hair. Image 2 is outfit and bag. Image 3 is pose only; do not render its skeleton. "
            "One full-body young East Asian woman, strict front, hair crown to shoe soles, with the image-right hand on the waist and elbow angled outward, plain warm off-white background."
        ),
    },
    "fullbody_front_outfit_only_candidate_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            HAND_ON_WAIST_OPENPOSE,
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 10,
        "size": (960, 1440),
        "prompt": (
            "Image 1 is face and hair. Image 2 is outfit and bag. Image 3 is pose only; do not render its skeleton. "
            "One full-body young East Asian woman, strict front, hair crown to shoe soles, with the image-right hand on the waist and elbow angled outward, plain warm off-white background."
        ),
    },
    "fullbody_profile_left_seven_head_qwen_outfit_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            f"{HAND_ON_WAIST_OPENPOSE_PREFIX}-yaw-90_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 30,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve only the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and "
            "high-volume petrol-teal bob. Image 2: use only as the exact Qwen-generated complete outfit reference; preserve its ultra-short white "
            "cropped utility jacket with long cuffed sleeves, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, white "
            "low-top sneakers, navy crossbody bag, and one exterior strap. Image 3: use only as the strict left-profile seven-head body-only "
            "OpenPose structural map; do not render it. Create one upright full-body left profile from hair crown to shoe soles: nose, chest, hips, knees, "
            "and shoes point to image left, with one visible eye and a compact natural neck. Keep relaxed arms and the visible exterior bag/strap. "
            "Plain warm off-white background, one person, no text, panel, collage, or scene."
        ),
    },
    "fullbody_profile_left_qwen_outfit_prompt_only": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 5,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve only the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and "
            "high-volume petrol-teal bob. Image 2: use only as the exact Qwen-generated complete outfit reference; preserve its ultra-short white "
            "cropped utility jacket with long cuffed sleeves, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, white "
            "low-top sneakers, navy crossbody bag, and one exterior strap. Do not create a frontal view. Create one upright strict full-body left profile "
            "from hair crown to shoe soles: nose, chest, hips, knees, and shoes all point to image left; show exactly one eye; hide the far eye, cheek, "
            "and shoulder behind the head and torso. Keep relaxed arms, a compact natural neck, and the visible exterior bag/strap. Plain warm off-white "
            "background, one person, no text, panel, collage, or scene."
        ),
    },
    "fullbody_quarter_left_seven_head_qwen_outfit_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            f"{HAND_ON_WAIST_OPENPOSE_PREFIX}-yaw-45_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 5,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve only the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and "
            "high-volume petrol-teal bob. Image 2: use only as the exact Qwen-generated complete outfit reference; preserve its ultra-short white "
            "cropped utility jacket with long cuffed sleeves, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, white "
            "low-top sneakers, navy crossbody bag, and one exterior strap. Image 3: use only as the strict 45-degree left-facing seven-head body-only "
            "OpenPose structural map with near/far foreshortening; do not render it. This must not be a frontal view. Create one upright full-body left front-quarter view from hair crown to shoe soles: the nose, "
            "chest, hips, knees, and shoes turn clearly 45 degrees toward image left; both eyes remain visible, the nearer image-right cheek, shoulder, arm, hip, and shoe are larger, and the image-left side is visibly compressed behind the torso. Keep "
            "relaxed arms, a compact natural neck, and the visible exterior bag/strap. Plain warm off-white background, one person, no text, panel, "
            "collage, or scene."
        ),
    },
    "fullbody_quarter_left_qwen_outfit_prompt_only": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 5,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve only the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and "
            "high-volume petrol-teal bob. Image 2: use only as the exact Qwen-generated complete outfit reference; preserve its ultra-short white "
            "cropped utility jacket with long cuffed sleeves, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, white "
            "low-top sneakers, navy crossbody bag, and one exterior strap. Do not create a frontal view. Create one upright full-body 45-degree left "
            "front-quarter view from hair crown to shoe soles: the nose, chest, hips, knees, and shoes turn clearly toward image left; both eyes remain "
            "visible; the nearer image-right cheek, shoulder, arm, hip, and shoe are larger; and the image-left side is visibly compressed behind the torso. "
            "Keep relaxed arms, a compact natural neck, and the visible exterior bag/strap. Plain warm off-white background, one person, no text, panel, "
            "collage, or scene."
        ),
    },
    "fullbody_quarter_left_raised_arm_skeleton_ablation": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            f"{HAND_ON_WAIST_OPENPOSE_PREFIX}-yaw-45_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 5,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve only the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and high-volume petrol-teal bob. "
            "Image 2: use only as the exact Qwen-generated complete outfit reference; preserve its ultra-short white cropped utility jacket with long cuffed sleeves, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, white low-top sneakers, navy crossbody bag, and one exterior strap. "
            "Image 3 is a body-only OpenPose structural map; do not render it. Create an upright full-body 45-degree left front-quarter view, from hair crown to shoe soles, with the image-right arm visibly raised beside the head and the other arm relaxed at the side. Keep the raised hand open and visible. Plain warm off-white background, one person, no text, panel, collage, or scene."
        ),
    },
    "fullbody_front_asymmetric_lowered_arms_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            "p7-5-2-openpose-front-hand-on-hip-weight-shift-v3/p7-5-2-openpose-relation-yaw+00_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 5,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve only the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and high-volume petrol-teal bob. "
            "Image 2: use only as the exact Qwen-generated complete outfit reference; preserve its ultra-short white cropped utility jacket with long cuffed sleeves, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, white low-top sneakers, navy crossbody bag, and one exterior strap. "
            "Image 3 is a body-only OpenPose structural map; do not render it. Create one upright strict-front full body from hair crown to shoe soles. Put the image-right hand on the waist with the elbow angled outward; keep the image-left arm lowered beside the body. Shift weight onto the image-left leg with a subtle hip shift; relax the image-right knee and place its foot slightly outward. Keep both arm and leg segments natural and equal in length to a relaxed standing body. Plain warm off-white background, one person, no text, panel, collage, or scene."
        ),
    },
    "fullbody_quarter_left_hand_on_hip_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            "p7-5-2-openpose-quarter-left-hand-on-hip-elbow-out-perspective-v5/p7-5-2-openpose-relation-yaw-45_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 5,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve only the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and high-volume petrol-teal bob. "
            "Image 2: use only as the exact Qwen-generated complete outfit reference; preserve its ultra-short white cropped utility jacket with long cuffed sleeves, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, white low-top sneakers, navy crossbody bag, and one exterior strap. "
            "Image 3 is a body-only OpenPose structural map; do not render it. Create one upright 45-degree left front-quarter full body from hair crown to shoe soles. The nearer image-right hand rests on the waist while its elbow is lifted wide at shoulder height, creating a large triangular arm silhouette; the image-left arm is lowered. Shift weight onto the nearer leg with the far knee and foot relaxed behind. Plain warm off-white background, one person, no text, panel, collage, or scene."
        ),
    },
    "fullbody_quarter_left_approved_front_openpose": {
        "inputs": (
            "p7-5-2-fullbody-front-qwen-approved-outfit-reference.png",
            f"{HAND_ON_WAIST_OPENPOSE_PREFIX}-yaw-45_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "input_roles": ["approved_fullbody_identity_outfit", "standard_openpose_fullbody_structure"],
        "default_steps": 30,
        "size": (960, 1440),
        "prompt": (
            "Image 1 is the exact approved Qwen character, full outfit, bag, and studio reference. Preserve the same young East Asian woman: "
            "petrol-teal jaw-length bob, orange-amber irises, white ultra-short cropped utility jacket with long cuffed sleeves, gray inner crop top, "
            "bare-midriff band, deep-teal high-waisted wide-leg trousers, white low-top sneakers, and one navy crossbody bag with its exterior strap. "
            "Image 2 is a body-only OpenPose structural map; use its pose and 45-degree left-facing orientation but never render its lines, dots, colours, or background. "
            "Create one upright full-body left front-quarter view from hair crown to shoe soles: the nose, chest, hips, knees, and shoes turn toward image left; "
            "both eyes remain visible; the nearer image-right cheek, shoulder, arm, hip, and shoe are larger, while the image-left side is compressed behind the torso. "
            "Keep relaxed arms and a compact natural neck. Plain warm off-white background, one person, no text, panel, collage, or scene."
        ),
    },
    "fullbody_front_quarter_left_qwen": {
        "inputs": (
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            f"{HAND_ON_WAIST_OPENPOSE_PREFIX}-yaw-45_pitch+00.png",
        ),
        "size": (960, 1440),
        "prompt": (
            "Use image 1 only as the exact full-body composition, outfit, crop-jacket length, bag, strap, trousers, shoes, "
            "and hair-to-sole framing reference. Use image 2 only as a non-rendered standard OpenPose structural guide, including its compact "
            "body-only landmark map; do not render its lines, dots, colors, or background. Create the same young "
            "East Asian adult woman in a true 45-degree left-facing front-quarter full-body view: the nose and torso point toward image left, "
            "both eyes remain visible, the image-right cheek is nearer and wider, and the image-left eye is narrower. "
            "Keep an upright relaxed pose, full body from hair crown to shoe soles, "
            "the short white cropped utility jacket with sleeves down to the wrists, gray inner crop top, visible midriff gap, "
            "high-waisted deep-teal wide-leg trousers, white low-top sneakers, and one navy crossbody bag with its strap outside the jacket. "
            "Plain warm off-white studio background, one person, no text, panel, collage, extra bag, or scene."
        ),
    },
    "fullbody_profile_left_qwen": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            f"{HAND_ON_WAIST_OPENPOSE_PREFIX}-yaw-90_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 10,
        "size": (960, 1440),
        "prompt": (
            "Use image 1 only for the young East Asian woman's head identity: compact oval face, high straight nose bridge, orange-amber "
            "irises, asymmetric fringe, and high-volume petrol-teal bob. Keep an ultra-short white cropped utility jacket with long cuffed "
            "sleeves, gray micro-crop top, bare-midriff gap, high-waisted deep-teal wide-leg trousers, white low-top sneakers, and one navy "
            "crossbody bag with one exterior strap. Use image 2 only as a non-rendered standard OpenPose structural guide, including its compact "
            "asymmetric profile head map; never render its lines, dots, colors, "
            "or black background. Create one strict full-body left profile, upright and centered from hair crown to shoe soles: face, nose, "
            "chest, hips, knees, and shoes all point toward image left. Show exactly one visible eye and eyebrow; hide the far eye, cheek, "
            "and ear behind the nose and hair. Keep relaxed arms, a compact natural neck, and the navy bag and strap on the visible exterior. "
            "Plain off-white background; one person; no text, panel, or scene."
        ),
    },
}


def approved_front_direction_target(yaw: int, direction: str, geometry: str) -> dict[str, object]:
    """Define a review-only direction candidate from the approved front anchor."""
    return {
        "inputs": (
            "p7-5-2-fullbody-front-qwen-approved-outfit-reference.png",
            f"{HAND_ON_WAIST_OPENPOSE_PREFIX}-yaw{yaw:+03d}_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "input_roles": ["approved_fullbody_identity_outfit", "standard_openpose_fullbody_structure"],
        "default_steps": 30,
        "size": (960, 1440),
        "prompt": (
            "Image 1 is the exact approved Qwen character, full outfit, bag, and studio reference. Preserve the same young East Asian woman: "
            "petrol-teal jaw-length bob, orange-amber irises, white ultra-short cropped utility jacket with long cuffed sleeves, gray inner crop top, "
            "bare-midriff band, deep-teal high-waisted wide-leg trousers, white low-top sneakers, and one navy crossbody bag with its exterior strap. "
            "Image 2 is a body-only OpenPose structural map; use its pose and orientation but never render its lines, dots, colours, or background. "
            f"Create one upright full-body {direction} view from hair crown to shoe soles. {geometry} "
            "Keep relaxed arms and a compact natural neck. Plain warm off-white background, one person, no text, panel, collage, or scene."
        ),
    }


TARGETS.update(
    {
        "fullbody_quarter_right_approved_front_openpose": approved_front_direction_target(
            45,
            "right front-quarter",
            "The nose, chest, hips, knees, and shoes turn toward image right; both eyes remain visible; the nearer image-left side is larger while the image-right side is compressed behind the torso.",
        ),
        "fullbody_profile_left_approved_front_openpose": approved_front_direction_target(
            -90,
            "strict left-profile",
            "The nose, chest, hips, knees, and shoes all point toward image left; show exactly one eye and keep the far eye hidden.",
        ),
        "fullbody_profile_right_approved_front_openpose": approved_front_direction_target(
            90,
            "strict right-profile",
            "The nose, chest, hips, knees, and shoes all point toward image right; show exactly one eye and keep the far eye hidden.",
        ),
    }
)

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
    pipe = QwenImageEditPlusPipeline.from_pretrained(MODEL_ID, transformer=transformer, torch_dtype=torch.bfloat16, local_files_only=True)
    transformer.set_offload(True, use_pin_memory=True, num_blocks_on_gpu=1)
    pipe._exclude_from_cpu_offload.append("transformer")
    pipe.enable_sequential_cpu_offload()
    return pipe


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=tuple(TARGETS), help="One target to generate.")
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=tuple(TARGETS),
        help="Generate these targets sequentially, in the supplied order.",
    )
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=None, help="Denoising steps; defaults to the target's configured value.")
    parser.add_argument("--run-label", default="v2-natural-eyes", help="Suffix that separates controlled reruns.")
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()
    if bool(args.target) == bool(args.targets):
        parser.error("provide exactly one of --target or --targets")
    if args.targets:
        for target_id in args.targets:
            command = [
                sys.executable,
                str(Path(__file__).resolve()),
                "--target",
                target_id,
                "--seed",
                str(args.seed),
                "--run-label",
                args.run_label,
                "--output-dir",
                str(args.output_dir),
            ]
            if args.steps is not None:
                command.extend(("--steps", str(args.steps)))
            subprocess.run(command, check=True)
        return
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    target = TARGETS[args.target]
    steps = args.steps if args.steps is not None else target.get("default_steps", DEFAULT_STEPS)
    if steps < 1:
        raise ValueError("--steps must be at least 1")
    inputs = [ASSETS / name for name in target["inputs"]]
    if missing := [str(path) for path in inputs if not path.is_file()]:
        raise FileNotFoundError("missing input asset(s): " + ", ".join(missing))
    if not PLAN.is_file() or not IDENTITY_CONTRACT.is_file() or not STYLE_CONTRACT.is_file() or not ILLUSTRATION_CONTRACT.is_file():
        raise FileNotFoundError("missing P7-5.2 Qwen transition plan, identity, style, or illustration contract")
    style_prompt = json.loads(STYLE_CONTRACT.read_text(encoding="utf-8"))["portrait_style_prompt"]
    illustration_prompt = json.loads(ILLUSTRATION_CONTRACT.read_text(encoding="utf-8"))["illustration_prompt"]
    prompt_parts = []
    if target.get("append_style_prompt", True):
        prompt_parts.append(style_prompt)
    if target.get("append_illustration_prompt", False):
        prompt_parts.append(illustration_prompt)
    prompt_parts.append(target["prompt"])
    prompt = " ".join(prompt_parts)

    width, height = target["size"]
    stem = f"p7-5-2-qwen-edit-prompt-style-{args.target}-{args.run_label}-seed-{args.seed}-steps-{steps}"
    output = args.output_dir / f"{stem}.png"
    result_record = args.output_dir / f"{stem}-result.json"
    started = time.monotonic()
    pipeline = load_pipeline()
    generation = {
        "prompt": prompt,
        "generator": torch.Generator("cpu").manual_seed(args.seed),
        "true_cfg_scale": 4.0,
        "negative_prompt": target.get("negative_prompt", " "),
        "num_inference_steps": steps,
        "guidance_scale": 1.0,
        "width": width,
        "height": height,
    }
    if inputs:
        generation["image"] = [load_image(str(path)).convert("RGB") for path in inputs]
    result = pipeline(**generation).images[0]
    result.save(output)
    record = {
        "status": "generated",
        "experiment_id": f"p7-5-2-qwen-edit-{args.target}",
        "model": MODEL_ID,
        "transformer": TRANSFORMER_ID,
        "runtime": runtime_record(),
        "transition_plan": asset_record(PLAN),
        "identity_contract": asset_record(IDENTITY_CONTRACT),
        "style_prompt_contract": asset_record(STYLE_CONTRACT),
        "illustration_prompt_contract": asset_record(ILLUSTRATION_CONTRACT),
        "prompt_contracts_applied": {
            "watercolor_style": target.get("append_style_prompt", True),
            "illustration": target.get("append_illustration_prompt", False),
        },
        "target": args.target,
        "run_label": args.run_label,
        "inputs": [asset_record(path) for path in inputs],
        "input_roles": target.get("input_roles") or (
            ["head_identity", "qwen_complete_outfit", "standard_openpose_fullbody_structure"]
            if args.target in {
                "fullbody_front_seven_head_qwen_outfit_skeleton",
                "fullbody_profile_left_seven_head_qwen_outfit_skeleton",
                "fullbody_quarter_left_seven_head_qwen_outfit_skeleton",
                "fullbody_quarter_left_raised_arm_skeleton_ablation",
                "fullbody_front_asymmetric_lowered_arms_skeleton",
                "fullbody_quarter_left_hand_on_hip_skeleton",
            }
            else
            ["head_identity", "qwen_complete_outfit"]
            if args.target in {"fullbody_quarter_left_qwen_outfit_prompt_only", "fullbody_profile_left_qwen_outfit_prompt_only"}
            else
            ["complete_head_identity", "standard_openpose_face_geometry"]
            if args.target == "face_front_quarter_left"
            else
            [
                "head_identity",
                "standard_openpose_fullbody_structure",
            ]
            if args.target in {"fullbody_front_jacket_bag", "fullbody_front_seven_head_skeleton", "fullbody_front_seven_head_qwen_outfit_skeleton", "fullbody_profile_left_qwen"}
            else
            ["body_and_complete_outfit", "standard_openpose_fullbody_structure"]
            if args.target == "fullbody_front_quarter_left_qwen"
            else
            ["body_and_complete_outfit", "face_identity"]
        ),
        "seed": args.seed,
        "steps": steps,
        "size": [width, height],
        "true_cfg_scale": 4.0,
        "guidance_scale": 1.0,
        "negative_prompt": " ",
        "prompt": prompt,
        "prompt_word_count": len(prompt.split()),
        "output": asset_record(output),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "decision": "Generated full-body reference; compare its pose, identity, outfit, and framing with the stated input roles.",
    }
    result_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result_record": str(result_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

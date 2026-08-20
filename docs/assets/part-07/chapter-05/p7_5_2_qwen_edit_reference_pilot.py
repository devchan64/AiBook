#!/usr/bin/env python3
"""Create review-only Qwen Edit candidates for the P7-5.2 front anchors.

Approved P7-5.2 reference PNGs remain immutable during this pilot. This script
writes a separate candidate PNG and run record; it never changes a stable
reference, manifest, or approval status.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import importlib.metadata
import json
import platform
import subprocess
import sys
import sysconfig
import time
import types
from pathlib import Path

import numpy as np
import torch
from diffusers import QwenImageEditPlusPipeline, QwenImagePipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel
from PIL import Image


ASSETS = Path(__file__).resolve().parent
PLAN = ASSETS / "p7-5-2-qwen-edit-transition-plan.json"
IDENTITY_CONTRACT = ASSETS / "p7-5-2-character-identity-contract.json"
STYLE_CONTRACT = ASSETS / "p7-5-2-character-reference-style-prompt-contract.json"
ILLUSTRATION_CONTRACT = ASSETS / "p7-5-2-character-reference-illustration-prompt-contract.json"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
TRANSFORMER_ID = "nunchaku-tech/nunchaku-qwen-image-edit-2509/svdq-fp4_r128-qwen-image-edit-2509.safetensors"
BASE_MODEL_ID = "Qwen/Qwen-Image"
BASE_TRANSFORMER_ID = "/home/cbsim/.cache/huggingface/hub/models--nunchaku-tech--nunchaku-qwen-image/snapshots/4d9f4f667ea571ab172e0ee29ac2c27b82a41a6b/svdq-fp4_r128-qwen-image.safetensors"
OUTPUT_DIR = ASSETS / "p7-5-2-qwen-edit-candidates"
DEFAULT_STEPS = 30
QWEN_FACE_REFERENCE = "p7-5-2-face-front-qwen-role-separated-reference.png"
QUARTER_LEFT_FACE_GUIDE = "face_front_quarter_left"
QUARTER_LEFT_FACE_GUIDE_FILENAME = "p7-5-2-openpose-face-quarter-left-declarative-guide.png"
HAIR_VOLUME_RULE = (
    "Preserve a high-volume crown and a wide rounded jaw-length bob silhouette: medium-density petrol-teal hair, "
    "large loose S-waves, pronounced inward C-curls at both ends, and tapered side locks that stay visibly wider than the neck."
)

TARGETS = {
    "head_front": {
        "inputs": (),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 10,
        "size": (768, 768),
        "prompt": (
            "Strict frontal head-and-neck studio reference of one young East Asian woman in her early twenties, face centered and facing the camera with both eyes and ears visible: compact oval face, "
            "a defined high nose bridge, and a refined straight nose line; "
            "high-volume petrol-teal jaw-length bob with asymmetric fringe, loose S-waves, inward-curled ends, and side locks wider "
            "than the neck. Long slender gently upturned eyes; equal orange-amber irises with distinct centered round dark pupils, "
            "separate from eyelids and eyeliner. Show ears and neck. No text, accessory, panel, collage, or background scene."
        ),
    },
    "outfit_integrated_front_hip": {
        "inputs": (),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 10,
        "size": (768, 1152),
        "prompt": (
            "Create one isolated front apparel-and-bag reference from shoulders through hips on a neutral headless torso. "
            "Show a very short white cropped utility jacket as the closed outer layer: its front panels cover the chest, "
            "two flap chest pockets and long cuffed sleeves are visible, and its hem ends immediately below the bust. "
            "Only below that hem, show a charcoal-gray micro-crop inner top, then a clear bare-midriff band, then the "
            "navel-height waistband of deep-teal high-waisted wide-leg trousers. Place one compact deep-navy woven-canvas "
            "crossbody bag at the wearer's outer-left hip. Show exactly one taut matching navy strap from the wearer's "
            "right shoulder across the exterior of the white jacket to the bag. Plain off-white background; no head, hands, "
            "legs, text, logo, hanger, extra strap, or other object."
        ),
    },
    "outfit_integrated_front_full_length": {
        "inputs": (),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 10,
        "size": (768, 1152),
        "prompt": (
            "Front full-length women's outfit reference. White ultra-short utility jacket ending immediately below the bust, gray crop top, clear bare-midriff band, "
            "deep-teal high-waisted wide-leg trousers, white low-top sneakers, navy crossbody bag and one strap. Plain off-white background."
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
    "fullbody_front_jacket_bag": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-openpose-fullbody-front-body-only-approved-guide.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 5,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and "
            "high-volume petrol-teal bob. Image 2: body-only OpenPose for a centered strict-front standing full body; do not render it. "
            "Preserve an ultra-short white cropped utility jacket, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, "
            "white low-top sneakers, and a navy crossbody bag from right shoulder to left hip. Hair crown to shoe soles, relaxed arms, compact neck, "
            "natural seven-head proportion, off-white background, one person, no text."
        ),
    },
    "fullbody_front_seven_head_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-openpose-turnaround-body-only-pitch0-v1/p7-5-2-openpose-relation-yaw+00_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 30,
        "size": (960, 1440),
        "prompt": (
            "Image 1: preserve the young East Asian woman's compact oval face, high straight nose, amber irises, asymmetric fringe, and "
            "high-volume petrol-teal bob. Image 2: use only as the centered strict-front seven-head body-only OpenPose structural map; do not render it. "
            "Create a full body from hair crown to white sneaker soles, with relaxed arms and natural compact neck. Preserve an ultra-short white cropped "
            "utility jacket with long cuffed sleeves, gray micro-crop top, bare midriff, deep-teal high-waisted wide-leg trousers, white low-top sneakers, "
            "and one navy crossbody bag from right shoulder to left hip. Plain warm off-white background, one person, no text, panel, collage, or scene."
        ),
    },
    "fullbody_front_seven_head_qwen_outfit_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            "p7-5-2-openpose-five-yaw-pitch0-fov30-frame-up-v1/p7-5-2-openpose-relation-yaw+00_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 30,
        "size": (960, 1440),
        "prompt": (
            "Image 1 is face and hair. Image 2 is outfit and bag. Image 3 is pose only; do not render its skeleton. "
            "One full-body young East Asian woman, strict front, hair crown to shoe soles, plain warm off-white background."
        ),
    },
    "fullbody_front_outfit_only_candidate_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            "p7-5-2-openpose-five-yaw-pitch0-fov30-5-v2/p7-5-2-openpose-relation-yaw+00_pitch+00.png",
        ),
        "append_style_prompt": False,
        "append_illustration_prompt": True,
        "default_steps": 10,
        "size": (960, 1440),
        "prompt": (
            "Image 1 is face and hair. Image 2 is outfit and bag. Image 3 is pose only; do not render its skeleton. "
            "One full-body young East Asian woman, strict front, hair crown to shoe soles, plain warm off-white background."
        ),
    },
    "fullbody_profile_left_seven_head_qwen_outfit_skeleton": {
        "inputs": (
            QWEN_FACE_REFERENCE,
            "p7-5-2-fullbody-front-qwen-jacket-bag-reference.png",
            "p7-5-2-openpose-turnaround-body-only-pitch0-v1/p7-5-2-openpose-relation-yaw-90_pitch+00.png",
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
            "p7-5-2-openpose-turnaround-body-only-perspective-face-anchor-quarter-left-v2/p7-5-2-openpose-relation-yaw-45_pitch+00.png",
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
            "p7-5-2-openpose-turnaround-raised-arm-quarter-left-v2/p7-5-2-openpose-relation-yaw-45_pitch+00.png",
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
            "p7-5-2-openpose-five-yaw-pitch0-fov30-frame-up-v1/p7-5-2-openpose-relation-yaw-45_pitch+00.png",
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
            "p7-5-2-openpose-fullbody-quarter-left-45deg-approved-guide.png",
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
            "p7-5-2-openpose-fullbody-profile-left-90deg-approved-guide.png",
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
            f"p7-5-2-openpose-five-yaw-pitch0-fov30-frame-up-v1/p7-5-2-openpose-relation-yaw{yaw:+03d}_pitch+00.png",
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

# Head-detail rotation must not use a low-resolution fullbody image as an
# identity source.  Keep the approved frontal face as the sole rendered
# reference; OpenPose communicates only the requested view geometry.
TARGETS["head_quarter_left_from_front_identity"] = {
    "inputs": (QWEN_FACE_REFERENCE, QUARTER_LEFT_FACE_GUIDE_FILENAME),
    "append_style_prompt": False,
    "append_illustration_prompt": False,
    "face_guide": QUARTER_LEFT_FACE_GUIDE,
    "input_roles": ["approved_front_face_detail_identity", "openpose_face_rotation_geometry"],
    "default_steps": 30,
    "size": (768, 768),
    "prompt": (
        "Rotation prompt — Image 1 is the immutable frontal identity and rendering reference: preserve its compact oval face, eye spacing, "
        "high straight nose bridge, amber iris shape and colour, line detail, contrast, and shading without restyling. Preserve the exact "
        "asymmetric hair colour layout: petrol-teal fringe and image-left front locks, with the dark near-black mass on image right; keep its "
        "high crown, loose S-waves, and inward-curled jaw-length ends rather than simplifying it into a uniform bob. Image 2 is a non-rendered "
        "OpenPose face geometry guide only. Create a detailed head-and-neck studio reference of the same young East Asian woman in a true "
        "45-degree left front-quarter view: nose tip points image left, near image-right eye and cheek are wider, and far image-left eye is "
        "narrower behind the bridge. Crop from crown to collarbones; simple cool blue-gray background with the same restrained directional "
        "shadow language as Image 1; no body, outfit, bag, text, panel, or scene."
    ),
}

def openpose_module():
    """Load controlnet_aux OpenPose without importing its optional top-level extras."""
    root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    package_name = "p7_5_2_openpose_aux"
    parent = types.ModuleType(package_name)
    parent.__path__ = [str(root)]
    sys.modules[package_name] = parent
    directory = root / "open_pose"
    spec = importlib.util.spec_from_file_location(
        f"{package_name}.open_pose",
        directory / "__init__.py",
        submodule_search_locations=[str(directory)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("controlnet_aux OpenPose renderer is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def save_openpose_guide(target_id: str, path: Path) -> None:
    """Render a canonical OpenPose BODY_18 + face-landmark guide.

    No subject RGB pixels are used.  Direction comes from the nose displacement
    and asymmetric face-landmark geometry, then the installed OpenPose renderer
    applies the standard black canvas, limb colours, and landmark convention.
    """
    module = openpose_module()

    def point(x: float, y: float):
        return module.Keypoint(x=x / 768, y=y / 768)

    neck = (385, 505)
    nose = (346, 350)
    face_center = (366, 342)
    if target_id in {"face_front_quarter_right", "face_profile_right"}:
        nose, face_center = (422, 350), (402, 342)
    if target_id == "face_profile_left":
        nose, face_center = (272, 352), (336, 344)
    if target_id == "face_profile_right":
        nose, face_center = (496, 352), (432, 344)

    keypoints = [None] * 18
    if target_id != "face_rear":
        keypoints[0] = point(*nose)
    keypoints[1] = point(*neck)
    keypoints[2] = point(500, 555)
    keypoints[5] = point(300, 555)

    face = None
    if target_id != "face_rear":
        cx, cy = face_center
        # A compact canonical OpenPose face mesh.  The right-facing variant
        # has a wider near (image-left) eye and cheek and a nose bridge shifted
        # toward the image-right edge, matching the target's screen direction.
        toward_right = target_id in {"face_front_quarter_right", "face_profile_right"}
        near_scale = 1.18 if toward_right else 0.86
        far_scale = 0.86 if toward_right else 1.18
        jaw = [
            (cx - 62, cy - 14), (cx - 57, cy + 8), (cx - 49, cy + 28), (cx - 38, cy + 45),
            (cx - 22, cy + 57), (cx, cy + 62), (cx + 22, cy + 57), (cx + 38, cy + 45),
            (cx + 49, cy + 28), (cx + 57, cy + 8), (cx + 62, cy - 14),
        ]
        if toward_right:
            jaw = [(cx + (x - cx) * (near_scale if x < cx else far_scale), y) for x, y in jaw]
        else:
            jaw = [(cx + (x - cx) * (near_scale if x > cx else far_scale), y) for x, y in jaw]
        left_eye = [(cx - 41, cy - 14), (cx - 30, cy - 20), (cx - 18, cy - 14), (cx - 30, cy - 8)]
        right_eye = [(cx + 18, cy - 14), (cx + 30, cy - 20), (cx + 41, cy - 14), (cx + 30, cy - 8)]
        if toward_right:
            left_eye = [(cx + (x - cx) * near_scale, y) for x, y in left_eye]
            right_eye = [(cx + (x - cx) * far_scale, y) for x, y in right_eye]
        else:
            left_eye = [(cx + (x - cx) * far_scale, y) for x, y in left_eye]
            right_eye = [(cx + (x - cx) * near_scale, y) for x, y in right_eye]
        landmarks = jaw + left_eye + right_eye + [
            (cx - 15, cy + 2), (cx, cy + 10), nose, (cx - 14, cy + 27), (cx, cy + 31), (cx + 14, cy + 27),
            (cx - 22, cy + 42), (cx, cy + 47), (cx + 22, cy + 42),
        ]
        face = [point(x, y) for x, y in landmarks]

    pose = module.PoseResult(
        body=module.BodyResult(keypoints=keypoints, total_score=1.0, total_parts=4),
        left_hand=None,
        right_hand=None,
        face=face,
    )
    rendered = module.draw_poses([pose], 768, 768, draw_body=True, draw_hand=False, draw_face=True)
    Image.fromarray(np.ascontiguousarray(rendered)).save(path)


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


def load_pipeline(image_edit: bool):
    transformer_id = TRANSFORMER_ID if image_edit else BASE_TRANSFORMER_ID
    model_id = MODEL_ID if image_edit else BASE_MODEL_ID
    transformer = NunchakuQwenImageTransformer2DModel.from_pretrained(transformer_id)
    pipeline_type = QwenImageEditPlusPipeline if image_edit else QwenImagePipeline
    pipe = pipeline_type.from_pretrained(model_id, transformer=transformer, torch_dtype=torch.bfloat16, local_files_only=True)
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
    generated_guides: dict[str, Path] = {}
    target = TARGETS[args.target]
    if face_guide := target.get("face_guide"):
        candidate_guide = args.output_dir / f"p7-5-2-qwen-edit-{args.target}-{face_guide}-guide.png"
        save_openpose_guide(face_guide, candidate_guide)
        generated_guides[QUARTER_LEFT_FACE_GUIDE_FILENAME] = candidate_guide
    steps = args.steps if args.steps is not None else target.get("default_steps", DEFAULT_STEPS)
    if steps < 1:
        raise ValueError("--steps must be at least 1")
    inputs = [generated_guides.get(name, ASSETS / name) for name in target["inputs"]]
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
    run_record = args.output_dir / f"{stem}-run.json"
    started = time.monotonic()
    pipeline = load_pipeline(image_edit=bool(inputs))
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
        "status": "review_required",
        "experiment_id": f"p7-5-2-qwen-edit-{args.target}",
        "model": MODEL_ID if inputs else BASE_MODEL_ID,
        "transformer": TRANSFORMER_ID if inputs else BASE_TRANSFORMER_ID,
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
            []
            if args.target in {"outfit_integrated_front_hip", "outfit_integrated_front_full_length"}
            else
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
            ["face_identity"]
            if args.target == "head_front"
            else ["body_and_complete_outfit", "face_identity"]
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
        "decision": "Candidate only; do not replace a stable P7-5.2 reference before human review.",
    }
    run_record.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "run_record": str(run_record)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

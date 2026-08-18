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
import sys
import sysconfig
import time
import types
from pathlib import Path

import numpy as np
import torch
from diffusers import QwenImageEditPlusPipeline
from diffusers.utils import load_image
from nunchaku import NunchakuQwenImageTransformer2DModel
from PIL import Image


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
        "inputs": (QWEN_FACE_REFERENCE,),
        "size": (768, 768),
        "prompt": (
            "Use image 1 only as the exact Qwen front-face identity reference. Preserve its compact oval face, "
            "petrol-teal jaw-length bob, long slender almond eyes with gently upturned outer corners, moderately narrow "
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
    "fullbody_front_jacket_bag": {
        "inputs": (QWEN_FACE_REFERENCE,),
        "size": (960, 1440),
        "prompt": (
            "Use image 1 only as the exact character face and hair identity reference. Create a clean strict full-body "
            "front studio character reference of the same adult woman, standing upright with both arms relaxed at her sides, "
            "centered and visible continuously from the hair crown to both shoe soles. Preserve the compact oval face, "
            "orange-amber irises, asymmetric fringe, and high-volume petrol-teal jaw-length bob. Dress her in a closed "
            "white cropped utility jacket with two chest flap pockets and long cuffed sleeves, over a charcoal-gray "
            "micro-crop crew-neck inner top with only a narrow gray band visible below the jacket hem and a small bare-midriff gap. "
            "Wear high-waisted deep-teal wide-leg trousers with a visibly loose straight drape from hip to ankle, never skinny pants; "
            "white lace-up low-top sneakers with complete soles; and one deep-navy crossbody bag resting at the outer left hip. "
            "The taut navy strap begins at the wearer's right shoulder, crosses outside the jacket, and connects visibly to the bag. "
            "Plain warm off-white studio background, full limbs, one person, no text, labels, panel, collage, extra bag, or background scene."
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
            "Use image 2 as the standard OpenPose structural control map for face-and-neck geometry; do not render its lines, dots, colors, or background. "
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

TARGETS["face_front_quarter_right"] = {
    "inputs": (QWEN_FACE_REFERENCE, OPENPOSE_GUIDES["face_front_quarter_right"]),
    "size": (768, 768),
    "append_style_prompt": False,
    "prompt": (
        "Use image 1 as the exact character identity: preserve the compact oval face, orange-amber irises, petrol-teal hair, asymmetric fringe, "
        "and high-volume jaw-length bob. Use image 2 as the standard OpenPose face-and-neck structural control map. Turn the same head "
        "toward the image's right edge: the nose tip and lips must point to screen right, the image-left cheek is nearer and wider, the image-right eye is narrower, "
        "and the image-right ear is hidden by hair. This is a right-facing front-quarter view, never left-facing and never frontal or profile. Keep the original loose S-waves "
        "and inward C-curls. Do not render image 2's black background, lines, dots, colors, or skeleton; do not create text, accessory, scene, or panel."
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
    """Render a canonical ControlNet/OpenPose BODY_18 + face-landmark map.

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
            ["complete_head_identity", "standard_openpose_face_geometry"]
            if args.target == "face_front_quarter_left"
            else
            ["face_identity"]
            if args.target == "face_front" or (args.target in FACE_DIRECTION_RULES and len(target["inputs"]) == 1)
            else ["face_identity", "standard_openpose_face_geometry"]
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

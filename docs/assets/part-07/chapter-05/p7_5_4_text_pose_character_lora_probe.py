#!/usr/bin/env python3
"""Probe text-pose compilation plus a character LoRA without image references.

The comparison keeps the prompt, seed, OpenPose image, base model and
ControlNet scale fixed.  It changes only the previously trained experimental
character LoRA from off to on.  The pose control is drawn from declarative
pose tickets, so no source character pixels enter the pipeline.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import sysconfig
import time
import types
from pathlib import Path

import numpy as np
import torch
from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline
from PIL import Image, ImageDraw


ROOT = Path("/home/cbsim/ws/AiBook")
ASSETS = ROOT / "docs/assets/part-07/chapter-05"
ANIMAGINE = Path(
    "/home/cbsim/.cache/huggingface/hub/models--cagliostrolab--animagine-xl-4.0/"
    "snapshots/2b7c1b397761bf5bd3cc42e5b39ec99314a75a96"
)
OPENPOSE = Path(
    "/home/cbsim/.cache/huggingface/hub/models--xinsir--controlnet-openpose-sdxl-1.0/"
    "snapshots/23f966cd5cfdd3f7729c903e243d87152162d2b7"
)
EXPERIMENTAL_LORA = ROOT / ".tmp/p7-5-3-animagine-character-lora"
SIZE = (512, 768)
NEGATIVE = "multiple people, child, cropped feet, extra arms, extra legs, text, watermark"
IDENTITY = json.loads((ASSETS / "p7-5-2-character-identity-contract.json").read_text(encoding="utf-8"))

# Each ticket is text-originated.  `points` describe the 18 OpenPose body keys
# in image coordinates; None means that key is intentionally absent.
TICKETS = (
    {
        "id": "walk-front-right",
        "text": "walk diagonally toward image right, face front-right",
        "points": {
            "nose": (276, 155), "neck": (270, 210),
            "r_shoulder": (320, 220), "r_elbow": (363, 285), "r_wrist": (390, 355),
            "l_shoulder": (220, 220), "l_elbow": (175, 275), "l_wrist": (145, 335),
            "r_hip": (300, 392), "r_knee": (352, 522), "r_ankle": (410, 680),
            "l_hip": (240, 392), "l_knee": (175, 500), "l_ankle": (112, 638),
            "r_eye": (290, 149), "l_eye": (260, 149), "r_ear": (307, 158), "l_ear": (243, 158),
        },
    },
    {
        "id": "reach-up-right",
        "text": "stand with weight on the left leg and reach the right hand upward",
        "points": {
            "nose": (260, 165), "neck": (258, 220),
            "r_shoulder": (308, 226), "r_elbow": (344, 140), "r_wrist": (373, 72),
            "l_shoulder": (208, 226), "l_elbow": (175, 310), "l_wrist": (166, 390),
            "r_hip": (290, 404), "r_knee": (307, 547), "r_ankle": (320, 692),
            "l_hip": (230, 404), "l_knee": (218, 547), "l_ankle": (214, 695),
            "r_eye": (274, 158), "l_eye": (246, 158), "r_ear": (291, 166), "l_ear": (230, 166),
        },
    },
)
OPENPOSE_KEYS = (
    "nose", "neck", "r_shoulder", "r_elbow", "r_wrist", "l_shoulder", "l_elbow", "l_wrist",
    "r_hip", "r_knee", "r_ankle", "l_hip", "l_knee", "l_ankle", "r_eye", "l_eye", "r_ear", "l_ear",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / ".tmp/p7-5-4-text-pose-character-lora")
    parser.add_argument("--steps", type=int, default=24)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--lora-scale", type=float, default=0.3)
    parser.add_argument("--lora-dir", type=Path, default=EXPERIMENTAL_LORA)
    return parser.parse_args()


def openpose_renderer():
    """Load only ControlNet Aux's OpenPose code, avoiding broken MediaPipe extras."""
    root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    parent = types.ModuleType("p7_text_pose_aux")
    parent.__path__ = [str(root)]
    sys.modules[parent.__name__] = parent
    directory = root / "open_pose"
    spec = importlib.util.spec_from_file_location(
        "p7_text_pose_aux.open_pose", directory / "__init__.py", submodule_search_locations=[str(directory)]
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("OpenPose renderer is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    body = sys.modules[f"{spec.name}.body"]
    util = sys.modules[f"{spec.name}.util"]
    return body.Keypoint, util.draw_bodypose


def render_openpose(ticket: dict) -> Image.Image:
    points = ticket["points"]
    # Use ControlNet Aux's native OpenPose drawing contract rather than a
    # generic cyan stick figure.  x/y must be normalized to the canvas.
    keypoint_type, draw_bodypose = openpose_renderer()
    keypoints = [
        keypoint_type(x=points[name][0] / SIZE[0], y=points[name][1] / SIZE[1], id=index)
        if name in points else None
        for index, name in enumerate(OPENPOSE_KEYS)
    ]
    canvas = draw_bodypose(np.zeros((SIZE[1], SIZE[0], 3), dtype=np.uint8), keypoints)
    return Image.fromarray(canvas)


def prompt(ticket: dict) -> str:
    return (
        "p7mira, adult Korean woman, "
        f"{IDENTITY['lora_hair_identity_description']}, "
        f"{IDENTITY['lora_eye_identity_description']}, "
        "webtoon watercolor, full body, "
        f"{ticket['text']}, simple pale studio background"
    )


def generate(pipe: StableDiffusionXLControlNetPipeline, ticket: dict, seed: int, steps: int) -> Image.Image:
    return pipe(
        prompt=prompt(ticket), negative_prompt=NEGATIVE, image=render_openpose(ticket), width=SIZE[0], height=SIZE[1],
        num_inference_steps=steps, guidance_scale=7.0, controlnet_conditioning_scale=1.0,
        generator=torch.Generator(device="cuda").manual_seed(seed),
    ).images[0]


def main() -> int:
    args = parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    if not args.lora_dir.is_dir():
        raise FileNotFoundError(f"experimental character LoRA missing: {args.lora_dir}")
    args.output.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    controlnet = ControlNetModel.from_pretrained(OPENPOSE, torch_dtype=torch.float16)
    pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
        ANIMAGINE, controlnet=controlnet, torch_dtype=torch.float16, use_safetensors=True, safety_checker=None
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    rows = []
    panels = []
    for offset, ticket in enumerate(TICKETS):
        seed = args.seed + offset
        pose = render_openpose(ticket)
        base = generate(pipe, ticket, seed, args.steps)
        pose.save(args.output / f"{ticket['id']}-text-pose.png")
        base.save(args.output / f"{ticket['id']}-lora-off.png")
        panels.append([ticket, seed, pose, base, None])

    pipe.load_lora_weights(args.lora_dir, adapter_name="p7mira")
    pipe.set_adapters("p7mira", adapter_weights=args.lora_scale)
    for ticket, seed, pose, base, _ in panels:
        lora = generate(pipe, ticket, seed, args.steps)
        lora.save(args.output / f"{ticket['id']}-lora-on.png")
        rows.append({"ticket": ticket["id"], "text": ticket["text"], "seed": seed})
        panels[TICKETS.index(ticket)][4] = lora

    sheet = Image.new("RGB", (SIZE[0] * 3, (SIZE[1] + 30) * len(panels)), "white")
    draw = ImageDraw.Draw(sheet)
    for row, (ticket, _seed, pose, base, lora) in enumerate(panels):
        ticket_id = ticket["id"]
        top = row * (SIZE[1] + 30)
        for column, (label, image) in enumerate((("text pose", pose), ("LoRA off", base), ("LoRA on", lora))):
            draw.text((column * SIZE[0] + 6, top + 6), f"{ticket_id}: {label}", fill="black")
            sheet.paste(image, (column * SIZE[0], top + 30))
    sheet.save(args.output / "text-pose-character-lora-on-off-contact-sheet.png")
    report = {
        "purpose": "text pose ticket + OpenPose ControlNet + experimental character LoRA off/on",
        "base_model": str(ANIMAGINE), "controlnet": str(OPENPOSE), "lora": str(args.lora_dir),
        "image_reference_inputs": [], "steps": args.steps, "lora_scale": args.lora_scale,
        "peak_vram_mib": round(torch.cuda.max_memory_allocated() / 1024**2, 1),
        "seconds": round(time.perf_counter() - started, 2), "rows": rows,
        "human_review": "pending; do not treat the experimental LoRA or output as an approved production asset",
    }
    (args.output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

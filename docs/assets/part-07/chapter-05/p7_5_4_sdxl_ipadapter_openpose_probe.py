#!/usr/bin/env python3
"""Compare SDXL OpenPose cuts with IP-Adapter identity off/on on 8 GB offload."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
import sysconfig
import types

import torch
from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline
from PIL import Image, ImageDraw


ANIMAGINE = Path("/home/cbsim/.cache/huggingface/hub/models--cagliostrolab--animagine-xl-4.0/snapshots/2b7c1b397761bf5bd3cc42e5b39ec99314a75a96")
CONTROLNET = Path("/home/cbsim/.cache/huggingface/hub/models--xinsir--controlnet-openpose-sdxl-1.0/snapshots/23f966cd5cfdd3f7729c903e243d87152162d2b7")
IP_ADAPTER = Path("/home/cbsim/.cache/huggingface/hub/models--h94--IP-Adapter/snapshots/018e402774aeeddd60609b4ecdb7e298259dc729")
ANNOTATORS = Path("/home/cbsim/.cache/huggingface/hub/models--lllyasviel--Annotators/snapshots/982e7edaec38759d914a963c48c4726685de7d96")
NEGATIVE = "multiple people, cropped body, cut off feet, extra bag, broken strap, deformed hands, text, watermark"
SCENES = {
    "mira-heldout-01": "apartment kitchen, side full body, left hand closes cupboard",
    "mira-heldout-02": "open ferry deck, three-quarter full body, right hand holds railing",
    "mira-heldout-03": "cinema foyer at night, low side three-quarter full body, left hand picks up ticket",
    "mira-heldout-04": "ceramics workshop, front three-quarter full body, right hand places cup",
}


def detector_class():
    root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    parent = types.ModuleType("p7_sdxl_pose_aux")
    parent.__path__ = [str(root)]
    sys.modules[parent.__name__] = parent
    directory = root / "open_pose"
    spec = importlib.util.spec_from_file_location("p7_sdxl_pose_aux.open_pose", directory / "__init__.py", submodule_search_locations=[str(directory)])
    if spec is None or spec.loader is None:
        raise RuntimeError("OpenPose implementation is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.OpenposeDetector


def prompt(source_id: str) -> str:
    return f"anime style, adult woman, teal bob, silver hair clip, white jacket, charcoal shirt, teal wide-leg trousers, white sneakers, navy crossbody bag, clean webtoon line art, {SCENES[source_id]}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path)
    parser.add_argument("reference", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    rows = [json.loads(line) for line in (args.dataset / "heldout" / "metadata.jsonl").read_text().splitlines()]
    args.output.mkdir(parents=True, exist_ok=True)
    detector = detector_class().from_pretrained(ANNOTATORS)
    controlnet = ControlNetModel.from_pretrained(CONTROLNET, torch_dtype=torch.float16)
    pipe = StableDiffusionXLControlNetPipeline.from_pretrained(ANIMAGINE, controlnet=controlnet, torch_dtype=torch.float16, use_safetensors=True, safety_checker=None)
    pipe.load_ip_adapter(str(IP_ADAPTER), subfolder="sdxl_models", weight_name="ip-adapter_sdxl.safetensors", image_encoder_folder="image_encoder")
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    reference_paths = [
        args.reference,
        args.reference.with_name("p7-5-2-mira-single-reference-05-front.png"),
        args.reference.with_name("p7-5-2-mira-single-reference-13-wave.png"),
        args.reference.with_name("p7-5-2-mira-detail-01-face-three-quarter.png"),
        args.reference.with_name("p7-5-2-mira-detail-02-hands-bag.png"),
    ]
    references = [Image.open(path).convert("RGB") for path in reference_paths]
    panels = []
    for index, row in enumerate(rows, 1):
        source = Image.open(args.dataset / "heldout" / row["file_name"]).convert("RGB")
        pose = detector(source, hand_and_face=False).convert("RGB").resize((512, 768))
        text = prompt(row["source_id"])
        seed = 4600 + index
        common = dict(prompt=text, negative_prompt=NEGATIVE, image=pose, ip_adapter_image=[references], width=512, height=768, num_inference_steps=15, guidance_scale=7.0, controlnet_conditioning_scale=1.1)
        pipe.set_ip_adapter_scale(0.0)
        off = pipe(**common, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]
        pipe.set_ip_adapter_scale(0.45)
        on = pipe(**common, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]
        panels.append((row["source_id"], pose, off, on))
    sheet = Image.new("RGB", (1536, len(panels) * 792), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (source_id, pose, off, on) in enumerate(panels):
        top = index * 792
        draw.text((6, top + 5), f"{source_id} pose", fill="black")
        draw.text((518, top + 5), "IP-Adapter off", fill="black")
        draw.text((1030, top + 5), "IP-Adapter on", fill="black")
        sheet.paste(pose, (0, top + 24)); sheet.paste(off, (512, top + 24)); sheet.paste(on, (1024, top + 24))
    sheet.save(args.output / "sdxl-ipadapter-openpose-on-off-contact-sheet.png")
    print(args.output / "sdxl-ipadapter-openpose-on-off-contact-sheet.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

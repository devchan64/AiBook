#!/usr/bin/env python3
"""Preflight separate SDXL Plus and Plus Face IP-Adapter conditions on 8 GB VRAM."""

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
IP_ADAPTER = Path("/home/cbsim/.cache/huggingface/models--h94--IP-Adapter/snapshots/018e402774aeeddd60609b4ecdb7e298259dc729")
ANNOTATORS = Path("/home/cbsim/.cache/huggingface/hub/models--lllyasviel--Annotators/snapshots/982e7edaec38759d914a963c48c4726685de7d96")
NEGATIVE = "multiple people, cropped body, cut off feet, extra bag, broken strap, deformed hands, text, watermark"
PROMPT = "anime style, adult woman, teal bob, silver hair clip, white jacket, charcoal shirt, teal wide-leg trousers, white sneakers, navy crossbody bag, clean webtoon line art, apartment kitchen, side full body, left hand closes cupboard"


def detector_class():
    root = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    parent = types.ModuleType("p7_sdxl_plus_face_aux")
    parent.__path__ = [str(root)]
    sys.modules[parent.__name__] = parent
    directory = root / "open_pose"
    spec = importlib.util.spec_from_file_location("p7_sdxl_plus_face_aux.open_pose", directory / "__init__.py", submodule_search_locations=[str(directory)])
    if spec is None or spec.loader is None:
        raise RuntimeError("OpenPose implementation is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.OpenposeDetector


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path)
    parser.add_argument("reference_dir", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--load-only", action="store_true")
    parser.add_argument("--adapter-mode", choices=("plus", "dual"), default="dual")
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    args.output.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(line) for line in (args.dataset / "heldout" / "metadata.jsonl").read_text().splitlines()]
    row = next(item for item in rows if item["source_id"] == "mira-heldout-01")
    source = Image.open(args.dataset / "heldout" / row["file_name"]).convert("RGB")
    global_reference = Image.open(args.reference_dir / "p7-5-1-mira-single-reference-01.png").convert("RGB")
    face_reference = Image.open(args.reference_dir / "p7-5-1-mira-detail-01-face-three-quarter.png").convert("RGB")

    detector = detector_class().from_pretrained(ANNOTATORS)
    pose = detector(source, hand_and_face=False).convert("RGB").resize((512, 768))
    controlnet = ControlNetModel.from_pretrained(CONTROLNET, torch_dtype=torch.float16)
    pipe = StableDiffusionXLControlNetPipeline.from_pretrained(ANIMAGINE, controlnet=controlnet, torch_dtype=torch.float16, use_safetensors=True, safety_checker=None)
    if args.adapter_mode == "plus":
        pipe.load_ip_adapter(str(IP_ADAPTER), subfolder="sdxl_models", weight_name="ip-adapter-plus_sdxl_vit-h.safetensors", image_encoder_folder="models/image_encoder")
        adapter_images = global_reference
        first_scale, second_scale = 0.0, 0.35
        first_label, second_label = "IP-Adapter off", "Plus global"
        adapter_names = ["ip-adapter-plus_sdxl_vit-h.safetensors"]
    else:
        pipe.load_ip_adapter(
            [str(IP_ADAPTER), str(IP_ADAPTER)],
            subfolder=["sdxl_models", "sdxl_models"],
            weight_name=["ip-adapter-plus_sdxl_vit-h.safetensors", "ip-adapter-plus-face_sdxl_vit-h.safetensors"],
            image_encoder_folder="models/image_encoder",
        )
        adapter_images = [global_reference, face_reference]
        first_scale, second_scale = [0.35, 0.0], [0.35, 0.20]
        first_label, second_label = "Plus global", "Plus global + Plus Face"
        adapter_names = ["ip-adapter-plus_sdxl_vit-h.safetensors", "ip-adapter-plus-face_sdxl_vit-h.safetensors"]
    if args.load_only:
        print(f"Loaded {args.adapter_mode} SDXL IP-Adapter configuration with the ViT-H image encoder.")
        return 0
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    common = dict(
        prompt=PROMPT,
        negative_prompt=NEGATIVE,
        image=pose,
        ip_adapter_image=adapter_images,
        width=512,
        height=768,
        num_inference_steps=15,
        guidance_scale=7.0,
        controlnet_conditioning_scale=1.1,
    )
    seed = 4801
    pipe.set_ip_adapter_scale(first_scale)
    global_only = pipe(**common, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]
    pipe.set_ip_adapter_scale(second_scale)
    global_and_face = pipe(**common, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]

    sheet = Image.new("RGB", (1536, 792), "white")
    draw = ImageDraw.Draw(sheet)
    for x, label, image in ((0, "OpenPose", pose), (512, first_label, global_only), (1024, second_label, global_and_face)):
        draw.text((x + 6, 5), label, fill="black")
        sheet.paste(image, (x, 24))
    output_stem = "p7-5-3-sdxl-plus-ipadapter-preflight" if args.adapter_mode == "plus" else "p7-5-3-sdxl-plus-face-ipadapter-preflight"
    image_path = args.output / f"{output_stem}.png"
    sheet.save(image_path)
    record = {
        "status": "generated_for_review",
        "base_model": "cagliostrolab/animagine-xl-4.0 (SDXL)",
        "controlnet": "xinsir/controlnet-openpose-sdxl-1.0",
        "image_encoder": "h94/IP-Adapter models/image_encoder (ViT-H)",
        "adapter_mode": args.adapter_mode,
        "adapters": adapter_names,
        "references": [global_reference.name, face_reference.name],
        "scales": {"first": first_scale, "second": second_scale},
        "size": [512, 768],
        "steps": 15,
        "seed": seed,
        "result": image_path.name,
    }
    (args.output / f"{output_stem}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(image_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

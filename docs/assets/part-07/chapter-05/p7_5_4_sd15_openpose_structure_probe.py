#!/usr/bin/env python3
"""Compare SD 1.5 ControlNet off/on using pose-only held-out structure maps."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
import sysconfig
import types

from huggingface_hub import snapshot_download
import torch
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline
from PIL import Image, ImageDraw


SD15_REPOSITORY = "stable-diffusion-v1-5/stable-diffusion-v1-5"
OPENPOSE_CONTROLNET_REPOSITORY = "lllyasviel/control_v11p_sd15_openpose"
ANNOTATOR_REPOSITORY = "lllyasviel/Annotators"
HF_HUB_CACHE = Path(__file__).resolve().parents[4] / ".tmp" / "download" / "huggingface" / "hub"
NEGATIVE_PROMPT = "multiple people, cropped body, cut off feet, missing bag, extra bag, broken strap, deformed hands, text, watermark, manga screentone, heavy shadow"
SCENE_PROMPTS = {
    "mira-heldout-01": "apartment kitchen, side full body, left hand closes cupboard",
    "mira-heldout-02": "open ferry deck, three-quarter full body, right hand holds railing",
    "mira-heldout-03": "cinema foyer at night, low side three-quarter full body, left hand picks up ticket",
    "mira-heldout-04": "ceramics workshop, front three-quarter full body, right hand places cup",
}


def openpose_detector_class():
    """Load only controlnet_aux.open_pose, avoiding its incompatible MediaPipe extras."""
    package_dir = Path(sysconfig.get_paths()["purelib"]) / "controlnet_aux"
    package_name = "p7_openpose_aux"
    package = types.ModuleType(package_name)
    package.__path__ = [str(package_dir)]
    sys.modules[package_name] = package
    openpose_dir = package_dir / "open_pose"
    spec = importlib.util.spec_from_file_location(
        f"{package_name}.open_pose",
        openpose_dir / "__init__.py",
        submodule_search_locations=[str(openpose_dir)],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load the cached OpenPose implementation")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.OpenposeDetector


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=384)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--steps", type=int, default=25)
    parser.add_argument("--guidance", type=float, default=7.0)
    return parser.parse_args()


def prompt_for(source_id: str) -> str:
    return (
        "adult woman, teal bob, white jacket, charcoal shirt, teal wide-leg trousers, white sneakers, "
        "navy crossbody bag, clean webtoon line art, low-saturation flat colors, "
        f"{SCENE_PROMPTS[source_id]}"
    )


def sheet(rows: list[tuple[str, Image.Image, Image.Image, Image.Image]], output: Path) -> None:
    label_height = 24
    image_width, image_height = 384, 512
    canvas = Image.new("RGB", (image_width * 3, len(rows) * (image_height + label_height)), "white")
    draw = ImageDraw.Draw(canvas)
    for index, (source_id, pose, baseline, controlled) in enumerate(rows):
        top = index * (image_height + label_height)
        draw.text((6, top + 5), f"{source_id} pose map", fill="black")
        draw.text((image_width + 6, top + 5), "ControlNet off", fill="black")
        draw.text((image_width * 2 + 6, top + 5), "ControlNet on", fill="black")
        canvas.paste(pose, (0, top + label_height))
        canvas.paste(baseline, (image_width, top + label_height))
        canvas.paste(controlled, (image_width * 2, top + label_height))
    canvas.save(output)


def main() -> int:
    args = parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the structure probe")
    rows = [json.loads(line) for line in (args.dataset / "heldout" / "metadata.jsonl").read_text().splitlines()]
    if len(rows) != 4:
        raise ValueError("P7-5.2 requires exactly four held-out rows")
    args.output.mkdir(parents=True, exist_ok=True)
    annotator_path = Path(
        snapshot_download(ANNOTATOR_REPOSITORY, cache_dir=HF_HUB_CACHE, local_files_only=True)
    )
    detector = openpose_detector_class().from_pretrained(annotator_path, local_files_only=True)
    controlnet_path = Path(
        snapshot_download(
            OPENPOSE_CONTROLNET_REPOSITORY, cache_dir=HF_HUB_CACHE, local_files_only=True
        )
    )
    sd15_path = Path(
        snapshot_download(SD15_REPOSITORY, cache_dir=HF_HUB_CACHE, local_files_only=True)
    )
    controlnet = ControlNetModel.from_pretrained(controlnet_path, torch_dtype=torch.float16, variant="fp16", local_files_only=True)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(sd15_path, controlnet=controlnet, torch_dtype=torch.float16, safety_checker=None, local_files_only=True).to("cuda")
    pipe.enable_attention_slicing()
    pipe.set_progress_bar_config(disable=True)
    torch.cuda.reset_peak_memory_stats()
    panel_rows: list[tuple[str, Image.Image, Image.Image, Image.Image]] = []
    report_rows: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        source = args.dataset / "heldout" / row["file_name"]
        pose = detector(Image.open(source).convert("RGB"), hand_and_face=False).convert("RGB").resize((args.width, args.height))
        pose_name = f"{row['source_id']}-openpose.png"
        pose.save(args.output / pose_name)
        prompt = prompt_for(row["source_id"])
        token_count = len(pipe.tokenizer(prompt, truncation=False).input_ids)
        if token_count > pipe.tokenizer.model_max_length:
            raise ValueError(f"prompt for {row['source_id']} has {token_count} tokens")
        seed = 4500 + index
        shared = {
            "prompt": prompt,
            "negative_prompt": NEGATIVE_PROMPT,
            "image": pose,
            "width": args.width,
            "height": args.height,
            "num_inference_steps": args.steps,
            "guidance_scale": args.guidance,
        }
        baseline = pipe(**shared, controlnet_conditioning_scale=0.0, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]
        controlled = pipe(**shared, controlnet_conditioning_scale=1.0, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]
        off_name = f"{row['source_id']}-controlnet-off.png"
        on_name = f"{row['source_id']}-controlnet-on.png"
        baseline.save(args.output / off_name)
        controlled.save(args.output / on_name)
        panel_rows.append((row["source_id"], pose, baseline, controlled))
        report_rows.append({"source_id": row["source_id"], "seed": seed, "prompt": prompt, "pose_map": pose_name, "controlnet_off": off_name, "controlnet_on": on_name})
    sheet_name = "sd15-openpose-controlnet-on-off-contact-sheet.png"
    sheet(panel_rows, args.output / sheet_name)
    (args.output / "result.json").write_text(json.dumps({
        "base_model": "stable-diffusion-v1-5/stable-diffusion-v1-5",
        "controlnet": "lllyasviel/control_v11p_sd15_openpose",
        "control_input": "OpenPose body map extracted from held-out source image; no source colors, face, clothing, or background are passed to ControlNet",
        "resolution": [args.width, args.height],
        "inference_steps": args.steps,
        "guidance_scale": args.guidance,
        "controlnet_scales": [0.0, 1.0],
        "peak_vram_mib": round(torch.cuda.max_memory_allocated() / 1024**2, 1),
        "panels": report_rows,
        "contact_sheet": sheet_name,
        "quality_status": "review_required",
    }, indent=2) + "\n")
    print(args.output / sheet_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

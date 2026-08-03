#!/usr/bin/env python3
"""Compare cached SD 1.5 bases with the P7-5.1 compact held-out prompts."""

from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw


MODELS = {
    "sd15": {
        "path": "/home/cbsim/.cache/huggingface/hub/models--stable-diffusion-v1-5--stable-diffusion-v1-5/snapshots/451f4fe16113bff5a5d2269ed5ad43b0592e9a14",
        "variant": None,
    },
    "wd15": {
        "path": "/home/cbsim/.cache/huggingface/hub/models--waifu-diffusion--wd-1-5-beta3/snapshots/9c7a5d539bb3e89481d9a6303bdb56cad535f37f",
        "variant": "fp16",
    },
}
SCENE_PROMPTS = {
    "mira-heldout-01": "apartment kitchen, side full body, left hand closes cupboard",
    "mira-heldout-02": "open ferry deck, three-quarter full body, right hand holds railing",
    "mira-heldout-03": "cinema foyer at night, low side three-quarter full body, left hand picks up ticket",
    "mira-heldout-04": "ceramics workshop, front three-quarter full body, right hand places cup",
}
NEGATIVE_PROMPT = "multiple people, cropped body, cut off feet, missing bag, extra bag, broken strap, deformed hands, text, watermark, manga screentone, heavy shadow"


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
        "woman, teal bob, silver right hair clip, white jacket, charcoal shirt, teal wide-leg trousers, "
        "white sneakers, navy flap crossbody bag at right hip, one diagonal strap, clean webtoon line art, "
        f"low-saturation flat colors, {SCENE_PROMPTS[source_id]}"
    )


def make_sheet(rows: list[tuple[str, Image.Image, Image.Image]], output: Path) -> None:
    label_height = 24
    sheet = Image.new("RGB", (768, len(rows) * (512 + label_height)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (source_id, sd15, wd15) in enumerate(rows):
        top = index * (512 + label_height)
        draw.text((6, top + 5), f"{source_id}  SD 1.5", fill="black")
        draw.text((390, top + 5), f"{source_id}  WD 1.5", fill="black")
        sheet.paste(sd15, (0, top + label_height))
        sheet.paste(wd15, (384, top + label_height))
    sheet.save(output)


def main() -> int:
    args = parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the base probe")
    rows = [json.loads(line) for line in (args.dataset / "heldout" / "metadata.jsonl").read_text().splitlines()]
    if len(rows) != 4:
        raise ValueError("P7-5.1 requires exactly four held-out rows")
    args.output.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, list[Image.Image]] = {}
    report: dict[str, object] = {"models": {}, "panels": []}
    for model_id, spec in MODELS.items():
        kwargs = {"torch_dtype": torch.float16, "safety_checker": None}
        if spec["variant"]:
            kwargs["variant"] = spec["variant"]
        torch.cuda.reset_peak_memory_stats()
        pipe = StableDiffusionPipeline.from_pretrained(spec["path"], **kwargs).to("cuda")
        pipe.set_progress_bar_config(disable=True)
        images: list[Image.Image] = []
        for index, row in enumerate(rows, start=1):
            prompt = prompt_for(row["source_id"])
            token_count = len(pipe.tokenizer(prompt, truncation=False).input_ids)
            if token_count > pipe.tokenizer.model_max_length:
                raise ValueError(f"prompt for {row['source_id']} has {token_count} tokens")
            image = pipe(
                prompt=prompt,
                negative_prompt=NEGATIVE_PROMPT,
                width=args.width,
                height=args.height,
                num_inference_steps=args.steps,
                guidance_scale=args.guidance,
                generator=torch.Generator(device="cuda").manual_seed(4300 + index),
            ).images[0]
            filename = f"{row['source_id']}-{model_id}.png"
            image.save(args.output / filename)
            images.append(image)
            if model_id == "sd15":
                report["panels"].append({"source_id": row["source_id"], "seed": 4300 + index, "prompt": prompt})
        outputs[model_id] = images
        report["models"][model_id] = {"path": spec["path"], "peak_vram_mib": round(torch.cuda.max_memory_allocated() / 1024**2, 1)}
        del pipe
        gc.collect()
        torch.cuda.empty_cache()
    sheet_file = "prompt-only-base-probe-contact-sheet.png"
    make_sheet([(row["source_id"], outputs["sd15"][index], outputs["wd15"][index]) for index, row in enumerate(rows)], args.output / sheet_file)
    report["resolution"] = [args.width, args.height]
    report["inference_steps"] = args.steps
    report["guidance_scale"] = args.guidance
    report["negative_prompt"] = NEGATIVE_PROMPT
    report["contact_sheet"] = sheet_file
    report["status"] = "review_required"
    (args.output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(args.output / sheet_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

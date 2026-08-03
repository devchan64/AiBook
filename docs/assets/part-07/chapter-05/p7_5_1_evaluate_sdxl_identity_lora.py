#!/usr/bin/env python3
"""Render fixed held-out SDXL LoRA off/on comparisons with 8 GB CPU offload."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from diffusers import StableDiffusionXLPipeline
from PIL import Image, ImageDraw


SCENES = {
    "mira-heldout-01": "apartment kitchen, side full body, left hand closes cupboard",
    "mira-heldout-02": "open ferry deck, three-quarter full body, right hand holds railing",
    "mira-heldout-03": "cinema foyer at night, low side three-quarter full body, left hand picks up ticket",
    "mira-heldout-04": "ceramics workshop, front three-quarter full body, right hand places cup",
}
NEGATIVE = "multiple people, cropped body, cut off feet, extra bag, broken strap, deformed hands, text, watermark, photorealistic"


def prompt(source_id: str) -> str:
    return (
        "p7mira, woman, teal bob, silver clip, white jacket, teal trousers, white sneakers, "
        f"navy flap bag, diagonal strap, webtoon line art, {SCENES[source_id]}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("adapter", type=Path)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=384)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--guidance", type=float, default=7.0)
    parser.add_argument("--lora-scale", type=float, default=1.0)
    parser.add_argument("--source-ids", nargs="+", choices=tuple(SCENES), default=tuple(SCENES))
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    all_rows = [json.loads(line) for line in (args.dataset / "heldout" / "metadata.jsonl").read_text().splitlines()]
    if {row["source_id"] for row in all_rows} != set(SCENES):
        raise ValueError("held-out rows do not match the P7-5.1 contract")
    rows_by_id = {row["source_id"]: row for row in all_rows}
    rows = [rows_by_id[source_id] for source_id in args.source_ids]
    args.output.mkdir(parents=True, exist_ok=True)
    pipe = StableDiffusionXLPipeline.from_pretrained(args.model, torch_dtype=torch.float16, use_safetensors=True)
    pipe.enable_sequential_cpu_offload()
    pipe.vae.enable_slicing()
    pipe.set_progress_bar_config(disable=True)
    results: list[tuple[str, Image.Image, Image.Image]] = []
    report_rows: list[dict[str, object]] = []
    for result_index, row in enumerate(rows):
        index = list(SCENES).index(row["source_id"]) + 1
        text = prompt(row["source_id"])
        if len(pipe.tokenizer(text, truncation=False).input_ids) > pipe.tokenizer.model_max_length:
            raise ValueError(f"prompt too long for {row['source_id']}")
        seed = 5200 + index
        baseline = pipe(prompt=text, negative_prompt=NEGATIVE, width=args.width, height=args.height, num_inference_steps=args.steps, guidance_scale=args.guidance, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]
        baseline_file = f"heldout-{index:02d}-lora-off.png"
        baseline.save(args.output / baseline_file)
        results.append((row["source_id"], baseline, Image.new("RGB", baseline.size)))
        report_rows.append({"source_id": row["source_id"], "seed": seed, "prompt": text, "lora_off": baseline_file})
    pipe.load_lora_weights(args.adapter, weight_name="pytorch_lora_weights.safetensors", adapter_name="p7mira")
    pipe.set_adapters("p7mira", adapter_weights=args.lora_scale)
    for result_index, row in enumerate(rows):
        index = list(SCENES).index(row["source_id"]) + 1
        text = prompt(row["source_id"])
        seed = 5200 + index
        adapted = pipe(prompt=text, negative_prompt=NEGATIVE, width=args.width, height=args.height, num_inference_steps=args.steps, guidance_scale=args.guidance, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]
        adapted_file = f"heldout-{index:02d}-lora-on.png"
        adapted.save(args.output / adapted_file)
        results[result_index] = (row["source_id"], results[result_index][1], adapted)
        report_rows[result_index]["lora_on"] = adapted_file
    sheet = Image.new("RGB", (args.width * 2, len(results) * (args.height + 24)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (source_id, baseline, adapted) in enumerate(results):
        top = index * (args.height + 24)
        draw.text((6, top + 5), f"{source_id} LoRA off", fill="black")
        draw.text((args.width + 6, top + 5), f"{source_id} LoRA on", fill="black")
        sheet.paste(baseline, (0, top + 24))
        sheet.paste(adapted, (args.width, top + 24))
    sheet_path = args.output / "heldout-sdxl-lora-on-off-contact-sheet.png"
    sheet.save(sheet_path)
    (args.output / "evaluation.json").write_text(json.dumps({
        "model": str(args.model), "adapter": str(args.adapter), "resolution": [args.width, args.height],
        "steps": args.steps, "guidance": args.guidance, "lora_scale": args.lora_scale,
        "negative_prompt": NEGATIVE, "panels": report_rows, "contact_sheet": sheet_path.name,
        "quality_status": "review_required",
    }, ensure_ascii=False, indent=2) + "\n")
    print(sheet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

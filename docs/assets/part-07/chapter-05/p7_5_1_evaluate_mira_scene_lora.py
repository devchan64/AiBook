#!/usr/bin/env python3
"""Render fixed-prompt held-out LoRA off/on comparisons for P7-5.1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw


NEGATIVE_PROMPT = "multiple people, cropped body, cut off feet, missing bag, extra bag, broken strap, deformed hands, text, watermark, manga screentone, heavy shadow"
SCENE_PROMPTS = {
    "mira-heldout-01": "apartment kitchen, side full body, left hand closes cupboard",
    "mira-heldout-02": "open ferry deck, three-quarter full body, right hand holds railing",
    "mira-heldout-03": "cinema foyer at night, low side three-quarter full body, left hand picks up ticket",
    "mira-heldout-04": "ceramics workshop, front three-quarter full body, right hand places cup",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("adapter", type=Path)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=384)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--steps", type=int, default=25)
    parser.add_argument("--guidance", type=float, default=7.0)
    parser.add_argument("--lora-scale", type=float, default=1.0)
    return parser.parse_args()


def render(pipe: StableDiffusionPipeline, prompt: str, seed: int, args: argparse.Namespace) -> Image.Image:
    generator = torch.Generator(device="cuda").manual_seed(seed)
    return pipe(
        prompt=prompt,
        negative_prompt=NEGATIVE_PROMPT,
        width=args.width,
        height=args.height,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance,
        generator=generator,
    ).images[0]


def compact_prompt(source_id: str) -> str:
    scene = SCENE_PROMPTS[source_id]
    return (
        "p7mira, woman, teal bob, silver right hair clip, white jacket, charcoal shirt, "
        "teal wide-leg trousers, white sneakers, "
        "navy flap crossbody bag at right hip, one diagonal strap, clean webtoon line art, "
        f"low-saturation flat colors, {scene}"
    )


def contact_sheet(rows: list[tuple[str, Image.Image, Image.Image]], output: Path) -> None:
    label_height = 24
    sheet = Image.new("RGB", (768, len(rows) * (512 + label_height)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (panel_id, baseline, adapted) in enumerate(rows):
        top = index * (512 + label_height)
        draw.text((6, top + 5), f"{panel_id}  LoRA off", fill="black")
        draw.text((390, top + 5), f"{panel_id}  LoRA on", fill="black")
        sheet.paste(baseline, (0, top + label_height))
        sheet.paste(adapted, (384, top + label_height))
    sheet.save(output)


def main() -> int:
    args = parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for held-out rendering")
    rows = [json.loads(line) for line in (args.dataset / "heldout" / "metadata.jsonl").read_text().splitlines()]
    if len(rows) != 4:
        raise ValueError("P7-5.1 requires exactly four held-out rows")
    args.output.mkdir(parents=True, exist_ok=True)
    pipe = StableDiffusionPipeline.from_pretrained(args.model, torch_dtype=torch.float16, safety_checker=None).to("cuda")
    pipe.set_progress_bar_config(disable=True)
    prompts = [compact_prompt(row["source_id"]) for row in rows]
    for row, prompt in zip(rows, prompts, strict=True):
        token_count = len(pipe.tokenizer(prompt, truncation=False).input_ids)
        if token_count > pipe.tokenizer.model_max_length:
            raise ValueError(f"prompt for {row['source_id']} has {token_count} tokens; shorten the contract")
    results: list[tuple[str, Image.Image, Image.Image]] = []
    report_rows: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        panel_id = f"heldout-{index:02d}"
        seed = 4200 + index
        baseline = render(pipe, prompts[index - 1], seed, args)
        baseline_file = f"{panel_id}-lora-off.png"
        baseline.save(args.output / baseline_file)
        results.append((panel_id, baseline, Image.new("RGB", baseline.size)))
        report_rows.append({"panel_id": panel_id, "source_id": row["source_id"], "seed": seed, "prompt": prompts[index - 1], "lora_off": baseline_file})
    pipe.load_lora_weights(args.adapter, weight_name="pytorch_lora_weights.safetensors", adapter_name="p7mira")
    pipe.set_adapters("p7mira", adapter_weights=args.lora_scale)
    for index, row in enumerate(rows, start=1):
        panel_id = f"heldout-{index:02d}"
        seed = 4200 + index
        adapted = render(pipe, prompts[index - 1], seed, args)
        adapted_file = f"{panel_id}-lora-on.png"
        adapted.save(args.output / adapted_file)
        results[index - 1] = (panel_id, results[index - 1][1], adapted)
        report_rows[index - 1]["lora_on"] = adapted_file
    sheet_file = "heldout-lora-on-off-contact-sheet.png"
    contact_sheet(results, args.output / sheet_file)
    (args.output / "evaluation.json").write_text(json.dumps({
        "base_model": str(args.model),
        "adapter": str(args.adapter),
        "resolution": [args.width, args.height],
        "inference_steps": args.steps,
        "guidance_scale": args.guidance,
        "lora_scale": args.lora_scale,
        "negative_prompt": NEGATIVE_PROMPT,
        "panels": report_rows,
        "contact_sheet": sheet_file,
        "quality_status": "review_required",
    }, indent=2) + "\n")
    print(args.output / sheet_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

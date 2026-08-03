#!/usr/bin/env python3
"""Test WD 1.5 image-to-image reference retention across P7-5.1 held-out scenes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image, ImageDraw


WD15 = Path("/home/cbsim/.cache/huggingface/hub/models--waifu-diffusion--wd-1-5-beta3/snapshots/9c7a5d539bb3e89481d9a6303bdb56cad535f37f")
NEGATIVE_PROMPT = "multiple people, cropped body, cut off feet, missing bag, extra bag, broken strap, deformed hands, text, watermark, manga screentone, heavy shadow"
SCENE_PROMPTS = {
    "mira-heldout-01": "apartment kitchen, side full body, left hand closes cupboard",
    "mira-heldout-02": "open ferry deck, three-quarter full body, right hand holds railing",
    "mira-heldout-03": "cinema foyer at night, low side three-quarter full body, left hand picks up ticket",
    "mira-heldout-04": "ceramics workshop, front three-quarter full body, right hand places cup",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("reference", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=384)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--strength", type=float, default=0.55)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--guidance", type=float, default=7.0)
    return parser.parse_args()


def reference_canvas(path: Path, width: int, height: int) -> Image.Image:
    image = Image.open(path).convert("RGB")
    scale = min(width / image.width, height / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)))
    canvas = Image.new("RGB", (width, height), "white")
    canvas.paste(resized, ((width - resized.width) // 2, (height - resized.height) // 2))
    return canvas


def prompt_for(source_id: str) -> str:
    return (
        "woman, teal bob, silver right hair clip, white jacket, charcoal shirt, teal wide-leg trousers, "
        "white sneakers, navy flap crossbody bag at right hip, one diagonal strap, clean webtoon line art, "
        f"low-saturation flat colors, {SCENE_PROMPTS[source_id]}"
    )


def make_sheet(reference: Image.Image, rows: list[tuple[str, Image.Image]], output: Path) -> None:
    label_height = 24
    sheet = Image.new("RGB", (768, len(rows) * (512 + label_height)), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (source_id, image) in enumerate(rows):
        top = index * (512 + label_height)
        draw.text((6, top + 5), "approved reference input", fill="black")
        draw.text((390, top + 5), f"{source_id} img2img", fill="black")
        sheet.paste(reference, (0, top + label_height))
        sheet.paste(image, (384, top + label_height))
    sheet.save(output)


def main() -> int:
    args = parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the img2img probe")
    rows = [json.loads(line) for line in (args.dataset / "heldout" / "metadata.jsonl").read_text().splitlines()]
    if len(rows) != 4:
        raise ValueError("P7-5.1 requires exactly four held-out rows")
    args.output.mkdir(parents=True, exist_ok=True)
    reference = reference_canvas(args.reference, args.width, args.height)
    pipe = StableDiffusionImg2ImgPipeline.from_pretrained(WD15, torch_dtype=torch.float16, variant="fp16", safety_checker=None).to("cuda")
    pipe.set_progress_bar_config(disable=True)
    torch.cuda.reset_peak_memory_stats()
    results: list[tuple[str, Image.Image]] = []
    report_rows: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        prompt = prompt_for(row["source_id"])
        token_count = len(pipe.tokenizer(prompt, truncation=False).input_ids)
        if token_count > pipe.tokenizer.model_max_length:
            raise ValueError(f"prompt for {row['source_id']} has {token_count} tokens")
        image = pipe(
            prompt=prompt,
            negative_prompt=NEGATIVE_PROMPT,
            image=reference,
            strength=args.strength,
            num_inference_steps=args.steps,
            guidance_scale=args.guidance,
            generator=torch.Generator(device="cuda").manual_seed(4400 + index),
        ).images[0]
        filename = f"{row['source_id']}-img2img.png"
        image.save(args.output / filename)
        results.append((row["source_id"], image))
        report_rows.append({"source_id": row["source_id"], "seed": 4400 + index, "prompt": prompt, "output": filename})
    sheet_file = "wd15-reference-img2img-contact-sheet.png"
    make_sheet(reference, results, args.output / sheet_file)
    (args.output / "report.json").write_text(json.dumps({
        "model": "waifu-diffusion/wd-1-5-beta3",
        "reference": str(args.reference),
        "resolution": [args.width, args.height],
        "strength": args.strength,
        "inference_steps": args.steps,
        "guidance_scale": args.guidance,
        "peak_vram_mib": round(torch.cuda.max_memory_allocated() / 1024**2, 1),
        "negative_prompt": NEGATIVE_PROMPT,
        "panels": report_rows,
        "contact_sheet": sheet_file,
        "status": "review_required",
    }, indent=2) + "\n")
    print(args.output / sheet_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

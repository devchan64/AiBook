#!/usr/bin/env python3
"""Compare candidate diffusion bases before choosing the P7-5.1 LoRA base."""

from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path
from typing import Any

import torch
from diffusers import StableDiffusionPipeline, StableDiffusionXLPipeline
from PIL import Image, ImageDraw


MODELS: dict[str, dict[str, Any]] = {
    "sd15": {
        "path": "/home/cbsim/.cache/huggingface/hub/models--stable-diffusion-v1-5--stable-diffusion-v1-5/snapshots/451f4fe16113bff5a5d2269ed5ad43b0592e9a14",
        "pipeline": StableDiffusionPipeline,
        "variant": None,
    },
    "wd15": {
        "path": "/home/cbsim/.cache/huggingface/hub/models--waifu-diffusion--wd-1-5-beta3/snapshots/9c7a5d539bb3e89481d9a6303bdb56cad535f37f",
        "pipeline": StableDiffusionPipeline,
        "variant": "fp16",
    },
    "sdxl-base": {
        "path": "/home/cbsim/.cache/huggingface/hub/models--stabilityai--stable-diffusion-xl-base-1.0/snapshots/462165984030d82259a11f4367a4eed129e94a7b",
        "pipeline": StableDiffusionXLPipeline,
        "variant": None,
    },
    "animagine-xl": {
        "path": "/home/cbsim/.cache/huggingface/hub/models--cagliostrolab--animagine-xl-4.0/snapshots/2b7c1b397761bf5bd3cc42e5b39ec99314a75a96",
        "pipeline": StableDiffusionXLPipeline,
        "variant": None,
    },
}
SCENES = {
    "mira-heldout-01": "apartment kitchen, side full body, left hand closes cupboard",
    "mira-heldout-02": "open ferry deck, three-quarter full body, right hand holds railing",
    "mira-heldout-03": "cinema foyer at night, low side three-quarter full body, left hand picks up ticket",
    "mira-heldout-04": "ceramics workshop, front three-quarter full body, right hand places cup",
}
PROMPT_PREFIX = (
    "adult woman, full body, teal bob, silver right hair clip, white cropped jacket, "
    "charcoal shirt, teal wide-leg trousers, white sneakers, navy flap crossbody bag at "
    "right hip, one diagonal strap, clean webtoon line art, low-saturation flat colors"
)
NEGATIVE = "multiple people, cropped body, cut off feet, extra bag, broken strap, deformed hands, text, watermark, photorealistic"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=768)
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--guidance", type=float, default=7.0)
    parser.add_argument("--model-ids", nargs="+", choices=tuple(MODELS), default=tuple(MODELS))
    parser.add_argument("--source-ids", nargs="+", choices=tuple(SCENES), default=tuple(SCENES))
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    all_rows = [json.loads(line) for line in (args.dataset / "heldout" / "metadata.jsonl").read_text().splitlines()]
    if {row["source_id"] for row in all_rows} != set(SCENES):
        raise ValueError("held-out rows do not match the P7-5.1 camera comparison contract")
    rows_by_id = {row["source_id"]: row for row in all_rows}
    rows = [rows_by_id[source_id] for source_id in args.source_ids]
    args.output.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, list[Image.Image]] = {}
    report: dict[str, Any] = {"models": {}, "panels": [], "status": "review_required"}
    for model_id in args.model_ids:
        spec = MODELS[model_id]
        kwargs = {"torch_dtype": torch.float16, "safety_checker": None, "use_safetensors": True}
        if spec["variant"]:
            kwargs["variant"] = spec["variant"]
        torch.cuda.reset_peak_memory_stats()
        pipe = spec["pipeline"].from_pretrained(spec["path"], **kwargs)
        if spec["pipeline"] is StableDiffusionXLPipeline:
            pipe.enable_sequential_cpu_offload()
            pipe.vae.enable_slicing()
        else:
            pipe.to("cuda")
        pipe.set_progress_bar_config(disable=True)
        images: list[Image.Image] = []
        for index, row in enumerate(rows, start=1):
            prompt = f"{PROMPT_PREFIX}, {SCENES[row['source_id']]}"
            token_count = len(pipe.tokenizer(prompt, truncation=False).input_ids)
            if token_count > pipe.tokenizer.model_max_length:
                raise ValueError(f"{model_id} prompt has {token_count} tokens")
            image = pipe(
                prompt=prompt,
                negative_prompt=NEGATIVE,
                width=args.width,
                height=args.height,
                num_inference_steps=args.steps,
                guidance_scale=args.guidance,
                generator=torch.Generator(device="cuda").manual_seed(5100 + index),
            ).images[0]
            image.save(args.output / f"{row['source_id']}-{model_id}.png")
            images.append(image)
            if not report["panels"]:
                report["panels"].append({"source_id": row["source_id"], "seed": 5100 + index, "prompt": prompt})
        outputs[model_id] = images
        report["models"][model_id] = {"path": spec["path"], "peak_vram_mib": round(torch.cuda.max_memory_allocated() / 1024**2, 1)}
        del pipe
        gc.collect()
        torch.cuda.empty_cache()
    label_height = 24
    sheet = Image.new("RGB", (args.width * len(args.model_ids), len(rows) * (args.height + label_height)), "white")
    draw = ImageDraw.Draw(sheet)
    for row_index, row in enumerate(rows):
        top = row_index * (args.height + label_height)
        for model_index, model_id in enumerate(args.model_ids):
            left = model_index * args.width
            draw.text((left + 6, top + 5), f"{row['source_id']} {model_id}", fill="black")
            sheet.paste(outputs[model_id][row_index], (left, top + label_height))
    sheet_path = args.output / "p7-5-1-base-model-selection-contact-sheet.png"
    sheet.save(sheet_path)
    report.update({"resolution": [args.width, args.height], "steps": args.steps, "guidance": args.guidance, "negative_prompt": NEGATIVE, "contact_sheet": sheet_path.name})
    (args.output / "p7-5-1-base-model-selection-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(sheet_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

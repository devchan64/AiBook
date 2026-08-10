#!/usr/bin/env python3
"""Test whether an approved outfit reference restores a masked SDXL jacket edit.

This is a preflight: the source is fixed, pixels outside the operator mask are
restored after generation, and the reference is only the new conditioning
variable relative to the manual-mask baseline.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import StableDiffusionXLInpaintPipeline
from diffusers.image_processor import IPAdapterMaskProcessor
from PIL import Image, ImageDraw, ImageFilter


MODEL_ID = "diffusers/stable-diffusion-xl-1.0-inpainting-0.1"
IP_ADAPTER = Path("/home/cbsim/.cache/huggingface/hub/models--h94--IP-Adapter/snapshots/018e402774aeeddd60609b4ecdb7e298259dc729")


def parse_adapter_scale(value: str) -> float | dict[str, object] | list[object]:
    """Accept the standard scalar or Diffusers' per-UNet-block JSON scale."""
    try:
        return float(value)
    except ValueError:
        parsed = json.loads(value)
        if not isinstance(parsed, (dict, list)):
            raise argparse.ArgumentTypeError("adapter scale JSON must be an object or array")
        return parsed


def all_nonnegative_numbers(value: object) -> bool:
    if isinstance(value, (int, float)):
        return value >= 0
    if isinstance(value, dict):
        return all(all_nonnegative_numbers(item) for item in value.values())
    if isinstance(value, list):
        return all(all_nonnegative_numbers(item) for item in value)
    return False


def gpu_memory_mib() -> int | None:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        return int(result.stdout.splitlines()[0])
    except (IndexError, ValueError):
        return None


def load_mask(path: Path, size: tuple[int, int]) -> Image.Image:
    mask = Image.open(path).convert("L")
    if mask.size != size:
        raise ValueError(f"mask size {mask.size} must match source size {size}")
    if mask.getextrema()[0] == mask.getextrema()[1]:
        raise ValueError("mask must contain both black preserve and white edit pixels")
    return mask


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("mask", type=Path)
    parser.add_argument("outfit_reference", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--negative-prompt", default="changed face, changed hair, changed trousers, changed shoes, changed pose, cropped person, extra limbs, text, watermark")
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--strength", type=float, default=0.75)
    parser.add_argument("--guidance-scale", type=float, default=12.0)
    parser.add_argument("--adapter-scale", type=parse_adapter_scale, default=0.55)
    parser.add_argument(
        "--adapter-weight",
        default="ip-adapter_sdxl.bin",
        help="cached SDXL adapter weight; generic SDXL is the inpaint-compatible baseline",
    )
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=768)
    parser.add_argument(
        "--mask-expand-px",
        type=int,
        default=0,
        help="expand the white editable region at source resolution before resizing",
    )
    parser.add_argument(
        "--padding-mask-crop",
        type=int,
        default=None,
        help="crop around the edit mask with padding, upscale that crop for inpainting, then composite it back",
    )
    parser.add_argument("--mask-feather-px", type=float, default=2.0)
    parser.add_argument(
        "--localize-ip-adapter",
        action="store_true",
        help="apply the same edit region as an IP-Adapter cross-attention mask",
    )
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for this 8 GB preflight")
    if not all(path.is_file() for path in (args.source, args.mask, args.outfit_reference)):
        raise FileNotFoundError("source, mask, and approved outfit reference must exist")
    if not IP_ADAPTER.is_dir():
        raise FileNotFoundError(f"cached IP-Adapter is missing: {IP_ADAPTER}")
    if not 0.0 < args.strength < 1.0 or args.guidance_scale <= 0 or not all_nonnegative_numbers(args.adapter_scale):
        raise ValueError("invalid strength, guidance scale, or adapter scale")
    if args.mask_expand_px < 0:
        raise ValueError("--mask-expand-px must be zero or positive")
    if args.padding_mask_crop is not None and args.padding_mask_crop < 0:
        raise ValueError("--padding-mask-crop must be zero or positive")

    source = Image.open(args.source).convert("RGB")
    mask = load_mask(args.mask, source.size)
    if args.mask_expand_px:
        # MaxFilter dilates the white edit region while preserving black areas.
        mask = mask.filter(ImageFilter.MaxFilter(size=args.mask_expand_px * 2 + 1))
    size = (args.width, args.height)
    source = source.resize(size, Image.Resampling.LANCZOS)
    mask = mask.resize(size, Image.Resampling.NEAREST)
    reference = Image.open(args.outfit_reference).convert("RGB").resize(size, Image.Resampling.LANCZOS)
    args.output.mkdir(parents=True, exist_ok=True)

    before = gpu_memory_mib()
    peak = before or 0
    stop = threading.Event()

    def observe_peak() -> None:
        nonlocal peak
        while not stop.is_set():
            used = gpu_memory_mib()
            if used is not None:
                peak = max(peak, used)
            time.sleep(0.2)

    observer = threading.Thread(target=observe_peak, daemon=True)
    observer.start()
    started = time.monotonic()
    try:
        pipe = StableDiffusionXLInpaintPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
        image_encoder_folder = (
            "models/image_encoder"
            if "plus_sdxl_vit-h" in args.adapter_weight
            else "sdxl_models/image_encoder"
        )
        pipe.load_ip_adapter(
            str(IP_ADAPTER),
            subfolder="sdxl_models",
            weight_name=args.adapter_weight,
            image_encoder_folder=image_encoder_folder,
        )
        pipe.set_ip_adapter_scale(args.adapter_scale)
        pipe.enable_sequential_cpu_offload()
        # Do not enable attention slicing here: this Diffusers release replaces
        # IP-Adapter attention processors with a generic sliced processor.
        pipe.vae.enable_slicing()
        pipe.set_progress_bar_config(disable=True)
        cross_attention_kwargs = None
        if args.localize_ip_adapter:
            processor = IPAdapterMaskProcessor()
            adapter_mask = processor.preprocess([mask], height=args.height, width=args.width)
            adapter_mask = adapter_mask.reshape(1, adapter_mask.shape[0], adapter_mask.shape[2], adapter_mask.shape[3])
            cross_attention_kwargs = {"ip_adapter_masks": [adapter_mask]}
        raw = pipe(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            image=source,
            mask_image=mask,
            ip_adapter_image=reference,
            strength=args.strength,
            guidance_scale=args.guidance_scale,
            num_inference_steps=args.steps,
            width=args.width,
            height=args.height,
            padding_mask_crop=args.padding_mask_crop,
            cross_attention_kwargs=cross_attention_kwargs,
            generator=torch.Generator(device="cuda").manual_seed(args.seed),
        ).images[0]
        if raw.size != source.size:
            raise RuntimeError(f"inpaint output {raw.size} did not match {source.size}")
        composite = Image.composite(raw, source, mask.filter(ImageFilter.GaussianBlur(args.mask_feather_px)))
        source.save(args.output / "source.png")
        mask.save(args.output / "manual-mask.png")
        reference.save(args.output / "outfit-reference.png")
        raw.save(args.output / "raw-model-output.png")
        composite.save(args.output / "inpaint-output.png")
        sheet = Image.new("RGB", (args.width * 4, args.height + 28), "white")
        draw = ImageDraw.Draw(sheet)
        for index, (label, image) in enumerate(
            (("fixed source", source), ("operator mask", mask.convert("RGB")), ("approved outfit reference", reference), ("composited candidate", composite))
        ):
            x = index * args.width
            draw.text((x + 6, 6), label, fill="black")
            sheet.paste(image, (x, 28))
        sheet.save(args.output / "contact-sheet.png")
    finally:
        stop.set()
        observer.join(timeout=2)

    record = {
        "status": "generated_for_human_review",
        "model": MODEL_ID,
        "ip_adapter": f"h94/IP-Adapter sdxl_models/{args.adapter_weight}",
        "source": str(args.source),
        "mask": str(args.mask),
        "outfit_reference": str(args.outfit_reference),
        "prompt": args.prompt,
        "resolution": list(size),
        "steps": args.steps,
        "strength": args.strength,
        "guidance_scale": args.guidance_scale,
        "adapter_scale": args.adapter_scale,
        "mask_expand_px": args.mask_expand_px,
        "padding_mask_crop": args.padding_mask_crop,
        "localize_ip_adapter": args.localize_ip_adapter,
        "seed": args.seed,
        "gpu_memory_before_mib": before,
        "gpu_memory_peak_mib": peak if peak else None,
        "elapsed_seconds": round(time.monotonic() - started, 1),
        "outputs": ["source.png", "manual-mask.png", "outfit-reference.png", "raw-model-output.png", "inpaint-output.png", "contact-sheet.png"],
    }
    (args.output / "run.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output / "inpaint-output.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

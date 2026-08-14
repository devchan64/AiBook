#!/usr/bin/env python3
"""Train a small tag-captioned character LoRA from approved dataset manifests."""

from __future__ import annotations

import argparse
import gc
import json
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as functional
from diffusers import AutoencoderKL, DDPMScheduler, StableDiffusionXLPipeline, UNet2DConditionModel
from diffusers.utils import convert_state_dict_to_diffusers
from peft import LoraConfig
from peft.utils import get_peft_model_state_dict
from PIL import Image
from transformers import AutoTokenizer, CLIPTextModel, CLIPTextModelWithProjection


ROOT = Path("/home/cbsim/ws/AiBook")
ASSETS = ROOT / "docs/assets/part-07/chapter-05"
DEFAULT_DATASET = ROOT / ".tmp/p7-5-4-character-lora-action-36/dataset-manifest.json"
DEFAULT_MODEL = Path(
    "/home/cbsim/.cache/huggingface/hub/models--cagliostrolab--animagine-xl-4.0/"
    "snapshots/2b7c1b397761bf5bd3cc42e5b39ec99314a75a96"
)
IDENTITY_TAGS = (
    "p7mira, 1girl, solo, adult, korean woman, teal blue hair, bob cut, brown eyes, hairclip, "
    "white cropped utility jacket, charcoal crop top, bare midriff, teal wide leg pants, white sneakers, "
    "navy crossbody messenger bag, webtoon style, clean lineart"
)
SOURCES = (
    ("p7-5-2-face-front-reference.png", "face, looking at viewer"),
    ("p7-5-2-face-front-quarter-left-reference.png", "face, looking left, three quarter view"),
    ("p7-5-2-face-front-quarter-right-reference.png", "face, looking right, three quarter view"),
    ("p7-5-2-face-profile-left-reference.png", "face, left profile"),
    ("p7-5-2-face-profile-right-reference.png", "face, right profile"),
    ("p7-5-2-face-rear-reference.png", "back of head"),
    ("p7-5-2-fullbody-front-reference.png", "full body, standing, front view"),
    ("p7-5-2-fullbody-front-quarter-left-reference.png", "full body, standing, left three quarter view"),
    ("p7-5-2-fullbody-front-quarter-right-reference.png", "full body, standing, right three quarter view"),
    ("p7-5-2-fullbody-profile-left-reference.png", "full body, standing, left profile"),
    ("p7-5-2-fullbody-profile-right-reference.png", "full body, standing, right profile"),
    ("p7-5-2-fullbody-rear-reference.png", "full body, standing, back view"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / ".tmp/p7-5-4-tagged-character-lora")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET, help="Prepared dataset-manifest.json")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL, help="SDXL base snapshot used for both training and inference")
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--width", type=int, default=320)
    parser.add_argument("--height", type=int, default=448)
    parser.add_argument(
        "--gradient-checkpointing",
        action="store_true",
        help="Recompute UNet activations during backward pass to fit larger buckets on 8 GB VRAM.",
    )
    parser.add_argument(
        "--aspect-ratio-buckets",
        action="store_true",
        help="Keep square portraits square and full-body sources at their native 2:3 ratio.",
    )
    return parser.parse_args()


def dataset_examples(manifest_path: Path) -> list[tuple[Path, str]]:
    """Read captions from a prepared local dataset without duplicating source PNGs."""
    if not manifest_path.is_file():
        raise FileNotFoundError(f"prepared dataset manifest is missing: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    dataset_dir = manifest_path.parent
    examples: list[tuple[Path, str]] = []
    for record in manifest["sources"]:
        image = dataset_dir / record["dataset_image"]
        caption = dataset_dir / record["dataset_caption"]
        if not image.is_file() or not caption.is_file():
            raise FileNotFoundError(f"prepared dataset entry is missing: {image} or {caption}")
        examples.append((image, caption.read_text(encoding="utf-8").strip()))
    if not examples:
        raise ValueError("prepared dataset contains no training images")
    return examples


def tokenize(tokenizer: AutoTokenizer, caption: str) -> torch.Tensor:
    return tokenizer(
        caption, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt"
    ).input_ids


def dimensions(path: Path, width: int, height: int, aspect_ratio_buckets: bool) -> tuple[int, int]:
    if not aspect_ratio_buckets:
        return width, height
    source_width, source_height = Image.open(path).size
    if source_width == source_height:
        return width, width
    return width, width * 3 // 2


def pixels(path: Path, width: int, height: int) -> torch.Tensor:
    image = Image.open(path).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
    array = np.asarray(image).copy()
    return torch.from_numpy(array).permute(2, 0, 1).float().div(127.5).sub(1.0).unsqueeze(0)


def main() -> int:
    args = parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    examples = dataset_examples(args.dataset)
    args.output.mkdir(parents=True, exist_ok=True)
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.backends.cuda.matmul.allow_tf32 = True
    device, dtype = torch.device("cuda"), torch.bfloat16

    if not args.model.is_dir():
        raise FileNotFoundError(f"SDXL base snapshot is missing: {args.model}")
    tokenizer_1 = AutoTokenizer.from_pretrained(args.model, subfolder="tokenizer", use_fast=False)
    tokenizer_2 = AutoTokenizer.from_pretrained(args.model, subfolder="tokenizer_2", use_fast=False)
    text_1 = CLIPTextModel.from_pretrained(args.model, subfolder="text_encoder", torch_dtype=dtype).eval()
    text_2 = CLIPTextModelWithProjection.from_pretrained(args.model, subfolder="text_encoder_2", torch_dtype=dtype).eval()
    vae = AutoencoderKL.from_pretrained(args.model, subfolder="vae", torch_dtype=dtype).eval()
    for module in (text_1, text_2, vae):
        module.requires_grad_(False)

    # Keep the encoder stages separate from the UNet.  This is essential when
    # the local ComfyUI server already occupies part of an 8 GB GPU.
    cached: list[tuple[torch.Tensor, torch.Tensor, torch.Tensor, int, int]] = []
    for path, caption in examples:
        image_width, image_height = dimensions(path, args.width, args.height, args.aspect_ratio_buckets)
        image = pixels(path, image_width, image_height).to(device=device, dtype=dtype)
        ids_1, ids_2 = tokenize(tokenizer_1, caption).to(device), tokenize(tokenizer_2, caption).to(device)
        with torch.no_grad():
            vae.to(device)
            latents = vae.encode(image).latent_dist.sample().mul_(vae.config.scaling_factor).cpu()
            vae.to("cpu")
            text_1.to(device)
            hidden_1 = text_1(ids_1, output_hidden_states=True).hidden_states[-2].cpu()
            text_1.to("cpu")
            text_2.to(device)
            encoded_2 = text_2(ids_2, output_hidden_states=True)
            hidden_2 = encoded_2.hidden_states[-2].cpu()
            pooled = encoded_2[0].cpu()
            text_2.to("cpu")
        cached.append((latents, torch.cat([hidden_1, hidden_2], dim=-1), pooled, image_width, image_height))
    del vae, text_1, text_2
    gc.collect()
    torch.cuda.empty_cache()

    unet = UNet2DConditionModel.from_pretrained(args.model, subfolder="unet", torch_dtype=dtype)
    scheduler = DDPMScheduler.from_pretrained(args.model, subfolder="scheduler")
    unet.requires_grad_(False)
    unet.add_adapter(LoraConfig(r=8, lora_alpha=8, target_modules=["to_k", "to_q", "to_v", "to_out.0"]))
    if args.gradient_checkpointing:
        unet.enable_gradient_checkpointing()
    unet.to(device)
    optimizer = torch.optim.AdamW((parameter for parameter in unet.parameters() if parameter.requires_grad), lr=args.learning_rate)
    losses: list[float] = []
    peak_mib = 0.0

    for step in range(1, args.steps + 1):
        latents, embeds, pooled, image_width, image_height = cached[(step - 1) % len(cached)]
        latents, embeds, pooled = latents.to(device), embeds.to(device), pooled.to(device)
        noise = torch.randn_like(latents)
        timesteps = torch.randint(0, scheduler.config.num_train_timesteps, (1,), device=device).long()
        noisy = scheduler.add_noise(latents, noise, timesteps)
        time_ids = torch.tensor([[image_height, image_width, 0, 0, image_height, image_width]], device=device, dtype=dtype)
        prediction = unet(noisy, timesteps, encoder_hidden_states=embeds, added_cond_kwargs={"text_embeds": pooled, "time_ids": time_ids}).sample
        loss = functional.mse_loss(prediction.float(), noise.float())
        loss.backward()
        torch.nn.utils.clip_grad_norm_([parameter for parameter in unet.parameters() if parameter.requires_grad], 1.0)
        optimizer.step(); optimizer.zero_grad(set_to_none=True)
        losses.append(float(loss.detach()))
        peak_mib = max(peak_mib, torch.cuda.max_memory_allocated(device) / 1024**2)
        if step == 1 or step % 50 == 0 or step == args.steps:
            print(json.dumps({"step": step, "loss": round(losses[-1], 6), "peak_mib": round(peak_mib, 1)}), flush=True)

    state = convert_state_dict_to_diffusers(get_peft_model_state_dict(unet))
    StableDiffusionXLPipeline.save_lora_weights(args.output, unet_lora_layers=state)
    report = {
        "status": "training_completed", "model": str(args.model), "dataset_manifest": str(args.dataset),
        "training_images": [str(path) for path, _caption in examples],
        "caption_format": "Animagine-compatible tag sequence", "steps": args.steps,
        "resolution": [args.width, args.height], "aspect_ratio_buckets": args.aspect_ratio_buckets,
        "bucket_dimensions": {"square_portrait": [args.width, args.width], "full_body": [args.width, args.width * 3 // 2]} if args.aspect_ratio_buckets else None,
        "rank": 8, "dtype": "bf16", "learning_rate": args.learning_rate, "gradient_checkpointing": args.gradient_checkpointing, "loss_first": losses[0],
        "loss_last": losses[-1], "peak_vram_mib": peak_mib, "adapter": "pytorch_lora_weights.safetensors",
        "scope": "Style-conditioned character identity and approved action-pose diversity; human evaluation remains required.",
    }
    (args.output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run an uncropped SD 1.5 UNet-LoRA anchor profile for P7-5.1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import torch.nn.functional as F
from diffusers import AutoencoderKL, DDPMScheduler, StableDiffusionPipeline, UNet2DConditionModel
from peft import LoraConfig, get_peft_model_state_dict
from PIL import Image
from transformers import CLIPTextModel, CLIPTokenizer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("--width", type=int, default=384)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--rank", type=int, default=8)
    parser.add_argument("--steps", type=int, default=1)
    parser.add_argument("--dtype", choices=["fp16", "bf16", "fp32"], default="bf16")
    parser.add_argument("--save-dir", type=Path)
    return parser.parse_args()


def load_example(dataset: Path, row: dict[str, str], width: int, height: int) -> tuple[torch.Tensor, str]:
    image = Image.open(dataset / "train" / row["file_name"]).convert("RGB")
    scale = min(width / image.width, height / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)))
    canvas = Image.new("RGB", (width, height), "white")
    canvas.paste(resized, ((width - resized.width) // 2, (height - resized.height) // 2))
    pixels = torch.from_numpy(__import__("numpy").asarray(canvas).copy())
    pixels = pixels.permute(2, 0, 1).float().div(127.5).sub(1.0).unsqueeze(0)
    return pixels, row["text"]


def main() -> int:
    args = parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the preflight step")
    if args.steps < 1:
        raise ValueError("--steps must be at least 1")
    torch.manual_seed(4101)
    device = torch.device("cuda")
    dtype = {"fp16": torch.float16, "bf16": torch.bfloat16, "fp32": torch.float32}[args.dtype]
    tokenizer = CLIPTokenizer.from_pretrained(args.model, subfolder="tokenizer")
    text_encoder = CLIPTextModel.from_pretrained(args.model, subfolder="text_encoder", torch_dtype=dtype)
    vae = AutoencoderKL.from_pretrained(args.model, subfolder="vae", torch_dtype=dtype)
    unet = UNet2DConditionModel.from_pretrained(args.model, subfolder="unet", torch_dtype=dtype)
    scheduler = DDPMScheduler.from_pretrained(args.model, subfolder="scheduler")
    text_encoder.requires_grad_(False).to(device)
    vae.requires_grad_(False).to(device)
    unet.requires_grad_(False).to(device)
    unet.add_adapter(LoraConfig(r=args.rank, lora_alpha=args.rank, target_modules=["to_q", "to_k", "to_v", "to_out.0"]))
    unet.enable_gradient_checkpointing()
    trainable = [parameter for parameter in unet.parameters() if parameter.requires_grad]
    optimizer = torch.optim.AdamW(trainable, lr=1e-4)
    rows = [json.loads(line) for line in (args.dataset / "train" / "metadata.jsonl").read_text().splitlines()]
    if not rows:
        raise RuntimeError("train metadata is empty")
    torch.cuda.reset_peak_memory_stats()
    losses: list[float] = []
    failure: str | None = None
    failure_step: int | None = None
    for step in range(args.steps):
        pixels, prompt = load_example(args.dataset, rows[step % len(rows)], args.width, args.height)
        pixels = pixels.to(device=device, dtype=dtype)
        token_ids = tokenizer(prompt, max_length=tokenizer.model_max_length, padding="max_length", truncation=True, return_tensors="pt").input_ids.to(device)
        with torch.no_grad():
            latents = vae.encode(pixels).latent_dist.sample() * vae.config.scaling_factor
            embeddings = text_encoder(token_ids)[0]
        noise = torch.randn_like(latents)
        timesteps = torch.randint(0, scheduler.config.num_train_timesteps, (1,), device=device).long()
        prediction = unet(scheduler.add_noise(latents, noise, timesteps), timesteps, embeddings).sample
        loss = F.mse_loss(prediction.float(), noise.float())
        if not torch.isfinite(loss):
            failure = "loss became non-finite before the optimizer update"
            failure_step = step + 1
            break
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        if not torch.isfinite(grad_norm):
            failure = "LoRA gradient norm became non-finite"
            failure_step = step + 1
            break
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        losses.append(float(loss.detach().cpu()))
    torch.cuda.synchronize()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps({
        "status": (
            "anchor_profile_failed_non_finite"
            if failure
            else "preflight_passed" if args.steps == 1 else "anchor_profile_completed"
        ),
        "base_model": str(args.model),
        "resolution": [args.width, args.height],
        "rank": args.rank,
        "dtype": args.dtype,
        "trainable_parameters": sum(parameter.numel() for parameter in trainable),
        "steps": args.steps,
        "completed_steps": len(losses),
        "loss_first": losses[0] if losses else None,
        "loss_last": losses[-1] if losses else None,
        "failure": failure,
        "failure_step": failure_step,
        "peak_vram_mib": round(torch.cuda.max_memory_allocated() / 1024**2, 1),
        "preprocessing": "aspect-ratio-preserving resize and white padding; no crop",
    }, indent=2) + "\n")
    if args.save_dir and not failure:
        args.save_dir.mkdir(parents=True, exist_ok=True)
        lora_state_dict = get_peft_model_state_dict(unet)
        StableDiffusionPipeline.save_lora_weights(args.save_dir, unet_lora_layers=lora_state_dict)
    print(args.report.read_text())
    return 1 if failure else 0


if __name__ == "__main__":
    raise SystemExit(main())

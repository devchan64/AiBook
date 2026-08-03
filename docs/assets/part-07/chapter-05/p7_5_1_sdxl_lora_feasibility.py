#!/usr/bin/env python3
"""Test one SDXL UNet-LoRA update with frozen CPU-offloaded encoders on 8 GB VRAM."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import torch.nn.functional as F
from diffusers import AutoencoderKL, DDPMScheduler, StableDiffusionXLPipeline, UNet2DConditionModel
from peft import LoraConfig, get_peft_model_state_dict
from PIL import Image
from transformers import CLIPTextModel, CLIPTextModelWithProjection, CLIPTokenizer


def pixels_from_image(path: Path, width: int, height: int) -> torch.Tensor:
    image = Image.open(path).convert("RGB")
    scale = min(width / image.width, height / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)))
    canvas = Image.new("RGB", (width, height), "white")
    canvas.paste(resized, ((width - resized.width) // 2, (height - resized.height) // 2))
    pixels = torch.from_numpy(__import__("numpy").asarray(canvas).copy())
    return pixels.permute(2, 0, 1).float().div(127.5).sub(1.0).unsqueeze(0)


def tokens(tokenizer: CLIPTokenizer, prompt: str) -> torch.Tensor:
    raw = tokenizer(prompt, truncation=False).input_ids
    if len(raw) > tokenizer.model_max_length:
        raise ValueError(f"caption has {len(raw)} tokens; maximum is {tokenizer.model_max_length}")
    return tokenizer(prompt, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt").input_ids


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("dataset", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("--width", type=int, default=384)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--rank", type=int, default=8)
    parser.add_argument("--steps", type=int, default=1)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--save-dir", type=Path)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    device = torch.device("cuda")
    dtype = torch.bfloat16
    rows = [json.loads(line) for line in (args.dataset / "train" / "metadata.jsonl").read_text().splitlines()]
    if args.steps < 1 or not rows:
        raise ValueError("--steps must be positive and the train metadata must not be empty")
    tokenizer_one = CLIPTokenizer.from_pretrained(args.model, subfolder="tokenizer")
    tokenizer_two = CLIPTokenizer.from_pretrained(args.model, subfolder="tokenizer_2")
    text_encoder_one = CLIPTextModel.from_pretrained(args.model, subfolder="text_encoder", torch_dtype=dtype).requires_grad_(False)
    text_encoder_two = CLIPTextModelWithProjection.from_pretrained(args.model, subfolder="text_encoder_2", torch_dtype=dtype).requires_grad_(False)
    vae = AutoencoderKL.from_pretrained(args.model, subfolder="vae", torch_dtype=dtype).requires_grad_(False)
    unet = UNet2DConditionModel.from_pretrained(args.model, subfolder="unet", torch_dtype=dtype)
    scheduler = DDPMScheduler.from_pretrained(args.model, subfolder="scheduler")
    unet.to(device)
    unet.add_adapter(LoraConfig(r=args.rank, lora_alpha=args.rank, target_modules=["to_q", "to_k", "to_v", "to_out.0"]))
    unet.enable_gradient_checkpointing()
    trainable = [parameter for parameter in unet.parameters() if parameter.requires_grad]
    optimizer = torch.optim.AdamW(trainable, lr=args.learning_rate)
    torch.cuda.reset_peak_memory_stats()
    losses: list[float] = []
    last_grad_norm: float | None = None
    token_counts: set[int] = set()
    for step in range(args.steps):
        row = rows[step % len(rows)]
        prompt = row["text"]
        token_one = tokens(tokenizer_one, prompt).to(device)
        token_two = tokens(tokenizer_two, prompt).to(device)
        token_counts.add(len(tokenizer_one(prompt, truncation=False).input_ids))
        with torch.no_grad():
            text_encoder_one.to(device)
            hidden_one = text_encoder_one(token_one, output_hidden_states=True).hidden_states[-2]
            text_encoder_one.to("cpu")
            torch.cuda.empty_cache()
            text_encoder_two.to(device)
            output_two = text_encoder_two(token_two, output_hidden_states=True)
            hidden_two = output_two.hidden_states[-2]
            pooled = output_two[0]
            text_encoder_two.to("cpu")
            torch.cuda.empty_cache()
            prompt_embeds = torch.cat((hidden_one, hidden_two), dim=-1)
            vae.to(device)
            latents = vae.encode(pixels_from_image(args.dataset / "train" / row["file_name"], args.width, args.height).to(device=device, dtype=dtype)).latent_dist.sample()
            latents = latents * vae.config.scaling_factor
            vae.to("cpu")
            torch.cuda.empty_cache()
        noise = torch.randn_like(latents)
        timestep = torch.randint(0, scheduler.config.num_train_timesteps, (1,), device=device).long()
        noisy = scheduler.add_noise(latents, noise, timestep)
        time_ids = torch.tensor([[args.height, args.width, 0, 0, args.height, args.width]], device=device, dtype=pooled.dtype)
        prediction = unet(noisy, timestep, prompt_embeds, added_cond_kwargs={"text_embeds": pooled, "time_ids": time_ids}).sample
        loss = F.mse_loss(prediction.float(), noise.float())
        if not torch.isfinite(loss):
            raise RuntimeError(f"loss became non-finite at step {step + 1}")
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        if not torch.isfinite(grad_norm):
            raise RuntimeError(f"LoRA gradient norm became non-finite at step {step + 1}")
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        losses.append(float(loss.detach().cpu()))
        last_grad_norm = float(grad_norm.detach().cpu())
        del token_one, token_two, hidden_one, hidden_two, output_two, pooled, prompt_embeds, latents, noise, noisy, prediction
    torch.cuda.synchronize()
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps({
        "status": "one_step_passed" if args.steps == 1 else "training_completed",
        "model": str(args.model),
        "resolution": [args.width, args.height],
        "rank": args.rank,
        "dtype": "bf16",
        "caption_tokens": sorted(token_counts),
        "steps": args.steps,
        "learning_rate": args.learning_rate,
        "loss_first": losses[0],
        "loss_last": losses[-1],
        "gradient_norm_last": last_grad_norm,
        "peak_vram_mib": round(torch.cuda.max_memory_allocated() / 1024**2, 1),
        "strategy": "frozen text encoders and VAE move to GPU only for their forward pass; UNet LoRA update runs on GPU",
    }, indent=2) + "\n")
    if args.save_dir:
        args.save_dir.mkdir(parents=True, exist_ok=True)
        StableDiffusionXLPipeline.save_lora_weights(args.save_dir, unet_lora_layers=get_peft_model_state_dict(unet))
    print(args.report.read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

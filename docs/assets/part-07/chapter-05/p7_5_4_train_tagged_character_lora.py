#!/usr/bin/env python3
"""Train a small tag-captioned character LoRA from current approved P7-5.2 masters.

This deliberately separates identity learning from pose control: every input is
an approved static face or turnaround image, and novel movement remains the
responsibility of the later text-pose OpenPose condition.
"""

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
MODEL = Path(
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
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--width", type=int, default=320)
    parser.add_argument("--height", type=int, default=448)
    return parser.parse_args()


def tokenize(tokenizer: AutoTokenizer, caption: str) -> torch.Tensor:
    return tokenizer(
        caption, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt"
    ).input_ids


def pixels(path: Path, width: int, height: int) -> torch.Tensor:
    image = Image.open(path).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
    array = np.asarray(image).copy()
    return torch.from_numpy(array).permute(2, 0, 1).float().div(127.5).sub(1.0).unsqueeze(0)


def main() -> int:
    args = parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    examples = [(ASSETS / name, f"{IDENTITY_TAGS}, {view}") for name, view in SOURCES]
    missing = [str(path) for path, _caption in examples if not path.is_file()]
    if missing:
        raise FileNotFoundError("approved training source missing: " + ", ".join(missing))
    args.output.mkdir(parents=True, exist_ok=True)
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.backends.cuda.matmul.allow_tf32 = True
    device, dtype = torch.device("cuda"), torch.bfloat16

    tokenizer_1 = AutoTokenizer.from_pretrained(MODEL, subfolder="tokenizer", use_fast=False)
    tokenizer_2 = AutoTokenizer.from_pretrained(MODEL, subfolder="tokenizer_2", use_fast=False)
    text_1 = CLIPTextModel.from_pretrained(MODEL, subfolder="text_encoder", torch_dtype=dtype).eval()
    text_2 = CLIPTextModelWithProjection.from_pretrained(MODEL, subfolder="text_encoder_2", torch_dtype=dtype).eval()
    vae = AutoencoderKL.from_pretrained(MODEL, subfolder="vae", torch_dtype=dtype).eval()
    for module in (text_1, text_2, vae):
        module.requires_grad_(False)

    # Keep the encoder stages separate from the UNet.  This is essential when
    # the local ComfyUI server already occupies part of an 8 GB GPU.
    cached: list[tuple[torch.Tensor, torch.Tensor, torch.Tensor]] = []
    for path, caption in examples:
        image = pixels(path, args.width, args.height).to(device=device, dtype=dtype)
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
        cached.append((latents, torch.cat([hidden_1, hidden_2], dim=-1), pooled))
    del vae, text_1, text_2
    gc.collect()
    torch.cuda.empty_cache()

    unet = UNet2DConditionModel.from_pretrained(MODEL, subfolder="unet", torch_dtype=dtype)
    scheduler = DDPMScheduler.from_pretrained(MODEL, subfolder="scheduler")
    unet.requires_grad_(False)
    unet.add_adapter(LoraConfig(r=8, lora_alpha=8, target_modules=["to_k", "to_q", "to_v", "to_out.0"]))
    unet.to(device)
    optimizer = torch.optim.AdamW((parameter for parameter in unet.parameters() if parameter.requires_grad), lr=args.learning_rate)
    losses: list[float] = []
    peak_mib = 0.0

    for step in range(1, args.steps + 1):
        latents, embeds, pooled = cached[(step - 1) % len(cached)]
        latents, embeds, pooled = latents.to(device), embeds.to(device), pooled.to(device)
        noise = torch.randn_like(latents)
        timesteps = torch.randint(0, scheduler.config.num_train_timesteps, (1,), device=device).long()
        noisy = scheduler.add_noise(latents, noise, timesteps)
        time_ids = torch.tensor([[args.height, args.width, 0, 0, args.height, args.width]], device=device, dtype=dtype)
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
        "status": "training_completed", "model": str(MODEL), "training_images": [name for name, _view in SOURCES],
        "caption_format": "Animagine-compatible tag sequence", "steps": args.steps, "resolution": [args.width, args.height],
        "rank": 8, "dtype": "bf16", "learning_rate": args.learning_rate, "loss_first": losses[0],
        "loss_last": losses[-1], "peak_vram_mib": peak_mib, "adapter": "pytorch_lora_weights.safetensors",
        "scope": "identity anchor only; no dynamic pose samples are claimed",
    }
    (args.output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

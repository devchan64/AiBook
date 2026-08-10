#!/usr/bin/env python3
"""Train a background-style LoRA from the approved P7-5.1 reference pack.

The P7-5.1 approval manifest, rather than a copied image directory, is the
single source of truth. This keeps a later approval replacement visible to the
trainer and makes every run record the exact file hashes it used.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import random
from dataclasses import dataclass
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
DEFAULT_MODEL = Path(
    "/home/cbsim/.cache/huggingface/hub/models--stabilityai--stable-diffusion-xl-base-1.0/"
    "snapshots/462165984030d82259a11f4367a4eed129e94a7b"
)
DEFAULT_DATASET = ASSETS / "p7-5-4-lora-style-dataset-manifest.json"

# These captions carry only the learned rendering token plus the scene contract.
# No character, garment, pose, or prop word may enter a style-only LoRA sample.
SCENE_CAPTIONS = {
    "indoor-dawn-high-angle": "indoor dawn atrium, high-angle wide background",
    "indoor-night-oblique": "night-lit reading room, oblique background",
    "outdoor-day-wide": "clear-day downtown, wide background",
    "outdoor-sunset-low-angle": "residential street at sunset, low-angle background",
    "outdoor-rainy-night-overhead": "rainy rooftop at night, overhead background",
    "courtyard-early-morning-high-angle": "courtyard in early morning, high-angle background",
    "venice-sunset-oblique": "canal district at sunset, oblique background",
    "park-clear-day-eye-level": "park on a clear day, eye-level background",
    "train-platform-rainy-night-oblique": "rainy train platform at night, oblique background",
    "ceramics-studio-afternoon": "ceramics studio in afternoon light, eye-level background",
    "gallery-midday-oblique": "empty gallery at midday, oblique background",
    "greenhouse-blue-hour": "greenhouse conservatory at blue hour, eye-level wide background",
    "hillside-alley-late-afternoon": "hillside alley in late afternoon, eye-level background",
    "ferry-deck-morning": "ferry deck in the morning, oblique wide background",
    "cinema-foyer-night": "cinema foyer at night, eye-level background",
    "market-arcade-overcast": "empty market arcade under overcast light, oblique background",
    "riverside-terrace-night": "riverside terrace at night, oblique background",
    "underpass-rainy-twilight": "rainy pedestrian underpass at twilight, centered background",
    "harbor-plaza-sunrise-high": "harbor plaza at sunrise, high-angle background",
    "library-tall-lobby-high-oblique": "daylit public-library tall lobby, high oblique background",
}
STYLE_TRAITS = "restrained webtoon background, sparse charcoal linework, transparent watercolor washes, low-saturation flat colors"


@dataclass(frozen=True)
class Example:
    scene_id: str
    path: Path
    sha256: str
    caption: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--output", type=Path, default=ROOT / ".tmp/p7-5-4-style-lora")
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--seed", type=int, default=5415)
    parser.add_argument("--width", type=int, default=384)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--rank", type=int, default=8)
    parser.add_argument("--validate-only", action="store_true", help="check the approved inputs without loading CUDA models")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_examples(dataset_path: Path) -> tuple[list[Example], list[Example]]:
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    pack_path = dataset_path.parent / dataset["source_manifest"]
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    if pack.get("status") != "approved_for_downstream_reference":
        raise ValueError(f"approved source pack is not ready: {pack.get('status')}")

    assets_by_scene = {record["scene_id"]: record["asset"] for record in pack["references"]}
    trigger = dataset["trigger"]

    def resolve(scene_ids: list[str], split: str) -> list[Example]:
        examples: list[Example] = []
        for scene_id in scene_ids:
            asset = assets_by_scene.get(scene_id)
            if asset is None:
                raise KeyError(f"{split} scene is missing from approved source pack: {scene_id}")
            if scene_id not in SCENE_CAPTIONS:
                raise KeyError(f"caption is missing for {scene_id}")
            path = pack_path.parent / asset
            if not path.is_file():
                raise FileNotFoundError(f"approved source is missing: {path}")
            examples.append(Example(scene_id, path, sha256(path), f"{trigger}, {SCENE_CAPTIONS[scene_id]}, {STYLE_TRAITS}"))
        return examples

    train = resolve(dataset["train_scene_ids"], "train")
    heldout = resolve(dataset["heldout_scene_ids"], "heldout")
    if len(train) != dataset["integrity"]["train_count"] or len(heldout) != dataset["integrity"]["heldout_count"]:
        raise ValueError("dataset count does not match its integrity contract")
    if {item.scene_id for item in train} & {item.scene_id for item in heldout}:
        raise ValueError("train and held-out scene IDs overlap")
    if {item.sha256 for item in train} & {item.sha256 for item in heldout}:
        raise ValueError("train and held-out source hashes overlap")
    return train, heldout


def tokenize(tokenizer: AutoTokenizer, caption: str) -> torch.Tensor:
    return tokenizer(
        caption, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt"
    ).input_ids


def pixels(path: Path, width: int, height: int) -> torch.Tensor:
    image = Image.open(path).convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
    return torch.from_numpy(np.asarray(image).copy()).permute(2, 0, 1).float().div(127.5).sub(1.0).unsqueeze(0)


def cache_examples(
    examples: list[Example], tokenizer_1: AutoTokenizer, tokenizer_2: AutoTokenizer,
    text_1: CLIPTextModel, text_2: CLIPTextModelWithProjection, vae: AutoencoderKL, args: argparse.Namespace,
    device: torch.device, dtype: torch.dtype,
) -> list[tuple[torch.Tensor, torch.Tensor, torch.Tensor]]:
    cached: list[tuple[torch.Tensor, torch.Tensor, torch.Tensor]] = []
    for example in examples:
        image = pixels(example.path, args.width, args.height).to(device=device, dtype=dtype)
        ids_1 = tokenize(tokenizer_1, example.caption).to(device)
        ids_2 = tokenize(tokenizer_2, example.caption).to(device)
        with torch.no_grad():
            vae.to(device)
            latents = vae.encode(image).latent_dist.sample().mul_(vae.config.scaling_factor).cpu()
            vae.to("cpu")
            text_1.to(device)
            hidden_1 = text_1(ids_1, output_hidden_states=True).hidden_states[-2].cpu()
            text_1.to("cpu")
            text_2.to(device)
            encoded_2 = text_2(ids_2, output_hidden_states=True)
            hidden_2, pooled = encoded_2.hidden_states[-2].cpu(), encoded_2[0].cpu()
            text_2.to("cpu")
        cached.append((latents, torch.cat([hidden_1, hidden_2], dim=-1), pooled))
    return cached


def main() -> int:
    args = parse_args()
    train, heldout = load_examples(args.dataset)
    input_report = {
        "dataset": str(args.dataset),
        "train": [{"scene_id": item.scene_id, "asset": item.path.name, "sha256": item.sha256} for item in train],
        "heldout": [{"scene_id": item.scene_id, "asset": item.path.name, "sha256": item.sha256} for item in heldout],
    }
    if args.validate_only:
        print(json.dumps({"status": "validated", **input_report}, ensure_ascii=False, indent=2))
        return 0
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required; use --validate-only for input validation without a GPU")
    if not args.model.is_dir():
        raise FileNotFoundError(f"base-model snapshot is missing: {args.model}")

    args.output.mkdir(parents=True, exist_ok=True)
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.backends.cuda.matmul.allow_tf32 = True
    device, dtype = torch.device("cuda"), torch.bfloat16
    tokenizer_1 = AutoTokenizer.from_pretrained(args.model, subfolder="tokenizer", use_fast=False)
    tokenizer_2 = AutoTokenizer.from_pretrained(args.model, subfolder="tokenizer_2", use_fast=False)
    text_1 = CLIPTextModel.from_pretrained(args.model, subfolder="text_encoder", torch_dtype=dtype).eval()
    text_2 = CLIPTextModelWithProjection.from_pretrained(args.model, subfolder="text_encoder_2", torch_dtype=dtype).eval()
    vae = AutoencoderKL.from_pretrained(args.model, subfolder="vae", torch_dtype=dtype).eval()
    for module in (text_1, text_2, vae):
        module.requires_grad_(False)
    cached = cache_examples(train, tokenizer_1, tokenizer_2, text_1, text_2, vae, args, device, dtype)
    del vae, text_1, text_2
    gc.collect()
    torch.cuda.empty_cache()

    unet = UNet2DConditionModel.from_pretrained(args.model, subfolder="unet", torch_dtype=dtype)
    scheduler = DDPMScheduler.from_pretrained(args.model, subfolder="scheduler")
    unet.requires_grad_(False)
    unet.add_adapter(LoraConfig(r=args.rank, lora_alpha=args.rank, target_modules=["to_k", "to_q", "to_v", "to_out.0"]))
    unet.to(device)
    parameters = [parameter for parameter in unet.parameters() if parameter.requires_grad]
    optimizer = torch.optim.AdamW(parameters, lr=args.learning_rate)
    losses: list[float] = []
    peak_mib = 0.0
    for step in range(1, args.steps + 1):
        latents, embeds, pooled = (tensor.to(device) for tensor in cached[(step - 1) % len(cached)])
        noise = torch.randn_like(latents)
        timesteps = torch.randint(0, scheduler.config.num_train_timesteps, (1,), device=device).long()
        noisy = scheduler.add_noise(latents, noise, timesteps)
        time_ids = torch.tensor([[args.height, args.width, 0, 0, args.height, args.width]], device=device, dtype=dtype)
        prediction = unet(noisy, timesteps, encoder_hidden_states=embeds, added_cond_kwargs={"text_embeds": pooled, "time_ids": time_ids}).sample
        loss = functional.mse_loss(prediction.float(), noise.float())
        loss.backward()
        torch.nn.utils.clip_grad_norm_(parameters, 1.0)
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        losses.append(float(loss.detach()))
        peak_mib = max(peak_mib, torch.cuda.max_memory_allocated(device) / 1024**2)
        if step == 1 or step % 50 == 0 or step == args.steps:
            print(json.dumps({"step": step, "loss": round(losses[-1], 6), "peak_mib": round(peak_mib, 1)}), flush=True)

    state = convert_state_dict_to_diffusers(get_peft_model_state_dict(unet))
    StableDiffusionXLPipeline.save_lora_weights(args.output, unet_lora_layers=state)
    report = {
        "status": "training_completed",
        "scope": "background rendering style only; excludes identity, garments, props, and pose control",
        "model": str(args.model),
        "steps": args.steps,
        "resolution": [args.width, args.height],
        "rank": args.rank,
        "dtype": "bf16",
        "learning_rate": args.learning_rate,
        "loss_first": losses[0],
        "loss_last": losses[-1],
        "peak_vram_mib": peak_mib,
        "adapter": "pytorch_lora_weights.safetensors",
        **input_report,
    }
    (args.output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

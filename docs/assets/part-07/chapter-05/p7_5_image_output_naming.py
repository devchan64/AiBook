"""Stable output names for Part 7 Chapter 5 image-generation candidates."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

import torch


def candidate_stem(prefix: str, *, seed: int, steps: int, contract: object) -> str:
    """Return a deterministic candidate stem with contract hash, seed, and diffusion steps."""
    encoded = json.dumps(contract, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    digest = sha256(encoded.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-hash-{digest}-seed-{seed}-steps-{steps}"


def preview_callback(pipe, *, height: int, width: int, every: int, directory: Path, prefix: str):
    """Return a Flux2 callback that writes decoded previews every ``every`` denoising steps."""
    if every < 1:
        return None
    directory.mkdir(parents=True, exist_ok=True)
    latent_ids = None

    def save_preview(_pipe, step: int, _timestep: int, callback_kwargs: dict):
        nonlocal latent_ids
        if (step + 1) % every:
            return callback_kwargs
        latents = callback_kwargs["latents"]
        if latent_ids is None:
            latent_height = 2 * (height // (pipe.vae_scale_factor * 2))
            latent_width = 2 * (width // (pipe.vae_scale_factor * 2))
            template = torch.empty((latents.shape[0], 1, latent_height, latent_width), device=latents.device)
            latent_ids = pipe._prepare_latent_ids(template).to(latents.device)
        with torch.no_grad():
            decoded = pipe._unpack_latents_with_ids(latents.detach(), latent_ids)
            mean = pipe.vae.bn.running_mean.view(1, -1, 1, 1).to(decoded.device, decoded.dtype)
            std = torch.sqrt(pipe.vae.bn.running_var.view(1, -1, 1, 1) + pipe.vae.config.batch_norm_eps).to(decoded.device, decoded.dtype)
            decoded = pipe._unpatchify_latents(decoded * std + mean)
            image = pipe.vae.decode(decoded, return_dict=False)[0]
            preview = pipe.image_processor.postprocess(image, output_type="pil")[0]
        preview.save(directory / f"{prefix}-step-{step + 1:02d}.png")
        return callback_kwargs

    return save_preview

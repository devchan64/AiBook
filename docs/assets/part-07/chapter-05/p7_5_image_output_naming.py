"""Experiment-scoped output names for Part 7 Chapter 5 image candidates."""

from __future__ import annotations

from pathlib import Path
from secrets import token_hex

import torch


_EXPERIMENT_CODE = token_hex(3)


def experiment_code() -> str:
    """Return the six-character random code shared by this process."""
    return _EXPERIMENT_CODE


def candidate_stem(prefix: str, *, seed: int, steps: int, contract: object) -> str:
    """Return a stem with the run code, seed, and diffusion steps.

    ``contract`` stays required so call sites keep their generation inputs
    explicit even though filenames no longer encode a contract digest.
    """
    _ = contract
    return f"{prefix}-code-{experiment_code()}-seed-{seed}-steps-{steps}"


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
            # Flux2KleinPipeline.prepare_latents() patchifies the VAE grid once
            # before packing it. The callback receives that packed grid, so its
            # position IDs must use the post-patch dimensions rather than the
            # intermediate pre-patch dimensions.
            latent_height = height // (pipe.vae_scale_factor * 2)
            latent_width = width // (pipe.vae_scale_factor * 2)
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

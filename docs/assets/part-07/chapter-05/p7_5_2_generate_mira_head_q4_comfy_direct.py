#!/usr/bin/env python3
"""Generate Mira's head with a Qwen-Image GGUF through direct Comfy nodes.

This runner opens no HTTP port and does not start a ComfyUI server. It reuses
the low-VRAM Qwen setup proven by P7-5.9: a GGUF diffusion model, FP8-scaled
Qwen2.5-VL text encoder, and CPU VAE.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import sys
import time
import traceback
from pathlib import Path

import torch


ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parents[3]
COMFY = ROOT / ".tmp" / "ComfyUI"
TEXT_ENCODER = "qwen_2.5_vl_7b_fp8_scaled.safetensors"
VAE = "qwen_image_vae.safetensors"
WEIGHT = ROOT / ".tmp/download/weight-unsloth-qwen-image-q4-ks-gguf/qwen-image-Q4_K_S.gguf"
IDENTITY = ASSETS / "p7-5-2-mira-identity-contract.json"
ILLUSTRATION = ASSETS / "p7-5-2-face-illustration-prompt-contract.json"


def require(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def digest(path: Path) -> str:
    hashed = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            hashed.update(chunk)
    return hashed.hexdigest()


def expose(weight: Path) -> None:
    target = COMFY / "models" / "diffusion_models" / weight.name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if target.resolve() == weight.resolve():
            return
        raise FileExistsError(target)
    target.symlink_to(weight)


def prompt() -> str:
    identity = json.loads(IDENTITY.read_text(encoding="utf-8"))
    illustration = json.loads(ILLUSTRATION.read_text(encoding="utf-8"))
    return " ".join((
        illustration["front_face_illustration_prompt"],
        identity["identity_description"],
        "Strict frontal head-and-shoulders studio portrait of Mira at a comfortable distance. Complete hair crown, centered face, both eyes and ears visible. Plain warm off-white background. No text or accessories.",
    ))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weight", type=Path, default=WEIGHT, help="Managed Qwen-Image GGUF transformer.")
    parser.add_argument("--quant", default="Q4_K_S", help="Quantization label written to the result record.")
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--cfg", type=float, default=4.0)
    parser.add_argument("--prompt", help="Override the default Mira head prompt for a controlled quantization comparison.")
    parser.add_argument("--label", default="front-v1")
    args = parser.parse_args()
    if args.size % 16 or args.steps < 1:
        parser.error("--size must be divisible by 16 and --steps must be positive")
    weight = require(args.weight.resolve())
    require(IDENTITY)
    require(ILLUSTRATION)
    expose(weight)
    generation_prompt = args.prompt or prompt()
    quant_slug = args.quant.lower().replace("_", "")
    output = ASSETS / f"p7-5-2-mira-head-qwen-image-{quant_slug}-comfy-direct-{args.label}-seed-{args.seed}-steps-{args.steps}-size-{args.size}.png"
    result = output.with_name(f"{output.stem}-result.json")
    stage = "initialization"
    started = time.monotonic()

    try:
        # Comfy nodes are imported as a library; no PromptServer or socket is created.
        # These are the same memory-policy inputs used by the working P7-5.9 probe.
        sys.argv = [sys.argv[0], "--lowvram", "--cpu-vae", "--disable-dynamic-vram", "--disable-auto-launch"]
        sys.path.insert(0, str(COMFY))
        os.chdir(COMFY)
        import nodes  # noqa: PLC0415
        asyncio.run(nodes.init_extra_nodes())
        classes = nodes.NODE_CLASS_MAPPINGS
        stage = "load_models"
        print(f"stage={stage}", flush=True)
        with torch.inference_mode():
            unet = classes["UnetLoaderGGUF"]().load_unet(weight.name)[0]
            model = classes["ModelSamplingAuraFlow"]().patch_aura(unet, 3.0)[0]
            # Let --lowvram choose the same placement used by the proven P7-5.9 graph.
            clip = classes["CLIPLoader"]().load_clip(TEXT_ENCODER, "qwen_image", "default")[0]
            vae = classes["VAELoader"]().load_vae(VAE)[0]
            positive = classes["CLIPTextEncode"]().encode(clip, generation_prompt)[0]
            negative = classes["CLIPTextEncode"]().encode(clip, "")[0]
            latent = classes["EmptySD3LatentImage"]().generate(args.size, args.size, 1)[0]
            stage = "sample"
            print(f"stage={stage}", flush=True)
            samples = classes["KSampler"]().sample(model, args.seed, args.steps, args.cfg, "euler", "simple", positive, negative, latent, 1.0)[0]
            stage = "decode"
            print(f"stage={stage}", flush=True)
            image = vae.decode(samples["samples"])[0][0].cpu().numpy()
        from PIL import Image  # noqa: PLC0415

        stage = "save"
        Image.fromarray((image * 255).clip(0, 255).astype("uint8")).save(output)
        payload = {
            "status": "generated", "execution_mode": "direct Comfy nodes; no server, port, or HTTP API",
            "quant": args.quant, "model": {"path": str(weight), "sha256": digest(weight)},
            "text_encoder": TEXT_ENCODER, "vae": VAE, "size": [args.size, args.size], "steps": args.steps,
            "cfg": args.cfg, "seed": args.seed, "prompt": generation_prompt, "output": str(output),
            "elapsed_seconds": round(time.monotonic() - started, 2),
        }
    except Exception as error:
        payload = {
            "status": "failed", "execution_mode": "direct Comfy nodes; no server, port, or HTTP API",
            "quant": args.quant, "stage": stage, "error": str(error),
            "traceback": traceback.format_exc(), "elapsed_seconds": round(time.monotonic() - started, 2),
        }
    result.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if payload["status"] == "failed":
        raise RuntimeError(f"generation failed during {stage}; see {result}")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

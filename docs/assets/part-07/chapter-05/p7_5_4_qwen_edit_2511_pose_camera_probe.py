#!/usr/bin/env python3
"""Test pose, character latent, and one Qwen Image Edit 2511 camera direction.

Picture 1 is a P7-5.3 white-background pose cutout. Picture 2 is a P7-5.3
full-body character reference and supplies the initial latent. The Multiple
Angles LoRA is the only camera control; no scene background is supplied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parents[3]
COMFY = ROOT / ".tmp" / "p7-5-3-scail-runtime" / "ComfyUI"
MODEL = "qwen-image-edit-2511-Q4_0.gguf"
TEXT_ENCODER = "qwen_2.5_vl_7b_fp8_scaled.safetensors"
VAE = "qwen_image_vae.safetensors"
ANGLE_LORA = "qwen-image-edit-2511-multiple-angles-lora.safetensors"
LIGHTNING_LORA = "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors"
DEFAULT_POSE = ASSETS / "p7-5-4-character-pose-cutout-white-scene-b-front-left-high-angle-v1.png"
DEFAULT_CHARACTER = ASSETS / "p7-5-3-qwen-edit-prompt-style-outfit_stage2_jacket_face-long-trousers-folded-collar-v3-seed-62294-steps-30.png"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def request_json(url: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def conditioning(image1: str, image2: str, prompt: str) -> dict:
    return {"class_type": "TextEncodeQwenImageEditPlus", "inputs": {"clip": ["clip", 0], "vae": ["vae", 0], "image1": [image1, 0], "image2": [image2, 0], "prompt": prompt}}


def workflow(pose_name: str, character_name: str, prompt: str, seed: int, steps: int, prefix: str) -> dict:
    return {
        "pose": {"class_type": "LoadImage", "inputs": {"image": pose_name}},
        "character": {"class_type": "LoadImage", "inputs": {"image": character_name}},
        "unet": {"class_type": "UnetLoaderGGUFAdvanced", "inputs": {"unet_name": MODEL, "dequant_dtype": "float16", "patch_dtype": "float16", "patch_on_device": False}},
        "camera_lora": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["unet", 0], "lora_name": ANGLE_LORA, "strength_model": 0.9}},
        "lightning_lora": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["camera_lora", 0], "lora_name": LIGHTNING_LORA, "strength_model": 1.0}},
        "sampling": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["lightning_lora", 0], "shift": 3.1}},
        "cfg_norm": {"class_type": "CFGNorm", "inputs": {"model": ["sampling", 0], "strength": 1.0}},
        "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": TEXT_ENCODER, "type": "qwen_image", "device": "default"}},
        "vae": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "positive": conditioning("pose", "character", prompt),
        "negative": conditioning("pose", "character", ""),
        "reference_method_positive": {"class_type": "FluxKontextMultiReferenceLatentMethod", "inputs": {"conditioning": ["positive", 0], "reference_latents_method": "index_timestep_zero"}},
        "reference_method_negative": {"class_type": "FluxKontextMultiReferenceLatentMethod", "inputs": {"conditioning": ["negative", 0], "reference_latents_method": "index_timestep_zero"}},
        "latent": {"class_type": "VAEEncode", "inputs": {"pixels": ["character", 0], "vae": ["vae", 0]}},
        "sample": {"class_type": "KSampler", "inputs": {"model": ["cfg_norm", 0], "positive": ["reference_method_positive", 0], "negative": ["reference_method_negative", 0], "latent_image": ["latent", 0], "seed": seed, "steps": steps, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "save": {"class_type": "SaveImage", "inputs": {"images": ["decode", 0], "filename_prefix": prefix}},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pose", type=Path, default=DEFAULT_POSE)
    parser.add_argument("--character", type=Path, default=DEFAULT_CHARACTER)
    parser.add_argument("--azimuth", default="front-left quarter view")
    parser.add_argument("--elevation", default="elevated shot")
    parser.add_argument("--distance", default="medium shot")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--run-label", default="q4-character-latent-v1")
    parser.add_argument("--port", type=int, default=8195)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    pose, character = args.pose.resolve(), args.character.resolve()
    for path in (pose, character):
        if not path.is_file():
            raise FileNotFoundError(path)
    if args.steps < 1:
        parser.error("--steps must be positive")
    camera = f"{args.azimuth} {args.elevation} {args.distance}"
    prompt = f"<sks> {camera}. Picture 1 pose. Picture 2 character and outfit."
    stem = f"p7-5-3-qwen-2511-pose-camera-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output, result = ASSETS / f"{stem}.png", ASSETS / f"{stem}-result.json"
    if args.dry_run:
        print(json.dumps({"prompt": prompt, "pose": str(pose), "character": str(character), "initial_latent": "Picture 2 character and outfit", "output": str(output)}, ensure_ascii=False))
        return
    pose_name = f"p7-5-3-pose-{sha256(pose)[:12]}.png"
    character_name = f"p7-5-3-character-{sha256(character)[:12]}.png"
    shutil.copy2(pose, COMFY / "input" / pose_name)
    shutil.copy2(character, COMFY / "input" / character_name)
    base_url, process = f"http://127.0.0.1:{args.port}", None
    try:
        try:
            request_json(f"{base_url}/system_stats")
        except (urllib.error.URLError, TimeoutError):
            env = {**os.environ, "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
            process = subprocess.Popen([sys.executable, "main.py", "--listen", "127.0.0.1", "--port", str(args.port), "--disable-auto-launch", "--lowvram", "--cpu-vae"], cwd=COMFY, env=env)
            for _ in range(90):
                try:
                    request_json(f"{base_url}/system_stats")
                    break
                except (urllib.error.URLError, TimeoutError):
                    time.sleep(1)
            else:
                raise TimeoutError("ComfyUI did not start")
        started = time.monotonic()
        prompt_id = request_json(f"{base_url}/prompt", {"prompt": workflow(pose_name, character_name, prompt, args.seed, args.steps, stem)})["prompt_id"]
        for _ in range(420):
            history = request_json(f"{base_url}/history/{prompt_id}")
            if prompt_id in history:
                generated = history[prompt_id]["outputs"]["save"]["images"][0]
                source = COMFY / generated.get("type", "output") / generated.get("subfolder", "") / generated["filename"]
                break
            time.sleep(1)
        else:
            raise TimeoutError("Qwen Image Edit 2511 did not finish")
        shutil.copy2(source, output)
        record = {"status": "generated", "experiment_id": "p7-5-3-qwen-edit-2511-pose-camera", "model": MODEL, "inputs": [{"role": "pose and framing", "path": str(pose), "sha256": sha256(pose)}, {"role": "character identity and outfit", "path": str(character), "sha256": sha256(character)}], "reference_order": "pose-character", "initial_latent": "Picture 2 character and outfit", "camera": {"azimuth": args.azimuth, "elevation": args.elevation, "distance": args.distance, "lora": ANGLE_LORA, "strength": 0.9}, "prompt": prompt, "seed": args.seed, "steps": args.steps, "output": {"path": str(output), "sha256": sha256(output)}, "elapsed_seconds": round(time.monotonic() - started, 2)}
        result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))
    finally:
        if process is not None:
            process.terminate()
            process.wait(timeout=20)


if __name__ == "__main__":
    main()

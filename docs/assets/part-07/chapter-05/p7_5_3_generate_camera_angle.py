#!/usr/bin/env python3
"""Create one P7-5.3 camera-angle image with Qwen Image Edit 2511.

The generator fixes the runtime to the 2511 Multiple Angles LoRA. Its prompt
has a deliberate three-field order: ``<sks> [azimuth] [elevation] [distance]``.
Use every field for reproducible production runs; ``--omit-azimuth`` exists
only to reproduce the explicit comparison experiment.
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
PROJECT_ROOT = ASSETS.parents[3]
DEFAULT_REFERENCE = ASSETS / "p7-5-3-qwen-storyboard-scene-a-349252-seed-5420-steps-20.png"
DEFAULT_COMFY_ROOT = PROJECT_ROOT / ".tmp/p7-5-3-scail-runtime/ComfyUI"
DEFAULT_MODEL = "qwen-image-edit-2511-Q4_0.gguf"
TEXT_ENCODER = "qwen_2.5_vl_7b_fp8_scaled.safetensors"
VAE = "qwen_image_vae.safetensors"
ANGLE_LORA = "qwen-image-edit-2511-multiple-angles-lora.safetensors"
LIGHTNING_LORA = "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors"
ANGLE_LORA_SOURCE = "https://huggingface.co/fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA"
AZIMUTHS = (
    "front view", "front-right quarter view", "right side view", "rear-right quarter view",
    "rear view", "rear-left quarter view", "left side view", "front-left quarter view",
)
ELEVATIONS = ("low-angle shot", "eye-level shot", "elevated shot", "high-angle shot")
DISTANCES = ("close-up", "medium shot", "wide shot")


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


def workflow(model_name: str, image_name: str, prompt: str, seed: int, steps: int, prefix: str) -> dict:
    """Return the tested low-VRAM ComfyUI graph for Qwen Edit 2511."""
    return {
        "1": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "2": {"class_type": "UnetLoaderGGUFAdvanced", "inputs": {"unet_name": model_name, "dequant_dtype": "float16", "patch_dtype": "float16", "patch_on_device": False}},
        "3": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["2", 0], "lora_name": ANGLE_LORA, "strength_model": 0.9}},
        "4": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["3", 0], "lora_name": LIGHTNING_LORA, "strength_model": 1.0}},
        "5": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["4", 0], "shift": 3.1}},
        "6": {"class_type": "CFGNorm", "inputs": {"model": ["5", 0], "strength": 1.0}},
        "7": {"class_type": "CLIPLoader", "inputs": {"clip_name": TEXT_ENCODER, "type": "qwen_image", "device": "default"}},
        "8": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "9": {"class_type": "TextEncodeQwenImageEditPlus", "inputs": {"clip": ["7", 0], "vae": ["8", 0], "image1": ["1", 0], "prompt": prompt}},
        "10": {"class_type": "TextEncodeQwenImageEditPlus", "inputs": {"clip": ["7", 0], "vae": ["8", 0], "image1": ["1", 0], "prompt": ""}},
        "11": {"class_type": "FluxKontextMultiReferenceLatentMethod", "inputs": {"conditioning": ["9", 0], "reference_latents_method": "index_timestep_zero"}},
        "12": {"class_type": "FluxKontextMultiReferenceLatentMethod", "inputs": {"conditioning": ["10", 0], "reference_latents_method": "index_timestep_zero"}},
        "13": {"class_type": "VAEEncode", "inputs": {"pixels": ["1", 0], "vae": ["8", 0]}},
        "14": {"class_type": "KSampler", "inputs": {"model": ["6", 0], "positive": ["11", 0], "negative": ["12", 0], "latent_image": ["13", 0], "seed": seed, "steps": steps, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "15": {"class_type": "VAEDecode", "inputs": {"samples": ["14", 0], "vae": ["8", 0]}},
        "16": {"class_type": "SaveImage", "inputs": {"images": ["15", 0], "filename_prefix": prefix}},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--model", default=DEFAULT_MODEL, help="GGUF transformer file registered in ComfyUI/models/unet/.")
    parser.add_argument("--azimuth", choices=AZIMUTHS, default="front view")
    parser.add_argument("--elevation", choices=ELEVATIONS, default="eye-level shot")
    parser.add_argument("--distance", choices=DISTANCES, default="medium shot")
    parser.add_argument("--omit-azimuth", action="store_true", help="Comparison-only: omit the required azimuth field.")
    parser.add_argument("--seed", type=int, default=5420)
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--comfy-root", type=Path, default=DEFAULT_COMFY_ROOT)
    parser.add_argument("--port", type=int, default=8191)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    reference = args.reference.resolve()
    if not reference.is_file():
        raise FileNotFoundError(reference)
    if args.steps < 1:
        parser.error("--steps must be positive")
    fields = ([] if args.omit_azimuth else [args.azimuth]) + [args.elevation, args.distance]
    prompt = "<sks> " + " ".join(fields)
    azimuth_label = "azimuth-omitted" if args.omit_azimuth else args.azimuth.replace(" ", "-")
    stem = f"p7-5-3-qwen-2511-camera-{azimuth_label}-{args.elevation.replace(' ', '-')}-{args.distance.replace(' ', '-')}-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output_dir = args.output_dir.resolve()
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    if args.dry_run:
        print(json.dumps({"input": str(reference), "prompt": prompt, "output": str(output), "result": str(result)}, ensure_ascii=False))
        return
    comfy_root = args.comfy_root.resolve()
    if not (comfy_root / "main.py").is_file():
        raise FileNotFoundError(f"ComfyUI runtime not found: {comfy_root}")
    input_name = f"p7-5-3-camera-input-{sha256(reference)[:12]}.png"
    shutil.copy2(reference, comfy_root / "input" / input_name)
    base_url = f"http://127.0.0.1:{args.port}"
    process = None
    try:
        try:
            request_json(f"{base_url}/system_stats")
        except (urllib.error.URLError, TimeoutError):
            env = {**os.environ, "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
            process = subprocess.Popen([sys.executable, "main.py", "--listen", "127.0.0.1", "--port", str(args.port), "--disable-auto-launch", "--lowvram", "--cpu-vae"], cwd=comfy_root, env=env)
            for _ in range(60):
                try:
                    request_json(f"{base_url}/system_stats")
                    break
                except (urllib.error.URLError, TimeoutError):
                    time.sleep(1)
            else:
                raise RuntimeError("ComfyUI did not start within 60 seconds")
        started = time.monotonic()
        reply = request_json(f"{base_url}/prompt", {"prompt": workflow(args.model, input_name, prompt, args.seed, args.steps, stem)})
        prompt_id = reply["prompt_id"]
        for _ in range(300):
            history = request_json(f"{base_url}/history/{prompt_id}")
            if prompt_id in history:
                image = history[prompt_id]["outputs"]["16"]["images"][0]
                generated = comfy_root / image.get("type", "output") / image.get("subfolder", "") / image["filename"]
                break
            time.sleep(1)
        else:
            raise TimeoutError("Qwen Image Edit 2511 did not finish within 300 seconds")
        output_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(generated, output)
        result.write_text(json.dumps({
            "status": "generated", "experiment_id": "p7-5-3-qwen-2511-camera-angle", "stage": "camera_angle",
            "model": args.model, "angle_lora": {"repository": "fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA", "source": ANGLE_LORA_SOURCE, "weight": ANGLE_LORA, "strength": 0.9},
            "lightning_lora": {"weight": LIGHTNING_LORA, "strength": 1.0}, "input": {"path": str(reference), "sha256": sha256(reference)},
            "azimuth": None if args.omit_azimuth else args.azimuth, "elevation": args.elevation, "distance": args.distance,
            "prompt": prompt, "prompt_format": "<sks> [azimuth] [elevation] [distance]", "seed": args.seed, "steps": args.steps,
            "output": {"path": str(output), "sha256": sha256(output)}, "elapsed_seconds": round(time.monotonic() - started, 2),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))
    finally:
        if process is not None:
            process.terminate()
            process.wait(timeout=20)


if __name__ == "__main__":
    main()

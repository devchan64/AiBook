#!/usr/bin/env python3
"""Run a reproducible 8GB-VRAM Qwen-Image Q4 GGUF text-to-image probe.

This is a feasibility probe, not a character-consistency workflow: a Qwen-Image
GGUF has no external reference-image input.  It tests whether ComfyUI can
complete a fixed 512px, 10-step T2I image through CPU offloading and records
the actual device memory and generated asset in a result JSON file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen


ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parents[3]
COMFY = ROOT / ".tmp" / "ComfyUI"
WEIGHT = ROOT / ".tmp" / "download" / "weight-unsloth-qwen-image-q4-ks-gguf" / "qwen-image-Q4_K_S.gguf"
COMFY_CACHE = ROOT / ".tmp" / "download" / "huggingface" / "hub" / "models--Comfy-Org--Qwen-Image_ComfyUI" / "snapshots"
TEXT_ENCODER_NAME = "qwen_2.5_vl_7b_fp8_scaled.safetensors"
VAE_NAME = "qwen_image_vae.safetensors"
MODEL_NAME = WEIGHT.name
OUTPUT_PREFIX = "p7-5-9-qwen-image-q4ks-low-vram-front-v1"
PROMPT = (
    "Front upper-torso illustration of a young woman with a short wavy dark teal bob, "
    "warm fair skin, amber eyes, and a grey cropped top. Plain light grey background."
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(path: Path) -> Path:
    if not path.is_file():
        raise FileNotFoundError(f"Missing required artifact: {path}")
    return path


def link(source: Path, target: Path) -> None:
    """Expose a managed cache artifact to ComfyUI without duplicating it."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if target.resolve() == source.resolve():
            return
        raise FileExistsError(f"Refusing to replace existing ComfyUI artifact: {target}")
    target.symlink_to(source)


def locate_comfy_component(filename: str) -> Path:
    matches = sorted(COMFY_CACHE.glob(f"*/split_files/**/{filename}"))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected exactly one cached {filename}, found {len(matches)}")
    return require(matches[0])


def gpu_memory() -> str:
    query = ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,memory.free", "--format=csv,noheader"]
    completed = subprocess.run(query, check=False, capture_output=True, text=True)
    return completed.stdout.strip() if completed.returncode == 0 else "unavailable"


def workflow(seed: int, steps: int, size: int, cfg: float) -> dict[str, object]:
    """Build the smallest native Qwen T2I graph with the GGUF UNet loader."""
    return {
        "unet": {"class_type": "UnetLoaderGGUF", "inputs": {"unet_name": MODEL_NAME}},
        "sampling": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["unet", 0], "shift": 3.0}},
        "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": TEXT_ENCODER_NAME, "type": "qwen_image", "device": "default"}},
        "vae": {"class_type": "VAELoader", "inputs": {"vae_name": VAE_NAME}},
        "positive": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["clip", 0], "text": PROMPT}},
        "negative": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["clip", 0], "text": ""}},
        "latent": {"class_type": "EmptySD3LatentImage", "inputs": {"width": size, "height": size, "batch_size": 1}},
        "sample": {"class_type": "KSampler", "inputs": {"model": ["sampling", 0], "positive": ["positive", 0], "negative": ["negative", 0], "latent_image": ["latent", 0], "seed": seed, "steps": steps, "cfg": cfg, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "save": {"class_type": "SaveImage", "inputs": {"images": ["decode", 0], "filename_prefix": OUTPUT_PREFIX}},
    }


def wait_for_server(port: int, process: subprocess.Popen[str]) -> None:
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("ComfyUI stopped before accepting the probe")
        try:
            with urlopen(f"http://127.0.0.1:{port}/system_stats", timeout=2):
                return
        except (URLError, TimeoutError):
            time.sleep(1)
    raise TimeoutError("ComfyUI did not start within 120 seconds")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--size", type=int, default=512)
    parser.add_argument("--cfg", type=float, default=4.0)
    parser.add_argument("--port", type=int, default=8192)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.size % 16 or args.steps < 1:
        parser.error("--size must be divisible by 16 and --steps must be positive")

    graph = workflow(args.seed, args.steps, args.size, args.cfg)
    if args.dry_run:
        print(json.dumps(graph, ensure_ascii=False, indent=2))
        return

    require(WEIGHT)
    link(WEIGHT, COMFY / "models" / "diffusion_models" / MODEL_NAME)
    link(locate_comfy_component(TEXT_ENCODER_NAME), COMFY / "models" / "text_encoders" / TEXT_ENCODER_NAME)
    link(locate_comfy_component(VAE_NAME), COMFY / "models" / "vae" / VAE_NAME)
    gpu_before = gpu_memory()
    started = time.monotonic()
    command = [sys.executable, "main.py", "--listen", "127.0.0.1", "--port", str(args.port), "--lowvram", "--cpu-vae", "--output-directory", str(ASSETS)]
    process = subprocess.Popen(command, cwd=COMFY, text=True)
    history: dict[str, object] = {}
    try:
        wait_for_server(args.port, process)
        request = Request(f"http://127.0.0.1:{args.port}/prompt", data=json.dumps({"prompt": graph}).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=30) as response:
            prompt_id = json.loads(response.read().decode("utf-8"))["prompt_id"]
        while True:
            with urlopen(f"http://127.0.0.1:{args.port}/history/{prompt_id}", timeout=30) as response:
                history = json.loads(response.read().decode("utf-8"))
            if prompt_id in history:
                break
            if process.poll() is not None:
                raise RuntimeError("ComfyUI stopped during sampling")
            time.sleep(2)
    finally:
        process.terminate()
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            process.kill()

    run = history[prompt_id]
    status = run["status"]["status_str"]
    result = ASSETS / f"{OUTPUT_PREFIX}-seed-{args.seed}-steps-{args.steps}-result.json"
    result.write_text(json.dumps({
        "status": "generated" if status == "success" else "failed",
        "experiment_id": "p7-5-9-qwen-image-q4ks-low-vram",
        "purpose": "Q4 GGUF 8GB-VRAM text-to-image feasibility; not reference-image character consistency",
        "model": {"repository": "unsloth/Qwen-Image-GGUF", "selector": MODEL_NAME, "sha256": sha256(WEIGHT), "bytes": WEIGHT.stat().st_size},
        "runtime_mode": {"comfy_arguments": ["--lowvram", "--cpu-vae"], "gpu_before": gpu_before},
        "seed": args.seed, "steps": args.steps, "cfg": args.cfg, "size": [args.size, args.size], "prompt": PROMPT,
        "workflow": graph, "history": run, "elapsed_seconds": round(time.monotonic() - started, 2), "gpu_after": gpu_memory(),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if status != "success":
        raise RuntimeError(f"ComfyUI sampling failed; see {result}")
    print(json.dumps({"image_prefix": OUTPUT_PREFIX, "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

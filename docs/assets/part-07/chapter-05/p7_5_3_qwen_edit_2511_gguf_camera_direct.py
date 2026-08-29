#!/usr/bin/env python3
"""Run one Qwen Edit 2511 GGUF camera edit in-process, without a ComfyUI server.

This runner retains the proven low-VRAM ComfyUI graph and its GGUF transformer,
but invokes ComfyUI's ``PromptExecutor`` directly.  It never opens a port,
starts a queue worker, or sends an HTTP request.  One invocation produces one
explicit camera conversion from one input image.

The Multiple-Angles LoRA model card requires the prompt contract
``<sks> [azimuth] [elevation] [distance]`` in that exact order.  Supply all
three camera fields even when only one field is intended to change.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import sys
import time
import uuid
from pathlib import Path


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
DEFAULT_COMFY_ROOT = PROJECT_ROOT / ".tmp" / "p7-5-3-scail-runtime" / "ComfyUI"
DEFAULT_REFERENCE = ASSETS / "p7-5-3-qwen-storyboard-scene-a-349252-seed-5420-steps-20.png"
DEFAULT_MODEL = "qwen-image-edit-2511-Q4_0.gguf"
TEXT_ENCODER = "qwen_2.5_vl_7b_fp8_scaled.safetensors"
VAE = "qwen_image_vae.safetensors"
ANGLE_LORA = "qwen-image-edit-2511-multiple-angles-lora.safetensors"
LIGHTNING_LORA = "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors"
ANGLE_LORA_REPOSITORY = "fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA"

AZIMUTHS = (
    "front view", "front-right quarter view", "right side view", "rear-right quarter view",
    "rear view", "rear-left quarter view", "left side view", "front-left quarter view",
)
ELEVATIONS = ("low-angle shot", "eye-level shot", "elevated shot", "high-angle shot")
DISTANCES = ("close-up", "medium shot", "wide shot")
CAMERA_PRESETS = {
    "a": ("front view", "elevated shot", "medium shot"),
    "c": ("front-right quarter view", "low-angle shot", "medium shot"),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def workflow(model_name: str, image_name: str, prompt: str, seed: int, steps: int, prefix: str) -> dict:
    """Return the existing Q4_0 GGUF, low-VRAM Qwen Edit 2511 graph."""
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


def prompt_for(azimuth: str, elevation: str, distance: str) -> str:
    return f"<sks> {azimuth} {elevation} {distance}"


def output_file(history: dict, comfy_root: Path) -> Path:
    try:
        image = history["outputs"]["16"]["images"][0]
        output = comfy_root / image.get("type", "output") / image.get("subfolder", "") / image["filename"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError(f"ComfyUI did not return SaveImage output: {history}") from error
    if not output.is_file():
        raise FileNotFoundError(f"ComfyUI reported missing output: {output}")
    return output


def initialize_comfy(comfy_root: Path):
    """Load ComfyUI nodes in this process without starting its web server."""
    if not (comfy_root / "main.py").is_file():
        raise FileNotFoundError(f"ComfyUI runtime not found: {comfy_root}")
    os.chdir(comfy_root)
    sys.path.insert(0, str(comfy_root))

    # Importing modules directly leaves Comfy's CLI parser disabled, so this
    # runner's arguments cannot be mistaken for server arguments.
    import execution
    import nodes
    import server

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    prompt_server = server.PromptServer(loop)
    loop.run_until_complete(nodes.init_extra_nodes(init_custom_nodes=True, init_api_nodes=False))
    required_nodes = {
        "UnetLoaderGGUFAdvanced", "LoraLoaderModelOnly", "TextEncodeQwenImageEditPlus",
        "FluxKontextMultiReferenceLatentMethod", "CFGNorm",
    }
    missing_nodes = sorted(required_nodes - set(nodes.NODE_CLASS_MAPPINGS))
    if missing_nodes:
        raise RuntimeError("required ComfyUI custom nodes were not loaded: " + ", ".join(missing_nodes))
    return execution, prompt_server, loop


def execute_graph(execution, prompt_server, comfy_root: Path, graph: dict) -> Path:
    """Execute one graph using already initialized in-process ComfyUI state."""
    executor = execution.PromptExecutor(
        prompt_server,
        cache_type=execution.CacheType.NONE,
        cache_args={"lru": 0, "ram": 0, "ram_inactive": 0},
    )
    prompt_id = str(uuid.uuid4())
    executor.execute(graph, prompt_id, execute_outputs=["16"])
    if not executor.success:
        messages = json.dumps(executor.status_messages, ensure_ascii=False, default=str, indent=2)
        raise RuntimeError(f"in-process ComfyUI execution failed:\n{messages}")
    return output_file(executor.history_result, comfy_root)


def stage_stem(camera: tuple[str, str, str], run_label: str, seed: int, steps: int) -> str:
    camera_slug = "-".join(camera).replace(" ", "-")
    return f"p7-5-3-qwen-2511-camera-{camera_slug}-{run_label}-seed-{seed}-steps-{steps}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--camera", choices=tuple(CAMERA_PRESETS), help="Named single-camera preset; overrides --azimuth, --elevation, and --distance.")
    parser.add_argument("--azimuth", choices=AZIMUTHS, default="front view")
    parser.add_argument("--elevation", choices=ELEVATIONS, default="eye-level shot")
    parser.add_argument("--distance", choices=DISTANCES, default="medium shot")
    parser.add_argument("--seed", type=int, default=5420)
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--run-label", default="q4-direct")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--comfy-root", type=Path, default=DEFAULT_COMFY_ROOT)
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--dry-run", action="store_true", help="Print the exact graph plan without importing ComfyUI or touching the GPU.")
    parser.add_argument("--check-runtime", action="store_true", help="Import and validate the required ComfyUI nodes without loading model weights or generating an image.")
    args = parser.parse_args()

    reference = args.reference.resolve()
    if not reference.is_file():
        raise FileNotFoundError(reference)
    if args.steps < 1:
        parser.error("--steps must be positive")
    output_dir = args.output_dir.resolve()
    camera = CAMERA_PRESETS[args.camera] if args.camera else (args.azimuth, args.elevation, args.distance)
    prompt = prompt_for(*camera)
    stem = stage_stem(camera, args.run_label, args.seed, args.steps)
    output = output_dir / f"{stem}.png"
    result = output_dir / f"{stem}-result.json"
    input_name = f"p7-5-3-direct-camera-input-{sha256(reference)[:12]}.png"
    graph = workflow(args.model, input_name, prompt, args.seed, args.steps, stem)
    plan = {
        "runtime": "ComfyUI PromptExecutor in-process; no HTTP server or port",
        "reference": str(reference), "camera_preset": args.camera,
        "camera": {"azimuth": camera[0], "elevation": camera[1], "distance": camera[2]},
        "prompt": prompt, "input_name": input_name, "output": str(output), "result": str(result), "graph": graph,
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    comfy_root = args.comfy_root.resolve()
    if args.check_runtime:
        _, _, loop = initialize_comfy(comfy_root)
        loop.close()
        print(json.dumps({"status": "ready", "execution_mode": plan["runtime"], "comfy_root": str(comfy_root)}, ensure_ascii=False))
        return
    execution, prompt_server, loop = initialize_comfy(comfy_root)
    try:
        input_path = comfy_root / "input" / input_name
        input_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(reference, input_path)
        output_dir.mkdir(parents=True, exist_ok=True)
        started = time.monotonic()
        generated = execute_graph(execution, prompt_server, comfy_root, graph)
        shutil.copy2(generated, output)
        record = {
            "status": "generated", "experiment_id": "p7-5-3-qwen-2511-gguf-direct-camera", "stage": "camera_angle",
            "execution_mode": "in-process ComfyUI PromptExecutor; no HTTP server",
            "model": {"file": args.model, "format": "GGUF"},
            "angle_lora": {"repository": ANGLE_LORA_REPOSITORY, "weight": ANGLE_LORA, "strength": 0.9},
            "lightning_lora": {"weight": LIGHTNING_LORA, "strength": 1.0},
            "input": {"path": str(reference), "sha256": sha256(reference)}, "camera_preset": args.camera,
            "camera": {"azimuth": camera[0], "elevation": camera[1], "distance": camera[2]},
            "prompt": prompt, "prompt_format": "<sks> [azimuth] [elevation] [distance]",
            "seed": args.seed, "steps": args.steps,
            "output": {"path": str(output), "sha256": sha256(output)},
            "elapsed_seconds": round(time.monotonic() - started, 2),
        }
        result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    finally:
        loop.close()
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

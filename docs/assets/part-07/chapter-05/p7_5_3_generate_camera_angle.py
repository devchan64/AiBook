#!/usr/bin/env python3
"""Create one or more sequential P7-5.3 camera-angle images with Qwen Edit 2511.

The generator fixes the runtime to the 2511 Multiple Angles LoRA. One stage
sends exactly one camera term after ``<sks>``. Repeat ``--stage`` when a camera
change needs more than one edit: each stage consumes the previous stage's PNG,
and every result JSON records that input chain. This prevents an azimuth edit
from being diluted by elevation or distance instructions.
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
CAMERA_TERMS = AZIMUTHS + ELEVATIONS + DISTANCES
# Named scene plans make each view transition explicit and reproducible.
# B and C deliberately use two edits. Every tuple contains only the one term
# that should change in that stage; the previous PNG carries all other state.
SCENE_PLANS = {
    "a": {
        "reference": "p7-5-3-qwen-image-q4ks-style-contract-scene-a-v1_00001_.png",
        "seed": 5420,
        "run_label": "q4ks-scene-a-v3",
        "stages": (("elevated shot",), ("wide shot",)),
    },
    "b": {
        "reference": "p7-5-3-qwen-image-q4ks-style-contract-scene-b-v1_00001_.png",
        "seed": 5421,
        "run_label": "q4ks-scene-b-v3",
        "stages": (
            ("front-left quarter view",),
            ("high-angle shot",),
        ),
    },
    "c": {
        "reference": "p7-5-3-qwen-image-q4ks-style-contract-scene-c-v1_00001_.png",
        "seed": 5422,
        "run_label": "q4ks-scene-c-v3",
        "stages": (
            ("front-right quarter view",),
            ("wide shot",),
        ),
    },
}


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


def stage_prompt(term: str) -> str:
    return f"<sks> {term}"


def stage_stem(
    term: str,
    run_label: str,
    seed: int,
    steps: int,
    index: int,
    total: int,
) -> str:
    target = term.replace(" ", "-")
    suffix = "" if total == 1 else f"-stage-{index:02d}-of-{total:02d}"
    return f"p7-5-3-qwen-2511-camera-{target}-{run_label}{suffix}-seed-{seed}-steps-{steps}"


def ensure_server(comfy_root: Path, port: int) -> subprocess.Popen | None:
    """Return a newly started server process, or None when it already exists."""
    base_url = f"http://127.0.0.1:{port}"
    try:
        request_json(f"{base_url}/system_stats")
        return None
    except (urllib.error.URLError, TimeoutError):
        env = {**os.environ, "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
        process = subprocess.Popen(
            [sys.executable, "main.py", "--listen", "127.0.0.1", "--port", str(port), "--disable-auto-launch", "--lowvram", "--cpu-vae"],
            cwd=comfy_root,
            env=env,
        )
        for _ in range(60):
            try:
                request_json(f"{base_url}/system_stats")
                return process
            except (urllib.error.URLError, TimeoutError):
                time.sleep(1)
        process.terminate()
        process.wait(timeout=20)
        raise RuntimeError("ComfyUI did not start within 60 seconds")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", choices=tuple(SCENE_PLANS), help="Use the named, fixed camera-stage plan for scene A, B, or C.")
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE, help="Input for an ad-hoc plan; --scene replaces it with the scene's fixed input.")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="GGUF transformer file registered in ComfyUI/models/unet/.")
    parser.add_argument(
        "--stage",
        action="append",
        choices=CAMERA_TERMS,
        metavar="CAMERA_TERM",
        help="Repeat for sequential edits. One stage accepts exactly one azimuth, elevation, or distance term.",
    )
    parser.add_argument("--seed", type=int, help="Seed for an ad-hoc plan; named scenes use their recorded seed by default.")
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--resume-from", type=Path, help="Existing PNG to use as the input for --start-stage; keeps the preceding stage output intact.")
    parser.add_argument("--start-stage", type=int, default=1, help="1-based stage to start from; requires --resume-from when greater than 1.")
    parser.add_argument("--through-stage", type=int, help="Run only through this 1-based stage of a named or ad-hoc plan.")
    parser.add_argument("--run-label", help="Label for an ad-hoc plan; named scenes use their recorded label by default.")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--comfy-root", type=Path, default=DEFAULT_COMFY_ROOT)
    parser.add_argument("--port", type=int, default=8191)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.scene and args.stage:
        parser.error("--scene already defines its stages; do not combine it with --stage")
    plan = SCENE_PLANS.get(args.scene) if args.scene else None
    if args.start_stage < 1:
        parser.error("--start-stage must be positive")
    if args.start_stage > 1 and args.resume_from is None:
        parser.error("--start-stage greater than 1 requires --resume-from")
    if args.resume_from is not None and args.start_stage == 1:
        parser.error("--resume-from is only valid with --start-stage greater than 1")
    reference = (args.resume_from if args.resume_from else (ASSETS / plan["reference"] if plan else args.reference)).resolve()
    if not reference.is_file():
        raise FileNotFoundError(reference)
    if args.steps < 1:
        parser.error("--steps must be positive")
    all_stages = list(plan["stages"]) if plan else [(term,) for term in (args.stage or ["front view"])]
    if args.start_stage > len(all_stages):
        parser.error(f"--start-stage must be between 1 and {len(all_stages)}")
    final_stage = args.through_stage if args.through_stage is not None else len(all_stages)
    if not args.start_stage <= final_stage <= len(all_stages):
        parser.error(f"--through-stage must be between {args.start_stage} and {len(all_stages)}")
    stage_numbers = list(range(args.start_stage, final_stage + 1))
    stages = all_stages[args.start_stage - 1:final_stage]
    seed = args.seed if args.seed is not None else (plan["seed"] if plan else 5420)
    run_label = args.run_label or (plan["run_label"] if plan else "v1")
    output_dir = args.output_dir.resolve()
    if args.dry_run:
        planned = []
        for index, (term,) in zip(stage_numbers, stages, strict=True):
            prompt = stage_prompt(term)
            stem = stage_stem(term, run_label, seed, args.steps, index, len(all_stages))
            planned.append({"stage": index, "input": str(reference) if index == args.start_stage else "previous-stage output", "prompt": prompt, "output": str(output_dir / f"{stem}.png"), "result": str(output_dir / f"{stem}-result.json")})
        print(json.dumps({"stages": planned}, ensure_ascii=False))
        return
    comfy_root = args.comfy_root.resolve()
    if not (comfy_root / "main.py").is_file():
        raise FileNotFoundError(f"ComfyUI runtime not found: {comfy_root}")
    base_url = f"http://127.0.0.1:{args.port}"
    process: subprocess.Popen | None = None
    try:
        process = ensure_server(comfy_root, args.port)
        previous = reference
        completed = []
        output_dir.mkdir(parents=True, exist_ok=True)
        for index, (term,) in zip(stage_numbers, stages, strict=True):
            prompt = stage_prompt(term)
            stem = stage_stem(term, run_label, seed, args.steps, index, len(all_stages))
            output = output_dir / f"{stem}.png"
            result = output_dir / f"{stem}-result.json"
            input_name = f"p7-5-3-camera-input-{sha256(previous)[:12]}.png"
            shutil.copy2(previous, comfy_root / "input" / input_name)
            started = time.monotonic()
            reply = request_json(f"{base_url}/prompt", {"prompt": workflow(args.model, input_name, prompt, seed, args.steps, stem)})
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
            shutil.copy2(generated, output)
            record = {
                "status": "generated", "experiment_id": "p7-5-3-qwen-2511-camera-angle", "stage": "camera_angle",
                "stage_index": index, "stage_count": len(all_stages), "model": args.model,
                "angle_lora": {"repository": "fal/Qwen-Image-Edit-2511-Multiple-Angles-LoRA", "source": ANGLE_LORA_SOURCE, "weight": ANGLE_LORA, "strength": 0.9},
                "lightning_lora": {"weight": LIGHTNING_LORA, "strength": 1.0}, "input": {"path": str(previous), "sha256": sha256(previous)},
                "camera_term": term, "prompt": prompt, "prompt_format": "<sks> [single camera term]", "seed": seed, "steps": args.steps,
                "output": {"path": str(output), "sha256": sha256(output)}, "elapsed_seconds": round(time.monotonic() - started, 2),
            }
            result.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            completed.append({"stage": index, "output": str(output), "result": str(result)})
            previous = output
        sequence_result = None
        if len(completed) > 1:
            sequence_result = output_dir / f"p7-5-3-qwen-2511-camera-sequence-{run_label}-seed-{seed}-steps-{args.steps}-result.json"
            sequence_result.write_text(json.dumps({"status": "generated", "experiment_id": "p7-5-3-qwen-2511-camera-angle-sequence", "scene": args.scene, "input": str(reference), "stage_count": len(completed), "stages": completed, "final_output": str(previous)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"final_output": str(previous), "sequence_result": str(sequence_result) if sequence_result else completed[0]["result"], "stages": completed}, ensure_ascii=False))
    finally:
        if process is not None:
            process.terminate()
            process.wait(timeout=20)


if __name__ == "__main__":
    main()

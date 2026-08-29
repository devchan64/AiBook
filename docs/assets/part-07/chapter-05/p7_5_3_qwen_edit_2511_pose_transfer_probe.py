#!/usr/bin/env python3
"""Transfer a camera-angle person cutout to a character reference.

Picture 1 is normalized to a white 1:1 canvas before it is encoded as the
initial latent. It supplies only pose and framing. Picture 2 supplies character
identity and outfit. A global camera-angle replacement remains a comparison
only because it did not preserve the character identity reliably.
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

from PIL import Image, ImageOps


ASSETS = Path(__file__).resolve().parent
ROOT = ASSETS.parents[3]
COMFY = ROOT / ".tmp" / "p7-5-3-scail-runtime" / "ComfyUI"
DEFAULT_MODEL = "qwen-image-edit-2511-Q4_0.gguf"
TEXT_ENCODER = "qwen_2.5_vl_7b_fp8_scaled.safetensors"
VAE = "qwen_image_vae.safetensors"
LIGHTNING_LORA = "Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors"
DEFAULT_POSE = ASSETS / "p7-5-3-character-pose-cutout-white-q4ks-camera-scene-b-v2.png"
DEFAULT_CHARACTER = ASSETS / "p7-5-3-qwen-2511-pose-transfer-cutout-quarter-plus45-q4-0-v2-seed-62294-steps-8.png"
DEFAULT_CANVAS_SIZE = 1280


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def request_json(url: str, payload: dict | None = None) -> dict:
    body = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def white_square_canvas(source: Path, size: int) -> Image.Image:
    """Contain the complete cutout on a white square without cropping its pose."""
    with Image.open(source) as loaded:
        image = loaded.convert("RGBA")
    white = Image.new("RGBA", image.size, "white")
    white.alpha_composite(image)
    contained = ImageOps.contain(white.convert("RGB"), (size, size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), "white")
    offset = ((size - contained.width) // 2, (size - contained.height) // 2)
    canvas.paste(contained, offset)
    return canvas


def conditioning(image1_node: str, image2_node: str, prompt: str) -> dict:
    return {
        "class_type": "TextEncodeQwenImageEditPlus",
        "inputs": {"clip": ["clip", 0], "vae": ["vae", 0], "image1": [image1_node, 0], "image2": [image2_node, 0], "prompt": prompt},
    }


def workflow(model_name: str, pose_name: str, character_name: str, mask_name: str | None, mask_grow: int, prompt: str, latent_source: str, seed: int, steps: int, prefix: str) -> dict:
    latent_image = "pose" if latent_source == "pose" else "character"
    graph = {
        "pose": {"class_type": "LoadImage", "inputs": {"image": pose_name}},
        "character": {"class_type": "LoadImage", "inputs": {"image": character_name}},
        "unet": {"class_type": "UnetLoaderGGUFAdvanced", "inputs": {"unet_name": model_name, "dequant_dtype": "float16", "patch_dtype": "float16", "patch_on_device": False}},
        "lightning_lora": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["unet", 0], "lora_name": LIGHTNING_LORA, "strength_model": 1.0}},
        "sampling": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["lightning_lora", 0], "shift": 3.1}},
        "cfg_norm": {"class_type": "CFGNorm", "inputs": {"model": ["sampling", 0], "strength": 1.0}},
        "clip": {"class_type": "CLIPLoader", "inputs": {"clip_name": TEXT_ENCODER, "type": "qwen_image", "device": "default"}},
        "vae": {"class_type": "VAELoader", "inputs": {"vae_name": VAE}},
        "positive": conditioning("pose", "character", prompt),
        "negative": conditioning("pose", "character", ""),
        "reference_method_positive": {"class_type": "FluxKontextMultiReferenceLatentMethod", "inputs": {"conditioning": ["positive", 0], "reference_latents_method": "index_timestep_zero"}},
        "reference_method_negative": {"class_type": "FluxKontextMultiReferenceLatentMethod", "inputs": {"conditioning": ["negative", 0], "reference_latents_method": "index_timestep_zero"}},
        # Picture 1 is the cutout canvas. Both pictures remain in the
        # conditioning, but only Picture 1 supplies the initial latent.
        "latent": {"class_type": "VAEEncode", "inputs": {"pixels": [latent_image, 0], "vae": ["vae", 0]}},
        "sample": {"class_type": "KSampler", "inputs": {"model": ["cfg_norm", 0], "positive": ["reference_method_positive", 0], "negative": ["reference_method_negative", 0], "latent_image": ["latent", 0], "seed": seed, "steps": steps, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "decode": {"class_type": "VAEDecode", "inputs": {"samples": ["sample", 0], "vae": ["vae", 0]}},
        "save": {"class_type": "SaveImage", "inputs": {"images": ["decode", 0], "filename_prefix": prefix}},
    }
    if mask_name is not None:
        graph["mask"] = {"class_type": "LoadImageMask", "inputs": {"image": mask_name, "channel": "red"}}
        graph["latent"] = {"class_type": "VAEEncodeForInpaint", "inputs": {"pixels": [latent_image, 0], "vae": ["vae", 0], "mask": ["mask", 0], "grow_mask_by": mask_grow}}
    return graph


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pose", type=Path, default=DEFAULT_POSE, help="White-background camera cutout (Picture 1): pose and framing.")
    parser.add_argument("--character", type=Path, default=DEFAULT_CHARACTER)
    parser.add_argument("--canvas-size", type=int, default=DEFAULT_CANVAS_SIZE, help="White square canvas size for Picture 1; must be a multiple of 32.")
    parser.add_argument("--inpaint-mask", type=Path, help="White replacement area on the selected initial-latent image.")
    parser.add_argument("--mask-grow", type=int, default=0)
    parser.add_argument("--pose-role", default="pose cutout and framing")
    parser.add_argument("--character-role", default="character identity and outfit")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="GGUF transformer file registered in ComfyUI/models/unet/.")
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--latent-source", choices=("pose", "character"), default="pose")
    parser.add_argument(
        "--pose-description",
        default="",
        help="Short positive pose cue appended after the two image-reference instructions.",
    )
    parser.add_argument("--prompt", default="", help="Use a complete, concise two-image instruction when the second reference is not an outfit image.")
    parser.add_argument("--run-label", default="pose-only-v1")
    parser.add_argument("--port", type=int, default=8194)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    pose, character = args.pose.resolve(), args.character.resolve()
    mask = args.inpaint_mask.resolve() if args.inpaint_mask else None
    for path in (pose, character, mask):
        if path is None:
            continue
        if not path.is_file():
            raise FileNotFoundError(path)
    if args.steps < 1 or args.mask_grow < 0:
        parser.error("--steps must be positive and --mask-grow cannot be negative")
    if args.canvas_size < 32 or args.canvas_size % 32:
        parser.error("--canvas-size must be a positive multiple of 32")

    prompt = args.prompt.strip() or "Replace the woman in Picture 1 with the woman in Picture 2. Preserve Picture 1 pose and framing. Plain white 1:1 square background."
    if args.pose_description.strip():
        prompt = f"{prompt} {args.pose_description.strip()}"
    stem = f"p7-5-3-qwen-2511-pose-transfer-{args.run_label}-seed-{args.seed}-steps-{args.steps}"
    output, result = ASSETS / f"{stem}.png", ASSETS / f"{stem}-result.json"
    if args.dry_run:
        print(json.dumps({"prompt": prompt, "reference_order": "pose-character", "initial_latent": args.latent_source, "pose": str(pose), "character": str(character), "canvas": {"width": args.canvas_size, "height": args.canvas_size, "background": "white"}, "inpaint_mask": str(mask) if mask else None, "output": str(output)}, ensure_ascii=False))
        return
    if not (COMFY / "main.py").is_file():
        raise FileNotFoundError(COMFY)

    pose_name = f"p7-5-3-pose-square-white-{sha256(pose)[:12]}-{args.canvas_size}.png"
    character_name = f"p7-5-3-character-{sha256(character)[:12]}.png"
    normalized_pose = COMFY / "input" / pose_name
    white_square_canvas(pose, args.canvas_size).save(normalized_pose)
    shutil.copy2(character, COMFY / "input" / character_name)
    mask_name = None
    if mask is not None:
        mask_name = f"p7-5-3-mask-{sha256(mask)[:12]}.png"
        shutil.copy2(mask, COMFY / "input" / mask_name)
    process = None
    base_url = f"http://127.0.0.1:{args.port}"
    try:
        try:
            request_json(f"{base_url}/system_stats")
        except (urllib.error.URLError, TimeoutError):
            environment = {**os.environ, "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"}
            process = subprocess.Popen([sys.executable, "main.py", "--listen", "127.0.0.1", "--port", str(args.port), "--disable-auto-launch", "--lowvram", "--cpu-vae"], cwd=COMFY, env=environment)
            for _ in range(90):
                try:
                    request_json(f"{base_url}/system_stats")
                    break
                except (urllib.error.URLError, TimeoutError):
                    time.sleep(1)
            else:
                raise TimeoutError("ComfyUI did not start")
        started = time.monotonic()
        prompt_id = request_json(f"{base_url}/prompt", {"prompt": workflow(args.model, pose_name, character_name, mask_name, args.mask_grow, prompt, args.latent_source, args.seed, args.steps, stem)})["prompt_id"]
        for _ in range(420):
            history = request_json(f"{base_url}/history/{prompt_id}")
            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                if "save" not in outputs:
                    raise RuntimeError(f"ComfyUI did not create an image: {history[prompt_id].get('status', {})}")
                generated = outputs["save"]["images"][0]
                source = COMFY / generated.get("type", "output") / generated.get("subfolder", "") / generated["filename"]
                break
            time.sleep(1)
        else:
            raise TimeoutError("Qwen Image Edit 2511 did not finish")
        shutil.copy2(source, output)
        initial_latent = "Picture 1" if args.latent_source == "pose" else "Picture 2"
        inputs = [
            {"role": args.pose_role, "path": str(pose), "sha256": sha256(pose)},
            {"role": "normalized white 1:1 pose canvas", "path": str(normalized_pose), "sha256": sha256(normalized_pose)},
            {"role": args.character_role, "path": str(character), "sha256": sha256(character)},
        ]
        if mask is not None:
            inputs.append({"role": "inpaint replacement area", "path": str(mask), "sha256": sha256(mask)})
        result.write_text(json.dumps({"status": "generated", "experiment_id": "p7-5-3-qwen-edit-2511-pose-transfer", "model": args.model, "inputs": inputs, "reference_order": "pose-character", "initial_latent": initial_latent, "canvas": {"width": args.canvas_size, "height": args.canvas_size, "aspect_ratio": "1:1", "background": "white", "fit": "contain without crop"}, "inpaint": {"enabled": mask is not None, "mask_grow": args.mask_grow}, "camera": "not used", "prompt": prompt, "seed": args.seed, "steps": args.steps, "output": {"path": str(output), "sha256": sha256(output)}, "elapsed_seconds": round(time.monotonic() - started, 2)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))
    finally:
        if process is not None:
            process.terminate()
            process.wait(timeout=20)


if __name__ == "__main__":
    main()

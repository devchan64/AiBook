#!/usr/bin/env python3
"""Apply FoxBaze Try-On LoRA to one subject and one white-background outfit.

Picture 1 is the sole output subject and Picture 2 is only the garment
reference.  The implementation deliberately uses the original full Qwen 2509
transformer path rather than the Nunchaku compatibility path.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
import time
from pathlib import Path


ASSETS = Path(__file__).resolve().parent
PROJECT_ROOT = ASSETS.parents[3]
HUB_CACHE = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"
TRANSFORMER_DIR = PROJECT_ROOT / ".tmp" / "download" / "model-qwen-image-edit-2509" / "transformer"
MODEL_ID = "Qwen/Qwen-Image-Edit-2509"
LORA_ID = "FoxBaze/Try_On_Qwen_Edit_Lora_Alpha"
LORA_DIR = PROJECT_ROOT / ".tmp" / "download" / "weight-foxbaze-try-on-qwen-edit-alpha"
LORA_FILENAME = "Try_On_Qwen_Edit_Lora.safetensors"
BASE_PROMPT = "A single full-body image of the woman in Picture 1, wearing every article of clothing from Picture 2"
DEFAULT_PERSON = ASSETS / "p7-5-4-qwen-2511-pose-identity-official-camera-scene-a-cutout-shadow-v1-size-1280x1280-seed-62294-steps-20.png"
DEFAULT_GARMENT = ASSETS / "p7-5-4-qwen-2511-xabsurd-clothing-extractor-shoe-gear-v2-size-1280x1280-seed-62294-steps-10.png"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def runtime_record() -> dict[str, object]:
    packages = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {"python": sys.version.split()[0], "platform": platform.platform(), "packages": packages}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--person", type=Path, default=DEFAULT_PERSON, help="The only output subject; first input.")
    parser.add_argument("--garment", type=Path, default=DEFAULT_GARMENT, help="White-background outfit reference; second input.")
    parser.add_argument("--steps", type=int, default=30)
    parser.add_argument("--size", type=int, default=1280)
    parser.add_argument("--lora-scale", type=float, default=1.0)
    parser.add_argument("--true-cfg-scale", type=float, default=2.5)
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32:
        parser.error("--steps must be positive and --size must be a multiple of 32")
    if args.lora_scale < 0 or args.true_cfg_scale <= 0:
        parser.error("LoRA scale must be non-negative and true CFG scale must be positive")

    person, garment = args.person.resolve(), args.garment.resolve()
    required = (
        person, garment, LORA_DIR / LORA_FILENAME, TRANSFORMER_DIR / "config.json",
        TRANSFORMER_DIR / "diffusion_pytorch_model.safetensors.index.json",
    )
    for path in required:
        if not path.is_file():
            raise FileNotFoundError(path)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"p7-5-4-qwen-2509-tryon-foxbaze-{args.run_label}-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}"
    output_path = output_dir / f"{stem}.png"
    result_path = output_dir / f"{stem}-result.json"

    import torch
    from diffusers import QwenImageEditPlusPipeline, QwenImageTransformer2DModel
    from diffusers.utils import load_image
    from huggingface_hub import snapshot_download

    started = time.monotonic()
    model_path = Path(snapshot_download(MODEL_ID, cache_dir=HUB_CACHE, local_files_only=True))
    transformer = QwenImageTransformer2DModel.from_pretrained(
        TRANSFORMER_DIR, torch_dtype=torch.bfloat16, local_files_only=True,
    )
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        model_path, transformer=transformer, torch_dtype=torch.bfloat16, local_files_only=True,
    )
    pipeline.enable_sequential_cpu_offload()
    pipeline.load_lora_weights(LORA_DIR, weight_name=LORA_FILENAME, adapter_name="foxbaze_tryon", local_files_only=True)
    pipeline.set_adapters(["foxbaze_tryon"], adapter_weights=[args.lora_scale])
    try:
        image = pipeline(
            image=[load_image(str(person)), load_image(str(garment))], prompt=BASE_PROMPT,
            generator=torch.Generator("cpu").manual_seed(args.seed),
            true_cfg_scale=args.true_cfg_scale, negative_prompt=" ", guidance_scale=1.0,
            num_inference_steps=args.steps, width=args.size, height=args.size,
        ).images[0]
    finally:
        pipeline.delete_adapters("foxbaze_tryon")
    image.save(output_path)
    result_path.write_text(json.dumps({
        "status": "generated", "stage": "subject_only_tryon",
        "execution_mode": "direct Diffusers; Qwen Image Edit 2509; no ComfyUI",
        "runtime": runtime_record(), "model": MODEL_ID,
        "lora": {"repository": LORA_ID, "weight": LORA_FILENAME, "adapter": "foxbaze_tryon"},
        "inputs": [
            {"role": "subject and sole output (Picture 1)", "path": str(person), "sha256": sha256(person)},
            {"role": "garment reference only (Picture 2)", "path": str(garment), "sha256": sha256(garment)},
        ],
        "prompt": BASE_PROMPT, "seed": args.seed, "steps": args.steps,
        "lora_scale": args.lora_scale, "true_cfg_scale": args.true_cfg_scale,
        "guidance_scale": 1.0, "generation_canvas": [args.size, args.size],
        "output": {"path": str(output_path), "sha256": sha256(output_path)},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output_path), "result": str(result_path)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

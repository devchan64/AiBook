#!/usr/bin/env python3
"""Restore a P7-5.3 background plate with mask-native LaMa ONNX inference."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path

import numpy as np
import onnxruntime as ort
import cv2
from huggingface_hub import hf_hub_download
from PIL import Image


ASSETS = Path(__file__).resolve().parent
HF_HUB_CACHE = ASSETS.parents[3] / ".tmp" / "download" / "huggingface" / "hub"
MODEL_REPOSITORY = "g-ronimo/lama"
MODEL_FILE = "lama.onnx"
MODEL_LICENSE = "Apache-2.0"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pad_to_thirty_two(image: np.ndarray) -> tuple[np.ndarray, tuple[int, int]]:
    height, width = image.shape[-2:]
    padded_height = (height + 31) // 32 * 32
    padded_width = (width + 31) // 32 * 32
    padded = np.pad(image, ((0, 0), (0, 0), (0, padded_height - height), (0, padded_width - width)), mode="reflect")
    return padded, (height, width)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", type=Path, required=True, help="Stage-2 camera-angle scene PNG.")
    parser.add_argument("--mask", type=Path, required=True, help="White=person to remove; black=preserved background.")
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--grow", type=int, default=25, help="Expand the white completion region by this many pixels.")
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    parser.add_argument("--model", type=Path, help="Local LaMa ONNX path; otherwise use the local Hugging Face cache.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    scene, mask = args.scene.resolve(), args.mask.resolve()
    for path in (scene, mask):
        if not path.is_file():
            raise FileNotFoundError(path)
    stem = f"p7-5-3-lama-background-{args.run_label}"
    output_dir = args.output_dir.resolve()
    output, result = output_dir / f"{stem}.png", output_dir / f"{stem}-result.json"
    if args.dry_run:
        print(json.dumps({"scene": str(scene), "mask": str(mask), "output": str(output), "result": str(result)}, ensure_ascii=False))
        return
    if args.grow < 0:
        parser.error("--grow must be non-negative")
    model = args.model.resolve() if args.model else Path(hf_hub_download(MODEL_REPOSITORY, MODEL_FILE, cache_dir=HF_HUB_CACHE, local_files_only=True))
    if not model.is_file():
        raise FileNotFoundError(model)
    started = time.monotonic()
    source = Image.open(scene).convert("RGB")
    mask_image = Image.open(mask).convert("L").resize(source.size, Image.Resampling.NEAREST)
    source_array = np.asarray(source, dtype=np.float32) / 255.0
    mask_array = np.asarray(mask_image, dtype=np.float32) / 255.0
    if args.grow:
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (args.grow * 2 + 1, args.grow * 2 + 1))
        mask_array = cv2.dilate(mask_array, kernel)
    source_tensor = source_array.transpose(2, 0, 1)[None]
    mask_tensor = mask_array[None, None]
    # LaMa expects RGB in 0..1 with the masked pixels explicitly zeroed.
    model_input, (height, width) = pad_to_thirty_two(np.concatenate((source_tensor * (1.0 - mask_tensor), mask_tensor), axis=1))
    providers = [provider for provider in ("CUDAExecutionProvider", "CPUExecutionProvider") if provider in ort.get_available_providers()]
    session = ort.InferenceSession(model, providers=providers)
    generated = session.run(None, {session.get_inputs()[0].name: model_input})[0][0, :, :height, :width].transpose(1, 2, 0)
    # LaMa completes the masked content. Preserve every unmasked source pixel exactly.
    composite = generated * mask_array[..., None] + source_array * (1.0 - mask_array[..., None])
    output_dir.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(composite * 255.0, 0, 255).astype(np.uint8), mode="RGB").save(output)
    result.write_text(json.dumps({
        "status": "generated", "stage": "background_restore", "model": {"repository": MODEL_REPOSITORY, "file": str(model), "sha256": sha256(model), "license": MODEL_LICENSE},
        "scene": {"path": str(scene), "sha256": sha256(scene)}, "mask": {"path": str(mask), "sha256": sha256(mask)},
        "mask_semantics": "white=LaMa completion; black=exact source-pixel preservation", "mask_grow_px": args.grow, "providers": providers,
        "output": {"path": str(output), "sha256": sha256(output)}, "runtime": {"python": platform.python_version(), "onnxruntime": importlib.metadata.version("onnxruntime")},
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

"""Shared paths, image preprocessing, and provenance helpers for Qwen edits."""
from __future__ import annotations

import hashlib
import importlib.metadata
import platform
import sys
from pathlib import Path

from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent

PROJECT_ROOT = ASSETS.parents[3]

CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"

MODEL_ID = "Qwen/Qwen-Image-Edit-2511"

DEFAULT_CHARACTER = ASSETS / 'p7-5-3-qwen-edit-prompt-style-outfit_stage3_jacket_face-three-stage-v1-seed-62294-steps-10.png'

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
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
    }

def square_canvas(path: Path, size: int) -> Image.Image:
    """Return an RGB, white-backed square canvas without distorting the input."""
    with Image.open(path) as source:
        source = source.convert("RGBA")
        source.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - source.width) // 2, (size - source.height) // 2)
        canvas.alpha_composite(source, offset)
    return canvas.convert("RGB")

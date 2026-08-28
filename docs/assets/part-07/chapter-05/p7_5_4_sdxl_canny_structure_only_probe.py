"""Measure camera-structure control without an identity reference adapter."""

import json
import subprocess
import threading
import time
from pathlib import Path

import cv2
import numpy as np
import torch
from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline
from huggingface_hub import snapshot_download
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[4]
BASE_MODEL_ID = "cagliostrolab/animagine-xl-4.0"
CONTROLNET_ID = "diffusers/controlnet-canny-sdxl-1.0"
HF_HUB_CACHE = ROOT / ".tmp" / "download" / "huggingface" / "hub"
SOURCE = ROOT / "docs/assets/part-07/chapter-05/p7-5-2-mira-single-reference-14-side-walk-pause.png"
OUTPUT_DIR = Path("/tmp/p7-5-4-sdxl-canny-structure-only")
PROMPT = (
    "clean illustrated line art, one adult woman in left side profile, full body from head to both shoes, "
    "one hand holds a single crossbody bag strap, wide-leg trousers, white sneakers, white studio background"
)
NEGATIVE = "front view, three-quarter view, multiple people, cropped body, cut off feet, extra bag, extra strap, broken strap, deformed hands, text, watermark"


def gpu_memory_mib() -> int:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        check=False,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.splitlines()[0])


def canny(image: Image.Image) -> Image.Image:
    gray = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2GRAY)
    return Image.fromarray(cv2.Canny(gray, 100, 200)).convert("RGB")


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE).convert("RGB").resize((512, 768))
    control = canny(source)
    control.save(OUTPUT_DIR / "camera-control-canny.png")

    before = gpu_memory_mib()
    peak = before
    stop = threading.Event()

    def observe_peak() -> None:
        nonlocal peak
        while not stop.is_set():
            peak = max(peak, gpu_memory_mib())
            time.sleep(0.2)

    observer = threading.Thread(target=observe_peak, daemon=True)
    observer.start()
    started = time.monotonic()
    try:
        controlnet_path = Path(
            snapshot_download(CONTROLNET_ID, cache_dir=HF_HUB_CACHE, local_files_only=True)
        )
        base_model_path = Path(
            snapshot_download(BASE_MODEL_ID, cache_dir=HF_HUB_CACHE, local_files_only=True)
        )
        controlnet = ControlNetModel.from_pretrained(
            controlnet_path, torch_dtype=torch.float16, variant="fp16", local_files_only=True
        )
        pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
            base_model_path, controlnet=controlnet, torch_dtype=torch.float16,
            use_safetensors=True, local_files_only=True
        )
        pipe.enable_sequential_cpu_offload()
        pipe.enable_vae_slicing()
        pipe.set_progress_bar_config(disable=True)
        common = {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image": control,
            "width": 512,
            "height": 768,
            "num_inference_steps": 15,
            "guidance_scale": 7.0,
        }
        seed = 5101
        off = pipe(**common, controlnet_conditioning_scale=0.0, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]
        on = pipe(**common, controlnet_conditioning_scale=0.75, generator=torch.Generator(device="cuda").manual_seed(seed)).images[0]
        off.save(OUTPUT_DIR / "controlnet-off.png")
        on.save(OUTPUT_DIR / "controlnet-on.png")
        sheet = Image.new("RGB", (1536, 792), "white")
        draw = ImageDraw.Draw(sheet)
        for x, label, image in ((0, "Canny camera source", control), (512, "ControlNet off", off), (1024, "ControlNet on", on)):
            draw.text((x + 6, 5), label, fill="black")
            sheet.paste(image, (x, 24))
        sheet.save(OUTPUT_DIR / "contact-sheet.png")
        report = {
            "status": "review_required",
            "purpose": "structure-only camera baseline; no identity, style, face, or LoRA anchor",
            "base_model": "cagliostrolab/animagine-xl-4.0 (SDXL)",
            "controlnet": "diffusers/controlnet-canny-sdxl-1.0",
            "source_image": str(SOURCE),
            "control_input": "Canny edges only; source RGB is not passed to the pipeline",
            "identity_adapter": None,
            "resolution": [512, 768],
            "steps": 15,
            "guidance_scale": 7.0,
            "controlnet_scales": [0.0, 0.75],
            "seed": seed,
            "elapsed_seconds": round(time.monotonic() - started, 1),
            "gpu_memory_before_mib": before,
            "gpu_memory_peak_mib": peak,
            "outputs": ["camera-control-canny.png", "controlnet-off.png", "controlnet-on.png", "contact-sheet.png"],
        }
        (OUTPUT_DIR / "result.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    finally:
        stop.set()
        observer.join(timeout=2)


if __name__ == "__main__":
    main()

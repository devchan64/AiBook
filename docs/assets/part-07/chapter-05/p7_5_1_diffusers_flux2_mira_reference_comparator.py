"""Compare FLUX.2 Klein outputs against incompatible Mira reference inputs."""

import json
import os
import subprocess
import threading
import time
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook")
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
CACHE_DIR = Path("/tmp/flux2-klein-diffusers-cache")
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "/tmp/p7-5-1-flux2-mira-reference-comparator"))
WIDTH = int(os.environ.get("WIDTH", "512"))
HEIGHT = int(os.environ.get("HEIGHT", "768"))
MIRA_REFERENCE = ROOT / "docs/assets/part-07/chapter-05/p7-5-1-mira-single-reference-01.png"
MALE_REFERENCE = ROOT / "docs/assets/part-07/chapter-05/p7-5-1-comparator-male-webtoon-no-bag.png"
WATERCOLOR_REFERENCE = ROOT / "docs/assets/part-07/chapter-05/p7-5-1-comparator-woman-watercolor-no-bag.png"

MIRA_PROMPT = (
    "Create one polished full-body Korean webtoon panel of Mira, a young woman. "
    "Mira has a teal bob haircut with one silver hair clip, a white cropped utility jacket, "
    "teal wide-leg trousers, white sneakers, and a navy rectangular flap shoulder bag at her right hip "
    "with exactly one diagonal navy strap. She stands naturally at a quiet cinema ticket counter, "
    "holding one ticket in her left hand and looking at it. Show her complete body from head to shoes "
    "with correct human anatomy, expressive face, detailed hands, clean Korean webtoon line art, "
    "soft flat colors, and a readable cinema lobby background."
)

CASES = [
    ("mira_reference", MIRA_REFERENCE, "same character and style reference"),
    ("male_webtoon_reference", MALE_REFERENCE, "different male character, same broad webtoon style"),
    ("woman_watercolor_reference", WATERCOLOR_REFERENCE, "different woman character and watercolor-ink style"),
    ("text_only", None, "no image reference"),
]


def gpu_memory_mib() -> int:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        check=False,
        capture_output=True,
        text=True,
    )
    return int(result.stdout.splitlines()[0])


def generate(pipe, case_id: str, reference: Path | None, description: str, seed: int) -> dict:
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
        arguments = {
            "prompt": MIRA_PROMPT,
            "width": WIDTH,
            "height": HEIGHT,
            "num_inference_steps": 4,
            "guidance_scale": 1.0,
            "generator": torch.Generator(device="cpu").manual_seed(seed),
            "max_sequence_length": 256,
        }
        if reference is not None:
            arguments["image"] = Image.open(reference).convert("RGB")
        output = OUTPUT_DIR / f"{case_id}.png"
        pipe(**arguments).images[0].save(output)
        return {
            "case_id": case_id,
            "description": description,
            "reference_image": str(reference) if reference else None,
            "output_image": str(output),
            "elapsed_seconds": round(time.monotonic() - started, 1),
            "gpu_memory_before_mib": before,
            "gpu_memory_peak_mib": peak,
        }
    finally:
        stop.set()
        observer.join(timeout=2)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pipe = Flux2KleinPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR)
    pipe.enable_sequential_cpu_offload()
    global MIRA_PROMPT
    MIRA_PROMPT = os.environ.get("PROMPT_OVERRIDE", MIRA_PROMPT)
    results = [generate(pipe, *case, seed=320241 + index) for index, case in enumerate(CASES)]
    report = {
        "runtime": "diffusers-0.37.0",
        "model_id": MODEL_ID,
        "status": "completed",
        "width": WIDTH,
        "height": HEIGHT,
        "prompt": MIRA_PROMPT,
        "results": results,
    }
    (OUTPUT_DIR / "run.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

"""Run one public FLUX.2 Klein 4B reference-image preflight through InvokeAI."""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests


BASE_URL = "http://127.0.0.1:9090"
REFERENCE = Path(
    "/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05/"
    "p7-5-1-mira-single-reference-01.png"
)
OUTPUT_DIR = Path("/tmp/invokeai-flux2-klein-probe")

MODEL_SOURCES = {
    "model": "https://huggingface.co/unsloth/FLUX.2-klein-4B-GGUF/resolve/main/flux-2-klein-4b-Q4_K_M.gguf",
    "vae": "black-forest-labs/FLUX.2-klein-4B::vae",
    "encoder": "black-forest-labs/FLUX.2-klein-4B::text_encoder+tokenizer",
}


def gpu_memory_mib() -> int | None:
    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        capture_output=True,
        check=False,
        text=True,
    )
    try:
        return int(result.stdout.splitlines()[0])
    except (IndexError, ValueError):
        return None


def installed_model(source: str) -> dict:
    response = requests.get(f"{BASE_URL}/api/v2/models", timeout=30)
    response.raise_for_status()
    matches = [model for model in response.json()["models"] if model.get("source") == source]
    if len(matches) != 1:
        raise RuntimeError(f"Install exactly one model for source: {source}")
    return matches[0]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    model = installed_model(MODEL_SOURCES["model"])
    vae = installed_model(MODEL_SOURCES["vae"])
    encoder = installed_model(MODEL_SOURCES["encoder"])
    with REFERENCE.open("rb") as image_file:
        upload = requests.post(
            f"{BASE_URL}/api/v1/images/upload",
            params={"image_category": "general", "is_intermediate": "false"},
            files={"file": (REFERENCE.name, image_file, "image/png")},
            timeout=120,
        )
    upload.raise_for_status()
    image = upload.json()["image_name"]

    default_prompt = (
        "Create one polished full-body Korean webtoon panel of the exact same young woman in the reference image. "
        "Keep her teal bob haircut with one silver hair clip, white cropped utility jacket, teal wide-leg trousers, "
        "white sneakers, and the navy rectangular flap shoulder bag at her right hip with exactly one diagonal navy strap. "
        "She stands naturally at a quiet cinema ticket counter, holding one ticket in her left hand and looking at it. "
        "Show her complete body from head to shoes with correct human anatomy, expressive face, detailed hands, "
        "clean Korean webtoon line art, soft flat colors, and a readable cinema lobby background."
    )
    prompt = os.environ.get("PROMPT_OVERRIDE", default_prompt)
    graph = {
        "id": "flux2-klein-mira-reference-preflight",
        "nodes": {
            "loader": {
                "id": "loader",
                "type": "flux2_klein_model_loader",
                "model": model,
                "vae_model": vae,
                "qwen3_encoder_model": encoder,
                "max_seq_len": 256,
            },
            "prompt": {"id": "prompt", "type": "flux2_klein_text_encoder", "prompt": prompt},
            "positive": {"id": "positive", "type": "collect"},
            "reference": {"id": "reference", "type": "flux_kontext", "image": {"image_name": image}},
            "references": {"id": "references", "type": "collect"},
            "denoise": {
                "id": "denoise",
                "type": "flux2_denoise",
                "width": 512,
                "height": 768,
                "num_steps": 4,
                "scheduler": "euler",
                "seed": 320241,
                "cfg_scale": 1.0,
            },
            "decode": {"id": "decode", "type": "flux2_vae_decode", "is_intermediate": False},
        },
        "edges": [
            {"source": {"node_id": "loader", "field": "qwen3_encoder"}, "destination": {"node_id": "prompt", "field": "qwen3_encoder"}},
            {"source": {"node_id": "loader", "field": "max_seq_len"}, "destination": {"node_id": "prompt", "field": "max_seq_len"}},
            {"source": {"node_id": "prompt", "field": "conditioning"}, "destination": {"node_id": "positive", "field": "item"}},
            {"source": {"node_id": "loader", "field": "transformer"}, "destination": {"node_id": "denoise", "field": "transformer"}},
            {"source": {"node_id": "loader", "field": "vae"}, "destination": {"node_id": "denoise", "field": "vae"}},
            {"source": {"node_id": "positive", "field": "collection"}, "destination": {"node_id": "denoise", "field": "positive_text_conditioning"}},
            {"source": {"node_id": "reference", "field": "kontext_cond"}, "destination": {"node_id": "references", "field": "item"}},
            {"source": {"node_id": "references", "field": "collection"}, "destination": {"node_id": "denoise", "field": "kontext_conditioning"}},
            {"source": {"node_id": "denoise", "field": "latents"}, "destination": {"node_id": "decode", "field": "latents"}},
            {"source": {"node_id": "loader", "field": "vae"}, "destination": {"node_id": "decode", "field": "vae"}},
        ],
    }
    before = gpu_memory_mib()
    enqueue = requests.post(
        f"{BASE_URL}/api/v1/queue/default/enqueue_batch",
        json={"batch": {"graph": graph, "runs": 1, "origin": "flux2-klein-reference-preflight"}},
        timeout=120,
    )
    enqueue.raise_for_status()
    item_id = enqueue.json()["item_ids"][0]
    peak = before or 0
    started = time.monotonic()
    while True:
        peak = max(peak, gpu_memory_mib() or 0)
        item = requests.get(f"{BASE_URL}/api/v1/queue/default/i/{item_id}", timeout=30).json()
        if item["status"] == "completed":
            image_results = [
                value for value in item["session"]["results"].values() if value.get("type") == "image_output"
            ]
            if len(image_results) != 1:
                raise RuntimeError(f"Expected one image output, got {len(image_results)}")
            result = image_results[0]["image"]["image_name"]
            image_response = requests.get(f"{BASE_URL}/api/v1/images/i/{result}/full", timeout=120)
            image_response.raise_for_status()
            output_path = OUTPUT_DIR / os.environ.get(
                "OUTPUT_NAME", "p7-5-1-flux2-klein-reference-preflight.png"
            )
            output_path.write_bytes(image_response.content)
            report = {
                "status": "completed",
                "item_id": item_id,
                "elapsed_seconds": round(time.monotonic() - started, 1),
                "gpu_memory_before_mib": before,
                "gpu_memory_peak_mib": peak,
                "reference_image": str(REFERENCE),
                "output_image": str(output_path),
                "prompt": prompt,
            }
            (OUTPUT_DIR / "run.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
            print(json.dumps(report, indent=2))
            return
        if item["status"] in {"failed", "canceled"}:
            raise RuntimeError(json.dumps(item, indent=2))
        time.sleep(2)


if __name__ == "__main__":
    main()

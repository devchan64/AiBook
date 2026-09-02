#!/usr/bin/env python3
"""Create a person mask for a Qwen image with Apache-2.0 models."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from pathlib import Path

import torch
from huggingface_hub import snapshot_download
from PIL import Image, ImageDraw
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor, Sam2Model


ASSETS = Path(__file__).resolve().parent
HF_HUB_CACHE = ASSETS.parents[3] / ".tmp" / "download" / "huggingface" / "hub"
GROUNDING_DINO_ID = "IDEA-Research/grounding-dino-tiny"
SAM2_ID = "facebook/sam2.1-hiera-small"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def record(path: Path) -> dict[str, str]:
    return {"path": str(path), "sha256": sha256(path)}


def runtime() -> dict[str, object]:
    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "transformers": importlib.metadata.version("transformers"),
        "torch": importlib.metadata.version("torch"),
        "cuda_device": torch.cuda.get_device_name(0),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reference",
        type=Path,
        required=True,
        help="Image whose single person will be segmented.",
    )
    parser.add_argument("--run-label", default="v1")
    parser.add_argument("--threshold", type=float, default=0.20)
    parser.add_argument(
        "--exclude-rect",
        action="append",
        default=[],
        metavar="LEFT,TOP,RIGHT,BOTTOM",
        help="Optional background region to force black after SAM2 (repeatable).",
    )
    parser.add_argument("--output-dir", type=Path, default=ASSETS)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    reference = args.reference.resolve()
    if not reference.is_file():
        raise FileNotFoundError(reference)

    started = time.monotonic()
    image = Image.open(reference).convert("RGB")
    device = torch.device("cuda")

    detector_path = Path(snapshot_download(GROUNDING_DINO_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    detector_processor = AutoProcessor.from_pretrained(detector_path, local_files_only=True)
    detector = AutoModelForZeroShotObjectDetection.from_pretrained(detector_path, local_files_only=True).to(device).eval()
    labels = [["a woman", "a person"]]
    detector_inputs = detector_processor(images=image, text=labels, return_tensors="pt").to(device)
    with torch.inference_mode():
        detector_outputs = detector(**detector_inputs)
    detection = detector_processor.post_process_grounded_object_detection(
        detector_outputs,
        detector_inputs.input_ids,
        threshold=args.threshold,
        text_threshold=args.threshold,
        target_sizes=[image.size[::-1]],
    )[0]
    if not len(detection["boxes"]):
        raise RuntimeError("Grounding DINO did not detect the requested woman/person")
    index = int(torch.argmax(detection["scores"]).item())
    box = [round(value, 2) for value in detection["boxes"][index].tolist()]
    score = round(float(detection["scores"][index].item()), 4)
    label = str(detection["labels"][index])
    del detector, detector_processor, detector_inputs, detector_outputs
    torch.cuda.empty_cache()

    sam_path = Path(snapshot_download(SAM2_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    sam_processor = AutoProcessor.from_pretrained(sam_path, local_files_only=True)
    sam = Sam2Model.from_pretrained(sam_path, local_files_only=True).to(device).eval()
    sam_inputs = sam_processor(images=image, input_boxes=[[box]], return_tensors="pt").to(device)
    with torch.inference_mode():
        sam_outputs = sam(**sam_inputs, multimask_output=False)
    masks = sam_processor.post_process_masks(sam_outputs.pred_masks.cpu(), sam_inputs["original_sizes"])[0]
    mask = masks[0, 0].to(torch.uint8).numpy() * 255
    excluded_rectangles = []
    for value in args.exclude_rect:
        try:
            left, top, right, bottom = (int(part) for part in value.split(","))
        except ValueError as error:
            raise ValueError("--exclude-rect must be LEFT,TOP,RIGHT,BOTTOM") from error
        left, right = sorted((max(0, left), min(image.width, right)))
        top, bottom = sorted((max(0, top), min(image.height, bottom)))
        if left >= right or top >= bottom:
            raise ValueError("--exclude-rect must overlap the input image")
        mask[top:bottom, left:right] = 0
        excluded_rectangles.append([left, top, right, bottom])

    stem = f"p7-5-4-sam2-person-mask-{args.run_label}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / f"{stem}.png"
    overlay = args.output_dir / f"{stem}-overlay.png"
    result = args.output_dir / f"{stem}-result.json"
    Image.fromarray(mask, mode="L").save(output)
    preview = image.copy().convert("RGBA")
    color = Image.new("RGBA", image.size, (255, 0, 0, 0))
    color.putalpha(Image.fromarray((mask * 0.45).astype("uint8"), mode="L"))
    preview.alpha_composite(color)
    draw = ImageDraw.Draw(preview)
    draw.rectangle(box, outline=(255, 255, 0, 255), width=3)
    preview.convert("RGB").save(overlay)
    result.write_text(
        json.dumps(
            {
                "status": "generated",
                "stage": "person_mask",
                "purpose": "Person mask for Qwen Image Edit compositing or inpainting",
                "models": {
                    "detector": GROUNDING_DINO_ID,
                    "segmenter": SAM2_ID,
                    "licenses": {"detector": "Apache-2.0", "segmenter": "Apache-2.0"},
                },
                "input": record(reference),
                "input_role": "single-person image",
                "grounding_prompt": labels[0],
                "selected_detection": {"label": label, "score": score, "box_xyxy": box},
                "mask_semantics": "white=person to repaint; black=preserve",
                "postprocess": {"excluded_rectangles_xyxy": excluded_rectangles},
                "output": record(output),
                "overlay": record(overlay),
                "runtime": runtime(),
                "elapsed_seconds": round(time.monotonic() - started, 2),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"mask": str(output), "overlay": str(overlay), "result": str(result)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

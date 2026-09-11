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
import numpy as np
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
        help="Scene containing the person to segment.",
    )
    parser.add_argument("--query", nargs="+", default=["a woman", "a person"])
    parser.add_argument("--target-point", nargs=2, type=float, metavar=("X", "Y"),
                        help="Select the highest-score detection containing this visible person point.")
    parser.add_argument("--negative-point", nargs=2, type=float, action="append", default=[],
                        metavar=("X", "Y"), help="SAM2 background point, repeatable.")
    parser.add_argument("--positive-point", nargs=2, type=float, action="append", default=[],
                        metavar=("X", "Y"), help="Additional SAM2 foreground point, repeatable.")
    parser.add_argument("--box", nargs=4, type=float, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"),
                        help="Reviewed segmentation box override; original detection is still recorded.")
    parser.add_argument("--keep-largest-component", action="store_true",
                        help="Remove disconnected mask fragments after segmentation.")
    parser.add_argument("--keep-prompt-components", action="store_true",
                        help="Keep every component touched by foreground prompts, including occluded body parts.")
    parser.add_argument("--fill-holes-max-area", type=int, default=0,
                        help="Fill enclosed mask holes no larger than this pixel area.")
    parser.add_argument("--exclude-polygon", nargs="+", type=int, action="append", default=[],
                        help="Reviewed background polygon as X Y pairs; repeatable.")
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
    if args.fill_holes_max_area < 0:
        parser.error("--fill-holes-max-area must be nonnegative")
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    reference = args.reference.resolve()
    if not reference.is_file():
        raise FileNotFoundError(reference)
    stem = f"p7-5-5-sam2-person-mask-{args.run_label}"
    args.output_dir = args.output_dir.resolve()
    for suffix in (".png", "-overlay.png", "-result.json"):
        if (args.output_dir / f"{stem}{suffix}").exists():
            raise FileExistsError(f"Output already exists: {stem}{suffix}")

    started = time.monotonic()
    image = Image.open(reference).convert("RGB")
    for x, y in args.positive_point + args.negative_point:
        if not (0 <= x < image.width and 0 <= y < image.height):
            raise ValueError("All prompt points must be within the input image")
    device = torch.device("cuda")

    detector_path = Path(snapshot_download(GROUNDING_DINO_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    detector_processor = AutoProcessor.from_pretrained(detector_path, local_files_only=True)
    detector = AutoModelForZeroShotObjectDetection.from_pretrained(detector_path, local_files_only=True).to(device).eval()
    labels = [args.query]
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
    candidates = [
        {"index": i, "label": str(detection["labels"][i]),
         "score": float(detection["scores"][i]), "box_xyxy": box.tolist()}
        for i, box in enumerate(detection["boxes"])
    ]
    eligible = candidates
    if args.target_point:
        x, y = args.target_point
        if not (0 <= x < image.width and 0 <= y < image.height):
            raise ValueError("--target-point must be within the source image")
        eligible = [c for c in candidates if c["box_xyxy"][0] <= x <= c["box_xyxy"][2]
                    and c["box_xyxy"][1] <= y <= c["box_xyxy"][3]]
    if not eligible:
        raise RuntimeError(f"No detection contains target point; candidates: {candidates}")
    index = max(eligible, key=lambda c: c["score"])["index"]
    box = [round(value, 2) for value in detection["boxes"][index].tolist()]
    detected_box = box.copy()
    if args.box:
        left, top, right, bottom = args.box
        if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
            raise ValueError("--box must be ordered and inside the input image")
        box = args.box
    score = round(float(detection["scores"][index].item()), 4)
    label = str(detection["labels"][index])
    del detector, detector_processor, detector_inputs, detector_outputs
    torch.cuda.empty_cache()

    sam_path = Path(snapshot_download(SAM2_ID, cache_dir=HF_HUB_CACHE, local_files_only=True))
    sam_processor = AutoProcessor.from_pretrained(sam_path, local_files_only=True)
    sam = Sam2Model.from_pretrained(sam_path, local_files_only=True).to(device).eval()
    prompts = {}
    foreground = ([args.target_point] if args.target_point else []) + args.positive_point
    points = foreground + args.negative_point
    if points:
        prompts = {"input_points": [[points]],
                   "input_labels": [[[1] * len(foreground) + [0] * len(args.negative_point)]]}
    sam_inputs = sam_processor(images=image, input_boxes=[[box]], **prompts, return_tensors="pt").to(device)
    with torch.inference_mode():
        sam_outputs = sam(**sam_inputs, multimask_output=False)
    masks = sam_processor.post_process_masks(sam_outputs.pred_masks.cpu(), sam_inputs["original_sizes"])[0]
    mask = masks[0, 0].to(torch.uint8).numpy() * 255
    if args.keep_largest_component or args.keep_prompt_components or args.fill_holes_max_area:
        from scipy import ndimage

        if args.keep_largest_component or args.keep_prompt_components:
            components, count = ndimage.label(mask > 0)
            if not count:
                raise RuntimeError("SAM2 returned an empty mask")
            sizes = np.bincount(components.ravel())
            sizes[0] = 0
            if args.keep_prompt_components:
                keep = {int(components[int(y), int(x)]) for x, y in foreground}
                keep.discard(0)
                if not keep:
                    raise RuntimeError("No mask component contains a foreground prompt")
                mask = np.isin(components, list(keep)).astype("uint8") * 255
            else:
                mask = (components == sizes.argmax()).astype("uint8") * 255
        if args.fill_holes_max_area:
            holes = ndimage.binary_fill_holes(mask > 0) & (mask == 0)
            components, _ = ndimage.label(holes)
            sizes = np.bincount(components.ravel())
            fill = (components > 0) & (sizes[components] <= args.fill_holes_max_area)
            mask[fill] = 255
    for vertices in args.exclude_polygon:
        if len(vertices) < 6 or len(vertices) % 2:
            raise ValueError("--exclude-polygon requires at least three X Y pairs")
        polygon_mask = Image.fromarray(mask)
        ImageDraw.Draw(polygon_mask).polygon(list(zip(vertices[::2], vertices[1::2])), fill=0)
        mask = np.array(polygon_mask)
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

    # Exclusions can detach fragments that were connected before the review edits.
    if args.keep_prompt_components:
        from scipy import ndimage

        components, _ = ndimage.label(mask > 0)
        keep = {int(components[int(y), int(x)]) for x, y in foreground} - {0}
        mask = np.isin(components, list(keep)).astype("uint8") * 255

    stem = f"p7-5-5-sam2-person-mask-{args.run_label}"
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
                "input_role": "scene; one selected visible character",
                "selection": {"target_point_xy": args.target_point, "negative_points_xy": args.negative_point,
                              "positive_points_xy": args.positive_point, "box_override_xyxy": args.box,
                              "method": "highest score containing target point" if args.target_point else "highest score",
                              "candidates": candidates},
                "grounding_prompt": labels[0],
                "selected_detection": {"label": label, "score": score, "box_xyxy": detected_box},
                "segmentation_box_xyxy": box,
                "mask_semantics": "white=person to repaint; black=preserve",
                "postprocess": {"excluded_rectangles_xyxy": excluded_rectangles,
                                "keep_largest_component": args.keep_largest_component,
                                "keep_prompt_components": args.keep_prompt_components,
                                "fill_holes_max_area": args.fill_holes_max_area,
                                "excluded_polygons_xy": args.exclude_polygon},
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

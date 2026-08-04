"""Create unapproved accessory and body-feature detail candidates from approved views."""

import argparse
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
STYLE = ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png"
FRONT = ROOT / "p7-5-2-multireference-turnaround-v1-front.png"
PROFILE_LEFT = ROOT / "p7-5-2-multireference-turnaround-v1-profile-left.png"

FEATURES = {
    "hands-wrists": {
        "references": [(FRONT, (0.25, 0.48, 0.43, 0.70)), (STYLE, None)],
        "size": (768, 768),
        "output_crop": (0.30, 0.30, 0.72, 0.95),
        "framing": "single-hand close-up: the character's viewer-left hand, palm, fingers, wrist, and jacket cuff fill at least eighty percent of the frame, cropped directly above the wrist and directly below the fingertips; no second hand, face, torso, trousers, legs, or shoes",
        "contract": "one anatomically correct hand with exactly five clearly readable fingers, visible palm and wrist, short natural unpainted nails, no rings, bracelets, watch, bag strap, handheld object, or duplicate hand",
    },
    "jacket-hardware": {
        "source_detail": (FRONT, (0.25, 0.25, 0.75, 0.43)),
        "size": (768, 768),
        "framing": "deterministic jacket-only crop from the approved front reference, from collar to hem; no face, hands, trousers, legs, shoes, or scene",
        "contract": "approved white cropped utility jacket with two matching chest pockets and circular silver buttons; no reconstructed or newly invented garment detail",
    },
    "shoes": {
        "source_detail": (FRONT, (0.33, 0.85, 0.67, 0.99)),
        "size": (768, 512),
        "contain_source_detail": True,
        "framing": "deterministic shoe-only crop from the approved front reference, containing one matching left-right pair of white sneakers and the trouser hems immediately above them; no legs above the hems, face, torso, hands, or scene",
        "contract": "approved matching plain white lace-up low-top sneakers with clean toe caps, thin light-gray outsole, and trouser hems covering the ankles; no reconstructed footwear or newly invented accessory",
    },
}


def prompt(feature: dict[str, object]) -> str:
    return (
        "Create exactly one original Korean webtoon character detail-reference illustration. "
        "Keep the same adult woman from the character references: deep teal-blue bob, warm light-peach skin, white cropped utility jacket, "
        "charcoal crew-neck shirt, teal wide-leg trousers, and plain white sneakers. "
        f"Framing contract: {feature['framing']}. Feature contract: {feature['contract']}. "
        "Transfer only thin charcoal drawing lines, pale-blue and muted-teal transparent watercolor washes, soft off-white paper tone, and cool-gray shadows "
        "from the style reference. Use a quiet off-white studio background. No extra person, duplicate anatomy, text, logo, watermark, panel border, outer frame line, "
        "photorealism, glossy cel shading, opaque shadow blocks, or heavy hatching."
    )


def load_reference(path: Path, crop: tuple[float, float, float, float] | None) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if crop is None:
        return image
    width, height = image.size
    left, top, right, bottom = crop
    return image.crop((round(width * left), round(height * top), round(width * right), round(height * bottom)))


def crop_output(image: Image.Image, crop: tuple[float, float, float, float] | None) -> Image.Image:
    if crop is None:
        return image
    width, height = image.size
    left, top, right, bottom = crop
    detail = image.crop((round(width * left), round(height * top), round(width * right), round(height * bottom)))
    return detail.resize((width, height), Image.Resampling.LANCZOS)


def fit_source_detail(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    canvas = Image.new("RGB", size, "#f8f7f2")
    detail = image.copy()
    detail.thumbnail(size, Image.Resampling.LANCZOS)
    left = (size[0] - detail.width) // 2
    top = (size[1] - detail.height) // 2
    canvas.paste(detail, (left, top))
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature", choices=FEATURES, nargs="+")
    parser.add_argument("--seed-offset", type=int, default=0)
    args = parser.parse_args()
    features = args.feature if args.feature else list(FEATURES)

    pipe = None

    for feature_id in features:
        feature = FEATURES[feature_id]
        started = time.monotonic()
        source_detail = feature.get("source_detail")
        if source_detail:
            source_path, source_crop = source_detail
            image = load_reference(source_path, source_crop)
            if feature.get("contain_source_detail"):
                image = fit_source_detail(image, feature["size"])
            else:
                image = image.resize(feature["size"], Image.Resampling.LANCZOS)
        else:
            if pipe is None:
                pipe = Flux2KleinPipeline.from_pretrained(
                    "black-forest-labs/FLUX.2-klein-4B",
                    torch_dtype=torch.bfloat16,
                    cache_dir="/tmp/flux2-klein-diffusers-cache",
                )
                pipe.enable_sequential_cpu_offload()
                pipe.set_progress_bar_config(disable=True)
            image = pipe(
                image=[load_reference(path, crop) for path, crop in feature["references"]],
                prompt=prompt(feature),
                width=feature["size"][0],
                height=feature["size"][1],
                num_inference_steps=feature.get("steps", 8),
                guidance_scale=1.0,
                generator=torch.Generator(device="cpu").manual_seed(
                    62300 + list(FEATURES).index(feature_id) + args.seed_offset
                ),
                max_sequence_length=256,
            ).images[0]
        image = crop_output(image, feature.get("output_crop"))
        output = ROOT / f"p7-5-2-feature-detail-v1-{feature_id}-candidate.png"
        image.save(output)
        print(f"{feature_id}: {time.monotonic() - started:.2f}s -> {output}")


if __name__ == "__main__":
    main()

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
FACE_FRONT = ROOT / "p7-5-2-face-detail-v1-front.png"
JOY = ROOT / "p7-5-2-expression-detail-v1-joy.png"

FEATURES = {
    "hair-clip-ear": {
        "references": [(JOY, None), (STYLE, None)],
        "size": (768, 768),
        "framing": "front-left three-quarter close-up from the top of the hair to the lower neck, with the viewer-left temple, ear, and hair clip fully visible",
        "contract": "one diamond-shaped silver hair clip tilted 45 degrees above the viewer-left temple only, one visible ear, a jaw-length teal bob, no earrings or other jewelry",
    },
    "eyes-skin": {
        "references": [(FACE_FRONT, None), (STYLE, None)],
        "size": (768, 768),
        "framing": "straight-on close-up from the hairline to the chin",
        "contract": "two dark-brown almond eyes, even warm light-peach skin, a small straight nose, a calm closed mouth, and no freckles, scars, makeup marks, or tears",
    },
    "hands-wrists": {
        "references": [(FRONT, (0.16, 0.34, 0.84, 0.72)), (STYLE, None)],
        "size": (768, 640),
        "framing": "mid-torso crop with both relaxed hands, wrists, jacket cuffs, and upper trousers fully visible",
        "contract": "two hands with five fingers each, short natural unpainted nails, no rings, bracelets, watch, bag strap, or handheld object",
    },
    "jacket-hardware": {
        "references": [(FRONT, (0.14, 0.18, 0.86, 0.58)), (STYLE, None)],
        "size": (768, 768),
        "framing": "front upper-torso crop from the chin to the waist, with collar, chest pockets, buttons, and both cuffs visible",
        "contract": "white cropped utility jacket, charcoal shirt, two matching chest pockets, circular silver buttons, and no logo, badge, zipper pull, or hanging strap",
    },
    "shoes": {
        "references": [(FRONT, (0.16, 0.72, 0.84, 1.0)), (STYLE, None)],
        "size": (768, 640),
        "framing": "shoe-focused lower-leg crop from below the knees to the shoe soles, with both sneakers occupying most of the image, both feet planted apart on one ground plane, and both full soles visible",
        "contract": "one pair of matching plain white lace-up low-top sneakers, clean toe caps, five eyelets per shoe, thin light-gray outsole, and trouser hems covering both ankles completely; no visible skin at the ankles, no ankle chain, sock jewelry, colored logo, heel lift, extra shoe, or hidden sole",
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--feature", choices=FEATURES, nargs="+")
    parser.add_argument("--seed-offset", type=int, default=0)
    args = parser.parse_args()
    features = args.feature if args.feature else list(FEATURES)

    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B", torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache"
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    for feature_id in features:
        feature = FEATURES[feature_id]
        started = time.monotonic()
        image = pipe(
            image=[load_reference(path, crop) for path, crop in feature["references"]],
            prompt=prompt(feature),
            width=feature["size"][0],
            height=feature["size"][1],
            num_inference_steps=8,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(
                62300 + list(FEATURES).index(feature_id) + args.seed_offset
            ),
            max_sequence_length=256,
        ).images[0]
        output = ROOT / f"p7-5-2-feature-detail-v1-{feature_id}-candidate.png"
        image.save(output)
        print(f"{feature_id}: {time.monotonic() - started:.2f}s -> {output}")


if __name__ == "__main__":
    main()

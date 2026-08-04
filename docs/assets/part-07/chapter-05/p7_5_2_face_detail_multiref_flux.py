"""Create unapproved face-detail reference candidates from the four-view baseline."""

import argparse
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
STYLE = ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png"
VIEWS = {
    "front": ROOT / "p7-5-2-multireference-turnaround-v1-front.png",
    "profile_left": ROOT / "p7-5-2-multireference-turnaround-v1-profile-left.png",
    "rear": ROOT / "p7-5-2-multireference-turnaround-v1-rear.png",
}
OUT = ROOT

VARIANTS = [
    {
        "id": "front",
        "references": [VIEWS["front"], STYLE],
        "camera_contract": "straight-on front head-and-shoulders view; face, neck, and both shoulders point directly toward the viewer",
    },
    {
        "id": "three-quarter-left",
        "references": [VIEWS["front"], VIEWS["profile_left"], STYLE],
        "camera_contract": "front-left three-quarter head-and-shoulders view; face, nose, neck, and shoulders all rotate 45 degrees toward image-left; both eyes remain visible",
    },
    {
        "id": "profile-left",
        "references": [VIEWS["profile_left"], VIEWS["front"], STYLE],
        "camera_contract": "strict left side head-and-shoulders profile; nose, chin, gaze, neck, and shoulders all point image-left; show one visible eye only",
    },
    {
        "id": "rear",
        "references": [VIEWS["rear"], VIEWS["front"], STYLE],
        "camera_contract": "straight rear head-and-shoulders view; show the back of the teal bob, hair clip placement, nape, rear collar, and both shoulders; show no face",
    },
]


def prompt(camera_contract: str) -> str:
    return (
        "Create exactly one original Korean webtoon character face-detail reference, cropped from the top of the hair to the upper chest. "
        "Keep the same adult woman from the character reference: jaw-length deep teal-blue bob, rectangular silver hair clip, warm light-peach skin, "
        "dark-brown almond eyes, calm neutral expression, white cropped utility jacket, and charcoal crew-neck shirt. "
        "Transfer only the thin charcoal drawing lines, pale-blue and muted-teal transparent watercolor washes, soft off-white paper tone, and cool-gray shadows "
        "from the style reference. "
        f"Camera contract: {camera_contract}. "
        "Preserve one coherent head, one neck, and one pair of shoulders. No bag, strap, jewelry, handheld object, extra person, duplicate face, extra eyes, "
        "cropped chin, text, logo, watermark, panel border, outer frame line, photorealism, glossy cel shading, opaque shadows, or heavy hatching."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=[item["id"] for item in VARIANTS])
    args = parser.parse_args()
    variants = [item for item in VARIANTS if args.variant is None or item["id"] == args.variant]

    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B", torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache"
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    for offset, variant in enumerate(variants):
        started = time.monotonic()
        image = pipe(
            image=[Image.open(path).convert("RGB") for path in variant["references"]],
            prompt=prompt(variant["camera_contract"]),
            width=768,
            height=1024,
            num_inference_steps=8,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(62110 + offset),
            max_sequence_length=256,
        ).images[0]
        output = OUT / f"p7-5-2-face-detail-v1-{variant['id']}-candidate.png"
        image.save(output)
        print(f"{variant['id']}: {time.monotonic() - started:.2f}s -> {output}")


if __name__ == "__main__":
    main()

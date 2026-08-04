"""Create unapproved face-detail reference candidates from the four-view baseline."""

import argparse
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
STYLE = ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png"
FRONT_FACE = ROOT / "p7-5-2-face-detail-v2-front-iris-pupil-spec.png"
VIEWS = {
    "front": ROOT / "p7-5-2-multireference-turnaround-v1-front.png",
    "profile_left": ROOT / "p7-5-2-multireference-turnaround-v1-profile-left.png",
    "profile_right": ROOT / "p7-5-2-multireference-turnaround-v1-profile-right.png",
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
        "id": "front-iris-pupil-spec",
        "references": [VIEWS["front"], STYLE],
        "camera_contract": "strict zero-yaw straight-on front head-and-shoulders view; face, nose bridge, chin, neck, and both shoulders point directly toward the viewer, with both eyes level and equal in size; no three-quarter turn, profile, tilted head, full body, or nested character",
        "detail_contract": "Draw the face first, then apply one matched eye specification to both eyes: almond-shaped dark chestnut-brown irises with the same dark limbal ring, one round black pupil centered inside each iris, and one small oval white catchlight at the upper viewer-left of each iris. Keep both eyes equal in size, shape, iris color, pupil placement, and catchlight position. Keep exactly one diamond-shaped silver hair clip tilted 45 degrees above the viewer-left temple, with no second clip or ornament.",
        "steps": 8,
        "output": "p7-5-2-face-detail-v2-front-iris-pupil-spec.png",
    },
    {
        "id": "three-quarter-left",
        "references": [FRONT_FACE, VIEWS["profile_left"], STYLE],
        "camera_contract": "front-left three-quarter head-and-shoulders view; face, nose, neck, and shoulders all rotate 45 degrees toward image-left; both eyes remain visible but the image-left eye is narrower; no mirror copy of the front view",
        "detail_contract": "Preserve the approved dark chestnut-brown iris color, centered pupil, and upper viewer-left catchlight in both visible eyes. Keep one diamond-shaped silver hair clip only on the viewer-left temple, with the face and body turned together.",
        "output": "p7-5-2-face-detail-v2-three-quarter-left-candidate.png",
    },
    {
        "id": "profile-left",
        "references": [FRONT_FACE, VIEWS["profile_left"], STYLE],
        "camera_contract": "strict left side head-and-shoulders profile; nose, chin, gaze, neck, and shoulders all point image-left; show one visible eye only, with no second eye contour or front-facing shoulders",
        "detail_contract": "Use the approved brown iris and centered pupil for the one visible eye. Do not mirror the face or duplicate the hair clip.",
        "output": "p7-5-2-face-detail-v2-profile-left-candidate.png",
    },
    {
        "id": "three-quarter-right",
        "references": [FRONT_FACE, VIEWS["profile_right"], STYLE],
        "camera_contract": "front-right three-quarter head-and-shoulders view; face, nose, neck, and shoulders all rotate 45 degrees toward image-right; both eyes remain visible but the image-right eye is narrower; no mirror copy of the front-left three-quarter view",
        "detail_contract": "Preserve the approved dark chestnut-brown iris color, centered pupil, and upper viewer-left catchlight in both visible eyes. Keep the single diamond-shaped silver hair clip on its original character side; it may be partly hidden by the head rotation but must not move to the opposite temple or duplicate.",
        "output": "p7-5-2-face-detail-v2-three-quarter-right-candidate.png",
    },
    {
        "id": "profile-right",
        "references": [FRONT_FACE, VIEWS["profile_right"], STYLE],
        "camera_contract": "strict right side head-and-shoulders profile; nose, chin, gaze, neck, and shoulders all point image-right; show one visible eye only, with no second eye contour or front-facing shoulders",
        "detail_contract": "Use the approved brown iris and centered pupil for the one visible eye. Keep the single hair clip on its original character side without mirroring or duplication.",
        "output": "p7-5-2-face-detail-v2-profile-right-candidate.png",
    },
    {
        "id": "rear-hair",
        "references": [FRONT_FACE, VIEWS["rear"], STYLE],
        "camera_contract": "straight rear head-and-shoulders view; show the back of the jaw-length teal bob, nape, rear collar, and both shoulders; show no face, eye, nose, mouth, or front hairline",
        "detail_contract": "Preserve the bob length, back silhouette, and the original side-specific hair-clip attachment without inventing a second clip. This view defines rear hair only, not facial identity.",
        "output": "p7-5-2-face-detail-v2-rear-hair-candidate.png",
    },
]


def prompt(camera_contract: str, detail_contract: str = "") -> str:
    return (
        "Create exactly one original Korean webtoon character face-detail reference, cropped from the top of the hair to the upper chest. "
        "Keep the same adult woman from the character reference: jaw-length deep teal-blue bob, one diamond-shaped silver hair clip, warm light-peach skin, "
        "dark-brown almond eyes, calm neutral expression, white cropped utility jacket, and charcoal crew-neck shirt. "
        "Transfer only the thin charcoal drawing lines, pale-blue and muted-teal transparent watercolor washes, soft off-white paper tone, and cool-gray shadows "
        "from the style reference. "
        f"Camera contract: {camera_contract}. "
        f"Detail contract: {detail_contract} "
        "Preserve one coherent head, one neck, and one pair of shoulders. No bag, strap, jewelry, handheld object, extra person, duplicate face, extra eyes, "
        "cropped chin, text, logo, watermark, panel border, outer frame line, photorealism, glossy cel shading, opaque shadows, or heavy hatching."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=[item["id"] for item in VARIANTS])
    parser.add_argument("--seed-offset", type=int, default=0)
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
            prompt=prompt(variant["camera_contract"], variant.get("detail_contract", "")),
            width=768,
            height=1024,
            num_inference_steps=variant.get("steps", 8),
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(62110 + offset + args.seed_offset),
            max_sequence_length=256,
        ).images[0]
        output = OUT / variant.get("output", f"p7-5-2-face-detail-v1-{variant['id']}-candidate.png")
        image.save(output)
        print(f"{variant['id']}: {time.monotonic() - started:.2f}s -> {output}")


if __name__ == "__main__":
    main()

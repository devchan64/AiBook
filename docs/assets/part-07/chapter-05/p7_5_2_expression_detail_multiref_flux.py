"""Create unapproved frontal expression-detail candidates from approved references."""

import argparse
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
CHARACTER = ROOT / "p7-5-2-multireference-turnaround-v1-front.png"
STYLE = ROOT / "p7-5-1-style-park-clear-day-eye-level-local-gpu-v1.png"

EXPRESSIONS = {
    "neutral": "level relaxed eyebrows, open centered almond eyes, a smooth nose bridge with relaxed nostrils, and a straight closed mouth",
    "joy": "outer eyebrows gently raised, upper eyelids lowered into smiling eyes, lower eyelids lifted, cheeks raised around the nose, and mouth corners clearly lifted into a closed smile",
    "concern": "inner eyebrows lifted high and tightly drawn together, two clear vertical creases between the brows above the nose bridge, eyes opened wider with pupils shifted upward, visibly flared nostrils, and a tense open mouth with the lower lip pulled down",
    "anger": "eyebrows forced sharply down and inward into a strong V, deep vertical creases at the nose bridge, narrowed glaring eyes with pupils aimed forward, tense lower lids, flared nostrils, and a wide hard mouth with clenched visible upper teeth; no shouting",
    "sadness": "inner eyebrows arched high, outer eyebrows lowered, upper eyelids drooping with pupils looking down, lower eyelids raised, nostrils relaxed, and a visibly trembling open mouth with both corners pulled clearly downward; no tears",
    "surprise": "eyebrows raised far above the eyes, round fully widened eyes with small centered pupils, visibly flared nostrils, and a large rounded open O-shaped mouth with the lower jaw dropped",
}


def prompt(expression: str) -> str:
    return (
        "Create exactly one original Korean webtoon character expression-detail reference, cropped from the top of the hair to the upper chest. "
        "Keep the same adult woman from the character reference: jaw-length deep teal-blue bob, rectangular silver hair clip, warm light-peach skin, "
        "dark-brown almond eyes, white cropped utility jacket, and charcoal crew-neck shirt. "
        "Face, neck, and both shoulders point directly forward. Keep head size, hairline, jaw, ear position, jacket collar, and one single diamond-shaped silver hair clip tilted 45 degrees above the viewer-left temple identical across expressions. "
        f"Expression contract: {expression}. "
        "The visible change must be in the eyebrows, eyelids, pupils, nose bridge or nostrils, and mouth; do not merely change the background, lighting, or head angle. "
        "Transfer only thin charcoal drawing lines, pale-blue and muted-teal transparent watercolor washes, soft off-white paper tone, and cool-gray shadows "
        "from the style reference. Preserve one coherent face with two eyes, one nose, one mouth, one neck, and both shoulders. "
        "No bag, strap, jewelry, handheld object, extra person, duplicate face, extra eyes, text, logo, watermark, panel border, outer frame line, "
        "photorealism, glossy cel shading, opaque shadows, heavy hatching, or dramatic scene lighting."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expression", choices=EXPRESSIONS)
    args = parser.parse_args()
    expressions = [args.expression] if args.expression else list(EXPRESSIONS)

    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B", torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache"
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    for expression in expressions:
        started = time.monotonic()
        image = pipe(
            image=[Image.open(CHARACTER).convert("RGB"), Image.open(STYLE).convert("RGB")],
            prompt=prompt(EXPRESSIONS[expression]),
            width=768,
            height=1024,
            num_inference_steps=8,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(62200 + list(EXPRESSIONS).index(expression)),
            max_sequence_length=256,
        ).images[0]
        output = ROOT / f"p7-5-2-expression-detail-v1-{expression}-candidate.png"
        image.save(output)
        print(f"{expression}: {time.monotonic() - started:.2f}s -> {output}")


if __name__ == "__main__":
    main()

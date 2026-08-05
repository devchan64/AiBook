"""Create unapproved frontal expression candidates from the approved face."""

import argparse
import json
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path("/home/cbsim/ws/AiBook/docs/assets/part-07/chapter-05")
CHARACTER = ROOT / "p7-5-2-face-front-v2.png"
REPORT = ROOT / "p7-5-2-expression-v2-review.json"

EXPRESSIONS = {
    "neutral": "relaxed level eyebrows, open centered almond eyes, relaxed nostrils, and a straight closed mouth",
    "joy": "outer eyebrows gently raised, upper eyelids softly lowered into smiling eyes, lower eyelids lifted, cheeks visibly raised around the nose, and both mouth corners lifted into a broad closed-mouth smile",
    "concern": "soft high worried eyebrows with inner ends drawn together, alert open eyes looking slightly image-right, one small worry crease, and a narrow tense closed mouth",
    "anger": "eyebrows sharply down and inward into a clear V, a deep vertical crease between the brows, narrowed eyes with forward pupils, tense lower lids, flared nostrils, and lips pressed into a flat hard line",
    "sadness": "inner eyebrows raised into a soft inverted V, drooping eyelids with lowered pupils, a small closed mouth with evenly downturned corners, and two small tears pooled at the lower eyelids",
    "surprise": "eyebrows raised high, upper eyelids lifted, round widened eyes with small centered pupils, slightly flared nostrils, and a visibly lowered jaw forming an open rounded O-shaped mouth",
}


def prompt(expression: str) -> str:
    return (
        "Frontal head-only expression reference of the same adult Korean webtoon woman on off-white paper. "
        "Use the face reference for identity, deep teal-blue jaw-length bob, warm light-peach skin, almond cat eyes, chestnut-brown and amber radial-wave irises with dark limbal rings and black pupils, high straight nose bridge, broad low-set cheekbones, and soft cheek fullness. "
        "Show full hair, face, jaw, and chin only; the lower edge ends directly beneath the chin. "
        f"Expression contract: {expression}. "
        "Change only eyebrows, eyelids, pupils, nostrils, and mouth while preserving face shape, hair, camera direction, and neutral paper background."
    )


def prompt_word_count(text: str) -> int:
    return len(text.split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--targets",
        nargs="+",
        choices=tuple(EXPRESSIONS),
        default=tuple(EXPRESSIONS),
        help="Expression IDs to generate. Omit to generate neutral, joy, concern, anger, sadness, and surprise.",
    )
    parser.add_argument("--seed-offset", type=int, default=0)
    parser.add_argument("--steps", type=int, default=8)
    args = parser.parse_args()
    expressions = args.targets

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B", torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache"
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)
    runs = []
    for expression in expressions:
        started = time.monotonic()
        rendered_prompt = prompt(EXPRESSIONS[expression])
        image = pipe(
            image=[Image.open(CHARACTER).convert("RGB")],
            prompt=rendered_prompt,
            width=768,
            height=768,
            num_inference_steps=args.steps,
            guidance_scale=1.0,
            generator=torch.Generator(device="cpu").manual_seed(
                62200 + list(EXPRESSIONS).index(expression) + args.seed_offset
            ),
            max_sequence_length=256,
        ).images[0]
        output = ROOT / f"p7-5-2-expression-v2-{expression}-candidate.png"
        image.save(output)
        elapsed = round(time.monotonic() - started, 2)
        runs.append(
            {
                "expression": expression,
                "output": output.name,
                "seed": 62200 + list(EXPRESSIONS).index(expression) + args.seed_offset,
                "prompt": rendered_prompt,
                "prompt_word_count": prompt_word_count(rendered_prompt),
                "elapsed_seconds": elapsed,
            }
        )
        print(f"{expression}: {elapsed:.2f}s -> {output}")

    REPORT.write_text(
        json.dumps(
            {
                "status": "review_required",
                "input": CHARACTER.name,
                "model": "black-forest-labs/FLUX.2-klein-4B",
                "image_size": [768, 768],
                "runs": runs,
                "decision": "Each expression is a candidate; human review is required before it becomes a facial expression reference.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

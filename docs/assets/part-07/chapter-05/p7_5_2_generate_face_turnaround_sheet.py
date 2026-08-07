#!/usr/bin/env python3
"""Generate individual directional face candidates from the frontal identity anchor."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import isqrt
from pathlib import Path
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image


ROOT = Path(__file__).resolve().parent
FRONT = ROOT / "p7-5-2-face-front-reference.png"
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
FACE_IDENTITY_CONTRACT_PATH = ROOT / "p7-5-2-face-identity-contract.json"
FACE_IDENTITY_CONTRACT = json.loads(FACE_IDENTITY_CONTRACT_PATH.read_text(encoding="utf-8"))
BASE_SEED = 62294
HEAD_INPUT_BOTTOM = 720
IMAGE_SIZE = 768
VIEW_RULES = {
    "front_quarter_left": (
        "45-degree front-quarter view turned toward the viewer's left, showing the subject's right side; "
        "the near right eye is fully visible and the far left eye is half visible"
    ),
    "front_quarter_right": (
        "45-degree front-quarter view turned toward the viewer's right, showing the subject's left side; "
        "the near left eye is fully visible and the far right eye is half visible"
    ),
    "profile_left": (
        "strict 90-degree profile turned toward the viewer's left, showing the subject's right side; "
        "only the near right eye is visible in side view and the far left eye is hidden"
    ),
    "profile_right": (
        "strict 90-degree profile turned toward the viewer's right, showing the subject's left side; "
        "only the near left eye is visible in side view and the far right eye is hidden"
    ),
    "rear": (
        "strict 180-degree rear view, facing directly away from the camera: show only the back of the bob haircut, "
        "back of head, ears if exposed, and nape; no face, eye, eyebrow, nose, lips, cheek, or side-profile outline"
    ),
}
TURNAROUND_FIDELITY_RULE = (
    "Keep visible radial iris texture, equal iris and pupil size and proportion, allowing only perspective foreshortening. "
    "Keep the visible gaze direction aligned with the nose direction."
)


def prompt_word_count(text: str) -> int:
    return len(text.split())


def output_contract_hash(prompt: str, view: str, seed: int, steps: int) -> str:
    """Return a stable short hash for the unified generation contract."""
    contract = json.dumps(
        {
            "model": MODEL_ID,
            "view": view,
            "seed": seed,
            "prompt": prompt,
            "image_size": [IMAGE_SIZE, IMAGE_SIZE],
            "steps": steps,
            "guidance_scale": 1.0,
            "identity_contract": FACE_IDENTITY_CONTRACT_PATH.name,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256(contract.encode("utf-8")).hexdigest()[:10]


def build_turnaround_prompt(view: str) -> str:
    identity_rule = (
        f"Preserve only {FACE_IDENTITY_CONTRACT['rear_hair_identity']} Do not reveal a face."
        if view == "rear"
        else f"{FACE_IDENTITY_CONTRACT['identity_description']} {TURNAROUND_FIDELITY_RULE}"
    )
    return (
        "One individual head-and-neck directional portrait of the same woman from the supplied frontal reference. "
        f"Fixed direction: {VIEW_RULES[view]}. "
        f"{identity_rule} "
        "Plain off-white background, one person, no text, no panels, no collage."
    )
def make_preview_callback(
    pipe: Flux2KleinPipeline,
    *,
    preview_prefix: Path,
    steps: int,
    interval: int,
) -> tuple[object | None, list[str]]:
    """Decode and save review-only FLUX previews after each interval of denoising steps."""
    if interval == 0:
        return None, []

    saved: list[str] = []

    def callback(pipeline: Flux2KleinPipeline, step: int, _timestep: int, callback_kwargs: dict) -> dict:
        completed_steps = step + 1
        if completed_steps % interval != 0 and completed_steps != steps:
            return callback_kwargs

        packed_latents = callback_kwargs["latents"]
        latent_side = isqrt(packed_latents.shape[1])
        if latent_side * latent_side != packed_latents.shape[1]:
            raise ValueError("Preview decoding requires square latent tokens")
        latent_ids = pipeline._prepare_latent_ids(
            torch.empty(
                (packed_latents.shape[0], 1, latent_side, latent_side),
                device=packed_latents.device,
                dtype=packed_latents.dtype,
            )
        ).to(packed_latents.device)
        with torch.no_grad():
            latents = pipeline._unpack_latents_with_ids(packed_latents, latent_ids)
            mean = pipeline.vae.bn.running_mean.view(1, -1, 1, 1).to(latents.device, latents.dtype)
            std = torch.sqrt(
                pipeline.vae.bn.running_var.view(1, -1, 1, 1) + pipeline.vae.config.batch_norm_eps
            ).to(latents.device, latents.dtype)
            image = pipeline.vae.decode(pipeline._unpatchify_latents(latents * std + mean), return_dict=False)[0]
            preview = pipeline.image_processor.postprocess(image, output_type="pil")[0]
        preview_path = preview_prefix.with_name(f"{preview_prefix.name}-preview-step-{completed_steps:03d}.png")
        preview.save(preview_path)
        saved.append(preview_path.name)
        return callback_kwargs

    return callback, saved


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--views",
        nargs="+",
        choices=tuple(VIEW_RULES),
        default=tuple(VIEW_RULES),
        help="Non-front directions to generate; front is produced by the dedicated front-face generator.",
    )
    parser.add_argument("--seed-offset", type=int, default=0, help="Offset applied to the first seed.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of consecutive seed variants.")
    parser.add_argument("--seed-step", type=int, default=1, help="Increment between seed variants.")
    parser.add_argument("--steps", type=int, default=3, help="Denoising steps for the unified generation.")
    parser.add_argument(
        "--preview-interval",
        type=int,
        default=0,
        help="Save a decoded FLUX preview every N denoising steps; use 0 to disable previews.",
    )
    parser.add_argument(
        "--output-prefix",
        default="p7-5-2-face-direction",
        help="Prefix placed before view, contract hash, seed, and step suffixes.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.seed_count < 1:
        raise ValueError("seed-count must be at least 1")
    if args.seed_step == 0:
        raise ValueError("seed-step must not be zero")
    if args.steps < 1:
        raise ValueError("steps must be at least 1")
    if args.preview_interval < 0:
        raise ValueError("preview-interval must be zero or a positive integer")
    if not FRONT.is_file():
        raise FileNotFoundError(FRONT.name)
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    pipe = Flux2KleinPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.bfloat16,
        cache_dir="/tmp/flux2-klein-diffusers-cache",
    )
    pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    with Image.open(FRONT) as source:
        anchor = source.convert("RGB").crop((0, 0, source.width, HEAD_INPUT_BOTTOM))
    first_seed = BASE_SEED + args.seed_offset
    for batch_index in range(args.seed_count):
        seed = first_seed + batch_index * args.seed_step
        for view in args.views:
            prompt = build_turnaround_prompt(view)
            contract_hash = output_contract_hash(prompt, view, seed, args.steps)
            stem = f"{args.output_prefix}-{view}-hash-{contract_hash}-seed-{seed}-steps-{args.steps}"
            candidate = ROOT / f"{stem}-candidate.png"
            report = ROOT / f"{stem}-review.json"
            started = time.monotonic()
            callback, previews = make_preview_callback(
                pipe,
                preview_prefix=candidate.with_suffix(""),
                steps=args.steps,
                interval=args.preview_interval,
            )
            image = pipe(
                image=anchor,
                prompt=prompt,
                width=IMAGE_SIZE,
                height=IMAGE_SIZE,
                num_inference_steps=args.steps,
                guidance_scale=1.0,
                generator=torch.Generator(device="cpu").manual_seed(seed),
                max_sequence_length=256,
                callback_on_step_end=callback,
                callback_on_step_end_tensor_inputs=["latents"],
            ).images[0]
            image.save(candidate)

            elapsed = round(time.monotonic() - started, 2)
            report.write_text(
                json.dumps(
                    {
                        "status": "review_required",
                        "output": candidate.name,
                        "view": view,
                        "seed": seed,
                        "contract_hash": contract_hash,
                        "steps": args.steps,
                        "preview_interval": args.preview_interval,
                        "seed_offset": args.seed_offset,
                        "seed_step": args.seed_step,
                        "batch_index": batch_index,
                        "batch_size": args.seed_count,
                        "output_prefix": args.output_prefix,
                        "generation": {
                            "prompt": prompt,
                            "prompt_word_count": prompt_word_count(prompt),
                            "identity_reference": FRONT.name,
                            "previews": previews,
                        },
                        "references": [FRONT.name],
                        "identity_contract": FACE_IDENTITY_CONTRACT_PATH.name,
                        "input_transform": f"Cropped the frontal anchor at y={HEAD_INPUT_BOTTOM} before inference.",
                        "model": MODEL_ID,
                        "image_size": [IMAGE_SIZE, IMAGE_SIZE],
                        "elapsed_seconds": elapsed,
                        "decision": "Candidate only; review direction and identity preservation against the frontal anchor.",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            print(f"[{batch_index + 1}/{args.seed_count}] {view}: {elapsed:.2f}s -> {candidate}")


if __name__ == "__main__":
    main()

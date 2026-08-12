#!/usr/bin/env python3
"""Render P7-5.2 identity anchors in the approved P7-5.1 visual style.

Every output remains a candidate until separately approved.  The source image
preserves identity, direction, and outfit; the style reference supplies only
the restrained webtoon-watercolor rendering contract.
"""

from __future__ import annotations

import argparse
import gc
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image

from p7_5_image_output_naming import candidate_stem, preview_callback


ROOT = Path(__file__).resolve().parent
MODEL_ID = "black-forest-labs/FLUX.2-klein-4B"
STYLE_REFERENCE = ROOT / "p7-5-1-style-atrium-dawn-high-angle-local-gpu-v5.png"
IDENTITY = json.loads((ROOT / "p7-5-2-character-identity-contract.json").read_text(encoding="utf-8"))
VIEWS = ("front", "front_quarter_left", "front_quarter_right", "profile_left", "profile_right", "rear")
VIEW = {
    "front": "front view", "front_quarter_left": "left three-quarter view", "front_quarter_right": "right three-quarter view",
    "profile_left": "left profile", "profile_right": "right profile", "rear": "rear back-of-head view",
}


@dataclass(frozen=True)
class Spec:
    candidate_id: str
    source_type: str
    view: str
    outfit: str

    @property
    def source(self) -> Path:
        if self.source_type == "face":
            return ROOT / f"p7-5-2-face-{self.view.replace('_', '-')}-reference.png"
        suffix = "-refined" if self.source_type == "refined" else ""
        return ROOT / f"p7-5-2-fullbody-{self.view.replace('_', '-')}{suffix}-reference.png"


SPECS = tuple(
    [Spec(f"face-{view}", "face", view, "") for view in VIEWS]
    + [Spec(f"basic-{view}", "basic", view, "charcoal crop top, deep teal wide-leg trousers, white sneakers") for view in VIEWS]
    + [Spec(f"refined-{view}", "refined", view, "white cropped utility jacket, charcoal crop top, deep teal wide-leg trousers, white sneakers, navy crossbody bag") for view in VIEWS]
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", nargs="+", choices=tuple(spec.candidate_id for spec in SPECS), default=tuple(spec.candidate_id for spec in SPECS))
    parser.add_argument("--seed", type=int, default=62294)
    parser.add_argument("--steps", type=int, default=6)
    parser.add_argument("--preview-every", type=int, default=0)
    parser.add_argument("--plan-only", action="store_true")
    return parser.parse_args()


def prompt(spec: Spec) -> str:
    if spec.source_type == "face":
        return (
            f"Head-and-shoulders portrait, {VIEW[spec.view]}, off-white studio background. Restrained webtoon watercolor. "
            f"{IDENTITY['lora_eye_identity_description']} {IDENTITY['lora_hair_identity_description']} Natural facial anatomy."
        )
    return (
        f"Full-body woman, {VIEW[spec.view]}, isolated on a plain off-white background. Restrained webtoon watercolor. "
        f"{IDENTITY['lora_eye_identity_description']} {IDENTITY['lora_hair_identity_description']} "
        f"{IDENTITY['lora_fullbody_proportion_description']} {spec.outfit}. Natural anatomy."
    )


def records(targets: tuple[str, ...], seed: int, steps: int) -> list[dict[str, object]]:
    selected = [spec for spec in SPECS if spec.candidate_id in targets]
    result: list[dict[str, object]] = []
    for spec in selected:
        if not spec.source.is_file() or not STYLE_REFERENCE.is_file():
            raise FileNotFoundError(f"missing source or style reference for {spec.candidate_id}")
        result.append({**asdict(spec), "source": spec.source.name, "style_reference": STYLE_REFERENCE.name, "seed": seed, "steps": steps, "prompt": prompt(spec)})
    return result


def main() -> int:
    args = parse_args()
    entries = records(tuple(args.targets), args.seed, args.steps)
    if args.plan_only:
        print(json.dumps({"status": "validated", "count": len(entries), "candidates": entries}, ensure_ascii=False, indent=2))
        return 0
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    pipe = Flux2KleinPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.bfloat16, cache_dir="/tmp/flux2-klein-diffusers-cache")
    pipe.enable_sequential_cpu_offload(); pipe.set_progress_bar_config(disable=True)
    for entry in entries:
        contract = {"model": MODEL_ID, **entry, "size": [1024, 1024]}
        stem = candidate_stem("p7-5-4-styled-identity-" + str(entry["candidate_id"]), seed=args.seed, steps=args.steps, contract=contract)
        output, review = ROOT / f"{stem}-candidate.png", ROOT / f"{stem}-review.json"
        started = time.monotonic()
        references = [Image.open(ROOT / str(entry["source"])).convert("RGB"), Image.open(STYLE_REFERENCE).convert("RGB")]
        image = pipe(image=references, prompt=str(entry["prompt"]), width=1024, height=1024, num_inference_steps=args.steps, guidance_scale=1.0, generator=torch.Generator(device="cpu").manual_seed(args.seed), max_sequence_length=256, callback_on_step_end=preview_callback(pipe, height=1024, width=1024, every=args.preview_every, directory=ROOT / "previews", prefix=stem)).images[0]
        image.save(output)
        payload = {"status": "review_required", "model": MODEL_ID, "image_size": [1024, 1024], **entry, "output": output.name, "review": review.name, "elapsed_seconds": round(time.monotonic() - started, 2), "decision": "Candidate only; require human approval before character-LoRA dataset inclusion."}
        review.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{entry['candidate_id']}: {payload['elapsed_seconds']}s -> {output.name}", flush=True)
        gc.collect(); torch.cuda.empty_cache()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

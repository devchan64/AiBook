#!/usr/bin/env python3
"""Compare Scene C BFS using native head crops from two 1280px torso references.

First run --prepare-reference to crop source pixels without generation or masks.
Then run the default command to apply BFS to the pre-style Scene C book result.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import hashlib
import importlib.metadata
import platform
import sys
from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent

PROJECT_ROOT = ASSETS.parents[3]

CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"

MODEL_ID = "Qwen/Qwen-Image-Edit-2511"

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def runtime_record() -> dict[str, object]:
    packages = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
    }

def square_canvas(path: Path, size: int) -> Image.Image:
    """Return an RGB, white-backed square canvas without distorting the input."""
    with Image.open(path) as source:
        source = source.convert("RGBA")
        source.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - source.width) // 2, (size - source.height) // 2)
        canvas.alpha_composite(source, offset)
    return canvas.convert("RGB")

SOURCES = {
    'a': 'section-05/p7-5-5-qwen-2511-cutout-identity-a-mira-audit-20260909-v1-size-1280x1280-seed-62294-steps-30.png',
    'b': 'section-05/p7-5-5-qwen-2511-mannequin-outfit-b-mira-stage3-v1-size-1280x1280-seed-62294-steps-20.png',
    'c': 'section-05/p7-5-5-qwen-2511-identity-c-mira-stage2-book-v1-size-1280x1280-seed-62294-steps-20.png',
}
DEFAULT_FACE = ASSETS / 'p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png'
REFERENCES = {
    'level': ('p7-5-2-qwen-2511-mira-torso-multiview-vertical-level-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png', (310, 20, 950, 660)),
    'elevated': ('p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png', (260, 40, 900, 680)),
}


def crop_paths(view: str) -> tuple[Path, Path]:
    stem = f'p7-5-5-bfs-c-{view}-native1280-head-crop-v1'
    return ASSETS / 'section-05' / f'{stem}.png', ASSETS / 'section-05' / f'{stem}-result.json'

LORA_FILE = 'bfs_head_v5_2511_original.safetensors'
LORA_PATH = ASSETS.parents[3] / '.tmp/download/weight-mr2along-bfs-head-v5-2511' / LORA_FILE
LORA_SHA256 = '5055ec271228d4767fd327efa59dbdea6f2a628d6d890101eb4fd5015cb1ac57'
PROMPT = (
    "head_swap: start with Picture 1 as the base image, keeping its lighting, "
    "environment, and background. remove the head from Picture 1 completely and "
    "replace it with the head from Picture 2, strictly preserving the hair, eye "
    "color, and nose structure of Picture 2. copy the eye direction, head rotation, "
    "and micro-expressions from Picture 1. high quality, sharp details, 4k"
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenes', nargs='+', choices=('c',), default=['c'])
    parser.add_argument('--prepare-reference', action='store_true')
    parser.add_argument('--views', nargs='+', choices=tuple(REFERENCES), default=list(REFERENCES))
    parser.add_argument('--prompt', default=PROMPT)
    parser.add_argument('--steps', type=int, default=10)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--run-label', default='v1')
    parser.add_argument('--output-dir', type=Path, default=ASSETS / "section-05")
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.steps < 1 or not args.prompt.strip():
        parser.error('Positive steps and a nonempty prompt are required.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label.')
    if args.prepare_reference:
        from PIL import Image
        for view in dict.fromkeys(args.views):
            source_name, crop_box = REFERENCES[view]
            source = ASSETS / source_name
            crop_path, crop_record = crop_paths(view)
            for path in (crop_path, crop_record):
                if path.exists():
                    raise FileExistsError(path)
            with Image.open(source) as original:
                if original.size != (1280, 1280):
                    raise ValueError(f'Expected native 1280px torso: {source}')
                cropped = original.crop(crop_box)
                cropped.save(crop_path)
            crop_record.write_text(json.dumps(dict(
                operation='pixel crop without resizing or AI generation',
                input=str(source), input_sha256=sha256(source),
                crop_box=list(crop_box), output=str(crop_path), size=list(cropped.size),
                output_sha256=sha256(crop_path), source_code_sha256=sha256(Path(__file__)),
            ), indent=2) + '\n')
            print(crop_path)
        return
    if not LORA_PATH.is_file() or sha256(LORA_PATH) != LORA_SHA256:
        raise ValueError(f'Missing or mismatched BFS weights: {LORA_PATH}')
    plans = []
    for experiment in dict.fromkeys(args.views):
        for scene in dict.fromkeys(args.scenes):
            source = ASSETS / SOURCES[scene]
            reference, crop_record = crop_paths(experiment)
            weight = 1.0
            for path in (source, reference):
                if not path.is_file():
                    raise FileNotFoundError(path)
            variant = f'{experiment}-native1280-headcrop-weight10'
            stem = (f'p7-5-5-qwen-2511-bfs-reviewed-{scene}-mira-{variant}-{args.run_label}'
                    f'-size-1280x1280-seed-{args.seed}-steps-{args.steps}')
            output = args.output_dir.resolve() / f'{stem}.png'
            result = output.with_name(f'{stem}-result.json')
            for path in (output, result):
                if path.exists():
                    raise FileExistsError(f'Refusing to overwrite: {path}')
            plans.append(dict(scene=scene, experiment=experiment, crop_provenance=json.loads(crop_record.read_text()), lora_weight=weight, inputs=[
                dict(role='Picture 1: reviewed pre-BFS identity result', path=str(source), sha256=sha256(source)),
                dict(role='Picture 2: native head crop from 1280px torso reference',
                     path=str(reference), sha256=sha256(reference)),
            ], output=str(output), result=str(result)))
    settings = dict(model=MODEL_ID, prompt=args.prompt.strip(), steps=args.steps, seed=args.seed,
                    size=[1280, 1280], true_cfg_scale=4.0, guidance_scale=1.0,
                    generator_device='cpu', dtype='bfloat16', mask=None, lora=dict(repository='mr2along/BFS',
                    revision='d9ffba9012dfa1b299a4294572791c3275ae6ae4',
                    file=LORA_FILE, sha256=LORA_SHA256))
    if args.dry_run:
        print(json.dumps(dict(status='planned', settings=settings, plans=plans), indent=2))
        return
    import torch
    from diffusers import QwenImageEditPlusPipeline

    if not torch.cuda.is_available():
        raise RuntimeError('A local CUDA GPU is required.')
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR, local_files_only=True,
    )
    pipeline.load_lora_weights(LORA_PATH.parent, weight_name=LORA_FILE,
                               adapter_name='bfs_head_v5', local_files_only=True)
    pipeline.enable_attention_slicing('max')
    pipeline.enable_sequential_cpu_offload()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    provenance = dict(source_code_sha256=sha256(Path(__file__)),

                      runtime=runtime_record(), cuda_device=torch.cuda.get_device_name(0),
                      offload='sequential CPU offload',
                      preprocessing='aspect-preserving resize on white 1280x1280 canvases')
    for plan in plans:
        for item in plan['inputs']:
            if sha256(Path(item['path'])) != item['sha256']:
                raise ValueError(f"Input changed after preflight: {item['path']}")
        pipeline.set_adapters('bfs_head_v5', adapter_weights=plan['lora_weight'])
        print(f"Starting experiment {plan['experiment']} scene {plan['scene']}", flush=True)
        started = time.monotonic()
        image = pipeline(
            image=[square_canvas(Path(item['path']), 1280) for item in plan['inputs']],
            prompt=settings['prompt'], height=1280, width=1280,
            generator=torch.Generator(device='cpu').manual_seed(args.seed),
            true_cfg_scale=4.0, negative_prompt=' ', num_inference_steps=args.steps,
            guidance_scale=1.0, num_images_per_prompt=1,
        ).images[0]
        with Path(plan['output']).open('xb') as stream:
            image.save(stream, format='PNG')
        record = dict(plan, **settings, **provenance, status='generated', stage='bfs_head_crop_reference_comparison',
                      output_sha256=sha256(Path(plan['output'])),
                      elapsed_seconds=round(time.monotonic()-started, 2))
        with Path(plan['result']).open('x', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print(json.dumps({'scene': plan['scene'], 'output': plan['output'], 'result': plan['result']}), flush=True)


if __name__ == '__main__':
    main()

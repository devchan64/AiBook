#!/usr/bin/env python3
"""Generate a standalone shoe-pair reference from the P7-5.3 outfit on local CUDA.

This is generative extraction, not segmentation or a pixel-preserving crop.
Use --dry-run to inspect the input, prompt and output paths without loading Qwen.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import re
import time
from pathlib import Path

ASSETS = Path(__file__).resolve().parent
CACHE = ASSETS.parents[3] / '.tmp/download/huggingface/hub'
MODEL_ID = 'Qwen/Qwen-Image-Edit-2511'
SOURCE = ASSETS / (
    'p7-5-3-qwen-edit-prompt-style-outfit_stage3_jacket_face-three-stage-v1-seed-62294-steps-10.png'
)
PROMPT = (
    'Extract the pair of shoes worn by the woman in Picture 1. '
    'Show only the two shoes, fully visible and side by side on a plain white background. '
    'Preserve their design, colors, laces, soles, and illustration style. '
    'Remove the person and all other clothing.'
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=SOURCE)
    parser.add_argument('--steps', type=int, default=30)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--size', type=int, default=1280)
    parser.add_argument('--run-label', default='v1')
    parser.add_argument('--output-dir', type=Path, default=ASSETS)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.steps < 1 or args.size < 32 or args.size % 32:
        parser.error('Use positive steps and a size divisible by 32 (at least 32).')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label.')
    source = args.input.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    stem = (f'p7-5-3-qwen-2511-extract-shoes-{args.run_label}-'
            f'size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}')
    target = args.output_dir.resolve() / (stem + '.png')
    result = target.with_name(stem + '-result.json')
    for path in (target, result):
        if path.exists():
            raise FileExistsError(path)
    from PIL import Image
    with Image.open(source) as image:
        rgba = image.convert('RGBA')
    image = Image.alpha_composite(Image.new('RGBA', rgba.size, 'white'), rgba).convert('RGB')
    record = dict(
        status='planned', stage='outfit_shoe_extraction', model=MODEL_ID,
        model_card='https://huggingface.co/' + MODEL_ID,
        prompt=PROMPT, inputs=[dict(path=str(source), sha256=sha256(source))],
        input_preprocessing=dict(mode='native aspect ratio; RGB; alpha on white', size=list(image.size)),
        settings=dict(steps=args.steps, seed=args.seed, size=args.size, true_cfg_scale=4.0,
                      guidance_scale=1.0, negative_prompt=' ', mask=False, lora=None,
                      output_compositing=False, generator_device='cuda'),
        output=dict(path=str(target)), result_path=str(result),
        script=dict(path=str(Path(__file__).resolve()), sha256=sha256(Path(__file__))),
    )
    if args.dry_run:
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return
    import torch
    from diffusers import QwenImageEditPlusPipeline
    if not torch.cuda.is_available():
        raise RuntimeError('Local CUDA GPU is required.')
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE, local_files_only=True)
    pipeline.enable_attention_slicing('max')
    pipeline.enable_sequential_cpu_offload()
    started = time.monotonic()
    generated = pipeline(
        image=[image], prompt=PROMPT, negative_prompt=' ',
        width=args.size, height=args.size, num_inference_steps=args.steps,
        true_cfg_scale=4.0, guidance_scale=1.0,
        generator=torch.Generator('cuda').manual_seed(args.seed),
    ).images[0]
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream:
        generated.save(stream, format='PNG')
    record.update(status='generated', elapsed_seconds=round(time.monotonic()-started, 2),
                  cuda_device=torch.cuda.get_device_name(0), dtype='bfloat16',
                  device_placement='sequential_cpu_offload',
                  packages={name: importlib.metadata.version(name)
                            for name in ('diffusers', 'transformers', 'torch', 'accelerate')})
    record['output'].update(sha256=sha256(target), width=generated.width, height=generated.height)
    with result.open('x') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(record, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()

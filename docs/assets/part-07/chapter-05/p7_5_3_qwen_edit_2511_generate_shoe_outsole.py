#!/usr/bin/env python3
"""Generate a sneaker outsole reference from the P7-5.3 shoe image.

Local Qwen Edit 2511; single image, no mask or LoRA. The unseen tread is
generated, not recovered from the source. Inspect before using downstream.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "section-05"))

from p7_5_5_qwen_edit_common import (
    ASSETS, CACHE_DIR, MODEL_ID, runtime_record, sha256, square_canvas,
)

SOURCE = ASSETS / 'p7-5-3-qwen-image-2512-white-sneakers-v1-size-1280x1280-seed-62294-steps-10.png'
PROMPT = 'Show one sneaker from Picture 1 from directly underneath, with its entire outsole facing the camera, toe at the top and heel at the bottom. Keep the shoe design and illustration style on a white background.'
STAGE = 'white-sneaker-outsole'
PAIRED_PROMPT = 'Show the sneakers from Picture 1 side by side: the left shoe from directly above, showing its upper and laces; the right shoe from directly below, showing a light taupe rubber outsole with clearly defined triangular tread grooves. Light both shoes evenly so the outsole pattern is clearly visible. Point both toes upward. Keep the white shoe design and illustration style on a white background.'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=SOURCE)
    parser.add_argument('--prompt', help='Override the selected experiment prompt.')
    parser.add_argument('--steps', type=int, default=20)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--run-label', default='v1')
    parser.add_argument('--output-dir', type=Path, default=ASSETS)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--paired-views', action='store_true', help='Show one upper view and one outsole view together.')
    args = parser.parse_args()
    if args.steps < 1 or (args.prompt is not None and not args.prompt.strip()):
        parser.error('Positive steps and a nonempty prompt are required.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label.')
    prompt = args.prompt or (PAIRED_PROMPT if args.paired_views else PROMPT)
    image_paths = [(args.input, 'Picture 1: P7-5.3 white sneaker design')]
    inputs = []
    for path, role in image_paths:
        path = path.resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        inputs.append(dict(path=str(path), role=role, sha256=sha256(path)))
    stem = (f'p7-5-3-qwen-2511-{STAGE}-{args.run_label}'
            f'-size-1280x1280-seed-{args.seed}-steps-{args.steps}')
    output = args.output_dir.resolve() / f'{stem}.png'
    result = output.with_name(f'{stem}-result.json')
    for path in (output, result):
        if path.exists():
            raise FileExistsError(f'Refusing to overwrite: {path}')
    plan = dict(stage=STAGE, model=MODEL_ID, inputs=inputs, prompt=prompt.strip(),
                output=str(output), result=str(result), steps=args.steps, seed=args.seed,
                size=[1280, 1280], true_cfg_scale=4.0, guidance_scale=1.0,
                generator_device='cpu', dtype='bfloat16', mask=None, lora=None,
                experiment='shoe-upper-and-bottom-views' if args.paired_views else 'shoe-bottom-view')
    if args.dry_run:
        print(json.dumps(dict(plan, status='planned'), indent=2))
        return
    import torch
    from diffusers import QwenImageEditPlusPipeline

    if not torch.cuda.is_available():
        raise RuntimeError('A local CUDA GPU is required.')
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR, local_files_only=True,
    )
    pipeline.enable_attention_slicing('max')
    pipeline.enable_sequential_cpu_offload()
    for item in inputs:
        if sha256(Path(item['path'])) != item['sha256']:
            raise ValueError(f"Input changed after preflight: {item['path']}")
    started = time.monotonic()
    image = pipeline(
        image=[square_canvas(Path(item['path']), 1280) for item in inputs],
        prompt=plan['prompt'], height=1280, width=1280,
        generator=torch.Generator(device='cpu').manual_seed(args.seed),
        true_cfg_scale=4.0, negative_prompt=' ', num_inference_steps=args.steps,
        guidance_scale=1.0, num_images_per_prompt=1,
    ).images[0]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('xb') as stream:
        image.save(stream, format='PNG')
    record = dict(plan, status='generated', output_sha256=sha256(output),
                  source_code_sha256=sha256(Path(__file__)),
                  helper_code_sha256=sha256(ASSETS / 'section-05/p7_5_5_qwen_edit_common.py'),
                  runtime=runtime_record(), cuda_device=torch.cuda.get_device_name(0),
                  offload='sequential CPU offload',
                  preprocessing='aspect-preserving resize on white 1280x1280 canvases',
                  elapsed_seconds=round(time.monotonic()-started, 2))
    with result.open('x', encoding='utf-8') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(dict(output=str(output), result=str(result))), flush=True)


if __name__ == '__main__':
    main()

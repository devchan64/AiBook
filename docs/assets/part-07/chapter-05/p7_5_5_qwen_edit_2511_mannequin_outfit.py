#!/usr/bin/env python3
"""First outfit pass: reviewed A/B/C mannequins + P7-5.3 stage-three outfit.

Inspect the generated clothes, shoes and pose before designing any refinement.
The mannequin is Picture 1; the outfit reference is Picture 2. No masks or LoRA.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

from p7_5_5_qwen_edit_2511_pose_identity import (
    ASSETS, CACHE_DIR, DEFAULT_CHARACTER, MODEL_ID, runtime_record, sha256, square_canvas,
)

SOURCES = {
    'a': 'p7-5-5-qwen-2511-cutout-mannequin-a-mira-compressed-v2-size-1280x1280-seed-62294-steps-20.png',
    'b': 'p7-5-5-qwen-2511-cutout-mannequin-b-mira-cutout-v1-size-1280x1280-seed-62294-steps-20.png',
    'c': 'p7-5-5-qwen-2511-cutout-mannequin-c-mira-cutout-v1-size-1280x1280-seed-62294-steps-20.png',
}
PROMPT = (
    'Dress the woman in Picture 1 in the complete outfit, including shoes, from Picture 2. '
    'Keep the face, hairstyle, pose, perspective, framing and white background of Picture 1.'
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenes', nargs='+', choices=tuple(SOURCES), default=list(SOURCES))
    parser.add_argument('--reference', type=Path, default=DEFAULT_CHARACTER)
    parser.add_argument('--prompt', default=PROMPT)
    parser.add_argument('--steps', type=int, default=20)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--run-label', default='stage3-v1')
    parser.add_argument('--output-dir', type=Path, default=ASSETS)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.steps < 1 or not args.prompt.strip():
        parser.error('Positive steps and a nonempty prompt are required.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label.')
    reference = args.reference.resolve()
    if not reference.is_file():
        raise FileNotFoundError(reference)
    plans = []
    for scene in dict.fromkeys(args.scenes):
        source = ASSETS / SOURCES[scene]
        if not source.is_file():
            raise FileNotFoundError(source)
        stem = (f'p7-5-5-qwen-2511-mannequin-outfit-{scene}-mira-{args.run_label}'
                f'-size-1280x1280-seed-{args.seed}-steps-{args.steps}')
        output = args.output_dir.resolve() / f'{stem}.png'
        result = output.with_name(f'{stem}-result.json')
        for path in (output, result):
            if path.exists():
                raise FileExistsError(f'Refusing to overwrite: {path}')
        plans.append(dict(scene=scene, inputs=[
            dict(role='Picture 1: reviewed pose mannequin', path=str(source), sha256=sha256(source)),
            dict(role='Picture 2: complete stage-three outfit including shoes', path=str(reference), sha256=sha256(reference)),
        ], output=str(output), result=str(result)))
    settings = dict(model=MODEL_ID, prompt=args.prompt.strip(), steps=args.steps, seed=args.seed,
                    size=[1280, 1280], true_cfg_scale=4.0, guidance_scale=1.0,
                    generator_device='cpu', dtype='bfloat16', mask=None, lora=None)
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
    pipeline.enable_attention_slicing('max')
    pipeline.enable_sequential_cpu_offload()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    provenance = dict(source_code_sha256=sha256(Path(__file__)),
                      helper_code_sha256=sha256(ASSETS / 'p7_5_5_qwen_edit_2511_pose_identity.py'),
                      runtime=runtime_record(), cuda_device=torch.cuda.get_device_name(0),
                      offload='sequential CPU offload',
                      preprocessing='aspect-preserving resize on white 1280x1280 canvases')
    for plan in plans:
        for item in plan['inputs']:
            if sha256(Path(item['path'])) != item['sha256']:
                raise ValueError(f"Input changed after preflight: {item['path']}")
        print(f"Starting scene {plan['scene']}", flush=True)
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
        record = dict(plan, **settings, **provenance, status='generated', stage='mannequin_outfit_first_pass',
                      output_sha256=sha256(Path(plan['output'])),
                      elapsed_seconds=round(time.monotonic()-started, 2))
        with Path(plan['result']).open('x', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print(json.dumps({'scene': plan['scene'], 'output': plan['output'], 'result': plan['result']}), flush=True)


if __name__ == '__main__':
    main()

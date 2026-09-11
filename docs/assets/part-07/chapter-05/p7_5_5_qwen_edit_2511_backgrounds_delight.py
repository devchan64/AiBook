#!/usr/bin/env python3
"""Apply Studio DeLight to the adopted A/B v1 and C v2 background plates.

Model card: https://huggingface.co/prithivMLmods/QIE-2511-Studio-DeLight
One input per background plate; no Lightning or BFS adapter in this pass.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

from p7_5_5_qwen_edit_2511_pose_identity import (
    ASSETS, CACHE_DIR, MODEL_ID, runtime_record, sha256, square_canvas,
)

SOURCES = {
    'a': ASSETS / 'p7-5-5-qwen-2511-background-scene-a-v1-size-1280x1280-seed-62294-steps-10.png',
    'b': ASSETS / 'p7-5-5-qwen-2511-background-scene-b-v1-size-1280x1280-seed-62294-steps-10.png',
    'c': ASSETS / 'p7-5-5-qwen-2511-background-scene-c-v2-size-1280x1280-seed-62294-steps-10.png',
}

PROMPT = 'Neutral uniform lighting Preserve identity and composition'
LORA = ASSETS.parents[3] / '.tmp/download/weight-prithivmlmods-qie-2511-studio-delight/QIE-2511-Studio-DeLight-5000.safetensors'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--targets', nargs='+', choices=tuple(SOURCES), default=list(SOURCES))
    parser.add_argument('--delight-scale', type=float, default=1.0)
    parser.add_argument('--prompt', default=PROMPT)
    parser.add_argument('--steps', type=int, default=10)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--run-label', default='v1')
    parser.add_argument('--output-dir', type=Path, default=ASSETS)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.steps < 1 or not args.prompt.strip():
        parser.error('Positive steps and a nonempty prompt are required.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label.')
    if args.delight_scale <= 0:
        parser.error('DeLight scale must be positive.')
    plans = []
    for target in dict.fromkeys(args.targets):
        source = SOURCES[target].resolve()
        if not source.is_file():
            raise FileNotFoundError(source)
        stem = (f'p7-5-5-qwen-2511-studio-delight-background-{target}-{args.run_label}'
                f'-size-1280x1280-seed-{args.seed}-steps-{args.steps}')
        output = args.output_dir.resolve() / f'{stem}.png'
        result = output.with_name(f'{stem}-result.json')
        for path in (output, result):
            if path.exists():
                raise FileExistsError(f'Refusing to overwrite: {path}')
        plans.append(dict(scene=target, inputs=[dict(role='Picture 1: adopted background plate',
                          path=str(source), sha256=sha256(source))],
                          output=str(output), result=str(result)))
    settings = dict(model=MODEL_ID, prompt=args.prompt.strip(), steps=args.steps, seed=args.seed,
                    size=[1280, 1280], true_cfg_scale=4.0, guidance_scale=1.0,
                    generator_device='cpu', dtype='bfloat16', mask=None, negative_prompt=' ', lora=dict(repository='prithivMLmods/QIE-2511-Studio-DeLight',
                    path=str(LORA), sha256=sha256(LORA), scale=args.delight_scale))
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
    pipeline.load_lora_weights(LORA.parent, weight_name=LORA.name, adapter_name='studio_delight', local_files_only=True)
    pipeline.set_adapters(['studio_delight'], adapter_weights=[args.delight_scale])
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
        record = dict(plan, **settings, **provenance, status='generated', stage='studio_delight_background_plate',
                      output_sha256=sha256(Path(plan['output'])),
                      elapsed_seconds=round(time.monotonic()-started, 2))
        with Path(plan['result']).open('x', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print(json.dumps({'scene': plan['scene'], 'output': plan['output'], 'result': plan['result']}), flush=True)


if __name__ == '__main__':
    main()

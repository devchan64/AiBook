#!/usr/bin/env python3
"""Compare BFS strength 0.7 and angle-reference replacement independently.

Experiment 2: frontal reference, weight 0.7.
Experiment 3: scene-specific angled reference, weight 1.0.
Both start from reviewed pre-BFS A/C sources and keep baseline prompt/seed/steps.
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
    'a': 'p7-5-5-qwen-2511-cutout-identity-a-mira-audit-20260909-v1-size-1280x1280-seed-62294-steps-30.png',
    'b': 'p7-5-5-qwen-2511-mannequin-outfit-b-mira-stage3-v1-size-1280x1280-seed-62294-steps-20.png',
    'c': 'p7-5-5-qwen-2511-identity-c-mira-stage2-book-v1-size-1280x1280-seed-62294-steps-20.png',
}
DEFAULT_FACE = ASSETS / 'p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-seed-62294-steps-30-size-1280.png'
ANGLE_FACES = {
    'a': ASSETS / 'p7-5-2-qwen-2511-mira-torso-multiview-vertical-low-yaw-zero-native1280-v1-size-1280x1280-seed-62294-steps-4.png',
    'c': ASSETS / 'p7-5-2-qwen-2511-mira-torso-multiview-vertical-elevated-yaw-minus-45-native1280-v1-size-1280x1280-seed-62294-steps-4.png',
}
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
    parser.add_argument('--scenes', nargs='+', choices=('a', 'c'), default=['a', 'c'])
    parser.add_argument('--experiments', nargs='+', choices=['2', '3'], default=['2', '3'])
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
    if not LORA_PATH.is_file() or sha256(LORA_PATH) != LORA_SHA256:
        raise ValueError(f'Missing or mismatched BFS weights: {LORA_PATH}')
    plans = []
    for experiment in dict.fromkeys(args.experiments):
        for scene in dict.fromkeys(args.scenes):
            source = ASSETS / SOURCES[scene]
            reference = DEFAULT_FACE if experiment == '2' else ANGLE_FACES[scene]
            weight = 0.7 if experiment == '2' else 1.0
            for path in (source, reference):
                if not path.is_file():
                    raise FileNotFoundError(path)
            variant = 'exp2-front-weight07' if experiment == '2' else 'exp3-angle-weight10'
            stem = (f'p7-5-5-qwen-2511-bfs-reviewed-{scene}-mira-{variant}-{args.run_label}'
                    f'-size-1280x1280-seed-{args.seed}-steps-{args.steps}')
            output = args.output_dir.resolve() / f'{stem}.png'
            result = output.with_name(f'{stem}-result.json')
            for path in (output, result):
                if path.exists():
                    raise FileExistsError(f'Refusing to overwrite: {path}')
            plans.append(dict(scene=scene, experiment=experiment, lora_weight=weight, inputs=[
                dict(role='Picture 1: reviewed pre-BFS identity result', path=str(source), sha256=sha256(source)),
                dict(role='Picture 2: frontal head' if experiment == '2' else 'Picture 2: angled torso reference',
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
                      helper_code_sha256=sha256(ASSETS / 'p7_5_5_qwen_edit_2511_pose_identity.py'),
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
        record = dict(plan, **settings, **provenance, status='generated', stage='bfs_direction_experiment',
                      output_sha256=sha256(Path(plan['output'])),
                      elapsed_seconds=round(time.monotonic()-started, 2))
        with Path(plan['result']).open('x', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print(json.dumps({'scene': plan['scene'], 'output': plan['output'], 'result': plan['result']}), flush=True)


if __name__ == '__main__':
    main()

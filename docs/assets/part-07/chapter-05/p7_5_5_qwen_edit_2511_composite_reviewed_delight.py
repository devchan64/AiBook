#!/usr/bin/env python3
"""Combine adopted DeLight backgrounds and characters with local Qwen Edit 2511.

Picture 1: background, Picture 2: Mira, Picture 3 (C only): supporting reader.
Use scene-specific placement instructions without masks, LoRA or pixel compositing.
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
    scene: [
        ASSETS / f'p7-5-5-qwen-2511-studio-delight-background-{scene}-v1-size-1280x1280-seed-62294-steps-10.png',
        ASSETS / f'p7-5-5-qwen-2511-studio-delight-reviewed-{scene}-mira-v1-size-1280x1280-seed-62294-steps-10.png',
    ] for scene in ('a', 'b', 'c')
}
SOURCES['c'].append(ASSETS / 'p7-5-5-qwen-2511-studio-delight-reviewed-c-supporting-v1-size-1280x1280-seed-62294-steps-10.png')
ROLES = ['Picture 1: DeLight background', 'Picture 2: DeLight Mira', 'Picture 3: DeLight supporting reader']
PROMPTS = {
    'a': 'Place the woman from Picture 2 in the center foreground of Picture 1, running toward the viewer. Preserve her pose, face, hair, outfit and large foreground shoe. Keep the six surrounding people and the background.',
    'b': 'Place the woman from Picture 2 in midair at the center of Picture 1. Preserve her split-leap pose, face, hair and outfit. Keep the rabbit, squirrel and forest background.',
    'c': 'Place the woman from Picture 2 seated on the left foreground rock in Picture 1, and the man from Picture 3 seated just behind her on the right. Preserve both characters, their poses, outfits and open books. Keep the three birds, railing and city background.',
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--targets', nargs='+', choices=tuple(SOURCES), default=list(SOURCES))
    parser.add_argument('--prompt', help='Optional prompt override for a single target.')
    parser.add_argument('--steps', type=int, default=10)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--run-label', default='v1')
    parser.add_argument('--output-dir', type=Path, default=ASSETS)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.steps < 1 or (args.prompt is not None and not args.prompt.strip()):
        parser.error('Positive steps and a nonempty prompt are required.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label.')
    if args.prompt is not None and len(set(args.targets)) != 1:
        parser.error('--prompt requires a single target.')
    plans = []
    for target in dict.fromkeys(args.targets):
        sources = [source.resolve() for source in SOURCES[target]]
        for source in sources:
            if not source.is_file():
                raise FileNotFoundError(source)
        stem = (f'p7-5-5-qwen-2511-delight-composite-scene-{target}-{args.run_label}'
                f'-size-1280x1280-seed-{args.seed}-steps-{args.steps}')
        output = args.output_dir.resolve() / f'{stem}.png'
        result = output.with_name(f'{stem}-result.json')
        for path in (output, result):
            if path.exists():
                raise FileExistsError(f'Refusing to overwrite: {path}')
        plans.append(dict(scene=target, prompt=args.prompt or PROMPTS[target], inputs=[dict(role=ROLES[index], path=str(source), sha256=sha256(source))
                          for index, source in enumerate(sources)],
                          output=str(output), result=str(result)))
    settings = dict(model=MODEL_ID, steps=args.steps, seed=args.seed,
                    size=[1280, 1280], true_cfg_scale=4.0, guidance_scale=1.0,
                    generator_device='cpu', dtype='bfloat16', mask=None, negative_prompt=' ', lora=None)
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
            prompt=plan['prompt'], height=1280, width=1280,
            generator=torch.Generator(device='cpu').manual_seed(args.seed),
            true_cfg_scale=4.0, negative_prompt=' ', num_inference_steps=args.steps,
            guidance_scale=1.0, num_images_per_prompt=1,
        ).images[0]
        with Path(plan['output']).open('xb') as stream:
            image.save(stream, format='PNG')
        record = dict(plan, **settings, **provenance, status='generated', stage='delight_background_character_composite',
                      output_sha256=sha256(Path(plan['output'])),
                      elapsed_seconds=round(time.monotonic()-started, 2))
        with Path(plan['result']).open('x', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print(json.dumps({'scene': plan['scene'], 'output': plan['output'], 'result': plan['result']}), flush=True)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Apply a character reference to the reviewed cutouts on the local GPU.

Picture 1 fixes pose and framing. Picture 2 supplies identity and outfit for
Mira, or rendering style only when --supporting-style is explicitly selected.
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
    'a-mira': 'section-05/p7-5-5-character-cutout-scene-a-mira-audit-20260909-v1.png',
    'b-mira': 'section-05/p7-5-5-character-cutout-scene-b-mira-audit-20260909-v1.png',
    'c-mira': 'section-05/p7-5-5-character-cutout-scene-c-mira-audit-20260909-v6.png',
    'c-supporting': 'section-05/p7-5-5-character-cutout-scene-c-supporting-audit-20260909-v2.png',
}
MIRA_PROMPT = (
    'Replace the woman in Picture 1 with the woman in Picture 2, preserving the pose. '
    'Preserve the framing and white background of Picture 1.'
)
STYLE_PROMPT = (
    'Redraw the man in Picture 1 using the rendering style of Picture 2. '
    'Use Picture 2 only as a rendering-style reference. Preserve the identity, '
    'face, hairstyle, clothing, pose, framing and white background of Picture 1.'
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--targets', nargs='+', choices=tuple(SOURCES), default=list(SOURCES)[:3])
    parser.add_argument('--reference', type=Path, default=DEFAULT_CHARACTER)
    parser.add_argument('--supporting-reference', type=Path)
    parser.add_argument('--supporting-style', action='store_true')
    parser.add_argument('--supporting-prompt', help='Text-only identity for C supporting; no second image.')
    parser.add_argument('--steps', type=int, default=30)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--run-label', default='audit-20260909-v1')
    parser.add_argument('--output-dir', type=Path, default=ASSETS / "section-05")
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.steps < 1 or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Positive steps and a filename-safe run label are required.')
    if 'c-supporting' in args.targets and not (args.supporting_reference or args.supporting_style or args.supporting_prompt):
        parser.error('C supporting requires a reference, style mode, or text prompt.')
    plans = []
    for target in dict.fromkeys(args.targets):
        source = ASSETS / SOURCES[target]
        supporting = target == 'c-supporting'
        reference = (args.supporting_reference if supporting and args.supporting_reference else args.reference).resolve()
        prompt = STYLE_PROMPT if supporting and args.supporting_style else MIRA_PROMPT
        if supporting and not args.supporting_style:
            prompt = MIRA_PROMPT.replace('woman', 'man')
        if supporting and args.supporting_prompt:
            prompt = args.supporting_prompt
        for path in (source, reference):
            if not path.is_file():
                raise FileNotFoundError(path)
        stem = f'p7-5-5-qwen-2511-cutout-identity-{target}-{args.run_label}-size-1280x1280-seed-{args.seed}-steps-{args.steps}'
        output = args.output_dir.resolve() / f'{stem}.png'
        result = output.with_name(f'{stem}-result.json')
        for path in (output, result):
            if path.exists():
                raise FileExistsError(path)
        plans.append(dict(target=target, source=str(source), reference=str(reference),
                          source_sha256=sha256(source), reference_sha256=sha256(reference),
                          prompt=prompt, output=str(output), result=str(result),
                          text_only=bool(supporting and args.supporting_prompt),
                          reference_role='none: text-only identity' if supporting and args.supporting_prompt else ('rendering style only' if supporting and args.supporting_style else 'identity and outfit')))
    for plan in plans:
        if plan['text_only']:
            plan['reference'] = None
            plan['reference_sha256'] = None
    if args.dry_run:
        print(json.dumps(plans, indent=2))
        return
    import torch
    from diffusers import QwenImageEditPlusPipeline

    if not torch.cuda.is_available():
        raise RuntimeError('A local CUDA GPU is required.')
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR, local_files_only=True,
    )
    pipe.enable_attention_slicing('max')
    pipe.enable_sequential_cpu_offload()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for plan in plans:
        print(f"Starting {plan['target']}", flush=True)
        started = time.monotonic()
        image = pipe(
            image=([square_canvas(Path(plan['source']), 1280)] if plan['text_only'] else
                   [square_canvas(Path(plan['source']), 1280), square_canvas(Path(plan['reference']), 1280)]),
            prompt=plan['prompt'], height=1280, width=1280,
            generator=torch.Generator(device='cpu').manual_seed(args.seed),
            true_cfg_scale=4.0, negative_prompt=' ', num_inference_steps=args.steps,
            guidance_scale=1.0, num_images_per_prompt=1,
        ).images[0]
        image.save(plan['output'])
        record = dict(plan, status='generated', model=MODEL_ID, runtime=runtime_record(),
                      source_code_sha256=sha256(Path(__file__)),
                      helper_code_sha256=sha256(ASSETS / 'section-05/p7_5_5_qwen_edit_2511_pose_identity.py'),
                      device=torch.cuda.get_device_name(0), dtype='bfloat16',
                      offload='sequential CPU offload', seed=args.seed, generator_device='cpu',
                      steps=args.steps, true_cfg_scale=4.0, guidance_scale=1.0,
                      size=[image.width, image.height], mask=None, lora=None,
                      output_sha256=sha256(Path(plan['output'])), elapsed_seconds=round(time.monotonic()-started, 2))
        Path(plan['result']).write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
        print(json.dumps({'target': plan['target'], 'output': plan['output'], 'result': plan['result']}), flush=True)


if __name__ == '__main__':
    main()

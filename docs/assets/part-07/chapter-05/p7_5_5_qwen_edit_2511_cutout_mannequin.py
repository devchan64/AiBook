#!/usr/bin/env python3
"""Generate pose mannequins from the reviewed B and C Mira cutouts.

A single cutout is the only image input. Replace its recognizable appearance
with a generic adult pose person before a separately reviewed identity pass.
This is local Qwen editing, not segmentation or pixel-preserving extraction.
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

from PIL import Image

from p7_5_5_qwen_edit_2511_pose_identity import (
    ASSETS, CACHE_DIR, MODEL_ID, runtime_record, sha256,
)

RECIPE = ASSETS / 'p7-5-5-character-separation-recipe-v1.json'
BASE_PROMPT = (
    'Replace the woman in Picture 1 with a generic adult female pose mannequin '
    'depicted as an illustrated person with a visible face, ordinary facial '
    'features, a very short buzz cut, a plain gray sports bra and plain gray '
    'briefs, and bare feet. Replace the original face, hairstyle, outfit and '
    'shoes with this neutral appearance. Preserve the original expression, '
    'head orientation, body proportions, joint positions, hand gestures, '
    'foot positions, perspective, body placement, framing and white background.'
)
POSE_PROMPTS = {
    'b': 'Preserve the airborne split-leap pose, the extended legs and the raised and outstretched arms.',
    'c': 'Preserve the seated pose, bent knees, lowered head and hands held in front of the body.',
}


def load_cutout(path: Path) -> Image.Image:
    """Keep the reviewed 1280px canvas and subject placement unchanged on input."""
    with Image.open(path) as image:
        if image.size != (1280, 1280):
            raise ValueError(f'Expected a 1280x1280 cutout: {path}')
        return image.convert('RGB')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scenes', nargs='+', choices=tuple(POSE_PROMPTS), default=list(POSE_PROMPTS))
    parser.add_argument('--steps', type=int, default=20)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--prompt', help='Override the appearance instruction for selected scenes.')
    parser.add_argument('--run-label', default='cutout-v1')
    parser.add_argument('--output-dir', type=Path, default=ASSETS)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if args.steps < 1 or (args.prompt is not None and not args.prompt.strip()):
        parser.error('Positive steps and a nonempty prompt are required.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label.')
    recipe = json.loads(RECIPE.read_text(encoding='utf-8'))
    targets = {row['target']: row for row in recipe['targets']}
    output_dir = args.output_dir.resolve()
    plans = []
    for scene in dict.fromkeys(args.scenes):
        # Select the segmentation output, not the later identity-edit result.
        source = ASSETS / targets[f'{scene}-mira']['baseline']['white']
        load_cutout(source)
        stem = (f'p7-5-5-qwen-2511-cutout-mannequin-{scene}-mira-{args.run_label}'
                f'-size-1280x1280-seed-{args.seed}-steps-{args.steps}')
        output = output_dir / f'{stem}.png'
        result = output_dir / f'{stem}-result.json'
        for path in (output, result):
            if path.exists():
                raise FileExistsError(f'Refusing to overwrite: {path}')
        base_prompt = args.prompt if args.prompt is not None else BASE_PROMPT
        plans.append(dict(scene=scene, inputs=[dict(role='Picture 1: original segmented Mira cutout',
                                                  path=str(source), sha256=sha256(source))],
                          prompt=f'{base_prompt.strip()} {POSE_PROMPTS[scene]}',
                          output=str(output), result=str(result)))
    settings = dict(model=MODEL_ID, steps=args.steps, seed=args.seed, size=[1280, 1280],
                    true_cfg_scale=4.0, guidance_scale=1.0, generator_device='cpu',
                    dtype='bfloat16', mask=None, lora=None, identity_reference=None)
    if args.dry_run:
        print(json.dumps(dict(status='planned', settings=settings, plans=plans), indent=2))
        return

    import torch
    from diffusers import QwenImageEditPlusPipeline

    if not torch.cuda.is_available():
        raise RuntimeError('A local CUDA GPU is required.')
    # One model load for all selected scenes; no downloads or identity reference.
    pipe = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR, local_files_only=True,
    )
    pipe.enable_attention_slicing('max')
    pipe.enable_sequential_cpu_offload()
    output_dir.mkdir(parents=True, exist_ok=True)
    provenance = dict(source_code_sha256=sha256(Path(__file__)), recipe_sha256=sha256(RECIPE),
                      helper_code_sha256=sha256(ASSETS / 'p7_5_5_qwen_edit_2511_pose_identity.py'),
                      runtime=runtime_record(), cuda_device=torch.cuda.get_device_name(0),
                      offload='sequential CPU offload')
    for plan in plans:
        source = Path(plan['inputs'][0]['path'])
        if sha256(source) != plan['inputs'][0]['sha256']:
            raise ValueError(f'Input changed after preflight: {source}')
        print(f"Starting scene {plan['scene']}", flush=True)
        started = time.monotonic()
        image = pipe(
            image=[load_cutout(source)], prompt=plan['prompt'], height=1280, width=1280,
            generator=torch.Generator(device='cpu').manual_seed(args.seed),
            true_cfg_scale=4.0, negative_prompt=' ', num_inference_steps=args.steps,
            guidance_scale=1.0, num_images_per_prompt=1,
        ).images[0]
        with Path(plan['output']).open('xb') as stream:
            image.save(stream, format='PNG')
        record = dict(plan, **settings, **provenance, status='generated',
                      stage='segmented_cutout_to_pose_mannequin',
                      output_sha256=sha256(Path(plan['output'])),
                      elapsed_seconds=round(time.monotonic()-started, 2),
                      review_required='Compare pose, foreshortening, hands and occluded boundaries before identity transfer.')
        with Path(plan['result']).open('x', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print(json.dumps({'scene': plan['scene'], 'output': plan['output'], 'result': plan['result']}), flush=True)


if __name__ == '__main__':
    main()

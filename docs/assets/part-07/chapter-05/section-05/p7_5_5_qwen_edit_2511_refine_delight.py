#!/usr/bin/env python3
"""Refine DeLight candidates with separately recorded local GPU edits.

Default order: B hair -> B shoes -> B trousers, C shoes, C supporting style.
Picture 1 supplies the composition; Picture 2 supplies only the requested
hair, clothing, footwear, or rendering style. These are prompt constraints, not masks:
pixel-level preservation must be checked in the generated images.
Use --dry-run to inspect dependencies and prompts without loading the model.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import platform
import re
import time
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent
ROOT = ASSETS.parents[3]
CACHE = ROOT / '.tmp/download/huggingface/hub'
MODEL_ID = 'Qwen/Qwen-Image-Edit-2511'
TASKS = ('b-hair', 'b-shoes', 'b-trousers', 'c-shoes', 'c-supporting-style')
PREDECESSORS = {'b-shoes': 'b-hair', 'b-trousers': 'b-shoes'}
MIRA_REFERENCE = ASSETS / ('p7-5-3-qwen-edit-prompt-style-outfit_stage3_jacket_face-three-stage-v1-seed-62294-steps-10.png')


def delight(label: str) -> Path:
    return ASSETS / (f'p7-5-5-qwen-2509-studio-delight-{label}'
                     '-size-1280x1280-seed-62294-steps-10.png')


SOURCES = {
    'b-hair': delight('scene-b-mira-extras-v8-v1'),
    'c-shoes': delight('scene-c-mira-extras-v7-v1'),
    'c-supporting-style': delight('scene-c-supporting-extras-v7-v1'),
}
STYLE_REFERENCE = SOURCES['c-shoes']
PROMPTS = {
    'b-hair': (
        "Shorten only the woman's hair in Image 1 to the jaw-length teal bob in Image 2. "
        "Keep the wind-swept direction, face, head angle, jumping pose, clothing, shoes, "
        "linework, lighting, framing, and background of Image 1."
    ),
    'b-shoes': (
        "Replace only both shoes in Image 1 with the white low-top lace-up sneakers "
        "in Image 2. Fit them to the existing feet and perspective. Preserve the "
        "jumping pose, foot directions, trouser hems, face, corrected short hair, "
        "linework, lighting, framing, and background of Image 1."
    ),
    'b-trousers': (
        "Replace the trousers in Image 1 with the trousers in Image 2. "
        "The trouser hems should reach ankle level without covering the shoes. "
        "Keep the pose and everything else in Image 1 unchanged."
    ),
    'c-shoes': (
        "Replace only both shoes in Image 1 with the white low-top lace-up sneakers "
        "in Image 2. Fit them to the existing feet and perspective. Preserve the "
        "seated pose, foot positions, trouser hems, face, hair, clothing, linework, "
        "lighting, framing, and background of Image 1."
    ),
    'c-supporting-style': (
        "Redraw the man in Image 1 using the clean outlined comic linework and flat "
        "restrained colors of Image 2. Use Image 2 only as a rendering-style reference. "
        "Preserve the man's identity, black short hair, gray hoodie and trousers, "
        "shoes, seated pose, hands, proportions, framing, lighting, and background "
        "of Image 1. Keep one man and the existing clothing design."
    ),
}


def sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def output_path(args, task: str) -> Path:
    return args.output_dir.resolve() / (
        f'p7-5-5-qwen-2511-delight-refine-{task}-{args.run_label}'
        f'-size-{args.size}x{args.size}-seed-{args.seed}-steps-{args.steps}.png'
    )


def build_plans(args) -> list[dict]:
    selected = [task for task in TASKS if task in args.tasks]
    scheduled = set()
    plans = []
    for task in selected:
        source = (args.input or (output_path(args, PREDECESSORS[task]) if task in PREDECESSORS
                                else SOURCES[task])).resolve()
        reference = (args.reference or (args.style_reference if task == 'c-supporting-style'
                                       else args.mira_reference)).resolve()
        output = output_path(args, task)
        result = output.with_name(output.stem + '-result.json')
        for path in (source, reference):
            if path not in scheduled and not path.is_file():
                raise FileNotFoundError(
                    f'{task}: missing input {path}. B shoes requires B hair; B trousers '
                    'requires B shoes. Select the preceding tasks or supply --input for one task.'
                )
        for path in (output, result):
            if path.exists():
                raise FileExistsError(f'Use a new --run-label or --output-dir: {path}')
            if path in (source, reference):
                raise ValueError('Output cannot overwrite an input')
        plans.append(dict(task=task, source=str(source), reference=str(reference),
                          source_generated_in_this_run=source in scheduled,
                          reference_role=('rendering style only' if task == 'c-supporting-style'
                                          else 'hair length only' if task == 'b-hair'
                                          else 'trouser design only' if task == 'b-trousers'
                                          else 'footwear design only'),
                          prompt=args.prompt or PROMPTS[task], output=str(output), result=str(result)))
        scheduled.add(output)
    return plans


def canvas(path: str, size: int):
    from PIL import Image
    with Image.open(path) as original:
        image = original.convert('RGBA')
    image.thumbnail((size, size), Image.Resampling.LANCZOS)
    background = Image.new('RGBA', (size, size), 'white')
    background.alpha_composite(image, ((size-image.width)//2, (size-image.height)//2))
    return background.convert('RGB')


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tasks', nargs='+', choices=TASKS, default=list(TASKS))
    parser.add_argument('--input', type=Path, help='Override Image 1 for one task.')
    parser.add_argument('--reference', type=Path, help='Override Image 2 for one task.')
    parser.add_argument('--prompt', help='Override the prompt for one task.')
    parser.add_argument('--mira-reference', type=Path, default=MIRA_REFERENCE)
    parser.add_argument('--style-reference', type=Path, default=STYLE_REFERENCE)
    parser.add_argument('--steps', type=int, default=20)
    parser.add_argument('--size', type=int, default=1280)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--true-cfg-scale', type=float, default=4.0)
    parser.add_argument('--run-label', default='v1')
    parser.add_argument('--output-dir', type=Path, default=ASSETS / "section-05")
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    if len(set(args.tasks)) != len(args.tasks):
        parser.error('Select each task only once')
    if any(value is not None for value in (args.input, args.reference, args.prompt)) and len(args.tasks) != 1:
        parser.error('--input, --reference and --prompt require exactly one task')
    if args.steps < 1 or args.size < 32 or args.size % 32 or args.seed < 0 or args.true_cfg_scale <= 0:
        parser.error('Positive steps/CFG, nonnegative seed, and size divisible by 32 are required')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('--run-label must contain only letters, digits, underscores and hyphens')
    return args


def main():
    args = parse_args()
    plans = build_plans(args)
    settings = dict(seed=args.seed, steps=args.steps, size=args.size,
                    true_cfg_scale=args.true_cfg_scale, guidance_scale=1.0)
    if args.dry_run:
        print(json.dumps(dict(status='planned', model=MODEL_ID, settings=settings,
                              plans=plans), ensure_ascii=False, indent=2))
        return
    import torch
    from diffusers import QwenImageEditPlusPipeline
    if not torch.cuda.is_available():
        raise RuntimeError('Local CUDA GPU required; CPU-only generation is not supported')
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE, local_files_only=True)
    pipeline.enable_attention_slicing('max')
    pipeline.enable_sequential_cpu_offload()
    try:
        for plan in plans:
            output, result = Path(plan['output']), Path(plan['result'])
            if output.exists() or result.exists():
                raise FileExistsError(output if output.exists() else result)
            inputs = [dict(role='Image 1: edit target', path=plan['source'],
                           sha256=sha256(Path(plan['source']))),
                      dict(role='Image 2: ' + plan['reference_role'], path=plan['reference'],
                           sha256=sha256(Path(plan['reference'])))]
            started = time.monotonic()
            image = pipeline(
                image=[canvas(plan['source'], args.size), canvas(plan['reference'], args.size)],
                prompt=plan['prompt'], negative_prompt=' ', width=args.size, height=args.size,
                num_inference_steps=args.steps, true_cfg_scale=args.true_cfg_scale,
                guidance_scale=1.0, generator=torch.Generator('cuda').manual_seed(args.seed),
            ).images[0]
            output.parent.mkdir(parents=True, exist_ok=True)
            with output.open('xb') as stream:
                image.save(stream, format='PNG')
            record = dict(status='generated', stage='post_delight_refinement', task=plan['task'],
                          inputs=inputs, prompt=plan['prompt'], settings=settings,
                          source_generated_in_this_run=plan['source_generated_in_this_run'],
                          model=dict(repository=MODEL_ID, dtype='bfloat16',
                                     device_placement='sequential_cpu_offload', lora=None),
                          runtime=dict(python=platform.python_version(), cuda_device=torch.cuda.get_device_name(0),
                                       packages={k: importlib.metadata.version(k) for k in ('torch','diffusers','transformers','accelerate')}),
                          output=dict(path=str(output), sha256=sha256(output), width=image.width, height=image.height),
                          elapsed_seconds=round(time.monotonic()-started, 2),
                          review_required='Prompt-only editing; check non-target drift, pose, identity, style and boundaries.')
            with result.open('x', encoding='utf-8') as stream:
                json.dump(record, stream, ensure_ascii=False, indent=2)
                stream.write('\n')
            print(json.dumps(dict(task=plan['task'], output=str(output), result=str(result))), flush=True)
    finally:
        del pipeline
        torch.cuda.empty_cache()


if __name__ == '__main__':
    main()

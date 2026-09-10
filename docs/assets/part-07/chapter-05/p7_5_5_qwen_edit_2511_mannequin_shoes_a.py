#!/usr/bin/env python3
"""Put white sneakers on the scene A mannequin before applying the outfit.

Local Qwen Edit 2511 with the barefoot mannequin as Picture 1.
Optional shoe and outsole references; no mask or LoRA.
Inspect both feet before the outfit stage.
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

SOURCE = ASSETS / 'p7-5-5-qwen-2511-cutout-mannequin-a-mira-compressed-v2-size-1280x1280-seed-62294-steps-20.png'
PROMPT = 'Make the woman in Picture 1 wear white sneakers. Replace the foreground bare foot with a white sneaker, its sole facing the camera. Keep everything else unchanged.'
STAGE = 'mannequin-shoes-a'
SHOE = ASSETS / 'p7-5-3-qwen-image-2512-white-sneakers-v1-size-1280x1280-seed-62294-steps-10.png'
OUTSOLE = ASSETS / 'p7-5-3-qwen-2511-white-sneaker-outsole-v1-size-1280x1280-seed-62294-steps-20.png'
REFERENCE_PROMPT = 'Make the woman in Picture 1 wear the sneakers from Picture 2. Replace the foreground bare foot with a sneaker, its sole facing the camera and matching Picture 3. Keep everything else unchanged.'
DESIGN = ASSETS / 'p7-5-3-qwen-2511-white-sneaker-outsole-upper-bottom-v3-size-1280x1280-seed-62294-steps-20.png'
DESIGN_PROMPT = 'Replace both the foreground and rear bare feet of the woman in Picture 1 with the sneakers from Picture 2.'
CUTOUT = ASSETS / 'p7-5-5-character-cutout-scene-a-mira-audit-20260909-v1.png'
CUTOUT_PROMPT = 'Replace both sneakers worn by the woman in Picture 1 with the sneakers from Picture 2.'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=SOURCE)
    parser.add_argument('--prompt', help='Override the selected experiment prompt.')
    parser.add_argument('--steps', type=int, default=20)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--run-label', default='v1')
    parser.add_argument('--output-dir', type=Path, default=ASSETS)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--with-shoe-references', action='store_true', help='Use P7-5.3 shoe and outsole images as Pictures 2 and 3.')
    parser.add_argument('--design-reference', type=Path, nargs='?', const=DESIGN, help='Use one combined upper/outsole design image as Picture 2.')
    parser.add_argument('--design-first', action='store_true', help='Put the combined design before the mannequin; remap image numbers in the default prompt.')
    parser.add_argument('--cutout', action='store_true', help='Replace existing shoes in the original scene A cutout using the combined design.')
    args = parser.parse_args()
    if args.cutout:
        if args.design_reference is None:
            parser.error('--cutout requires --design-reference.')
        if args.input != SOURCE:
            parser.error('--cutout selects its own input; omit --input.')
        args.input = CUTOUT
    if args.design_first and args.design_reference is None:
        parser.error('--design-first requires --design-reference.')
    if args.design_reference is not None and args.with_shoe_references:
        parser.error('Choose either a combined design or separate shoe references.')
    if args.steps < 1 or (args.prompt is not None and not args.prompt.strip()):
        parser.error('Positive steps and a nonempty prompt are required.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label.')
    prompt = args.prompt or (REFERENCE_PROMPT if args.with_shoe_references else PROMPT)
    design_prompt = CUTOUT_PROMPT if args.cutout else DESIGN_PROMPT
    subject_role = 'original scene A Mira cutout' if args.cutout else 'barefoot scene A mannequin'
    if args.design_reference is not None and args.prompt is None:
        prompt = design_prompt
    image_paths = [(args.input, f'Picture 1: {subject_role}')]
    if args.design_reference is not None:
        image_paths.append((args.design_reference, 'Picture 2: sneaker upper and outsole design'))
    if args.with_shoe_references:
        image_paths.extend([(SHOE, 'Picture 2: complete sneaker design'),
                            (OUTSOLE, 'Picture 3: sneaker outsole design')])
    if args.design_first:
        image_paths = [(args.design_reference, 'Picture 1: sneaker upper and outsole design'),
                       (args.input, f'Picture 2: {subject_role}')]
        if args.prompt is None:
            prompt = design_prompt.replace('Picture 1', 'Picture TEMP').replace('Picture 2', 'Picture 1').replace('Picture TEMP', 'Picture 2')
    inputs = []
    for path, role in image_paths:
        path = path.resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        inputs.append(dict(path=str(path), role=role, sha256=sha256(path)))
    stage = 'cutout-shoes-a' if args.cutout else STAGE
    stem = (f'p7-5-5-qwen-2511-{stage}-{args.run_label}'
            f'-size-1280x1280-seed-{args.seed}-steps-{args.steps}')
    output = args.output_dir.resolve() / f'{stem}.png'
    result = output.with_name(f'{stem}-result.json')
    for path in (output, result):
        if path.exists():
            raise FileExistsError(f'Refusing to overwrite: {path}')
    plan = dict(stage=stage, model=MODEL_ID, inputs=inputs, prompt=prompt.strip(),
                output=str(output), result=str(result), steps=args.steps, seed=args.seed,
                size=[1280, 1280], true_cfg_scale=4.0, guidance_scale=1.0,
                generator_device='cpu', dtype='bfloat16', mask=None, lora=None,
                design_first=args.design_first, subject='cutout' if args.cutout else 'mannequin',
                experiment=f'{stage}-combined-design' if args.design_reference is not None else ('mannequin-shoes-with-references' if args.with_shoe_references else 'mannequin-shoes-before-outfit'))
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
                  helper_code_sha256=sha256(ASSETS / 'p7_5_5_qwen_edit_2511_pose_identity.py'),
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

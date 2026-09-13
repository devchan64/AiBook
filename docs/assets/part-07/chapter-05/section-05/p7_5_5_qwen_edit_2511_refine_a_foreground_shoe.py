#!/usr/bin/env python3
"""Refine only the foreground shoe in the scene A outfit result.

Local Qwen 2511, one to three image inputs, no masks or LoRA. Face/hair refinement is
reserved for the final BFS pass. Inspect the result before further editing.
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

SOURCE = ASSETS / 'section-05/p7-5-5-qwen-2511-mannequin-outfit-a-mira-stage3-v1-size-1280x1280-seed-62294-steps-20.png'
REFERENCE = ASSETS / 'p7-5-3-qwen-2511-white-sneaker-outsole-v1-size-1280x1280-seed-62294-steps-20.png'
REFERENCE_ROLE = 'Picture 2: sneaker outsole design'
PROMPT = 'Replace the large foreground bare foot in Picture 1 with the sneaker from Picture 2, its outsole facing the camera. Keep everything else in Picture 1 unchanged.'
SHOD_SOURCE = ASSETS / 'section-05/p7-5-5-qwen-2511-refine-a-foreground-shoe-single-v2-size-1280x1280-seed-62294-steps-20.png'
SOLE_PROMPT = 'Change the sole of the large foreground sneaker in Picture 1 to match Picture 2. Keep everything else unchanged.'
SHOE_VIEW = ASSETS / 'p7-5-3-qwen-image-2512-white-sneakers-v1-size-1280x1280-seed-62294-steps-10.png'
TWO_SHOE_PROMPT = 'Make the woman in Picture 1 wear the sneakers shown in Pictures 2 and 3. Replace the foreground bare foot with a white sneaker, its sole facing the camera. Keep her pose unchanged.'
STAGE = 'refine-a-foreground-shoe'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='Override the input selected by the experiment mode.')
    parser.add_argument('--reference', type=Path, default=REFERENCE)
    parser.add_argument('--prompt', help='Override the selected experiment prompt.')
    parser.add_argument('--steps', type=int, default=20)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--run-label', default='outsole-v3')
    parser.add_argument('--output-dir', type=Path, default=ASSETS / "section-05")
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--no-reference', action='store_true', help='Single-image shoe replacement experiment.')
    parser.add_argument('--sole-only', action='store_true', help='Start from the successful sneaker result and change only its sole.')
    parser.add_argument('--shoe-reference', type=Path, nargs='?', const=SHOE_VIEW, help='Add the full shoe as Picture 2 and use --reference as Picture 3 outsole. Defaults to the P7-5.3 sneaker image when no path is supplied.')
    args = parser.parse_args()
    if args.shoe_reference is not None and (args.sole_only or args.no_reference):
        parser.error('--shoe-reference uses the barefoot input and cannot combine with --sole-only or --no-reference.')
    if args.sole_only and args.no_reference:
        parser.error('--sole-only requires a reference; do not combine with --no-reference.')
    source = args.input or (SHOD_SOURCE if args.sole_only else SOURCE)
    if args.steps < 1 or (args.prompt is not None and not args.prompt.strip()):
        parser.error('Positive steps and a nonempty prompt are required.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label.')
    prompt = args.prompt or ('Replace the large foreground bare foot in Picture 1 with a white sneaker, its sole facing the camera. Keep everything else unchanged.' if args.no_reference else PROMPT)
    if args.sole_only and args.prompt is None:
        prompt = SOLE_PROMPT
    image_paths = [(source, 'Picture 1: successful sneaker replacement' if args.sole_only else 'Picture 1: outfit first-pass result')]
    if args.shoe_reference is not None:
        if args.prompt is None:
            prompt = TWO_SHOE_PROMPT
        image_paths.extend([(args.shoe_reference, 'Picture 2: complete sneaker design'),
                            (args.reference, 'Picture 3: sneaker outsole design')])
    elif not args.no_reference:
        image_paths.append((args.reference, REFERENCE_ROLE))
    inputs = []
    for path, role in image_paths:
        path = path.resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        inputs.append(dict(path=str(path), role=role, sha256=sha256(path)))
    stem = (f'p7-5-5-qwen-2511-{STAGE}-{args.run_label}'
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
                experiment='two-shoe-references' if args.shoe_reference is not None else ('sole-only' if args.sole_only else ('single-image' if args.no_reference else 'two-image')))
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
                  helper_code_sha256=sha256(ASSETS / 'section-05/p7_5_5_qwen_edit_2511_pose_identity.py'),
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

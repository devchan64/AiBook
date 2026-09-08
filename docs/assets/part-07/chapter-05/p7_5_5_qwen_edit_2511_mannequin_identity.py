#!/usr/bin/env python3
"""Experiment: B cutout -> neutral mannequin -> Mira, with a review between stages.

Run --stage mannequin first, inspect its pose, then run --stage identity.
The identity stage places Mira first and the mannequin second (from v4 onward).
Both stages use local Qwen 2511 without masks, LoRA, or output compositing.
To compare a depth reference, run --stage depth with local Depth Anything V2
Small, inspect it, then run --stage depth-identity. The depth PNG is an ordinary
Qwen image reference, not a ControlNet input. Raw relative depth is saved as NPY.
Use --stage pose-person-face-hair to replace only the face and hairstyle of the
20-step pose person, using Mira's frontal head asset as Picture 2 (from v3).
Default generation is 20 steps.
"""
import argparse
import json
import re
import time
from pathlib import Path

from p7_5_5_qwen_edit_2511_refine_delight import (
    ASSETS, CACHE, MODEL_ID, MIRA_REFERENCE, sha256,
)

SOURCE = ASSETS / 'p7-5-5-character-cutout-scene-b-mira-extras-v8-v1.png'
MIRA_HEAD_REFERENCE = ASSETS / (
    'p7-5-2-mira-head-qwen-image-bf16-front-v1-code-63ece7-'
    'seed-62294-steps-30-size-1280.png'
)
DEPTH_MODEL_ID = 'depth-anything/Depth-Anything-V2-Small-hf'
DEPTH_MODEL_PATH = ASSETS.parents[3] / '.tmp/download/model-depth-anything-v2-small-hf'
PROMPTS = {
    'shoes-stage53': (
        'Put the shoes worn by the woman in Picture 2 on the feet of the woman '
        'in Picture 1. Keep everything else in Picture 1 unchanged.'
    ),
    'outfit-stage53': (
        'Replace the outfit of the woman in Picture 1, including her shoes, '
        'with the outfit of the woman in Picture 2. '
        'Preserve the face, hairstyle, pose, and background of Picture 1.'
    ),
    'diagnostic-single-edit': (
        'Change the sports bra in Picture 1 to bright red. Keep everything else unchanged.'
    ),
    'pose-person-face-hair': (
        'Replace the woman in Picture 1 with the woman in Picture 2, preserving the pose. '
        'Preserve the split-leap pose and the cast shadow beneath the woman.'
    ),
    'pose-person-identity': (
        'Replace the person in Picture 1 with the person in Picture 2, '
        'preserving the pose of Picture 1.'
    ),
    'pose-person': (
        'Change the person in Picture 1 into an adult woman with a very short '
        'buzz cut, wearing a plain sports bra and briefs. Keep her face, facial '
        'features, and expression. Preserve the original pose, head orientation, '
        'joint positions, fingertips, toes, body placement, framing, and illustration style.'
    ),
    'cutout-identity': (
        'Make the person in Picture 1 adopt the pose of the person in Picture 2. '
        'Preserve the identity and appearance from Picture 1. '
        'Use Picture 2 only as a pose reference.'
    ),
    'mannequin': (
        'Replace the character in Image 1 with a smooth gray anatomical mannequin '
        'without facial features, hair, clothing, or accessories. Preserve the pose, '
        'body proportions, head direction, hand and foot positions, framing, and background.'
    ),
    'identity': (
        'Make the person in Picture 1 adopt the pose in Picture 2. '
        'Preserve the identity and appearance from Picture 1.'
    ),
    'depth-identity': (
        'Make the person in Picture 1 adopt the pose indicated by the depth map '
        'in Picture 2. Preserve the identity and appearance from Picture 1. '
        'Use Picture 2 only as a pose reference.'
    ),
}


def output(stage, run_label='v1', steps=20):
    return ASSETS / (f'p7-5-5-qwen-2511-scene-b-{stage}-{run_label}-'
                     f'size-1280x1280-seed-62294-steps-{steps}.png')


def reference_image(path):
    """Keep native dimensions; let Qwen resize each reference at its own ratio."""
    from PIL import Image
    with Image.open(path) as source:
        rgba = source.convert('RGBA')
    background = Image.new('RGBA', rgba.size, 'white')
    return Image.alpha_composite(background, rgba).convert('RGB')


def generate_depth(dry_run):
    source, target = output('mannequin'), output('mannequin-depth')
    result = target.with_name(target.stem + '-result.json')
    raw = target.with_suffix('.npy')
    for p in (target, result, raw):
        if p.exists():
            raise FileExistsError(p)
    if not source.is_file():
        raise FileNotFoundError(source)
    if dry_run:
        print(json.dumps(dict(model=DEPTH_MODEL_ID, input=str(source), output=str(target))))
        return
    import numpy as np
    import torch
    from PIL import Image
    from transformers import AutoImageProcessor, AutoModelForDepthEstimation
    if not torch.cuda.is_available():
        raise RuntimeError('Local CUDA GPU is required')
    processor = AutoImageProcessor.from_pretrained(DEPTH_MODEL_PATH, local_files_only=True)
    model = AutoModelForDepthEstimation.from_pretrained(
        DEPTH_MODEL_PATH, local_files_only=True).to('cuda').eval()
    image = Image.open(source).convert('RGB')
    inputs = processor(images=image, return_tensors='pt').to('cuda')
    with torch.inference_mode():
        depth = model(**inputs).predicted_depth
        depth = torch.nn.functional.interpolate(depth.unsqueeze(1), size=image.size[::-1],
                                                mode='bicubic', align_corners=False)[0, 0]
    values = depth.cpu().numpy()
    low, high = float(values.min()), float(values.max())
    if high <= low:
        raise RuntimeError('Depth prediction is constant')
    preview = Image.fromarray(np.rint((values-low)/(high-low)*255).astype('uint8'))
    with target.open('xb') as stream:
        preview.save(stream, format='PNG')
    with raw.open('xb') as stream:
        np.save(stream, values)
    record = dict(stage='mannequin-depth', model=DEPTH_MODEL_ID,
                  model_card='https://huggingface.co/' + DEPTH_MODEL_ID,
                  weights_sha256=sha256(DEPTH_MODEL_PATH / 'model.safetensors'),
                  inputs=[dict(path=str(source), sha256=sha256(source))],
                  output=dict(path=str(target), sha256=sha256(target)),
                  raw=dict(path=str(raw), sha256=sha256(raw)),
                  normalization=dict(method='whole-image min-max', min=low, max=high),
                  interpretation='relative inverse depth; brighter is nearer; not metric distance',
                  mask=False, cuda_device=torch.cuda.get_device_name(0))
    with result.open('x') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(record), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', choices=[*PROMPTS, 'depth'], required=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--steps', type=int, default=20)
    parser.add_argument('--face-reference', type=Path,
                        help='Override Picture 2 for pose-person-face-hair comparisons.')
    parser.add_argument('--run-label', default='v1',
                        help='Output version for Qwen stages; input mannequin remains v1.')
    args = parser.parse_args()
    if args.face_reference and args.stage != 'pose-person-face-hair':
        parser.error('--face-reference requires --stage pose-person-face-hair')
    if args.steps < 1:
        parser.error('--steps must be positive')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label')
    if args.stage == 'depth':
        generate_depth(args.dry_run)
        return
    pose_stage = 'mannequin-depth' if args.stage == 'depth-identity' else 'mannequin'
    paths = [SOURCE] if args.stage == 'mannequin' else [output(pose_stage), MIRA_REFERENCE]
    roles = ['Image 1: pose cutout'] if args.stage == 'mannequin' else [
        'Image 1: ' + pose_stage, 'Image 2: Mira face, hair and complete outfit']
    if args.stage == 'identity':
        paths = [MIRA_REFERENCE, output('mannequin')]
        roles = ['Image 1: Mira face, hair and complete outfit', 'Image 2: mannequin pose']
    elif args.stage == 'depth-identity':
        paths = [MIRA_REFERENCE, output('mannequin-depth')]
        roles = ['Image 1: Mira face, hair and complete outfit', 'Image 2: depth pose reference']
    elif args.stage == 'cutout-identity':
        paths = [MIRA_REFERENCE, SOURCE]
        roles = ['Image 1: Mira identity reference', 'Image 2: original B cutout pose reference']
    elif args.stage == 'pose-person':
        paths = [SOURCE]
        roles = ['Picture 1: original B cutout; preserve face and pose']
    elif args.stage == 'pose-person-identity':
        paths = [output('pose-person', 'v1', 5), MIRA_REFERENCE]
        roles = ['Picture 1: face-bearing person pose reference', 'Picture 2: Mira identity reference']
    elif args.stage == 'pose-person-face-hair':
        paths = [output('pose-person', 'v1', 20),
                 args.face_reference.resolve() if args.face_reference else MIRA_HEAD_REFERENCE]
        roles = ['Picture 1: 20-step pose person', 'Picture 2: face and hairstyle reference']
    elif args.stage == 'diagnostic-single-edit':
        paths = [output('pose-person', 'v1', 20)]
        roles = ['Picture 1: 20-step pose person; single-image edit control']
    elif args.stage == 'outfit-stage53':
        paths = [output('pose-person-face-hair', 'v5-outfit', 30), MIRA_REFERENCE]
        roles = ['Picture 1: B identity-transfer result', 'Picture 2: Section 5.3 final outfit reference']
    elif args.stage == 'shoes-stage53':
        paths = [output('pose-person-face-hair', 'v5-outfit', 30), MIRA_REFERENCE]
        roles = ['Picture 1: B identity-transfer result with bare feet',
                 'Picture 2: Section 5.3 shoe reference']
    target = output(args.stage, args.run_label, args.steps)
    record_path = target.with_name(target.stem + '-result.json')
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
    for path in (target, record_path):
        if path.exists():
            raise FileExistsError(path)
    record = dict(stage=args.stage, prompt=PROMPTS[args.stage],
                  inputs=[dict(path=str(p), role=r, sha256=sha256(p)) for p, r in zip(paths, roles)],
                  settings=dict(size=1280, steps=args.steps, seed=62294, true_cfg_scale=4.0,
                                mask=False, lora=None, output_compositing=False),
                  model=MODEL_ID, output=dict(path=str(target)))
    images = [reference_image(p) for p in paths]
    record['input_preprocessing'] = dict(
        mode='native aspect ratio; RGB; transparency on white; no square padding',
        sizes=[list(im.size) for im in images],
        pipeline='QwenImageEditPlusPipeline performs per-image condition and VAE resizing')
    if args.dry_run:
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return
    import torch
    from diffusers import QwenImageEditPlusPipeline
    if not torch.cuda.is_available():
        raise RuntimeError('Local CUDA GPU is required')
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, torch_dtype=torch.bfloat16, cache_dir=CACHE, local_files_only=True)
    pipeline.enable_attention_slicing('max')
    pipeline.enable_sequential_cpu_offload()
    started = time.monotonic()
    image = pipeline(image=images,
                     prompt=PROMPTS[args.stage], negative_prompt=' ', width=1280, height=1280,
                     num_inference_steps=args.steps, true_cfg_scale=4.0, guidance_scale=1.0,
                     generator=torch.Generator('cuda').manual_seed(62294)).images[0]
    with target.open('xb') as stream:
        image.save(stream, format='PNG')
    record.update(status='generated', elapsed_seconds=round(time.monotonic()-started, 2),
                  cuda_device=torch.cuda.get_device_name(0), dtype='bfloat16',
                  device_placement='sequential_cpu_offload')
    record['output'].update(sha256=sha256(target), width=image.width, height=image.height)
    with record_path.open('x') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps(record, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Relight one composed image using text lighting notes from the original scene.

By default, original P7-5.4 images were visually inspected to author the prompts; they are
provenance only and are not passed to the pipeline in the default mode. Lighting descriptions
are qualitative interpretations, not measured light parameters.
The --lighting-image-reference option restores the historical two-image comparison.
Uses the manuscript dx8152 Relight LoRA and 2509 base. No mask.
Local CUDA execution only.

LoRA source: https://huggingface.co/dx8152/Qwen-Image-Edit-2509-Relight
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import hashlib
import importlib.metadata
import platform
import sys
from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent

PROJECT_ROOT = ASSETS.parents[3]

CACHE_DIR = PROJECT_ROOT / ".tmp" / "download" / "huggingface" / "hub"

def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def runtime_record() -> dict[str, object]:
    packages = {}
    for package in ("diffusers", "torch", "transformers", "accelerate"):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = "not-installed"
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": packages,
    }

def square_canvas(path: Path, size: int) -> Image.Image:
    """Return an RGB, white-backed square canvas without distorting the input."""
    with Image.open(path) as source:
        source = source.convert("RGBA")
        source.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (size, size), "white")
        offset = ((size - source.width) // 2, (size - source.height) // 2)
        canvas.alpha_composite(source, offset)
    return canvas.convert("RGB")

MODEL_ID = 'Qwen/Qwen-Image-Edit-2509'
TRANSFORMER_DIR = ASSETS.parents[3] / '.tmp/download/model-qwen-image-edit-2509/transformer'
LORA_ID = 'dx8152/Qwen-Image-Edit-2509-Relight'
LORA = ASSETS.parents[3] / '.tmp/download/weight-dx8152-qwen-image-edit-2509-relight/Qwen-Edit-Relight.safetensors'
LORA_SHA256 = '2a11c2b74ce0965abf35a8c8db52305072e970a689ca904b5a5b5a94d0aab86c'

SOURCES = {
    scene: [ASSETS / f'section-05/p7-5-5-qwen-2511-delight-composite-scene-{scene}-v1-size-1280x1280-seed-62294-steps-10.png']
    for scene in ('a', 'b', 'c')
}
PROMPT_BASIS = {
    scene: ASSETS / f'p7-5-4-qwen-2511-lineart-scene-{scene}-extras-audit-20260909-v1-size-1280x1280-seed-{seed}-steps-20.png'
    for scene, seed in (('a', 5420), ('b', 5421), ('c', 5422))
}
ROLES = ['Picture 1: composed scene to relight']
PROMPTS = {
    'a': '重新照明, bright neutral daylight from the open sky above, illuminating the street and people, with shaded building sides. Preserve the scene content and composition.',
    'b': '重新照明, warm golden sunset backlight from low on the central horizon, with warm rim light on the woman and tree edges and soft cool skylight on the front. Preserve the scene content and composition.',
    'c': '重新照明, soft neutral daylight from the open sky, evenly illuminating the readers, books and rocks, with gentle shade beneath the tree. Preserve the scene content and composition.',
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--targets', nargs='+', choices=tuple(SOURCES), default=list(SOURCES))
    parser.add_argument('--prompt', help='Optional prompt override for a single target.')
    parser.add_argument('--lora-scale', type=float, default=1.0)
    parser.add_argument('--steps', type=int, default=10)
    parser.add_argument('--seed', type=int, default=62294)
    parser.add_argument('--run-label', default='text-v2')
    parser.add_argument('--output-dir', type=Path, default=ASSETS / "section-05")
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--lighting-image-reference', action='store_true',
                        help='Historical comparison: pass original scene as Picture 2 instead of text-only lighting.')
    args = parser.parse_args()
    if args.steps < 1 or (args.prompt is not None and not args.prompt.strip()):
        parser.error('Positive steps and a nonempty prompt are required.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', args.run_label):
        parser.error('Use letters, digits, underscores and hyphens for --run-label.')
    if args.prompt is not None and len(set(args.targets)) != 1:
        parser.error('--prompt requires a single target.')
    if not 0 < args.lora_scale < float('inf'):
        parser.error('--lora-scale must be finite and positive.')
    if sha256(LORA) != LORA_SHA256:
        raise ValueError('Relight LoRA SHA-256 mismatch.')
    if not (TRANSFORMER_DIR / 'config.json').is_file():
        raise FileNotFoundError(TRANSFORMER_DIR / 'config.json')
    plans = []
    for target in dict.fromkeys(args.targets):
        sources = [source.resolve() for source in SOURCES[target]]
        if args.lighting_image_reference:
            sources.append(PROMPT_BASIS[target].resolve())
        for source in sources:
            if not source.is_file():
                raise FileNotFoundError(source)
        stem = (f'p7-5-5-qwen-2509-{"reference" if args.lighting_image_reference else "text"}-relight-scene-{target}-{args.run_label}'
                f'-size-1280x1280-seed-{args.seed}-steps-{args.steps}')
        output = args.output_dir.resolve() / f'{stem}.png'
        result = output.with_name(f'{stem}-result.json')
        for path in (output, result):
            if path.exists():
                raise FileExistsError(f'Refusing to overwrite: {path}')
        plans.append(dict(scene=target, prompt=args.prompt or (
            '重新照明, relight Picture 1 to match the light direction, color temperature, brightness and contrast of Picture 2. Use Picture 2 only as a lighting reference. Preserve the characters, faces, hairstyles, outfits, poses, objects and composition of Picture 1.'
            if args.lighting_image_reference else PROMPTS[target]), inputs=[dict(role=(ROLES + ['Picture 2: original scene lighting reference'])[index], path=str(source), sha256=sha256(source))
                          for index, source in enumerate(sources)],
                          output=str(output), result=str(result),
                          prompt_basis=dict(path=str(PROMPT_BASIS[target]), sha256=sha256(PROMPT_BASIS[target]),
                                            usage=('Picture 2 model input' if args.lighting_image_reference else 'visual prompt authoring only; not a model input'),
                                            description_type='qualitative visual interpretation',
                                            prompt_override=args.prompt is not None)))
    settings = dict(model=MODEL_ID, steps=args.steps, seed=args.seed,
                    size=[1280, 1280], true_cfg_scale=4.0, guidance_scale=1.0,
                    generator_device='cpu', dtype='bfloat16', mask=None, negative_prompt=' ', lora=dict(repository=LORA_ID, path=str(LORA), sha256=LORA_SHA256,
                    adapter='dx8152_relight', trigger='重新照明', scale=args.lora_scale),
                    reference_mode=('two images: composite and original lighting reference' if args.lighting_image_reference else 'single image with text lighting instruction'))
    if args.dry_run:
        print(json.dumps(dict(status='planned', settings=settings, plans=plans), indent=2))
        return
    import torch
    from diffusers import QwenImageEditPlusPipeline, QwenImageTransformer2DModel

    if not torch.cuda.is_available():
        raise RuntimeError('A local CUDA GPU is required.')
    transformer = QwenImageTransformer2DModel.from_pretrained(
        TRANSFORMER_DIR, torch_dtype=torch.bfloat16, local_files_only=True,
    )
    pipeline = QwenImageEditPlusPipeline.from_pretrained(
        MODEL_ID, transformer=transformer, torch_dtype=torch.bfloat16, cache_dir=CACHE_DIR, local_files_only=True,
    )
    pipeline.load_lora_weights(LORA.parent, weight_name=LORA.name, adapter_name='dx8152_relight', local_files_only=True)
    pipeline.set_adapters(['dx8152_relight'], adapter_weights=[args.lora_scale])
    pipeline.enable_attention_slicing('max')
    pipeline.enable_sequential_cpu_offload()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    provenance = dict(source_code_sha256=sha256(Path(__file__)),

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
            image=([square_canvas(Path(item['path']), 1280) for item in plan['inputs']]
                   if args.lighting_image_reference else square_canvas(Path(plan['inputs'][0]['path']), 1280)),
            prompt=plan['prompt'], height=1280, width=1280,
            generator=torch.Generator(device='cpu').manual_seed(args.seed),
            true_cfg_scale=4.0, negative_prompt=' ', num_inference_steps=args.steps,
            guidance_scale=1.0, num_images_per_prompt=1,
        ).images[0]
        with Path(plan['output']).open('xb') as stream:
            image.save(stream, format='PNG')
        record = dict(plan, **settings, **provenance, status='generated', stage=('scene_reference_lighting_relight' if args.lighting_image_reference else 'scene_text_lighting_relight'),
                      output_sha256=sha256(Path(plan['output'])),
                      elapsed_seconds=round(time.monotonic()-started, 2))
        with Path(plan['result']).open('x', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        print(json.dumps({'scene': plan['scene'], 'output': plan['output'], 'result': plan['result']}), flush=True)


if __name__ == '__main__':
    main()

---
language:
- en
- ko
license: apache-2.0
base_model: Qwen/Qwen-Image-Edit-2511
base_model_relation: adapter
library_name: diffusers
pipeline_tag: image-to-image
tags:
- lora
- qwen-image-edit
- character
- image-editing
---
# Mira BFS: Character Consistency LoRA for Qwen-Image-Edit-2511

An educational LoRA for **Mira character consistency across different input people and scenes**, trained for AiBook supplementary section P7-5.10. Face, hairstyle and illustration style are the learned identity cues. The concept was inspired by [BFS Head V5](https://huggingface.co/mr2along/BFS). This adapter was trained anew on Qwen-Image-Edit-2511; BFS weights were not used as initialization.

The intended edit changes the input person's face and hair into Mira's identity (including a teal bob) and renders the whole image in the target illustration style. The input expression, head direction, pose, clothing design, framing, props and scene layout should remain. These are training goals, not verified guarantees; visual quality review of this release is pending.

## AiBook manuscript

The supplementary lesson **P7-5.10: LoRA training and evaluation for character consistency** explains the LoRA purpose, the BFS-inspired concept, training-image generation, paired dataset construction, training, a planned evaluation on 19 held-out pairs, and completed generation on 45 independently generated synthetic inputs (15 each for a man, woman and toddler).

[Read the Korean lesson P7-5.10](https://devchan64.github.io/AiBook/parts/part-07/chapter-05/section-10).

## Quick start: download the trained adapter

You can try the trained adapter without generating a dataset or running training again. Download **mira_bfs.safetensors** (590,153,704 bytes; about 590 MB) and prepare the Qwen-Image-Edit-2511 base model and a GPU inference environment separately.

[Download the 366-pair dataset / 1600-step LoRA](https://huggingface.co/devchan64/mira-bfs-qwen-image-edit-2511-lora/resolve/main/mira_bfs.safetensors?download=true)

```bash
hf download devchan64/mira-bfs-qwen-image-edit-2511-lora mira_bfs.safetensors \
  --revision main \
  --local-dir ./mira-bfs
```

The main branch provides this release; verify the exact weights using the checksum. SHA-256: `9cddfaec307af146ce5311669c2e0ab42fdf68abe836364fa329e32861e9e37e`. The adapter has rank 16 and alpha 16; it is not a standalone model. See `SHA256SUMS` and `training-settings.json`.

**한국어 안내:** 이 LoRA는 BFS의 얼굴·헤어 편집을 참고하여 Mira의 얼굴·헤어·화풍을 일관되게 표현하도록 학습한 실습용 어댑터입니다. 학습을 다시 실행하지 않고 위 파일을 내려받아 사용할 수 있습니다. 입력 한 장만 전달하고, 출력의 캐릭터 특징과 입력 자세·표정·배경 보존을 따로 검수합니다. 이번 배포는 보강된 366쌍 중 347쌍으로 학습한 1600스텝 모델입니다. 외부 입력 45장 생성은 완료했으며 시각적 품질 판정은 아직 미확정입니다. 누적 3200스텝 재개 학습은 이번 가중치에 포함되지 않습니다. 자세한 학습 흐름은 위의 5.10 원고에서 안내합니다.

## Apply with Diffusers

The example follows the tested Diffusers 0.37.0 pipeline. The process-local VAE reference size override matches the 512-resolution training control. It is an internal API and should be checked before changing Diffusers versions. The vision-language condition retains its default 384 size.

```python
import torch
from PIL import Image
from diffusers import QwenImageEditPlusPipeline
from diffusers.pipelines.qwenimage import pipeline_qwenimage_edit_plus as pipeline_module

pipeline_module.VAE_IMAGE_SIZE = 512 ** 2
assert pipeline_module.CONDITION_IMAGE_SIZE == 384 ** 2
pipe = QwenImageEditPlusPipeline.from_pretrained(
    "Qwen/Qwen-Image-Edit-2511", torch_dtype=torch.bfloat16
)
pipe.load_lora_weights(
    "./mira-bfs",
    weight_name="mira_bfs.safetensors", adapter_name="mira"
)
pipe.set_adapters("mira", adapter_weights=1.0)
pipe.enable_sequential_cpu_offload()
pipe.vae.enable_slicing()
image = Image.open("input.png").convert("RGB")
assert image.size == (512, 512), "Use a square 512x512 input for this generation setup"
prompt = "Transform the person into mira_person with Mira's facial identity and hairstyle, and render the entire image in Mira's target illustration style. Preserve the input facial expression, head direction, pose, clothing design, camera viewpoint, perspective, framing, subject position, apparent body scale, background objects and scene layout."
with torch.inference_mode():
    result = pipe(
        image=[image], prompt=prompt, negative_prompt=" ",
        width=512, height=512, num_inference_steps=20,
        true_cfg_scale=4.0, guidance_scale=1.0,
        generator=torch.Generator(device="cuda").manual_seed(62294),
    ).images[0]
result.save("mira-output.png")
```

Only the input image is passed to the model. Do not provide the target portrait as an additional reference to reproduce this evaluation. GPU inference and the base model are required. The full evaluated base model is large; downloading the adapter alone does not supply its dependencies.

## Training data and settings

Synthetic paired edits: **366 accepted pairs**, split into **347 training and 19 held-out validation pairs**. There are 42 unique training targets and 4 validation targets (46 total). Variants of the same target remain in the same split. The original 193 pairs were supplemented with 173 accepted proportion inputs; torso targets reuse the existing section 5.2 direction images. The separate 123 target candidates are not in this training set.

Training used Musubi Tuner commit `e0cbd8f3dfe38365b10f8bc790b980f8894e8ba1`, resolution/control resolution 512, batch size 1, rank/alpha 16, learning rate 1e-4, **1600 total steps**, seed 62294, FP8 base/scaled processing and 55 swapped blocks. This is a new training run, not the former 193-pair adapter. A step uses one pair: 1600 steps is approximately 4.6 passes over 347 pairs, not 1600 steps per image.

Optimizer/resume state and base-model weights are not distributed here. A continuation restoring the final training state is in progress toward 3200 cumulative steps; those weights are **not included in this release**. See `training-settings.json` for the exact configuration and dataset checksum.

## Evaluation and limitations

All 45 external synthetic inputs were processed with this checkpoint. Input hashes do not overlap the training inputs. Only the input image was passed to the pipeline; no target face was supplied. Settings: LoRA strength 1.0, seed 62294, 20 inference steps, CFG 4.0, 512×512 output and VAE reference, 384×384 vision-language reference, no crop.

[Open the 45-input visual review table](evaluation/README.md). **Generation and file integrity are verified; visual quality judgments are pending.** Inspect Mira face, hair and illustration style separately from preservation of expression, pose, clothing, background and composition. Pay particular attention to head proportions at ±45° and ±90°. This table contains input and adapter output only; it does not establish an improvement over a no-adapter baseline. The 19 held-out pairs have not yet been evaluated with this new checkpoint.

Historical evaluation examples from the previous adapter have been removed from the current release. The previous checkpoint remains accessible through Git history.

## Sources and license

- [AiBook repository](https://github.com/devchan64/AiBook), P7-5.10 (Korean manuscript, dataset construction and detailed review).
- [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511), base model (model card declares Apache-2.0).
- [Musubi Tuner](https://github.com/kohya-ss/musubi-tuner), trainer.
- [BFS](https://huggingface.co/mr2along/BFS), concept inspiration.

This release is distributed under Apache-2.0. See LICENSE. No affiliation with or endorsement by Qwen or the BFS authors is implied.

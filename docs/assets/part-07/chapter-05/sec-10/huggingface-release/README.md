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

The intended edit changes the input person's face and hair into Mira's identity (including a teal bob) and renders the whole image in the target illustration style. The input expression, head direction, pose, clothing design, framing, props and scene layout should remain. These preservation goals are not fully achieved; see limitations below.

## AiBook manuscript

The supplementary lesson **P7-5.10: LoRA training and evaluation for character consistency** explains the LoRA purpose, the BFS-inspired concept, training-image generation, paired dataset construction, training, evaluation on 19 held-out pairs, and additional evaluation on 45 independently generated synthetic inputs (15 each for a man, woman and toddler).

[Read the Korean lesson P7-5.10](https://devchan64.github.io/AiBook/parts/part-07/chapter-05/section-10).

## Quick start: download the trained adapter

You can try the trained adapter without generating a dataset or running training again. Download **mira_bfs.safetensors** (590,153,704 bytes; about 590 MB) and prepare the Qwen-Image-Edit-2511 base model and a GPU inference environment separately.

[Download the evaluated 1600-step LoRA](https://huggingface.co/devchan64/mira-bfs-qwen-image-edit-2511-lora/resolve/83c28cc630d01f887c401769ab1504fdaa1447a6/mira_bfs.safetensors?download=true)

```bash
hf download devchan64/mira-bfs-qwen-image-edit-2511-lora mira_bfs.safetensors \
  --revision 83c28cc630d01f887c401769ab1504fdaa1447a6 \
  --local-dir ./mira-bfs
```

The pinned revision identifies the exact evaluated weights. SHA-256: `4606552aecbe5a50880c666ddc89a16138d7bd8e532255888712cb5daab794fb`. The adapter has rank 16 and alpha 16; it is not a standalone model. See `SHA256SUMS` and `training-settings.json`.

**한국어 안내:** 이 LoRA는 BFS의 얼굴·헤어 편집을 참고하여 Mira의 얼굴·헤어·화풍을 일관되게 표현하도록 학습한 실습용 어댑터입니다. 학습을 다시 실행하지 않고 위 파일을 내려받아 사용할 수 있습니다. 입력 한 장만 전달하고, 출력의 캐릭터 특징과 입력 자세·표정·배경 보존을 따로 검수합니다. 자세한 설명은 위의 5.10 원고 링크에서 제공할 예정이며, 현재 사이트 배포는 대기 중입니다.

## Apply with Diffusers

The example follows the tested Diffusers 0.37.0 pipeline. The process-local VAE reference size override is important: the default 1024 reference processing caused severe zoom/cropping in our initial 512-resolution evaluation. It is an internal API and should be checked before changing Diffusers versions. The vision-language condition retains its default 384 size.

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
assert image.size == (512, 512), "Use a square 512x512 input for this evaluated setup"
prompt = (
    "Transform the woman into mira_person with Mira's facial identity and hairstyle, "
    "and render the entire image in Mira's target illustration style. "
    "Preserve the input facial expression, head direction, pose, clothing design, "
    "camera viewpoint, perspective, framing, subject position, apparent body scale, "
    "background objects and scene layout."
)
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

Synthetic paired edits: 193 accepted input/target pairs, split into 174 training and 19 validation pairs. They use 41 unique Mira targets (37 training, 4 validation). Inputs were generated in five appearances/styles from existing Mira targets; training reverses that generation direction. Variants of the same target remain in the same split. The extra 123 target candidates are not in this training set.

Training used Musubi Tuner commit `e0cbd8f3dfe38365b10f8bc790b980f8894e8ba1`, resolution/control resolution 512, batch size 1, rank/alpha 16, learning rate 1e-4, 1600 steps, seed 62294, FP8 base/scaled processing and 55 swapped blocks. No optimizer/resume state or base-model weights are distributed here. Training settings are in `training-settings.json`.

## Evaluation

Previous evaluation assets and findings have been removed from this repository. Evaluate newly trained checkpoints separately; this published adapter predates the expanded 366-pair dataset.

## Sources and license

- [AiBook repository](https://github.com/devchan64/AiBook), P7-5.10 (Korean manuscript, dataset construction and detailed review).
- [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511), base model (model card declares Apache-2.0).
- [Musubi Tuner](https://github.com/kohya-ss/musubi-tuner), trainer.
- [BFS](https://huggingface.co/mr2along/BFS), concept inspiration.

This release is distributed under Apache-2.0. See LICENSE. No affiliation with or endorsement by Qwen or the BFS authors is implied.

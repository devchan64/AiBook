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

The intended edit changes the input person's face and hair into Mira's identity (including a teal bob) and renders the whole image in the target illustration style. The input expression, head direction, pose, clothing design, framing, props and scene layout should remain. These are training goals, not guarantees. The follow-up review compares 1600 and cumulative 3200 training steps and LoRA strengths 0.5, 0.75 and 1.0. The current experimental recommendation is **3200 steps / strength 0.75**; the downloadable adapter below remains the **1600-step** release.

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

**한국어 안내:** 현재 실험 권장값은 **누적 3200스텝·강도 0.75**입니다. 사용자 검수에서는 1600스텝의 홍채·이목구비 간 거리 차이가 3200스텝에서 거의 보이지 않았고, 강도 1.0보다 0.75에서 머리 방향 오류가 적다고 판단했습니다. 아래 샘플과 비교시트에 근거를 정리했습니다. **이 저장소에서 내려받는 가중치는 여전히 1600스텝 모델**이며, 이번 문서 업데이트에 3200스텝 가중치 배포는 포함되지 않습니다.

## Apply with Diffusers

This example reproduces the published **1600-step / strength 1.0** evaluation, not the 3200-step recommendation. Changing strength alone does not change the training checkpoint. The example follows the tested Diffusers 0.37.0 pipeline. The process-local VAE reference size override matches the 512-resolution training control. It is an internal API and should be checked before changing Diffusers versions. The vision-language condition retains its default 384 size.

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

Optimizer/resume state and base-model weights are not distributed here. A continuation restoring the final training state completed another 1600 steps, reaching **3200 cumulative steps**; those weights are **not included in this release**. This resumed run is not assumed numerically identical to an uninterrupted 3200-step run. See `training-settings.json` for the exact configuration and dataset checksum.

## Evaluation and current recommendation

**Current experimental recommendation: cumulative 3200 training steps, LoRA strength 0.75.** This is a qualitative selection for this experiment, not a measured error rate or a universal optimum.

| Criterion | Review finding | Decision |
| --- | --- | --- |
| Mira facial identity | User review found iris and facial-feature spacing differences at 1600 steps, with almost no such errors visible at 3200 steps. | Prefer cumulative 3200 steps. |
| Head direction | User review found more head-direction errors at strength 1.0 than at 0.75. | Prefer strength 0.75. |
| Clothing, hands, gaze and proportions | Existing AI per-case observations still record preservation errors. | Review separately from facial identity. |

The earlier assessment that face and hair were generally consistent is retained as historical context; the follow-up checks examine finer facial details. AI observations and the user's final setting preference are distinguished in the detailed records.

### Comparison sheets / 결과 검수 비교시트

- [Review summary and case guide / 검수 요약](evaluation/README.md)
- [45 inputs: 1600 vs 3200 steps at strength 1.0 / 스텝 비교](evaluation/step-review.md)
- [12 selected inputs: no adapter and strengths 0.5, 0.75, 1.0 / 강도 비교](evaluation/scale-review.md)

Each detailed case includes the input, a direction-matched **Mira torso reference**, outputs and Korean review notes. The Mira image is a visual identity/style reference only; it was **not passed to the inference pipeline**. Clothing, pose and scene preservation must be judged against the input, not against the Mira torso.

### Illustrated samples / 설명을 곁들인 샘플

Compare the input and Mira reference first, then compare the outputs at the same strength. These examples illustrate both the intended transformation and remaining errors.

#### 006: Side-view preservation / 측면 방향 보존

| Input / 입력 | Mira reference / 참조 |
| --- | --- |
| ![P712-CAM-006 입력](evaluation/images/6942052db445d4ba.png) | ![Mira 토르소 참조 · level / -90°](evaluation/images/34889d61da4dfff6.png) |

| 1600 steps · strength 0.75 | 3200 steps · strength 0.75 |
| --- | --- |
| ![P712-CAM-006 1600 · 0.75](evaluation/images/e4112b98ef581c4d.png) | ![P712-CAM-006 3200 · 0.75](evaluation/images/e105de20a0fcbf74.png) |

At 3200 steps, strength 1.0 turns the face toward the front and reduces subject size. Strength 0.75 better retains the side view, but head/body scale still differs from the input. / 3200스텝의 강도 1.0에서 보인 정면 회전은 0.75에서 완화되지만 크기·비율 차이는 남습니다.

<details>
<summary>Compare 3200-step strength 1.0 / 강도 1.0 결과 펼치기</summary>

![P712-CAM-006 3200 · 1.0](evaluation/images/64d68bd56b0617e0.png)

</details>

#### 009: Collar preservation / 셔츠 칼라 보존

| Input / 입력 | Mira reference / 참조 |
| --- | --- |
| ![P712-CAM-009 입력](evaluation/images/d2bc2b5784186387.png) | ![Mira 토르소 참조 · level / 45°](evaluation/images/8a1e341703b2b2ff.png) |

| 1600 steps · strength 0.75 | 3200 steps · strength 0.75 |
| --- | --- |
| ![P712-CAM-009 1600 · 0.75](evaluation/images/531a294269170da4.png) | ![P712-CAM-009 3200 · 0.75](evaluation/images/ca7c72541e02e002.png) |

The 1600-step strength-1.0 output loses the collar; the 0.75 outputs retain it. Face direction, body and hand proportions still differ. / 얼굴 변환과 칼라 보존을 따로 확인합니다. 강도 0.75에서도 방향·손·몸 비율 변화는 남습니다.

<details>
<summary>Compare 3200-step strength 1.0 / 강도 1.0 결과 펼치기</summary>

![P712-CAM-009 3200 · 1.0](evaluation/images/8e4ebd5b13d25cb2.png)

</details>

<details>
<summary>Evaluation conditions and limitations / 검수 조건과 한계 펼치기</summary>

The 45 external synthetic inputs (15 each for man, woman and toddler) are separate from the 19 held-out validation pairs. Input hashes do not overlap the training inputs. Comparing both checkpoints at strength 1.0 gives 90 outputs. The strength experiment selected 12 of those inputs to examine preservation issues: 12 no-adapter outputs plus 48 new outputs at strengths 0.5/0.75 and 24 reused strength-1.0 outputs, for 84 compared outputs.

Settings: seed 62294, 20 inference steps, CFG 4.0, 512×512 output and VAE reference, 384×384 vision-language reference, no crop. Only the input image is passed to the pipeline. Generation and file integrity were checked. The selected 12 inputs are not an independent test set; this single-seed qualitative comparison does not establish general performance or overfitting. The 19 held-out pairs have not yet been evaluated with this checkpoint.

The cumulative 3200-step comparison checkpoint has SHA-256 `3614fd3e83d9f99408cab412ff678a82c5b8a8700e2d5e731507de5b2ee75cc5`. This identifies the experimental checkpoint, not the downloadable 1600-step file.

</details>

## Sources and license

- [AiBook repository](https://github.com/devchan64/AiBook), P7-5.10 (Korean manuscript, dataset construction and detailed review).
- [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511), base model (model card declares Apache-2.0).
- [Musubi Tuner](https://github.com/kohya-ss/musubi-tuner), trainer.
- [BFS](https://huggingface.co/mr2along/BFS), concept inspiration.

This release is distributed under Apache-2.0. See LICENSE. No affiliation with or endorsement by Qwen or the BFS authors is implied.

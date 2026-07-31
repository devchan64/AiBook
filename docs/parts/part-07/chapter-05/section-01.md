# P7-5.1 diffusers로 Stable Diffusion과 LoRA 조건 고정하기

> Section ID: `P7-5.1`
> Version: `v2026.07.31`

Stable Diffusion과 LoRA를 처음 조합할 때는 먼저 조건을 고정해야 합니다. 이 절에서는 `huggingface/diffusers`를 사용해 `base_model`, `lora_adapter`, `adapter_weight`, `prompt`, `seed`, `output_file`을 명시적으로 남깁니다.

목표는 좋은 이미지 한 장을 뽑는 것이 아닙니다. 같은 prompt와 seed에서 LoRA를 쓰지 않은 결과, LoRA를 약하게 얹은 결과, LoRA를 강하게 얹은 결과를 나란히 비교하는 것입니다. 그래야 `LoRA가 스타일을 바꿨다`는 말을 감상으로만 쓰지 않고, 다시 실행할 수 있는 비교 기록으로 남길 수 있습니다.

외부 자료를 보면 Stable Diffusion 생태계에서는 Web UI와 ComfyUI처럼 별도 화면을 제공하는 대형 저장소가 널리 쓰입니다. 그럼에도 이 절을 `diffusers`로 시작하는 이유는 조건 고정이 가장 잘 드러나기 때문입니다. 초심자는 먼저 코드에서 바뀌는 값을 하나로 줄여 보고, 다음 절에서 같은 조합을 workflow 화면으로 옮겨 보는 편이 안전합니다.

## 고정값과 변경값이 만드는 비교

- Stable Diffusion base 모델과 LoRA adapter를 어떻게 구분해 기록할 것인가?
- prompt와 seed를 고정한 상태에서 adapter weight만 바꾸면 무엇이 보이는가?
- 생성 결과를 `좋다/나쁘다`가 아니라 `base 대비 바뀐 점`, `과하게 바뀐 점`, `다음 조정값`으로 어떻게 적을 것인가?

핵심은 `Stable Diffusion을 실행했다`가 아니라, `어떤 조합을 비교했는가`입니다. 생성형 모델은 같은 문장을 넣어도 설정과 난수 seed에 따라 결과가 달라집니다. 따라서 첫 실습에서는 바꿀 값을 하나로 줄여야 합니다.

## 준비할 것

`diffusers` 실습은 코드로 기록을 남기기 좋지만, 실행 환경 준비가 필요합니다.

| 준비할 것 | 확인할 내용 |
| --- | --- |
| GPU 실행 환경 | CUDA 또는 호환 가능한 가속 환경이 있는가 |
| Python 패키지 | `torch`, `diffusers`, `transformers`, `accelerate`, `safetensors`를 설치했는가 |
| 모델 접근 권한 | 사용할 base 모델과 LoRA의 라이선스와 접근 조건을 확인했는가 |
| 저장 위치 | 생성 이미지와 실행 기록을 어디에 저장할지 정했는가 |

이 절에서는 설치 절차 자체를 길게 다루지 않습니다. 설치는 바뀔 수 있으므로 공식 문서를 확인하고, 본문에서는 실험 조건을 어떻게 고정하고 읽을지만 다룹니다.

## Python 예제

다음 예제는 Stable Diffusion XL base 모델을 열고, 공개 LoRA adapter를 얹은 뒤 adapter weight를 바꿔 이미지를 저장하는 형태입니다.

```python
from pathlib import Path

import torch
from diffusers import AutoPipelineForText2Image

output_dir = Path("outputs/p7-5-1-lora")
output_dir.mkdir(parents=True, exist_ok=True)

base_model = "stabilityai/stable-diffusion-xl-base-1.0"
lora_repo = "ostris/super-cereal-sdxl-lora"
lora_weight_name = "cereal_box_sdxl_v1.safetensors"
adapter_name = "cereal"

prompt = "a small robot assistant printed on a colorful cereal box, product photo"
negative_prompt = "blurry, low quality, distorted text"
seed = 42

pipeline = AutoPipelineForText2Image.from_pretrained(
    base_model,
    torch_dtype=torch.float16,
).to("cuda")

pipeline.load_lora_weights(
    lora_repo,
    weight_name=lora_weight_name,
    adapter_name=adapter_name,
)

experiment_rows = []

for adapter_weight in [0.0, 0.5, 1.0]:
    pipeline.set_adapters(adapter_name, adapter_weights=adapter_weight)
    generator = torch.Generator(device="cuda").manual_seed(seed)

    image = pipeline(
        prompt=prompt,
        negative_prompt=negative_prompt,
        generator=generator,
        num_inference_steps=30,
        guidance_scale=7.0,
    ).images[0]

    output_file = output_dir / f"robot-cereal-lora-{adapter_weight:.1f}.png"
    image.save(output_file)

    experiment_rows.append(
        {
            "base_model": base_model,
            "lora_adapter": f"{lora_repo}/{lora_weight_name}",
            "adapter_weight": adapter_weight,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "seed": seed,
            "output_file": str(output_file),
        }
    )

for row in experiment_rows:
    print(row)
```

이 코드에서 일부러 고정한 값과 바꾼 값은 분리해서 읽어야 합니다.

| 구분 | 값 | 이유 |
| --- | --- | --- |
| 고정 | `base_model` | 기준 모델이 바뀌면 비교가 다른 실험이 됩니다. |
| 고정 | `lora_repo`, `lora_weight_name` | 어떤 LoRA를 얹었는지 추적하기 위해 필요합니다. |
| 고정 | `prompt`, `negative_prompt` | 문장이 바뀌면 LoRA weight 효과와 prompt 효과가 섞입니다. |
| 고정 | `seed` | 난수 차이를 줄이고 weight 차이를 먼저 보기 위해 필요합니다. |
| 변경 | `adapter_weight` | LoRA 영향 강도만 바꾸어 결과 차이를 읽습니다. |

## 결과를 읽는 법

실행 뒤에는 세 이미지를 나란히 놓고 다음처럼 읽습니다.

| 비교 | 읽어야 할 질문 |
| --- | --- |
| `adapter_weight=0.0` | base 모델만 쓴 기준 결과가 무엇인가 |
| `adapter_weight=0.5` | LoRA 특징이 들어오되 prompt의 원래 대상이 유지되는가 |
| `adapter_weight=1.0` | LoRA 특징이 너무 강해져 대상, 구도, 글자 품질이 무너지는가 |

기록은 다음처럼 남깁니다.

```text
run_id: diffusers-lora-weight-001
base_model:
lora_adapter:
fixed_prompt:
fixed_seed:
changed_value: adapter_weight = 0.0 / 0.5 / 1.0
observed_change:
next_trial:
```

`observed_change`에는 감상보다 비교를 씁니다. 예를 들어 `0.5에서는 cereal box 스타일이 보이지만 robot 형태가 유지됨`, `1.0에서는 포장지 질감은 강해졌지만 글자와 얼굴이 흐려짐`처럼 base 대비 바뀐 점과 과해진 점을 나눕니다.

## 직접 바꿔 보며 확인할 것

1. `adapter_weight`를 `0.2`, `0.6`, `1.0`으로 바꿔 봅니다.
   관찰할 점: 어느 지점부터 LoRA 특징이 분명해지고, 어느 지점부터 prompt의 대상이 흐려지는가?

2. seed를 `42`, `43`, `44`로 바꿔 봅니다.
   관찰할 점: 특정 seed에서만 좋아 보이는 결과인지, 여러 seed에서 반복되는 변화인지 구분할 수 있는가?

3. 같은 LoRA로 prompt의 대상만 바꿔 봅니다.
   관찰할 점: LoRA가 스타일만 옮기는지, 특정 대상까지 강하게 끌고 가는지 확인할 수 있는가?

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 기준 모델 | base 모델 ID를 기록했는가? |
| LoRA adapter | LoRA 저장소, 파일명, adapter 이름을 남겼는가? |
| 비교 조건 | prompt와 seed를 고정한 상태에서 adapter weight만 바꿨는가? |
| 결과 해석 | base 대비 바뀐 점과 과하게 바뀐 점을 분리했는가? |
| 다음 실험 | 다음에 바꿀 값이 prompt인지, weight인지, seed인지 적었는가? |

## 출처와 참고 자료

- Hugging Face, [diffusers GitHub 저장소](https://github.com/huggingface/diffusers){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- Hugging Face, [Diffusers LoRA 문서](https://huggingface.co/docs/diffusers/tutorials/using_peft_for_inference){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.

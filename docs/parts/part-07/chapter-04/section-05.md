# P7-4.5 Stable Diffusion과 LoRA 조합 실습

> Section ID: `P7-4.5`
> Version: `v2026.07.31`

Stable Diffusion과 LoRA를 함께 쓸 때는 `base_model`, `lora_adapter`, `adapter_weight`, `prompt`, `seed`, `output_review`를 나누어 둡니다. 생성형 이미지 실습도 결과 이미지 한 장으로 끝내지 않고, 어떤 기준 모델에 어떤 작은 적응 가중치를 얹었는지 기록하기 위한 기준입니다.

여기서 목표는 멋진 이미지를 한 번 뽑는 것이 아닙니다. 같은 prompt와 seed를 고정한 뒤, LoRA를 쓰지 않은 결과와 LoRA를 얹은 결과, LoRA 가중치를 약하게 준 결과와 강하게 준 결과를 나란히 비교하는 것입니다. 그렇게 해야 `LoRA가 스타일을 바꿨다`는 말을 감상으로만 쓰지 않고, 재현 가능한 실습 기록으로 남길 수 있습니다.

LoRA는 전체 Stable Diffusion 모델을 새로 학습하는 대신, 작은 추가 가중치를 붙여 특정 스타일이나 개념을 빠르게 반영하는 방식입니다. 따라서 Part 7에서는 LoRA 자체의 수학을 깊게 파기보다, `기준 모델은 그대로 두고 작은 adapter를 바꾸면 출력과 실패 양상이 어떻게 달라지는가`를 확인합니다.

## 기준 모델과 LoRA가 가르는 질문

- 같은 prompt에서 base 모델만 쓴 결과와 LoRA를 얹은 결과는 어떻게 다른가?
- LoRA 가중치를 `0.0`, `0.5`, `1.0`처럼 바꾸면 어떤 변화가 커지는가?
- 결과가 좋아 보이더라도 prompt, seed, 모델 ID, LoRA 파일명을 남기지 않으면 왜 다시 확인하기 어려운가?

핵심은 `Stable Diffusion을 실행했다`가 아니라, `어떤 조합을 비교했는가`입니다. 생성형 모델은 같은 문장을 넣어도 설정과 난수 seed에 따라 결과가 달라집니다. 그래서 실습 기록에는 prompt보다 먼저 base 모델, LoRA adapter, adapter weight, seed가 같이 남아야 합니다.

## 저장소 후보와 역할

Stable Diffusion과 LoRA 조합 실습에는 다음 GitHub 저장소를 후보로 볼 수 있습니다.

| 저장소 | 실습에 맞는 역할 | Part 7에서의 위치 |
| --- | --- | --- |
| `huggingface/diffusers` | Python 코드로 base 모델, LoRA 로딩, adapter weight를 명시적으로 기록하기 좋다 | 기본 실습 |
| `AUTOMATIC1111/stable-diffusion-webui` | 웹 UI에서 LoRA 파일을 넣고 prompt 안에 `<lora:파일명:가중치>` 형식으로 빠르게 비교하기 좋다 | 선택 실습 |
| `Comfy-Org/ComfyUI` | 노드 그래프로 checkpoint, LoRA, prompt, sampler 흐름을 눈으로 연결하기 좋다 | 워크플로우 시각화 확장 |
| `bmaltais/kohya_ss` | 직접 LoRA를 학습하는 GUI와 CLI를 제공한다 | 후속 확장 실습 |

초심자 기준의 첫 실습은 `huggingface/diffusers`가 가장 안전합니다. 코드 안에 `base_model`, `lora_adapter`, `adapter_weight`, `seed`를 그대로 남길 수 있기 때문입니다. `AUTOMATIC1111`과 `ComfyUI`는 실제 이미지 제작 흐름에서는 편하지만, 책의 Part 7 기준으로는 설정을 따로 문서화하지 않으면 어떤 조합을 비교했는지 흐려지기 쉽습니다. `kohya_ss`는 LoRA를 직접 학습하고 싶을 때 필요하지만, 첫 절에서 바로 학습까지 들어가면 데이터 준비, caption, 반복 횟수, GPU 메모리 문제가 실습의 중심을 빼앗을 수 있습니다.

## 판단 기준

- Stable Diffusion base 모델과 LoRA adapter를 구분해 적을 수 있습니다.
- LoRA 가중치를 바꾸는 실험에서 prompt와 seed를 고정해야 하는 이유를 설명할 수 있습니다.
- 생성 결과를 `좋다/나쁘다`가 아니라 `base 대비 바뀐 점`, `과하게 바뀐 점`, `다음 조정값`으로 기록할 수 있습니다.

## 실습 기록 표

먼저 결과를 저장할 표의 열을 정합니다. 이미지를 만들기 전에 기록 형식을 먼저 잡아야, 생성 결과가 나온 뒤 감상문으로 흘러가지 않습니다.

| 열 | 남길 내용 |
| --- | --- |
| `run_id` | 실행 번호 |
| `base_model` | 기준 Stable Diffusion 모델 ID |
| `lora_adapter` | LoRA 저장소 또는 파일명 |
| `adapter_weight` | LoRA 적용 강도 |
| `prompt` | 고정한 prompt |
| `negative_prompt` | 제외하고 싶은 요소 |
| `seed` | 난수 seed |
| `output_file` | 저장한 이미지 파일명 |
| `review_note` | base 대비 바뀐 점과 실패 |
| `next_trial` | 다음에 바꿀 값 |

이 표에서 `prompt`만 길게 남기고 모델과 seed를 빼면 다시 실행하기 어렵습니다. 반대로 `base_model`, `lora_adapter`, `adapter_weight`, `seed`가 같이 있으면 결과 이미지를 보지 않는 사람도 어떤 비교였는지 추적할 수 있습니다.

## Python 예제

다음 예제는 `diffusers`로 Stable Diffusion XL base 모델을 열고, 공개 LoRA adapter를 얹은 뒤 adapter weight를 바꿔 이미지를 저장하는 형태입니다. 실제 실행에는 GPU, PyTorch, diffusers 설치, 모델 다운로드 권한, 모델별 라이선스 확인이 필요합니다. 이 절의 핵심은 실행 환경 설치가 아니라, LoRA 조합 실험을 어떤 기록 단위로 남길지입니다.

```python
from pathlib import Path

import torch
from diffusers import AutoPipelineForText2Image

output_dir = Path("outputs/p7-4-5-lora")
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

실행 뒤에는 세 이미지를 나란히 놓고 다음처럼 읽습니다.

| 비교 | 읽어야 할 질문 |
| --- | --- |
| `adapter_weight=0.0` | base 모델만 쓴 기준 결과가 무엇인가 |
| `adapter_weight=0.5` | LoRA 스타일이 들어오되 prompt의 원래 대상이 유지되는가 |
| `adapter_weight=1.0` | LoRA 특징이 너무 강해져 대상, 구도, 글자 품질이 무너지는가 |

## 결과 해석 기준

이미지 생성 실습의 실패는 분류 실습의 오답과 모양이 다릅니다. 정답 라벨이 없기 때문에, 평가 문장을 먼저 정해야 합니다.

| 관찰 | 회고 문장 |
| --- | --- |
| LoRA를 켜도 거의 차이가 없다 | adapter weight가 낮거나 prompt가 LoRA의 trigger와 잘 맞지 않을 수 있다 |
| LoRA 특징이 너무 강하다 | adapter weight를 낮추고 prompt에서 핵심 대상 표현을 더 분명히 한다 |
| seed를 바꿀 때마다 판단이 흔들린다 | seed 여러 개를 작은 평가셋처럼 보고 공통 실패를 따로 적는다 |
| 스타일은 맞지만 대상이 흐려진다 | style adapter와 subject prompt가 서로 충돌하는지 확인한다 |

여기서 좋은 기록은 `1.0이 제일 예쁘다`가 아닙니다. 예를 들어 다음처럼 적어야 다시 실행할 수 있습니다.

```text
base_model:
lora_adapter:
adapter_weight:
prompt:
negative_prompt:
seed:
base 대비 바뀐 점:
과하게 바뀐 점:
다음 조정값:
```

## 직접 바꿔 보며 확인할 것

1. `adapter_weight`를 `0.2`, `0.6`, `1.0`으로 바꿔 봅니다.
   관찰할 점: 어느 지점부터 LoRA 특징이 분명해지고, 어느 지점부터 prompt의 대상이 흐려지는가?

2. seed를 `42`, `43`, `44`로 바꿔 봅니다.
   관찰할 점: 특정 seed에서만 좋아 보이는 결과인지, 여러 seed에서 반복되는 변화인지 구분할 수 있는가?

3. 같은 LoRA로 prompt의 대상만 바꿔 봅니다.
   관찰할 점: LoRA가 스타일만 옮기는지, 특정 대상까지 강하게 끌고 가는지 확인할 수 있는가?

4. `kohya_ss` 문서를 열어 직접 LoRA 학습 항목을 확인해 봅니다.
   관찰할 점: 직접 학습으로 넘어가려면 이미지 수, caption 규칙, 반복 횟수, 검토 이미지 저장 규칙을 추가로 정해야 한다는 점이 보이는가?

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
- AUTOMATIC1111, [Stable Diffusion web UI Features - Extra networks와 LoRA](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- Comfy-Org, [ComfyUI GitHub 저장소](https://github.com/comfy-org/ComfyUI){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- bmaltais, [kohya_ss GitHub 저장소](https://github.com/bmaltais/kohya_ss){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.

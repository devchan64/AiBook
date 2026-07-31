# P7-5.2 ComfyUI workflow로 LoRA, ControlNet, IP-Adapter 조합 보기

> Section ID: `P7-5.2`
> Version: `v2026.07.31`

diffusers 실습이 코드로 조건을 고정하는 연습이라면, ComfyUI 실습은 모델 조합을 눈으로 보는 연습입니다. 이 절에서는 LoRA, ControlNet, IP-Adapter가 각각 어떤 입력을 맡는지 workflow 단위로 확인합니다.

목표는 더 많은 모델을 붙이는 것이 아닙니다. checkpoint가 기본 생성을 맡고, LoRA가 스타일이나 개념을 보강하고, ControlNet이 구조를 잡고, IP-Adapter가 참조 이미지를 반영한다는 역할 분담을 실제 workflow에서 읽는 것입니다.

## 노드 그래프가 보여 주는 역할 분담

- checkpoint, LoRA, ControlNet, IP-Adapter는 각각 무엇을 조절하는가?
- 여러 모델을 동시에 켰을 때 결과가 좋아지는가, 아니면 서로 밀어내는가?
- workflow 파일명, 모델 파일명, 입력 이미지, 바꾼 노드 값을 어떻게 남겨야 다시 확인할 수 있는가?

ComfyUI workflow는 이미지 생성 과정을 노드로 보여 줍니다. 초심자에게 중요한 점은 모든 노드 이름을 외우는 것이 아니라, 어떤 입력이 어느 모델을 거쳐 결과 이미지에 영향을 주는지 따라가는 것입니다.

## 사용할 workflow 후보

처음부터 복잡한 custom node workflow로 들어가기보다, 예제가 정리된 저장소를 먼저 엽니다.

| 저장소 | 먼저 볼 것 | 이 절에서의 역할 |
| --- | --- | --- |
| `Comfy-Org/ComfyUI` | 기본 설치와 workflow 저장 방식 | 노드 기반 조합 실습의 중심 도구 |
| `comfyanonymous/ComfyUI_examples` | `lora`, `controlnet`, `sdxl`, `model_merging` | ComfyUI 기본 예제 구조 |
| `pwillia7/Basic_ComfyUI_Workflows` | `txt2img LORA`, `img2img LORA`, `Controlnet Multi`, `IPAdapter + Controlnet` | 초심자용 조합 workflow |
| `comfyorg/comfyui-ipadapter` | examples directory | 참조 이미지 기반 스타일과 구도 반영 |

workflow를 열 때는 결과 이미지보다 노드 이름과 연결선을 먼저 봅니다. 특히 checkpoint loader, LoRA loader, ControlNet loader, IP-Adapter loader가 어디에 있고, 어떤 입력 이미지나 prompt와 연결되는지 확인합니다.

## 규모가 큰 저장소를 어떻게 볼 것인가

스타와 포크가 많은 저장소는 실습 후보를 고를 때 좋은 신호입니다. 사용자가 많으면 예제, 이슈, 확장, 오류 해결 기록도 함께 쌓이기 때문입니다. 다만 Part 7의 목적은 `가장 인기 있는 도구를 모두 설치하기`가 아니라, 모델 조합을 읽고 기록하는 것입니다.

| 우선 검토 저장소 | 규모 신호 | 이 절에서의 판단 |
| --- | --- | --- |
| `AUTOMATIC1111/stable-diffusion-webui` | 약 163k stars, 30.4k forks | 대중적인 실행 환경 비교 후보입니다. LoRA 사용 형식과 확장 생태계를 확인하되, 이 절의 주 실습은 workflow 기록이 쉬운 ComfyUI로 둡니다. |
| `Comfy-Org/ComfyUI` | 약 121k stars, 14.2k forks | 이 절의 중심 도구입니다. checkpoint, LoRA, ControlNet, IP-Adapter의 연결을 눈으로 추적하기 좋습니다. |
| `lllyasviel/ControlNet` | 약 33.9k stars, 3k forks | ControlNet이 왜 `구조 제어`로 설명되는지 확인하는 기준 자료로 사용합니다. |
| `Mikubill/sd-webui-controlnet` | 약 17.8k stars, 2.0k forks | Web UI 경로를 택한 독자가 ControlNet 조합을 실습할 때 참고할 보조 후보입니다. |
| `cubiq/ComfyUI_IPAdapter_plus` | 약 6k stars, 465 forks | 참조 이미지 기반 조합을 넓혀 볼 때 참고하되, 유지보수 상태를 확인하고 사용합니다. |
| `pwillia7/Basic_ComfyUI_Workflows` | 약 427 stars, 19 forks | 규모는 작지만 `txt2img LORA`, `Controlnet Multi`, `IPAdapter + Controlnet`처럼 초심자용 workflow 이름이 바로 드러나므로 예제 탐색 후보로 둡니다. |

위 숫자는 2026-07-31에 GitHub 페이지에서 확인한 대략적 규모입니다. 숫자는 바뀔 수 있으므로, 이 표는 순위를 고정하려는 용도가 아니라 `어떤 저장소를 먼저 열어 볼지` 정하는 신호로만 사용합니다. 따라서 이 절의 실습 판단은 `대형 저장소를 우선 검토하되, 초심자 실습 산출물은 workflow 파일, 모델 파일명, 입력 이미지, 바꾼 노드 값으로 남길 수 있는가`에 맞춥니다. Web UI는 널리 쓰이는 대안이고, ComfyUI는 조합 구조를 읽기 좋은 학습 도구입니다.

## 모델별 기록 기준

ComfyUI workflow에서는 보통 다음 역할이 나뉩니다.

| 모델 또는 노드 | 맡는 역할 | 기록할 질문 |
| --- | --- | --- |
| checkpoint | 기본 이미지 생성 모델 | 어떤 base 모델이 전체 화풍과 기본 능력을 만드는가 |
| LoRA | 특정 스타일, 인물, 물체, 질감 보강 | 어떤 개념이 어느 강도로 추가되는가 |
| ControlNet | pose, depth, edge 같은 구조 제어 | 결과가 입력 구조를 얼마나 따르는가 |
| IP-Adapter | 참조 이미지의 스타일이나 구도 반영 | 참조 이미지가 색감, 형태, 분위기 중 무엇을 끌고 오는가 |
| sampler / scheduler | 노이즈를 줄이는 생성 절차 | steps와 sampler가 결과 안정성을 어떻게 바꾸는가 |

이 표를 workflow 옆에 두고 보면, 모델 조합이 단순히 `많이 연결한 것`이 아니라 서로 다른 제어 신호를 합치는 일이라는 점이 보입니다.

## 실습 순서

1. `txt2img LORA` workflow를 열어 checkpoint와 LoRA 노드만 확인합니다.
2. 같은 prompt에서 LoRA 강도를 낮음, 중간, 높음으로 바꿉니다.
3. `IPAdapter + Controlnet` workflow를 열어 입력 이미지가 두 갈래로 쓰이는지 확인합니다.
4. ControlNet 입력은 구조를, IP-Adapter 입력은 스타일이나 참조 이미지를 맡는지 결과를 나누어 봅니다.
5. workflow 파일명, 사용한 모델 파일명, 입력 이미지, 바꾼 노드 값을 기록합니다.

2단계 diffusers 실습과 달리, 여기서는 코드보다 workflow 파일 자체가 중요한 산출물입니다. 가능한 한 변경한 workflow를 저장하고, 결과 이미지와 함께 묶어 둡니다.

## workflow 기록 양식

```text
workflow_name:
checkpoint:
lora_name:
lora_strength:
controlnet_model:
control_image:
ip_adapter_model:
reference_image:
changed_node:
output_review:
```

`changed_node`에는 `LoRA strength`, `ControlNet conditioning scale`, `IP-Adapter scale`, `sampler steps`처럼 실제로 바꾼 값을 씁니다. `output_review`에는 어느 모델의 영향이 강해졌는지 씁니다.

## 조합 충돌 읽기

이 단계에서 중요한 실패는 `이미지가 마음에 안 든다`가 아닙니다. 더 중요한 실패는 역할 충돌입니다. 예를 들어 ControlNet은 자세를 강하게 고정하려 하고, IP-Adapter는 참조 이미지의 구도를 따라가려 하며, LoRA는 특정 스타일을 밀어붙일 수 있습니다. 세 신호가 동시에 강하면 결과가 뻣뻣해지거나 prompt의 대상이 흐려질 수 있습니다.

| 관찰 질문 | 해석 |
| --- | --- |
| ControlNet을 끄면 구도가 얼마나 달라지는가 | 구조 제어가 실제로 작동하는지 확인합니다. |
| IP-Adapter scale을 낮추면 참조 이미지 영향이 줄어드는가 | 스타일 또는 참조 이미지 영향이 과한지 봅니다. |
| LoRA strength를 낮추면 대상이 더 또렷해지는가 | LoRA가 스타일보다 대상을 잡아먹고 있는지 봅니다. |
| 세 모델을 모두 켰을 때만 깨지는가 | 단일 모델 문제가 아니라 조합 충돌일 수 있습니다. |

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| workflow 파일 | 어떤 workflow를 열었는지 남겼는가? |
| 모델 역할 | checkpoint, LoRA, ControlNet, IP-Adapter 역할을 구분했는가? |
| 입력 이미지 | ControlNet 이미지와 IP-Adapter 참조 이미지를 따로 기록했는가? |
| 변경 노드 | 어떤 노드의 어떤 값을 바꿨는가? |
| 충돌 해석 | 결과 실패를 모델별 역할 충돌로 다시 읽었는가? |

## 출처와 참고 자료

- Comfy-Org, [ComfyUI GitHub 저장소](https://github.com/Comfy-Org/ComfyUI){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- comfyanonymous, [ComfyUI_examples GitHub 저장소](https://github.com/comfyanonymous/ComfyUI_examples){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- pwillia7, [Basic_ComfyUI_Workflows GitHub 저장소](https://github.com/pwillia7/Basic_ComfyUI_Workflows){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- comfyorg, [comfyui-ipadapter GitHub 저장소](https://github.com/comfyorg/comfyui-ipadapter){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- AUTOMATIC1111, [stable-diffusion-webui GitHub 저장소](https://github.com/AUTOMATIC1111/stable-diffusion-webui){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- lllyasviel, [ControlNet GitHub 저장소](https://github.com/lllyasviel/ControlNet){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- Mikubill, [sd-webui-controlnet GitHub 저장소](https://github.com/Mikubill/sd-webui-controlnet){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- cubiq, [ComfyUI_IPAdapter_plus GitHub 저장소](https://github.com/cubiq/ComfyUI_IPAdapter_plus){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.

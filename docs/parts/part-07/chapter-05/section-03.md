# P7-5.3 kohya_ss로 직접 LoRA 학습 확장하기

> Section ID: `P7-5.3`
> Version: `v2026.07.31`

앞의 두 절은 이미 있는 LoRA를 불러와 조합하는 실습이었습니다. 이 절은 작은 이미지셋으로 직접 LoRA를 학습하는 확장 실습입니다. 여기서는 생성 버튼보다 데이터 준비, caption 규칙, sample image 검토 기록이 더 중요합니다.

LoRA를 직접 학습하면 특정 스타일, 물체, 복장, 질감을 base 모델에 더 강하게 연결할 수 있습니다. 하지만 데이터셋과 caption 규칙이 흐리면 결과가 왜 달라졌는지 설명하기 어렵습니다. 따라서 이 절에서는 `학습했다`보다 `무엇을 학습시키려 했고, 어떤 실패를 보았고, 다음 데이터셋을 어떻게 고칠 것인가`를 기록합니다.

## 직접 학습 전에 정해야 할 것

- LoRA가 배워야 할 대상은 스타일인가, 물체인가, 인물인가, 질감인가?
- caption은 trigger token과 장면 설명을 어떻게 나눌 것인가?
- sample prompt를 어떻게 고정해 학습 중간 결과를 비교할 것인가?

직접 LoRA 학습은 생성 실습이 아니라 데이터 준비 실습에 가깝습니다. 적은 이미지로 시작할 수는 있지만, 이미지셋과 caption 규칙을 먼저 정하지 않으면 과적합과 학습 부족을 구분하기 어렵습니다.

## 학습 설계 표

직접 학습으로 넘어가기 전에 다음 표를 먼저 채웁니다.

| 항목 | 예시 기록 | 왜 필요한가 |
| --- | --- | --- |
| 학습 목표 | 특정 물체 스타일, 제품 질감, 캐릭터 복장 | LoRA가 무엇을 배워야 하는지 정합니다. |
| 이미지 수 | 15장, 30장, 50장 | 데이터가 너무 적거나 반복적이면 과적합을 의심해야 합니다. |
| caption 규칙 | 공통 trigger token, 장면 설명, 제외할 배경 | prompt와 학습 신호를 연결합니다. |
| 반복 횟수 | epoch, steps, save interval | 어느 시점의 LoRA가 가장 안정적인지 비교합니다. |
| sample prompt | 학습 중 같은 prompt로 저장 | 학습 진행에 따른 변화와 붕괴를 봅니다. |
| 검토 기준 | 닮음, 과적합, 다양성, prompt 반응 | 결과를 감상 대신 평가 기준으로 읽습니다. |

`kohya_ss`는 이 과정을 GUI와 CLI로 돕습니다. 하지만 Part 7의 실습에서는 모든 옵션을 설명하지 않습니다. 먼저 `데이터셋 준비 -> caption 확인 -> 낮은 반복으로 첫 학습 -> sample image 검토 -> 반복 횟수 조정`까지만 봅니다.

외부 자료 기준으로 보면 `kohya_ss`는 직접 LoRA 학습을 다루는 대표 저장소로 남겨 두는 것이 좋습니다. 2026-07-31에 확인한 GitHub 규모는 약 12.3k stars, 1.6k forks이고, README도 Gradio GUI와 CLI로 LoRA, DreamBooth, fine-tuning, SDXL training을 지원한다고 설명합니다. 다만 로컬 GPU 환경 준비가 어려운 독자에게는 Colab형 예제 저장소도 보조 경로가 될 수 있습니다. 예를 들어 `hollowstrawberry/kohya-colab`은 약 807 stars, 134 forks 규모의 노트북형 LoRA 학습 예제 저장소이며, 이 절의 기준 실습은 옵션과 산출물을 더 직접 확인할 수 있는 `kohya_ss`로 둡니다.

## 첫 학습 흐름

처음에는 작은 범위로 닫힌 실습을 구성합니다.

1. 한 가지 목표만 고릅니다.
   예를 들어 `작은 로봇 캐릭터의 제품 패키지 스타일`처럼 대상과 스타일을 한 문장으로 적습니다.

2. 이미지셋을 한 폴더에 모읍니다.
   너무 비슷한 이미지가 반복되면 LoRA가 한 장면을 외울 수 있으므로, 구도와 배경이 조금씩 다른 이미지를 넣습니다.

3. caption 규칙을 정합니다.
   공통 trigger token과 장면 설명을 분리합니다. 예를 들어 `p7robot, small robot on cereal box, bright package design`처럼 trigger와 장면을 함께 씁니다.

4. 낮은 반복으로 첫 학습을 돌립니다.
   첫 실행에서는 성능보다 실패 신호를 빨리 보는 것이 중요합니다.

5. sample prompt를 고정해 중간 결과를 봅니다.
   같은 sample prompt에서 checkpoint별 출력이 어떻게 달라지는지 비교합니다.

## 실패 신호와 다음 조치

처음 직접 LoRA를 만들 때는 다음 실패를 의도적으로 확인하는 편이 좋습니다.

| 실패 신호 | 가능한 원인 | 다음 조치 |
| --- | --- | --- |
| trigger token을 넣어도 변화가 거의 없다 | 학습 부족, caption 불일치, LoRA weight 낮음 | steps와 caption을 확인합니다. |
| 모든 출력이 학습 이미지와 너무 비슷하다 | 과적합, 이미지 다양성 부족 | 반복 횟수를 줄이거나 이미지셋을 넓힙니다. |
| 특정 배경까지 따라온다 | caption에서 배경과 대상이 분리되지 않음 | caption에 대상과 배경을 더 분명히 나눕니다. |
| 다른 prompt를 거의 듣지 않는다 | LoRA 영향이 너무 강함 | LoRA weight를 낮추거나 학습 설정을 다시 봅니다. |

실패 기록은 다음 학습 데이터 수정으로 이어져야 합니다. 결과 이미지가 마음에 들지 않는다는 말만 남기면 다음 실험이 열리지 않습니다.

## 학습 결과 기록 양식

```text
lora_training_goal:
training_images:
caption_rule:
trigger_token:
training_steps:
sample_prompt:
best_checkpoint:
failure_seen:
next_dataset_fix:
```

이 기록이 있어야 직접 학습한 LoRA를 다시 앞 절로 가져갈 수 있습니다. `kohya_ss`에서 만든 LoRA를 P7-5.1의 diffusers 코드에 로드해 adapter weight를 비교하거나, P7-5.2의 ComfyUI workflow에 넣어 ControlNet, IP-Adapter와 함께 조합할 수 있습니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 학습 목표 | LoRA가 배워야 할 대상을 한 문장으로 적었는가? |
| 이미지셋 | 이미지 수와 다양성을 기록했는가? |
| caption 규칙 | trigger token과 장면 설명을 구분했는가? |
| sample prompt | 학습 중간 결과를 같은 prompt로 비교했는가? |
| 다음 수정 | 실패를 다음 데이터셋 수정으로 바꾸었는가? |

## 출처와 참고 자료

- bmaltais, [kohya_ss GitHub 저장소](https://github.com/bmaltais/kohya_ss){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- hollowstrawberry, [kohya-colab GitHub 저장소](https://github.com/hollowstrawberry/kohya-colab){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.

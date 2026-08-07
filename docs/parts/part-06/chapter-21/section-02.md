# P6-21.2 로컬 실행 환경과 메모리 배치

> Section ID: `P6-21.2`
> Version: `v2026.08.07`

오픈웨이트 모델을 직접 실행한다는 말은 모델 파일을 내려받는다는 뜻에서 끝나지 않습니다. 사용자는 모델을 어느 장치에 올릴지, 어떤 숫자 표현으로 읽을지, 한 번에 얼마나 긴 입력을 처리할지, 부족한 메모리를 어떤 방식으로 나눌지까지 함께 결정해야 합니다. 이 절의 질문은 **오픈웨이트 모델을 로컬이나 직접 관리 환경에서 실행할 때, GPU VRAM·CPU RAM·dtype·양자화·[CPU offloading](../../../reference/concept-glossary-parts/08-ieung.md#cpu-offloading)을 어떻게 구분해 읽어야 하는가**입니다.

여기서 중요한 것은 `돌아간다`와 `좋다`를 섞지 않는 것입니다. 모델이 실행되었다는 사실은 실행 가능성의 증거입니다. 출력이 목적에 맞는지는 별도의 품질 평가입니다. 큰 모델을 작은 장비에서 다룰수록 이 두 판단을 분리해야 합니다.

## 모델 실행은 가중치와 중간 계산을 놓을 자리를 정하는 일이다

모델을 실행하려면 학습된 가중치, 입력을 처리하는 중간 tensor, 출력 생성을 위한 임시 상태가 필요합니다. GPU는 이런 계산을 빠르게 처리하지만 VRAM이 제한적입니다. CPU RAM은 보통 더 넓지만 GPU보다 계산 속도가 느리고, GPU와 CPU 사이를 오가는 데 시간이 듭니다.

그래서 로컬 실행에서는 다음 질문을 먼저 봅니다.

| 확인할 것 | 뜻 | 실패하면 보이는 현상 |
| --- | --- | --- |
| 모델 크기 | 가중치와 구조가 차지하는 기본 메모리 | 적재 단계에서 실패하거나 너무 느리게 시작함 |
| dtype | 가중치를 어떤 숫자 표현으로 읽는가 | 메모리 사용량과 일부 연산 호환성이 달라짐 |
| context 또는 해상도 | 한 번에 처리할 입력 규모 | 긴 입력, 큰 이미지, 큰 batch에서 중간 tensor가 늘어남 |
| 실행 장치 | CPU, GPU, 혼합 배치 중 무엇을 쓰는가 | 속도, 메모리, 비용이 크게 달라짐 |
| offload 방식 | 쓰지 않는 부분을 어디에 대기시키는가 | 실행은 되지만 느려지거나 CPU RAM 병목이 생김 |

이 표는 모델 선택을 성능 순위표로만 읽지 않게 해 줍니다. 같은 모델도 숫자 표현, 입력 길이, 실행 장치, offload 방식이 달라지면 실행 기록이 달라집니다.

## dtype, 양자화, CPU offloading은 같은 말이 아니다

로컬 실행 설명에서 `bfloat16`, `float16`, `INT8`, `4-bit`, `offload`가 함께 나오면 모두 메모리를 줄이는 말처럼 보일 수 있습니다. 하지만 각각 줄이는 대상과 비용이 다릅니다.

| 구분 | 바꾸는 것 | 주된 효과 | 주의할 점 |
| --- | --- | --- | --- |
| dtype 선택 | 가중치와 계산에 쓰는 숫자 표현 | 같은 가중치를 더 작은 표현으로 읽어 메모리를 줄일 수 있음 | 장치와 연산 지원에 따라 속도나 호환성이 달라짐 |
| 양자화 | 가중치를 더 낮은 bit 표현으로 변환하거나 저장 | 모델 파일 크기와 메모리 사용량을 크게 줄일 수 있음 | 품질, 속도, 안정성은 모델·런타임·양자화 방식별로 검수해야 함 |
| CPU offloading | 모델 일부가 머무는 장치 배치 | GPU VRAM 부족을 CPU RAM으로 우회할 수 있음 | GPU와 CPU 사이 이동이 늘어 느려질 수 있음 |
| 입력 규모 축소 | context 길이, 해상도, batch, step | 중간 계산량과 임시 메모리를 줄임 | 과하게 줄이면 사용 목적 자체가 달라질 수 있음 |

예를 들어 `torch_dtype=torch.bfloat16`으로 모델을 읽는 것은 가중치 표현을 줄이는 선택입니다. 반면 `enable_sequential_cpu_offload()`는 pipeline의 세부 module을 필요할 때 GPU로 옮기고, 필요하지 않은 동안 CPU 쪽에 두는 실행 배치 선택입니다. 둘은 함께 쓸 수 있지만 서로를 대신하지 않습니다.

## CPU offloading은 메모리를 아끼는 대신 시간을 쓴다

CPU offloading은 GPU VRAM에 모든 구성요소를 계속 올려 두기 어렵기 때문에 씁니다. Diffusers와 Accelerate 문서는 inactive layer나 model component를 CPU 쪽에 두고, 실행 시점에 필요한 부분을 accelerator로 옮기는 방식을 설명합니다. 이 방식은 GPU 메모리를 줄일 수 있지만, 장치 사이 이동과 동기화가 늘어 실행 시간이 길어질 수 있습니다.

대표적인 offload 방식은 다음처럼 구분할 수 있습니다.

| 방식 | 이동 단위 | 메모리 절감 | 속도 경향 | 읽는 기준 |
| --- | --- | --- | --- | --- |
| model CPU offload | pipeline의 큰 구성요소 단위 | 중간 | 비교적 빠른 편 | 큰 module을 번갈아 쓰는 pipeline에서 먼저 검토 |
| sequential CPU offload | 세부 module 또는 leaf module 단위 | 큼 | 느린 편 | VRAM이 아주 부족할 때 실행 가능성 확보에 사용 |
| group offloading | 여러 layer를 묶은 group 단위 | 중간에서 큼 | 중간 | 모델 구조와 라이브러리 지원 상태를 함께 확인 |

sequential CPU offload는 메모리 절감 폭이 크지만 느릴 수 있습니다. 또한 Diffusers에서는 pipeline을 먼저 GPU로 옮기기 전에 offload hook을 설정해야 합니다. 따라서 실행 코드에서는 `pipe.to("cuda")`를 먼저 호출했는지, offload 설정이 실제 pipeline에 붙었는지 확인해야 합니다.

## 실행 가능성 gate와 품질 gate를 분리한다

로컬 모델 실험에서 가장 흔한 혼동은 `이미지가 나왔다`, `답변이 나왔다`를 곧바로 성공으로 기록하는 것입니다. 제한된 메모리 환경에서는 먼저 실행 가능성 gate를 통과했는지 확인하고, 그 다음 품질 gate를 따로 봐야 합니다.

| gate | 묻는 질문 | 대표 기록 |
| --- | --- | --- |
| 실행 가능성 gate | 이 설정으로 모델이 끝까지 실행되는가? | 모델 ID, dtype, 양자화, offload 방식, 입력 규모, peak memory, elapsed time, 오류 |
| 품질 gate | 출력이 목적과 기준을 만족하는가? | 정답 포함 여부, 화풍·pose·identity 보존, 근거 충실도, 사람 검수 결과 |
| 운용 gate | 반복 실행 가능한 부담인가? | 평균 지연, 처리량, CPU RAM 사용량, 저장공간, 재시도 비용 |

이 구분이 있어야 다음 행동도 정확해집니다. OOM이면 메모리 배치나 입력 규모를 줄여야 하고, 출력 품질이 틀리면 prompt, 참조 입력, 모델 선택, 평가 기준을 다시 봐야 합니다. 느리지만 품질은 맞는 경우에는 배치, 캐시, 더 빠른 런타임, 더 작은 모델을 검토해야 합니다.

## 기록 양식

로컬 실행 실험은 출력물만 저장하면 나중에 다시 읽기 어렵습니다. 최소한 아래 값을 함께 남깁니다.

```text
run_id:
model_id:
model_revision:
weight_format:
dtype:
quantization:
runtime:
device:
offload_mode:
input_size:
context_length:
width:
height:
batch_size:
steps:
peak_vram:
peak_ram:
elapsed_seconds:
status:
quality_note:
next_trial:
```

LLM 실험이라면 `context_length`, `input_tokens`, `output_tokens`가 중요해지고, 이미지 생성 실험이라면 `width`, `height`, `steps`, `guidance`, `seed`가 중요해집니다. 하지만 두 경우 모두 `실행 조건`, `실행 부담`, `품질 메모`를 분리해서 남긴다는 원칙은 같습니다.

## Part 7로 넘어가는 연결

Part 7의 현재 모델 실행 실습은 이 절의 개념을 실제 기록으로 바꿉니다.

| Part 7 위치 | 여기서 가져갈 기준 |
| --- | --- |
| P7-5.1~P7-5.5 FLUX 이미지 실험 | sequential CPU offload를 실행 가능성 확보 장치로 읽고, 모델 파일, dtype, 참조 입력, 해상도, 사람 검수 ledger를 함께 기록 |
| P7-6.1 로컬 LLM 실험 | 양자화, context 길이, 실행 시간, 답변 안정성을 같은 질문으로 비교 |
| P7-7.1 비전 모델 실험 | prompt 입력 구조와 실행 부담을 mask 품질 판정과 분리 |

따라서 오픈웨이트 모델을 직접 다룬다는 것은 `내 컴퓨터에서 한번 실행해 본다`보다 넓은 판단입니다. 모델 공개 범위를 확인하고, 실행 조건을 고정하고, 메모리 배치를 기록하고, 품질 판정을 따로 남기는 일까지 포함합니다.

## 체크리스트

- dtype, 양자화, CPU offloading을 서로 다른 층위로 설명할 수 있는가?
- 모델이 실행된 사실과 출력이 품질 기준을 만족한 사실을 따로 기록했는가?
- GPU VRAM 부족, CPU RAM 병목, 느린 실행, 품질 실패를 같은 실패로 묶지 않았는가?
- offload 방식을 썼다면 어떤 단위로 CPU와 GPU 사이를 이동시키는지 설명할 수 있는가?
- Part 7 실험으로 넘어갈 때 실행 조건과 품질 검수 항목을 같은 표 안에 남길 수 있는가?

## 출처와 참고 자료

- Hugging Face Diffusers, [Reduce memory usage](https://huggingface.co/docs/diffusers/optimization/memory){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-07.
- Hugging Face Diffusers, [Pipelines overview](https://huggingface.co/docs/diffusers/api/pipelines/overview){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-07.
- Hugging Face Accelerate, [Working with large models](https://huggingface.co/docs/accelerate/en/package_reference/big_modeling){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-07.

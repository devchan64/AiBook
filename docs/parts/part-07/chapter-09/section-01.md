# P7-9.1 로컬 LLM으로 양자화와 context 길이 비교하기

> Section ID: `P7-9.1`
> Version: `v2026.07.31`

Part 6에서 LLM을 배울 때는 token, context, inference, parameter 같은 말을 개념으로 먼저 봅니다. 이 절에서는 그 말을 로컬 실행 실습으로 다시 확인합니다. 목표는 가장 똑똑한 모델을 고르는 것이 아니라, 같은 질문을 작은 모델과 양자화 모델에 넣었을 때 속도, 메모리, 답변 안정성이 어떻게 달라지는지 기록하는 것입니다.

로컬 LLM 실습은 `API를 호출했다`와 다릅니다. 모델 파일, 양자화 형식, context 길이, 실행 장치가 결과와 비용을 직접 바꿉니다. 따라서 이 절에서는 `llama.cpp` 같은 로컬 추론 도구를 기준으로, Qwen이나 Gemma 계열의 작은 모델을 실행 후보로 둡니다.

## 무엇을 바꿀 것인가

처음부터 여러 모델을 많이 비교하지 않습니다. 한 번에 하나의 조건만 바꿉니다.

| 비교 축 | 바꿀 값 | 읽어야 할 질문 |
| --- | --- | --- |
| 모델 크기 | 작은 모델, 더 큰 모델 | 답변 품질이 좋아지는 대신 실행 부담이 얼마나 커지는가 |
| 양자화 | 4-bit, 8-bit, 원본에 가까운 형식 | 속도와 메모리 사용량이 줄어드는 대신 답변이 얼마나 흔들리는가 |
| context 길이 | 짧은 입력, 긴 입력 | 긴 문맥에서 앞 정보가 유지되는가 |
| 실행 방식 | CLI, local server | 한 번 실행과 반복 호출의 기록 방식이 어떻게 달라지는가 |

## 실습 순서

1. 같은 질문 세 개를 준비합니다.
   하나는 짧은 사실 질문, 하나는 긴 문맥 요약, 하나는 단계별 추론이 필요한 질문으로 둡니다.

2. 같은 모델의 양자화 형식을 두 개 고릅니다.
   예를 들어 같은 계열의 4-bit 모델과 8-bit 모델을 고르면, 모델 지식 차이보다 양자화 차이를 먼저 볼 수 있습니다.

3. 같은 prompt를 두 모델에 넣습니다.
   출력만 보지 말고 실행 시간, token 수, context 길이, 실패 문장을 함께 남깁니다.

4. 긴 문맥 입력을 넣고 앞부분 정보가 유지되는지 확인합니다.
   context 길이가 커졌다는 설명이 실제 답변에서 어떻게 드러나는지 봅니다.

## 최소 실행 예시

설치와 모델 다운로드 방식은 운영체제와 장치에 따라 달라질 수 있으므로, 이 절에서는 실행 기록에 필요한 최소 형태만 둡니다. 실제 명령은 사용하는 `llama.cpp` 버전과 모델 저장소 안내를 함께 확인해야 합니다.

```bash
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF \
  -p "Part 6에서 말한 context length가 왜 중요한지 한 문단으로 설명해 줘." \
  -n 180
```

같은 prompt를 더 긴 context 설정으로 다시 실행합니다.

```bash
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF \
  -c 8192 \
  -p "다음 프로젝트 메모를 읽고, 기준점과 다음 실험을 분리해 줘: ..." \
  -n 220
```

로컬 파일을 이미 받은 경우에는 모델 파일 경로를 직접 남깁니다.

```bash
llama-cli -m models/example-model-q4_k_m.gguf \
  -p "같은 질문에 대해 짧게 답해 줘." \
  -n 120
```

이 명령의 목적은 좋은 답변을 얻는 것이 아니라, `model_file`, `quantization`, `context_length`, `prompt`, `elapsed_time`, `failure_seen`을 한 줄씩 채우는 것입니다.

## 기록 양식

```text
run_id:
tool:
model_id:
model_file:
quantization:
context_length:
prompt:
input_tokens:
output_tokens:
elapsed_time:
answer_summary:
failure_seen:
next_trial:
```

`answer_summary`에는 답변 전체를 길게 붙이지 않습니다. 대신 `핵심 답은 맞음`, `앞 문맥의 제약을 잊음`, `근거 없는 세부사항을 덧붙임`처럼 비교 가능한 문장으로 적습니다.

## Part 1~6으로 되돌아가기

| 다시 확인할 개념 | 이 실습에서 보이는 장면 |
| --- | --- |
| Part 1의 모델 실행 | 같은 모델도 실행 환경과 입력 조건에 따라 다르게 보입니다. |
| Part 2의 메모리와 계산 | 양자화는 모델 파일 크기와 실행 부담을 직접 바꿉니다. |
| Part 5의 Transformer | 긴 context에서 앞 정보가 어떻게 유지되거나 흐려지는지 봅니다. |
| Part 6의 token과 prompt | prompt 길이와 답변 길이가 실행 시간과 실패 양상을 바꿉니다. |

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 모델 파일 | 어떤 모델과 양자화 형식을 썼는가? |
| 입력 조건 | 같은 prompt와 context 길이로 비교했는가? |
| 실행 기록 | 속도, token 수, 실패 문장을 함께 남겼는가? |
| 답변 해석 | 답변 품질을 감상이 아니라 비교 문장으로 적었는가? |
| 다음 실행 | 모델 크기, 양자화, context 중 다음에 바꿀 값을 하나로 정했는가? |

## 출처와 참고 자료

- ggml-org, [llama.cpp GitHub 저장소](https://github.com/ggml-org/llama.cpp){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- QwenLM, [Qwen3 GitHub 저장소](https://github.com/QwenLM/Qwen3){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.
- google, [gemma.cpp GitHub 저장소](https://github.com/google/gemma.cpp){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-07-31.

# P7-6.1 로컬 LLM으로 양자화와 context 길이 비교하기

> Section ID: `P7-6.1`
> Version: `v2026.08.01`

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

## 실제 CPU 실행: FP32와 동적 INT8의 비교

이 절의 비교 조건이 실제 출력에서 어떻게 갈리는지 확인하기 위해 `Qwen/Qwen2.5-0.5B-Instruct`를 CPU에서 직접 실행했습니다. Qwen 모델 카드는 Transformers의 `AutoTokenizer`, `AutoModelForCausalLM`, chat template, `generate()`를 사용하는 실행 방식을 제시합니다. 여기서는 그 형식을 사용하되, GPU나 GGUF 파일이 없는 환경에서도 비교할 수 있도록 PyTorch FP32 실행과 `Linear` 계층의 CPU 동적 INT8 변환을 나란히 두었습니다.

이 결과는 모델의 일반 성능 순위가 아닙니다. `Qwen/Qwen2.5-0.5B-Instruct`, PyTorch `2.13.0+cpu`, CPU 4 thread, `max_new_tokens=16`, greedy decoding이라는 한 환경에서 얻은 스냅샷입니다. 특히 동적 INT8은 이 예제에서 `torch.ao.quantization.quantize_dynamic()`으로 실행 중 변환한 것이며, GGUF의 Q4/Q8 파일 또는 다른 양자화 도구의 결과와 같다고 볼 수 없습니다.

### 입력과 실행 자산

- 질문 입력: [`p7-6-1-prompts.csv`](../../../assets/part-07/chapter-06/p7-6-1-prompts.csv) · [CSV 미리보기](../../../assets/part-07/chapter-06/p7-6-1-prompts.csv){ .csv-preview }
- 실행 스크립트: [`p7_6_1_local_llm_experiment.py`](../../../assets/part-07/chapter-06/p7_6_1_local_llm_experiment.py)
- 실제 실행 로그: [`p7-6-1-local-llm-results.csv`](../../../assets/part-07/chapter-06/p7-6-1-local-llm-results.csv) · [CSV 미리보기](../../../assets/part-07/chapter-06/p7-6-1-local-llm-results.csv){ .csv-preview }

질문 파일의 한 행은 `짧은 또는 긴 프로젝트 기록에서 사실 하나를 되찾는 요청`입니다. 세 가지 사실, 두 context 조건, 여섯 가지 질문 표현을 사용했고, 36개 입력을 FP32와 동적 INT8에서 각각 실행해 총 72개의 원문 응답을 남겼습니다. `expected_answer_seen`은 응답에 기대 사실 문자열이 들어 있는지 보는 가벼운 관찰 열일 뿐, 생성 답변의 완전한 정확도 평가는 아닙니다.

모델과 의존성을 받은 뒤에는 다음 명령으로 같은 스냅샷을 다시 만들 수 있습니다.

```bash
HF_HUB_OFFLINE=1 .venv/bin/python \
  docs/assets/part-07/chapter-06/p7_6_1_local_llm_experiment.py
```

`HF_HUB_OFFLINE=1`은 이미 Hugging Face cache에 받은 모델을 다시 쓰는 조건입니다. 처음 실행에는 `torch`, `transformers`, `psutil`과 모델 다운로드가 필요합니다. 모델이나 PyTorch 버전을 바꾸면 로그의 수치와 문장이 달라질 수 있으므로, 기존 CSV를 정답표로 덮어쓰지 말고 새 `run_date`, 모델 이름, 설정을 함께 기록합니다.

### 2026-08-01 실행 결과

| 실행 조건 | 기대 사실 포함 | 평균 지연 | 모델 적재 뒤 RSS | 읽을 점 |
| --- | ---: | ---: | ---: | --- |
| FP32, 짧은 입력 40~45 tokens | 17 / 18 | 333.2 ms | 2,350.2 MB | 대부분의 사실을 유지했고, 한 action 표현만 기대 문자열을 놓쳤습니다. |
| FP32, 긴 입력 358~363 tokens | 18 / 18 | 1,133.2 ms | 2,350.2 MB | 입력 token이 약 8배로 늘자 평균 지연은 약 3.4배가 됐지만, 이 작은 사실 회수에서는 기대 사실이 유지됐습니다. |
| 동적 INT8 `Linear`, 짧은 입력 40~45 tokens | 1 / 18 | 296.9 ms | 4,372.0 MB | 지연은 약간 낮지만 기대 사실을 포함한 응답은 거의 없었습니다. |
| 동적 INT8 `Linear`, 긴 입력 358~363 tokens | 2 / 18 | 749.3 ms | 4,372.0 MB | 평균 지연은 FP32 긴 입력보다 낮았지만, 대부분 관련 없는 문장이나 기록을 바꾼 답을 냈습니다. |

전체 평균은 FP32 `733.2 ms`, 동적 INT8 `523.1 ms`였습니다. 이 실행에서는 동적 INT8이 약 29% 빨랐지만, 기대 사실 포함은 FP32 `35 / 36`, 동적 INT8 `3 / 36`으로 크게 갈렸습니다. 또한 별도 프로세스에서 모델을 적재해 기록한 RSS도 동적 INT8 쪽이 더 컸습니다. 따라서 이 결과로 `INT8은 항상 메모리를 줄인다`거나 `더 빠르므로 더 낫다`고 결론내릴 수 없습니다.

실패를 실제 출력으로 읽으면 더 분명합니다. 동적 INT8의 `owner-short-1`은 `Mina` 대신 원통의 밑면과 높이를 말했고, `seed-long-1`은 기록의 `42`를 `50`으로 바꿨습니다. 이 경우의 다음 행동은 더 긴 context를 주는 것이 아니라, 같은 모델·도구 조합에서 양자화 방식의 출력 보존을 먼저 검증하고, 실패 응답을 남기는 것입니다. 양자화 비교는 시간과 메모리만 적는 벤치마크가 아니라, 같은 사실을 유지하는지 확인하는 출력 비교여야 합니다.

## 기록 양식

```text
run_id:
tool:
model_id:
model_file:
quantization:
context_length:
input_tokens:
max_new_tokens:
device:
torch_version:
prompt:
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
- Qwen, [Qwen2.5-0.5B-Instruct model card](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.
- PyTorch, [quantize_dynamic API reference](https://docs.pytorch.org/docs/2.13/generated/torch.ao.quantization.quantize_dynamic.html){: target="_blank" rel="noopener noreferrer" }, 확인일: 2026-08-01.

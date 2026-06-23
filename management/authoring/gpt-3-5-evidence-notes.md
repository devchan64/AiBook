# GPT-3.5 근거 메모

## 목적

- GPT-3.5와 GPT-3.5 Turbo를 11.3 또는 후속 LLM 사용 경험 절에서 어떻게 설명할지 검토합니다.
- GPT-3.5를 GPT-3처럼 공개 논문 하나로 설명할 수 있는지, 아니면 여러 공식 발표와 외부 평가 논문으로 설명해야 하는지 확인합니다.

## 1차 판단

GPT-3.5는 GPT-3처럼 단일 공개 기술 논문으로 설명하기 어렵습니다. 공개적으로 확인 가능한 흐름은 다음 자료들을 조합해야 합니다.

```text
GPT-3
-> InstructGPT: instruction following과 RLHF
-> GPT-3.5 series: text-davinci-002, text-davinci-003, gpt-3.5-turbo 등
-> ChatGPT: GPT-3.5 series 모델을 대화형으로 fine-tuning한 제품 경험
-> GPT-3.5 Turbo API: chat/message 형식과 저비용 API 확산
```

따라서 GPT-3.5의 의미는 “새로운 아키텍처의 공개”라기보다, 다음 네 가지 변화로 보는 편이 안전합니다.

- instruction following이 전면화됨
- RLHF(reinforcement learning from human feedback)가 사용자 의도 정렬(alignment)의 핵심 방법으로 부각됨
- ChatGPT를 통해 dialogue format과 대화형 맥락 처리 경험이 대중화됨
- `gpt-3.5-turbo` API를 통해 서비스형 LLM이 빠르게 확산됨

## 공식 자료

### OpenAI, Aligning language models to follow instructions, 2022

- URL: <https://openai.com/index/instruction-following/>
- 관련 논문: Ouyang et al., *Training language models to follow instructions with human feedback*, arXiv:2203.02155
- 핵심 근거:
  - 모델을 크게 만드는 것만으로 사용자 의도를 잘 따르는 것은 아니라고 설명합니다.
  - GPT-3를 human feedback으로 fine-tuning해 InstructGPT를 만들었습니다.
  - 1.3B InstructGPT가 175B GPT-3보다 선호되는 결과를 보고했습니다.
  - truthfulness 개선과 toxic output 감소를 보고하지만, simple mistake와 alignment 한계도 인정합니다.
- 본문 반영:
  - GPT-3.5로 이어지는 핵심 전환은 “더 큰 모델”보다 “사용자 지시를 따르도록 정렬된 모델”이라는 방향입니다.

### OpenAI, Introducing ChatGPT, 2022

- URL: <https://openai.com/index/chatgpt/>
- 핵심 근거:
  - ChatGPT는 GPT-3.5 series 모델에서 fine-tuning된 대화형 모델로 설명됩니다.
  - dialogue format이 follow-up question, mistake admission, incorrect premise challenge, inappropriate request rejection을 가능하게 한다고 설명합니다.
  - RLHF를 사용했으며 InstructGPT와 유사한 방법을 사용하되 대화 데이터 구성이 다릅니다.
- 본문 반영:
  - 사용자가 기억하는 “문맥을 이어 가는 느낌”은 모델 구조 하나의 변화가 아니라 dialogue format, RLHF, 제품 인터페이스가 결합된 경험으로 설명합니다.

### OpenAI, Introducing APIs for GPT-3.5 Turbo and Whisper, 2023

- URL: <https://openai.com/index/introducing-chatgpt-and-whisper-apis/>
- 핵심 근거:
  - `gpt-3.5-turbo`는 ChatGPT 제품에 쓰인 모델과 같은 모델로 소개됩니다.
  - 기존 GPT-3.5 모델보다 저렴하며, 많은 non-chat use case에도 적합하다고 설명합니다.
  - 전통적 GPT 모델은 unstructured text를 입력으로 받았지만, ChatGPT 모델은 metadata를 포함한 message sequence를 입력으로 받는다고 설명합니다.
  - `gpt-3.5-turbo`는 stable model alias로 제공되고, 특정 snapshot을 선택할 수 있음을 설명합니다.
- 본문 반영:
  - GPT-3.5 Turbo의 도메인적 변화는 “모델 성능”만이 아니라 chat/message API 형식, 비용 절감, 개발자 확산, snapshot/drift 문제로 연결됩니다.

## 학술 자료

### Ouyang et al., Training language models to follow instructions with human feedback, 2022

- URL: <https://arxiv.org/abs/2203.02155>
- 다운로드: `.tmp/gpt-3-5-turbo-evidence/ouyang-2022-instructgpt.pdf`
- 핵심 근거:
  - InstructGPT는 GPT-3를 supervised fine-tuning과 RLHF로 조정한 모델입니다.
  - 1.3B InstructGPT가 175B GPT-3보다 선호된다는 결과는 “크기만이 사용 경험을 결정하지 않는다”는 설명에 중요합니다.
  - truthfulness와 toxicity 개선이 보고되지만, 편향과 안전 문제는 완전히 해결되지 않습니다.

### Ye et al., A Comprehensive Capability Analysis of GPT-3 and GPT-3.5 Series Models, 2023

- URL: <https://arxiv.org/abs/2303.10420>
- 다운로드: `.tmp/gpt-3-5-turbo-evidence/ye-2023-gpt3-gpt35-capability-analysis.pdf`
- 핵심 근거:
  - GPT-3 series와 GPT-3.5 series를 비교합니다.
  - GPT-3.5 series에는 `code-davinci-002`, `text-davinci-002`, `text-davinci-003`, `gpt-3.5-turbo`가 포함됩니다.
  - NLU 과업에서 모델 진화가 항상 선형적 성능 향상으로 이어지지는 않는다고 보고합니다.
  - RLHF는 human-like response에는 도움을 주지만, 일부 과업 능력과 robustness에는 복잡한 영향을 줄 수 있다고 설명합니다.

### Chen et al., How is ChatGPT's behavior changing over time?, 2023

- URL: <https://arxiv.org/abs/2307.09009>
- 다운로드: `.tmp/gpt-3-5-turbo-evidence/chen-2023-chatgpt-behavior-changing.pdf`
- 핵심 근거:
  - 2023년 3월과 6월의 GPT-3.5/GPT-4 동작 변화를 비교합니다.
  - 같은 이름의 LLM 서비스라도 성능, verbosity, formatting, instruction following이 바뀔 수 있다고 보고합니다.
  - GPT-3.5 Turbo 같은 API 모델은 “고정된 논문 모델”이 아니라 업데이트되는 서비스 모델로 다뤄야 합니다.

### Chalkidis, ChatGPT may Pass the Bar Exam soon, but has a Long Way to Go for the LexGLUE benchmark, 2023

- URL: <https://arxiv.org/abs/2304.12202>
- 다운로드: `.tmp/gpt-3-5-turbo-evidence/chalkidis-2023-chatgpt-lexglue.pdf`
- 핵심 근거:
  - `gpt-3.5-turbo`를 첫 ChatGPT 모델로 보고 LexGLUE 법률 벤치마크를 zero-shot으로 평가합니다.
  - 의미 있는 성능을 보이지만 전문 법률 벤치마크에서는 한계가 있습니다.
  - “대화가 자연스럽다”와 “전문 과업을 안정적으로 해결한다”를 구분하는 근거입니다.

### Kabir et al., An empirical study of ChatGPT-3.5 on question answering and code maintenance, 2023

- URL: <https://arxiv.org/abs/2310.02104>
- 다운로드: `.tmp/gpt-3-5-turbo-evidence/kabir-2023-chatgpt35-code-maintenance.pdf`
- 핵심 근거:
  - StackOverflow 질의응답과 Java 유지보수 작업에서 ChatGPT-3.5를 평가합니다.
  - 기술 질문 답변에서는 강점을 보이지만, 프로젝트 맥락에 맞는 코드 유지보수에서는 한계가 큽니다.
  - Codex와 agent 장에서 “AI 도구는 보조 도구이지 독립 유지보수자가 아니다”라는 설명에 활용할 수 있습니다.

## 본문에 반영할 안전한 문장 후보

```text
GPT-3.5는 GPT-3처럼 하나의 공개 논문으로 설명되는 단일 전환이라기보다,
InstructGPT의 instruction following, RLHF, ChatGPT의 dialogue format,
그리고 gpt-3.5-turbo API 확산이 결합된 흐름으로 보는 편이 안전하다.
```

```text
GPT-3.5/ChatGPT가 바꾼 것은 Transformer 구조 자체라기보다,
사용자가 LLM을 대화형 작업 도구로 인식하게 만든 사용 경험이었다.
```

```text
다만 GPT-3.5 계열의 성능은 과업마다 다르게 나타났고,
외부 평가 논문들은 버전 상승이나 RLHF가 모든 과업에서 선형적 성능 향상을 보장하지 않는다고 보고한다.
```

## 반영 위치 제안

- 11.3 본문에는 반영하지 않습니다.
- 이 내용은 Transformer와 사전학습 LLM 자체보다, 여러 기술 요소가 통합되어 AI를 대화형 작업 도구로 인식하게 만든 변화에 가깝습니다.
- 따라서 자세한 설명은 이후 다음 주제에서 다룹니다.
  - LLM과 prompt
  - ChatGPT와 AI 도구 사용 경험
  - Codex와 agent
  - AI 서비스 모델과 API
  - 모델 drift와 검증

## 주의할 표현

피해야 할 표현:

```text
GPT-3.5에서 AI가 문맥을 이해하기 시작했다.
GPT-3.5는 GPT-3보다 모든 면에서 더 우수하다.
GPT-3.5 Turbo는 GPT-3.5의 학술적으로 공개된 최종 형태다.
```

권장 표현:

```text
GPT-3.5/ChatGPT는 instruction following, RLHF, dialogue format, API 제품화가 결합되면서
사용자가 LLM을 대화형 작업 도구로 경험하게 만든 전환점이었다.
```

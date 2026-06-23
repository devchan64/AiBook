# Section 12.2 근거 검토: 지시, 맥락, 예시

## 검토 목적

- 12.2의 중심 질문은 “프롬프트 안에서 지시, 맥락, 예시는 어떤 다른 역할을 하는가?”입니다.
- 12.1에서 프롬프트가 무엇을 지정하는지 설명했으므로, 12.2는 세부 기법 목록이 아니라 기본 구성 요소를 구분하는 절로 작성했습니다.

## 확인한 자료

12.1에서 내려받아 확인한 자료를 재사용했습니다. 원문 PDF와 HTML은 `.tmp/section-12-1-evidence/` 아래에 있습니다.

| 자료 | 반영 판단 |
| --- | --- |
| Brown et al., *Language Models are Few-Shot Learners*, 2020 | few-shot setting에서 task demonstration을 입력에 넣고, gradient update 없이 과업을 수행한다는 설명의 근거로 사용했습니다. |
| Ouyang et al., *Training language models to follow instructions with human feedback*, 2022 | instruction following이 LLM 사용 경험에서 별도 연구 주제가 되었고, prompt가 task를 지정하는 입력으로 쓰인다는 배경 근거로 사용했습니다. |
| Sahoo et al., *A Systematic Survey of Prompt Engineering in Large Language Models*, 2024 | prompt가 instruction과 context를 포함해 모델 행동을 유도한다는 설명, zero-shot/few-shot prompting 구분의 근거로 사용했습니다. |
| OpenAI, *Prompt engineering*, OpenAI API documentation | 명확한 지시와 예시를 통해 결과를 개선하는 실무적 설명의 보조 근거로 사용했습니다. |

## 본문 반영 기준

- 지시(instruction)는 수행할 작업을 지정하는 요소로 설명했습니다.
- 맥락(context)은 작업 대상, 독자, 목적, 앞선 결정, 제외할 범위처럼 모델이 참고해야 할 정보로 설명했습니다.
- 예시(example)는 원하는 입력-출력 패턴을 보여 주는 현재 입력 안의 demonstration으로 설명했습니다.
- 예시를 fine-tuning이나 영구 학습으로 설명하지 않았습니다.
- 프롬프트 구조화가 사실성, 근거성, 안전성을 보장한다고 설명하지 않았습니다.

## Section 경계 검토

- 12.2는 지시, 맥락, 예시의 역할 구분에 집중합니다.
- 12.3의 주제인 프롬프트 한계, 평가 기준, 검증 절차는 짧게 예고만 했습니다.
- RAG, vector search, tool use, 에이전트(agent)는 Chapter 13과 14로 넘겼습니다.
- Chain-of-thought(CoT), self-consistency, automatic prompt optimization 같은 고급 프롬프트 엔지니어링(prompt engineering) 기법은 이 절에서 자세히 다루지 않았습니다.

## 용어 검토

- `프롬프트(prompt)`, `지시(instruction)`, `맥락(context)`, `예시(example)`, `모델 실행(inference)`, `파인튜닝(fine-tuning)`, `도구 사용(tool use)`, `에이전트(agent)`를 한영 병기했습니다.
- `instruction`을 단순 명령문으로만 좁히지 않고, 수행할 작업과 기준을 지정하는 요소로 설명했습니다.
- `context`를 긴 배경 설명이 아니라 모델이 참고해야 할 입력 정보로 설명했습니다.
- `example`을 정답 자체가 아니라 패턴을 보여 주는 demonstration으로 설명했습니다.

## 주의한 오해

- 예시를 넣으면 모델이 새 지식을 영구적으로 배운다고 설명하지 않았습니다.
- 맥락을 제공하면 사실 검증이 자동으로 끝난다고 설명하지 않았습니다.
- 프롬프트가 길수록 좋다고 설명하지 않았습니다.
- 고급 prompt engineering 기법을 초심자용 기본 구조와 섞지 않았습니다.

## 참고 자료

- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), arXiv, 2020, 확인 날짜: 2026-06-23.
- Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155), arXiv, 2022, 확인 날짜: 2026-06-23.
- Pranab Sahoo et al., [A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications](https://arxiv.org/abs/2402.07927), arXiv, 2024, 확인 날짜: 2026-06-23.
- OpenAI, [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering), OpenAI API documentation, 확인 날짜: 2026-06-23.

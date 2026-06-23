# Section 12.1 근거 검토: 프롬프트는 무엇을 지정하는가

## 검토 목적

- 12.1의 중심 질문은 “프롬프트는 모델에게 무엇을 알려 주는 입력인가?”입니다.
- 이 메모는 프롬프트를 지시, 맥락, 예시, 제약, 출력 형식으로 설명하는 것이 근거와 Section 경계에 맞는지 확인하기 위한 관리 자료입니다.

## 확인한 자료

원문 PDF와 HTML은 `.tmp/section-12-1-evidence/` 아래에 내려받아 확인했습니다.

| 자료 | 반영 판단 |
| --- | --- |
| Brown et al., *Language Models are Few-Shot Learners*, 2020 | GPT-3가 zero-shot, one-shot, few-shot setting에서 task와 demonstration을 텍스트로 제공받고, gradient update나 fine-tuning 없이 수행된다는 설명의 근거입니다. |
| Ouyang et al., *Training language models to follow instructions with human feedback*, 2022 | prompt가 instruction, few-shot example, continuation 같은 방식으로 task를 지정할 수 있고, instruction following이 별도 연구 주제가 되었음을 보여 주는 근거입니다. |
| Sahoo et al., *A Systematic Survey of Prompt Engineering in Large Language Models*, 2024 | prompt engineering을 모델 파라미터를 바꾸지 않고 task-specific instruction과 context로 모델 행동을 유도하는 접근으로 설명하는 근거입니다. |
| OpenAI, *Prompt engineering*, OpenAI API documentation | 프롬프트를 더 명확하게 구성하고, 지시와 예시를 통해 결과를 개선하는 실무적 가이드의 근거로 사용했습니다. |

## 본문 반영 기준

- 프롬프트를 “모델에게 말 거는 요령”이 아니라 “현재 입력 안에 작업 조건을 배치하는 방법”으로 설명했습니다.
- 프롬프트를 LLM 내부 구조를 직접 설명하는 수단으로 쓰지 않고, 입력 조건에 따른 출력 변화를 관찰하는 입구로 제한했습니다.
- 12.1에서는 prompt engineering의 세부 기법 목록을 다루지 않았습니다.
- 지시, 맥락, 예시, 제약, 출력 형식을 프롬프트가 지정할 수 있는 기본 요소로 정리했습니다.
- in-context learning은 모델 가중치 업데이트가 아니라 입력 문맥 안에서 일어나는 행동 변화로 설명했습니다.
- 프롬프트가 사실성, 근거성, 안전성을 자동으로 보장하지 않는다는 점을 명시했습니다.

## Section 경계 검토

- 12.1은 “프롬프트가 무엇을 지정하는가”만 다룹니다.
- 12.2는 지시, 맥락, 예시를 더 구체적으로 나누는 절로 남깁니다.
- 12.3은 프롬프트의 한계와 평가 기준을 다루는 절로 남깁니다.
- RAG, vector search, tool use는 Chapter 13과 14로 넘깁니다.
- Codex와 에이전트(agent)는 GPT-3.5/ChatGPT 이후의 도구 사용 경험으로 후속 장에서 다루는 것이 적절합니다.
- 재검토 결과 에이전트(agent), MCP(Model Context Protocol), 하네스(harness)는 프롬프트 자체보다 LLM을 실행 환경, 도구 연결, 평가 장치와 묶어 설명하는 주제입니다. 따라서 12장을 확장하기보다 Chapter 14의 서비스 아키텍처와 실행 환경 안에서 다루는 편이 Section 경계를 덜 침범합니다.

## 용어 검토

- `프롬프트(prompt)`, `지시(instruction)`, `맥락(context)`, `예시(example)`, `제약(constraint)`, `출력 형식(output format)`, `문맥 내 학습(in-context learning)`, `컨텍스트 윈도우(context window)`, `파인튜닝(fine-tuning)`을 한영 병기했습니다.
- `추론`이라는 표현은 이 절의 핵심이 아니므로 reasoning과 inference를 혼용하지 않았습니다.
- `학습`이라는 표현은 fine-tuning과 in-context learning의 차이를 설명할 때만 제한적으로 사용했습니다.

## 주의한 오해

- 프롬프트를 모델 가중치를 바꾸는 학습 데이터로 설명하지 않았습니다.
- 프롬프트를 사실 검증 장치로 설명하지 않았습니다.
- few-shot prompting을 “모델이 새 지식을 배운다”로 설명하지 않았습니다.
- 프롬프트가 길수록 항상 좋다는 식으로 설명하지 않았습니다.
- prompt engineering을 마법적 요령이나 만능 해결책으로 설명하지 않았습니다.
- 프롬프트만으로 LLM 내부 회로나 학습된 표현을 알 수 있다고 설명하지 않았습니다.

## 참고 자료

- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165), arXiv, 2020, 확인 날짜: 2026-06-23.
- Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155), arXiv, 2022, 확인 날짜: 2026-06-23.
- Pranab Sahoo et al., [A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications](https://arxiv.org/abs/2402.07927), arXiv, 2024, 확인 날짜: 2026-06-23.
- OpenAI, [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering), OpenAI API documentation, 확인 날짜: 2026-06-23.

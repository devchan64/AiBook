# Section 12.3 근거 검토: 프롬프트의 한계와 평가

## 검토 목적

- 12.3의 중심 질문은 “프롬프트가 보장하지 못하는 것은 무엇이고, 무엇을 평가해야 하는가?”입니다.
- 12.1과 12.2가 프롬프트의 구성 요소를 설명했으므로, 12.3은 프롬프트의 한계와 검토 기준을 정리하는 절로 작성했습니다.

## 확인한 자료

12.1에서 내려받은 prompt 관련 자료와 10.3에서 내려받은 생성 결과 위험 관련 자료를 재사용했습니다.

| 자료 | 위치 | 반영 판단 |
| --- | --- | --- |
| Ouyang et al., *Training language models to follow instructions with human feedback*, 2022 | `.tmp/section-12-1-evidence/ouyang-2022-instructgpt.pdf`, `.txt` | human evaluation, truthfulness, helpfulness, harmlessness, hallucination rate 등 LLM 출력 평가가 다기준 문제라는 근거로 사용했습니다. |
| Sahoo et al., *A Systematic Survey of Prompt Engineering in Large Language Models*, 2024 | `.tmp/section-12-1-evidence/sahoo-2024-prompt-engineering-survey.pdf`, `.txt` | prompt engineering 기법들이 benchmark와 accuracy, robustness, hallucination 같은 기준으로 비교된다는 배경 근거로 사용했습니다. |
| NIST, *Generative Artificial Intelligence Profile*, 2024 | `.tmp/section-10-3-evidence/nist-ai-600-1-genai-profile.pdf`, `.txt` | confabulation/hallucination을 그럴듯하지만 잘못되었거나 거짓인 생성물로 설명하는 근거로 사용했습니다. |
| OpenAI, *Prompt engineering*, OpenAI API documentation | `.tmp/section-12-1-evidence/openai-prompt-engineering-guide.html` | 명확한 지시와 예시가 유용하더라도 prompt를 반복적으로 개발하고 검토해야 한다는 실무적 배경으로 사용했습니다. |

## 본문 반영 기준

- 프롬프트를 결과 보증이 아니라 출력 조건 지정으로 설명했습니다.
- 사실성(factuality), 근거성(evidence), 최신성(recency)을 구분했습니다.
- 환각(hallucination)은 10.3의 NIST 근거와 연결해 “그럴듯한 오류”로 설명했습니다.
- 평가(evaluation)는 한 번의 마음에 드는 출력 선택이 아니라 목적에 맞춘 검토 기준으로 설명했습니다.
- RAG, 도구 사용(tool use), 에이전트(agent), 하네스(harness)는 다음 장의 주제로 예고만 했습니다.

## Section 경계 검토

- 12.3은 프롬프트의 한계와 평가 기준에 집중합니다.
- RAG, vector search는 Chapter 13에서 설명합니다.
- 도구 사용(tool use), 에이전트(agent), MCP(Model Context Protocol), 하네스(harness)는 Chapter 14에서 설명합니다.
- 윤리, 저작권, 보안의 구체 쟁점은 Chapter 15로 넘깁니다.
- 10.3의 생성 결과 위험 설명을 반복하지 않고, 프롬프트 사용 맥락에서 필요한 만큼만 연결했습니다.

## 용어 검토

- `프롬프트(prompt)`, `한계(limit)`, `평가(evaluation)`, `사실성(factuality)`, `근거성(evidence)`, `최신성(recency)`, `안전성(safety)`, `일관성(consistency)`, `환각(hallucination)`, `RAG(retrieval-augmented generation)`, `벡터 검색(vector search)`, `도구 사용(tool use)`, `에이전트(agent)`, `하네스(harness)`를 한영 병기했습니다.
- `평가`를 점수 하나로 환원하지 않고, 작업 목적에 따른 검토 기준으로 설명했습니다.
- `근거성`은 출처 존재뿐 아니라 출처가 실제 주장을 뒷받침하는지 확인하는 문제로 설명했습니다.

## 주의한 오해

- 프롬프트를 잘 쓰면 사실성이 보장된다고 설명하지 않았습니다.
- RAG나 도구 사용(tool use)을 만능 해결책처럼 설명하지 않았습니다.
- hallucination을 모델이 드물게 보이는 예외적 오류로 축소하지 않았습니다.
- Chapter 13, 14, 15의 세부 구조를 12.3에서 미리 설명하지 않았습니다.

## 참고 자료

- Long Ouyang et al., [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155), arXiv, 2022, 확인 날짜: 2026-06-23.
- Pranab Sahoo et al., [A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications](https://arxiv.org/abs/2402.07927), arXiv, 2024, 확인 날짜: 2026-06-23.
- NIST, [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://doi.org/10.6028/NIST.AI.600-1), NIST AI 600-1, 2024, 확인 날짜: 2026-06-23.
- OpenAI, [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering), OpenAI API documentation, 확인 날짜: 2026-06-23.

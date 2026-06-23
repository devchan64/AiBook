# Section 14.3 근거 검토: 에이전트(agent)

## 검토 목적

- 14.3의 중심 질문은 “에이전트(agent)는 RAG와 도구 사용을 포함해 목표를 어떻게 여러 단계 작업 흐름으로 이어 가는가?”입니다.
- 에이전트를 모델 이름이나 단순 챗봇으로 설명하지 않고, 목표(goal), 상태(state), 행동(action), 관찰(observation), 종료 조건(stop condition)을 포함한 실행 구조로 설명하는 것이 목적입니다.
- 14.4의 MCP(Model Context Protocol), 14.5의 하네스(harness)와 평가 실행 환경을 침범하지 않도록 범위를 제한했습니다.

## 확인한 자료

| 자료 | 위치 | 반영 판단 |
| --- | --- | --- |
| Shunyu Yao et al., *ReAct: Synergizing Reasoning and Acting in Language Models*, 2022 | `.tmp/section-14-3-evidence/yao-2022-react.pdf`, `.html` | 추론(reasoning)과 행동(acting)을 번갈아 사용하고, 외부 지식베이스나 환경과 상호작용하는 연구 사례로 반영했습니다. |
| OpenAI, *Agents SDK* | `.tmp/section-14-3-evidence/openai-agents-guide.html` | 에이전트 앱에서 런타임 루프(runtime loop), 상태(state), 오케스트레이션(orchestration), 도구 실행(tool execution), 승인(approval), 관찰 가능성(observability)이 중요하다는 현재 구현 관점으로 반영했습니다. |
| OpenAI, *Function calling* | `.tmp/section-14-1-evidence/openai-function-calling.html` | 도구 호출이 모델을 외부 데이터와 시스템에 연결하는 방식이라는 14.2의 근거를 재사용했습니다. |
| OpenAI, Agents overview URL | `.tmp/section-14-3-evidence/openai-agents-overview.html` | 다운로드했으나 `Page not found` 상태로 확인되어 본문 근거로 사용하지 않았습니다. |

## 본문 반영 기준

- 에이전트(agent)를 `목표를 여러 단계 작업 흐름으로 이어 가는 구조`로 일반화했습니다.
- 핵심 구성요소를 목표(goal), 상태(state), 행동(action), 관찰(observation), 종료 조건(stop condition)으로 정리했습니다.
- ReAct는 에이전트 전체의 표준 정의가 아니라, 추론과 행동을 결합하는 연구 흐름의 사례로만 사용했습니다.
- OpenAI Agents SDK 문서는 특정 제품/개발 문서이므로, “현재 구현 관점에서 서버가 오케스트레이션, 도구 실행, 상태, 승인을 소유할 수 있다”는 근거로 제한해 사용했습니다.
- Codex는 사용자의 책에서 중요한 도구이므로 예시로 언급했지만, Codex 사용법 설명이나 제품 문서로 확장하지 않았습니다.

## Section 경계 검토

- 14.3은 에이전트의 작업 흐름 구조에 집중합니다.
- 14.4의 MCP(Model Context Protocol)는 다음 절로 예고만 했습니다.
- 14.5의 하네스(harness), 로그(log), 평가(evaluation), 재현성(reproducibility)은 필요성만 언급했습니다.
- 14.6의 비용(cost), 지연 시간(latency), 운영(operation)은 다루지 않았습니다.
- 15장의 보안(security), 개인정보(privacy), 윤리(ethics)는 권한과 승인 필요성 수준에서만 언급했습니다.

## 용어 검토

- `에이전트(agent)`, `목표(goal)`, `작업 흐름(workflow)`, `상태(state)`, `행동(action)`, `관찰(observation)`, `종료 조건(stop condition)`, `오케스트레이션(orchestration)`, `권한(permission)`, `승인(approval)`, `검증(validation)`, `정책(policy)`, `로그(log)`를 한영 병기했습니다.
- `추론(reasoning)`은 5장에서 정리한 inference와 혼동하지 않도록, ReAct 문맥에서만 reasoning으로 병기했습니다.
- `에이전트`를 무제한 자율 실행 또는 인간 대체 주체로 설명하지 않았습니다.

## 주의한 오해

- 에이전트가 RAG와 같은 말이라고 설명하지 않았습니다.
- 도구 사용(tool use)이 곧 에이전트라고 설명하지 않았습니다.
- 모델이 직접 외부 세계를 바꾼다고 설명하지 않았습니다.
- ReAct의 reasoning trace를 실제 서비스에서 그대로 사용자에게 공개해야 한다고 설명하지 않았습니다.
- MCP를 에이전트 자체로 설명하지 않았습니다.
- Codex를 일반 AI 에이전트의 유일한 표준 사례처럼 설명하지 않았습니다.

## 참고 자료

- Shunyu Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629), arXiv, 2022, 확인 날짜: 2026-06-23.
- OpenAI, [Agents SDK](https://developers.openai.com/api/docs/guides/agents), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Function calling](https://developers.openai.com/api/docs/guides/function-calling), OpenAI API Docs, 확인 날짜: 2026-06-23.

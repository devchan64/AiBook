# Section 14.2 근거 검토: RAG와 도구 사용의 위치

## 검토 목적

- 14.2의 중심 질문은 “RAG와 도구 사용(tool use)은 모두 모델 밖의 자원을 쓰는데, AI 서비스 안에서 어떻게 다른가?”입니다.
- 14.1이 모델, 앱, 데이터, 도구의 지도를 제공했으므로, 14.2는 RAG와 도구 사용의 역할 차이를 구분했습니다.

## 확인한 자료

기존에 내려받은 자료를 재사용했습니다.

| 자료 | 위치 | 반영 판단 |
| --- | --- | --- |
| Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, 2020 | `.tmp/section-13-3-evidence/lewis-2020-retrieval-augmented-generation.pdf`, `.html` | RAG를 외부 검색 자료를 생성 입력에 결합하는 구조로 설명하는 근거로 사용했습니다. |
| OpenAI, *Function calling* | `.tmp/section-14-1-evidence/openai-function-calling.html` | 도구 호출이 모델을 외부 데이터와 시스템에 연결하는 방식이라는 근거로 사용했습니다. |
| OpenAI, *Text generation* | `.tmp/section-14-1-evidence/openai-text-generation.html` | 모델 입력, 출력, 프롬프트 구성과 도구 호출 결과가 앱 흐름에 들어가는 배경 근거로 사용했습니다. |

## 본문 반영 기준

- RAG(retrieval-augmented generation)는 외부 자료를 검색해 입력 맥락(context)에 붙이는 구조로 설명했습니다.
- 도구 사용(tool use)은 외부 시스템의 기능을 호출해 조회하거나 행동을 실행하는 구조로 설명했습니다.
- 두 구조의 차이를 `자료를 읽는 것`과 `행동을 실행하는 것`으로 일반화했습니다.
- RAG와 도구 사용이 함께 쓰일 수 있음을 업무 예시로 설명했습니다.
- 도구 사용에는 권한(permission), 승인(approval), 검증(validation), 실행 로그(log)가 필요하다는 점을 짧게 반영했습니다.

## Section 경계 검토

- 14.2는 RAG와 도구 사용의 위치 비교에 집중합니다.
- 14.3의 에이전트(agent) 구조는 예고만 하고 자세히 설명하지 않았습니다.
- 14.4의 MCP(Model Context Protocol)는 언급만 하고, 도구 연결 표준화 설명은 넘겼습니다.
- 14.5의 하네스(harness), 평가 실행 환경, 로그 구조는 길게 다루지 않았습니다.
- 15장의 보안, 개인정보, 윤리 쟁점은 권한과 승인 필요성만 언급하고 확장하지 않았습니다.

## 용어 검토

- `RAG(retrieval-augmented generation)`, `도구 사용(tool use)`, `검색(retrieval)`, `생성(generation)`, `맥락(context)`, `모델(model)`, `앱(application)`, `서버(server)`, `권한(permission)`, `승인(approval)`, `검증(validation)`, `실행 로그(log)`, `에이전트(agent)`를 한영 병기했습니다.
- `tool`은 단순 버튼이나 UI 기능이 아니라 외부 시스템의 기능을 호출하는 실행 수단으로 제한했습니다.
- `RAG`를 도구 사용의 한 종류로 단정하지 않고, 데이터 검색과 입력 보강 구조로 설명했습니다.

## 주의한 오해

- RAG가 외부 시스템의 상태를 직접 바꾸는 구조라고 설명하지 않았습니다.
- 도구 사용이 항상 에이전트와 같다고 설명하지 않았습니다.
- 모델이 직접 외부 API를 실행한다고 설명하지 않았습니다.
- 도구 호출을 승인 없이 항상 실행해도 된다고 설명하지 않았습니다.
- RAG와 도구 사용을 대립 관계로 설명하지 않고 함께 쓰일 수 있음을 반영했습니다.

## 참고 자료

- Patrick Lewis et al., [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401), arXiv, 2020, 확인 날짜: 2026-06-23.
- OpenAI, [Function calling](https://developers.openai.com/api/docs/guides/function-calling), OpenAI API Docs, 확인 날짜: 2026-06-23.
- OpenAI, [Text generation](https://developers.openai.com/api/docs/guides/text), OpenAI API Docs, 확인 날짜: 2026-06-23.

# Section 14.4 근거 검토: MCP(Model Context Protocol)

## 검토 목적

- 14.4의 중심 질문은 “MCP(Model Context Protocol)는 에이전트가 외부 도구와 데이터에 연결되는 방식을 어떻게 표준화하는가?”입니다.
- MCP를 모델(model), 에이전트(agent), 하네스(harness)와 섞지 않고 연결 프로토콜(protocol)로 설명하는 것이 목적입니다.
- 14.5의 하네스(harness), 평가(evaluation), 로그(log) 논의를 침범하지 않도록 범위를 제한했습니다.

## 확인한 자료

| 자료 | 위치 | 반영 판단 |
| --- | --- | --- |
| Model Context Protocol, *What is the Model Context Protocol (MCP)?* | `.tmp/section-14-4-evidence/mcp-intro.html` | MCP를 AI 애플리케이션과 외부 시스템을 연결하는 공개 표준으로 설명하는 근거로 사용했습니다. |
| Model Context Protocol, *Architecture overview* | `.tmp/section-14-4-evidence/mcp-architecture.html` | 호스트(host), 클라이언트(client), 서버(server), 데이터 계층(data layer), 전송 계층(transport layer), 도구(tools), 리소스(resources), 프롬프트(prompts) 설명의 근거로 사용했습니다. |
| Model Context Protocol, *Security Best Practices* | `.tmp/section-14-4-evidence/mcp-security-best-practices.html` | MCP 연결이 보안과 신뢰 경계 문제를 동반한다는 주의점으로만 짧게 반영했습니다. |

## 본문 반영 기준

- MCP를 `AI 앱과 외부 시스템 사이의 연결 방식을 표준화하는 프로토콜`로 일반화했습니다.
- 공식 문서의 USB-C 비유는 직접 중심 표현으로 삼지 않고, 입문 설명에서는 `공통 연결 규칙`으로 풀어 썼습니다.
- 호스트(host), 클라이언트(client), 서버(server)의 역할을 구분했습니다.
- 도구(tools), 리소스(resources), 프롬프트(prompts)를 구분해 14.2의 RAG와 도구 사용 차이에 연결했습니다.
- `tools/list`, `tools/call`은 구현 상세가 아니라 발견(discovery)과 호출(call)의 직관을 설명하는 예로만 사용했습니다.
- 보안은 MCP 서버 연결의 신뢰 경계와 승인 필요성을 보여 주는 수준으로 제한했습니다.

## Section 경계 검토

- 14.4는 MCP의 기본 역할과 연결 구조에 집중합니다.
- MCP 서버 구현, SDK 코드, JSON-RPC 메시지 상세, OAuth 인증 흐름은 다루지 않았습니다.
- 14.5의 하네스(harness), 실행 로그(log), 평가(evaluation), 재현성(reproducibility)은 다음 절로 넘겼습니다.
- 14.6의 비용(cost), 지연 시간(latency), 운영(operation)은 다루지 않았습니다.
- 15장의 보안(security), 개인정보(privacy), 윤리(ethics)는 위험 예고 수준으로만 다뤘습니다.

## 용어 검토

- `MCP(Model Context Protocol)`, `프로토콜(protocol)`, `호스트(host)`, `클라이언트(client)`, `서버(server)`, `도구(tools)`, `리소스(resources)`, `프롬프트(prompts)`, `발견(discovery)`, `호출(call)`, `권한(permission)`, `승인(approval)`, `검증(validation)`, `신뢰 경계(trust boundary)`를 한영 병기했습니다.
- `client`는 일반 웹 브라우저 클라이언트와 혼동될 수 있으므로 MCP 문맥에서 특정 서버와 연결을 유지하는 구성요소로 설명했습니다.
- `server`는 원격 서버만이 아니라 로컬 프로그램일 수도 있음을 반영했습니다.

## 주의한 오해

- MCP를 에이전트(agent) 자체로 설명하지 않았습니다.
- MCP를 모델(model)의 내부 기능으로 설명하지 않았습니다.
- MCP가 연결된 도구의 안전성, 권한, 승인, 평가를 자동으로 보장한다고 설명하지 않았습니다.
- MCP의 보안 쟁점을 깊게 확장해 15장의 보안 도메인을 침범하지 않았습니다.
- `프롬프트(prompts)`를 일반 프롬프트 작성 기법 전체로 확장하지 않고, MCP 서버가 제공할 수 있는 재사용 템플릿으로 제한했습니다.

## 참고 자료

- Model Context Protocol, [What is the Model Context Protocol (MCP)?](https://modelcontextprotocol.io/docs/getting-started/intro), 확인 날짜: 2026-06-23.
- Model Context Protocol, [Architecture overview](https://modelcontextprotocol.io/docs/learn/architecture), 확인 날짜: 2026-06-23.
- Model Context Protocol, [Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices), 확인 날짜: 2026-06-23.

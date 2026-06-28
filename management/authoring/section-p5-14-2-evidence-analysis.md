# P5-14.2 근거 검토 메모

## 절의 역할

- function calling을 tool use의 구조화 방식으로 설명한다.
- 자연어 요청과 구조화된 실행 요청의 차이를 정리한다.

## 이번 절의 핵심 주장

- 함수 호출은 도구 이름과 인자를 구조적으로 표현하는 방식이다.
- 구조화는 검증 가능성과 통제 가능성을 높인다.
- 함수 호출만으로 실행 안전성이 자동 보장되지는 않는다.

## 반영한 근거

- OpenAI의 function calling 문서
- Anthropic의 tool use 문서
- LLM application engineering 교육 자료

## 집필 판단

- JSON schema 전체 세부보다 이름/인자/결과 구조를 먼저 설명했다.
- agent, MCP로 넘어가기 위한 연결 절로 배치했다.

## 제외한 내용

- schema 문법 전체
- SDK별 API 세부

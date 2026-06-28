# P5-16.2 근거 검토 메모

## 절의 역할

- harness를 agent 실행을 감싸는 운영 장치로 설명한다.
- trace, log, eval, replay의 중요성을 초심자 수준에서 정리한다.

## 이번 절의 핵심 주장

- harness는 실행을 감싸고 기록하고 평가하는 운영 구조다.
- MCP는 연결 인터페이스, harness는 실행 관리라는 점에서 다르다.
- harness는 디버깅, 재현성, 승인, 개선의 기반이다.

## 반영한 근거

- OpenAI의 agents/evaluation 관련 문서
- 관련 agent engineering 및 observability 자료

## 집필 판단

- 단일 도구명처럼 보이지 않도록 운영 패턴 관점으로 설명했다.
- 평가 장으로 자연스럽게 이어지게 구성했다.

## 제외한 내용

- 관측성 스택 전체
- 테스트 프레임워크 세부

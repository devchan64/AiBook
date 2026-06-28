# P5-15.2 근거 검토 메모

## 절의 역할

- plan, action, observation, stop condition을 분리해 agent loop를 설명한다.
- 단계별 실패 분석의 기준을 만든다.

## 이번 절의 핵심 주장

- agent는 계획, 행동, 관찰, 종료 판단의 반복 구조를 가진다.
- 이 구분은 디버깅과 평가를 위해 중요하다.
- stop condition이 없으면 비용과 실패가 커질 수 있다.

## 반영한 근거

- ReAct 논문
- OpenAI Agents 문서
- 관련 agent engineering 자료

## 집필 판단

- 이론 구분에 그치지 않고 코딩/문서 조사 사례로 연결했다.
- MCP, harness, evaluation으로 이어지는 연결 절로 배치했다.

## 제외한 내용

- 장기 메모리 설계
- planner/executor 세부 패턴 비교

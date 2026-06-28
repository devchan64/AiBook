# P5-18.2 근거 검토 메모

## 절의 역할

- 운영 중 실패를 모델 실패와 시스템 실패로 나누어 설명한다.
- trace, retry, fallback, approval의 역할을 정리한다.

## 이번 절의 핵심 주장

- AI 서비스 실패는 여러 층위에서 발생한다.
- 모델 실패와 시스템 실패를 구분해야 한다.
- trace, retry, fallback, approval은 핵심 운영 장치다.

## 반영한 근거

- OpenAI agents/evaluation/observability 문서
- 관련 LLM application engineering 운영 자료

## 집필 판단

- 장애 대응을 추상화하지 않고 검색/도구/지연 시간 사례로 분리했다.
- Part 6 프로젝트와 직접 연결되도록 마무리했다.

## 제외한 내용

- 온콜 조직 운영
- 장애 등급 체계 전체

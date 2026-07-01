# P5-4.2 근거 검토 메모

## 절의 역할

- attention과 context window를 구분해 설명한다.
- 이후 RAG와 서비스 구조 설명에 필요한 문맥 길이 관점을 준비한다.

## 이번 절의 핵심 주장

- attention은 윈도우 안에서 관련도를 계산하는 구조다.
- context window는 한 번에 들어오는 토큰 범위를 제한한다.
- 문맥 길이 제한은 비용, 지연 시간, RAG 설계와 직접 연결된다.

## 제외한 내용

- RoPE, ALiBi 비교
- sparse attention 계열 세부 구조

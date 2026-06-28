# P5-4.2 근거 검토 메모

## 절의 역할

- attention과 context window를 구분해 설명한다.
- 이후 RAG와 서비스 구조 설명에 필요한 문맥 길이 관점을 준비한다.

## 이번 절의 핵심 주장

- attention은 윈도우 안에서 관련도를 계산하는 구조다.
- context window는 한 번에 들어오는 토큰 범위를 제한한다.
- 문맥 길이 제한은 비용, 지연 시간, RAG 설계와 직접 연결된다.

## 반영한 근거

- Vaswani et al., `Attention Is All You Need`
- Raffel et al., `Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer`
- OpenAI API Docs의 입력 길이/문맥 관련 설명

## 집필 판단

- long-context 최적화 기법은 넣지 않고, 초심자 기준의 서비스 관점 설명을 우선했다.
- RAG 필요성을 context window 제약과 직접 연결했다.

## 제외한 내용

- RoPE, ALiBi 비교
- sparse attention 계열 세부 구조

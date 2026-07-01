# P5-4.1 근거 검토 메모

## 절의 역할

- Part 4의 Transformer 설명을 Part 5의 LLM 관점으로 다시 정리한다.
- 토큰, 임베딩, attention, next-token prediction을 하나의 구조 흐름으로 묶는다.

## 이번 절의 핵심 주장

- LLM에서 Transformer는 토큰 임베딩을 입력으로 받아 self-attention과 반복 블록으로 표현을 정제하고 다음 토큰 점수로 이어지는 구조다.
- Part 4의 구조 설명은 Part 5에서 생성 모델 구조로 다시 읽어야 한다.

## 제외한 내용

- KV cache
- serving optimization
- multi-head attention 수식

# P4-14.1 Transformer의 기본 구성 근거 메모

## Section 역할

- Part 4 Module 4 Chapter 14의 첫 번째 절입니다.
- self-attention 이후 Transformer block의 기본 구성 요소를 큰 그림으로 정리합니다.
- Part 5 LLM 구조 설명을 위한 최소 공통 블록을 제공합니다.

## 핵심 주장

1. Transformer는 self-attention, feed-forward, residual connection, layer normalization의 조합으로 설명할 수 있다.
2. self-attention은 문맥 관계를 읽고, feed-forward는 위치별 표현을 다시 가공하는 역할로 설명할 수 있다.
3. residual과 layer normalization은 깊은 학습을 안정화하는 장치로 설명할 수 있다.
4. Transformer는 attention 중심 sequence modeling의 대표 구조다.

## 근거 출처

### 1) Attention Is All You Need

- 문서: `Attention Is All You Need`
- 저자: Ashish Vaswani et al.
- 매체: NeurIPS 2017
- 확인 날짜: 2026-06-29

### 2) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

### 3) Illustrated Transformer

- 문서: `The Illustrated Transformer`
- 저자: Jay Alammar
- 확인 날짜: 2026-06-29
- URL: https://jalammar.github.io/illustrated-transformer/

## 제외한 내용

- positional encoding detail
- decoder masking detail
- architecture variants

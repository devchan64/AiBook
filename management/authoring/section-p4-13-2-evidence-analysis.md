# P4-13.2 self-attention으로 이어지는 흐름 근거 메모

## Section 역할

- Part 4 Module 4 Chapter 13의 두 번째 절입니다.
- attention을 self-attention으로 확장해, Transformer 직전의 핵심 발상을 정리합니다.
- Part 5의 LLM 설명과 직접 연결되는 준비 절입니다.

## 핵심 주장

1. self-attention은 같은 시퀀스 내부 토큰들이 서로를 참고해 표현을 다시 계산하는 방식으로 설명할 수 있다.
2. 이는 RNN식 순차 상태 전달과 다른 계산 감각을 제공한다.
3. self-attention은 먼 위치 참조와 병렬 계산에 유리한 방향을 보여 준다.
4. Transformer는 self-attention을 핵심 계산 장치로 삼는 구조로 이어진다.

## 근거 출처

### 1) Attention Is All You Need

- 문서: `Attention Is All You Need`
- 저자: Ashish Vaswani et al.
- 매체: NeurIPS 2017
- 확인 날짜: 2026-06-29

### 2) Bahdanau et al. 2015

- 문서: `Neural Machine Translation by Jointly Learning to Align and Translate`
- 저자: Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio
- 매체: ICLR 2015
- 확인 날짜: 2026-06-29

### 3) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

## 제외한 내용

- QKV math
- positional encoding details
- multi-head implementation

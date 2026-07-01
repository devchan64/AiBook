# P4-12.1 RNN, LSTM, GRU의 필요성 근거 메모

## Section 역할

- Part 4 Module 4 Chapter 12의 첫 번째 절입니다.
- 이미지 이후 순차 데이터로 관심사를 옮기며 RNN 계열의 필요성을 설명합니다.
- 다음 절의 장기 의존성 문제를 위한 도입 절입니다.

## 핵심 주장

1. 순차 데이터에서는 현재 입력만이 아니라 순서와 이전 문맥이 중요하다.
2. RNN은 이전 상태를 이어받아 현재 입력을 처리하려는 기본 아이디어로 설명할 수 있다.
3. LSTM과 GRU는 더 오래 기억하기 어려운 문제를 더 잘 다루기 위해 등장한 구조로 설명할 수 있다.
4. RNN 계열은 Transformer 이전 순차 모델링의 핵심 기준점이다.

## 근거 출처

### 1) Rumelhart, Hinton, Williams 1986

- 문서: `Learning representations by back-propagating errors`
- 저자: David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams
- 매체: Nature, 1986
- 확인 날짜: 2026-06-29

### 2) LSTM paper

- 문서: `Long Short-Term Memory`
- 저자: Sepp Hochreiter, Jürgen Schmidhuber
- 매체: Neural Computation, 1997
- 확인 날짜: 2026-06-29

### 3) GRU / encoder-decoder paper

- 문서: `Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation`
- 저자: Kyunghyun Cho et al.
- 매체: arXiv, 2014
- 확인 날짜: 2026-06-29

## 제외한 내용

- BPTT derivation
- gate equations
- sequence-to-sequence architecture detail

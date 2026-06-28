# P4-12.2 장기 의존성 근거 메모

## Section 역할

- Part 4 Module 4 Chapter 12의 두 번째 절입니다.
- RNN 계열의 필요성 다음에, 왜 오래전 정보를 유지하기 어려운지 핵심 문제를 분리해 설명합니다.
- Attention 장으로 넘어가기 위한 문제 제기 절입니다.

## 핵심 주장

1. 장기 의존성은 오래전 정보가 현재 판단에 중요하지만 충분히 유지되지 않는 문제로 설명할 수 있다.
2. 기본 RNN에서는 시간이 길어질수록 오래전 정보가 희미해지기 쉽다는 직관적 설명이 가능하다.
3. LSTM/GRU는 이 문제를 더 잘 다루기 위해 등장한 구조로 설명할 수 있다.
4. attention은 이 문제에 더 직접적으로 응답하는 다음 발상으로 연결할 수 있다.

## 근거 출처

### 1) Bengio et al. 1994

- 문서: `Learning Long-Term Dependencies with Gradient Descent is Difficult`
- 저자: Yoshua Bengio, Patrice Simard, Paolo Frasconi
- 매체: IEEE Transactions on Neural Networks, 1994
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - long-term dependency difficulty의 고전적 문제 제기

### 2) LSTM paper

- 문서: `Long Short-Term Memory`
- 저자: Sepp Hochreiter, Jürgen Schmidhuber
- 매체: Neural Computation, 1997
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - long memory management motivation

### 3) Deep Learning

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - RNN difficulty and gradient intuition

## 집필 판단

- 수식보다 상태 희석(state decay) 비유를 우선했습니다.
- vanishing gradient라는 말을 직접 전개하지 않고도 초심자가 문제 구조를 이해할 수 있게 구성했습니다.
- attention 장과의 연결을 위해 `기억 유지`에서 `직접 참조`로 관점이 이동한다는 흐름을 강조했습니다.

## 제외한 내용

- BPTT derivation
- gradient explosion details
- gated cell equations

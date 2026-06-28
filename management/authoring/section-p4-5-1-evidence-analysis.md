# P4-5.1 역전파의 직관 근거 메모

## Section 역할

- Part 4 Module 2 Chapter 5의 첫 번째 절입니다.
- 손실 함수 다음에, 그 손실이 각 파라미터에 어떻게 연결되는지 설명하는 절입니다.
- 역전파를 학습 전체가 아니라 gradient 계산 절차로 구분해 주는 입문 역할을 합니다.

## 핵심 주장

1. 역전파는 손실이 각 가중치에 미치는 영향을 뒤에서 앞으로 효율적으로 계산하는 절차로 설명할 수 있다.
2. 역전파는 학습 전체가 아니라 gradient computation 단계이며, 실제 업데이트는 optimizer가 담당한다.
3. 역전파는 신경망의 합성 함수 구조에 연쇄 법칙(chain rule)을 적용한 절차로 이해할 수 있다.
4. 다층 신경망의 학습 가능성을 널리 보여 준 역사적 전환점으로 Rumelhart, Hinton, Williams 1986을 언급할 수 있다.

## 근거 출처

### 1) Rumelhart, Hinton, Williams 1986

- 문서: `Learning representations by back-propagating errors`
- 저자: David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams
- 매체: Nature, 1986
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - backpropagation이 다층 신경망 학습의 실제 전환점으로 널리 알려진 대표 문헌

### 2) Werbos 1974

- 문서: `Beyond Regression: New Tools for Prediction and Analysis in the Behavioral Sciences`
- 저자: Paul J. Werbos
- 기관: Harvard University doctoral thesis
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - backpropagation 관련 더 이른 역사적 맥락

### 3) Deep Learning book

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - backpropagation을 gradient 계산 절차로 설명하는 교재 기준
  - chain rule과 multilayer network 학습 연결

## 집필 판단

- 이 절은 행렬 미분을 전개하지 않고, 책임 분해와 방향 신호라는 직관으로 먼저 설명했습니다.
- Python 예제는 단일 가중치 사례로 축소해, gradient의 부호가 어떤 업데이트 방향을 뜻하는지 읽게 했습니다.
- 역사 설명은 Rumelhart-Hinton-Williams 1986을 중심에 두되, Werbos 1974를 배경으로 보강하는 수준으로 제한했습니다.

## 제외한 내용

- full matrix derivation
- auto-diff general theory
- backprop through time

이 내용은 P4-5.2나 후속 심화 절에서 확장할 수 있습니다.

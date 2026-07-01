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

### 2) Werbos 1974

- 문서: `Beyond Regression: New Tools for Prediction and Analysis in the Behavioral Sciences`
- 저자: Paul J. Werbos
- 기관: Harvard University doctoral thesis
- 확인 날짜: 2026-06-29

### 3) Deep Learning book

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29

## 제외한 내용

- full matrix derivation
- auto-diff general theory
- backprop through time

이 내용은 P4-5.2나 후속 심화 절에서 확장할 수 있습니다.

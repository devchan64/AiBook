# P4-4.1 손실 함수 근거 메모

## Section 역할

- Part 4 Module 2 Chapter 4의 첫 번째 절입니다.
- 활성화 함수 다음에, 학습 계산의 중심 기준인 손실 함수(loss function)를 소개합니다.
- 손실과 metric의 차이를 초심자에게 다시 분명히 하면서, P4-5 역전파와 P4-7 옵티마이저의 기반을 만드는 절입니다.

## 핵심 주장

1. 손실 함수는 모델 예측과 목표 사이의 어긋남을 하나의 숫자로 만드는 학습 기준으로 설명할 수 있다.
2. 손실 함수는 metric과 역할이 다르며, 학습용 내부 기준과 사람이 읽는 외부 성능 기준을 구분해야 한다.
3. 딥러닝 학습은 손실을 줄이는 방향으로 파라미터를 조정하는 최적화 문제로 읽는 것이 적절하다.
4. 학습 손실 감소는 중요하지만, 그것만으로 일반화를 보장하지는 않는다.

## 근거 출처

### 1) Deep Learning book

- 문서: `Deep Learning`
- 저자: Ian Goodfellow, Yoshua Bengio, Aaron Courville
- 출판: MIT Press, 2016
- URL: https://www.deeplearningbook.org/
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - loss function과 optimization을 딥러닝 학습의 핵심 축으로 설명하는 교재 기준

### 2) Bishop - Pattern Recognition and Machine Learning

- 문서: `Pattern Recognition and Machine Learning`
- 저자: Christopher M. Bishop
- 출판: Springer, 2006
- 확인 날짜: 2026-06-29
- 반영 포인트:
  - error/loss 개념과 objective function을 머신러닝 전반의 학습 기준으로 보는 표준 교재 맥락

## 집필 판단

- 이 절은 특정 손실 공식보다 손실의 역할을 먼저 설명하는 데 집중했습니다.
- Part 3에서 다룬 metric과의 차이를 다시 강조해, 초심자가 손실과 정확도를 혼동하지 않게 했습니다.
- Python 예제는 mean squared error 직관을 보여 주는 최소한의 계산으로 제한했습니다.

## 제외한 내용

- cross-entropy, KL divergence의 세부 수학
- gradient derivation
- regularized objective와 composite loss

이 내용은 P4-4.2와 이후 학습 계산 절에서 확장할 수 있습니다.

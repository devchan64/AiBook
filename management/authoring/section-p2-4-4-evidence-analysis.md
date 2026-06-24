# P2-4.4 근거 검토: 학습에서 미분이 필요한 이유

## 작성 대상

- 본문: `docs/parts/part-02/chapter-04/section-04.md`
- 주제: 학습(training), 손실(loss), 파라미터(parameter), 미분(derivative), 그래디언트(gradient)의 연결
- 작성일: 2026-06-24

## Section 범위

이 절은 P2-4.3의 미분과 그래디언트 설명을 받아, AI 학습에서 미분이 왜 필요한지 연결하는 절이다.

다음 내용은 이 절에서 깊게 다루지 않는다.

- 경사하강법(gradient descent)의 반복 업데이트 공식
- 옵티마이저(optimizer)의 종류
- 역전파(backpropagation)의 계산 절차
- 신경망의 계층별 미분 계산
- 실제 딥러닝 프레임워크의 자동 미분(automatic differentiation)

위 내용은 P2-6장, 딥러닝 파트, 실습 파트에서 이어서 다루는 것이 적절하다.

## 확인한 근거

### OpenStax Calculus Volume 1, 3.1 Defining the Derivative

- URL: https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative
- 로컬 확인 파일: `.tmp/section-p2-4-1-evidence/openstax-calculus-3-1-defining-derivative.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 도함수는 평균 변화율을 극한으로 좁혀 순간 변화율을 보는 흐름에서 도입된다.
- 본문에서는 이 엄밀한 정의를 반복하지 않고, “한 파라미터를 조금 바꿨을 때 손실이 어떻게 변하는가”라는 학습 문맥으로 연결했다.

### OpenStax Calculus Volume 3, 4.6 Directional Derivatives and the Gradient

- URL: https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient
- 로컬 확인 파일: `.tmp/section-p2-4-3-evidence/openstax-calculus-4-6-directional-derivatives-gradient.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 그래디언트는 편미분을 성분으로 갖는 벡터로 정의된다.
- 그래디언트는 함수가 가장 빠르게 증가하는 방향과 연결되며, 반대 방향은 감소 방향을 이해하는 데 쓰인다.
- 본문에서는 방향도함수 계산을 생략하고, 손실을 줄이는 방향을 이해하기 위한 입문적 설명으로 제한했다.

### Deep Learning, Chapter 8. Optimization for Training Deep Models

- URL: https://www.deeplearningbook.org/contents/optimization.html
- 로컬 확인 파일: `.tmp/section-p2-4-4-evidence/deeplearningbook-optimization.html`
- 확인 날짜: 2026-06-24

검토 내용:

- 딥러닝 학습은 최적화 문제와 밀접하게 연결된다.
- 신경망 학습에서는 파라미터를 찾아 비용 함수(cost function) 또는 손실에 해당하는 목적을 줄이는 흐름이 중요하다.
- 머신러닝에서 학습에 쓰이는 최적화는 단순한 수학적 최적화와 달리, 훈련 데이터와 일반화 성능의 관계를 함께 고려한다.

본문 반영 방식:

- 본문은 “파라미터를 조정해 손실을 줄인다”는 큰 흐름만 사용했다.
- 딥러닝 최적화의 난점, 일반화, SGD, 모멘텀, 적응형 학습률 등은 다루지 않았다.

## 표현 검토

### 학습

안전한 표현:

```text
학습은 파라미터를 조정해 손실을 줄이는 과정으로 볼 수 있다.
```

주의할 표현:

```text
학습은 미분만 하면 자동으로 정답을 찾는 과정이다.
```

미분과 그래디언트는 방향 정보를 제공하지만, 실제 학습 성능은 데이터, 모델 구조, 초기값, 학습률, 옵티마이저, 일반화 조건에 영향을 받는다.

### 손실

본문에서는 손실(loss)을 모델 예측이 목표와 얼마나 다른지 숫자로 표현한 값으로 설명했다. 이는 입문적 설명이며, 실제 손실 함수의 선택은 문제 유형과 학습 목적에 따라 달라진다.

### 미분과 그래디언트

본문에서는 미분을 한 파라미터에 대한 손실 변화 정보로, 그래디언트를 여러 파라미터에 대한 변화 정보 묶음으로 설명했다.

주의할 점:

- 그래디언트가 항상 전역 최적해를 보장한다고 쓰지 않는다.
- 그래디언트는 현재 위치 주변의 지역적 변화 정보라는 점을 유지한다.
- 손실이 줄어드는 방향을 설명하되, 실제 업데이트 공식은 P2-6장으로 넘긴다.

### 역전파

본문에서는 역전파(backpropagation)를 “그래디언트를 효율적으로 계산하는 절차”로만 예고했다.

주의할 점:

- 역전파를 학습 전체와 동일시하지 않는다.
- 연쇄 법칙(chain rule)과 계산 그래프(computation graph)의 상세 설명은 딥러닝 파트로 넘긴다.

## 후속 작성 지점

- P2-6.1에서 최적화(optimization)를 “좋은 값을 찾는 문제”로 정리한다.
- P2-6.2에서 손실 함수(loss function)와 목적 함수(objective function)의 관계를 구체화한다.
- P2-6.3에서 경사하강법(gradient descent)의 반복 업데이트와 학습률(learning rate)을 설명한다.
- 딥러닝 파트에서 역전파(backpropagation), 연쇄 법칙(chain rule), 계산 그래프(computation graph)를 다시 다룬다.

# P2-4.3 근거 검토: 미분(derivative)과 그래디언트(gradient)

## 작성 대상

- 본문: `docs/parts/part-02/chapter-04/section-03.md`
- 주제: 미분(derivative), 편미분(partial derivative), 그래디언트(gradient)의 입문적 연결
- 작성일: 2026-06-24

## Section 범위

이 절은 P2-4.2의 변화율과 기울기 설명을 받아, 단일 입력의 미분과 여러 입력의 그래디언트를 구분하는 절이다.

다음 내용은 이 절에서 깊게 다루지 않는다.

- 미분 공식의 체계적 암기
- 연쇄 법칙(chain rule)의 상세 계산
- 야코비안(Jacobian), 헤시안(Hessian)
- 경사하강법(gradient descent)의 업데이트 공식
- 역전파(backpropagation)

위 내용은 P2-4.4, P2-6장, 딥러닝 파트에서 이어서 다루는 것이 적절하다.

## 확인한 근거

### OpenStax Calculus Volume 1, 3.1 Defining the Derivative

- URL: https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative
- 로컬 확인 파일: `.tmp/section-p2-4-1-evidence/openstax-calculus-3-1-defining-derivative.html`
- 확인 날짜: 2026-06-24

검토 내용:

- OpenStax는 도함수를 평균 변화율의 극한과 접선의 기울기 흐름으로 도입한다.
- 본문에서는 엄밀한 정의를 그대로 전개하지 않고, “한 입력에 대한 순간 변화율”이라는 입문적 해석으로 제한했다.

### OpenStax Calculus Volume 3, 4.6 Directional Derivatives and the Gradient

- URL: https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient
- 로컬 확인 파일: `.tmp/section-p2-4-3-evidence/openstax-calculus-4-6-directional-derivatives-gradient.html`
- 확인 날짜: 2026-06-24

검토 내용:

- OpenStax는 여러 변수 함수에서 편미분과 방향도함수(directional derivative)를 다룬 뒤 그래디언트를 정의한다.
- 그래디언트는 편미분을 성분으로 갖는 벡터로 정의된다.
- 그래디언트는 방향도함수와 연결되며, 함수가 가장 빠르게 증가하는 방향과 관련된 성질을 갖는다.

본문 반영 방식:

- 본문에서는 방향도함수와 등위곡선(level curve)을 깊게 설명하지 않았다.
- 그래디언트를 “여러 편미분을 모은 벡터”로 소개하고, AI 학습에서는 손실이 각 파라미터 방향으로 어떻게 변하는지 보는 언어로 연결했다.

## 표현 검토

### 미분

안전한 표현:

```text
미분은 한 입력에 대한 순간 변화율로 볼 수 있다.
```

주의할 표현:

```text
미분은 항상 기울기다.
```

기울기는 단일 변수 함수 그래프에서 미분을 직관적으로 설명하는 좋은 표현이지만, 일반적인 미분 개념 전체를 모두 덮지는 않는다.

### 미분계수와 도함수

본문에서는 미분계수를 특정 지점의 순간 변화율, 도함수를 각 지점의 순간 변화율을 알려 주는 함수로 설명했다. 이는 초심자용 구분이며, 엄밀한 수학 정의는 이후 고급 내용에서 더 정리할 수 있다.

### 편미분

편미분(partial derivative)은 여러 입력 중 하나를 바꿨을 때의 변화율로 설명했다. 다른 변수는 고정하고 하나의 변수에 대한 변화율을 본다는 설명은 후속 절에서 더 보강할 수 있다.

### 그래디언트

그래디언트(gradient)는 편미분을 모은 벡터로 설명했다. “가장 빠르게 증가하는 방향”이라는 성질도 언급했지만, 방향도함수와 내적 계산은 깊게 다루지 않았다.

AI 문맥에서는 손실(loss)을 줄이기 위해 그래디언트의 반대 방향을 생각한다는 직관을 소개했다. 실제 업데이트 공식과 학습률은 경사하강법 절로 넘겼다.

## 후속 작성 지점

- P2-4.4에서 학습에서 미분이 필요한 이유를 설명할 때, `손실 함수 -> 파라미터 -> 그래디언트 -> 업데이트 방향` 흐름을 더 명확히 연결한다.
- P2-6.3에서 경사하강법을 다룰 때, 그래디언트의 반대 방향과 학습률을 공식화한다.
- 딥러닝 파트에서 역전파를 다룰 때, 편미분과 연쇄 법칙을 다시 참조한다.

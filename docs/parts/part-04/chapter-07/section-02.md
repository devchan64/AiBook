# P4-7.2 SGD, Adam의 직관

P4-7.1에서는 옵티마이저(optimizer)를 `gradient를 실제 파라미터 업데이트로 바꾸는 규칙`이라고 설명했습니다. 여기서 다음 질문이 바로 이어집니다.

그렇다면 실제로 많이 언급되는 SGD와 Adam은 무엇이 다르며, 왜 둘 다 계속 배우는가?

이 절은 그 질문에 답합니다.

SGD는 단순한 기본 보폭 규칙에 가깝고, Adam은 좌표별 적응과 누적 정보를 더 많이 활용하는 업데이트 규칙에 가깝다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- SGD(stochastic gradient descent)는 왜 기본 출발점으로 자주 소개되는가?
- Adam은 무엇을 더 보완하려는가?
- 둘의 차이를 입문 수준에서 어떻게 읽으면 좋은가?
- 실무에서 왜 Adam이 많이 언급되면서도 SGD가 여전히 중요한가?

이 절은 다음 내용은 깊게 다루지 않습니다.

- momentum, RMSProp, AdamW의 세부 수식 비교
- 일반화 성능에 대한 이론적 논쟁의 세밀한 정리
- 학습률 스케줄러(scheduler)의 상세 구현

이 절의 목적은 optimizer 논문을 깊게 비교하는 것이 아니라, `업데이트 철학의 차이`를 설명하는 것입니다. regularization과 일반화의 관점은 P4-8.1, P4-8.2에서 다시 연결하고, AdamW와 scheduler 같은 후속 최적화 실무는 이 책의 현재 본편 범위 밖에 둡니다.

## 이 절의 목표

- SGD와 Adam을 각각 한 문장으로 설명할 수 있습니다.
- `단순한 기본 업데이트`와 `적응형 업데이트`의 차이를 이해할 수 있습니다.
- optimizer 선택이 학습 속도와 안정성에 어떤 영향을 주는지 말할 수 있습니다.
- 작은 Python 예제로 업데이트 감각 차이를 확인할 수 있습니다.

## SGD는 왜 기본 출발점인가

SGD(stochastic gradient descent)는 이름 그대로, gradient를 이용해 조금씩 파라미터를 움직이는 가장 기본적인 사고를 담고 있습니다.

다음처럼 이해하면 충분합니다.

`SGD는 현재 gradient가 가리키는 방향으로, 정해 둔 learning rate만큼 한 걸음 움직이는 방식이다.`

이 방식이 기본 출발점으로 자주 소개되는 이유는 단순합니다.

- 직관이 분명합니다
- gradient descent의 핵심 아이디어가 드러납니다
- 업데이트 규칙을 가장 직접적으로 볼 수 있습니다

즉, SGD는 optimizer 세계의 입문용 좌표축 같은 역할을 합니다.

## Adam은 무엇을 더 하려는가

Adam은 SGD보다 더 많은 정보를 사용합니다. 다음 정도로 이해하면 충분합니다.

- 최근 gradient의 방향을 누적해서 보고
- 좌표마다 변화 크기를 다르게 조절하려고 하며
- 초기 학습을 더 빠르고 안정적으로 만들려는 실용적 목적이 있습니다

즉, Adam은 `모든 파라미터를 같은 보폭으로 움직이는 것`보다 더 정교한 업데이트를 시도합니다.

독자용 한 문장으로 줄이면 다음과 같습니다.

`Adam은 gradient의 최근 흐름과 좌표별 크기 차이를 함께 참고해, 파라미터마다 더 적응적으로 움직이려는 optimizer이다.`

## 둘의 차이를 어떻게 읽으면 좋은가

입문 단계에서는 복잡한 수식보다 다음 표가 더 중요합니다.

| 항목 | SGD | Adam |
| --- | --- | --- |
| 기본 감각 | 단순한 한 걸음 업데이트 | 더 많은 누적 정보를 반영한 적응형 업데이트 |
| 장점 | 직관이 단순하고 기준점이 분명함 | 초반 학습이 빠르고 실무에서 다루기 편한 경우가 많음 |
| 주의점 | 학습률 설정에 민감할 수 있음 | 설정이 편해 보여도 항상 최종 일반화가 더 좋다고 단정할 수는 없음 |

이 표에서 핵심은 `어느 것이 절대적으로 우월한가`가 아닙니다. 오히려 다음처럼 이해하는 편이 안전합니다.

`SGD는 학습의 기본 형태를 보여 주고, Adam은 그 기본 형태를 더 실용적으로 보완하려는 시도다.`

## 왜 Adam이 실무에서 많이 쓰이나

실무에서는 Adam이 자주 언급됩니다. 이유는 대체로 다음과 같습니다.

- 초기 설정으로도 비교적 잘 동작하는 경우가 많고
- 학습 초반 손실이 빠르게 줄어드는 경험을 주기 쉽고
- 큰 모델이나 복잡한 데이터에서 입문 장벽이 낮게 느껴질 수 있습니다

하지만 여기서 중요한 주의점이 있습니다.

`Adam이 자주 쓰인다고 해서, 모든 문제에서 무조건 더 좋은 최종 결과를 보장하는 것은 아니다.`

즉, Adam의 인기는 실용성과 편의성에서 오는 부분이 크며, 문제에 따라 다른 판단이 필요합니다.

## 왜 SGD가 여전히 중요한가

독자는 `Adam이 편하면 SGD는 이제 중요하지 않은가?`라는 질문을 자주 합니다. 그렇지 않습니다.

SGD는 여전히 중요합니다.

- gradient descent의 핵심 아이디어를 가장 명확하게 보여 줍니다
- optimizer 비교의 기준점 역할을 합니다
- 일부 문제에서는 여전히 강한 기준선(baseline)이 됩니다

또한 연구와 교육에서는 `복잡한 optimizer를 쓰기 전에 기본 형태가 어떻게 움직이는지`를 이해하는 것이 중요합니다.

즉, SGD는 오래된 방식이라기보다, optimizer를 읽는 기준 언어에 가깝습니다.

## 사례로 보기

### 사례 1. 손실이 천천히 줄어드는 장난감 문제

간단한 회귀 문제에서 SGD는 직관적으로 잘 설명됩니다. 현재 gradient를 보고 한 걸음 이동하므로, `왜 loss가 줄어드는지`를 추적하기 쉽습니다.

### 사례 2. 복잡한 딥러닝 모델의 초기 실험

실무에서 새로운 모델을 빠르게 시험할 때는 Adam이 편하게 느껴지는 경우가 많습니다. 초반에 손실이 빨리 줄고, 기본 설정으로도 학습이 시작되는 경험을 주기 쉽기 때문입니다.

### 사례 3. 비교 실험

연구나 실험 기록에서는 같은 모델을 SGD와 Adam으로 모두 돌려 보며:

- 수렴 속도
- 최종 성능
- 진동 정도

를 비교하기도 합니다. 이때 optimizer는 부수 설정이 아니라 실험의 핵심 변수 중 하나가 됩니다.

## 작은 Python 예제로 업데이트 감각 보기

이번 예제의 목표는 `같은 gradient라도`, 단순한 SGD식 업데이트와 누적 평균을 반영한 Adam식 업데이트 감각이 다를 수 있다는 점을 직관적으로 보는 것입니다.

입력:

- 현재 가중치 `w`
- 여러 step에서의 gradient 목록

출력:

- SGD 방식의 연속 업데이트 결과
- Adam 식 누적 평균을 단순화한 직관적 업데이트 결과

```python
gradients = [-4.0, -2.0, -1.0]
w_sgd = 1.0
w_adam_like = 1.0
learning_rate = 0.1
moving_avg = 0.0
beta = 0.9

print("SGD updates")
for g in gradients:
    w_sgd = w_sgd - learning_rate * g
    print(" gradient =", g, "-> w =", round(w_sgd, 3))

print()
print("Adam-like updates (simplified intuition)")
for g in gradients:
    moving_avg = beta * moving_avg + (1 - beta) * g
    w_adam_like = w_adam_like - learning_rate * moving_avg
    print(" gradient =", g, "moving_avg =", round(moving_avg, 3), "-> w =", round(w_adam_like, 3))
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
SGD updates
 gradient = -4.0 -> w = 1.4
 gradient = -2.0 -> w = 1.6
 gradient = -1.0 -> w = 1.7

Adam-like updates (simplified intuition)
 gradient = -4.0 moving_avg = -0.4 -> w = 1.04
 gradient = -2.0 moving_avg = -0.56 -> w = 1.096
 gradient = -1.0 moving_avg = -0.604 -> w = 1.156
```

이 예제는 진짜 Adam 전체 공식을 구현한 것은 아닙니다. 여기서 읽어야 할 핵심은 다음입니다.

- SGD는 현재 gradient를 비교적 직접 반영합니다
- Adam류의 아이디어는 최근 방향을 누적해 더 매끈하게 움직이려 합니다
- optimizer는 단순히 `감소시킨다`가 아니라, `어떤 방식으로 감소시킬지`를 정합니다

## 역사와 커리큘럼 관점

SGD는 오랫동안 대규모 머신러닝과 신경망 학습의 기본 출발점으로 다뤄져 왔습니다. 이후 momentum, RMSProp, Adam 같은 알고리즘은 더 빠르고 안정적인 학습을 얻기 위한 실용적 요구 속에서 발전했습니다.

딥러닝 커리큘럼에서 SGD와 Adam을 나란히 두는 이유는 분명합니다.

- SGD만 보면 기본 원리는 이해되지만 현대 실무 감각이 부족해지고
- Adam만 보면 왜 optimizer가 그런 설계를 갖게 되었는지 기준점이 사라지기 때문입니다

즉, 이 절은 `기본 원리`와 `현대 실무 감각`을 함께 붙이는 자리입니다.

## 다음 절과의 연결

여기까지 오면 다음 질문이 남습니다.

- optimizer가 잘 작동하더라도, 모델이 학습 데이터에만 과하게 맞아 버리면 어떻게 해야 하는가?
- 성능을 높이기보다 일반화(generalization)를 지키기 위한 제약은 무엇이 있는가?

이 질문은 바로 P4-8.1 정규화(regularization)로 이어집니다.

## 이 절에서 기억할 관점

- SGD는 기본적인 gradient-based update의 직관을 가장 분명하게 보여 줍니다.
- Adam은 누적 정보와 좌표별 조절을 더 반영하는 적응형 optimizer입니다.
- Adam이 실무에서 자주 쓰여도, SGD는 여전히 중요한 기준점입니다.
- optimizer 비교는 속도, 안정성, 일반화까지 함께 보아야 합니다.

## 체크리스트

- SGD와 Adam을 각각 한 문장으로 설명할 수 있는가?
- 현재 gradient를 직접 반영하는 방식과 누적 정보를 쓰는 방식의 차이를 말할 수 있는가?
- Adam이 자주 쓰인다고 해서 항상 절대 우위라고 단정하면 안 되는 이유를 설명할 수 있는가?
- 다음 장의 regularization이 왜 optimizer 다음에 오는지 연결할 수 있는가?

## 출처와 참고 자료

- Léon Bottou, `Large-Scale Machine Learning with Stochastic Gradient Descent`, COMPSTAT, 2010, 확인 날짜: 2026-06-29.
- Diederik P. Kingma, Jimmy Ba, `Adam: A Method for Stochastic Optimization`, arXiv, 2014, 확인 날짜: 2026-06-29.
- Sebastian Ruder, `An overview of gradient descent optimization algorithms`, arXiv, 2016, 확인 날짜: 2026-06-29.

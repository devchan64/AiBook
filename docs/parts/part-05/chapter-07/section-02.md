# P5-7.2 Adam의 직관: 적응형 업데이트

Section ID: `P5-7.2`
Version: `v2026.07.16`

P5-7.1에서는 옵티마이저(optimizer)를 `gradient를 실제 파라미터 업데이트로 바꾸는 규칙`이라고 설명했습니다. 여기서 다음 질문이 바로 이어집니다.

그렇다면 Adam은 기본적인 update 규칙에 무엇을 더 보완하려는 optimizer인가?

Adam은 단순히 `더 유명한 optimizer`가 아니라, 최근 gradient 흐름과 좌표별 변화 크기를 더 참고해 update를 적응적으로 조절하려는 optimizer다.

대표 옵티마이저의 차이를 다시 짧게 복습해야 할 때는 개념사전의 [경사하강법(gradient descent)](../../../reference/concept-glossary.md#gradient-descent)과 [옵티마이저(optimizer)](../../../reference/concept-glossary.md#optimizer) 항목을 함께 다시 봅니다.

## 이 절의 범위

- Adam은 기본적인 gradient update에 무엇을 더 보완하려는가?
- 최근 gradient 흐름과 좌표별 조절이라는 Adam의 핵심 직관은 무엇인가?
- Adam을 설명할 때 왜 단순 update 기준과 함께 비교해야 하는가?
- Adam이 실무에서 많이 언급되지만 왜 절대 우열로 외우면 안 되는가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- momentum, RMSProp, AdamW의 세부 수식 비교
- 일반화 성능에 대한 이론적 논쟁의 세밀한 정리
- 학습률 스케줄러(scheduler)의 상세 구현

이 절에서는 optimizer 논문을 깊게 비교하기보다, Adam이 어떤 문제의식에서 적응형 update를 추가하는지 설명합니다. momentum, RMSProp, AdamW의 세부 수식 비교와 일반화 논쟁의 세밀한 정리는 여기서 길게 다루지 않고, regularization과 일반화의 관점은 P5-8.1, P5-8.2에서 다시 연결합니다. 학습률 스케줄러와 AdamW 같은 후속 최적화 실무는 이 책의 현재 본편 범위 밖에 둡니다. 여기서는 `새 모델 구조`보다 이미 계산된 gradient를 Adam이 `어떤 규칙으로 실제 update로 바꾸려 하는가`를 읽습니다.

| 지금 절에서 구분할 것 | 왜 중요한가 |
| --- | --- |
| 모델 구조 | CNN, RNN, Transformer처럼 입력 구조를 어떻게 표현할지 정하는 문제이기 때문입니다. |
| optimizer 절차 | 같은 구조라도 파라미터를 어떤 보폭과 어떤 누적 규칙으로 움직일지 정하는 문제이기 때문입니다. |
| regularization과의 차이 | optimizer는 `어떻게 움직일까`, regularization은 `어떤 해를 덜 선호할까`를 다루기 때문입니다. |

## 이 절의 목표

- Adam을 `최근 gradient 흐름과 좌표별 조절을 반영하는 적응형 optimizer`로 설명할 수 있습니다.
- 단순한 기본 업데이트와 Adam식 적응형 업데이트의 차이를 이해할 수 있습니다.
- Adam이 학습 속도와 안정성에 어떤 기대를 주는지 말할 수 있습니다.
- 실행 가능한 Python 예제로 업데이트 감각 차이를 확인할 수 있습니다.

## Adam을 이해할 때 필요한 단순 update 기준

Adam을 바로 공식으로 시작하면 초심자는 `무엇이 추가된 것인지`를 놓치기 쉽습니다. 그래서 먼저 가장 단순한 update 기준을 하나 둡니다. SGD(stochastic gradient descent)는 gradient를 이용해 조금씩 파라미터를 움직이는 기본 사고를 잘 보여 주는 기준선입니다.

다음처럼 이해하면 충분합니다.

`SGD는 현재 gradient가 가리키는 방향으로, 정해 둔 learning rate만큼 한 걸음 움직이는 방식이다.`

여기서 SGD를 길게 다루는 목적은 SGD 자체를 중심 주제로 바꾸기 위해서가 아닙니다. Adam이 무엇을 더 보완하는지 보려면, 먼저 `현재 gradient와 learning rate만으로 움직이는 단순 기준`이 보여야 하기 때문입니다.

- 직관이 분명합니다
- gradient descent의 핵심 아이디어가 드러납니다
- 업데이트 규칙을 가장 직접적으로 볼 수 있습니다

즉, 이 절에서 SGD는 Adam을 설명하기 위한 비교 기준입니다.

## Adam은 단순 update에 무엇을 더 보완하는가

Adam은 단순한 현재 gradient 기준 update보다 더 많은 정보를 사용합니다. 다음 정도로 이해하면 충분합니다.

- 최근 gradient의 방향을 누적해서 보고
- 좌표마다 변화 크기를 다르게 조절하려고 하며
- 초기 학습을 더 빠르고 안정적으로 만들려는 실용적 목적이 있습니다

즉, Adam은 `모든 파라미터를 같은 기준 보폭으로 움직이는 것`보다 더 정교한 업데이트를 시도합니다.

독자용 한 문장으로 줄이면 다음과 같습니다.

`Adam은 gradient의 최근 흐름과 좌표별 크기 차이를 함께 참고해, 파라미터마다 더 적응적으로 움직이려는 optimizer이다.`

조금 더 직관적으로 바꾸면 다음처럼 읽을 수 있습니다.

- 단순 update 기준: `지금 보이는 경사 방향으로 같은 기준 보폭을 내딛는다`
- Adam: `최근 몇 걸음의 흔들림을 같이 보고, 좌표마다 보폭을 다르게 조절한다`

예를 들어 어떤 파라미터는 gradient가 계속 크게 흔들리고, 다른 파라미터는 아주 작고 안정적으로 움직인다고 해 보겠습니다. 단순 update 기준은 둘을 같은 learning rate 기준으로 함께 밀지만, Adam은 `지금 이 좌표는 너무 크게 흔들리고 있지 않은가`, `이 좌표는 너무 느리게 움직이고 있지 않은가`를 조금 더 반영하려고 합니다. 그래서 Adam은 `같은 한 걸음`보다 `좌표마다 다른 한 걸음`에 가깝게 느껴집니다.

## Adam의 보완점을 어떻게 읽으면 좋은가

입문 단계에서는 복잡한 수식보다 다음 표가 더 중요합니다.

| 항목 | 단순 update 기준 | Adam |
| --- | --- | --- |
| 기본 감각 | 단순한 한 걸음 업데이트 | 더 많은 누적 정보를 반영한 적응형 업데이트 |
| 장점 | 직관이 단순하고 기준점이 분명함 | 초반 학습이 빠르고 실무에서 다루기 편한 경우가 많음 |
| 주의점 | 학습률 설정에 민감할 수 있음 | 설정이 편해 보여도 항상 최종 일반화가 더 좋다고 단정할 수는 없음 |

이 표에서 핵심은 `어느 것이 절대적으로 우월한가`가 아닙니다. 오히려 다음처럼 이해하는 편이 안전합니다.

`Adam은 단순한 gradient update 기준에 최근 흐름과 좌표별 조절을 더해, 더 적응적인 update를 만들려는 시도다.`

## 왜 Adam이 실무에서 많이 쓰이나

실무에서는 Adam이 자주 언급됩니다. 이유는 대체로 다음과 같습니다.

- 초기 설정으로도 비교적 잘 동작하는 경우가 많고
- 학습 초반 손실이 빠르게 줄어드는 경험을 주기 쉽고
- 큰 모델이나 복잡한 데이터에서 입문 장벽이 낮게 느껴질 수 있습니다

하지만 여기서 중요한 주의점이 있습니다.

`Adam이 자주 쓰인다고 해서, 모든 문제에서 무조건 더 좋은 최종 결과를 보장하는 것은 아니다.`

즉, Adam의 인기는 실용성과 편의성에서 오는 부분이 크며, 문제에 따라 다른 판단이 필요합니다.

## 왜 단순 update 기준도 함께 남기는가

Adam을 설명하는 절에서도 단순 update 기준은 필요합니다. 기준선이 없으면 Adam의 장점도 `그냥 더 좋은 optimizer`처럼 외우기 쉽기 때문입니다.

SGD에서 확인할 수 있는 기준은 복잡한 보정 없이도 gradient 방향을 따라 파라미터가 어떻게 움직이는지를 가장 직접적으로 읽을 수 있다는 점입니다.

- gradient descent의 핵심 아이디어를 가장 직접적으로 읽게 해 줍니다
- optimizer 비교의 기준점 역할을 합니다
- 일부 문제에서는 여전히 강한 기준선(baseline)이 됩니다

또한 연구와 교육에서는 `Adam 같은 optimizer가 무엇을 추가로 보정하는지`를 이해하려면, 먼저 기본 형태가 어떻게 움직이는지 구분해 볼 필요가 있습니다.

즉, 이 절에서 SGD는 Adam의 반대편 주인공이 아니라, Adam의 보완 지점을 보이게 하는 기준 언어에 가깝습니다.

이 차이를 업데이트 규칙만 남겨 압축하면 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-07/sgd-vs-adam-flow-ko.mmd"
```

이 도식에서 먼저 확인할 결과는, SGD가 `현재 gradient에 같은 기준 보폭으로 반응`하는 감각에 가깝다면, Adam은 `최근 흐름과 좌표별 차이를 더 반영해 보폭을 조절`하는 감각에 가깝다는 점입니다.

## 사례 및 예시

이 절의 사례는 `어느 optimizer가 더 좋은가`를 고르는 사례가 아닙니다. Adam이 단순 update 기준에 무엇을 더 반영하는지 읽는 사례입니다. 사례 수를 늘리기보다, Adam이 필요한 장면 하나를 분명히 보고 그 해석을 잘못 확장하지 않는 데 집중합니다.

1. 지금 들어온 gradient가 현재 step 하나를 주로 설명하는가, 여러 step의 흐름까지 함께 보아야 하는가
2. 단순 update 기준에서는 현재 gradient가 이번 update에 얼마나 직접 반영되는가
3. Adam류에서는 최근 gradient 흐름과 좌표별 차이가 update에 어떻게 섞이는가
4. 빠른 초반 감소를 최종 우열이나 일반화 성능으로 바로 바꿔 말하지 않는가

### 중심 사례. 복잡한 딥러닝 모델과 큰 모델의 초기 실험

새 이미지 분류 모델이나 문장 분류 모델을 처음 붙여 보는데, 어떤 learning rate가 맞는지 아직 감이 없을 수 있습니다. 사람이 이 단계에서 먼저 바라는 것은 대개 `수식이 가장 순수한가`보다 `초반 학습이 너무 흔들리지 않고 시작되는가`입니다. 이때 Adam은 최근 gradient 경향을 함께 반영해 초반 학습을 비교적 안정적으로 시작하게 해 주는 경우가 많아서, `일단 돌아가게 만들기` 단계에서 편하게 느껴질 수 있습니다. 즉, 사용자는 복잡한 튜닝 전에 먼저 손실이 줄기 시작하는 경험을 얻기 쉽습니다.

모델이 커지면 사람은 `가중치가 많아졌을 뿐이니 같은 방식으로 업데이트하면 되지 않을까`라고 생각하기 쉽습니다. 단순 update 기준에서는 현재 gradient와 learning rate가 이번 이동량을 직접 정하므로, 이 감각 자체는 이해하기 쉽습니다. 하지만 실제 큰 모델에서는 어떤 층은 아주 민감하게 반응하고, 어떤 층은 거의 움직이지 않으며, gradient 스케일도 고르게 맞지 않는 경우가 많습니다. 같은 learning rate를 모든 파라미터에 단순히 적용하면 일부 층은 과하게 흔들리고, 다른 층은 거의 학습되지 않을 수 있습니다.

Adam은 이런 차이를 완전히 해결하는 마법 같은 방법은 아니지만, 최근 gradient 흐름과 좌표별 변화 크기를 함께 읽어 초반 update를 조금 더 균형 있게 만들려 합니다. 그래서 `왜 Adam이 초반 실험에서 덜 답답하게 느껴지는가`를 이해할 때는 `더 똑똑한 공식`보다 `파라미터마다 보폭을 조금 다르게 잡으려는 태도`를 떠올리는 편이 더 정확합니다. 그래서 이 사례에서 확인해야 할 결과는 같은 learning rate를 두어도, 좌표별 gradient 크기 차이와 층별 흔들림이 초반 업데이트에 다르게 반영되는가입니다.

### 주의 사례. 초반 속도만 보고 Adam의 우열을 단정하는 경우

연구나 실험 기록에서는 같은 모델을 단순 기준과 Adam으로 모두 돌려 보는 경우가 많습니다. 사람은 로그를 볼 때 `어느 쪽 손실이 더 빨리 내려갔는가`만 먼저 보기 쉽지만, 실제 비교 기준은 수렴 속도, 최종 성능, 진동 정도처럼 여러 축으로 나뉩니다. 예를 들어 Adam은 초반에 빠르게 내려가지만, 단순 기준이 더 오래 학습했을 때 최종 검증 성능이 더 좋아질 수도 있습니다. 따라서 이 주의 사례에서 확인해야 할 결과는 Adam의 적응형 update가 초반 안정성과 편의성을 줄 수 있어도, 그것을 최종 우열이나 일반화 성능 보장으로 바꾸어 말하면 안 된다는 점입니다.

| 사람이 먼저 보기 쉬운 기준 | 단순 update 기준으로 다시 읽는 기준 | Adam 관점으로 다시 읽는 기준 |
| --- | --- | --- |
| 큰 모델도 가중치가 많을 뿐 같은 보폭으로 밀면 된다고 느끼기 쉽다 | 모든 좌표를 같은 기준으로 움직이면 민감한 층과 둔한 층의 차이를 놓칠 수 있다 | 좌표별 gradient 크기와 최근 흐름을 반영해 update 균형을 맞추려 한다 |
| 초반 손실이 빨리 줄면 무조건 더 좋은 optimizer라고 생각하기 쉽다 | 수렴 속도와 최종 일반화는 따로 비교해야 하고, 단순 기준은 기준선 역할을 잘 보여 준다 | 초반 안정성과 실용성은 좋을 수 있지만 최종 결과 우위를 자동 보장하지는 않는다 |
| Adam이 많이 쓰이니 단순 기준은 이제 덜 중요하다고 느끼기 쉽다 | 단순 기준은 `현재 gradient에 직접 반응하는 기본 보폭` 감각을 가장 분명히 보여 주는 기준점이다 | Adam은 그 기준점 위에 적응형 보정이 무엇을 더하는지 읽게 해 준다 |

이 사례 구간에서 최종적으로 확인해야 할 결과는 분명합니다. Adam의 차이는 `더 최신 optimizer인가`가 아니라, 현재 gradient 기준의 직접 업데이트 위에 누적 정보와 좌표별 차이를 더 반영한 적응형 업데이트를 만든다는 데 있습니다.

## 연습 및 예제

이번 예제의 목표는 `같은 위험 가중치 gradient 흐름이라도`, 단순 직접 업데이트와 Adam-like 누적 업데이트가 서로 다른 step별 update를 만든다는 점을 직관적으로 보는 것입니다. 여기서는 진짜 Adam 전체 공식을 구현하지 않고, Adam류 optimizer가 최근 gradient 흐름을 누적해 update에 반영한다는 감각만 단순화해 확인합니다.

입력:

- 현재 위험 가중치 `risk_weight`
- 여러 step에서의 위험 가중치 gradient 목록

출력:

- 단순 직접 업데이트 방식의 연속 위험 가중치 업데이트 결과
- Adam-like 누적 평균을 단순화한 직관적 업데이트 결과
- step별 `sgd_delta`와 `adam_like_delta`

문제 상황:

- optimizer 차이는 수식 이름보다 같은 gradient 흐름이 어떤 step별 update로 바뀌는지로 보는 편이 직관적이다

확인할 개념:

- 단순 직접 업데이트는 현재 gradient에 바로 반응한다
- Adam류 방식은 최근 gradient 정보를 누적해 이동량을 조절한다

입력(input):

압력 미복귀 신호를 읽는 `risk_weight` 하나가 있고, 학습 step마다 `gradient_risk_weight`가 `-4.0`, `-2.0`, `-1.0` 순서로 들어온다고 가정합니다. 같은 gradient 흐름을 보더라도 단순 직접 업데이트와 Adam-like가 `risk_weight`를 얼마나 직접적으로, 혹은 얼마나 누적 평균을 섞어 움직이는지 비교합니다.

코드를 보기 전에 먼저 어떤 쪽 이동량이 더 직접적이고 어떤 쪽이 더 매끈할지 예상해 보면, `현재 gradient 반응`과 `누적 평균 반응`의 차이가 더 잘 보입니다.

| 비교 항목 | 먼저 예상해 볼 update | 예상 이유 |
| --- | --- | --- |
| 첫 번째 `sgd_delta` | 가장 크게 움직일 가능성이 큼 | 첫 `gradient_risk_weight` `-4.0`이 learning rate와 바로 곱해져 직접 반영되기 때문입니다. |
| 첫 번째 `adam_like_delta` | `sgd_delta`보다 훨씬 작을 가능성이 큼 | moving average가 처음에는 전체 gradient를 부분적으로만 반영하기 때문입니다. |
| step이 지날수록 `sgd_delta` | gradient 절대값이 줄어들며 함께 바로 작아질 가능성이 큼 | 단순 직접 업데이트는 현재 `gradient_risk_weight` 크기에 직접 반응합니다. |
| step이 지날수록 `adam_like_delta` | 더 천천히 변하거나 상대적으로 매끈하게 이어질 가능성이 큼 | 이전 step들의 gradient가 moving average 안에 남아 있기 때문입니다. |

이 표의 목적은 정확한 숫자를 미리 암기하는 데 있지 않습니다. 같은 `gradient_risk_weight` 흐름이어도 단순 직접 업데이트는 `지금 기울기`를 바로 반영하고, Adam-like는 `최근 흐름`을 남기며 더 매끈하게 움직일 수 있다는 점을 코드 전에 붙잡는 데 있습니다.

```python
gradient_risk_weight_history = [-4.0, -2.0, -1.0]
risk_weight_sgd = 1.0
risk_weight_adam_like = 1.0
learning_rate = 0.1
moving_avg = 0.0
beta = 0.9

print("Direct updates")
for gradient_risk_weight in gradient_risk_weight_history:
    sgd_delta = -learning_rate * gradient_risk_weight
    risk_weight_sgd = risk_weight_sgd + sgd_delta
    print(
        " gradient_risk_weight =", gradient_risk_weight,
        "sgd_delta =", round(sgd_delta, 3),
        "-> risk_weight =", round(risk_weight_sgd, 3)
    )

print()
print("Adam-like updates (simplified intuition)")
for gradient_risk_weight in gradient_risk_weight_history:
    moving_avg = beta * moving_avg + (1 - beta) * gradient_risk_weight
    adam_like_delta = -learning_rate * moving_avg
    risk_weight_adam_like = risk_weight_adam_like + adam_like_delta
    print(
        " gradient_risk_weight =", gradient_risk_weight,
        "moving_avg =", round(moving_avg, 3),
        "adam_like_delta =", round(adam_like_delta, 3),
        "-> risk_weight =", round(risk_weight_adam_like, 3)
    )
```

출력에서는 같은 `gradient_risk_weight` 흐름에서도 단순 직접 업데이트와 Adam-like의 step별 update가 어떻게 달라지는지부터 비교하면 됩니다.

```text
Direct updates
 gradient_risk_weight = -4.0 sgd_delta = 0.4 -> risk_weight = 1.4
 gradient_risk_weight = -2.0 sgd_delta = 0.2 -> risk_weight = 1.6
 gradient_risk_weight = -1.0 sgd_delta = 0.1 -> risk_weight = 1.7

Adam-like updates (simplified intuition)
 gradient_risk_weight = -4.0 moving_avg = -0.4 adam_like_delta = 0.04 -> risk_weight = 1.04
 gradient_risk_weight = -2.0 moving_avg = -0.56 adam_like_delta = 0.056 -> risk_weight = 1.096
 gradient_risk_weight = -1.0 moving_avg = -0.604 adam_like_delta = 0.06 -> risk_weight = 1.156
```

같은 출력도 `입력 gradient -> step별 update -> 누적된 risk_weight`로 나누어 보면 Adam-like가 무엇을 더 보완하려는지 더 분명합니다.

![단순 직접 업데이트와 Adam-like 비교에 쓰는 gradient 입력 흐름](../../../assets/part-05/chapter-07/sgd-adam-gradient-history-ko.png)

첫 단계의 입력은 optimizer가 아직 바꾸지 않은 gradient 흐름입니다. 여기서는 step이 지날수록 `gradient_risk_weight`의 절대값이 작아지며, 단순 직접 업데이트와 Adam-like는 모두 같은 입력을 받습니다.

![단순 직접 업데이트와 Adam-like의 step별 delta 비교](../../../assets/part-05/chapter-07/sgd-adam-delta-comparison-ko.png)

delta 단계에서 차이가 생깁니다. 단순 직접 업데이트는 현재 gradient를 바로 learning rate와 곱해 첫 step에서 크게 움직이고, Adam-like는 moving average를 거치기 때문에 같은 입력을 더 작은 이동량으로 바꿉니다.

![단순 직접 업데이트와 Adam-like의 risk_weight 이동 경로](../../../assets/part-05/chapter-07/sgd-adam-risk-weight-trajectory-ko.png)

최종 risk_weight 경로를 보면 이 차이가 누적됩니다. 단순 직접 업데이트는 빠르게 1.7까지 이동하지만, Adam-like는 최근 흐름을 누적해 더 천천히 1.156까지 움직입니다. 이 단계에서 달라지는 것은 `같은 gradient를 받았다`가 아니라, optimizer 규칙이 실제 파라미터 경로를 다르게 만든다는 점입니다.

이 예제는 진짜 Adam 전체 공식을 구현한 것도 아니고, 단순 직접 업데이트와 Adam의 성능 우열을 판정하는 실험도 아닙니다. 여기서 읽어야 할 핵심은 다음입니다.

- 단순 직접 업데이트는 현재 `gradient_risk_weight`를 비교적 직접 반영합니다
- Adam류의 아이디어는 최근 방향을 누적해 step별 update를 다르게 만듭니다
- optimizer는 단순히 `감소시킨다`가 아니라, 같은 gradient를 `어떤 update 경로로 바꿀지`를 정합니다

이 예제는 여기서 끝내기보다, 값을 조금 바꿔 보며 `어떤 변화가 어느 방식에 더 민감하게 반영되는가`를 같이 보는 편이 더 좋습니다.

| 먼저 바꿔 볼 값 | 무엇을 비교하게 되는가 | 이 절에서 먼저 확인할 결과 |
| --- | --- | --- |
| `learning_rate`를 0.1에서 0.3으로 키운다 | 두 방식의 step별 이동량이 얼마나 더 거칠어지는가 | SGD 쪽 `risk_weight` 이동 폭이 더 직접적으로 커지는가 |
| `beta`를 0.9에서 0.5로 낮춘다 | Adam-like가 최근 gradient를 얼마나 빨리 따라가는가 | 누적 평균이 덜 매끈해지고 현재 gradient 반영이 빨라지는가 |
| `gradient_risk_weight_history`를 `[-4.0, 3.0, -1.0]`처럼 흔들리게 바꾼다 | 방향이 뒤집힐 때 두 방식이 얼마나 다르게 반응하는가 | Adam-like가 방향 전환을 더 천천히 반영하는가 |

즉, 이 절의 실험은 `Adam이 다르다`를 보는 데서 멈추지 않고, `어떤 값을 흔들면 Adam-like 보완이 더 분명해지는가`까지 확인해야 optimizer 감각이 더 오래 남습니다.

SGD는 오랫동안 대규모 머신러닝과 신경망 학습의 기본 출발점으로 다뤄져 왔습니다. 이후 momentum, RMSProp, Adam 같은 알고리즘은 더 빠르고 안정적인 학습을 얻기 위한 실용적 요구 속에서 발전했습니다.

딥러닝 커리큘럼에서 Adam을 설명할 때 단순 update 기준을 함께 두는 이유는 분명합니다.

- 바로 앞의 P5-7.1 옵티마이저 역할에서 본 `gradient를 실제 update로 바꾸는 기본 구조`를 기준점으로 잡아야 하고
- 단순 기준만 보면 기본 원리는 이해되지만 현대 실무 감각이 부족해지고
- Adam만 보면 왜 그런 설계를 갖게 되었는지 기준점이 사라지기 때문입니다

즉, 이 절은 `기본 원리`와 `현대 실무 감각`을 함께 붙이는 자리입니다.

## 언제 Adam 관점을 먼저 꺼내는가

optimizer의 일반 역할을 이해한 뒤에는 `지금 기본 업데이트 감각만으로 충분한가, 아니면 Adam식 적응형 업데이트 감각이 필요한가`를 나누어 읽는 편이 좋습니다.

| 먼저 보이는 문제 장면 | 먼저 떠올릴 optimizer 관점 | 이유 |
| --- | --- | --- |
| gradient 방향과 보폭의 가장 기본 구조를 설명해야 한다 | 단순 update 기준 | 현재 gradient에 직접 반응하는 기본 업데이트 감각을 가장 분명히 보여 줍니다. |
| 초반 학습이 너무 거칠거나 좌표별 스케일 차이가 크다 | Adam | 누적 정보와 좌표별 적응을 반영하는 업데이트 감각이 더 중요해집니다. |
| 실무에서 왜 Adam이 자주 쓰이는지 설명해야 한다 | Adam을 먼저 언급하되 SGD와 함께 비교한다 | 편의성과 실용성은 크지만 기준점 없이 설명하면 감각이 흐려지기 때문입니다. |
| optimizer를 절대 우열로 외우려는 경향이 보인다 | 단순 기준과 Adam을 나란히 둔다 | 속도, 안정성, 일반화를 분리해 읽어야 하기 때문입니다. |

## 체크리스트

- Adam이 기본 update에 무엇을 더 보완하려는지 설명할 수 있는가?
- 왜 Adam이 널리 쓰이면서도 절대적으로 더 좋은 optimizer라고 단정하면 안 되는지 말할 수 있는가?
- 단순 update 기준을 Adam의 보완 지점을 보이게 하는 기준점으로 설명할 수 있는가?
- Adam은 누적 정보와 좌표별 조절을 더 반영하는 적응형 optimizer라는 점을 설명할 수 있는가?
- 단순 update 기준과 Adam을 `기본 보폭 업데이트`와 `적응형 업데이트`의 차이로 설명할 수 있는가?
- optimizer 비교는 속도, 안정성, 일반화까지 함께 보아야 한다는 점을 말할 수 있는가?
- optimizer를 무조건 우열 순위처럼 외우려 할 때, Adam을 기준점과 적응형 업데이트 차이로 다시 떠올릴 수 있는가?
- 이 절 다음에는 optimizer 자체가 아니라 일반화 제약과 regularization 장으로 넘어간다는 흐름을 이해했는가?

## 출처와 참고 자료

- Léon Bottou, `Large-Scale Machine Learning with Stochastic Gradient Descent`, COMPSTAT, 2010, 확인 날짜: 2026-06-29.
- Diederik P. Kingma, Jimmy Ba, `Adam: A Method for Stochastic Optimization`, arXiv, 2014, 확인 날짜: 2026-06-29.
- Sebastian Ruder, `An overview of gradient descent optimization algorithms`, arXiv, 2016, 확인 날짜: 2026-06-29.

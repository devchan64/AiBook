# P5-7.3 적응형 업데이트의 직관: Adam을 예로

> Section ID: `P5-7.3`
> Version: `v2026.07.19`

P5-7.2에서는 같은 gradient라도 learning rate에 따라 실제 update 보폭이 어떻게 달라지는지 보았습니다. 여기서 바로 다음 질문이 생깁니다. 그 보폭을 모든 파라미터에 언제나 같은 방식으로 적용해도 충분한가?

적응형 업데이트(adaptive update)는 바로 이 지점에서 나옵니다. 기본 직접 update가 `현재 gradient와 learning rate를 바탕으로 한 번 움직이는 방식`이라면, 적응형 업데이트는 여기에 최근 gradient 흐름과 파라미터 좌표별 차이까지 함께 보며 실제 이동량을 조절하려고 합니다.

이 절에서는 Adam(Adaptive Moment Estimation)을 대표 예로 삼아 그 직관을 읽습니다. 중심은 Adam이라는 이름 자체보다, `왜 update 규칙에 최근 흐름과 좌표별 조절이 들어가는가`입니다.

기본 업데이트와 적응형 업데이트의 차이가 다시 섞이면 개념사전의 [경사하강법(gradient descent)](../../../reference/concept-glossary.md#gradient-descent)과 [옵티마이저(optimizer)](../../../reference/concept-glossary.md#optimizer) 항목을 함께 다시 봅니다.

## 이 절의 범위

- 적응형 업데이트는 기본적인 gradient update에 무엇을 더 보완하려는가?
- 최근 gradient 흐름과 좌표별 조절이라는 적응형 update의 핵심 직관은 무엇인가?
- Adam은 그 적응형 update 감각을 설명할 때 어떤 대표 예가 되는가?
- Adam이 실무에서 많이 언급되지만 왜 절대 우열로 외우면 안 되는가?

이 절에서는 optimizer 이름을 더 많이 늘어놓기보다, 적응형 update가 어떤 문제의식에서 나오는지 설명합니다. 여기서 읽어야 할 것은 `이미 계산된 gradient를 어떤 규칙으로 실제 update로 바꾸는가`, 그리고 왜 그 규칙에 최근 흐름과 좌표별 차이가 들어가는가입니다. Adam은 이 직관을 붙잡는 대표 예로 사용합니다. optimizer 계열 이름을 처음 구분하는 비교는 P5-7.5 보충학습에서, optimizer state와 parameter-wise update는 P5-7.7 보충학습에서 다시 이어집니다. regularization과 일반화의 관점은 P5-8.1, P5-8.2에서 다시 연결하고, adaptive optimization의 수렴 분석은 P5-7.4 보충학습으로 이어집니다.

| 지금 절에서 구분할 것 | 왜 중요한가 |
| --- | --- |
| 모델 구조 | CNN, RNN, Transformer처럼 입력 구조를 어떻게 표현할지 정하는 문제이기 때문입니다. |
| optimizer 절차 | 같은 구조라도 파라미터를 어떤 보폭과 어떤 누적 규칙으로 움직일지 정하는 문제이기 때문입니다. |
| regularization과의 차이 | optimizer는 `어떻게 움직일까`, regularization은 `어떤 해를 덜 선호할까`를 다루기 때문입니다. |

## 이 절의 목표

- 적응형 업데이트를 `최근 gradient 흐름과 좌표별 조절을 반영하는 update 방식`으로 설명할 수 있습니다.
- 기본 직접 업데이트와 적응형 업데이트의 차이를 이해할 수 있습니다.
- Adam이 왜 적응형 update의 대표 예로 자주 언급되는지 말할 수 있습니다.
- 실행 가능한 Python 예제로 업데이트 감각 차이를 확인할 수 있습니다.

## 적응형 업데이트를 이해할 때 먼저 필요한 기준선

적응형 업데이트를 바로 공식으로 시작하면 초심자는 `무엇이 추가된 것인지`를 놓치기 쉽습니다. 그래서 먼저 가장 단순한 기준선부터 둡니다. 여기서 먼저 붙잡아야 할 것은 특정 optimizer 이름보다, `현재 gradient와 learning rate를 바탕으로 바로 한 번 움직인다`는 기본 감각입니다.

다음처럼 이해하면 충분합니다.

`현재 gradient가 가리키는 방향으로, 정해 둔 learning rate만큼 한 걸음 움직이는 방식이다.`

이 감각은 P5-7.2에서 본 `learning rate가 update 보폭을 정한다`는 설명을 그대로 이어받습니다. P5-7.2가 보폭 자체를 설명했다면, 여기서는 그 보폭을 `모든 파라미터에 같은 식으로 바로 적용하는 기본 update`를 기준선으로 삼습니다.

여기서 특정 optimizer 이름을 앞세우지 않는 이유도 분명합니다. 지금 필요한 것은 이름 구분이 아니라, 적응형 update가 무엇을 더 보완하는지 읽기 위한 가장 얇은 기준선이기 때문입니다.

- 직관이 분명합니다
- gradient descent의 핵심 아이디어가 드러납니다
- 업데이트 규칙을 가장 직접적으로 볼 수 있습니다

즉, 이 절의 기준선은 특정 optimizer 소개가 아니라, 적응형 업데이트를 설명하기 위한 `가장 단순한 직접 update 감각`입니다.

## 적응형 업데이트는 무엇을 더 보완하려 하는가

적응형 업데이트는 단순한 현재 gradient 기준 update보다 더 많은 정보를 사용합니다. Adam을 대표 예로 두고 보면 다음 정도로 이해하면 충분합니다.

- 최근 gradient의 방향을 누적해서 보고
- 좌표마다 변화 크기를 다르게 조절하려고 하며
- 초기 학습을 더 빠르고 안정적으로 만들려는 실용적 목적이 있습니다

즉, 적응형 업데이트는 `모든 파라미터를 같은 기준 보폭으로 움직이는 것`만으로는 놓치기 쉬운 정보를 함께 반영하려고 합니다.

한 문장으로 줄이면 다음과 같습니다.

`Adam은 gradient의 최근 흐름과 좌표별 크기 차이를 함께 참고해, 파라미터마다 더 적응적으로 움직이려는 optimizer이다.`

조금 더 직관적으로 바꾸면 다음처럼 읽을 수 있습니다.

- 단순 update 기준: `지금 보이는 경사 방향으로 같은 기준 보폭을 내딛는다`
- Adam: `최근 몇 걸음의 흔들림을 같이 보고, 좌표마다 보폭을 다르게 조절한다`

예를 들어 어떤 파라미터는 gradient가 계속 크게 흔들리고, 다른 파라미터는 아주 작고 안정적으로 움직인다고 해 보겠습니다. 기본 직접 update는 둘을 같은 learning rate 기준으로 함께 밀지만, Adam 같은 적응형 update는 `지금 이 좌표는 너무 크게 흔들리고 있지 않은가`, `이 좌표는 너무 느리게 움직이고 있지 않은가`를 함께 반영하려고 합니다. 그래서 적응형 업데이트는 `같은 한 걸음`보다 `좌표마다 다른 한 걸음`에 가깝게 느껴집니다.

## Adam을 예로 보면 적응형 업데이트의 무엇이 보이는가

입문 단계에서는 복잡한 수식보다 다음 표가 더 중요합니다.

| 항목 | 단순 update 기준 | Adam |
| --- | --- | --- |
| 기본 감각 | 단순한 한 걸음 업데이트 | 더 많은 누적 정보를 반영한 적응형 업데이트 |
| 장점 | 직관이 단순하고 기준점이 분명함 | 초반 학습이 빠르고 실무에서 다루기 편한 경우가 많음 |
| 주의점 | 학습률 설정에 민감할 수 있음 | 설정이 편해 보여도 항상 최종 일반화가 더 좋다고 단정할 수는 없음 |

이 표에서 핵심은 `어느 것이 절대적으로 우월한가`가 아닙니다. 오히려 다음처럼 이해하는 편이 안전합니다.

`Adam은 단순한 gradient update 기준에 최근 흐름과 좌표별 조절을 더해, 더 적응적인 update를 만들려는 대표적 예다.`

## 왜 Adam이 대표 예로 자주 언급되는가

실무에서는 Adam이 자주 언급됩니다. 여기서 독자가 오래 붙잡아야 할 것은 `많이 쓰인다`보다 `왜 적응형 update의 대표 예로 자주 선택되는가`입니다.

- 초기 설정으로도 비교적 잘 동작하는 경우가 많고
- 학습 초반 손실이 빠르게 줄어드는 경험을 주기 쉽고
- 큰 모델이나 복잡한 데이터에서 입문 장벽이 낮게 느껴질 수 있습니다

하지만 여기서 중요한 주의점이 있습니다.

`Adam이 자주 쓰인다고 해서, 모든 문제에서 무조건 더 좋은 최종 결과를 보장하는 것은 아니다.`

즉, Adam의 인기는 실용성과 편의성에서 오는 부분이 크며, 문제에 따라 다른 판단이 필요합니다.

여기까지를 한 번 압축하면, 적응형 업데이트는 `기본 직접 update 위에 최근 흐름과 좌표별 조절을 더하는 방식`이고, Adam은 그 직관을 읽기 좋은 대표 예입니다.

이 차이를 업데이트 규칙만 남겨 압축하면 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-07/sgd-vs-adam-flow-ko.mmd"
```

이 도식에서 먼저 확인할 결과는, 기본 직접 update가 `현재 gradient에 같은 기준 보폭으로 반응`하는 감각에 가깝다면, Adam은 `최근 흐름과 좌표별 차이를 더 반영해 보폭을 조절`하는 감각에 가깝다는 점입니다.

## 연습 및 예제

이제 예제로 바로 넘어가면 됩니다. 이번 절의 두 예제는 모두 `진짜 Adam 전체 구현`이 아니라, 적응형 업데이트의 핵심 직관을 분리해서 보는 단순화 예제입니다. 첫 예제는 `최근 gradient 흐름을 누적해 보는 축`, 두 번째 예제는 `좌표별로 보폭을 다르게 조절하는 축`을 보여 줍니다. Adam은 이 두 축을 함께 가진 대표 예로 읽으면 됩니다.

입력:

- 현재 위험 가중치 `risk_weight`
- 여러 step에서의 위험 가중치 gradient 목록

출력:

- 단순 직접 업데이트 방식의 연속 위험 가중치 업데이트 결과
- Adam-like 누적 평균을 단순화한 직관적 업데이트 결과
- step별 `direct_delta`와 `adam_like_delta`
- 두 번째 미니 실험에서 두 파라미터의 gradient 크기가 다를 때 좌표별 보폭 조절이 어떻게 나타나는지

문제 상황:

- 적응형 업데이트의 차이는 수식 이름보다 같은 gradient 흐름이 어떤 step별 update로 바뀌는지로 보는 편이 직관적이다

확인할 개념:

- 단순 직접 업데이트는 현재 gradient에 바로 반응한다
- Adam류 방식은 최근 gradient 정보를 누적해 이동량을 조절한다
- Adam류 방식은 좌표별 gradient 크기 차이도 update 크기에 반영하려 한다

입력(input):

압력 미복귀 신호를 읽는 `risk_weight` 하나가 있고, 학습 step마다 `gradient_risk_weight`가 `-4.0`, `-2.0`, `-1.0` 순서로 들어온다고 가정합니다. 같은 gradient 흐름을 보더라도 단순 직접 업데이트와 Adam-like가 `risk_weight`를 얼마나 직접적으로, 혹은 얼마나 누적 평균을 섞어 움직이는지 비교합니다.

코드를 보기 전에 먼저 어떤 쪽 이동량이 더 직접적이고 어떤 쪽이 더 매끈할지 예상해 보면, `현재 gradient 반응`과 `누적 평균 반응`의 차이가 더 잘 보입니다.

| 비교 항목 | 먼저 예상해 볼 update | 예상 이유 |
| --- | --- | --- |
| 첫 번째 `direct_delta` | 가장 크게 움직일 가능성이 큼 | 첫 `gradient_risk_weight` `-4.0`이 learning rate와 바로 곱해져 직접 반영되기 때문입니다. |
| 첫 번째 `adam_like_delta` | `direct_delta`보다 훨씬 작을 가능성이 큼 | moving average가 처음에는 전체 gradient를 부분적으로만 반영하기 때문입니다. |
| step이 지날수록 `direct_delta` | gradient 절대값이 줄어들며 함께 바로 작아질 가능성이 큼 | 단순 직접 업데이트는 현재 `gradient_risk_weight` 크기에 직접 반응합니다. |
| step이 지날수록 `adam_like_delta` | 더 천천히 변하거나 상대적으로 매끈하게 이어질 가능성이 큼 | 이전 step들의 gradient가 moving average 안에 남아 있기 때문입니다. |

이 표의 목적은 정확한 숫자를 미리 암기하는 데 있지 않습니다. 같은 `gradient_risk_weight` 흐름이어도 단순 직접 업데이트는 `지금 기울기`를 바로 반영하고, Adam-like는 `최근 흐름`을 남기며 더 매끈하게 움직일 수 있다는 점을 코드 전에 붙잡는 데 있습니다.

```python
gradient_risk_weight_history = [-4.0, -2.0, -1.0]
risk_weight_direct = 1.0
risk_weight_adam_like = 1.0
learning_rate = 0.1
moving_avg = 0.0
beta = 0.9

print("Direct updates")
for gradient_risk_weight in gradient_risk_weight_history:
    direct_delta = -learning_rate * gradient_risk_weight
    risk_weight_direct = risk_weight_direct + direct_delta
    print(
        " gradient_risk_weight =", gradient_risk_weight,
        "direct_delta =", round(direct_delta, 3),
        "-> risk_weight =", round(risk_weight_direct, 3)
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
 gradient_risk_weight = -4.0 direct_delta = 0.4 -> risk_weight = 1.4
 gradient_risk_weight = -2.0 direct_delta = 0.2 -> risk_weight = 1.6
 gradient_risk_weight = -1.0 direct_delta = 0.1 -> risk_weight = 1.7

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

### 좌표별 조절 미니 실험

위 예제는 적응형 업데이트의 첫 번째 축인 `최근 gradient 흐름`을 남기는 감각을 보여 줍니다. 하지만 적응형 업데이트를 이해하려면 한 가지를 더 봐야 합니다. 큰 모델에서는 파라미터가 하나가 아니라 많고, 각 파라미터의 gradient 크기도 서로 다릅니다. 이때 Adam류 optimizer는 `모든 좌표를 같은 기준 보폭으로 밀기`보다, 좌표별 gradient 크기를 참고해 update를 조절하려고 합니다.

다음 미니 실험은 진짜 Adam 전체 구현이 아니라, Adam의 좌표별 조절 직관 중 `두 번째 모멘트(second moment)로 gradient 크기 차이를 보정한다`는 부분만 단순화한 것입니다. 여기서는 두 파라미터를 비교합니다.

| 파라미터 | 들어오는 gradient 흐름 | 단순 직접 업데이트에서 먼저 예상할 일 | Adam-like 좌표별 조절에서 먼저 예상할 일 |
| --- | --- | --- | --- |
| `risk_weight` | `[-8.0, -4.0]` | gradient가 커서 update도 매우 커진다 | 큰 gradient 좌표는 보폭이 상대적으로 눌린다 |
| `recovery_weight` | `[-0.5, -0.25]` | gradient가 작아서 update도 매우 작아진다 | 작은 gradient 좌표도 완전히 묻히지 않게 조절된다 |

```python
gradient_by_parameter = {
    "risk_weight": [-8.0, -4.0],
    "recovery_weight": [-0.5, -0.25],
}

learning_rate = 0.1
beta2 = 0.9
second_moment = {
    "risk_weight": 0.0,
    "recovery_weight": 0.0,
}

for step in range(2):
    print("step", step + 1)
    for parameter_name, gradient_history in gradient_by_parameter.items():
        gradient = gradient_history[step]
        direct_delta = -learning_rate * gradient

        second_moment[parameter_name] = (
            beta2 * second_moment[parameter_name]
            + (1 - beta2) * gradient * gradient
        )
        adam_like_delta = -learning_rate * gradient / (second_moment[parameter_name] ** 0.5)

        print(
            parameter_name,
            "gradient =", gradient,
            "direct_delta =", round(direct_delta, 3),
            "second_moment =", round(second_moment[parameter_name], 3),
            "adam_like_delta =", round(adam_like_delta, 3),
        )
```

출력은 숫자를 다시 읽는 것보다, `같은 gradient 흐름이 어떤 update 규칙을 거치며 다른 이동 경로가 되는가`를 확인하는 데 집중해 읽습니다.

```text
step 1
risk_weight gradient = -8.0 direct_delta = 0.8 second_moment = 6.4 adam_like_delta = 0.316
recovery_weight gradient = -0.5 direct_delta = 0.05 second_moment = 0.025 adam_like_delta = 0.316
step 2
risk_weight gradient = -4.0 direct_delta = 0.4 second_moment = 7.36 adam_like_delta = 0.147
recovery_weight gradient = -0.25 direct_delta = 0.025 second_moment = 0.029 adam_like_delta = 0.147
```

단순 직접 업데이트에서는 `risk_weight`의 첫 update가 `0.8`이고 `recovery_weight`는 `0.05`입니다. gradient 크기 차이가 update 크기 차이로 거의 그대로 옮겨갑니다. 반면 Adam-like 좌표별 조절에서는 각 좌표가 자기 gradient 크기 이력을 `second_moment`에 따로 쌓고, 그 값으로 update를 나눕니다. 그래서 큰 gradient 좌표는 상대적으로 눌리고, 작은 gradient 좌표는 완전히 묻히지 않습니다.

이 숫자를 Adam 전체 공식으로 외울 필요는 없습니다. 여기서 붙잡아야 할 학습 포인트는 하나입니다. Adam의 `적응형(adaptive)`이라는 말은 단순히 최근 흐름을 기억한다는 뜻만이 아니라, 파라미터 좌표마다 gradient 크기 이력을 따로 보고 update 보폭을 조절하려 한다는 뜻입니다.

다만 이 미니 실험을 `Adam은 서로 다른 파라미터의 update를 항상 같게 만든다`로 읽으면 안 됩니다. 위 숫자에서 두 `adam_like_delta`가 같아 보이는 이유는 두 gradient 흐름의 비율이 같은 단순 예제를 썼기 때문입니다. 실제 Adam에는 첫 번째 모멘트, 두 번째 모멘트, bias correction, 작은 안정화 상수 같은 요소가 함께 들어갑니다. 여기서는 전체 공식을 재현하려는 것이 아니라, `큰 gradient는 자기 크기 이력으로 나뉘고, 작은 gradient도 자기 크기 이력으로 나뉜다`는 좌표별 조절 감각만 분리해 보는 것입니다.

두 예제를 함께 읽으면 적응형 업데이트의 보완점이 두 축으로 나뉩니다.

| 예제 | 보는 축 | 직접 확인할 변화 | 이 절에서 남길 문장 |
| --- | --- | --- | --- |
| `risk_weight` 한 개의 여러 step | 시간축 | 최근 gradient가 moving average에 남아 step별 update가 매끈해진다 | 적응형 업데이트는 현재 gradient만 보지 않고 최근 흐름을 함께 볼 수 있다 |
| `risk_weight`와 `recovery_weight` 비교 | 좌표축 | 파라미터마다 자기 gradient 크기 이력을 따로 쌓아 보폭을 조절한다 | 적응형 업데이트는 모든 파라미터를 같은 기준 보폭으로만 밀지 않는다 |

이 표까지 읽고 나면 적응형 업데이트의 핵심을 `시간축 누적과 좌표축 조절을 update 규칙에 넣는 방식`으로 말할 수 있어야 합니다. 그리고 Adam은 그 방식을 대표적으로 보여 주는 예라고 정리하면 충분합니다.

## 언제 적응형 업데이트 관점을 먼저 꺼내는가

optimizer의 일반 역할을 이해한 뒤에는 `지금 기본 업데이트 감각만으로 충분한가, 아니면 적응형 업데이트 감각이 필요한가`를 나누어 읽는 편이 좋습니다.

| 먼저 보이는 문제 장면 | 먼저 떠올릴 optimizer 관점 | 이유 |
| --- | --- | --- |
| gradient 방향과 보폭의 가장 기본 구조를 설명해야 한다 | 단순 update 기준 | 현재 gradient에 직접 반응하는 기본 업데이트 감각을 가장 분명히 보여 줍니다. |
| 초반 학습이 너무 거칠거나 좌표별 스케일 차이가 크다 | 적응형 업데이트 | 누적 정보와 좌표별 적응을 반영하는 업데이트 감각이 더 중요해집니다. |
| 실무에서 왜 Adam이 자주 쓰이는지 설명해야 한다 | 적응형 업데이트를 먼저 떠올리고 Adam은 대표 예로 본다 | 편의성과 실용성은 크지만 대표 예를 곧바로 일반 원리와 혼동하면 감각이 흐려지기 때문입니다. |
| optimizer를 절대 우열로 외우려는 경향이 보인다 | 단순 기준과 적응형 업데이트를 나란히 둔다 | 속도, 안정성, 일반화를 분리해 읽어야 하기 때문입니다. |

## 체크리스트

- 적응형 업데이트가 기본 update에 무엇을 더 보완하려는지 설명할 수 있는가?
- 적응형 업데이트는 누적 정보와 좌표별 조절을 더 반영하는 방식이라는 점을 설명할 수 있는가?
- 단순 update 기준과 적응형 업데이트를 `현재 gradient에 바로 반응하는 방식`과 `누적 정보와 좌표별 차이를 더 반영하는 방식`의 차이로 설명할 수 있는가?
- 첫 예제에서는 시간축 누적, 두 번째 예제에서는 좌표축 조절을 읽어야 한다는 점을 구분할 수 있는가?
- Adam은 적응형 업데이트의 대표 예일 뿐, 절대적으로 더 좋은 optimizer라고 단정할 수 없다는 점을 말할 수 있는가?

## 출처와 참고 자료

- Léon Bottou, `Large-Scale Machine Learning with Stochastic Gradient Descent`, COMPSTAT, 2010, 확인 날짜: 2026-07-19. [https://doi.org/10.1007/978-3-7908-2604-3_16](https://doi.org/10.1007/978-3-7908-2604-3_16){: target="_blank" rel="noopener noreferrer" }
- Diederik P. Kingma, Jimmy Ba, `Adam: A Method for Stochastic Optimization`, arXiv, 2014, 확인 날짜: 2026-07-19. [https://arxiv.org/abs/1412.6980](https://arxiv.org/abs/1412.6980){: target="_blank" rel="noopener noreferrer" }
- Sebastian Ruder, `An overview of gradient descent optimization algorithms`, arXiv, 2016, 확인 날짜: 2026-07-19. [https://arxiv.org/abs/1609.04747](https://arxiv.org/abs/1609.04747){: target="_blank" rel="noopener noreferrer" }

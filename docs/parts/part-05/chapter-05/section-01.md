# P5-5.1 손실은 어떻게 gradient 신호가 되는가

Section ID: `P5-5.1`
Version: `v2026.07.16`

P5-4장에서는 손실 함수(loss function)가 현재 출력과 목표 사이의 어긋남을 숫자로 만든다는 점을 보았습니다. 하지만 손실 숫자만으로는 아직 파라미터(parameter)를 바꿀 수 없습니다.

손실은 `얼마나 틀렸는가`를 말해 주지만, `어느 파라미터를 어느 방향으로 얼마나 움직일 것인가`는 따로 계산해야 합니다.

이때 필요한 신호가 그래디언트(gradient)입니다. gradient는 손실이 특정 파라미터에 얼마나 민감하게 반응하는지 나타내는 값입니다. 이 gradient를 손실에서 시작해 뒤쪽 계산부터 앞쪽 계산으로 구하는 절차가 역전파(backpropagation)입니다.

뒤 절에서 계산 그래프나 optimizer와 섞여 보일 때는 개념사전의 [역전파(backpropagation)](../../../reference/concept-glossary.md#backpropagation) 항목으로 돌아가 계산 역할부터 다시 구분합니다.

이 절에서는 다음 세 문장을 먼저 고정합니다.

- 손실은 현재 출력이 얼마나 틀렸는지를 숫자로 만듭니다.
- gradient는 각 파라미터가 손실에 어떤 방향과 강도로 연결되는지를 계산합니다.
- optimizer는 그 gradient를 받아 실제 파라미터 업데이트를 수행합니다.

## 이 절의 범위

- 손실 숫자만으로는 왜 파라미터를 바로 업데이트할 수 없는가?
- gradient는 무엇을 추가로 알려 주는가?
- 역전파는 손실에서 gradient를 어떻게 계산하는 절차인가?
- 자동미분(automatic differentiation)은 이 계산을 코드에서 어떻게 가능하게 하는가?
- gradient 계산과 optimizer update는 어떻게 다른가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- 행렬 미분의 엄밀한 전개
- 다층 네트워크 전체의 상세 기호 유도
- 자동미분 엔진의 내부 구현과 reverse-mode automatic differentiation의 엄밀한 일반 이론

복잡한 계산 관계를 노드와 연결로 펼쳐 보는 관점은 P5-5.2에서 이어서 다루고, gradient를 실제 파라미터 이동으로 바꾸는 optimizer의 역할은 P5-7.1, P5-7.2에서 다시 연결합니다. 여기서는 `손실 숫자`가 `파라미터별 gradient 신호`로 바뀌어야 학습이 이어진다는 점을 먼저 닫습니다.

## 이 절의 목표

- 손실, gradient, optimizer update를 구분할 수 있습니다.
- gradient를 `손실이 특정 파라미터에 얼마나 민감한가를 나타내는 신호`로 설명할 수 있습니다.
- 역전파를 `손실에서 출발해 앞쪽 계산으로 거슬러 올라가며 gradient를 계산하는 절차`로 설명할 수 있습니다.
- 자동미분을 `순전파 계산 기록을 이용해 gradient 계산을 자동으로 조직하는 기술`로 설명할 수 있습니다.
- 작은 예제로 손실 크기와 gradient 방향이 같지 않다는 점을 확인할 수 있습니다.

## 손실은 왜 바로 업데이트가 아닌가

손실(loss)은 하나의 숫자입니다. 예를 들어 어떤 모델의 손실이 `4.0`이라고 해도, 그 숫자만으로는 다음 질문에 답할 수 없습니다.

- 어떤 파라미터가 이 손실에 더 크게 연결되어 있는가?
- 그 파라미터를 키워야 하는가, 줄여야 하는가?
- 조금 움직이면 충분한가, 크게 움직여야 하는가?

따라서 학습에는 손실 다음 단계가 필요합니다. 손실을 각 파라미터별 신호로 다시 풀어야 합니다.

| 단계 | 묻는 질문 | 결과 |
| --- | --- | --- |
| 손실 계산(loss computation) | 현재 출력이 목표와 얼마나 어긋났는가? | 손실 숫자 |
| gradient 계산 | 각 파라미터가 손실에 어떤 방향과 강도로 연결되는가? | 파라미터별 gradient |
| optimizer update | 계산된 gradient로 실제로 얼마나 움직일 것인가? | 새 파라미터 값 |

이 표에서 중요한 점은 gradient 계산과 update가 다르다는 것입니다. gradient는 `움직여야 할 신호`이고, optimizer는 그 신호를 사용해 `실제 이동 규칙`을 정합니다.

## gradient는 무엇을 알려 주는가

gradient는 손실이 어떤 파라미터에 얼마나 민감한지를 알려 줍니다. 단순한 예로 다음 식을 봅니다.

\[
predicted\_block\_score = risk\_weight \times pressure\_unrecovered
\]

\[
L = (predicted\_block\_score - target\_block\_score)^2
\]

여기서 손실 \(L\)이 크다는 사실만으로는 `risk_weight`를 키워야 하는지 줄여야 하는지 알 수 없습니다. 예측 점수가 목표보다 낮으면 `risk_weight`를 키우는 쪽이 필요할 수 있고, 예측 점수가 목표보다 높으면 줄이는 쪽이 필요할 수 있습니다.

gradient는 이 차이를 부호와 크기로 남깁니다.

| gradient에서 읽는 것 | 의미 |
| --- | --- |
| 부호(sign) | 파라미터를 조금 키울 때 손실이 커지는가, 작아지는가 |
| 절댓값(magnitude) | 손실이 그 파라미터에 얼마나 민감한가 |

즉, 손실은 `틀림의 크기`를 말하고, gradient는 `파라미터별 민감도 신호`를 말합니다. 실제 update는 보통 손실이 커지는 방향이 아니라 그 반대 방향으로 움직입니다. 그래서 gradient가 양수이면 파라미터를 줄이는 쪽이, gradient가 음수이면 파라미터를 키우는 쪽이 손실을 줄이는 방향이 됩니다.

## 역전파는 어디에 들어가는가

신경망은 여러 계산이 이어진 구조입니다.

\[
input \rightarrow hidden \rightarrow output \rightarrow loss
\]

순전파(forward pass)는 입력에서 출발해 출력과 손실을 계산합니다. 역전파(backpropagation)는 반대로 손실에서 출발해 앞쪽 계산으로 거슬러 올라가며 gradient를 계산합니다.

```mermaid
--8<-- "assets/part-05/chapter-05/loss-to-gradient-role-ko.mmd"
```

이 도식에서 먼저 확인할 결과는, 역전파가 손실을 바로 업데이트로 바꾸는 단계가 아니라 `손실 -> 파라미터별 gradient`를 계산해 다음 optimizer 단계로 넘기는 절차라는 점입니다.

## 왜 뒤에서 앞으로 계산하나

출력층은 손실과 가장 직접적으로 연결되어 있습니다.

- 최종 출력이 있고
- 목표값이 있고
- 그 둘을 비교해 손실이 계산됩니다

따라서 먼저 알기 쉬운 것은 `손실이 최종 출력에 어떻게 반응하는가`입니다. 그다음에는 최종 출력이 바로 앞 층의 값과 파라미터에 의존했다는 점을 이용해, 영향도를 한 단계씩 거꾸로 전달합니다.

순전파와 역전파는 방향만 반대인 같은 말이 아닙니다. 두 흐름은 묻는 질문이 다릅니다.

| 흐름 | 계산 방향 | 묻는 질문 |
| --- | --- | --- |
| 순전파(forward pass) | 입력에서 출력과 손실로 간다 | 지금 무엇을 예측했고 얼마나 틀렸는가 |
| 역전파(backward pass) | 손실에서 앞쪽 파라미터로 거슬러 간다 | 그 틀림이 각 파라미터에 어떤 gradient를 남기는가 |

즉, 역전파를 뒤에서 앞으로 계산하는 이유는 손실이 이미 계산의 끝에 있기 때문입니다. 손실에서 가장 가까운 계산부터 gradient를 구하고, 그 gradient를 앞쪽 계산으로 넘겨야 앞단 파라미터까지 수정 신호가 도달합니다.

이를 아주 단순하게 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-05/forward-loss-backward-flow-ko.mmd"
```

이 도식의 핵심은 `출력의 틀림을 본다 -> 마지막 계산의 gradient를 구한다 -> 그 영향을 앞쪽 계산으로 넘긴다 -> 처음 층까지 반복한다`는 순서입니다.

## 연쇄 법칙(chain rule)은 왜 등장하나

신경망은 함수가 여러 단계로 겹쳐 있는 구조입니다.

예를 들어 아주 단순하게 쓰면 다음과 같습니다.

\[
x \rightarrow z \rightarrow a \rightarrow y \rightarrow loss
\]

손실은 처음 입력이나 앞쪽 파라미터에 직접 달려 있는 것이 아니라, 여러 중간 값을 거쳐 간접적으로 연결됩니다. 이런 구조에서는 한 단계 변화가 다음 단계에 어떤 영향을 주는지를 이어 붙여야 합니다. 이때 등장하는 것이 연쇄 법칙(chain rule)입니다.

다음처럼 이해하면 충분합니다.

`뒤쪽 결과가 앞쪽 값에 의존하고 있다면, 그 의존 관계를 단계별로 곱해 가며 영향도를 전파한다.`

수식보다 먼저 붙잡아야 할 질문은 이것입니다.

`이 층의 출력이 다음 층의 입력이 되었다면, 뒤에서 생긴 틀림은 앞 층에도 gradient를 나누어 줄 수밖에 없지 않은가?`

연쇄 법칙은 이 직관을 수학적으로 가능하게 해 주는 규칙입니다. 역전파는 신경망의 깊은 함수 구조에 연쇄 법칙을 효율적으로 적용해, 손실을 파라미터별 gradient 신호로 바꾸는 절차입니다.

## 자동미분은 왜 함께 알아야 하는가

현대 딥러닝에서는 사용자가 모든 미분식을 손으로 전개하지 않습니다. PyTorch, TensorFlow, JAX 같은 프레임워크는 순전파 계산 과정을 기록해 두었다가, 손실에서 거꾸로 따라가며 gradient 계산을 자동으로 조직합니다.

이 기술이 자동미분(automatic differentiation)입니다.

자동미분은 gradient를 마법처럼 만들어 내는 기능이 아닙니다. 순전파 때 어떤 값이 어떤 연산으로 만들어졌는지 기록하고, 역방향으로 각 연산의 미분 규칙을 적용해 gradient를 계산하는 방법입니다.

이 절에서 필요한 수준은 다음 정도입니다.

| 구분 | 이 절에서 알아야 할 것 | 지금 깊게 다루지 않는 것 |
| --- | --- | --- |
| 역전파 | 손실에서 출발해 앞쪽 파라미터의 gradient를 계산하는 절차 | 깊은 네트워크 전체의 엄밀한 행렬 미분 유도 |
| 자동미분 | 프레임워크가 순전파 기록을 이용해 gradient 계산을 자동으로 조직한다는 점 | 자동미분 엔진의 메모리 관리, 최적화, 내부 구현 |
| 계산 그래프 | 어떤 계산을 기록하고 따라가는지 이해하는 표현 | 그래프 엔진 구현 세부 |

따라서 자동미분은 `몰라도 되는 주제`가 아닙니다. 역전파가 실제 코드에서 실행되는 이유를 이해하기 위해 필요한 개념입니다. 다만 자동미분의 일반 이론과 프레임워크 내부 구현은 P5-5.1의 중심 범위가 아닙니다.

## 사례 및 예시

### 사례 1. 같은 손실이 있어도 update 방향은 다를 수 있다

재기동 차단 점수를 예측하는 작은 모델을 생각해 봅니다. 입력은 `pressure_unrecovered`, 파라미터는 `risk_weight`, 목표는 `target_block_score`입니다.

사람은 먼저 손실이 큰지 작은지를 보려고 합니다. 하지만 학습 단계에서는 손실 크기만 보는 것으로 충분하지 않습니다. 예측이 목표보다 낮아서 `risk_weight`를 키워야 하는 경우와, 예측이 목표보다 높아서 `risk_weight`를 줄여야 하는 경우를 구분해야 합니다.

| 사례 | 예측과 목표의 관계 | 손실만 보면 | gradient까지 보면 |
| --- | --- | --- | --- |
| 조금 낮게 예측 | 목표보다 조금 작다 | 오차가 작다 | `risk_weight`를 약하게 키우는 신호 |
| 많이 낮게 예측 | 목표보다 많이 작다 | 오차가 크다 | `risk_weight`를 강하게 키우는 신호 |
| 높게 예측 | 목표보다 크다 | 오차가 있다 | `risk_weight`를 줄이는 신호 |

이 사례에서 확인해야 할 결과는 하나입니다. 손실은 오차 크기를 알려 주지만, gradient는 파라미터별 방향과 강도를 알려 줍니다.

### 사례 2. 마지막 점수만 고치면 왜 부족한가

실제 신경망은 점수 하나를 바로 만들지 않고, 여러 입력을 중간 표현으로 먼저 묶은 뒤 최종 출력을 냅니다. 예를 들어 `온도 경고`, `압력 경고`, `진동 경고`를 먼저 섞어 `전체 위험 신호`를 만들고, 그다음 최종 정지 점수를 만든다고 생각해 보겠습니다.

이때 최종 점수가 틀렸다고 해서 마지막 층만 보면 충분할 것처럼 느끼기 쉽습니다. 하지만 마지막 점수는 이미 앞단이 만든 `전체 위험 신호`에 기대고 있으므로, 앞단이 어떤 입력을 얼마나 강하게 묶었는지도 함께 고쳐야 할 수 있습니다.

역전파의 직관은 바로 여기서 중요해집니다.

- 최종 출력이 틀렸다면 마지막 연결만이 아니라
- 그 마지막 연결을 만든 앞단 표현에도 책임이 있고
- 그 앞단 표현을 만든 더 앞 가중치에도 gradient가 전달됩니다

즉, 역전파는 `마지막 점수만 고친다`가 아니라 `출력 오차의 gradient를 앞단까지 차례로 나눈다`는 구조입니다. 그래서 이 사례에서 확인해야 할 결과는 마지막 층뿐 아니라 앞단 가중치들에도 서로 다른 크기와 방향의 gradient가 실제로 붙는가입니다.

두 사례를 한 번에 다시 압축하면, 이 절에서 먼저 붙잡아야 할 흐름은 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-05/backprop-direction-and-responsibility-flow-ko.mmd"
```

이 도식은 사례 1의 `점수가 너무 작다/크다`는 방향 감각과 사례 2의 `gradient가 앞단까지 전달된다`는 구조를 한 번에 다시 묶기 위한 것입니다. 여기서 핵심은 `손실을 본다 -> 방향이 생긴다 -> gradient가 뒤에서 앞으로 전달된다`는 흐름입니다.

두 사례를 나란히 놓고 보면, 역전파는 `손실이 크다`는 사실만 말하는 절차가 아니라 `누가 얼마나 어떻게 고쳐져야 하는가`를 각 파라미터별로 다시 적는 절차입니다.

| 장면 | 손실만 보면 남기 쉬운 해석 | gradient 계산이 더 분명하게 남기는 것 |
| --- | --- | --- |
| 점수 하나 보정 | 예측이 작으니 키우고, 크니 줄이면 된다고 느낀다 | 방향뿐 아니라 수정 강도까지 파라미터별로 남긴다 |
| 여러 입력을 거친 최종 점수 | 마지막 출력만 보고 마지막 층만 고치고 싶어진다 | 중간 층과 앞단 층까지 gradient를 나누어 붙인다 |

이 표에서 독자가 먼저 붙잡아야 할 결과는, 핵심이 `손실을 안다`가 아니라 `손실을 파라미터별 gradient 신호로 다시 바꾼다`는 점입니다.

## 연습 및 예제

이번 예제의 목표는 역전파 전체를 구현하는 것이 아닙니다. 아주 작은 식에서 `손실 숫자`와 `gradient 신호`가 어떻게 다른지 확인합니다. 한 사례만 보는 대신 `차단 점수가 작은 경우`와 `차단 점수가 큰 경우`를 같이 돌려, gradient 부호가 어떻게 바뀌는지도 함께 봅니다.

입력:

- 압력 미복귀 정도 `pressure_unrecovered`
- 목표 차단 점수 `target_block_score`
- 현재 위험 가중치 `risk_weight`

출력:

- 예측된 차단 점수
- 손실
- `risk_weight`에 대한 gradient
- gradient가 가리키는 수정 방향

문제 상황:

- gradient는 수식으로만 보면 추상적이므로 차단 점수가 작을 때와 클 때 방향이 어떻게 달라지는지 직접 보는 편이 좋다
- 같은 방향이라도 오차가 더 큰 경우 gradient 절댓값이 더 커지는지 같이 볼 필요가 있다

확인할 개념:

- 손실은 항상 0 이상이므로 방향 정보를 직접 담지 않는다
- gradient 부호를 보면 손실을 줄이기 위해 파라미터를 어느 쪽으로 움직여야 하는지 해석할 수 있다
- gradient 절댓값은 손실이 그 파라미터에 얼마나 민감한지 보여 준다

코드를 보기 전에 먼저 어느 사례가 어떤 신호를 낼지 예상해 보면 좋습니다.

| 사례 | 먼저 예상해 볼 비교 | 예상 이유 |
| --- | --- | --- |
| `slightly_under_block_signal` | `increase_risk_weight`, 하지만 강도는 약할 가능성 | 목표보다 조금만 작기 때문에 방향은 키우기지만 수정량은 크지 않을 수 있습니다. |
| `too_weak_block_signal` | `increase_risk_weight`, 강도는 더 클 가능성 | 같은 방향이라도 목표보다 더 많이 모자라기 때문에 gradient 절댓값이 더 커질 수 있습니다. |
| `too_strong_block_signal` | `decrease_risk_weight` | 목표보다 크므로 반대 방향 신호가 나와야 합니다. |

이 표의 목적은 공식 암기보다 `방향`과 `강도`를 따로 읽는 연습입니다.

직접 바꿔 볼 값은 `risk_weight`입니다. 값을 `2.5`에 가깝게 두면 예측이 목표에 가까워지고, 더 작게 두거나 더 크게 두면 gradient 부호와 절댓값이 어떻게 달라지는지 확인할 수 있습니다.

```python
cases = [
    {
        "name": "slightly_under_block_signal",
        "pressure_unrecovered": 2.0,
        "target_block_score": 5.0,
        "risk_weight": 2.3,
    },
    {
        "name": "too_weak_block_signal",
        "pressure_unrecovered": 2.0,
        "target_block_score": 5.0,
        "risk_weight": 1.5,
    },
    {
        "name": "too_strong_block_signal",
        "pressure_unrecovered": 2.0,
        "target_block_score": 5.0,
        "risk_weight": 3.2,
    },
]

for case in cases:
    pressure_unrecovered = case["pressure_unrecovered"]
    target_block_score = case["target_block_score"]
    risk_weight = case["risk_weight"]

    predicted_block_score = risk_weight * pressure_unrecovered
    loss = (predicted_block_score - target_block_score) ** 2
    gradient_risk_weight = 2 * (
        predicted_block_score - target_block_score
    ) * pressure_unrecovered

    direction = (
        "increase_risk_weight"
        if gradient_risk_weight < 0
        else "decrease_risk_weight"
    )

    print(f"[{case['name']}]")
    print("predicted_block_score =", round(predicted_block_score, 3))
    print("loss =", round(loss, 3))
    print("gradient_risk_weight =", round(gradient_risk_weight, 3))
    print("direction_from_gradient =", direction)
    print("---")
```

출력은 다음처럼 읽습니다.

```text
[slightly_under_block_signal]
predicted_block_score = 4.6
loss = 0.16
gradient_risk_weight = -1.6
direction_from_gradient = increase_risk_weight
---
[too_weak_block_signal]
predicted_block_score = 3.0
loss = 4.0
gradient_risk_weight = -8.0
direction_from_gradient = increase_risk_weight
---
[too_strong_block_signal]
predicted_block_score = 6.4
loss = 1.96
gradient_risk_weight = 5.6
direction_from_gradient = decrease_risk_weight
---
```

이 출력은 `예측 점수 -> 손실 -> gradient` 순서로 나누어 읽어야 합니다.

![사례별 예측 차단 점수](/AiBook/assets/part-05/chapter-05/backprop-example-prediction-ko.png)

첫 그래프는 각 사례의 예측 차단 점수입니다. 목표는 `5.0`입니다. 앞의 두 사례는 목표보다 낮고, 마지막 사례는 목표보다 높습니다.

![사례별 손실](/AiBook/assets/part-05/chapter-05/backprop-example-loss-ko.png)

두 번째 그래프는 손실입니다. 손실은 오차 크기를 보여 주지만 방향을 직접 보여 주지는 않습니다. 예를 들어 손실이 있다는 사실만으로는 `risk_weight`를 키울지 줄일지 알 수 없습니다.

![사례별 위험 가중치 gradient](/AiBook/assets/part-05/chapter-05/backprop-example-gradient-ko.png)

세 번째 그래프에서 방향이 드러납니다. 음수 gradient는 `risk_weight`를 키우는 쪽으로 읽고, 양수 gradient는 줄이는 쪽으로 읽습니다. 그래서 이 예제의 핵심 변화는 `손실 숫자`가 아니라 `파라미터별 gradient 신호`입니다.

세 사례를 다시 묶으면 `부호`와 `크기`를 같이 읽어야 한다는 점이 분명해집니다.

| 사례 | 손실에서 보이는 것 | gradient에서 보이는 것 | 지금 읽어야 할 핵심 |
| --- | --- | --- | --- |
| `slightly_under_block_signal` | 오차가 작다 | 약한 증가 신호 | 목표보다 조금 모자라므로 키우되, 미세 조정에 가깝습니다. |
| `too_weak_block_signal` | 오차가 크다 | 강한 증가 신호 | 같은 증가 방향이라도 훨씬 더 많이 모자라므로 gradient 절댓값이 커집니다. |
| `too_strong_block_signal` | 오차가 있다 | 감소 신호 | 방향 자체가 반대로 바뀌어 `risk_weight`를 줄여야 합니다. |

- 차단 점수가 너무 작으면 gradient가 음수가 되어 `risk_weight`를 키우는 방향 신호를 줍니다.
- 차단 점수가 너무 크면 gradient가 양수가 되어 `risk_weight`를 줄이는 방향 신호를 줍니다.
- 같은 방향 안에서도 오차가 더 크면 gradient 절댓값이 커져 더 강한 수정 신호가 됩니다.

이 예제에서 반드시 남겨야 할 말은 다음입니다.

`손실은 틀림을 숫자로 만들고, gradient는 그 틀림을 파라미터별 방향과 강도 신호로 다시 풀어 쓴다.`

이 결과를 손실과 gradient 기준으로 다시 나누면 차이가 더 또렷합니다.

| 실행 결과에서 보인 차이 | 손실만 보면 남기 쉬운 해석 | gradient까지 보면 바뀌는 해석 |
| --- | --- | --- |
| `slightly_under_block_signal`와 `too_weak_block_signal`는 둘 다 차단 점수가 작다 | 둘 다 위험 가중치를 키우면 된다고만 읽기 쉽다 | 같은 방향이라도 누가 더 강한 증가 신호를 받는지 읽는다 |
| `too_weak_block_signal`와 `too_strong_block_signal`는 둘 다 손실이 있다 | 둘 다 오차가 있으니 비슷한 수정이 필요하다고 느끼기 쉽다 | 하나는 증가, 다른 하나는 감소로 방향 자체가 갈린다 |
| 손실 숫자 하나만 먼저 보인다 | 오차 크기만 알면 충분하다고 느끼기 쉽다 | 실제 업데이트에는 파라미터별 gradient 신호가 추가로 필요하다고 읽는다 |

이 표까지 읽고 나면, 역전파의 핵심이 `손실을 계산했다`가 아니라 `손실을 파라미터별 방향·크기 신호로 다시 풀어 썼다`는 점이 더 분명해집니다.

## 다층 신경망에서는 무엇이 더 어려워지나

방금 예제는 파라미터가 하나뿐이라 단순했습니다. 다층 신경망에서는 상황이 바로 어려워집니다.

- 출력이 여러 층을 거쳐 오고
- 각 층마다 파라미터가 많고
- 각 층의 값이 다음 층의 입력이 됩니다

따라서 손실의 영향도를 각 층과 파라미터에 다시 분배해 주는 절차가 필요합니다. 역전파는 손실에서 출발해 앞쪽 계산으로 거슬러 올라가며 이 gradient들을 효율적으로 계산합니다. 자동미분은 프레임워크가 이 계산을 실행 기록을 바탕으로 자동으로 조직하게 해 줍니다.

다음처럼 기억하면 충분합니다.

`층이 깊어질수록 gradient를 직접 손으로 쓰기는 어렵지만, 역전파는 그 계산을 체계적으로 뒤에서 앞으로 전달한다.`

역전파의 역사에서는 여러 전조와 기여가 있지만, 신경망 학습 맥락에서 널리 알려진 전환점은 Rumelhart, Hinton, Williams의 1986년 논문입니다. 이 작업은 다층 신경망이 유용한 내부 표현을 학습할 수 있음을 널리 보여 주는 계기가 되었습니다.

더 넓게 보면 Paul Werbos의 1974년 박사 논문 같은 더 이른 작업도 자주 언급됩니다. 여기서는 다음 정도로 기억하면 충분합니다.

- 더 이른 수학적/최적화적 아이디어가 있었고
- 1980년대 중반에 신경망 학습 절차로 널리 알려지며 큰 전환점이 되었다

커리큘럼 관점에서도 역전파는 중요한 절입니다. P5-4.1, P5-4.2에서 손실 함수를 왜 두는지 배웠다면, 이제 그 손실이 각 층 파라미터로 어떻게 전달되는지를 이해해야 합니다. 이유는 단순합니다.

- 손실 함수가 있어도
- 그 손실이 각 층에 어떻게 연결되는지 모르면
- 실제 학습 업데이트가 불가능하기 때문입니다

즉, 역전파는 `딥러닝이 실제로 학습된다`는 말을 가능하게 하는 gradient 계산 절차입니다.

다음 절 P5-5.2에서는 이 실행 기록을 계산 그래프(computation graph)로 펼쳐 봅니다. 계산 그래프를 보면, 순전파에서 어떤 중간값이 만들어지고 역전파에서 gradient가 어떤 경로로 되돌아가는지 더 분명해집니다.

## 언제 gradient 계산 관점으로 읽는가

| 먼저 보이는 문제 장면 | gradient 계산 관점이 필요한 이유 | 바로 다음에 넘길 질문 |
| --- | --- | --- |
| 손실은 알겠는데 어느 파라미터를 바꿔야 할지 모르겠다 | 손실을 파라미터별 방향과 강도 신호로 풀어야 한다 | 복잡한 계산에서는 그 신호를 어떻게 추적하는가 |
| 손실이 크면 무조건 크게 업데이트하면 된다고 느껴진다 | 손실 크기와 update 방향은 같은 정보가 아니다 | optimizer는 이 gradient를 어떤 보폭으로 사용할 것인가 |
| 프레임워크가 `.backward()`로 gradient를 구하는 것이 마법처럼 보인다 | 자동미분이 순전파 기록을 이용한다는 점을 알아야 한다 | 계산 그래프는 무엇을 기록하는가 |

## 체크리스트

- 손실이 계산되었다고 해서 바로 파라미터가 업데이트되는 것이 아니라는 점을 설명할 수 있는가?
- gradient가 파라미터별 방향과 강도 신호라는 점을 설명할 수 있는가?
- 역전파가 손실에서 출발해 앞쪽 계산으로 거슬러 올라가며 gradient를 계산하는 절차라는 점을 말할 수 있는가?
- 자동미분이 순전파 계산 기록을 이용해 gradient 계산을 자동으로 조직한다는 점을 설명할 수 있는가?
- gradient 계산과 optimizer update를 구분할 수 있는가?
- 다음 절에서 계산 그래프를 보는 이유가 `복잡한 gradient 계산을 추적하기 위해서`라는 점을 이해했는가?

## 출처와 참고 자료

- David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams, `Learning representations by back-propagating errors`, Nature, 1986, 확인 날짜: 2026-06-29.
- Paul J. Werbos, `Beyond Regression: New Tools for Prediction and Analysis in the Behavioral Sciences`, Harvard University doctoral thesis, 1974, 확인 날짜: 2026-06-29.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }

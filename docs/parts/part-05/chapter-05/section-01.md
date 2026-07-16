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
| 부호(sign) | 파라미터를 어느 방향으로 움직여야 손실이 줄어드는가 |
| 절댓값(magnitude) | 손실이 그 파라미터에 얼마나 민감한가 |

즉, 손실은 `틀림의 크기`를 말하고, gradient는 `파라미터별 수정 신호`를 말합니다.

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

연쇄 법칙(chain rule)은 이때 등장합니다. 손실이 앞쪽 파라미터에 직접 달려 있는 것이 아니라 여러 중간 계산을 거쳐 연결되어 있기 때문입니다. 역전파는 각 단계의 영향도를 뒤에서 앞으로 이어 붙여 파라미터별 gradient를 구합니다.

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

### 사례. 같은 손실이 있어도 update 방향은 다를 수 있다

재기동 차단 점수를 예측하는 작은 모델을 생각해 봅니다. 입력은 `pressure_unrecovered`, 파라미터는 `risk_weight`, 목표는 `target_block_score`입니다.

사람은 먼저 손실이 큰지 작은지를 보려고 합니다. 하지만 학습 단계에서는 손실 크기만 보는 것으로 충분하지 않습니다. 예측이 목표보다 낮아서 `risk_weight`를 키워야 하는 경우와, 예측이 목표보다 높아서 `risk_weight`를 줄여야 하는 경우를 구분해야 합니다.

| 사례 | 예측과 목표의 관계 | 손실만 보면 | gradient까지 보면 |
| --- | --- | --- | --- |
| 조금 낮게 예측 | 목표보다 조금 작다 | 오차가 작다 | `risk_weight`를 약하게 키우는 신호 |
| 많이 낮게 예측 | 목표보다 많이 작다 | 오차가 크다 | `risk_weight`를 강하게 키우는 신호 |
| 높게 예측 | 목표보다 크다 | 오차가 있다 | `risk_weight`를 줄이는 신호 |

이 사례에서 확인해야 할 결과는 하나입니다. 손실은 오차 크기를 알려 주지만, gradient는 파라미터별 방향과 강도를 알려 줍니다.

## 연습 및 예제

이번 예제의 목표는 역전파 전체를 구현하는 것이 아닙니다. 아주 작은 식에서 `손실 숫자`와 `gradient 신호`가 어떻게 다른지 확인합니다.

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

- 손실이 있어도 파라미터를 어느 방향으로 바꿀지는 아직 정해지지 않았다
- gradient를 계산해야 방향과 강도를 읽을 수 있다

확인할 개념:

- 손실은 항상 0 이상이므로 방향 정보를 직접 담지 않는다
- gradient 부호는 파라미터를 키울지 줄일지 알려 준다
- gradient 절댓값은 손실이 그 파라미터에 얼마나 민감한지 보여 준다

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

세 사례를 다시 묶으면 다음과 같습니다.

| 사례 | 손실에서 보이는 것 | gradient에서 보이는 것 |
| --- | --- | --- |
| `slightly_under_block_signal` | 오차가 작다 | 약한 증가 신호 |
| `too_weak_block_signal` | 오차가 크다 | 강한 증가 신호 |
| `too_strong_block_signal` | 오차가 있다 | 감소 신호 |

이 예제에서 반드시 남겨야 할 말은 다음입니다.

`손실은 틀림을 숫자로 만들고, gradient는 그 틀림을 파라미터별 방향과 강도 신호로 다시 풀어 쓴다.`

## 다층 신경망에서는 무엇이 더 어려워지나

방금 예제는 파라미터가 하나뿐이라 단순했습니다. 다층 신경망에서는 손실이 여러 중간 계산을 거쳐 많은 파라미터에 연결됩니다.

따라서 각 파라미터의 gradient를 손으로 모두 전개하기 어렵습니다. 역전파는 손실에서 출발해 앞쪽 계산으로 거슬러 올라가며 이 gradient들을 효율적으로 계산합니다. 자동미분은 프레임워크가 이 계산을 실행 기록을 바탕으로 자동으로 조직하게 해 줍니다.

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

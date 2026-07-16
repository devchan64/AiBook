# P5-7.1 옵티마이저(optimizer)의 역할

Section ID: `P5-7.1`
Version: `v2026.07.16`

P5-6장에서는 학습(learning)과 모델 실행(inference), 그리고 학습 모드(training mode)와 평가 모드(evaluation mode)를 구분했습니다. 여기까지 오면 이제 아주 직접적인 질문이 남습니다.

손실도 계산했고, gradient도 구했는데, 실제로 가중치는 누가 바꾸는가?

그 역할을 맡는 것이 옵티마이저(optimizer)입니다.

옵티마이저는 역전파가 계산한 gradient를 받아, 손실을 줄이는 방향으로 파라미터를 실제로 업데이트하는 규칙이다.

손실, gradient, update의 역할이 다시 섞이면 개념사전의 [옵티마이저(optimizer)](../../../reference/concept-glossary.md#optimizer) 항목을 기준으로 역할을 다시 나눕니다.

여기서는 다음 세 문장을 먼저 붙잡는 편이 좋습니다.

- 손실은 틀림을 숫자로 만듭니다.
- 역전파는 각 가중치의 방향 신호를 계산합니다.
- 옵티마이저는 그 신호를 실제 업데이트로 바꿉니다.

## 이 절의 범위

- 옵티마이저는 학습 절차에서 어떤 자리에 있는가?
- 손실 함수, 역전파, 학습률(learning rate)과 어떤 관계가 있는가?
- 왜 `좋은 gradient`만으로는 충분하지 않고 `업데이트 규칙`이 따로 필요한가?
- optimizer를 단순한 구현 함수가 아니라 파라미터를 실제로 바꾸는 역할로 읽으려면 무엇을 보아야 하는가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- SGD, Momentum, Adam의 세부 공식 비교
- adaptive optimization의 이론적 수렴 분석
- optimizer state의 메모리 최적화

대표 옵티마이저 비교는 P5-7.2에서 이어서 다루고, adaptive optimization의 이론적 수렴 분석은 P5-7.3 보충학습에서 논문을 처음 읽는 기준만 따로 정리합니다. regularization과의 역할 차이는 P5-8.1에서 다시 연결합니다. optimizer state의 메모리 최적화는 이 책의 현재 본편 범위 밖에 둡니다.

## 이 절의 목표

- 옵티마이저를 `gradient를 실제 업데이트로 바꾸는 규칙`으로 설명할 수 있습니다.
- 손실 함수, 역전파, 옵티마이저의 역할을 구분할 수 있습니다.
- 학습률이 optimizer의 update 보폭에 붙는 설정값이라는 점을 말할 수 있습니다.
- 실행 가능한 Python 예제로 gradient와 update의 차이를 확인할 수 있습니다.

## 옵티마이저는 학습 절차의 어디에 있는가

Part 5 초반 흐름을 다시 묶어 보면 딥러닝 학습은 다음 순서로 진행됩니다.

1. 순전파(forward pass)로 예측을 계산합니다
2. 손실 함수(loss function)로 틀림을 숫자로 만듭니다
3. 역전파(backpropagation)로 gradient를 계산합니다
4. 옵티마이저(optimizer)가 파라미터를 업데이트합니다

즉, 옵티마이저는 gradient를 계산하는 장치가 아니라, `계산된 gradient를 보고 다음 파라미터를 정하는 장치`입니다.

이를 아주 단순하게 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-07/optimizer-loop-flow-ko.mmd"
```

다음 구분을 먼저 잡아야 `틀림을 재는 단계`, `책임을 계산하는 단계`, `실제로 파라미터를 움직이는 단계`를 섞지 않게 됩니다.

- 손실 함수: 무엇이 틀렸는지 숫자로 말해 준다
- 역전파: 누가 얼마나 틀림에 기여했는지 계산해 준다
- 옵티마이저: 그래서 실제로 얼마만큼 바꿀지 결정한다

이 세 문장이 Part 5의 학습 계산 흐름을 읽는 가장 작은 지도입니다. 독자는 세 용어를 따로 외우기보다, `틀림 -> 책임 -> 실제 수정`의 순서로 묶어 기억하는 편이 훨씬 안전합니다.

## 왜 gradient만으로는 충분하지 않은가

gradient는 방향(direction)에 대한 정보입니다. 보통은 `어느 쪽으로 움직이면 손실이 줄어드는가`를 알려 줍니다. 하지만 실제 업데이트에는 방향만으로 부족합니다.

예를 들어 다음 질문이 남습니다.

- 한 번에 얼마나 크게 움직일 것인가?
- 이전 단계에서 움직이던 방향을 얼마나 참고할 것인가?
- 좌표마다 다른 속도로 움직일 것인가?

즉, gradient는 지도(map)에 가깝고, optimizer는 이동 규칙(rule of movement)에 가깝습니다.

다음처럼 이해하면 충분합니다.

`gradient가 길의 방향표지라면, optimizer는 얼마나 빠르게 어떤 방식으로 걸을지를 정하는 규칙이다.`

이 비유를 실제 문장으로 다시 쓰면 다음과 같습니다.

- gradient는 `어느 쪽이 내려가는가`를 알려 줍니다.
- optimizer는 `얼마나 움직일까`, `한 번에 얼마나 바꿀까`를 정합니다.
- 그래서 같은 gradient라도 optimizer와 learning rate가 다르면 실제 학습 모습이 달라질 수 있습니다.

## optimizer가 update를 만들 때 learning rate는 어디에 붙는가

옵티마이저의 역할을 설명할 때 학습률(learning rate)이 함께 나오는 이유는, optimizer가 gradient를 실제 update로 바꾸는 순간에 학습률이 보폭으로 붙기 때문입니다. 학습률 자체가 가중치를 바꾸는 것은 아니지만, optimizer가 `얼마나 크게 바꿀지`를 정할 때 핵심 배율로 쓰입니다.

너무 작으면:

- 학습이 매우 느려질 수 있고
- 손실이 줄어드는 데 오래 걸릴 수 있습니다

너무 크면:

- 좋은 방향을 알고도 지나쳐 버릴 수 있고
- 손실이 불안정하게 흔들릴 수 있습니다

즉, 학습률은 optimizer가 update를 만들 때 사용하는 `업데이트의 보폭(step size)`입니다.

Part 4에서 하이퍼파라미터(hyperparameter)를 다루었듯, 학습률은 학습으로 자동 생성되는 파라미터가 아니라 사람이 정하거나 탐색하는 설정값입니다.

여기서는 다음 구분을 함께 잡는 편이 안전합니다.

| 값 | 역할 |
| --- | --- |
| gradient | 현재 위치에서 어느 방향이 내려가는지 알려 주는 신호 |
| learning rate | 그 방향으로 한 번에 얼마나 움직일지 정하는 보폭 |
| optimizer | 그 보폭과 규칙을 적용해 실제 이동을 만드는 절차 |

이 차이는 손실 곡선 위에서 보면 더 분명합니다. 같은 위치에서 내려갈 방향을 알아도, 보폭이 너무 작으면 거의 움직이지 못하고, 적절하면 낮은 손실 근처로 가며, 너무 크면 좋은 지점을 지나쳐 손실이 다시 커질 수 있습니다.

![learning rate와 손실 곡선 위 보폭](../../../assets/part-05/chapter-07/learning-rate-step-size-ko.svg)

이 그래프에서 중요한 것은 `gradient 방향이 맞다`와 `optimizer가 만든 update가 적절하다`가 같은 말이 아니라는 점입니다. optimizer의 역할을 읽을 때는 방향 신호뿐 아니라 그 신호가 실제로 어느 위치까지 파라미터를 움직였는지를 함께 봐야 합니다.

## 옵티마이저는 왜 하나만 있지 않은가

딥러닝 역사에서는 처음부터 모든 상황에 완벽한 optimizer 하나가 있었던 것이 아닙니다. 네트워크가 깊어지고, 데이터가 커지고, 파라미터 수가 늘어나면서 업데이트 규칙도 더 정교해질 필요가 있었습니다.

여기서는 다음 이유를 먼저 잡으면 됩니다.

- 어떤 문제는 단순하고 안정적인 업데이트가 중요합니다
- 어떤 문제는 학습 속도가 더 중요합니다
- 어떤 문제는 좌표별 스케일 차이나 잡음이 큽니다

즉, optimizer는 단순한 구현 취향이 아니라, `학습 문제를 어떤 방식으로 풀 것인가`에 대한 선택입니다.

독자용으로 더 줄이면 다음처럼 기억할 수 있습니다.

`옵티마이저는 gradient를 받아 파라미터를 실제로 어디까지 움직일지 정하는 update 규칙이다.`

## 사례 및 예시

이 절의 사례는 optimizer를 고르는 사례가 아니라, `gradient가 계산된 뒤 실제 파라미터 update가 어떻게 만들어졌는가`를 읽는 사례입니다. 따라서 사례를 볼 때는 항상 다음 순서로 확인합니다.

1. gradient가 계산됐는가
2. optimizer가 그 gradient를 어느 크기의 update로 바꿨는가
3. update 뒤 파라미터와 손실이 실제로 어떻게 달라졌는가

### 사례 1. gradient는 계산됐지만 파라미터가 거의 움직이지 않는 경우

학습 로그에서 손실이 조금씩 내려가고 있다고 해 보겠습니다. 사람은 보통 `방향은 맞으니 더 오래 돌리면 되겠다`고 판단하기 쉽습니다. 하지만 몇 시간 동안 검증 성능이 거의 움직이지 않는다면, 실제 문제는 gradient의 방향보다 업데이트 보폭이 지나치게 작은 데 있을 수 있습니다.

이 장면에서 optimizer 관점은 질문을 바꿉니다. `gradient가 계산됐는가`에서 멈추지 않고, `optimizer가 그 gradient를 실제 파라미터 변화로 충분히 바꿨는가`를 봅니다. 학습률이 너무 작거나 update rule이 지나치게 보수적이면 방향 신호는 맞아도 한 step의 이동량이 작아, 손실 곡선은 내려가지만 실용적인 속도로는 거의 전진하지 못합니다.

그래서 이 사례에서 확인해야 할 결과는 손실이 줄고 있다는 사실만이 아닙니다. 같은 학습 시간 안에 검증 성능이 실제로 따라 올라오는지, update 뒤 파라미터 변화량이 너무 작게 묶여 있지는 않은지를 함께 봐야 합니다.

| 사람이 먼저 보기 쉬운 기준 | optimizer 관점으로 다시 읽는 기준 |
| --- | --- |
| gradient가 있으니 오래 돌리기만 하면 된다 | 같은 gradient라도 optimizer가 만든 실제 update가 너무 작을 수 있다 |
| 손실이 조금씩 줄면 설정도 괜찮다고 느끼기 쉽다 | 파라미터가 실용적인 폭으로 바뀌고 있는지 따로 봐야 한다 |
| 느린 학습은 데이터나 모델 문제라고만 생각하기 쉽다 | update rule과 learning rate가 병목일 수 있다 |
| 확인할 로그를 손실 하나로 좁히기 쉽다 | 같은 시간 대비 검증 성능, 파라미터 이동량, update 후 손실 변화를 같이 봐야 한다 |

### 사례 2. gradient 방향은 맞지만 optimizer update가 너무 큰 경우

반대로 손실이 내려가다가 다시 튀고, 한 배치에서는 좋아졌다가 다음 배치에서는 다시 나빠지는 경우도 있습니다. 사람은 이 장면을 보면 `모델이 전혀 못 배우는 것 아닌가`라고 느끼기 쉽습니다. 하지만 실제로는 내려가는 방향은 잡았는데 한 번에 너무 크게 움직여 좋은 지점을 계속 지나치는 경우가 많습니다.

이때는 gradient가 쓸모없어서가 아니라, 학습률이 너무 크거나 optimizer 설정이 현재 문제에 비해 거칠어서 update가 과격해진 것일 수 있습니다. 표면 현상은 `불안정한 손실`이지만, 구조적으로는 `optimizer가 방향 신호를 너무 큰 파라미터 이동으로 바꾼 상황`입니다. 이 경우에는 손실이 들쭉날쭉한지뿐 아니라, update 뒤 예측값이 목표를 반복해서 넘어서는지까지 같이 봐야 합니다.

그래서 이 사례에서 확인해야 할 결과는 학습이 아예 안 되는지보다, update 보폭이 커서 좋은 지점을 반복해서 지나치고 있는가입니다. P5-7.2에서는 이 문제를 더 확장해, SGD와 Adam처럼 서로 다른 optimizer가 같은 gradient 흐름을 어떤 방식으로 다르게 움직이는지 비교합니다.

두 사례를 같이 놓고 보면 optimizer를 `업데이트 함수`보다 `학습 동역학을 읽는 기준`으로 보는 이유가 더 분명해집니다.

| 장면 | 사람이 먼저 보기 쉬운 결과 | optimizer 관점에서 실제로 구분해야 할 것 | 바로 다음에 확인할 것 |
| --- | --- | --- | --- |
| 파라미터가 거의 움직이지 않는 학습 | gradient만 있으면 더 오래 돌리면 된다고 보기 쉽습니다. | optimizer가 gradient를 너무 작은 update로 바꾸고 있을 수 있습니다. | update 뒤 파라미터 변화량과 검증 성능 변화를 같이 봅니다. |
| update 뒤 손실이 계속 흔들리는 학습 | 모델이 아예 못 배우는 것으로 보기 쉽습니다. | optimizer가 방향 신호를 너무 큰 update로 바꾸고 있을 수 있습니다. | 손실 진동이 `gradient 실패`인지 `과한 update`인지 구분해 봅니다. |

두 사례를 한 번에 다시 압축하면, optimizer의 역할을 읽는 첫 흐름은 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-07/optimizer-step-bridge-ko.mmd"
```

이 도식은 느린 학습과 흔들리는 학습을 따로 다시 설명하려는 것이 아니라, 두 사례가 공통으로 보여 준 `optimizer가 gradient를 실제 update로 바꾸는 방식이 결과를 바꾼다`는 흐름을 한 번에 다시 붙잡기 위한 것입니다.

## 연습 및 예제

이번 예제의 목표는 gradient 계산과 optimizer가 만든 실제 update를 분리해서 보는 것입니다. 여기서 learning rate는 독립 주제가 아니라, optimizer가 `optimizer_delta = -learning_rate * gradient`라는 update를 만들 때 쓰는 배율입니다. 따라서 출력도 learning rate 자체보다 `optimizer_delta`가 얼마나 달라지는지를 중심으로 읽습니다.

입력:

- 현재 위험 가중치 `risk_weight`
- 압력 미복귀 정도 `pressure_unrecovered`
- 목표 차단 점수 `target_block_score`
- 학습률 `learning_rate`

출력:

- 예측된 차단 점수
- 손실
- gradient
- optimizer가 만든 update 값
- learning rate별 업데이트 후 가중치
- 업데이트 뒤 목표값에 더 가까워지는 정도 비교

문제 상황:

- learning rate는 gradient 자체를 바꾸지 않지만, optimizer가 만드는 위험 가중치 update 폭을 크게 바꾼다
- 너무 큰 learning rate는 좋은 방향을 알고도 지나칠 수 있으므로 결과를 함께 비교해야 한다

확인할 개념:

- optimizer는 gradient를 실제 update 값으로 바꾼다
- 같은 gradient라도 optimizer가 만든 update 값에 따라 이동 폭과 학습 안정성이 달라질 수 있다
- optimizer update 뒤 예측이 목표에 얼마나 가까워졌는지를 같이 봐야 한다

입력(input):

위에 정리한 `pressure_unrecovered`, `target_block_score`, 초기 가중치 `risk_weight`와 여러 learning rate를 사용합니다.

코드를 보기 전에 먼저 어느 learning rate가 `한 번의 update 뒤` 목표 차단 점수 6.0에 가장 가까워질지 예상해 보면 좋습니다.

| learning rate | 먼저 예상해 볼 optimizer update | 예상 이유 |
| --- | --- | --- |
| `0.01` | 너무 조금만 움직일 가능성 | gradient 방향은 맞아도 보폭이 작아 목표에 덜 가까워질 수 있습니다. |
| `0.1` | 비교적 적절할 가능성 | 한 번의 이동으로 의미 있게 가까워지되 지나치지 않을 수 있습니다. |
| `0.5` | 지나칠 가능성 | 같은 방향이라도 너무 크게 움직여 목표를 넘어설 수 있습니다. |

이 표의 목적은 `같은 gradient`와 `optimizer가 만든 다른 update 결과`를 분리해서 읽는 것입니다.

```python
pressure_unrecovered = 2.0
target_block_score = 6.0
risk_weight = 1.0
prediction = pressure_unrecovered * risk_weight
loss = (prediction - target_block_score) ** 2
gradient_risk_weight = 2 * (prediction - target_block_score) * pressure_unrecovered

print("predicted_block_score =", round(prediction, 3))
print("loss =", round(loss, 3))
print("gradient_risk_weight =", round(gradient_risk_weight, 3))
for lr in [0.01, 0.1, 0.5]:
    optimizer_delta = -lr * gradient_risk_weight
    updated_risk_weight = risk_weight + optimizer_delta
    updated_prediction = pressure_unrecovered * updated_risk_weight
    updated_loss = (updated_prediction - target_block_score) ** 2
    print(
        "lr =", lr,
        "-> optimizer_delta =", round(optimizer_delta, 3),
        "-> updated_risk_weight =", round(updated_risk_weight, 3),
        ", updated_block_score =", round(updated_prediction, 3),
        ", updated_loss =", round(updated_loss, 3),
    )
```

출력에서는 `predicted_block_score`, `loss`, `gradient_risk_weight`를 먼저 보고, learning rate마다 optimizer가 만든 `optimizer_delta`가 얼마나 달라지는지 이어서 보면 됩니다.

```text
predicted_block_score = 2.0
loss = 16.0
gradient_risk_weight = -16.0
lr = 0.01 -> optimizer_delta = 0.16 -> updated_risk_weight = 1.16 , updated_block_score = 2.32 , updated_loss = 13.542
lr = 0.1 -> optimizer_delta = 1.6 -> updated_risk_weight = 2.6 , updated_block_score = 5.2 , updated_loss = 0.64
lr = 0.5 -> optimizer_delta = 8.0 -> updated_risk_weight = 9.0 , updated_block_score = 18.0 , updated_loss = 144.0
```

이 출력은 같은 gradient가 optimizer의 update 규칙을 거치며 서로 다른 `optimizer_delta`로 바뀌는 장면입니다. 따라서 `gradient가 얼마인가`에서 멈추지 말고, optimizer가 만든 update 값, 업데이트된 가중치, 업데이트 후 점수, 업데이트 후 손실을 단계별로 나누어 읽습니다.

![learning rate별 업데이트 후 위험 가중치](/AiBook/assets/part-05/chapter-07/optimizer-example-updated-weight-ko.png)

첫 그래프는 같은 gradient `-16.0`을 optimizer가 update로 바꾼 뒤 위험 가중치가 얼마나 달라지는지 보여 줍니다. 보이지 않는 중간값은 `optimizer_delta`입니다. `0.01`은 `0.16`만 움직이고, `0.5`는 `8.0`만큼 같은 방향으로 너무 멀리 이동합니다.

![learning rate별 업데이트 후 차단 점수](/AiBook/assets/part-05/chapter-07/optimizer-example-updated-score-ko.png)

두 번째 그래프는 업데이트된 가중치가 다시 예측 차단 점수로 바뀐 결과입니다. 목표는 `6.0`이고, `0.1`은 목표에 가까워지지만 `0.5`는 목표를 크게 넘어섭니다. 이 단계에서 `방향이 맞다`와 `결과가 적절하다`가 다른 말이라는 점이 보입니다.

![learning rate별 업데이트 후 손실](/AiBook/assets/part-05/chapter-07/optimizer-example-updated-loss-ko.png)

세 번째 그래프는 업데이트 후 손실입니다. `0.1`은 손실을 크게 줄이지만, `0.5`는 같은 gradient 방향을 사용했는데도 optimizer가 만든 `optimizer_delta`가 너무 커서 손실을 더 키웁니다. 즉, 이 예제의 핵심 변화는 `gradient -> optimizer_delta -> 새 가중치 -> 새 예측 -> 새 손실`입니다.

즉, 같은 gradient라도 optimizer 설정에 따라 실제 이동 폭은 크게 달라집니다. 운영 판단 관점으로 읽으면, 같은 `압력 미복귀 위험` 신호라도 learning rate에 따라 `조금 더 위험하게 읽는 보정`, `거의 맞는 수준의 보정`, `과하게 차단 쪽으로 튀는 보정`이 갈린다는 뜻입니다.

이 예제에서 독자가 꼭 읽어야 할 것은 다음입니다.

- `gradient_risk_weight`는 그대로인데 결과는 달라질 수 있습니다.
- 달라지는 이유는 optimizer가 만든 `optimizer_delta`가 다르기 때문입니다.
- `0.1`은 목표에 가까워졌지만 `0.5`는 방향은 맞아도 너무 크게 움직여 오히려 손실을 키웠습니다.
- 따라서 `gradient를 구했다`와 `학습이 잘 된다`는 같은 말이 아닙니다.

출력 숫자를 읽을 때는 `gradient 자체`와 `update 결과`를 분리해서 봐야 합니다.

| learning rate | optimizer가 만든 update | gradient만 보면 남기 쉬운 해석 | optimizer까지 보면 바뀌는 해석 |
| --- | --- | --- | --- |
| `0.01` | `optimizer_delta = 0.16` | 방향만 맞으니 학습은 충분히 잘 시작됐다고 보기 쉽습니다. | update가 너무 작아 실용적인 속도로는 거의 전진하지 못하고 있습니다. |
| `0.1` | `optimizer_delta = 1.6` | gradient가 특별히 더 좋아졌다고 보기 쉽습니다. | gradient는 같고, 달라진 것은 optimizer update라 실제 이동이 더 적절했던 것입니다. |
| `0.5` | `optimizer_delta = 8.0` | gradient가 틀렸거나 모델이 못 배운다고 보기 쉽습니다. | 방향은 맞아도 update가 너무 커 목표를 지나쳤기 때문에 설정이 학습을 망친 경우입니다. |

초기 신경망 학습에서는 가장 단순한 경사하강법(gradient descent)이나 확률적 경사하강법(stochastic gradient descent)이 기본 출발점이었습니다. 하지만 네트워크가 깊어지고 데이터가 커지면서, 학습 속도와 안정성을 개선하려는 다양한 시도가 이어졌습니다.

이 흐름 때문에 modern deep learning 커리큘럼에서는 optimizer를 단순한 구현 옵션이 아니라, `학습 동역학(training dynamics)`의 핵심 요소로 다룹니다.

독자 기준에서 이 절이 필요한 이유도 분명합니다.

- 손실 함수와 역전파만 배우면 학습이 이미 끝난 것처럼 느껴질 수 있고
- 실제 파라미터 업데이트를 누가 담당하는지 흐려질 수 있으며
- 뒤에서 SGD와 Adam을 비교할 때 무엇이 달라지는지 기준이 없어지기 때문입니다

즉, 이 절은 `gradient 계산`과 `업데이트 전략`을 분리해 읽게 만드는 기준 절입니다.

## 언제 optimizer 관점으로 먼저 읽는가

이 절을 꺼내야 하는 시점은 `gradient를 계산했다`는 설명만으로는 아직 파라미터가 실제로 어떻게 움직이는지 닫히지 않을 때입니다.

| 먼저 보이는 문제 장면 | optimizer 관점이 먼저 유용한 이유 | 바로 다음에 넘길 질문 |
| --- | --- | --- |
| gradient는 알겠는데 실제 이동 폭과 규칙이 안 보인다 | update를 별도 규칙으로 읽게 해 줍니다. | 어떤 대표 optimizer들이 이 규칙을 다르게 구현하는지 봐야 합니다. |
| 손실, 역전파, 업데이트가 한 묶음으로 섞여 보인다 | `틀림 -> gradient -> 실제 수정`의 역할 차이를 분명히 할 수 있습니다. | SGD와 Adam 비교로 넘어가야 합니다. |
| 학습이 느리거나 흔들리는데 원인이 불분명하다 | learning rate와 update rule이 별도 변수라는 점을 드러낼 수 있습니다. | regularization과 optimizer의 역할 차이도 뒤에서 봐야 합니다. |
| 같은 gradient여도 결과가 다를 수 있다는 점이 직관적이지 않다 | optimizer가 학습 동역학 자체를 바꾼다는 점을 고정할 수 있습니다. | 대표 optimizer 비교 절에서 그 차이를 구체화해야 합니다. |

## 체크리스트

- 옵티마이저(optimizer)가 역전파 결과를 실제 파라미터 업데이트로 바꾼다는 점을 설명할 수 있는가?
- 손실, 역전파, 학습률, 옵티마이저의 관계를 말할 수 있는가?
- 손실 함수, 역전파, optimizer는 각각 역할이 다르다는 점을 구분할 수 있는가?
- learning rate가 optimizer update 보폭에 붙는 하이퍼파라미터라는 점을 설명할 수 있는가?
- 왜 gradient를 계산했다고 해서 학습 전략 설명이 끝난 것이 아니라, update 규칙이 따로 더 필요하다고 말할 수 있는가?
- gradient는 이해했는데 실제 파라미터가 어떻게 움직이는지 설명이 비어 있을 때, optimizer 관점을 먼저 떠올릴 수 있는가?
- 이 절 다음에는 SGD와 Adam 같은 대표 update 규칙 비교로 넘어간다는 흐름을 알고 있는가?

## 출처와 참고 자료

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Léon Bottou, `Large-Scale Machine Learning with Stochastic Gradient Descent`, COMPSTAT, 2010, 확인 날짜: 2026-06-29.
- Sebastian Ruder, `An overview of gradient descent optimization algorithms`, arXiv, 2016, 확인 날짜: 2026-06-29.

# P5-7.1 옵티마이저(optimizer)의 역할

Section ID: `P5-7.1`
Version: `v2026.07.17`

P5-6장에서는 학습 루프, step/batch/epoch, 학습(learning)과 모델 실행(inference), 그리고 학습 모드(training mode)와 평가 모드(evaluation mode)를 구분했습니다. 여기까지 오면 이제 아주 직접적인 질문이 남습니다.

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
- 손실 함수, 역전파, 옵티마이저는 어떤 역할 차이를 가지는가?
- 왜 `좋은 gradient`만으로는 충분하지 않고 `업데이트 규칙`이 따로 필요한가?
- optimizer를 단순한 구현 함수가 아니라 파라미터를 실제로 바꾸는 역할로 읽으려면 무엇을 보아야 하는가?

이 절에서는 `누가 파라미터를 실제로 바꾸는가`를 닫는 데 집중합니다. 즉, 여기서는 gradient를 계산하는 단계와 gradient를 실제 update로 바꾸는 단계를 분리해 읽는 기준을 먼저 세웁니다.

대신 이번 절에서 바로 넓히지 않을 질문도 분명합니다. 같은 gradient라도 learning rate에 따라 update 보폭이 어떻게 달라지는지는 다음 Section인 P5-7.2에서 이어서 설명합니다. Adam 같은 적응형 optimizer가 단순 기준 update에 무엇을 더 보완하려 하는지는 P5-7.3에서 다시 설명합니다. adaptive optimization의 수렴 분석은 P5-7.4 보충학습으로 분리합니다.

## 이 절의 목표

- 옵티마이저를 `gradient를 실제 업데이트로 바꾸는 규칙`으로 설명할 수 있습니다.
- 손실 함수, 역전파, 옵티마이저의 역할을 구분할 수 있습니다.
- `gradient를 계산했다`와 `파라미터가 실제로 바뀌었다`가 같은 말이 아니라는 점을 말할 수 있습니다.
- 작은 Python 예제로 gradient와 update의 차이를 확인할 수 있습니다.

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
- 그래서 같은 gradient라도 optimizer 규칙이 다르면 실제 학습 모습이 달라질 수 있습니다.

## 옵티마이저는 무엇을 update로 만든다고 읽어야 하는가

초심자에게 자주 생기는 오해는 `gradient를 계산했다`는 말과 `모델이 이미 바뀌었다`는 말을 같은 뜻으로 읽는 것입니다. 하지만 실제로는 단계가 하나 더 있습니다.

1. 현재 파라미터에서 gradient를 계산합니다.
2. optimizer가 그 gradient를 보고 update 값을 만듭니다.
3. 파라미터에 그 update를 반영합니다.

즉, gradient는 아직 `바뀌어야 할 방향과 크기에 대한 신호`이고, update는 `실제로 파라미터에 적용되는 이동량`입니다.

이 차이를 구분하지 않으면, 학습이 느릴 때 무엇이 병목인지 읽기 어려워집니다. gradient 계산은 잘 됐는데 update가 지나치게 보수적일 수도 있고, 반대로 방향은 맞지만 update가 과격할 수도 있기 때문입니다. 이런 보폭 문제는 다음 절 P5-7.2에서 learning rate와 함께 더 직접적으로 읽습니다.

## 사례 및 예시

### 사례 1. 손실과 gradient는 계산됐지만 update는 아직 적용되지 않은 경우

학습 코드를 읽다 보면 `loss.backward()`까지는 실행됐는데, 아직 `optimizer.step()`이 호출되지 않은 지점을 만날 수 있습니다. 사람은 이 장면을 보면 이미 학습이 끝났다고 느끼기 쉽지만, 실제로는 파라미터가 아직 바뀌지 않았을 수 있습니다.

이 장면에서 optimizer 관점은 질문을 바꿉니다. `gradient가 계산됐는가`에서 멈추지 않고, `그 gradient가 실제 update로 적용됐는가`를 확인합니다. 손실과 gradient는 계산 결과이고, optimizer step은 그 계산 결과를 모델 내부 숫자 변화로 바꾸는 마지막 절차입니다.

그래서 이 사례에서 확인해야 할 결과는 `backward를 했다`가 아니라, `optimizer step까지 가서 파라미터가 실제로 달라졌는가`입니다.

| 사람이 먼저 보기 쉬운 기준 | optimizer 관점으로 다시 읽는 기준 |
| --- | --- |
| gradient까지 구했으니 학습이 이미 끝났다고 느끼기 쉽다 | gradient 계산과 update 적용은 별도 단계다 |
| loss가 찍혔으니 모델도 바로 더 좋아졌다고 생각하기 쉽다 | loss는 상태를 보여 주는 숫자이고, 실제 파라미터 변화는 optimizer가 만든다 |
| backward만 보면 충분하다고 느끼기 쉽다 | 파라미터가 바뀌려면 optimizer step이 실제로 실행돼야 한다 |

### 사례 2. 같은 gradient라도 update 규칙이 학습 동역학을 바꾸는 경우

두 실험이 같은 gradient 방향을 얻었다고 해 보겠습니다. 사람은 여기서 `방향이 같으니 결과도 비슷하겠지`라고 생각하기 쉽습니다. 하지만 실제로는 update를 만드는 규칙이 다르면 파라미터 경로가 달라질 수 있습니다.

이 절에서는 그 차이를 길게 비교하지 않고, `gradient 계산`과 `실제 수정`을 분리하는 기준만 먼저 남깁니다. 즉, optimizer를 단순한 부속 함수가 아니라 `학습 동역학을 실제로 만드는 마지막 규칙`으로 읽어야 한다는 점이 중요합니다. 구체적으로 같은 gradient가 learning rate에 따라 어떻게 다른 보폭으로 바뀌는지는 P5-7.2에서, Adam류가 최근 흐름과 좌표별 차이를 어떻게 더 반영하는지는 P5-7.3에서 이어집니다.

두 사례를 한 번에 다시 압축하면, optimizer의 역할을 읽는 첫 흐름은 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-07/optimizer-step-bridge-ko.mmd"
```

이 도식은 사례를 다시 설명하려는 것이 아니라, `gradient 계산`과 `실제 update 적용`을 한 번에 다시 분리해 붙잡기 위한 것입니다.

## 연습 및 예제

이번 예제의 목표는 gradient 계산과 실제 update 적용을 분리해서 보는 것입니다. 여기서는 learning rate의 크기 비교보다, `gradient를 구한 뒤 optimizer가 update를 만들고, 그 다음에야 파라미터가 바뀐다`는 순서를 확인합니다.

입력:

- 현재 위험 가중치 `risk_weight`
- 압력 미복귀 정도 `pressure_unrecovered`
- 목표 차단 점수 `target_block_score`
- 고정된 학습률 `learning_rate`

출력:

- 예측된 차단 점수
- 손실
- gradient
- optimizer가 만든 update 값
- 업데이트 전후 위험 가중치와 손실

문제 상황:

- gradient를 계산했다고 해서 파라미터가 자동으로 바뀌는 것은 아니다
- optimizer가 만든 update가 실제로 적용돼야 모델 내부 숫자가 변한다

확인할 개념:

- gradient는 방향 신호다
- optimizer는 그 신호를 update 값으로 바꾼다
- 파라미터 변화는 update 적용 뒤에야 생긴다

```python
pressure_unrecovered = 2.0
target_block_score = 6.0
risk_weight_before = 1.0
learning_rate = 0.1

predicted_block_score_before = pressure_unrecovered * risk_weight_before
loss_before = (predicted_block_score_before - target_block_score) ** 2
gradient_risk_weight = 2 * (predicted_block_score_before - target_block_score) * pressure_unrecovered

optimizer_delta = -learning_rate * gradient_risk_weight
risk_weight_after = risk_weight_before + optimizer_delta
predicted_block_score_after = pressure_unrecovered * risk_weight_after
loss_after = (predicted_block_score_after - target_block_score) ** 2

print("predicted_block_score_before =", round(predicted_block_score_before, 3))
print("loss_before =", round(loss_before, 3))
print("gradient_risk_weight =", round(gradient_risk_weight, 3))
print("optimizer_delta =", round(optimizer_delta, 3))
print("risk_weight_after =", round(risk_weight_after, 3))
print("predicted_block_score_after =", round(predicted_block_score_after, 3))
print("loss_after =", round(loss_after, 3))
```

```text
predicted_block_score_before = 2.0
loss_before = 16.0
gradient_risk_weight = -16.0
optimizer_delta = 1.6
risk_weight_after = 2.6
predicted_block_score_after = 5.2
loss_after = 0.64
```

이 출력에서는 `loss_before`, `gradient_risk_weight`를 먼저 보고, 그 다음 `optimizer_delta`가 별도 값으로 만들어진다는 점을 확인하면 됩니다. 마지막으로 `risk_weight_after`와 `loss_after`를 보면, 실제 파라미터 변화와 손실 변화가 update 적용 뒤에야 나타난다는 점이 보입니다.

즉, 이 예제에서 독자가 꼭 읽어야 할 것은 다음입니다.

- `gradient_risk_weight`는 아직 파라미터 자체가 아닙니다.
- `optimizer_delta`는 gradient를 실제 이동량으로 바꾼 값입니다.
- 파라미터 변화는 `risk_weight_after`에서 비로소 보입니다.
- 따라서 `gradient를 구했다`와 `모델을 실제로 업데이트했다`는 같은 말이 아닙니다.

같은 gradient라도 update 보폭을 어떻게 정하느냐에 따라 결과가 더 달라지는지는 다음 절 P5-7.2에서 이어집니다.

## 언제 optimizer 관점으로 먼저 읽는가

이 절을 꺼내야 하는 시점은 `gradient를 계산했다`는 설명만으로는 아직 파라미터가 실제로 어떻게 움직이는지 닫히지 않을 때입니다.

| 먼저 보이는 문제 장면 | optimizer 관점이 먼저 유용한 이유 | 바로 다음에 넘길 질문 |
| --- | --- | --- |
| gradient는 알겠는데 실제 이동 폭과 규칙이 안 보인다 | update를 별도 규칙으로 읽게 해 줍니다. | 같은 gradient라도 learning rate가 보폭을 어떻게 바꾸는지 봐야 합니다. |
| 손실, 역전파, 업데이트가 한 묶음으로 섞여 보인다 | `틀림 -> gradient -> 실제 수정`의 역할 차이를 분명히 할 수 있습니다. | update 보폭과 적응형 보정은 뒤 절에서 봐야 합니다. |
| 같은 gradient여도 결과가 다를 수 있다는 점이 직관적이지 않다 | optimizer가 학습 동역학 자체를 바꾼다는 점을 고정할 수 있습니다. | P5-7.2, P5-7.3에서 보폭과 적응형 update 차이를 봐야 합니다. |

## 체크리스트

- 옵티마이저(optimizer)가 역전파 결과를 실제 파라미터 업데이트로 바꾼다는 점을 설명할 수 있는가?
- 손실, 역전파, 옵티마이저의 역할 차이를 말할 수 있는가?
- `gradient를 계산했다`와 `파라미터가 실제로 바뀌었다`를 구분할 수 있는가?
- optimizer가 만든 update 값이 적용된 뒤에야 파라미터와 손실이 바뀐다는 점을 설명할 수 있는가?
- 다음 절 P5-7.2에서 learning rate가 update 보폭을 어떻게 바꾸는지, P5-7.3에서 Adam류가 무엇을 더 보완하는지 이어진다는 흐름을 알고 있는가?

## 출처와 참고 자료

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Léon Bottou, `Large-Scale Machine Learning with Stochastic Gradient Descent`, COMPSTAT, 2010, 확인 날짜: 2026-06-29.
- Sebastian Ruder, `An overview of gradient descent optimization algorithms`, arXiv, 2016, 확인 날짜: 2026-06-29.

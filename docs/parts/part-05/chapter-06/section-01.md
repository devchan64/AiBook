# P5-6.1 학습 루프의 네 단계

> Section ID: `P5-6.1`
> Version: `v2026.07.26`

P5-5장에서는 손실(loss), 역전파(backpropagation), 계산 그래프(computation graph)를 통해 딥러닝 모델이 어떻게 gradient를 계산하는지 보았습니다. 여기까지 오면 다음 질문이 자연스럽게 남습니다.

gradient까지 계산했다면, 실제 학습 과정에서는 어떤 순서로 모델이 바뀌는가?

딥러닝 학습 루프의 핵심 4단계는 `forward -> loss -> backward -> optimizer step`이다. 먼저 이 4단계를 한 번의 공통 반복으로 붙잡는 편이 안전하다.

학습 루프 안에서 손실, 역전파, 업데이트, 모드 전환의 자리가 다시 섞이면 개념사전의 [학습(training)](../../../reference/concept-glossary-parts/14-hieut.md#training), [역전파(backpropagation)](../../../reference/concept-glossary-parts/08-ieung.md#backpropagation), [옵티마이저(optimizer)](../../../reference/concept-glossary-parts/08-ieung.md#optimizer) 항목을 함께 다시 봅니다.

## 학습 루프가 한 바퀴 도는 질문

- 지금까지 본 손실과 역전파는 하나의 학습 루프에서 어떻게 이어지는가?
- optimizer step은 gradient 계산 뒤 어디에 붙는가?
- batch 반복은 이 4단계를 어떻게 실제 학습 절차로 묶는가?

여기서는 단일 학습 루프의 공통 골격만 먼저 잡습니다. gradient가 optimizer update로 이어지는 관점 자체는 앞선 P5-5.1, P5-5.2에서 본 흐름 위에 놓고, 이 절에서는 `forward -> loss -> backward -> optimizer step`과 batch 반복이 한 묶음으로 어떻게 읽히는지만 먼저 닫습니다.

대신 이번 절에서 바로 넓히지 않을 질문도 분명합니다. step, batch, epoch가 왜 필요한지는 다음 Section인 P5-6.2에서 이어서 설명하고, learning과 inference의 차이는 P5-6.3에서, training mode와 evaluation mode의 차이는 P5-6.4에서 다시 설명합니다. 즉, 이번 절은 `학습 루프의 순서`를 붙잡는 자리이고, 바로 다음 절들은 `그 루프가 어떤 단위로 반복되고 언제 어떤 방식으로 실행되는가`를 구분하는 자리입니다.

## forward-loss-backward-step 판단 기준

- 딥러닝 학습 루프를 한 번에 설명할 수 있습니다.
- forward, loss, backward, optimizer step의 순서를 말할 수 있습니다.
- batch 반복이 왜 `핵심 4단계`와 함께 읽혀야 하는지 설명할 수 있습니다.
- 뒤 장의 구조 설명을 `학습 가능한 구조` 관점에서 읽을 수 있습니다.

## 가장 작은 학습 루프

딥러닝 모델을 학습시킬 때는 보통 다음 순서가 반복됩니다.

1. 입력을 넣고 출력값을 계산한다.
2. 출력과 정답 차이를 손실로 계산한다.
3. 손실이 각 가중치에 미친 영향을 뒤로 전달한다.
4. 옵티마이저가 그 영향을 바탕으로 가중치를 갱신한다.
5. 이 과정을 여러 배치(batch)에 대해 반복한다.

이 다섯 단계가 Part 5 초반부에서 따로 보았던 내용을 실제로 연결하는 가장 작은 골격입니다.

여기서 용어 층위를 한 번 분리해 두면 더 덜 헷갈립니다.

| 구분 | 이 절에서 먼저 잡을 것 |
| --- | --- |
| 핵심 계산 단계 | `forward -> loss -> backward -> optimizer step` |
| 반복 단위 | 이 4단계를 batch마다 다시 수행한다는 점 |

즉, `forward`, `loss`, `backward`, `optimizer step`은 한 번의 학습 step 안에서 직접 이어지는 계산 단계 이름이고, `batch`는 그 4단계가 실제 학습에서 어떻게 반복되는지를 보여 주는 운영 단위입니다.

하지만 초심자 기준에서는 영어 이름만 나열해 두면 여전히 한눈에 들어오지 않을 수 있습니다. 이 책에서는 각 단계를 다음처럼 풀어 읽는 편이 더 안전합니다.

| 단계 이름 | 이 책에서 먼저 붙잡을 기준 표현 | 지금 이 절에서의 뜻 |
| --- | --- | --- |
| forward | 입력을 넣고 현재 모델 출력값을 계산하는 단계 | `지금 파라미터로 예측을 만든다` |
| loss | 출력과 목표의 차이를 숫자로 요약하는 단계 | `얼마나 어긋났는지 점수화한다` |
| backward | 그 차이가 각 파라미터에 어떻게 책임으로 되돌아가는지 계산하는 단계 | `어디를 어떤 방향으로 고쳐야 하는지 gradient를 계산한다` |
| optimizer step | 계산된 gradient를 바탕으로 파라미터를 실제로 바꾸는 단계 | `모델 내부 숫자를 한 번 갱신한다` |

이 연결이 필요한 이유는 네 단계가 모두 `계산`처럼 보이지만, 책 안에서 맡는 역할은 조금씩 다르기 때문입니다. `forward`는 결과를 만드는 계산이고, `loss`는 그 결과를 평가하는 계산이며, `backward`는 책임을 되돌리는 계산이고, `optimizer step`은 모델을 실제로 바꾸는 계산입니다. 같은 루프 안에 있어도 `출력 만들기`, `오차 읽기`, `책임 되돌리기`, `값 갱신하기`라는 서로 다른 역할로 읽어야 전체 학습 흐름이 덜 섞입니다.

따라서 이 절에서는 영어 이름 자체를 외우는 것보다, 다음 한 문장으로 먼저 잡는 편이 좋습니다.

`학습 루프는 예측을 만들고, 오차를 읽고, 책임을 되돌리고, 모델 값을 한 번 바꾸는 반복이다.`

## 이 절에서 먼저 고정할 경계

P5-6.1에서는 먼저 `예측 만들기 -> 오차 점수화 -> 책임 되돌리기 -> 값 갱신`이라는 핵심 4단계만 고정합니다. step, batch, epoch의 반복 단위는 P5-6.2에서, learning과 inference의 차이는 P5-6.3에서, training mode와 evaluation mode의 차이는 P5-6.4에서 다시 읽습니다. regularization도 뒤 장에서 다시 연결합니다.

즉, 이 절의 역할은 `학습 루프의 뼈대`를 먼저 붙잡는 데 있습니다. 여기서 다른 기법 이름까지 넓히기보다, 어떤 구조가 오더라도 공통으로 남는 반복 순서를 먼저 고정하는 편이 더 안전합니다.

## 아주 단순하게 그리면

```mermaid
--8<-- "assets/part-05/chapter-06/training-loop-regularization-flow-ko.mmd"
```

이 도식의 핵심은 `핵심 계산 4단계`가 batch마다 반복된다는 가장 작은 학습 뼈대를 먼저 보이는 데 있습니다.

여기서 한 번 더 짚어 둘 기준은 `한 번의 학습 step 안에서 바로 이어지는 것`과 `그 step이 여러 번 반복되는 것`을 섞지 않는 일입니다.

| 질문 | 먼저 떠올릴 답 |
| --- | --- |
| 한 번의 step 안에서 바로 이어지는 순서는 무엇인가? | `forward -> loss -> backward -> optimizer step` |
| 이 순서를 여러 번 반복하게 만드는 운영 단위는 무엇인가? | batch |
| 실제로 모델 값이 바뀌는 시점은 언제인가? | `optimizer step`에서 한 번 바뀐다 |

이 세 문장을 분리해 기억하면, `loss를 구했다`, `gradient를 계산했다`, `배치를 돌렸다` 같은 표현이 한 문단 안에 함께 나와도 무엇이 계산 단계이고 무엇이 반복 단위인지 덜 헷갈립니다.

## 사례 및 예시

### 사례 1. 이미지 분류 학습

이미지를 넣고 분류 점수를 계산한 뒤 손실을 구하고, 역전파와 optimizer step으로 가중치를 갱신하는 흐름은 CNN에서도 그대로 유지됩니다. 사람은 CNN처럼 구조가 바뀌면 학습 방식도 완전히 새로 바뀐다고 느끼기 쉽습니다. 하지만 실제로 사람이 먼저 보던 기준이 `새 구조 이름이 붙었는가`였다면, 더 중요한 기준은 `그 구조가 forward 안에 어떤 계산 블록으로 들어가고 backward와 update는 그대로 이어지는가`입니다. 즉, 바뀌는 것은 합성곱 같은 내부 계산 블록이지 `forward -> loss -> backward -> update`라는 뼈대 자체는 아닙니다. 그래서 이 사례에서 확인해야 할 결과는 CNN이라는 이름을 외우는 것보다, 합성곱이 들어가도 학습 루프의 공통 골격은 유지된다는 점을 설명할 수 있는가입니다.

```mermaid
flowchart TD
    A[문제 장면: 이미지 분류 모델을 학습한다] --> B[사람이 먼저 보기 쉬운 기준: CNN이니 학습 절차도 새로 배워야 하나?]
    B --> C[한계: 구조 이름에만 주목하면 공통 학습 루프를 놓치기 쉽다]
    C --> D[개념이 바꾸는 기준: 합성곱은 forward 안의 계산 블록이다]
    D --> E[공통 골격 확인: loss -> backward -> optimizer step은 그대로 이어진다]
    E --> F[다음 확인: 구조가 달라도 학습 루프 뼈대는 유지된다]
```

### 사례 2. 문장 분류 학습

입력을 텍스트로 바꾸고 구조를 RNN이나 Transformer로 바꿔도, 손실 계산과 backward, optimizer step이라는 루프는 그대로 남습니다. 사람은 텍스트 모델이 되면 완전히 다른 절차를 쓸 것처럼 느끼기 쉽습니다. 하지만 사람이 하던 단순 구분이 `이미지 모델`과 `텍스트 모델`처럼 입력 종류만 나누는 수준에 머물면, 토큰 길이, 임베딩, attention이 붙어도 공통으로 남는 학습 골격을 놓치기 쉽습니다. 실제로 바뀌는 것은 입력 구조와 내부 계산이고, 한 배치를 forward로 통과시키고 손실을 계산한 뒤 gradient를 되돌려 업데이트한다는 흐름은 같습니다. 그래서 이 사례에서 확인해야 할 결과는 모델 종류가 달라져도 `어디가 입력 표현 변화이고 어디가 공통 학습 단계인가`를 나눠 읽을 수 있는가입니다.

```mermaid
flowchart TD
    A[문제 장면: 문장 분류 모델을 학습한다] --> B[사람이 먼저 보기 쉬운 기준: 텍스트 모델은 절차도 완전히 다를까?]
    B --> C[한계: 입력 종류만 보면 공통 학습 단계가 흐려진다]
    C --> D[개념이 바꾸는 기준: 토큰과 attention은 forward 안의 입력 표현과 계산 구조다]
    D --> E[공통 골격 확인: batch forward -> loss -> backward -> optimizer step]
    E --> F[다음 확인: 바뀌는 것은 입력과 내부 계산이지 학습 루프 자체가 아니다]
```

### 사례 3. 구조 변화와 공통 루프를 함께 읽기
| 사람이 먼저 보기 쉬운 기준 | 학습 루프 관점으로 다시 읽는 기준 |
| --- | --- |
| CNN, RNN, Transformer처럼 새 구조 이름이 붙으면 학습 절차도 완전히 바뀐다고 느끼기 쉽다 | 바뀌는 것은 내부 계산 블록이고, `forward -> loss -> backward -> optimizer step`이라는 공통 반복은 그대로 남는다 |
| 이미지 모델과 텍스트 모델은 학습 방식도 완전히 다를 것처럼 느끼기 쉽다 | 입력 표현과 내부 구조는 달라도 batch 단위 forward, loss, backward, update라는 뼈대는 공통으로 유지된다 |

이 사례들에서 최종적으로 확인해야 할 결과는 분명합니다. 학습 루프의 핵심은 `새 구조 이름을 많이 아는가`가 아니라, 어떤 구조가 오더라도 공통 반복은 유지되고, 그 반복 안에서 `예측 -> 오차 -> gradient -> update`가 어떻게 이어지는지를 설명할 수 있는가에 있습니다.

## 연습 및 예제

이번 예제의 목표는 실제 딥러닝 프레임워크를 다루는 것이 아니라, 학습 루프 안에서 `forward -> loss -> backward -> optimizer step`이 어떻게 한 운영 배치(batch)씩 반복되는지 확인하는 것입니다.

입력:

- 경보 수치를 두 개씩 묶은 batch 2개
- 각 batch의 목표 차단 점수
- 위험 가중치 하나 `risk_weight`

출력:

- batch별 예측 차단 점수 목록
- batch별 평균 loss
- batch별 평균 gradient
- step 이후 갱신된 위험 가중치

문제 상황:

- 배치 학습은 샘플 하나가 아니라 묶음 단위로 gradient를 계산하므로, batch별 평균 손실과 평균 gradient를 같이 보는 것이 중요하다

확인할 개념:

- 배치 단위 gradient는 여러 샘플의 오차를 모아 계산한 결과다
- 샘플별 계산을 평균한 뒤 한 번 업데이트하는 구조가 학습 루프의 기본 형태다

입력(input):

각 batch는 `alarm_count` 두 건과 그에 대응하는 `target_block_score` 두 건을 담고 있다고 가정합니다. 학습 루프는 현재 `risk_weight`로 batch 안 모든 예측 차단 점수를 먼저 계산한 뒤, 평균 손실과 평균 gradient를 모아 한 번만 업데이트합니다.

코드를 보기 전에 먼저 각 batch에서 무엇이 먼저 계산되고, 무엇이 마지막에 한 번만 바뀌는지 예상해 보면 학습 루프의 순서가 더 잘 고정됩니다.

| 비교 항목 | 먼저 예상해 볼 출력 | 예상 이유 |
| --- | --- | --- |
| `predictions` | 각 batch 안의 샘플마다 먼저 계산될 가능성이 큼 | forward 단계에서는 현재 `risk_weight`로 각 입력의 예측 차단 점수를 먼저 만듭니다. |
| `batch_loss`, `batch_gradient` | 샘플별 계산 뒤 평균으로 한 번 모일 가능성이 큼 | 손실과 gradient는 batch 안 여러 샘플 결과를 묶어 읽어야 하기 때문입니다. |
| `updated_risk_weight` | batch마다 한 번씩만 바뀔 가능성이 큼 | optimizer step은 샘플별로 즉시 바꾸지 않고 batch 평균 gradient 뒤에 한 번 적용됩니다. |
| 두 번째 batch의 `predictions` | 첫 번째 batch에서 갱신된 `risk_weight` 영향을 받을 가능성이 큼 | 학습 루프는 이전 update 결과를 다음 batch forward가 이어받는 반복 구조이기 때문입니다. |

이 표의 목적은 정확한 수치를 미리 외우는 데 있지 않습니다. 학습 루프를 읽을 때 `무엇이 샘플별 forward 결과인가`, `무엇이 batch 평균으로 모이는가`, `무엇이 step 끝에서 한 번 바뀌는가`를 코드 전에 붙잡는 데 있습니다.

```python
# batch 안의 샘플별 예측과 gradient를 평균한 뒤 risk_weight를 한 번 업데이트하는 학습 루프 예제입니다.
batches = [
    [
        {"alarm_count": 1.0, "target_block_score": 2.0},
        {"alarm_count": 2.0, "target_block_score": 4.0},
    ],
    [
        {"alarm_count": 3.0, "target_block_score": 6.0},
        {"alarm_count": 4.0, "target_block_score": 8.0},
    ],
]

risk_weight = 0.5
learning_rate = 0.1

for step, batch in enumerate(batches, start=1):
    predictions = []
    losses = []
    gradients = []

    for sample in batch:
        alarm_count = sample["alarm_count"]
        target_block_score = sample["target_block_score"]

        prediction = risk_weight * alarm_count
        loss = (prediction - target_block_score) ** 2
        gradient_risk_weight = 2 * (prediction - target_block_score) * alarm_count

        predictions.append(round(prediction, 3))
        losses.append(loss)
        gradients.append(gradient_risk_weight)

    batch_loss = sum(losses) / len(losses)
    batch_gradient = sum(gradients) / len(gradients)

    risk_weight = risk_weight - learning_rate * batch_gradient

    print(f"[batch {step}]")
    print("predictions =", predictions)
    print("batch_loss =", round(batch_loss, 3))
    print("batch_gradient =", round(batch_gradient, 3))
    print("updated_risk_weight =", round(risk_weight, 3))
    print("---")
```

출력에서는 각 batch마다 predictions가 먼저 계산되고, 그 뒤 평균 loss와 평균 gradient가 모인 다음 updated_risk_weight가 한 번 바뀌는 순서를 보면 됩니다.

```text
[batch 1]
predictions = [0.5, 1.0]
batch_loss = 5.625
batch_gradient = -7.5
updated_risk_weight = 1.25
---
[batch 2]
predictions = [3.75, 5.0]
batch_loss = 7.031
batch_gradient = -18.75
updated_risk_weight = 3.125
---
```

이 예제에서 핵심은 다음입니다.

- 딥러닝 학습은 한 번의 계산이 아니라 batch마다 반복되는 루프입니다
- 각 batch에서 forward, loss, backward, optimizer step이 같은 순서로 다시 등장합니다
- 구조 설명과 학습 설명은 이 루프 안에서 다시 만나야 합니다

이 흐름을 예제 산출물 기준으로 나누어 보면 먼저 forward 결과가 보입니다. 첫 번째 batch는 `risk_weight=0.5`로 예측하므로 목표보다 낮게 나오고, 두 번째 batch는 첫 업데이트 뒤 `risk_weight=1.25`가 반영된 상태에서 다시 예측됩니다.

![학습 루프 batch별 예측과 목표](../../../assets/part-05/chapter-06/training-loop-predictions-ko.png)

다음 산출물은 batch 평균 loss입니다. loss는 각 batch 안의 샘플별 오차를 평균으로 묶은 값이므로, optimizer가 바로 보는 것은 개별 샘플 하나가 아니라 batch가 만든 평균 신호입니다.

![학습 루프 batch별 평균 loss](../../../assets/part-05/chapter-06/training-loop-batch-loss-ko.png)

그다음 산출물은 batch 평균 gradient입니다. 두 값이 모두 음수라는 점은 현재 `risk_weight`가 목표보다 낮은 예측을 만들고 있어서, update가 `risk_weight`를 키우는 방향으로 이어진다는 뜻입니다.

![학습 루프 batch별 평균 gradient](../../../assets/part-05/chapter-06/training-loop-batch-gradient-ko.png)

마지막 산출물은 optimizer step 뒤의 `risk_weight`입니다. 이 그래프는 학습 루프가 출력값을 한 번 계산하고 끝나는 절차가 아니라, batch 평균 gradient를 통해 다음 batch의 forward 조건 자체를 바꾸는 반복 구조라는 점을 보여 줍니다.

![학습 루프 risk_weight 갱신](../../../assets/part-05/chapter-06/training-loop-risk-weight-update-ko.png)

이 예제를 한 번 더 짧게 접어 보면 batch 안쪽과 batch 바깥의 역할을 다음처럼 나눌 수 있습니다.

| 구간 | 실제로 일어나는 일 | 이 구간이 필요한 이유 |
| --- | --- | --- |
| batch 안쪽 | 각 샘플의 prediction, loss, gradient를 계산한다 | 샘플별 오차가 어디서 생기는지 먼저 모아야 하기 때문이다 |
| batch 끝 | 샘플별 loss와 gradient를 평균으로 묶는다 | 한 번의 update에 사용할 공통 신호를 만들기 때문이다 |
| step 끝 | `risk_weight`를 한 번 갱신한다 | 다음 batch forward가 이전 결과를 이어받게 하기 때문이다 |

즉, forward와 loss는 샘플별로 먼저 펼쳐지고, backward 결과는 batch 평균 신호로 모인 뒤, optimizer step에서 모델 값이 한 번 바뀝니다. 이 순서를 붙잡고 나면 학습 루프를 볼 때 `계산이 여러 번 일어나는 구간`과 `모델이 실제로 바뀌는 구간`을 구분해 읽을 수 있습니다.

여기서 바로 다음 Section으로 넘어가기 전에, `공통 학습 절차`와 `뒤에서 달라질 구조`를 짧게 다시 나누어 두면 읽기 축이 덜 섞입니다.

| 지금 절에서 고정할 것 | 뒤 구조 장에서 달라질 것 | 왜 지금 나눠 두는가 |
| --- | --- | --- |
| `forward -> loss -> backward -> optimizer step`이라는 공통 루프 | CNN의 지역 패턴 읽기, RNN의 순차 상태, attention의 선택적 참조, Transformer의 병렬 블록 | 뒤 장에서 새 이름이 나와도 `학습 절차가 바뀌는가`와 `내부 계산 구조가 바뀌는가`를 분리해 읽기 위해 |

## 언제 학습 루프를 다시 한 번에 묶어 읽는가

이 절을 꺼내야 하는 시점은 손실, 역전파, optimizer, mode, regularization을 각각 따로는 이해했지만 하나의 반복 구조로는 아직 잘 안 보일 때입니다.

| 먼저 보이는 문제 장면 | 학습 루프 요약이 먼저 유용한 이유 | 바로 다음에 이어질 곳 |
| --- | --- | --- |
| 개념은 알겠는데 순서가 자꾸 섞인다 | forward, loss, backward, update의 공통 골격을 다시 고정할 수 있습니다. | P5-6.2에서 step, batch, epoch 구분으로 이어집니다. |
| 구조 장으로 넘어가기 전에 공통 학습 뼈대를 다시 확인하고 싶다 | CNN, RNN, Transformer도 결국 같은 루프 안에서 학습된다는 점을 정리할 수 있습니다. | P5-6.2, P5-6.3, P5-6.4와 뒤 구조 장으로 이어집니다. |
| 문제 원인을 구조 탓으로만 돌리기 시작한다 | 학습 절차 문제와 내부 구조 문제를 분리하는 기준선을 다시 세울 수 있습니다. | 뒤 장의 구조 비교와 디버깅 읽기로 이어집니다. |

## 체크리스트

- `forward -> loss -> backward -> optimizer step` 학습 루프를 한 번에 설명할 수 있는가?
- 딥러닝 학습 루프는 forward, loss, backward, optimizer step의 반복이라는 점을 설명할 수 있는가?
- 개념은 알겠는데 순서가 자꾸 섞일 때, forward -> loss -> backward -> update의 공통 학습 루프를 먼저 떠올릴 수 있는가?
- 뒤 장의 CNN, RNN, Transformer를 볼 때 `공통 학습 절차`와 `달라지는 내부 구조`를 분리해 읽어야 한다는 점을 말할 수 있는가?
- 이 절 다음에는 learning/inference 구분과 mode 차이를 뒤 절에서 다시 읽는 흐름을 알고 있는가?

## 출처와 참고 자료

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Aurélien Géron, `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow`, 3rd ed., O'Reilly, 2022, 확인 날짜: 2026-07-19. [https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/](https://www.oreilly.com/library/view/hands-on-machine-learning/9781098125967/){: target="_blank" rel="noopener noreferrer" }

# P5-6.1 학습(learning)과 모델 실행(inference)

Section ID: `P5-6.1`
Version: `v2026.07.12`

P5-5장에서는 손실(loss), 역전파(backpropagation), 계산 그래프(computation graph)를 통해 딥러닝 모델이 어떻게 gradient를 계산하는지 보았습니다. 여기까지 오면 다음 질문이 생깁니다.

gradient까지 계산했다면, 지금 이 모델은 학습 중인가, 아니면 그냥 사용 중인가?

이 질문은 매우 중요합니다. 독자는 모델이 언제나 같은 방식으로 작동한다고 생각하기 쉽지만, 딥러닝에서는 `파라미터를 바꾸는 단계`와 `이미 배운 파라미터를 사용하는 단계`를 분리해서 보는 것이 매우 중요합니다.

학습(learning)은 모델 파라미터를 바꾸는 단계이고, 모델 실행(inference)은 바꾸지 않고 현재 파라미터로 결과를 계산하는 단계이다.

학습과 모델 실행의 구분이 뒤 절에서 다시 흐려지면 개념사전의 [학습(training)](../../../reference/concept-glossary.md#training)과 [추론(inference)](../../../reference/concept-glossary.md#inference) 항목을 함께 다시 보는 편이 좋습니다.

## 이 절의 범위

- 학습과 모델 실행은 왜 구분해야 하는가?
- 딥러닝 문맥에서 학습 단계는 무엇을 포함하는가?
- 모델 실행 단계에서는 무엇이 달라지는가?
- 같은 모델이라도 학습 중과 사용 중에 읽는 관점이 왜 다른가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- dropout과 batch normalization의 내부 수식
- 배포 인프라(inference serving) 세부 구조
- mixed precision, quantization 같은 시스템 최적화

학습 모드와 평가 모드의 구체적 차이는 P5-6.2에서 이어서 다루고, dropout과 regularization의 큰 의미는 P5-8.1, P5-8.2에서 다시 연결합니다. mixed precision, quantization, 배포 인프라 세부 구조는 이 책의 현재 본편 범위 밖에 둡니다.

## 이 절의 목표

- 학습과 모델 실행을 `파라미터 변경 여부`로 구분할 수 있습니다.
- 학습이 순전파만이 아니라 손실 계산, 역전파, 업데이트까지 포함한다는 점을 설명할 수 있습니다.
- 모델 실행은 결과를 계산하지만 파라미터를 바꾸지 않는 단계라는 점을 말할 수 있습니다.
- 실행 가능한 Python 예제로 두 단계의 차이를 확인할 수 있습니다.

## 왜 이 구분이 중요한가

딥러닝 입문에서 흔한 오해는 다음과 같습니다.

- 데이터를 넣고 결과가 나오면 그게 곧 학습이다
- 모델이 한 번 결과를 냈으니 이미 배웠다
- 예측을 여러 번 하면 모델이 점점 더 좋아진다

하지만 실제로는 그렇지 않습니다.

모델이 좋아지려면 다음 단계가 필요합니다.

1. 현재 파라미터로 예측을 만듭니다
2. 정답과 비교해 손실을 계산합니다
3. gradient를 계산합니다
4. optimizer가 파라미터를 업데이트합니다

즉, 단순히 `결과를 낸다`는 사실만으로는 학습이 일어나지 않습니다.

`결과 계산은 inference에서도 할 수 있지만, learning은 그 결과를 이용해 모델 내부 숫자를 실제로 바꾸는 과정까지 포함한다.`

## 딥러닝에서 학습(learning)은 무엇을 포함하나

여기서는 딥러닝 문맥의 학습을 다음 네 단계 묶음으로 이해하면 충분합니다.

| 단계 | 역할 |
| --- | --- |
| 순전파(forward pass) | 현재 파라미터로 예측을 계산 |
| 손실 계산(loss computation) | 예측과 정답의 차이를 숫자로 계산 |
| 역전파(backpropagation) | 각 파라미터에 대한 gradient를 계산 |
| 업데이트(update) | optimizer가 파라미터를 실제로 바꿈 |

이 네 단계가 모두 있어야 `학습이 한 번 일어났다`고 말할 수 있습니다.

즉, 딥러닝에서 learning은 단순히 데이터를 많이 보는 일이 아니라, `손실을 기준으로 파라미터를 반복적으로 조정하는 일`입니다.

## 모델 실행(inference)은 무엇을 하는가

모델 실행(inference)은 현재 파라미터를 고정한 채 입력에 대한 결과를 계산하는 단계입니다.

예를 들어:

- 사용자가 사진을 올리면 분류 결과를 보여 줍니다
- 설비 점검 메모를 넣으면 위험 요약 결과를 돌려줍니다
- 문서 일부를 넣으면 다음 토큰을 생성합니다

이때 모델은 계산을 합니다. 하지만 그 계산이 곧바로 파라미터 업데이트를 뜻하지는 않습니다.

즉, inference는 `현재 알고 있는 것을 사용해 답을 만드는 단계`입니다.

`learning은 모델을 바꾸는 시간이고, inference는 바꾸지 않고 쓰는 시간이다.`

## 같은 순전파라도 의미가 다르다

여기서 중요한 점이 하나 더 있습니다. 학습과 실행 모두 순전파(forward pass)를 사용합니다. 그래서 독자는 둘이 비슷해 보일 수 있습니다.

하지만 목적이 다릅니다.

- 학습 중의 순전파: 손실 계산과 업데이트를 위한 중간 단계
- 실행 중의 순전파: 최종 결과를 내기 위한 계산

즉, `같은 계산처럼 보여도 왜 계산하는가`가 다릅니다.

이를 아주 단순하게 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-06/training-vs-inference-flow-ko.mmd"
```

이 도식에서 확인해야 할 결과는 같은 예측값이라도 학습 단계에서는 손실 계산과 업데이트로 이어지고, 실행 단계에서는 바로 사용자 결과로 이어진다는 점입니다.

- 학습에서는 예측 뒤에 `얼마나 틀렸는지`를 계산하고 파라미터를 바꾸는 단계가 붙습니다.
- 실행에서는 예측이 곧바로 사용자에게 보여 줄 결과나 다음 시스템 단계 입력이 됩니다.

## 왜 inference를 `추론`만으로 옮기면 혼동이 생기나

Part 1에서도 보았듯이 한국어 `추론`은 reasoning, inference, prediction을 한데 섞어 들리게 만들 수 있습니다. 딥러닝 문맥에서 inference는 보통 `학습된 모델을 실행해 출력값을 계산하는 단계`를 가리킵니다.

즉, 이 절에서 inference는 `깊은 사고`나 `논리 추론`보다 더 넓고 더 기계적인 의미를 가집니다.

- 입력을 넣고
- 현재 파라미터로 계산하고
- 출력을 만든다

이것이 기본 뜻입니다.

따라서 이 절에서는 `모델 실행(inference)`이라는 병기를 유지해 두는 편이 안전합니다.

## 사례 및 예시

### 사례 1. 경보 분류 모델

운영자가 새 설비 경보 로그 한 건을 넣어 `즉시 정지`, `현장 확인`, `기록만` 같은 분류 결과를 보는 장면을 떠올려 볼 수 있습니다. 사람은 화면에 판정 결과가 바로 나오면 모델이 그 로그를 보고 곧바로 더 배웠다고 느끼기 쉽습니다. 하지만 그 장면에서 실제로 일어나는 일은 현재 파라미터로 점수를 계산해 정지, 확인, 기록 같은 후속 정책으로 넘기는 inference입니다. 학습은 별도의 데이터셋에서 과거 경보 로그와 정답 라벨을 비교하고, 손실과 gradient를 계산해 파라미터를 조정하는 절차를 포함해야만 일어납니다. 여기서 바뀌는 점은 `새 경보를 본다`가 아니라 `파라미터를 실제로 수정하느냐`이고, 결과적으로 운영 화면에 보이는 즉시 판정과 모델 재학습은 같은 일이 아닙니다. 그래서 이 사례에서 확인해야 할 결과는 새 경보 판정 직후 출력은 바뀌어도, 모델 파라미터 자체는 그대로 유지되는가입니다.

| 사람이 먼저 보기 쉬운 기준 | learning/inference 관점으로 다시 읽는 기준 |
| --- | --- |
| 새 입력을 처리했으니 모델도 바로 더 배웠을 것 같다 | 출력 계산만 했고 파라미터 업데이트는 없을 수 있다 |
| 결과가 달라졌으니 모델 내부 숫자도 바뀌었을 것 같다 | 입력이 달라져 출력이 달라진 것과 파라미터 변경은 별개다 |
| 많이 쓰면 저절로 학습될 것 같다 | 손실, gradient, update 절차가 실제로 있어야 learning이다 |

### 사례 2. 검사 이미지 데모

검사 화면에 패널 사진 한 장을 올렸는데 바로 `scratch_detected`가 나온다고 해 보겠습니다. 사람은 결과가 즉시 바뀌는 화면을 보면 방금 올린 이미지를 보고 모델이 새로 적응했다고 생각하기 쉽습니다. 하지만 그 순간에는 현재 파라미터로 한 장의 이미지를 계산해 가장 가능성 높은 클래스를 반환할 뿐입니다. 학습이라면 수천 장 이상의 검사 이미지와 라벨을 기준으로 손실을 계산하고, 그 오차를 바탕으로 gradient와 optimizer가 작동해야 합니다. 즉, 데모 화면에서 확인되는 것은 `이 입력을 지금 어떻게 분류했는가`이지 `이 입력 덕분에 모델이 곧바로 더 좋아졌는가`가 아닙니다. 그래서 이 사례에서 확인해야 할 결과는 이미지 한 장을 넣는 즉시 분류 결과는 얻어도, 그 입력 하나만으로 학습 단계가 자동으로 시작되지는 않는가입니다.

### 사례 3. LLM 채팅

현장 지원 채팅에서 같은 재기동 질문을 조금 다르게 쓰면 안내 문장이 달라지는 장면이 자주 보입니다. 사람은 이 변화를 보고 대화 자체가 모델을 실시간으로 다시 학습시키는 것처럼 느끼기 쉽습니다. 하지만 일반적인 서비스 사용에서 일어나는 일은 대화 문맥이 달라져 다음 토큰 계산 경로가 바뀌는 inference입니다. 파라미터 업데이트가 실제로 일어나려면 대화 로그를 모으고, 정답 기준이나 선호 기준을 마련한 뒤, 별도 학습 파이프라인에서 다시 조정해야 합니다. 즉, 채팅창에서 보이는 변화는 `입력이 달라져 출력이 달라진 것`이지 `모델이 그 자리에서 새로 배운 것`이 아닙니다. 그래서 이 사례에서 확인해야 할 결과는 프롬프트 표현이 바뀌어 응답은 달라져도, 그 변화가 곧바로 실시간 파라미터 학습을 뜻하지는 않는가입니다.

세 사례를 나란히 놓고 보면, learning과 inference의 차이는 `결과가 나왔는가`가 아니라 `그 결과가 파라미터를 실제로 바꾸는 계산으로 이어졌는가`에 있습니다.

| 장면 | 사람이 먼저 보기 쉬운 결과 | learning/inference 관점에서 실제로 구분해야 할 것 | 파라미터가 바뀌는가 |
| --- | --- | --- | --- |
| 경보 분류 모델 | 새 경보 결과가 바로 나왔다 | 현재 파라미터로 점수를 계산했는지, 손실-업데이트까지 갔는지 | 보통 inference에서는 바뀌지 않음 |
| 검사 이미지 데모 | 이미지 한 장을 넣자 분류가 바로 나왔다 | 입력 처리와 학습 파이프라인을 분리해서 봐야 함 | 데모 한 장 처리만으로는 바뀌지 않음 |
| LLM 채팅 | 질문을 바꾸자 답이 달라졌다 | 문맥 변화에 따른 출력 변화와 실시간 재학습을 구분해야 함 | 일반 서비스 사용에서는 바뀌지 않음 |

이 표에서 독자가 먼저 붙잡아야 할 결과는, learning과 inference를 가르는 핵심이 `출력 변화 유무`가 아니라 `손실과 업데이트가 실제로 붙어 파라미터가 바뀌었는가`라는 점입니다.

세 사례를 한 번에 다시 압축하면, learning과 inference를 읽는 첫 흐름은 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-06/learning-inference-parameter-bridge-ko.mmd"
```

이 도식은 경보 로그, 검사 이미지, 현장 지원 채팅 사례를 따로 다시 설명하려는 것이 아니라, 세 사례가 공통으로 보여 준 `새 입력을 처리해 출력이 달라지는 것`과 `손실-업데이트가 붙어 파라미터가 바뀌는 것`을 한 번에 다시 구분하기 위한 것입니다.

## 연습 및 예제

이번 예제의 목표는 같은 작은 위험 점수 모델이 `학습 배치`를 볼 때는 위험 가중치를 바꾸고, `서비스 입력`을 볼 때는 그 가중치를 바꾸지 않는다는 점을 여러 step으로 확인하는 것입니다.

입력:

- 학습용 경보 샘플 3개
- 초기 위험 가중치 `risk_weight`
- 학습률 `learning_rate`

출력:

- step별 위험 점수 예측값, 손실, 위험 가중치 변화
- 학습 완료 뒤 inference 결과
- inference 전후 위험 가중치 비교
- 같은 위험 가중치로 여러 서비스 입력을 처리했을 때 출력만 달라지는지 확인

문제 상황:

- 학습과 추론은 같은 수식을 써도 목적이 다르므로, 가중치가 업데이트되는 구간과 고정된 구간을 나눠 볼 필요가 있다
- 서비스 입력이 여러 번 들어와도 update가 없으면 파라미터는 그대로인지 직접 봐야 한다

확인할 개념:

- 학습 단계에서는 손실을 줄이기 위해 가중치가 계속 바뀐다
- 추론 단계에서는 학습된 가중치를 고정한 채 결과만 계산한다
- 입력이 달라져 출력이 달라져도 파라미터가 바뀌었다는 뜻은 아니다

입력(input):

학습 배치에서는 `alarm_count`를 받아 `predicted_block_score`를 만들고, 목표값 `target_block_score`와 비교해 `risk_weight`를 갱신한다고 가정합니다. 이후 서비스 구간에서는 새 `alarm_count`가 들어와도 같은 `risk_weight`를 그대로 사용하는지만 확인합니다.

코드를 보기 전에 먼저 어느 구간에서만 `weight`가 바뀔지 예상해 보면 좋습니다.

| 구간 | 먼저 예상해 볼 비교 | 예상 이유 |
| --- | --- | --- |
| `train step 1~3` | `risk_weight_before`와 `risk_weight_after`가 달라질 가능성 | 손실과 gradient를 이용해 실제 업데이트를 수행하기 때문입니다. |
| `service alarm_count=4.0` | 출력은 계산되지만 `risk_weight`는 유지될 가능성 | inference는 현재 파라미터를 사용만 하기 때문입니다. |
| `service alarm_count=5.0` | 출력은 달라질 수 있어도 `risk_weight`는 여전히 같을 가능성 | 입력 변화와 파라미터 변화는 별개이기 때문입니다. |

이 표의 목적은 `출력 변화`와 `파라미터 변화`를 분리해서 읽는 것입니다.

```python
train_alarm_data = [
    {"alarm_count": 1.0, "target_block_score": 3.0},
    {"alarm_count": 2.0, "target_block_score": 6.0},
    {"alarm_count": 3.0, "target_block_score": 9.0},
]

risk_weight = 0.5
learning_rate = 0.1

def predict_block_score(alarm_count, risk_weight):
    return alarm_count * risk_weight

print("initial_risk_weight =", round(risk_weight, 3))

for step, sample in enumerate(train_alarm_data, start=1):
    alarm_count = sample["alarm_count"]
    target_block_score = sample["target_block_score"]
    prediction = predict_block_score(alarm_count, risk_weight)
    loss = (prediction - target_block_score) ** 2
    gradient_risk_weight = 2 * (prediction - target_block_score) * alarm_count
    new_risk_weight = risk_weight - learning_rate * gradient_risk_weight
    print(
        f"train step {step}: "
        f"alarm_count={alarm_count}, target_block_score={target_block_score}, "
        f"prediction={prediction:.3f}, loss={loss:.3f}, "
        f"risk_weight_before={risk_weight:.3f}, risk_weight_after={new_risk_weight:.3f}"
    )
    risk_weight = new_risk_weight

weight_before_inference = risk_weight
service_alarm_counts = [4.0, 5.0]
for alarm_count in service_alarm_counts:
    print(
        f"inference: alarm_count={alarm_count}, "
        f"prediction={predict_block_score(alarm_count, risk_weight):.3f}, "
        f"risk_weight_used={risk_weight:.3f}"
    )
print("weight_before_inference =", round(weight_before_inference, 3))
print("weight_after_inference =", round(risk_weight, 3))
```

출력에서는 학습 단계의 weight_before/after 변화와 inference 단계의 weight 불변을 먼저 비교하면 됩니다.

```text
initial_risk_weight = 0.5
train step 1: alarm_count=1.0, target_block_score=3.0, prediction=0.500, loss=6.250, risk_weight_before=0.500, risk_weight_after=1.000
train step 2: alarm_count=2.0, target_block_score=6.0, prediction=2.000, loss=16.000, risk_weight_before=1.000, risk_weight_after=2.600
train step 3: alarm_count=3.0, target_block_score=9.0, prediction=7.800, loss=1.440, risk_weight_before=2.600, risk_weight_after=3.320
weight_before_inference = 3.32
inference: alarm_count=4.0, prediction=13.280, risk_weight_used=3.320
inference: alarm_count=5.0, prediction=16.600, risk_weight_used=3.320
weight_after_inference = 3.32
```

여기서는 학습 step에서 `risk_weight`가 실제로 바뀌고, inference에서는 새 입력이 들어와도 같은 `risk_weight`가 유지된다는 점을 먼저 확인하면 됩니다.

- 학습 step에서는 `risk_weight_before`와 `risk_weight_after`가 다르므로 파라미터가 실제로 바뀝니다
- inference에서는 서로 다른 입력을 넣어도 `risk_weight_used`가 계속 같고, `weight_before_inference`와 `weight_after_inference`도 같습니다
- 즉, 서비스 입력을 많이 넣는다고 자동으로 재학습이 일어나는 것은 아닙니다

| 구간 | 지금 읽어야 할 핵심 |
| --- | --- |
| `train step 1~3` | 출력과 손실을 본 뒤 실제 update가 붙으므로 `risk_weight`가 계속 달라집니다. |
| `inference alarm_count=4.0` | 새 입력을 처리해도 현재 `risk_weight`를 그대로 사용합니다. |
| `inference alarm_count=5.0` | 출력은 달라지지만, 바뀐 것은 입력이지 파라미터가 아닙니다. |

이 결과를 `출력 변화`와 `파라미터 변화` 기준으로 다시 묶으면 차이가 더 또렷합니다.

| 실행 결과에서 보인 차이 | 결과만 보면 남기 쉬운 해석 | learning/inference 관점에서 다시 읽는 해석 |
| --- | --- | --- |
| `train step 1~3`에서 prediction이 계속 달라진다 | 그냥 경보 샘플을 여러 번 본 결과라고 느끼기 쉽다 | 손실과 update가 붙어 `risk_weight` 자체가 바뀌었기 때문이라고 읽는다 |
| `inference alarm_count=4.0`, `alarm_count=5.0`에서 prediction이 달라진다 | 출력이 달라졌으니 모델도 같이 변했다고 느끼기 쉽다 | 입력만 달라졌고 `risk_weight_used`는 그대로라고 읽는다 |
| `weight_before_inference`와 `weight_after_inference`가 같다 | 출력도 나왔으니 뭔가 학습이 있었을 수 있다고 느끼기 쉽다 | inference는 계산만 했고 파라미터는 고정됐다고 읽는다 |

이 표까지 읽고 나면, learning과 inference의 핵심이 `둘 다 forward를 쓴다`가 아니라 `언제 update가 실제로 붙는가`를 구분하는 일이라는 점이 더 분명해집니다.

전통적인 통계 모델과 머신러닝 교육에서도 `학습용 데이터(training data)`와 `예측 단계(prediction stage)`를 구분하는 관점은 오래전부터 중요했습니다. 딥러닝에서는 여기에 역전파, optimizer, 모드 전환 같은 요소가 더해지면서 이 구분이 더 중요해졌습니다.

커리큘럼 관점에서 이 절이 필요한 이유도 분명합니다. 바로 앞의 P5-5.1, P5-5.2에서 gradient가 어떻게 계산되는지 보았다면, 이제 `계산이 되었을 때 언제 실제 업데이트가 일어나고 언제 단순 실행만 하는가`를 구분해야 합니다.

- 역전파를 배운 직후에는 모든 계산이 곧 학습처럼 느껴질 수 있고
- 모델 실행은 단지 `forward만 하는 단순한 단계`처럼 과소평가되기 쉽고
- 뒤에서 나올 dropout, batch normalization, evaluation mode를 이해하려면 먼저 `언제 업데이트가 일어나고 언제 안 일어나는가`를 분명히 알아야 합니다

즉, 이 절은 딥러닝 학습 절차를 운영 관점으로 읽기 시작하는 첫 절입니다.

## 언제 learning과 inference를 먼저 분리해서 읽는가

이 절을 꺼내야 하는 시점은 `모델이 결과를 낸다`는 설명만으로는 파라미터가 실제로 언제 바뀌는지, 언제 고정되는지가 흐려질 때입니다.

| 먼저 보이는 문제 장면 | learning/inference 구분이 먼저 유용한 이유 | 바로 다음에 넘길 질문 |
| --- | --- | --- |
| 결과가 나오면 곧바로 학습이 일어났다고 느껴진다 | 파라미터 변경 여부를 기준으로 학습과 실행을 분명히 가를 수 있습니다. | 같은 모델인데도 모드가 왜 달라지는지 봐야 합니다. |
| 순전파만 보이고 손실·역전파·업데이트가 하나로 섞여 있다 | learning이 update까지 포함하는 절차라는 점을 닫을 수 있습니다. | training/eval mode에서 계산 규칙이 어떻게 달라지는지 이어서 봐야 합니다. |
| 채팅, 분류 데모, 서비스 응답이 실시간 재학습처럼 보인다 | inference는 현재 파라미터를 사용하는 단계라는 점을 분명히 할 수 있습니다. | optimizer가 실제 업데이트를 언제 맡는지 뒤 장에서 봐야 합니다. |
| 학습 데이터 처리와 사용자 요청 처리가 같은 것으로 보인다 | 학습용 계산과 서비스 실행 계산의 목적 차이를 분리할 수 있습니다. | 모드 차이에 민감한 층을 다음 절에서 봐야 합니다. |

## 체크리스트

- 학습(learning)과 모델 실행(inference)이 무엇을 기준으로 나뉘는지 설명할 수 있는가?
- 파라미터를 바꾸는 단계와 고정된 파라미터를 쓰는 단계를 구분할 수 있는가?
- learning은 파라미터를 바꾸는 단계이고, inference는 바꾸지 않고 사용하는 단계라는 점을 설명할 수 있는가?
- 딥러닝 학습은 순전파, 손실 계산, 역전파, 업데이트를 포함한다는 점을 말할 수 있는가?
- inference에서도 forward는 수행되지만 목적과 후속 단계가 다르다는 점을 설명할 수 있는가?
- 결과가 나왔다는 사실만으로 학습이 일어난 것은 아니라는 점을 말할 수 있는가?
- 같은 모델 실행이라도 학습과 서비스 처리를 같은 것으로 말하고 있을 때, learning/inference 구분을 먼저 떠올릴 수 있는가?
- 이 절 다음에는 학습 모드와 평가 모드의 계산 차이를 따로 봐야 한다는 흐름을 알고 있는가?

## 출처와 참고 자료

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Christopher M. Bishop, `Pattern Recognition and Machine Learning`, Springer, 2006, 확인 날짜: 2026-06-29.
- Aurélien Géron, `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow`, 3rd ed., O'Reilly, 2022, 확인 날짜: 2026-06-29.

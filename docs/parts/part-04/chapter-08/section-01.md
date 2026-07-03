# P4-8.1 정규화(regularization)

P4-7장에서는 optimizer가 gradient를 실제 업데이트로 바꾸는 규칙이라는 점을 보았습니다. 하지만 optimizer가 잘 작동한다고 해서 항상 좋은 모델이 되는 것은 아닙니다. 여기서 바로 다음 질문이 생깁니다.

모델이 학습 데이터에는 아주 잘 맞는데, 새로운 데이터에서는 잘 안 맞는다면 무엇을 해야 하는가?

이 질문에 답하는 핵심 개념 중 하나가 정규화(regularization)입니다.

정규화는 모델이 학습 데이터에만 과하게 맞추지 않도록, 학습 과정에 제약이나 비용을 추가하는 생각이다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- 정규화는 왜 필요한가?
- 과적합(overfitting)과 어떤 관계가 있는가?
- 정규화는 단순한 벌점(penalty)만 뜻하는가?
- 딥러닝에서 정규화를 어떤 넓은 관점으로 읽으면 좋은가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- L1, L2의 상세 수식 유도
- weight decay의 프레임워크 구현 차이
- data augmentation, early stopping의 세부 튜닝

드롭아웃(dropout)은 P4-8.2에서 별도 절로 이어서 다루고, 학습 모드와 평가 모드의 계산 차이는 P4-6.2에서 다시 연결합니다. weight decay의 프레임워크 구현 차이와 data augmentation, early stopping의 세부 튜닝은 이 책의 현재 본편 범위 밖에 둡니다.

처음 읽을 때는 이 절을 `optimizer 다음에 붙는 또 하나의 설정`으로만 보지 말고, `업데이트 규칙`과 `선호하는 해의 성질`을 갈라 읽는 절로 보면 더 안전합니다.

| 지금 절에서 구분할 것 | 왜 중요한가 |
| --- | --- |
| optimizer | gradient를 보고 실제로 어떤 보폭으로 움직일지 정하는 절차이기 때문입니다. |
| regularization | 그 움직임이 너무 복잡한 해법으로 가지 않게 제약을 주는 관점이기 때문입니다. |
| normalization | 과적합 억제와 달리 값의 스케일과 분포를 다루기 쉽게 맞추는 질문이기 때문입니다. |

## 이 절의 목표

- 정규화를 `과적합을 줄이기 위한 제약`으로 설명할 수 있습니다.
- optimizer와 regularization의 역할 차이를 구분할 수 있습니다.
- regularization과 normalization이 왜 다른 질문에 답하는지 설명할 수 있습니다.
- 정규화가 손실 함수, 모델 크기, 데이터 양과 어떤 관계가 있는지 말할 수 있습니다.
- 실행 가능한 Python 예제로 벌점이 업데이트 크기에 어떤 영향을 주는지 확인할 수 있습니다.

## regularization과 normalization은 왜 다른가

이 절에서 말하는 정규화는 regularization입니다. 그런데 실무에서는 `normalize`, `normalization`이라는 말도 자주 나와서 처음 읽을 때 쉽게 섞입니다.

두 말은 이름이 비슷하지만, 겨냥하는 질문이 다릅니다.

| 항목 | regularization | normalization |
| --- | --- | --- |
| 먼저 답하려는 질문 | 모델이 너무 과하게 외우지 않게 하려면? | 입력값이나 중간값의 스케일을 더 다루기 쉽게 맞추려면? |
| 주된 관심 | 일반화(generalization), 과적합 억제 | 값의 범위, 분포, 학습 안정성 |
| 대표 예 | L2 penalty, dropout, early stopping | 입력 정규화, batch normalization, layer normalization |

즉, regularization은 `어떤 해를 덜 좋아하게 만들 것인가`에 가깝고, normalization은 `값을 어떤 범위와 분포로 다루기 쉽게 만들 것인가`에 더 가깝습니다.

물론 실제 딥러닝에서는 둘이 완전히 떨어져 있지 않습니다. 예를 들어 batch normalization은 계산 안정성과 학습 속도에 더 직접 연결되지만, 결과적으로 regularization 비슷한 효과가 함께 관찰되기도 합니다. 그래도 입문 단계에서는 먼저 다음처럼 나누는 편이 안전합니다.

- regularization: `과하게 외우지 않게 묶는 장치`
- normalization: `값의 스케일과 분포를 다루기 쉽게 맞추는 장치`

## 왜 정규화가 필요한가

딥러닝 모델은 표현력이 큽니다. 이 말은 강력하다는 뜻이기도 하지만, 동시에 학습 데이터의 우연한 패턴이나 잡음(noise)까지 따라가 버릴 위험이 있다는 뜻이기도 합니다.

예를 들어:

- 훈련 데이터(training data)에서는 손실이 계속 줄어듭니다
- 그런데 검증 데이터(validation data)에서는 어느 순간부터 성능이 더 좋아지지 않거나 오히려 나빠집니다

이런 상황은 Part 3에서 본 과적합(overfitting)과 연결됩니다.

정규화는 바로 이 지점에서 등장합니다. 모델에게 `훈련 데이터에 맞추되, 너무 복잡하게 맞추지는 말라`는 제약을 거는 것입니다.

## 정규화는 무엇을 막으려 하나

독자에게는 정규화의 목적을 다음 세 줄로 이해하면 충분합니다.

- 너무 큰 파라미터에 과하게 의존하지 않게 한다
- 특정 샘플의 우연한 패턴만 외우지 않게 한다
- 새로운 데이터에서도 더 안정적으로 작동하게 돕는다

즉, 정규화는 단순히 손실을 낮추는 것이 아니라, `어떤 방식으로 낮출 것인가`까지 제한하는 생각입니다.

## 정규화는 벌점만 뜻하는가

입문 교과서에서는 정규화를 자주 `손실 함수에 벌점(penalty) 항을 더하는 방식`으로 소개합니다. 이 설명은 중요하지만, 그 자체로는 다소 좁습니다.

딥러닝에서는 regularization을 더 넓게 보는 편이 좋습니다.

예를 들어 다음도 넓은 의미의 regularization으로 읽을 수 있습니다.

- 가중치 크기를 제어하는 penalty
- dropout처럼 일부 연결을 무작위로 끊는 방식
- early stopping처럼 너무 오래 학습하지 않는 전략
- data augmentation처럼 입력 다양성을 늘리는 방식

즉, regularization은 `하나의 공식`보다 `과적합을 줄이려는 설계 철학`에 가깝습니다.

## 손실 함수와 어떤 관계가 있는가

정규화는 종종 손실 함수와 함께 나타납니다.

\[
total\ loss = data\ loss + regularization\ term
\]

이 식을 다음처럼 읽으면 충분합니다.

- `data loss`: 예측이 정답과 얼마나 다른가
- `regularization term`: 모델이 너무 복잡한 방향으로 가지 않는가

즉, regularization은 `정답을 맞추는 비용` 외에 `너무 과한 복잡성을 쓰는 비용`을 더 붙이는 생각입니다.

이 때문에 optimizer는 이제 단순한 원래 손실이 아니라, regularization이 반영된 전체 목적을 줄이게 됩니다.

## optimizer와 regularization은 무엇이 다른가

독자는 optimizer와 regularization을 둘 다 `학습을 조정하는 것`으로 느낄 수 있습니다. 하지만 역할은 다릅니다.

| 항목 | 역할 |
| --- | --- |
| optimizer | gradient를 바탕으로 파라미터를 어떻게 업데이트할지 정함 |
| regularization | 어떤 해를 선호하고 어떤 복잡성을 피할지 제약을 줌 |

즉:

- optimizer는 `어떻게 움직일까`
- regularization은 `어떤 방향을 덜 좋아할까`

를 다룹니다.

이 구분이 잡혀야 이후 weight decay, dropout, early stopping을 하나의 관점으로 묶기 쉽습니다.

## 사례로 보기

### 사례 1. 훈련 성능은 높지만 검증 성능이 떨어지는 경우

사람은 보통 훈련 손실이 계속 줄고 정확도가 높아지면 `학습이 잘되고 있다`고 먼저 생각합니다. 그런데 검증 데이터에서 성능이 오히려 떨어지기 시작하면, 이 모델은 훈련 데이터 세부 패턴을 너무 잘 외운 것일 수 있습니다. 예를 들어 연습 문제에서는 거의 다 맞는데, 숫자 위치나 문장 표현을 조금만 바꾼 새 문제에서는 갑자기 흔들리는 장면과 비슷합니다. 이때 사람이 먼저 보는 기준은 `연습 세트를 얼마나 잘 맞췄는가`보다 `새 데이터에서도 비슷하게 버티는가`여야 합니다. regularization은 바로 이런 `훈련 성능만 좋고 새 데이터에서는 흔들리는` 경향을 줄이려는 장치로 등장합니다. 즉, 훈련 점수를 조금 덜 공격적으로 올리더라도 검증 성능이 덜 무너지게 만드는 쪽이 더 좋은 해법일 수 있습니다. 그래서 이 사례에서 확인해야 할 결과는 훈련 점수 최고치보다, 검증 성능 하락이 실제로 덜 심해지는가입니다.

### 사례 2. 파라미터가 지나치게 커지는 경우

사람이 모델을 손으로 해석할 때는 보통 `오차만 줄면 된다`고 생각하기 쉽습니다. 하지만 어떤 모델은 손실을 줄이기 위해 일부 가중치를 지나치게 크게 키우기도 합니다. 이렇게 되면 특정 입력 특징 하나에 과하게 기대는 불안정한 모델이 될 수 있습니다. 예를 들어 표 데이터 분류에서 한 열 값이 조금만 흔들려도 예측이 크게 뒤집힌다면, 모델이 그 열 하나에 너무 의존하고 있을 수 있습니다. 이때 regularization penalty를 주면 `맞추는 것`과 `지나치게 큰 가중치를 피하는 것`을 함께 고려하게 됩니다. 즉, 정규화는 정답을 덜 맞추게 하려는 것이 아니라 `너무 한쪽으로 몰린 해법`을 덜 선호하게 만드는 장치입니다. 결과적으로 입력이 조금 바뀌어도 예측이 덜 급격하게 흔들리는 쪽으로 유도할 수 있습니다. 그래서 이 사례에서 확인해야 할 결과는 손실 감소만이 아니라, 특정 열 값이 조금 바뀌어도 예측이 과격하게 뒤집히지 않는가입니다.

### 사례 3. 입력 스케일 조정과 과적합 억제를 같은 것으로 보면 왜 헷갈릴까

표 데이터 실험에서 키, 몸무게, 연봉처럼 범위가 크게 다른 열을 함께 넣는다고 해 보겠습니다. 이때 어떤 사람은 값을 0과 1 사이로 맞추는 작업도 `정규화`라고 부르고, 가중치가 너무 커지지 않게 벌점을 주는 작업도 `정규화`라고 부를 수 있습니다. 하지만 앞의 작업은 `값의 스케일을 맞춰 계산을 다루기 쉽게 만드는 일`이고, 뒤의 작업은 `모델이 너무 복잡한 해법으로 가지 않게 묶는 일`입니다. 예를 들어 입력 스케일만 맞췄다고 해서 과적합이 자동으로 사라지는 것은 아니고, 반대로 regularization을 넣었다고 해서 입력 범위 차이가 저절로 정리되는 것도 아닙니다. 그래서 이 사례에서 확인해야 할 결과는 스케일 조정만으로 해결되는 문제와, 가중치 제약을 넣어야 줄어드는 문제가 실제로 서로 다르게 나타나는가입니다.

### 사례 4. 데이터가 적은 문제

사람은 데이터가 적으면 `그만큼 더 열심히 맞추면 되지 않을까`라고 생각하기 쉽습니다. 하지만 실제로는 데이터가 적을수록 모델이 우연한 잡음과 예외를 규칙처럼 외워 버릴 위험이 더 커집니다. 예를 들어 샘플 몇 개 안에서만 보인 특이한 표현이나 배경 색 하나를 마치 일반 규칙처럼 학습할 수 있습니다. 그러면 훈련 셋에서는 잘 맞지만, 실제 새 입력에서는 그 우연한 단서가 사라져 성능이 급격히 떨어질 수 있습니다. 이때 정규화는 더 중요해집니다. 즉, data size와 model capacity의 균형 문제와 연결되며, 적은 데이터일수록 `과하게 외우지 않게 묶어 두는 장치`가 더 필요해집니다. 그래서 이 사례에서 확인해야 할 결과는 작은 데이터셋에서 훈련 성능만 높아지는 대신, 새 입력에서의 급격한 성능 붕괴가 실제로 덜해지는가입니다.

## 실행 가능한 Python 예제로 보기

이번 예제의 목표는 regularization 항이 들어가면 업데이트가 `정답만 맞추는 방향`에서 조금 더 보수적으로 바뀔 수 있음을 확인하는 것입니다. 한 번의 업데이트만 보는 대신, 여러 step에서 가중치가 얼마나 빨리 커지는지 비교해 보겠습니다.

입력:

- 현재 가중치 `w`
- 데이터 손실에서 나온 gradient
- regularization 강도 `lambda_value`

출력:

- regularization 없이 업데이트한 결과
- regularization을 더한 뒤 업데이트한 결과
- step이 반복될수록 가중치 크기 차이가 어떻게 벌어지는지에 대한 비교

문제 상황:

- regularization은 정의만 보면 막연하므로, 같은 gradient에 추가 항이 붙을 때 가중치 크기가 어떻게 달라지는지 직접 볼 필요가 있다

확인할 개념:

- regularization은 데이터 gradient 외에 가중치 크기를 줄이려는 방향을 더한다
- step이 반복될수록 규제가 있는 쪽이 더 작은 가중치를 유지하는 경향을 보일 수 있다

입력(input):

위에 정리한 초기 가중치, 데이터 gradient, 학습률, regularization 강도를 사용합니다.

```python
initial_w = 2.5
data_gradient = -4.0
learning_rate = 0.1
lambda_value = 0.2
steps = 3

w_without_reg = initial_w
w_with_reg = initial_w

for step in range(1, steps + 1):
    w_without_reg = w_without_reg - learning_rate * data_gradient

    reg_gradient = 2 * lambda_value * w_with_reg
    total_gradient = data_gradient + reg_gradient
    w_with_reg = w_with_reg - learning_rate * total_gradient

    print(f"[step {step}]")
    print("without_reg =", round(w_without_reg, 3))
    print("reg_gradient =", round(reg_gradient, 3))
    print("total_gradient =", round(total_gradient, 3))
    print("with_reg =", round(w_with_reg, 3))
    print("---")
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
[step 1]
without_reg = 2.9
reg_gradient = 1.0
total_gradient = -3.0
with_reg = 2.8
---
[step 2]
without_reg = 3.3
reg_gradient = 1.12
total_gradient = -2.88
with_reg = 3.088
---
[step 3]
without_reg = 3.7
reg_gradient = 1.235
total_gradient = -2.765
with_reg = 3.365
---
```

이 결과에서 읽어야 할 핵심은 다음입니다.

- regularization이 없으면 가중치는 더 크게 증가합니다
- regularization 항이 들어오면 step이 반복될수록 증가 폭이 조금씩 더 줄어듭니다
- 즉, regularization은 단순히 성능을 깎는 것이 아니라 `덜 과격한 해`를 선호하게 만듭니다

정규화는 딥러닝 이전의 통계적 학습 이론(statistical learning theory)와도 깊게 연결됩니다. 모델이 너무 복잡해지면 훈련 데이터에는 잘 맞지만 일반화가 나빠질 수 있다는 문제는 오래전부터 핵심 주제였습니다.

딥러닝 시대에 regularization이 더 중요해진 이유는 분명합니다.

- 모델 용량(capacity)이 매우 커졌고
- 데이터 분포의 편향과 잡음 문제도 여전하며
- 높은 훈련 성능만으로는 좋은 모델을 보장할 수 없기 때문입니다

커리큘럼 관점에서 이 절은 optimizer 다음에 오는 것이 자연스럽습니다.

- 바로 앞의 P4-7.1, P4-7.2가 `어떻게 내려갈 것인가`를 다루었다면
- optimizer는 잘 내려가는 방법을 다루고
- regularization은 어디까지 내려가게 허용할지, 어떤 해를 더 선호할지를 다룹니다

즉, 두 절은 모두 학습을 조정하지만 질문이 다릅니다.

## 다음 절과의 연결

여기까지 오면 다음 질문이 남습니다.

- regularization을 벌점이 아니라 구조적 흔들림으로 넣는 방법은 무엇인가?
- 왜 일부 연결을 무작위로 끊는 dropout이 과적합 억제에 도움이 되는가?

이 질문은 바로 P4-8.2 드롭아웃(dropout)으로 이어집니다.

## 이 절에서 기억할 관점

- regularization은 과적합을 줄이기 위한 제약이나 비용을 추가하는 생각입니다.
- regularization과 normalization은 이름이 비슷하지만, 하나는 과적합 억제 쪽을, 다른 하나는 값의 스케일과 분포 정리 쪽을 더 직접 다룹니다.
- regularization은 벌점 공식만이 아니라 더 넓은 설계 철학으로 볼 수 있습니다.
- optimizer는 업데이트 방법을, regularization은 선호하는 해의 성질을 조정합니다.
- 일반화 문제를 이해하려면 regularization을 반드시 함께 봐야 합니다.

## 체크리스트

- regularization을 과적합 억제 관점으로 설명할 수 있는가?
- regularization과 normalization의 차이를 말할 수 있는가?
- optimizer와 regularization의 역할 차이를 구분할 수 있는가?
- data loss와 regularization term을 함께 읽는 이유를 말할 수 있는가?
- 다음 절의 dropout이 왜 regularization 장 안에 들어오는지 설명할 수 있는가?

## 출처와 참고 자료

- Trevor Hastie, Robert Tibshirani, Jerome Friedman, `The Elements of Statistical Learning`, 2nd ed., Springer, 2009, 확인 날짜: 2026-06-29.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 확인 날짜: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Christopher M. Bishop, `Pattern Recognition and Machine Learning`, Springer, 2006, 확인 날짜: 2026-06-29.

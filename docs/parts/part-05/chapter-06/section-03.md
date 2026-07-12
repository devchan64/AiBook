# P5-6.3 보충학습: 초기화(initialization), 수치 안정성(numerical stability), 배치 정규화(batch normalization)를 처음 묶어 읽는 법

Section ID: `P5-6.3`
Version: `v2026.07.12`

P5-6.2에서는 학습 모드(training mode)와 평가 모드(evaluation mode)를 구분하면서 dropout과 batch normalization이 왜 특별히 모드 차이에 민감한지 보았습니다. 여기서 초심자에게 자주 남는 질문이 하나 더 있습니다.

층을 더 깊게 쌓았다고 해서 왜 바로 잘 학습되지 않는가?

이 질문에 답하려면 초기화(initialization), 수치 안정성(numerical stability), 배치 정규화(batch normalization)를 따로따로 외우기보다, `깊은 네트워크가 실제로 덜 흔들리게 된 이유`라는 하나의 축으로 함께 읽는 편이 좋습니다.

초기화는 학습이 시작될 출발점을 정하고, 수치 안정성은 값과 gradient가 계산 중에 너무 커지거나 작아지지 않게 보는 기준이며, batch normalization은 학습 중 활성값 분포를 더 다루기 쉬운 범위로 정리해 주는 장치다.

이 축이 다시 흐려질 때는 개념사전의 [학습 모드(training mode)](../../../reference/concept-glossary.md#학습-모드training-mode), [배치 정규화(batch normalization)](../../../reference/concept-glossary.md#glossary-batch-normalization), [초기화(initialization)](../../../reference/concept-glossary.md#glossary-initialization), [수치 안정성(numerical stability)](../../../reference/concept-glossary.md#glossary-numerical-stability) 항목을 함께 다시 보는 편이 좋습니다.

## 이 절의 범위

- 왜 깊은 네트워크는 층만 늘린다고 바로 잘 학습되지 않는가?
- 초기화(initialization)는 무엇을 정하는가?
- 수치 안정성(numerical stability)은 무엇을 걱정하는 개념인가?
- batch normalization은 왜 학습 안정화 도구로 자주 함께 언급되는가?
- 이 세 개념은 optimizer, regularization과 어떻게 다른 질문에 답하는가?

이 절에서는 다음 내용을 깊게 다루지 않습니다.

- Xavier 초기화와 He 초기화의 엄밀한 수식 유도
- softmax/log-sum-exp의 상세 수치 안정화 구현
- batch normalization의 역전파 수식
- layer normalization, group normalization의 상세 비교

ReLU 계열과 깊은 학습 확산의 큰 흐름은 P5-3.2에서 다시 연결하고, batch normalization이 학습/평가 모드 차이에 왜 민감한지는 P5-6.2에서 이미 본 기준 위에서 다시 읽습니다. regularization과 normalization을 구분하는 넓은 관점은 P5-8.1에서 이어지고, optimizer update 자체는 P5-7.1, P5-7.2에서 다시 붙입니다. normalization 계열의 세부 분화 비교는 이 책의 현재 본편 범위 밖에 둡니다.

## 이 절의 목표

- 초기화를 `학습 시작점의 값 배치`로 설명할 수 있습니다.
- 수치 안정성을 `값과 gradient가 계산 중에 감당 가능한 범위를 유지하는 문제`로 설명할 수 있습니다.
- batch normalization을 `활성값 분포를 정리해 학습을 덜 흔들리게 하는 장치`로 설명할 수 있습니다.
- optimizer, regularization, batch normalization이 서로 다른 질문에 답한다는 점을 구분할 수 있습니다.
- 실행 가능한 Python 예제로 출력 스케일과 batch normalization의 직관을 확인할 수 있습니다.

## 왜 이 셋을 한 번에 묶어 읽어야 하나

깊은 네트워크를 처음 배우면 다음 오해가 자주 생깁니다.

- 층을 더 쌓으면 자동으로 더 잘 배울 것이다
- optimizer만 Adam으로 바꾸면 대부분 해결될 것이다
- batch normalization은 그냥 라이브러리 옵션 하나일 뿐이다

하지만 실제로는 학습이 시작되는 출발점, 중간 계산에서 값이 어떻게 커지거나 줄어드는지, 각 층이 다음 층으로 어떤 범위의 값을 넘기는지가 함께 맞물립니다.

이 흐름을 아주 짧게 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-05/chapter-06/stabilization-bridge-flow-ko.mmd"
```

핵심은 `학습이 잘 안 된다`는 현상이 항상 한 가지 원인으로만 생기지 않는다는 점입니다.

- 시작값이 너무 비슷하거나 극단적일 수 있고
- 층을 지나며 값이 너무 커지거나 거의 사라질 수 있고
- 활성값 분포가 다음 계산을 계속 흔들 수 있습니다

그래서 이 절에서는 이 셋을 `깊은 학습이 실제로 가능해지는 조건`으로 묶어 봅니다.

## 초기화(initialization)는 무엇을 정하나

초기화는 학습을 시작하기 전 파라미터(parameter)에 어떤 숫자를 배치할지 정하는 일입니다.

겉으로 보면 단순히 출발점만 정하는 것처럼 보이지만, 실제로는 다음 두 질문과 직접 연결됩니다.

1. 서로 다른 뉴런이 서로 다른 역할을 배우기 시작할 수 있는가?
2. 첫 몇 번의 forward와 backward에서 값이 지나치게 커지거나 작아지지 않는가?

예를 들어 모든 가중치를 완전히 같은 값, 특히 0으로 시작하면 여러 뉴런이 같은 입력에 같은 반응을 보이고 같은 gradient를 받을 수 있습니다. 그러면 층을 여러 개 둬도 서로 다른 특징을 나눠 배우기 어렵습니다.

즉, 초기화의 첫 책임은 `아무렇게나 시작하지 않는 것`보다 `모든 뉴런이 똑같이 시작하지 않게 하는 것`에 가깝습니다.

## 왜 출발점이 같으면 안 되나

퍼셉트론 하나만 있을 때는 시작값이 약간 엉성해도 큰 문제가 없어 보일 수 있습니다. 하지만 다층 구조에서는 같은 층 안 여러 뉴런이 서로 다른 조합을 배워야 합니다.

만약 출발점이 완전히 같다면:

- 같은 입력을 보고
- 같은 출력을 만들고
- 같은 gradient를 받고
- 같은 방향으로 업데이트됩니다

그 결과 여러 뉴런을 둔 이점이 줄어듭니다.

이 점을 초심자 기준으로 한 줄로 묶으면 다음과 같습니다.

`초기화는 단지 첫 숫자를 찍는 일이 아니라, 여러 뉴런이 서로 다른 역할로 갈라질 가능성을 열어 두는 일이다.`

## 수치 안정성(numerical stability)은 무엇을 걱정하나

수치 안정성은 계산 과정에서 값이나 gradient가 너무 커지거나 너무 작아져 학습이 흔들리지 않는지 보는 기준입니다.

여기서는 다음 두 장면만 먼저 떠올리면 충분합니다.

- 층을 지날수록 값이 계속 커져 폭발하는 경우
- 층을 지날수록 값이나 gradient가 너무 작아져 사실상 사라지는 경우

딥러닝은 같은 종류의 계산을 층마다 반복합니다. 그래서 한 번의 작은 불안정이 깊은 층을 지나며 더 커질 수 있습니다.

| 문제 장면 | 초심자용 직관 | 학습에서 생기는 결과 |
| --- | --- | --- |
| 값이 너무 커짐 | 다음 층이 지나치게 큰 숫자를 계속 받는다 | 출력과 gradient가 흔들리기 쉽습니다 |
| 값이 너무 작아짐 | 다음 층이 거의 비슷한 작은 값만 본다 | gradient가 약해져 학습이 더뎌질 수 있습니다 |

이 절에서는 수학 증명을 하지 않지만, 중요한 직관은 분명합니다.

`깊은 학습은 층을 많이 쌓는 문제이기도 하지만, 그 많은 계산을 숫자 범위 안에서 버티게 하는 문제이기도 하다.`

## ReLU, 초기화, 수치 안정성은 왜 같이 언급되나

P5-3.2에서 본 것처럼 ReLU 계열은 깊은 네트워크에서 널리 쓰입니다. 하지만 활성화 함수 하나만 바뀌었다고 모든 문제가 자동으로 해결되는 것은 아닙니다.

실제로는 다음 요소들이 함께 맞물립니다.

- ReLU처럼 양수 구간을 더 직접 통과시키는 함수
- 너무 작거나 큰 값으로 시작하지 않게 하는 초기화
- optimizer와 학습률 설정
- batch normalization 같은 분포 안정화 장치

즉, `깊은 학습이 실용화되었다`는 말은 보통 한 발명만 뜻하지 않고, 여러 안정화 장치가 함께 맞물렸다는 뜻에 더 가깝습니다.

## batch normalization은 왜 중요한가

batch normalization은 한 배치(batch) 안의 평균(mean)과 분산(variance)을 참고해 활성값 분포를 다시 정리하는 방식입니다.

초심자 기준에서는 다음처럼 이해하면 충분합니다.

- 앞 층 출력이 너무 들쭉날쭉하면
- 다음 층이 계속 흔들리는 분포를 받아 학습해야 하고
- 그러면 학습 속도와 안정성이 함께 영향을 받을 수 있습니다

batch normalization은 이때 `현재 배치 기준으로 값을 한 번 더 다루기 쉬운 범위로 정리하고 넘기는 장치`처럼 읽을 수 있습니다.

P5-6.2에서 본 mode 차이도 여기서 다시 연결됩니다.

- 학습 중에는 현재 배치 통계를 참고하고
- 평가 중에는 학습 동안 쌓인 기준을 더 많이 참고합니다

즉, batch normalization은 단순히 `정규화 이름 하나`가 아니라, 학습 안정화와 mode 전환을 함께 읽게 만드는 대표 사례입니다.

## regularization과는 무엇이 다른가

초심자는 batch normalization, dropout, weight decay를 모두 `학습을 돕는 옵션`처럼 한 덩어리로 볼 수 있습니다. 하지만 질문이 다릅니다.

| 항목 | 먼저 답하는 질문 |
| --- | --- |
| initialization | 학습을 어떤 출발점에서 시작할 것인가? |
| numerical stability | 반복 계산 중 값과 gradient가 감당 가능한 범위를 유지하는가? |
| batch normalization | 활성값 분포를 더 다루기 쉬운 범위로 정리할 것인가? |
| optimizer | gradient를 실제로 어떤 보폭과 규칙으로 업데이트할 것인가? |
| regularization | 모델이 너무 복잡한 해법으로 가지 않게 어떤 제약을 둘 것인가? |

이 표를 먼저 고정해 두면, 뒤에서 새로운 기법 이름을 만나도 `출발점`, `계산 안정성`, `업데이트`, `일반화` 중 어디에 가까운지 분리해 읽기 쉬워집니다.

## 사례 및 예시

### 사례 1. 모든 가중치를 0으로 시작하면 왜 답답한가

같은 층에 뉴런 두 개가 있고 둘 다 같은 입력을 받는다고 해 보겠습니다. 사람은 뉴런이 두 개면 자동으로 서로 다른 특징을 배울 것처럼 느끼기 쉽습니다. 하지만 두 뉴런의 가중치를 모두 0으로 시작하면 처음 출력도 같고, 역전파에서 받는 gradient도 같아질 가능성이 큽니다. 그러면 업데이트 뒤에도 두 뉴런이 계속 비슷하게 움직일 수 있습니다. 여기서 바뀌는 점은 `뉴런 개수`가 아니라 `서로 다른 역할로 갈라질 출발점이 있느냐`입니다. 그래서 이 사례에서 확인해야 할 결과는 뉴런 수를 늘리는 것만으로는 충분하지 않고, 초기화가 서로 다른 학습 경로를 열어 주는가입니다.

### 사례 2. 층을 지나며 값이 너무 커지는 경우

입력값이 2나 3 정도인데 큰 가중치를 여러 층에서 곱해 간다고 생각해 보겠습니다. 사람은 각 층이 하는 일이 비슷하니 전체 계산도 대충 비슷하겠지라고 느끼기 쉽습니다. 하지만 큰 값이 반복 곱해지면 뒤 층으로 갈수록 값이 지나치게 커질 수 있습니다. 그러면 활성화 함수 반응이 치우치거나 gradient도 불안정해질 수 있습니다. 이때 확인해야 할 핵심은 모델이 `깊다`는 사실 자체보다 `반복 계산이 숫자 범위를 어디로 밀고 가는가`입니다. 그래서 이 사례에서 확인해야 할 결과는 수치 안정성이 단순한 구현 취향이 아니라, 깊은 학습이 실제로 버티는 조건과 연결되는가입니다.

### 사례 3. batch normalization이 왜 mode와 함께 읽히는가

학습 중에는 한 배치의 평균과 분산을 참고해 값을 정리했는데, 배포에서는 한 번에 한 샘플만 들어온다고 해 보겠습니다. 사람은 같은 모델이니 같은 방식으로 계산해도 되지 않을까라고 생각하기 쉽습니다. 하지만 이 경우 현재 배치 통계만 그대로 쓰면 결과가 배치 구성에 지나치게 민감해질 수 있습니다. 그래서 학습과 평가에서 batch normalization 동작을 나눠 읽어야 합니다. 여기서 바뀌는 점은 `층의 이름`이 아니라 `어떤 통계를 기준으로 값을 정리할 것인가`입니다. 그래서 이 사례에서 확인해야 할 결과는 batch normalization이 mode 설명과 함께 있을 때 더 자연스럽게 이해되는가입니다.

| 사람이 먼저 보기 쉬운 기준 | 초기화·수치 안정성·batch normalization 관점으로 다시 읽는 기준 |
| --- | --- |
| 층만 더 쌓으면 표현력이 늘어 자동으로 더 잘 배울 것 같다고 느끼기 쉽다 | 층을 깊게 쌓을수록 출발점, 값 범위, 활성 분포가 함께 흔들릴 수 있어 안정화 조건을 같이 봐야 한다 |
| optimizer만 Adam으로 바꾸면 대부분 해결될 것 같다고 느끼기 쉽다 | optimizer는 업데이트 규칙이고, 초기화·수치 안정성·batch normalization은 그 이전에 계산이 버틸 조건을 다룬다 |
| batch normalization은 라이브러리 옵션 하나라고 생각하기 쉽다 | batch normalization은 학습 중 활성 분포를 정리하고 mode 차이까지 함께 읽게 만드는 안정화 장치다 |
| 뉴런 수나 층 수만 늘리면 서로 다른 특징을 자동으로 배울 것 같다고 느끼기 쉽다 | 초기화가 같으면 여러 뉴런이 같은 경로로 움직일 수 있고, 큰 값은 반복 계산 중 불안정을 키울 수 있다 |

이 사례들에서 최종적으로 확인해야 할 결과는 분명합니다. 깊은 네트워크 안정화의 핵심은 `기법 이름을 많이 외우는가`가 아니라, 초기화는 출발점을, 수치 안정성은 반복 계산 범위를, batch normalization은 중간 분포를 다루며 셋이 함께 학습을 덜 흔들리게 만든다는 점입니다.

## 연습 및 예제

이번 예제의 목표는 같은 입력 묶음이라도 가중치 스케일이 다르면 출력 범위가 크게 달라질 수 있고, 간단한 batch normalization으로 그 범위를 다시 정리할 수 있다는 점을 보는 것입니다.

입력:

- 같은 배치 입력 3개
- 작은 스케일의 가중치
- 큰 스케일의 가중치

출력:

- 작은 초기화일 때의 선형 출력
- 큰 초기화일 때의 선형 출력
- 큰 초기화 출력에 간단한 batch normalization을 적용한 값

문제 상황:

- 초기화와 batch normalization이 각각 무엇을 바꾸는지 숫자 범위 차이로 먼저 확인할 필요가 있다

확인할 개념:

- 출발 가중치 스케일이 다르면 같은 입력도 매우 다른 출력 범위를 만들 수 있다
- batch normalization은 출력값 자체를 없애는 것이 아니라 분포를 다시 정리한다

입력(input):

아래 배치 입력과 두 종류의 가중치를 사용합니다.

코드를 보기 전에 먼저 어떤 출력이 어디서 크게 벌어질지 예상해 보면, `초기화가 바꾸는 것`과 `batch normalization이 바꾸는 것`을 더 분리해서 볼 수 있습니다.

| 비교 항목 | 먼저 예상해 볼 출력 | 예상 이유 |
| --- | --- | --- |
| `small_init_outputs` | 0 근처의 비교적 작은 범위에 머물 가능성이 큼 | 가중치 크기가 작아 같은 입력이라도 선형 출력 스케일이 크게 커지지 않습니다. |
| `large_init_outputs` | 값 범위가 더 크게 벌어질 가능성이 큼 | 큰 가중치가 같은 입력 차이를 더 크게 증폭하기 때문입니다. |
| `batch_mean`, `batch_variance` | `large_init_outputs` 쪽에서 분포 중심과 퍼짐이 더 두드러질 가능성이 큼 | 큰 출력 스케일일수록 평균과 분산 차이도 더 눈에 띄게 드러납니다. |
| `normalized_large_outputs` | 평균 0 근처, 비교적 정리된 범위로 다시 옮겨질 가능성이 큼 | batch normalization은 큰 출력 자체를 지우는 것이 아니라 분포를 다시 다루기 쉬운 기준으로 맞춥니다. |

이 표의 목적은 정확한 수치를 미리 암기하는 데 있지 않습니다. 같은 입력이라도 초기화 스케일은 `출력 범위를 얼마나 벌리는가`를 먼저 바꾸고, batch normalization은 이미 벌어진 출력을 `어떻게 다시 정리해 넘길 것인가`를 바꾼다는 점을 코드 전에 붙잡는 데 있습니다.

```python
inputs = [
    [1.0, 2.0],
    [2.0, 1.0],
    [0.5, 3.0],
]

weights_small = [0.2, -0.1]
weights_large = [3.0, -2.0]

def linear(batch, weights):
    outputs = []
    for x1, x2 in batch:
        outputs.append(x1 * weights[0] + x2 * weights[1])
    return outputs

def batch_norm(values, eps=1e-5):
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    normalized = [(v - mean) / ((variance + eps) ** 0.5) for v in values]
    return mean, variance, normalized

small_outputs = linear(inputs, weights_small)
large_outputs = linear(inputs, weights_large)
mean, variance, normalized_large = batch_norm(large_outputs)

print("small_init_outputs =", [round(v, 3) for v in small_outputs])
print("large_init_outputs =", [round(v, 3) for v in large_outputs])
print("batch_mean =", round(mean, 3))
print("batch_variance =", round(variance, 3))
print("normalized_large_outputs =", [round(v, 3) for v in normalized_large])
```

출력(output) 예시는 다음처럼 읽으면 됩니다.

```text
small_init_outputs = [0.0, 0.3, -0.2]
large_init_outputs = [-1.0, 4.0, -4.5]
batch_mean = -0.5
batch_variance = 12.5
normalized_large_outputs = [-0.141, 1.273, -1.131]
```

이 예제에서 바로 읽어야 할 핵심은 다음입니다.

- 작은 초기화와 큰 초기화는 같은 입력에도 다른 출력 스케일을 만듭니다.
- 큰 출력이 바로 `틀렸다`는 뜻은 아니지만, 반복 계산이 많아지면 안정성에 영향을 줄 수 있습니다.
- batch normalization은 활성값 분포를 다시 정리해 다음 층이 더 다루기 쉬운 범위를 보게 합니다.

즉, 이 예제는 `초기화가 출발 범위를 바꾸고, batch normalization이 중간 분포를 정리한다`는 점을 보여 주는 축약 안정화 비교입니다.

출력 숫자도 `값이 달라졌다`에서 멈추지 않고, 어떤 종류의 안정화 질문을 보여 주는지 나눠 읽어야 합니다.

| 비교 장면 | 출력에서 먼저 보이는 것 | 그대로 두면 남기 쉬운 해석 | 안정화 관점에서 다시 읽는 해석 |
| --- | --- | --- | --- |
| `small_init_outputs` vs `large_init_outputs` | 같은 입력인데 출력 범위가 크게 벌어진다 | 큰 값이 나왔으니 무조건 더 좋은 표현이라고 느끼기 쉽다 | 초기화 스케일이 출발 출력 범위를 얼마나 밀어 올리는지 먼저 읽는다 |
| `large_init_outputs` | `-1.0`, `4.0`, `-4.5`처럼 퍼짐이 크다 | 숫자가 다양하니 정보가 많다고만 느끼기 쉽다 | 깊은 반복 계산에서는 이런 큰 스케일이 다음 층과 gradient를 더 흔들 수 있다고 읽는다 |
| `normalized_large_outputs` | 평균 0 근처의 더 정리된 범위로 다시 옮겨진다 | batch normalization이 큰 값을 그냥 없애 버렸다고 느끼기 쉽다 | 분포 중심과 퍼짐을 다시 맞춰 다음 층이 더 다루기 쉬운 입력으로 바꿨다고 읽는다 |

이 비교까지 같이 보면, 초기화와 batch normalization은 같은 `학습 보조 옵션`이 아니라 서로 다른 위치에서 다른 종류의 흔들림을 줄인다는 점이 더 선명해집니다.

## 체크리스트

- 깊은 네트워크는 구조를 쌓는 문제이면서 동시에 계산을 버티게 하는 문제라는 점을 설명할 수 있는가?
- 초기화(initialization)를 `출발 가중치 배치`라는 관점으로 설명할 수 있는가?
- 수치 안정성(numerical stability)을 `깊은 반복 계산이 숫자 범위를 어떻게 흔드는가`라는 관점으로 설명할 수 있는가?
- batch normalization이 왜 학습 안정화와 mode 차이 설명에 함께 등장하는지 말할 수 있는가?
- batch normalization은 활성값 분포를 더 다루기 쉬운 범위로 정리하는 학습 안정화 장치라는 점을 설명할 수 있는가?
- optimizer, regularization, batch normalization이 서로 다른 질문에 답한다는 점을 구분할 수 있는가?

## 출처와 참고 자료

- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, `Dive into Deep Learning`, `5.4 Numerical Stability and Initialization`, `8.5 Batch Normalization`, `12 Optimization Algorithms`, 확인 날짜: 2026-07-11. [https://d2l.ai/](https://d2l.ai/){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, Part II `Modern Practical Deep Networks`, 확인 날짜: 2026-07-11. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Stanford `CS231n: Deep Learning for Computer Vision`, Schedule and course notes on `Regularization and Optimization`, `Neural Networks and Backpropagation`, `CNN Architectures`, 확인 날짜: 2026-07-11. [https://cs231n.stanford.edu/](https://cs231n.stanford.edu/){: target="_blank" rel="noopener noreferrer" }

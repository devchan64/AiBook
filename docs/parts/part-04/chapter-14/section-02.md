# P4-14.2 트리의 과적합

> Section ID: `P4-14.2`
> Version: `v2026.07.20`

P4-14.1에서는 결정트리(decision tree)를 `질문을 나누어 예측하는 모델`로 보았습니다. 그 절의 장점은 분명했습니다.

- 질문 흐름으로 읽기 쉽다.
- 조건문처럼 설명하기 쉽다.
- 표 형식 데이터(tabular data)에서 직관적으로 느껴진다.

하지만 같은 성질이 바로 위험으로도 이어집니다. 질문을 계속 더 만들 수 있다면, 트리는 훈련 데이터를 거의 외워 버릴 수도 있습니다. 이 지점이 바로 트리의 과적합(overfitting) 문제입니다.

P4-14.1이 `좋은 첫 질문과 다음 질문을 어떻게 읽을 것인가`를 다루는 절이었다면, 이 절은 그 질문 흐름이 어디서부터 패턴 설명이 아니라 예외 암기로 바뀌는지를 읽는 절입니다. 그래서 여기서는 트리를 더 깊게 만드는 일이 언제 도움이 되고 언제 구조를 흔드는지까지 같이 봐야 합니다.

이 절은 결정트리의 기본 정의를 다시 길게 반복하지 않습니다. `질문을 나누어 예측한다`는 핵심 직관은 P4-14.1과 [개념사전](../../../reference/concept-glossary.md)을 기준으로 다시 연결하고, 과적합 자체의 일반 손잡이는 P4-5.1을 함께 다시 떠올려야 합니다.

## 트리의 과적합에서 닫을 질문

이 절은 다음 질문에 답합니다.

- 결정트리는 왜 다른 모델보다 과적합이 쉽게 눈에 띄는가?
- 트리가 깊어질수록 무슨 일이 생기는가?
- `max_depth`, `min_samples_leaf`, `ccp_alpha`는 어떤 역할을 하는가?
- train 성능과 test 성능이 왜 다르게 움직일 수 있는가?

이 내용은 P4-15, P4-16, 그리고 P4-9의 튜닝 문맥과 다시 연결합니다. 즉, 이번 절은 트리의 질문 흐름이 어디서부터 패턴 설명이 아니라 예외 암기로 바뀌는지를 먼저 붙잡는 자리입니다.

## 트리의 과적합에서 남길 판단 기준

- 트리의 과적합을 `너무 세밀한 질문이 훈련 데이터를 외우는 현상`으로 설명할 수 있습니다.
- 깊이(depth), leaf 크기, pruning이 트리 복잡도를 제어하는 장치라는 점을 말할 수 있습니다.
- train 성능 상승이 test 성능 상승을 보장하지 않는다는 점을 다시 확인할 수 있습니다.
- 결정트리의 장점과 과적합 위험을 함께 읽는 기준을 갖게 됩니다.

## 학습 배경

### 왜 트리는 과적합이 잘 보이는가

결정트리는 본질적으로 `분기(split)를 반복하면서 node를 더 작게 나누는 구조`입니다. 이 구조는 강력하지만, 제한이 없으면 점점 더 작은 잎(leaf)을 만들 수 있습니다.

scikit-learn 사용자 가이드는 결정트리 학습기가 `over-complex trees`를 만들 수 있고, 이런 트리는 데이터를 잘 일반화(generalize)하지 못한다고 설명합니다. 같은 문서는 이를 overfitting이라고 부르며, pruning, `min_samples_leaf`, `max_depth` 같은 장치가 필요하다고 설명합니다.

`트리는 질문을 더 추가할수록 훈련 데이터의 예외까지 따라갈 수 있다. 하지만 그 예외가 새 데이터에서도 반복된다는 보장은 없다.`

여기서도 기록 구조를 같이 고정해 둡니다. 과적합 절은 단순히 `깊어지면 위험하다`고 말하는 절이 아니라, `복잡도가 늘 때 어떤 실패가 새로 생기는가`, `어떤 review 사례가 계속 남는가`, `어느 지점에서 가지를 멈추거나 줄일 것인가`를 기록하는 절이기 때문입니다. 같은 정확도나 비슷한 평균 점수대처럼 보여도, 깊어진 트리가 어떤 사례를 새로 외우고 어떤 실패를 그대로 남기는지는 따로 읽어야 합니다.

| 같이 남길 기록 | 왜 필요한가 |
| --- | --- |
| 깊이 또는 leaf 크기 변화 | 복잡도 손잡이가 어떻게 바뀌었는지 보기 위해서입니다. |
| train/test 차이 | 외우기와 일반화를 구분하기 위해서입니다. |
| 계속 남는 실패 사례 | 가지를 더 만들어도 해결되지 않는 사례를 다시 보기 위해서입니다. |
| 다음 가지치기 질문 | `max_depth`, `min_samples_leaf`, `ccp_alpha` 중 무엇을 조정할지 정하기 위해서입니다. |

### 언제 트리 과적합을 먼저 의심해야 하는가

트리는 성능 숫자보다 `질문이 지나치게 세밀해졌는가`를 함께 보아야 과적합을 빨리 잡을 수 있습니다.

| 보이는 신호 | 먼저 의심할 것 | 이유 |
| --- | --- | --- |
| train은 거의 완벽한데 test가 떨어진다 | 깊이 과도 | 훈련 데이터를 외우기 시작했을 수 있기 때문 |
| leaf 하나에 샘플이 거의 없다 | leaf 과소화 | 예외 사례를 패턴처럼 말할 수 있기 때문 |
| 가지가 늘어도 같은 실패 사례가 남는다 | 잘못된 복잡도 증가 | 질문 수만 늘고 본질 문제는 안 풀리고 있기 때문 |
| 첫 분기 이후 뒤쪽 분기가 지나치게 많다 | 후반부 미세 분할 | 뒤쪽 가지가 우연한 흔들림을 따라갈 수 있기 때문 |
| 설명은 길어졌는데 해석은 오히려 어려워졌다 | pruning 필요 | 읽기 쉬움이라는 장점이 사라지고 있기 때문 |

이 표는 트리 과적합을 `깊어지면 위험하다` 수준에서 멈추지 않고, `어디서부터 질문이 패턴이 아니라 예외를 말하기 시작하는가`로 읽게 해 줍니다.

## 주요 학습내용

### 작은 트리와 큰 트리를 비교하는 직관

예를 들어 고객 이탈 데이터를 다시 생각합니다.

| 트리 상태 | 직관 |
| --- | --- |
| 얕은 트리 | 큰 경향만 본다 |
| 적당한 깊이의 트리 | 중요한 패턴과 예외를 균형 있게 본다 |
| 지나치게 깊은 트리 | 훈련 데이터의 우연한 흔들림까지 따라간다 |

같은 내용을 더 짧게 그리면 다음과 같습니다.

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-01-ko.mmd"
```

이 도식은 트리의 과적합이 `질문을 더 많이 만들수록 무조건 좋아진다`가 아니라는 점을 보여 줍니다. 분기가 늘어나면 훈련 데이터에는 더 잘 맞을 수 있지만, 그 마지막 단계에서 일반화가 아니라 외우기가 시작될 수 있습니다.

핵심은 마지막 화살표입니다.

`더 잘 맞춘다`와 `더 잘 일반화한다`는 같은 말이 아닙니다.

프로젝트 메모 형식으로 줄이면 다음처럼 적을 수 있습니다.

| 기록 항목 | 예 |
| --- | --- |
| 복잡도 변화 | `max_depth 3 -> 5` |
| train 변화 | `0.971 -> 1.000` |
| test 변화 | `0.933 -> 0.911` |
| review 필요 여부 | `깊이는 늘었지만 실패 사례는 남음` |
| 다음 질문 | `leaf를 키우거나 pruning을 할 것인가` |

이 표가 있으면 과적합 절이 `복잡도 변화 -> 남는 실패 -> 다음 가지치기 질문` 구조로 읽힙니다. 결국 중요한 것은 숫자 한 칸보다 `남는 실패 패턴이 더 단순해졌는가, 아니면 단지 훈련 데이터에만 더 맞아졌는가`를 같이 보는 일입니다.

### 깊어질수록 무슨 일이 생기는가

트리가 깊어질수록 각 leaf에는 더 적은 수의 샘플이 남습니다. 그러면 다음과 같은 일이 벌어집니다.

1. 한두 개의 예외 사례가 분기를 새로 만들 수 있습니다.
2. leaf 하나가 아주 적은 샘플만 보고 예측을 내릴 수 있습니다.
3. train 데이터에서는 거의 틀리지 않게 될 수 있습니다.
4. 하지만 test 데이터에서는 작은 흔들림에도 예측이 쉽게 바뀔 수 있습니다.

scikit-learn 문서는 트리의 레벨이 하나 늘어날 때마다 트리를 채워야 하는 샘플 수가 두 배로 늘어난다고 설명하며, `max_depth`로 크기를 제어하라고 권합니다. 또 `min_samples_split`과 `min_samples_leaf`를 사용해 모든 결정이 여러 샘플의 정보를 바탕으로 이루어지게 하라고 권합니다.

이 설명을 짧게 바꾸면 다음과 같습니다.

`트리가 깊어질수록 더 자세해지지만, 그 자세함을 떠받칠 데이터가 충분하지 않으면 트리는 똑똑해지는 것이 아니라 예민해질 수 있다.`

### 과적합을 데이터 흐름으로 보기

과적합을 수식보다 흐름으로 이해하면 더 오래 갑니다.

앞쪽 분기는 종종 의미 있는 큰 경향을 잡습니다. 문제는 뒤로 갈수록 생깁니다. 마지막 몇 단계는 `진짜 구조`가 아니라 `훈련 데이터에서만 보인 우연한 흔들림`을 설명하게 될 수 있습니다.

이 흐름을 단계로 나누면 다음처럼 읽을 수 있습니다.

| 흐름 단계 | 트리가 주로 하는 일 | 먼저 떠올릴 질문 |
| --- | --- | --- |
| 앞쪽 분기 | 큰 패턴을 나눈다 | 정말 중요한 차이를 잡고 있는가? |
| 중간 분기 | 예외와 하위 패턴을 더 본다 | 아직 반복되는 구조를 보고 있는가? |
| 뒤쪽 분기 | 소수 사례를 따로 떼기 시작한다 | 이제는 우연한 흔들림을 외우는가? |
| 마지막 leaf | 거의 훈련 데이터 전용 규칙이 될 수 있다 | 새 데이터에서도 이 leaf가 살아남을까? |

예를 들어 앞쪽에서는 `온도가 높고 진동이 큰가`, `접속 감소와 불만 신호가 같이 있는가`처럼 비교적 큰 기준이 작동할 수 있습니다. 그런데 뒤쪽으로 갈수록 `셋째 시점에만 값이 살짝 흔들렸는가`, `특정 주차에만 접속이 두 번 줄었는가` 같은 좁은 질문이 붙기 쉽습니다.

이때 중요한 것은 `질문이 많아졌다`는 사실 자체가 아니라, `질문의 성격이 큰 패턴 설명에서 훈련 데이터 예외 설명으로 바뀌기 시작했는가`입니다.

즉, 과적합을 데이터 흐름으로 본다는 것은 다음 이동을 읽는 일에 가깝습니다.

- 앞쪽: 많은 샘플이 함께 움직이는 큰 경향
- 뒤쪽: 점점 더 적은 샘플만 설명하는 잔질문
- 마지막: train 점수는 오르지만 test에서 반복되지 않을 수 있는 leaf

그래서 트리를 읽을 때는 `분기가 늘었는가`만 보는 것이 아니라, `뒤쪽 분기가 아직 구조를 설명하는가, 아니면 소수 사례를 따로 외우는가`를 같이 봐야 합니다.

### train 성능과 test 성능을 함께 봐야 하는 이유

트리의 과적합은 train 성능과 test 성능을 같이 보면 특히 잘 드러납니다.

| 관찰 | 해석 |
| --- | --- |
| train과 test가 둘 다 낮다 | 아직 단순해서 충분히 배우지 못했을 수 있다 |
| train과 test가 함께 높다 | 현재는 균형이 괜찮아 보인다 |
| train만 아주 높고 test가 떨어진다 | 과적합을 의심해야 한다 |

이 관점은 결정트리에서 특히 자주 보이지만, 사실 Part 4 전체의 공통 원리이기도 합니다. 선형회귀, 로지스틱 회귀, SVM, 트리 모델 모두 결국 `보지 못한 데이터에서 어떻게 버티는가`가 더 중요합니다.

## 세부 학습내용

### `min_samples_leaf`는 왜 필요한가

`max_depth`가 트리 전체의 높이를 제한하는 손잡이라면, `min_samples_leaf`는 leaf 하나가 너무 작아지는 것을 막는 손잡이입니다.

API 문서는 `min_samples_leaf`를 leaf node에 들어가야 하는 최소 샘플 수로 설명합니다. 또 이 값이 회귀(regression)에서는 모델을 더 부드럽게(smoothing) 만드는 효과를 줄 수 있다고 설명합니다.

`leaf 하나가 한두 개 사례만 품게 두면, 그 leaf는 패턴보다 예외를 말할 가능성이 커진다.`

예를 들어:

- `min_samples_leaf=1`: 한 개 사례만 남는 leaf도 허용
- `min_samples_leaf=5`: 적어도 다섯 사례는 있어야 leaf로 인정

이 차이는 `얼마나 작은 예외를 믿을 것인가`의 차이로 읽을 수 있습니다.

### Python 예제로 leaf 크기 제어 보기

이번에는 깊이를 고정하지 않고 leaf 크기만 바꾸어 봅니다.

문제 상황:

- 같은 데이터에서 leaf를 얼마나 작게 허용할지 바꾸면 train과 test의 읽는 방식이 달라질 수 있다

입력(input):

- iris 데이터셋의 `X_train`, `X_test`, `y_train`, `y_test`
- 여러 `leaf_size`

기대 출력(output):

- leaf 크기별 train score
- leaf 크기별 test score

확인할 개념:

- leaf가 너무 작으면 train 점수는 높아지기 쉽다
- leaf 크기를 키우면 구조가 덜 예민해질 수 있다

```python
# min_samples_leaf를 바꾸며 작은 leaf 제한이 train/test 점수와 트리 구조에 미치는 영향을 보는 예제입니다.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for leaf_size in [1, 2, 5, 10]:
    model = DecisionTreeClassifier(
        min_samples_leaf=leaf_size,
        random_state=42
    )
    model.fit(X_train, y_train)

    print(f"min_samples_leaf={leaf_size}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(model.score(X_train, y_train), 3))
    print("  test accuracy  :", round(model.score(X_test, y_test), 3))
    print()
```

실행 결과 예시는 다음과 같습니다.

```text
min_samples_leaf=1
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911

min_samples_leaf=2
  depth          : 4
  leaves         : 7
  train accuracy : 0.981
  test accuracy  : 0.933

min_samples_leaf=5
  depth          : 3
  leaves         : 4
  train accuracy : 0.971
  test accuracy  : 0.933

min_samples_leaf=10
  depth          : 2
  leaves         : 3
  train accuracy : 0.952
  test accuracy  : 0.889
```

이 예제는 중요한 감각 하나를 줍니다.

`작은 leaf를 막는다고 해서 무조건 성능이 나빠지는 것은 아니다. 오히려 test 쪽이 더 안정되는 경우가 있다.`

### pruning은 무엇을 하는가

깊이를 미리 막는 방법을 `pre-pruning`처럼 읽을 수 있다면, 이미 자란 트리를 다시 단순하게 줄이는 방법은 `pruning`이라고 읽을 수 있습니다.

scikit-learn은 `Minimal Cost-Complexity Pruning`을 지원하며, API 문서에서는 `ccp_alpha`를 그 pruning의 복잡도 파라미터로 설명합니다. 값이 커질수록 더 많은 노드가 잘려 나갈 수 있습니다.

- `max_depth`, `min_samples_leaf`: 처음부터 너무 복잡해지지 않게 막는다.
- `ccp_alpha`: 자란 뒤에 복잡도를 벌점처럼 주어 줄인다.

즉, 둘 다 목적은 같습니다.

`훈련 데이터를 외우기보다, 새 데이터에서도 버틸 구조를 남기려는 것`

여기서 초심자가 먼저 잡아야 할 차이는 `언제 멈추는가`입니다.

| 방식 | 언제 개입하는가 | 먼저 읽을 뜻 |
| --- | --- | --- |
| `max_depth`, `min_samples_leaf` | 트리가 자라는 도중 | 처음부터 너무 세밀한 분기를 막는다 |
| pruning, `ccp_alpha` | 일단 자란 뒤 | 효과가 약한 잔가지를 다시 줄인다 |

즉, pre-pruning은 `애초에 너무 깊게 자라지 않게 막는 손잡이`이고, pruning은 `한번 자란 트리에서 남길 가지와 버릴 가지를 다시 고르는 손잡이`입니다.

작은 장면으로 보면 더 분명합니다.

| 가지 상태 | pruning 전 | pruning 후 |
| --- | --- | --- |
| 앞쪽 큰 분기 | 유지 | 대체로 유지 |
| 소수 사례만 설명하는 leaf | 남아 있을 수 있음 | 잘려 나갈 수 있음 |
| train 점수 | 더 높아 보일 수 있음 | 약간 내려갈 수 있음 |
| test 안정성 | 흔들릴 수 있음 | 더 안정될 수 있음 |

이 표의 핵심은 pruning이 `트리를 망가뜨리는 일`이 아니라, `큰 구조는 남기고 잔질문만 덜어 내는 일`로 읽혀야 한다는 점입니다.

예를 들어 뒤쪽 가지 하나가 `온도는 높고`, `진동은 크고`, `셋째 시점 압력만 특정 범위였는가` 같은 아주 좁은 조건으로 leaf를 하나 더 만든다고 해 보겠습니다. 이 leaf가 훈련 데이터의 두 제품만 겨우 설명하고 있다면, pruning은 바로 이런 가지를 `남겨 둘 가치가 큰가`라는 질문으로 다시 보게 합니다.

그래서 `ccp_alpha`는 단순히 숫자를 하나 더 붙이는 옵션이 아니라, `이 작은 가지가 train 점수를 올리는 이익이 복잡도를 늘리는 비용보다 큰가`를 다시 묻게 하는 손잡이입니다.

방향만 먼저 읽으면 다음처럼 기억하면 됩니다.

- `ccp_alpha`가 아주 작으면 더 많은 가지를 남기기 쉽습니다.
- `ccp_alpha`가 커질수록 작은 가지를 더 적극적으로 자르기 쉽습니다.
- 너무 작으면 외우기 쪽으로 기울 수 있고, 너무 크면 중요한 패턴도 함께 잘릴 수 있습니다.

### pruning을 흐름으로 보기

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-02-ko.mmd"
```

이 절에서는 pruning 공식을 계산하지 않습니다. 대신 `어떤 잔가지를 남기지 않을 것인가`, `왜 train 점수를 조금 포기하고 test 안정성을 얻으려 하는가`를 중심으로 읽습니다.

## 사례 및 예시

### 사례 1. 불량 탐지 트리가 공장 데이터의 예외까지 외워 버릴 때

제조 팀이 센서 값으로 제품 불량 여부를 가르는 결정트리를 만들고 있습니다. 사람이 먼저 보던 기준은 `온도가 기준보다 높은가`, `진동이 특정 범위를 넘는가`, `압력 변화가 급격한가` 같은 질문들이었습니다.

질문을 많이 만들수록 모델이 똑똑해지는 것처럼 보일 수 있습니다. 실제로 트리를 깊게 두면 훈련 데이터에서는 거의 틀리지 않게 될 수 있습니다. 하지만 뒤쪽 가지를 보면 한두 개의 예외 사례만 설명하는 leaf가 생기고, 그 leaf는 공정이 조금만 달라져도 새 데이터에서 쉽게 흔들립니다.

작은 장면으로 바꾸면 다음처럼 볼 수 있습니다.

| 제품 | 온도 | 진동 | 압력 변화 | 사람이 먼저 보는 판단 |
| --- | --- | --- | --- | --- |
| A | 높음 | 큼 | 급격함 | 불량 review 우선순위 높음 |
| B | 보통 | 작음 | 안정적 | 정상 가능성 높음 |
| C | 높음 | 보통 | 약간 큼 | review 후보 |
| D | 약간 높음 | 아주 짧게 큼 | 안정적 | 바로 불량으로 단정하기 어려움 |

여기서 사람이 먼저 보는 기준은 `온도 상승 + 진동/압력 이상`처럼 비교적 큰 패턴입니다. 그런데 지나치게 깊은 트리는 `셋째 측정 시점에서만 진동이 잠깐 올랐는가`, `압력 변화가 특정 범위 안에서 두 번 꺾였는가` 같은 잔질문을 더 붙여, 훈련 데이터에서 D와 비슷했던 소수 제품 몇 개만 따로 설명하려고 할 수 있습니다.

| 사람이 먼저 보던 기준 | 지나치게 깊어진 트리가 붙잡기 쉬운 것 |
| --- | --- |
| 온도와 진동 이상이 함께 보이는가 | 특정 시점의 짧은 흔들림 |
| 압력 변화가 공정 이상으로 읽히는가 | 훈련 데이터의 드문 센서 조합 |
| review 대상으로 먼저 볼 만한가 | 한두 개 제품만 맞추는 세밀한 분기 |

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-03-ko.mmd"
```

같은 장면을 `비교적 단순한 읽기`와 `지나치게 깊은 읽기`로 나누면 차이가 더 잘 보입니다.

| 읽는 방식 | 제품 D를 어떻게 보나 |
| --- | --- |
| 비교적 단순한 트리 | 온도는 약간 높지만 압력은 안정적이어서 review 후보 정도로 남김 |
| 지나치게 깊은 트리 | 특정 시점의 진동 흔들림과 드문 센서 조합을 붙여 별도 leaf로 분리 |

이 장면에서 트리의 과적합은 `질문을 너무 세밀하게 늘려 훈련 데이터를 외우는 현상`으로 읽어야 합니다. `max_depth`는 트리가 어디까지 자랄지 막고, `min_samples_leaf`는 leaf가 너무 작은 예외 집합이 되지 않게 막으며, `ccp_alpha`는 이미 자란 가지를 다시 줄이는 역할을 합니다. 즉, 더 많은 질문이 항상 더 좋은 설명을 뜻하지는 않습니다.

확인 가능한 결과는 train accuracy와 test accuracy를 함께 볼 때 드러납니다. train 점수는 계속 오르는데 test 점수가 어느 지점 이후 떨어지거나 정체한다면, 그 이후 분기는 일반화가 아니라 외우기에 가까웠다는 신호로 읽어야 합니다. 결국 중요한 질문은 `센서 이상을 더 잘 설명했는가`가 아니라 `새 공정 데이터에서도 반복될 기준을 더 선명하게 만들었는가`입니다.

### 사례 2. 고객 이탈 트리가 review 기준보다 예외 고객을 더 자세히 외우기 시작할 때

구독 서비스 팀이 고객 이탈 여부를 예측하는 결정트리를 만들고 있다고 해 보겠습니다. 사람이 먼저 보던 기준은 `최근 접속이 급감했는가`, `결제 실패가 있었는가`, `고객센터 문의 뒤 불만 신호가 있었는가` 같은 비교적 큰 흐름이었습니다.

그런데 트리를 계속 깊게 키우면 뒤쪽 가지에서 `최근 17일 동안 접속이 2회였고`, `지난달 결제 금액이 특정 범위였고`, `프로모션 메일을 한 번 열었는가`처럼 훈련 데이터 안의 소수 고객만 설명하는 조합이 늘어날 수 있습니다. 훈련 데이터에서는 이런 조합이 매우 잘 맞아 보일 수 있지만, 실제 운영에서는 같은 조합이 다시 나오지 않거나 의미가 약할 수 있습니다.

작은 장면으로 바꾸면 다음처럼 볼 수 있습니다.

| 고객 | 최근 접속 변화 | 결제 실패 | 불만 신호 | 사람이 먼저 보는 판단 |
| --- | --- | --- | --- | --- |
| A | 크게 감소 | 있음 | 있음 | review 우선순위 높음 |
| B | 조금 감소 | 없음 | 없음 | 바로 이탈로 보기 어려움 |
| C | 크게 감소 | 없음 | 있음 | review 후보 |
| D | 거의 변화 없음 | 없음 | 없음 | 유지 가능성 높음 |

여기서 사람이 먼저 보는 기준은 `접속 감소 + 결제/불만 신호`처럼 비교적 큰 패턴입니다. 그런데 지나치게 깊은 트리는 `지난 3주 중 둘째 주만 접속이 0회였는가`, `이벤트 메일을 수요일 오전에 열었는가` 같은 잔질문을 더 붙여, 훈련 데이터에서 C와 비슷했던 소수 고객 몇 명만 따로 설명하려고 할 수 있습니다.

| 사람이 먼저 보던 기준 | 지나치게 깊어진 트리가 붙잡기 쉬운 것 |
| --- | --- |
| 접속 감소가 뚜렷한가 | 특정 주차의 작은 흔들림 |
| 결제 문제와 불만 신호가 같이 있었는가 | 훈련 데이터의 소수 고객 조합 |
| review 대상으로 먼저 볼 만한가 | leaf 하나만 맞추는 세밀한 분기 |

같은 장면을 `얕은 읽기`와 `지나치게 깊은 읽기`로 나누면 차이가 더 잘 보입니다.

| 읽는 방식 | 고객 C를 어떻게 보나 |
| --- | --- |
| 비교적 단순한 트리 | 접속 감소와 불만 신호가 있어 review 후보로 올림 |
| 지나치게 깊은 트리 | 훈련 데이터의 특정 주차 패턴, 금액 범위, 메일 반응까지 붙여 별도 leaf로 분리 |

이 장면에서 과적합은 `설명력이 높아 보이는 잔질문`이 실제로는 review 기준을 더 선명하게 만드는 것이 아니라, 훈련 데이터의 우연한 조합을 더 정교하게 외우는 현상으로 읽어야 합니다. 그래서 트리를 볼 때는 `설명이 자세해졌는가`만이 아니라 `그 자세함이 새 고객에서도 반복될 만한가`, `review 우선순위를 더 잘 세우는가`를 같이 물어야 합니다.

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-04-ko.mmd"
```

같은 장면을 점수표가 아니라 leaf 장면으로 다시 읽으면, 과적합을 더 빨리 알아차릴 수 있습니다.

| leaf를 볼 때 먼저 볼 것 | 과적합 신호처럼 읽히는 장면 |
| --- | --- |
| leaf 안 샘플 수 | 한두 건만 남은 leaf가 많아진다 |
| leaf를 만든 질문의 성격 | 큰 패턴보다 특정 주차, 특정 시점, 특정 조합 같은 잔질문이 늘어난다 |
| leaf의 실무 의미 | review 기준이 선명해지기보다 훈련 데이터 사례 메모처럼 보인다 |

이 표를 붙잡으면 `train accuracy가 올랐다`는 사실만으로 트리를 좋게 보지 않게 됩니다. 초심자 기준에서는 `이 leaf가 새 고객을 설명하는가, 아니면 훈련 데이터의 소수 고객을 따로 외우는가`를 한 번 더 문장으로 물어 보는 습관이 중요합니다.

### 실무에서 어떤 손잡이를 보아야 하는가

입문자와 실무 초반에는 모든 값을 한 번에 건드리기보다 역할별로 나누어 보는 편이 낫습니다.

| 손잡이 | 먼저 읽는 질문 |
| --- | --- |
| `max_depth` | 트리가 어디까지 깊어지게 둘 것인가? |
| `min_samples_split` | 이 node를 더 나눌 만큼 샘플이 충분한가? |
| `min_samples_leaf` | leaf 하나가 너무 작아지지 않게 할 것인가? |
| `ccp_alpha` | 이미 자란 가지를 얼마나 줄일 것인가? |

실무 감각으로 바꾸면 다음과 같습니다.

- 설명이 너무 길고 복잡하게 느껴진다 -> `max_depth` 확인
- 소수 사례만 설명하는 leaf가 많아 보인다 -> `min_samples_leaf` 확인
- 가지가 지나치게 많고 잔가지가 많다 -> `ccp_alpha` 검토

## 연습 및 예제

### Python 예제로 깊이에 따른 과적합 보기

이번 예제는 같은 결정트리 분류기에서 깊이만 바꾸어 train/test 결과가 어떻게 갈라지는지 보는 실습입니다.

- 문제 상황: iris 데이터셋으로 품종 분류를 한다.
- 입력(input): 꽃받침, 꽃잎 길이와 너비
- 정답(label): 세 가지 품종
- 확인할 개념:
  - 깊이가 커질수록 train 성능은 쉽게 올라갈 수 있다.
  - test 성능은 어느 지점 이후 정체하거나 떨어질 수 있다.
  - 트리 깊이는 복잡도 손잡이 중 하나다.

입력과 출력에서 무엇을 비교할지 먼저 표로 잡으면 다음과 같습니다.

| 비교할 값 | 왜 같이 보나 |
| --- | --- |
| `max_depth` | 트리가 어디까지 자라는지 보기 위해서입니다. |
| `leaves` | 깊이가 실제로 얼마나 많은 끝노드를 만들었는지 보기 위해서입니다. |
| train accuracy | 훈련 데이터 적합 정도를 보기 위해서입니다. |
| test accuracy | 새 데이터 일반화 정도를 보기 위해서입니다. |
| `train - test` 차이 | 외우기와 일반화 차이가 얼마나 벌어지는지 보기 위해서입니다. |

```python
# max_depth를 바꾸며 트리 깊이와 train-test gap이 과적합 신호로 어떻게 보이는지 확인하는 예제입니다.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for depth in [1, 2, 3, 5, None]:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"max_depth={depth}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(train_score, 3))
    print("  test accuracy  :", round(test_score, 3))
    print("  train-test gap :", round(train_score - test_score, 3))
    print()
```

실행 결과 예시는 다음과 같습니다.

```text
max_depth=1
  depth          : 1
  leaves         : 2
  train accuracy : 0.667
  test accuracy  : 0.667
  train-test gap : 0.0

max_depth=2
  depth          : 2
  leaves         : 3
  train accuracy : 0.952
  test accuracy  : 0.889
  train-test gap : 0.063

max_depth=3
  depth          : 3
  leaves         : 5
  train accuracy : 0.981
  test accuracy  : 0.933
  train-test gap : 0.048

max_depth=5
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089

max_depth=None
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089
```

이 결과에서 읽어야 할 것은 다음입니다.

1. 깊이를 늘리면 train accuracy는 계속 좋아지기 쉽습니다.
2. 하지만 test accuracy는 어느 지점 이후 더 좋아지지 않을 수 있습니다.
3. `train-test gap`이 커질수록 외우기 신호가 강해질 수 있습니다.
4. `max_depth=3` 부근이 현재 예제에서는 더 균형 있어 보입니다.

즉, 트리의 성능을 볼 때는 `깊어졌는가`보다 `깊어졌을 때 train/test가 어떻게 갈리는가`를 같이 봐야 합니다.

여기서 한 번 더 중요한 것은 `정확도 숫자만` 보지 않는 일입니다. `max_depth=5`와 `max_depth=3`의 차이는 단지 점수 차이만이 아니라, 더 깊은 트리가 더 많은 leaf를 만들며 train 데이터를 더 세밀하게 설명하기 시작했다는 구조 차이이기도 합니다.

짧게 다시 묶으면 다음 비교가 핵심입니다.

| 깊이 구간 | 먼저 읽을 판단 |
| --- | --- |
| 너무 얕음 | 아직 단순해서 충분히 배우지 못했는가 |
| 중간 깊이 | train과 test가 함께 좋아지는가 |
| 너무 깊음 | train만 더 좋아지고 gap이 커지는가 |

직접 값을 바꿔 보면 더 잘 보이는 질문도 있습니다.

- `max_depth=4`를 넣으면 깊이 3과 5 사이에서 어떤 변화가 생기는가
- `random_state`를 바꾸면 깊이별 gap 패턴이 어느 정도 반복되는가
- `max_depth=None`이 실제로 어느 깊이에서 멈추는가

### 값 하나 더 바꿔 보며 `depth`와 `leaf`를 같이 읽기

이번에는 깊이만 볼 때와 leaf 크기를 같이 볼 때 판단이 어떻게 달라지는지 확인합니다.

- 바꿔 볼 값: `min_samples_leaf`
- 바꾸는 이유: 같은 깊이 제한 아래에서도 작은 leaf를 막으면 예외 외우기가 줄어드는지 보기 위해서입니다.
- 확인할 개념:
  - `max_depth`와 `min_samples_leaf`는 같은 복잡도 문제를 서로 다른 위치에서 제어합니다.
  - 깊이가 같아 보여도 leaf가 더 커지면 train/test 해석이 달라질 수 있습니다.
  - 과적합 점검은 `깊이 하나`가 아니라 `깊이 + leaf 크기 + gap`을 함께 읽는 편이 안전합니다.

```python
# 같은 깊이 제한에서 min_samples_leaf까지 함께 바꾸어 leaf 크기와 gap을 같이 읽는 예제입니다.
for leaf_size in [1, 2, 5]:
    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=leaf_size,
        random_state=42,
    )
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"min_samples_leaf={leaf_size}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(train_score, 3))
    print("  test accuracy  :", round(test_score, 3))
    print("  train-test gap :", round(train_score - test_score, 3))
    print()
```

실행 결과 예시는 다음과 같습니다.

```text
min_samples_leaf=1
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089

min_samples_leaf=2
  depth          : 4
  leaves         : 7
  train accuracy : 0.981
  test accuracy  : 0.933
  train-test gap : 0.048

min_samples_leaf=5
  depth          : 3
  leaves         : 4
  train accuracy : 0.971
  test accuracy  : 0.933
  train-test gap : 0.038
```

이 비교에서 먼저 봐야 할 것은 `train accuracy가 약간 내려가도 test accuracy가 더 안정될 수 있다`는 점입니다. 즉 과적합 완화는 점수를 포기하는 패배가 아니라, `덜 외우고 더 버티게 만드는 조정`으로 읽어야 합니다.

초심자 기준에서는 아래 세 문장을 직접 적어 보면 좋습니다.

1. `max_depth=5, min_samples_leaf=1`은 어떤 면에서 가장 예민한 구조인가
2. `min_samples_leaf=2`나 `5`가 되면 무엇이 덜 예민해졌는가
3. 다음에 pruning까지 비교한다면 어떤 잔가지가 잘릴 것 같은가

### `ccp_alpha`를 바꿔 pruning 방향 읽어 보기

이제 같은 데이터에서 `이미 자란 트리`를 얼마나 줄일지 한 번 더 흔들어 봅니다.

- 바꿔 볼 값: `ccp_alpha`
- 바꾸는 이유: depth 제한과 leaf 크기 조정이 `처음부터 덜 자라게 하는 방법`이었다면, pruning은 `자란 뒤 잔가지를 줄이는 방법`이라는 차이를 직접 확인하기 위해서입니다.
- 확인할 개념:
  - `ccp_alpha`가 커질수록 작은 가지를 더 적극적으로 줄이기 쉽다.
  - train 점수는 조금 내려가도 test 쪽이 더 안정될 수 있다.
  - pruning은 `트리를 망가뜨리는 것`이 아니라 `남길 큰 구조를 다시 고르는 것`에 가깝다.

```python
# ccp_alpha를 바꾸며 pruning이 깊이, leaf 수, train/test gap을 어떻게 바꾸는지 확인하는 예제입니다.
for alpha in [0.0, 0.005, 0.02]:
    model = DecisionTreeClassifier(
        random_state=42,
        ccp_alpha=alpha,
    )
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"ccp_alpha={alpha}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(train_score, 3))
    print("  test accuracy  :", round(test_score, 3))
    print("  train-test gap :", round(train_score - test_score, 3))
    print()
```

실행 결과 예시는 다음과 같습니다.

```text
ccp_alpha=0.0
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089

ccp_alpha=0.005
  depth          : 4
  leaves         : 6
  train accuracy : 0.981
  test accuracy  : 0.933
  train-test gap : 0.048

ccp_alpha=0.02
  depth          : 2
  leaves         : 3
  train accuracy : 0.952
  test accuracy  : 0.889
  train-test gap : 0.063
```

이 결과에서 먼저 읽어야 할 것은 `조금 자르자 더 나아졌지만, 너무 많이 자르면 다시 단순해진다`는 점입니다. 즉 pruning도 `많이 할수록 좋다`가 아니라, `잔가지를 덜어 내되 큰 패턴은 남기는 균형`을 찾는 일입니다.

가능하면 여기서 아래 문장도 직접 적어 봅니다.

1. `ccp_alpha=0.005`는 어떤 작은 가지를 덜어 낸 상태처럼 읽히는가
2. `ccp_alpha=0.02`는 왜 지나치게 단순해진 후보처럼 보이는가
3. `max_depth`, `min_samples_leaf`, `ccp_alpha` 중 지금 내 데이터에서 먼저 건드릴 손잡이는 무엇인가

### 연습: 복잡도 손잡이를 기록 언어로 남기기

위 두 실험을 실행했다면, 이제 결과를 짧은 비교 기록으로 남겨 봅니다.

| 비교 항목 | depth만 바꾼 실험 | leaf 크기까지 바꾼 실험 |
| --- | --- | --- |
| 가장 균형 있어 보이는 설정 |  |  |
| 가장 예민해 보이는 설정 |  |  |
| train-test gap이 가장 크게 벌어진 설정 |  |  |
| 다음에 조정할 손잡이 |  |  |

이 표를 채울 때는 `점수가 가장 높은 설정`만 적지 말고, `왜 그 설정을 균형 있다고 읽었는가`를 한 문장으로 같이 남기는 편이 좋습니다.

가능하면 pruning 실험도 같은 방식으로 한 줄 더 적습니다.

| pruning 비교 항목 | 기록 |
| --- | --- |
| 가장 균형 있어 보이는 `ccp_alpha` |  |
| 너무 많이 잘랐다고 느껴지는 `ccp_alpha` |  |
| 다음에 함께 비교할 손잡이 |  |

예를 들면 다음처럼 적을 수 있습니다.

- `max_depth=3`은 train과 test가 함께 좋아져 기본 기준선으로 삼기 좋다.
- `max_depth=5, min_samples_leaf=1`은 train은 완벽하지만 gap이 커져 예외를 더 많이 외우는 후보처럼 보인다.
- 다음에는 `ccp_alpha`를 써서 잔가지를 줄였을 때 같은 실패가 남는지 보고 싶다.

## 체크리스트

- train 성능 상승과 test 성능 상승을 같은 말처럼 읽고 있지 않은가?
- leaf가 너무 작아져 예외 사례를 규칙처럼 말하고 있지 않은가?
- 다음 조정이 깊이 제한인지, leaf 크기 조정인지, pruning인지 구분하고 있는가?
- 트리는 읽기 쉽지만 제한이 없으면 훈련 데이터를 과하게 따라가기 쉽고, 깊이가 커지고 leaf가 작아질수록 과적합 위험이 커진다는 점을 설명할 수 있는가
- train 성능이 높아져도 test 성능이 같이 좋아진다는 보장은 없다는 점을 설명할 수 있는가
- `max_depth`, `min_samples_leaf`, `ccp_alpha`가 각각 어떤 방식으로 트리 복잡도를 제어하는지 설명할 수 있는가

## 출처와 참고 자료

- scikit-learn developers, `1.10. Decision Trees`, scikit-learn User Guide, 확인 날짜: 2026-06-27. [https://scikit-learn.org/stable/modules/tree.html](https://scikit-learn.org/stable/modules/tree.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `DecisionTreeClassifier`, scikit-learn API Reference, 확인 날짜: 2026-06-27. [https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html){: target="_blank" rel="noopener noreferrer" }
- Leo Breiman, Jerome Friedman, Richard Olshen, Charles Stone, *Classification and Regression Trees*, Routledge, 1984. 확인 날짜: 2026-07-19. [https://doi.org/10.1201/9781315139470](https://doi.org/10.1201/9781315139470){: target="_blank" rel="noopener noreferrer" }

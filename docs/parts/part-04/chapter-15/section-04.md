# P4-15.4 보충학습: Extra Trees와 랜덤포레스트 비교

> Section ID: `P4-15.4`
> Version: `v2026.07.26`

P4-15.1에서 [랜덤포레스트(random forest)](../../../reference/concept-glossary-parts/04-rieul.md#random-forest)를 배우면 비슷한 이름의 Extra Trees(Extremely Randomized Trees)도 곧 만나게 됩니다. 둘 다 `트리를 여러 개 모아 평균내는 숲`처럼 보이기 때문에, 처음에는 사실상 같은 모델 아닌가 하고 넘기기 쉽습니다.

하지만 이 둘은 `어디까지 무작위성을 넣는가`, `분기 기준을 어떻게 고르는가`, [bootstrap](../../../reference/concept-glossary-parts/06-bieup.md#bootstrap)과 [OOB](../../../reference/concept-glossary-parts/08-ieung.md#oob-score)를 기본으로 쓰는가에서 분명한 차이가 있습니다.

이 절은 랜덤포레스트의 본편 설명을 다시 반복하지 않고, Extra Trees를 처음 비교할 때 독자가 헷갈리는 지점을 보충학습으로 정리합니다.

## 보충학습: Extra Trees와 랜덤포레스트를 처음 비교하는 법에서 닫을 질문

이 절은 다음 질문에 답합니다.

- Extra Trees는 랜덤포레스트와 같은 계열인가?
- 둘 다 여러 트리를 평균내는데, 무엇이 실제로 다른가?
- [`best split`](../../../reference/concept-glossary-parts/04-rieul.md#random-forest)과 [random threshold](../../../reference/concept-glossary-parts/04-rieul.md#random-forest)의 차이는 무엇인가?
- 왜 Extra Trees는 더 무작위적이라고 설명되는가?
- [OOB(out-of-bag)](../../../reference/concept-glossary-parts/08-ieung.md#oob-score)는 랜덤포레스트와 Extra Trees에서 어떻게 다르게 읽어야 하는가?

이 절은 먼저 `랜덤포레스트와 Extra Trees를 어디서 같게 보고 어디서 다르게 읽어야 하는가`를 닫습니다. Extra Trees와 그래디언트 부스팅의 철학 차이는 P4-16.1, P4-16.2에서 다시 이어집니다.

## 보충학습: Extra Trees와 랜덤포레스트를 처음 비교하는 법에서 남길 판단 기준

- Extra Trees를 `더 강한 무작위성을 넣은 트리 앙상블`로 설명할 수 있습니다.
- 랜덤포레스트와 Extra Trees의 차이를 `샘플 추출`, `분기 임계값 선택`, `OOB 가능 조건` 기준으로 비교할 수 있습니다.
- Extra Trees가 보통 [분산(variance)](../../../reference/concept-glossary-parts/06-bieup.md#variance)을 더 줄이는 대신 [편향(bias)](../../../reference/concept-glossary-parts/13-pieup.md#bias)을 조금 더 늘릴 수 있다는 뜻을 입문 수준에서 설명할 수 있습니다.
- 언제 랜덤포레스트와 Extra Trees를 함께 비교 후보로 올리면 좋은지 말할 수 있습니다.

## 왜 이 절이 필요한가

랜덤포레스트를 이해한 직후에는 이런 오해가 생기기 쉽습니다.

- 둘 다 숲이다.
- 둘 다 feature를 무작위로 고른다.
- 그러면 이름만 다른 같은 모델 아닌가?

여기서 한 단계 더 구분해야 합니다.

| 질문 | 랜덤포레스트 | Extra Trees |
| --- | --- | --- |
| 학습 데이터 | 보통 bootstrap sample | 기본값은 전체 훈련 세트 |
| 분기 임계값 | 후보 중 가장 좋은 split 탐색 | 임계값을 무작위로 뽑고 그중 고름 |
| 무작위성 강도 | 크다 | 더 크다 |
| OOB 기본 흐름 | 자연스럽게 연결됨 | 기본값 그대로는 연결되지 않음 |

즉, Extra Trees는 `랜덤포레스트와 같은 숲 계열`이지만, `분기 기준을 고르는 방식까지 더 무작위화한 숲`으로 읽어야 합니다.

## 주요 학습내용

### Extra Trees도 같은 트리 앙상블 계열인가

scikit-learn 사용자 가이드는 random forest와 Extra-Trees를 모두 `randomized decision tree ensemble` 계열의 averaging algorithm으로 설명합니다. 즉, 두 모델 모두 트리를 여러 개 만들고, 각 트리의 예측을 평균내거나 집계해 일반화 성능과 안정성을 높이려는 계열입니다.

공통점부터 먼저 잡으면 다음과 같습니다.

- 둘 다 결정트리(decision tree)를 여러 개 사용합니다.
- 둘 다 feature 일부만 보며 분기 후보를 만듭니다.
- 둘 다 여러 트리의 예측을 평균내거나 집계합니다.
- 둘 다 단일 트리보다 흔들림을 줄이려는 목적이 큽니다.

따라서 Extra Trees를 `전혀 다른 새 가족`으로 볼 필요는 없습니다. 먼저는 `랜덤포레스트와 매우 가까운 비교 후보`라고 잡으면 충분합니다.

### 핵심 차이 1. 분기 임계값을 어떻게 고르는가

scikit-learn 사용자 가이드는 random forest가 각 노드에서 `best split`을 찾는다고 설명합니다. 반면 extremely randomized trees는 random forest처럼 feature 부분집합을 보되, 각 feature에 대해 분기 threshold를 무작위로 뽑고 그중 가장 좋은 것을 고른다고 설명합니다.

이 차이를 초심자 기준으로 바꾸면 다음과 같습니다.

- 랜덤포레스트: `이번 노드에서 어디를 자르는 게 가장 좋을까?`를 더 많이 탐색한다.
- Extra Trees: `몇 개를 무작위로 잘라 보고, 그중 덜 나쁜 쪽을 쓰자.`에 가깝다.

즉, Extra Trees는 feature 선택만 무작위인 것이 아니라, `어디에서 자를지`도 더 무작위적입니다.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-4-mermaid-01-ko.mmd"
```

이 도식의 핵심은 두 모델 모두 feature 부분집합은 공유하지만, threshold를 고르는 태도는 다르다는 점입니다.

### 핵심 차이 2. bootstrap 기본값이 다르다

scikit-learn 사용자 가이드는 random forest의 기본값이 `bootstrap=True`이고, Extra Trees의 기본값은 `bootstrap=False`라고 설명합니다. Extra Trees API 문서도 `bootstrap=False`일 때 각 트리가 전체 데이터셋으로 학습된다고 설명합니다.

이 차이는 생각보다 중요합니다.

| 항목 | 랜덤포레스트 기본값 | Extra Trees 기본값 |
| --- | --- | --- |
| `bootstrap` | `True` | `False` |
| 각 트리 입력 | 복원추출한 샘플 | 전체 훈련 세트 |
| OOB 가능 여부 | 기본 흐름에서 자연스럽다 | 기본값 그대로는 불가능하다 |

즉, Extra Trees는 `더 무작위적인 숲`이지만, 그 무작위성이 반드시 `샘플을 다르게 뽑는다`에서 오는 것은 아닙니다. 기본값에서는 `분기 threshold 무작위화`가 핵심이고, 샘플은 전체 훈련 세트를 그대로 씁니다.

### 핵심 차이 3. OOB는 두 모델에서 같은 기본 손잡이가 아니다

P4-15.3에서 본 것처럼 OOB는 `bootstrap으로 빠진 샘플`이 있어야 성립합니다. scikit-learn API 문서는 random forest와 Extra Trees 모두 `oob_score`는 `bootstrap=True`일 때만 사용할 수 있다고 설명합니다.

따라서:

- 랜덤포레스트는 기본값이 `bootstrap=True`라서 OOB가 자연스럽게 이어집니다.
- Extra Trees는 기본값이 `bootstrap=False`라서, 기본 설정 그대로는 OOB를 점검 손잡이로 쓸 수 없습니다.

이 차이를 모르고 `왜 Extra Trees에는 OOB가 안 보이지?`라고 당황하는 경우가 많습니다. 모델이 다른 것이 아니라, 기본 샘플링 전략이 다르기 때문입니다.

### Extra Trees는 왜 더 무작위적인데도 후보가 되는가

scikit-learn 사용자 가이드는 extremely randomized trees가 split 계산 단계의 무작위성을 더 키워, 분산을 조금 더 줄이는 대신 편향을 약간 더 늘릴 수 있다고 설명합니다.

이를 짧게 바꾸면:

`한 트리 한 그루는 조금 덜 정교해질 수 있지만, 숲 전체는 더 덜 닮은 트리들로 구성될 수 있다.`

즉, Extra Trees는 `트리 한 그루의 정밀한 분기 탐색`을 조금 포기하는 대신, `숲 전체 다양성`을 더 키우려는 방향으로 읽으면 됩니다.

| 관점 | 랜덤포레스트 | Extra Trees |
| --- | --- | --- |
| 한 트리의 split 탐색 | 더 신중하다 | 더 거칠다 |
| 숲 전체 다양성 | 크다 | 더 커질 수 있다 |
| 기대 효과 | 안정성 향상 | 안정성 향상 + 추가 분산 감소 가능성 |
| 함께 생길 수 있는 대가 | 계산 비용 | 약간 더 큰 bias |

이 표를 읽을 때 중요한 것은 `무조건 Extra Trees가 더 좋다`가 아니라, `무작위성 주입 위치가 다르다`는 점입니다.

### 언제 Extra Trees를 같이 비교하면 좋은가

Extra Trees는 랜덤포레스트와 같은 후보군 안에서 `조금 더 빠르고, 조금 더 무작위적인 숲`이 필요할 때 같이 시험해 볼 가치가 있습니다.

| 현재 상황 | Extra Trees를 같이 올릴 이유 | 같이 확인할 점 |
| --- | --- | --- |
| 랜덤포레스트는 알겠는데 비교 후보가 하나 더 필요하다 | 매우 가까운 트리 앙상블 비교축이 되기 때문 | test 기준으로 실제 차이가 나는지 |
| 깊은 트리 탐색 비용이 부담된다 | split 탐색이 더 단순해질 수 있기 때문 | 속도 이점이 실제로 체감되는지 |
| 단일 트리 흔들림을 더 강하게 줄이고 싶다 | 분기 단계 무작위성이 더 크기 때문 | bias 증가로 test가 떨어지지 않는지 |
| OOB보다 train/test 비교 중심으로 보고 있다 | 기본값이 `bootstrap=False`라 OOB 의존이 약하기 때문 | 별도 validation 또는 test 관리 |
| feature importance, 예측 안정성, 계산 시간까지 같이 본다 | 랜덤포레스트와 나란히 비교하기 좋은 형제 모델이기 때문 | 중요도 해석을 과신하지 않는지 |

이 표의 목적은 Extra Trees를 무조건 추가하라는 것이 아니라, `랜덤포레스트 바로 옆에서 시험해 볼 비교 후보`로 올바르게 위치시키는 데 있습니다.

## 사례 및 예시

### 사례 1. 고객 이탈 문제에서 두 숲을 어떻게 다르게 읽을까

고객 이탈(churn) 예측에서 팀이 먼저 랜덤포레스트를 써 보니 test 성능은 무난하지만, `이 숲이 분기를 너무 세밀하게 맞추는가`, `조금 더 거친 무작위화가 오히려 안정성을 높일까`라는 질문이 남습니다.

이때 Extra Trees를 같이 올리는 이유는 `전혀 다른 철학의 모델`이 필요해서가 아닙니다. 같은 트리 앙상블 안에서 `분기 탐색을 더 무작위화하면 결과가 어떻게 달라지는지` 보기 위해서입니다.

예를 들어:

- 랜덤포레스트는 `최근 접속 수 < 3.5`, `결제 실패 횟수 < 1.5`처럼 더 좋은 threshold를 탐색합니다.
- Extra Trees는 threshold 후보를 더 무작위로 뽑고, 그중 덜 나쁜 분기를 고릅니다.

팀이 검토 중인 고객 표를 아주 작게 줄이면 다음처럼 생각할 수 있습니다.

| 고객 | 최근 접속 수 | 결제 실패 횟수 | 상담 횟수 | 실제 이탈 |
| --- | ---: | ---: | ---: | --- |
| A | 1 | 2 | 4 | 예 |
| B | 2 | 1 | 3 | 예 |
| C | 5 | 0 | 1 | 아니오 |
| D | 6 | 0 | 0 | 아니오 |

이 표를 볼 때 랜덤포레스트는 `접속 수 2와 5 사이 어디를 자르는가`, `결제 실패 0과 1 사이 어디가 가장 좋은가`를 더 열심히 찾는 쪽에 가깝습니다. 반면 Extra Trees는 몇 개의 자름 후보를 더 무작위로 골라 보고, 그중 덜 나쁜 쪽을 쓰는 감각에 가깝습니다.

그래서 두 모델을 비교할 때 질문도 조금 달라집니다.

| 비교 질문 | 랜덤포레스트에서 더 먼저 보는 점 | Extra Trees에서 더 먼저 보는 점 |
| --- | --- | --- |
| 왜 맞췄나 | 더 정교한 split 탐색이 도움이 되었는가 | 더 거친 무작위화가 오히려 일반화에 도움이 되었는가 |
| 왜 틀렸나 | 세밀한 threshold가 예외 고객에 끌렸는가 | 거친 threshold 때문에 중요한 경계가 흐려졌는가 |
| 다음 조정은 무엇인가 | `max_features`, depth, leaf 크기 | `max_features`, depth, 필요시 `bootstrap` |

따라서 실험 메모에는 `둘 다 숲`이라고만 적지 않고 다음을 같이 남겨야 합니다.

- test 점수 차이
- train과 test 간격
- 중요도 순위가 크게 바뀌는지
- 계산 시간 차이

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-4-mermaid-02-ko.mmd"
```

이 흐름에서 중요한 것은 `누가 이겼는가` 하나보다, `무작위성 위치를 바꾸면 성능, 흔들림, 계산 비용이 어떻게 달라지는가`를 함께 보는 일입니다.

### 사례 2. 불량 탐지에서 Extra Trees를 왜 같이 돌려 볼까

공장 불량 탐지 문제에서는 센서 값이 많고, 일부 경계는 매우 미세하게 갈라질 수 있습니다. 팀이 랜덤포레스트를 먼저 써 보니 train 성능은 매우 높지만, test에서는 특정 생산일의 예외 패턴에 따라 흔들리는 모습이 보입니다.

이때 Extra Trees를 같이 돌려 보는 이유는 `더 고급 모델`이기 때문이 아니라, `분기 threshold를 덜 집요하게 찾으면 오히려 특정 날짜의 우연한 경계에 덜 매달릴까`를 보기 위해서입니다.

예를 들어 센서 기록을 아주 작게 줄이면 다음처럼 볼 수 있습니다.

| 배치 | 온도 편차 | 진동 편차 | 압력 편차 | 실제 불량 |
| --- | ---: | ---: | ---: | --- |
| A | 0.8 | 0.9 | 0.3 | 예 |
| B | 0.7 | 0.8 | 0.4 | 예 |
| C | 0.2 | 0.3 | 0.2 | 아니오 |
| D | 0.3 | 0.2 | 0.1 | 아니오 |

랜덤포레스트는 `진동 편차 0.82` 같은 더 세밀한 자름점을 찾으려 할 수 있습니다. 이런 탐색은 도움이 될 때도 있지만, 데이터가 작거나 특정 날짜 잡음이 끼어 있으면 그 잡음까지 경계처럼 읽을 수 있습니다. Extra Trees는 threshold를 더 무작위로 잡기 때문에, 한 트리 한 그루는 덜 정교해 보여도 숲 전체가 특정 예외 날짜 패턴을 덜 닮게 될 수 있습니다.

이 장면에서는 다음을 같이 적어 두면 비교가 쉬워집니다.

- 랜덤포레스트가 높인 train 점수가 test에서도 유지되는가
- Extra Trees가 test를 약간 높이거나 비슷하게 유지하면서 흔들림을 줄이는가
- 중요도 상위 센서가 두 모델에서 비슷한가
- 계산 시간이 실제로 차이 나는가

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-4-mermaid-03-ko.mmd"
```

이 사례의 핵심은 Extra Trees가 `항상 더 잘 맞는다`가 아니라, `세밀한 threshold 탐색이 오히려 예외 패턴에 민감할 때 바로 옆 비교 후보가 된다`는 점입니다.

## 연습 및 예제

이번 예제는 같은 데이터에 `RandomForestClassifier`와 `ExtraTreesClassifier`를 나란히 학습시켜, 기본 설정 차이와 점수 읽기 포인트를 같이 보는 작은 실습입니다.

- 문제 상황: 랜덤포레스트와 Extra Trees가 비슷해 보여도 `bootstrap`, `OOB`, train/test 읽기 포인트가 어떻게 달라지는지 본다.
- 입력(input): 유방암 분류 데이터 30개 연속형 특징
- 정답(label): 악성/양성 class
- 확인할 개념:
  - 랜덤포레스트 기본값은 `bootstrap=True` 흐름과 잘 맞는다
  - Extra Trees 기본값은 `bootstrap=False`라 OOB가 자동으로 따라오지 않는다
  - 두 모델은 test 점수뿐 아니라 train/test 간격, 계산 시간까지 같이 비교해야 한다
- 조작해 볼 값:
  - `et`에도 `bootstrap=True, oob_score=True`를 넣어 OOB가 어떤 조건에서 생기는지 확인한다.
  - 두 모델의 `n_estimators`를 100, 300, 600으로 바꿔 test 점수와 계산 시간 변화를 함께 본다.
  - `max_features`를 바꿔 두 숲의 무작위성 차이가 점수와 중요도에 어떻게 나타나는지 본다.

```python
# 같은 유방암 데이터에서 Random Forest와 Extra Trees의 기본 차이와 점수를 비교하는 예제입니다.
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier

X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

rf = RandomForestClassifier(
    n_estimators=300,
    bootstrap=True,
    oob_score=True,
    random_state=42
)

et = ExtraTreesClassifier(
    n_estimators=300,
    random_state=42
)

rf.fit(X_train, y_train)
et.fit(X_train, y_train)

print("[Random Forest]")
print("  bootstrap     :", rf.bootstrap)
print("  oob score     :", round(rf.oob_score_, 3))
print("  train accuracy:", round(rf.score(X_train, y_train), 3))
print("  test accuracy :", round(rf.score(X_test, y_test), 3))

print("[Extra Trees]")
print("  bootstrap     :", et.bootstrap)
print("  train accuracy:", round(et.score(X_train, y_train), 3))
print("  test accuracy :", round(et.score(X_test, y_test), 3))
```

실행 결과 예시는 다음과 비슷하게 나올 수 있습니다. 실제 값은 데이터 분할, 라이브러리 버전, 난수 설정에 따라 조금 달라질 수 있습니다.

```text
[Random Forest]
  bootstrap     : True
  oob score     : 0.96
  train accuracy: 1.0
  test accuracy : 0.947

[Extra Trees]
  bootstrap     : False
  train accuracy: 1.0
  test accuracy : 0.953
```

이 결과를 읽는 순서는 다음과 같습니다.

1. 두 모델 모두 train accuracy가 매우 높을 수 있으므로, train만 보고 판단하면 안 됩니다.
2. 랜덤포레스트는 OOB를 같이 읽을 수 있지만, Extra Trees는 기본값 그대로는 OOB가 없습니다.
3. test accuracy가 비슷하거나 Extra Trees가 약간 높게 보여도, 그 한 번의 숫자만으로 일반화하지 말고 데이터셋별 차이를 다시 확인해야 합니다.

즉, 이 예제의 핵심은 `누가 항상 더 좋다`가 아니라, `같은 숲 계열 안에서도 무작위성 주입 방식이 다르다`는 점을 출력으로 직접 확인하는 데 있습니다.

## 체크리스트

- Extra Trees를 랜덤포레스트와 같은 `randomized tree ensemble` 계열로 설명할 수 있는가?
- Extra Trees를 `랜덤포레스트의 아주 가까운 형제 모델`로 설명할 수 있는가?
- 차이가 `feature 무작위 선택` 자체보다 `threshold를 얼마나 무작위로 고르느냐`에서 더 크게 드러난다는 점을 이해했는가?
- `best split`과 `random threshold`의 차이를 말할 수 있는가?
- 랜덤포레스트는 bootstrap과 OOB 흐름에 잘 연결되고, Extra Trees는 기본값 그대로는 그렇지 않다는 점을 알고 있는가?
- Extra Trees 기본값에서 왜 OOB가 바로 나오지 않는지 설명할 수 있는가?
- Extra Trees를 분산을 조금 더 줄이는 대신 bias를 약간 더 늘릴 수 있는 비교 후보로 읽고 있는가?
- 랜덤포레스트와 Extra Trees를 비교할 때 train/test 간격, OOB 가능 여부, 계산 비용을 함께 봐야 한다는 점을 알고 있는가?

## 출처와 참고 자료

- scikit-learn, "1.11.2. Random forests and other randomized tree ensembles", User Guide, 확인 날짜: 2026-07-26. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, "ExtraTreesClassifier", API Reference, 확인 날짜: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, "RandomForestClassifier", API Reference, 확인 날짜: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
- Pierre Geurts, Damien Ernst, Louis Wehenkel, "Extremely randomized trees", *Machine Learning*, 63(1), 3-42, 2006, 확인 날짜: 2026-07-26. [https://doi.org/10.1007/s10994-006-6226-1](https://doi.org/10.1007/s10994-006-6226-1){: target="_blank" rel="noopener noreferrer" }

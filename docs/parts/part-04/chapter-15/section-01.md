# P4-15.1 랜덤포레스트(random forest)

> Section ID: `P4-15.1`
> Version: `v2026.07.31`

P4-14에서는 [결정트리(decision tree)](../../../reference/concept-glossary-parts/01-giyeok.md#decision-tree)가 왜 직관적이면서도 [과적합(overfitting)](../../../reference/concept-glossary-parts/01-giyeok.md#overfitting)에 쉽게 빠질 수 있는지 보았습니다. 특히 `max_depth`, `min_samples_leaf`, `ccp_alpha`를 바꾸어도 한 그루의 구조 흔들림이 완전히 사라지지 않을 수 있다는 점을 확인했습니다. 이제 다음 질문이 나옵니다.

그렇다면 트리의 장점은 살리고, 한 그루의 과한 흔들림은 줄일 방법이 없을까?

이 질문이 바로 [랜덤포레스트(random forest)](../../../reference/concept-glossary-parts/04-rieul.md#random-forest)의 출발점입니다.

랜덤포레스트는 서로 조금씩 다르게 학습된 여러 결정트리의 예측을 모아, 한 그루 트리보다 더 안정적인 판단을 만들려는 모델이다.

즉, 랜덤포레스트는 `트리를 버리는 모델`이 아니라 `트리를 여러 개 모아 약점을 줄이는 모델`입니다.

이 절은 [랜덤포레스트(random forest)](../../../reference/concept-glossary-parts/04-rieul.md#random-forest), [앙상블(ensemble)](../../../reference/concept-glossary-parts/08-ieung.md#ensemble), [부트스트랩(bootstrap)](../../../reference/concept-glossary-parts/06-bieup.md#bootstrap), feature 무작위 선택의 기본 뜻을 설명합니다. 뒤 절에서는 이 손잡이를 바탕으로 현재 맥락의 판단을 이어 가고, 여러 트리의 합의로 흔들림을 줄이는 기본 감각은 이 절과 개념사전의 해당 항목을 기준으로 다시 연결합니다.

## 랜덤포레스트(random forest)에서 닫을 질문

이 절은 다음 질문에 답합니다.

- 랜덤포레스트는 왜 여러 트리를 쓰는가?
- [부트스트랩(bootstrap)](../../../reference/concept-glossary-parts/06-bieup.md#bootstrap), [max_features](../../../reference/concept-glossary-parts/14-hieut.md#hyperparameter), `averaging`은 어떤 역할을 하는가?
- 한 그루 트리보다 왜 더 안정적으로 보일 수 있는가?
- 분류와 회귀에서 랜덤포레스트는 어떻게 동작하는가?
- [n_estimators](../../../reference/concept-glossary-parts/14-hieut.md#hyperparameter), [max_features](../../../reference/concept-glossary-parts/14-hieut.md#hyperparameter), [부트스트랩(bootstrap)](../../../reference/concept-glossary-parts/06-bieup.md#bootstrap), [oob_score](../../../reference/concept-glossary-parts/08-ieung.md#oob-score)는 무엇을 뜻하는가?

이 절은 먼저 `여러 트리를 모아 왜 한 그루보다 더 안정적인 판단을 만들려 하는가`를 닫습니다. 특징 중요도는 P4-15.2에서, OOB(out-of-bag) 점수의 평가 해석은 P4-15.3에서, Extra Trees 비교는 P4-15.4 보충학습에서, 그래디언트 부스팅과의 대비는 P4-16.1, P4-16.2에서 이어집니다.

## 랜덤포레스트(random forest)에서 남길 판단 기준

- 랜덤포레스트를 `여러 randomized tree의 평균/집계 모델`로 설명할 수 있습니다.
- bootstrap 샘플링과 feature 무작위 선택이 왜 필요한지 말할 수 있습니다.
- 랜덤포레스트가 결정트리의 분산(variance)을 줄이려는 시도라는 점을 이해할 수 있습니다.
- 대표 하이퍼파라미터의 역할을 입문 수준에서 구분할 수 있습니다.

## 학습 배경

결정트리 장까지 오면 보통 두 감각을 동시에 갖게 됩니다.

- 좋았던 점: 읽기 쉽고 표 형식 데이터에 잘 맞아 보인다.
- 불안한 점: 트리가 깊어지면 너무 많이 외우는 것 같다.

랜덤포레스트는 바로 이 긴장 위에서 등장합니다.

| 14장에서 남은 질문 | 15.1이 답하려는 방향 |
| --- | --- |
| 한 그루 트리가 흔들리면 어떻게 할까? | 여러 그루를 모아 흔들림을 평균낸다 |
| 예외에 끌리는 분기를 줄일 수 있을까? | 각 트리를 서로 다르게 만들어 오류를 덜 묶이게 한다 |
| 트리의 해석 가능성을 완전히 잃는가? | 일부 잃지만, 안정성과 성능을 얻는 경우가 많다 |

즉, 랜덤포레스트는 `결정트리의 단점을 부정`하기보다, `여러 트리의 앙상블(ensemble) 구조로 그 단점을 완화`하는 방식입니다.

여기에 한 가지를 더 붙이면 랜덤포레스트 절이 지금까지 정리한 비교 기록 구조와 직접 이어집니다. 랜덤포레스트를 후보로 올릴 때는 `트리를 여러 개 쓴다`는 설명만 남기는 것이 아니라, `단일 트리 대비 어떤 오류 사례가 덜 흔들리는가`, `여전히 남는 애매한 사례는 무엇인가`, `다음에 어떤 숲 설정을 더 볼 것인가`를 함께 적어 둡니다. 같은 평균 점수처럼 보여도 어떤 모델이 특정 오류 유형을 더 자주 반복하는지, 어떤 모델이 시드를 바꿔도 더 안정적으로 유지되는지는 따로 읽어야 합니다.

| 같이 남길 기록 | 왜 필요한가 |
| --- | --- |
| 단일 트리와 랜덤포레스트 비교 | 앙상블이 실제로 무엇을 더 안정화하는지 보기 위해서입니다. |
| 남는 오류 사례 | 여러 트리를 모아도 계속 틀리거나 애매한 사례를 다시 보기 위해서입니다. |
| 흔들림 감소 여부 | 한 번의 높은 점수보다 평균적 안정성이 좋아졌는지 보기 위해서입니다. |
| 다음 실험 질문 | `n_estimators`, `max_features`, `bootstrap` 중 무엇을 더 조정할지 정하기 위해서입니다. |

트리 계열 안에서도 질문이 어떻게 달라지는지는 다음처럼 정리할 수 있습니다.

| 모델 | 먼저 붙잡는 질문 | 더 강하게 보는 기준 |
| --- | --- | --- |
| 결정트리 | 어떤 질문 순서로 데이터를 나눌까? | 읽기 쉬운 분기 구조와 leaf 규칙 |
| 랜덤포레스트 | 한 그루의 흔들림을 어떻게 줄일까? | 여러 트리의 다양성과 평균적 안정성 |
| 그래디언트 부스팅 | 앞 단계의 오차를 다음 단계가 어떻게 고칠까? | 순차 보정과 residual 감소 |

즉, 랜덤포레스트는 `트리를 더 많이 쓴다`보다 `서로 다른 트리들의 흔들림을 모아 줄인다`가 더 핵심입니다. 이 기준이 잡혀야 뒤의 그래디언트 부스팅도 단순한 다음 앙상블 이름이 아니라, `안정성 중심 앙상블`과 `오차 보정 중심 앙상블`의 대비로 읽힙니다.

### 언제 랜덤포레스트를 먼저 후보로 올리면 좋은가

랜덤포레스트는 단일 트리의 해석 가능성을 조금 희생하더라도, 표 형식 데이터에서 더 안정적인 기본 후보를 빠르게 세우고 싶을 때 강합니다.

| 현재 문제 상태 | 랜덤포레스트를 먼저 올릴 이유 | 먼저 확인할 점 |
| --- | --- | --- |
| 단일 트리가 자주 흔들린다 | 여러 트리 평균으로 분산을 줄일 수 있기 때문 | 시드나 분할에 따라 점수가 얼마나 흔들리는지 |
| 표 형식 데이터에서 강한 기본 후보가 필요하다 | 트리 계열의 장점을 유지하며 안정성을 얻기 쉽기 때문 | 깊이와 leaf 크기 제어가 되어 있는지 |
| 선형 모델이 놓치는 비선형 패턴이 의심된다 | 트리 앙상블이 복잡한 분기 구조를 더 유연하게 담을 수 있기 때문 | 과적합과 계산 비용을 함께 보는지 |
| 해석보다 먼저 튼튼한 baseline 상향이 필요하다 | 단일 트리보다 덜 예민한 기본 성능을 기대할 수 있기 때문 | 남는 오류 사례가 무엇인지 |
| 이후 중요도나 OOB까지 함께 보고 싶다 | 트리 계열 내부 점검 수단을 같이 활용할 수 있기 때문 | 중요도와 OOB를 과신하지 않는지 |

이 표의 핵심은 랜덤포레스트를 `트리 많이 쓰기`가 아니라 `단일 트리의 흔들림을 줄이는 안정성 후보`로 읽는 데 있습니다.

## 랜덤포레스트를 앙상블의 큰 틀에서 읽기

scikit-learn 사용자 가이드는 ensemble methods를 `여러 base estimator의 예측을 결합해 단일 estimator보다 더 나은 generalizability / robustness를 얻으려는 방법`으로 설명합니다.

랜덤포레스트는 이 앙상블(ensemble) 계열 안에서, 트리를 여러 개 쓰는 대표 사례입니다.

랜덤포레스트는 서로 조금 다른 여러 트리의 판단을 모아 더 안정적인 답을 만들려는 앙상블 방식입니다.

`한 모델의 판단을 그대로 믿기보다, 서로 조금 다른 여러 모델의 판단을 모아 더 안정적인 답을 만들자.`

이 큰 틀을 보면 랜덤포레스트가 왜 나왔는지 더 분명해집니다.

### 랜덤포레스트는 어떤 모델인가

scikit-learn 문서는 random forests를 `decision tree 기반의 averaging algorithm`으로 설명합니다. 각 트리는 훈련 세트에서 복원추출(with replacement)한 bootstrap sample로 학습되고, 각 split에서는 feature의 임의 부분집합만 후보로 봅니다.

핵심은 두 가지 무작위성입니다.

1. 샘플을 다르게 뽑는다.  
2. 각 분기에서 feature를 다르게 본다.

그리고 마지막에 여러 트리의 예측을 모읍니다.

이 구조를 짧게 바꾸면 다음과 같습니다.

`랜덤포레스트는 같은 데이터를 모든 트리에 똑같이 주지 않고, 각 트리가 조금씩 다른 데이터와 다른 feature 후보를 보게 만든 뒤, 마지막에 결과를 합친다.`

### 한 장면으로 보기

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-1-mermaid-01-ko.mmd"
```

이 그림에서 중요한 점은 `모든 트리가 완전히 같은 것을 보지 않는다`는 것입니다. 그래야 서로 다른 실수를 만들 여지가 생기고, 그 실수를 평균내거나 투표로 묶을 수 있습니다.

### 왜 같은 트리를 여러 번 복사하는 것만으로는 부족한가

여기서 초심자가 자주 드는 질문이 있습니다.

`결정트리를 100번 학습시키면 그냥 랜덤포레스트가 되는 것 아닐까?`

핵심은 `그 100개가 정말 서로 다른가`입니다. 같은 데이터, 같은 feature 후보, 같은 규칙으로 거의 같은 트리를 여러 개 만들면 실수도 거의 같은 방향으로 반복될 수 있습니다. 이 경우에는 `여러 개를 모았다`기보다 `같은 판단을 크게 반복했다`에 가깝습니다.

랜덤포레스트가 필요한 이유는 `트리 수`만 늘리는 데 있지 않고, `트리들이 서로 다른 이유`를 만들어 주는 데 있습니다.

| 비교 장면 | 실제로 생기는 일 | 읽어야 하는 결론 |
| --- | --- | --- |
| 같은 트리를 여러 번 복사 | 거의 같은 분기와 거의 같은 실수를 반복한다 | 평균을 내도 흔들림이 잘 줄지 않는다 |
| bootstrap만 다르게 준다 | 각 트리가 보는 사례가 조금씩 달라진다 | 예외 사례에 끌리는 정도가 조금씩 달라진다 |
| feature 후보도 무작위로 제한한다 | 첫 분기와 이후 경로가 더 다르게 갈 수 있다 | 트리들이 서로 덜 닮아 합의의 의미가 커진다 |
| 마지막에 집계한다 | 한 트리의 과한 확신이 완화된다 | 숲 전체의 판단이 더 안정적으로 읽힌다 |

즉, 랜덤포레스트의 핵심은 `많은 트리`보다 `서로 덜 닮은 트리들의 집계`입니다.

### 왜 여러 트리를 모으면 더 안정적일 수 있는가

결정트리는 high variance 모델로 자주 설명됩니다. scikit-learn 사용자 가이드도 개별 결정트리는 variance가 크고 overfit하기 쉽다고 설명합니다. 랜덤포레스트는 이 variance를 줄이기 위해 여러 diverse tree를 결합합니다.

독자용 직관은 다음과 같습니다.

- 한 트리는 특정 예외 사례에 과하게 끌릴 수 있습니다.
- 다른 트리는 bootstrap 샘플이 달라 그 예외를 덜 강하게 볼 수 있다.
- 또 다른 트리는 분기 feature 후보가 달라 전혀 다른 경로를 만들 수 있습니다.
- 여러 트리의 답을 모으면, 한 트리만의 과한 흔들림이 덜 드러날 수 있습니다.

즉, 랜덤포레스트는 보통 `한 그루의 확신`보다 `여러 그루의 합의`를 택합니다.

프로젝트 메모 형식으로 줄이면 다음처럼 적을 수 있습니다.

| 기록 항목 | 예 |
| --- | --- |
| baseline 또는 단일 후보 | `single tree` |
| ensemble 후보 | `random forest` |
| 남는 review 사례 | `고객 X는 여전히 애매하다` |
| 흔들림 변화 | `시드를 바꿔도 test 점수 차이가 줄었다` |
| 다음 질문 | `트리 수를 늘리면 안정성이 더 좋아지는가` |

이 표가 있으면 랜덤포레스트 절이 `비교 후보 -> 남는 오류 사례 -> 다음 질문` 구조로 읽힙니다. 즉, 랜덤포레스트의 장점은 평균 숫자 하나보다 `남는 실패 패턴이 덜 흔들리는가`를 같이 볼 때 더 분명해집니다.

그래서 실무에서 랜덤포레스트를 고려하는 장면은 대체로 `단일 트리는 너무 흔들리지만, 신경망까지 바로 갈 만큼 데이터 규모나 구조가 크지 않은 표 형식 문제`입니다. 이때 중요한 기대값은 `최고 한 번의 점수`보다 `덜 흔들리는 기본 후보`를 빠르게 세우는 일입니다.

### bootstrap은 무엇을 하는가

random forest의 첫 번째 무작위성은 bootstrap sampling입니다.

scikit-learn 문서는 각 트리가 훈련 세트에서 복원추출한 bootstrap sample로 만들어진다고 설명합니다. 복원추출이므로 어떤 샘플은 한 트리에 두 번 들어갈 수 있고, 어떤 샘플은 아예 빠질 수 있습니다.

이를 직관으로 읽으면 다음과 같습니다.

`각 트리는 전체 데이터를 복사해 그대로 배우는 것이 아니라, 조금 다른 훈련 경험을 하게 된다.`

아주 작은 예를 생각합니다.

원래 데이터가 `A, B, C, D, E`라면 한 bootstrap sample은 다음처럼 보일 수 있습니다.

- tree 1: `A, B, B, D, E`
- tree 2: `A, C, D, D, E`
- tree 3: `B, C, C, D, E`

같은 원본 데이터에서 출발했어도 각 트리의 시야가 조금씩 다릅니다.

이 장치를 한 문장으로 줄이면 다음과 같습니다.

`bootstrap은 트리마다 다른 훈련 경험을 만들어, 같은 예외 사례를 모두가 똑같이 외우지 않게 하려는 장치다.`

### feature 무작위 선택은 무엇을 하는가

두 번째 무작위성은 feature sub-sampling입니다.

scikit-learn 문서는 각 split에서 candidate feature의 무작위 부분집합을 본다고 설명합니다. 이 역할을 하는 대표 하이퍼파라미터가 `max_features`입니다.

왜 이게 필요할까요?

만약 강한 feature 하나가 항상 모든 트리의 첫 분기를 장악한다면, 트리들이 너무 비슷해질 수 있습니다. 그러면 여러 개를 모아도 diversity가 부족합니다.

따라서 feature 후보를 일부만 보게 하면:

- 어떤 트리는 feature A를 중심으로 분기하고
- 어떤 트리는 feature B를 먼저 보고
- 어떤 트리는 다른 우회 경로를 만들 수 있습니다

즉, `max_features`는 단순 속도 옵션이 아니라 `트리들을 서로 덜 닮게 만드는 장치`로 읽는 것이 더 중요합니다.

bootstrap과 `max_features`를 함께 놓고 보면 역할 차이가 더 잘 보입니다.

| 장치 | 직접 바꾸는 것 | 막으려는 문제 |
| --- | --- | --- |
| `bootstrap` | 각 트리가 보는 샘플 묶음 | 같은 사례에 모두 똑같이 끌리는 현상 |
| `max_features` | 각 분기에서 보는 feature 후보 | 항상 같은 feature가 모든 트리를 지배하는 현상 |
| `averaging` 또는 vote | 마지막 예측 결합 방식 | 한 트리의 과한 확신이 최종 답을 지배하는 현상 |

이 표를 기준으로 읽으면 랜덤포레스트는 `무작위로 섞는다`는 막연한 느낌이 아니라, `샘플 다양성`, `분기 다양성`, `최종 집계`를 각각 따로 설계한 구조로 보입니다.

### 분류와 회귀에서 어떻게 합치는가

랜덤포레스트는 분류와 회귀에 모두 쓰일 수 있습니다. 달라지는 것은 여러 트리의 답을 합치는 방법입니다.

| 문제 유형 | 여러 트리의 출력 | 최종 집계 |
| --- | --- | --- |
| 분류(classification) | 각 트리의 class 또는 class 확률 | 투표 또는 확률 평균 |
| 회귀(regression) | 각 트리의 예측 수치 | 평균 |

scikit-learn 문서는 분류 random forest에서 트리들의 확률 예측을 평균해 결합한다고 설명합니다. `majority vote`라는 설명도 큰 흐름에서는 통하지만, scikit-learn 구현 기준으로는 확률 평균 쪽이 더 정확합니다.

### 랜덤포레스트를 흐름으로 읽기

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-1-mermaid-02-ko.mmd"
```

핵심은 `더 많은 트리` 자체가 아니라 `서로 다른 오류를 만들 수 있는 트리들`이라는 점입니다.

## 랜덤포레스트의 대표 하이퍼파라미터를 읽는 기준

API 문서 기준으로 랜덤포레스트에서 먼저 알아야 할 손잡이는 다음 정도입니다.

| 하이퍼파라미터 | 먼저 읽는 질문 |
| --- | --- |
| `n_estimators` | 트리를 몇 그루 만들 것인가? |
| `max_features` | 각 분기에서 feature를 몇 개 후보로 볼 것인가? |
| `bootstrap` | 각 트리를 복원추출 샘플로 학습시킬 것인가? |
| `max_depth` | 개별 트리가 어디까지 깊어질 수 있는가? |
| `min_samples_leaf` | 개별 트리의 leaf가 너무 작아지지 않게 할 것인가? |
| `oob_score` | bootstrap에서 빠진 샘플로 내부 평가를 볼 것인가? |

이 중에서 15.1 수준에서 가장 중요한 것은 세 가지입니다.

- `n_estimators`: 숲의 크기
- `max_features`: 트리 다양성의 정도
- `bootstrap`: 각 트리의 학습 경험을 다르게 만드는가

이 세 손잡이는 이름만 외우기보다, 값을 바꿨을 때 무엇이 달라질지를 같이 읽어야 합니다.

| 하이퍼파라미터 | 값을 바꿀 때 먼저 생기는 변화 | 먼저 경계할 점 |
| --- | --- | --- |
| `n_estimators` | 트리 수가 늘어나며 평균 판단이 더 안정될 수 있다 | 계산 비용이 늘고, 어느 시점부터 개선 폭이 작아질 수 있다 |
| `max_features` | 트리들이 서로 덜 닮거나 더 닮게 된다 | 너무 크면 트리가 비슷해지고, 너무 작으면 개별 트리 힘이 약해질 수 있다 |
| `bootstrap` | 각 트리의 훈련 경험 차이가 생긴다 | 끄면 트리 다양성이 줄어 숲의 장점이 약해질 수 있다 |
| `max_depth` | 개별 트리의 복잡도가 달라진다 | 너무 깊으면 숲 안의 각 트리도 예외를 과하게 외울 수 있다 |
| `min_samples_leaf` | leaf가 지나치게 잘게 쪼개지는 것을 막는다 | 너무 크면 필요한 분기까지 둔해질 수 있다 |

실무적으로는 다음처럼 읽으면 됩니다.

- 점수는 괜찮지만 시드마다 흔들리면 `n_estimators`와 `max_features`를 먼저 봅니다.
- 트리들이 모두 비슷해 보이면 `max_features`가 너무 큰지 의심합니다.
- 각 트리가 지나치게 예외를 외우는 것 같으면 `max_depth`, `min_samples_leaf`도 함께 봅니다.

### OOB(out-of-bag)는 무엇인가

bootstrap sampling을 하면 어떤 샘플은 특정 트리의 학습에 들어가지 않습니다. scikit-learn 문서는 이런 빠진 샘플을 이용해 OOB(out-of-bag) 방식의 일반화 오차 추정을 할 수 있다고 설명합니다.

OOB는 각 트리가 보지 못한 샘플을 활용해, 별도 검증 감각을 일부 얻는 방식으로 이해할 수 있습니다.

다만 OOB를 `아무 검증 절차나 대체하는 만능 장치`로 이해하면 안 됩니다. 이 절에서는 이름과 역할만 잡고 넘어갑니다.

그래도 OOB를 왜 같이 언급하는지는 알아둘 필요가 있습니다. 랜덤포레스트는 bootstrap 때문에 `각 트리가 학습하지 않은 샘플`이 자연스럽게 생기고, OOB는 바로 그 남는 샘플을 다시 활용하는 구조입니다. 즉, OOB는 랜덤포레스트 바깥에서 억지로 붙인 평가 장치가 아니라, `bootstrap을 썼기 때문에 같이 따라오는 내부 확인 수단`으로 읽는 편이 더 자연스럽습니다.

## 랜덤포레스트: 확인할 판단 기준

이 사례에서는 랜덤포레스트가 여러 트리의 평균화로 안정성을 얻는다는 점이 드러나는지 확인한다.

### 사례 1. 고객 이탈 예측에서 한 그루 규칙보다 여러 그루 합의가 더 나을 때

구독 서비스 팀이 고객 이탈 예측을 위해 결정트리를 먼저 써 보았습니다. 사람이 먼저 보던 기준은 `최근 방문 수`, `결제 지연`, `문의 횟수`, `멤버십 등급` 같은 신호였습니다.

단일 트리는 규칙을 읽기 쉬웠지만, 특정 예외 고객 몇 명에 경계가 쉽게 끌리는 문제가 있었습니다. 어떤 데이터 분할에서는 잘 맞고, 다른 분할에서는 조금만 바뀌어도 첫 분기와 예측 결과가 흔들립니다. 팀은 트리의 질문 흐름은 유지하되, 한 그루의 과한 예민함은 줄이고 싶어 합니다.

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-1-mermaid-03-ko.mmd"
```

이 장면에서 랜덤포레스트는 `트리를 버리는 방법`이 아니라 `조금씩 다른 트리를 여러 개 모아 합의하는 방법`으로 읽어야 합니다. bootstrap으로 각 트리가 조금 다른 고객 집합을 보고, `max_features`로 분기 후보도 다르게 보면, 한 그루가 특정 예외에 끌리는 현상이 숲 전체에서는 평균적으로 약해질 수 있습니다.

이 사례를 업무 메모처럼 더 짧게 적으면 다음 순서입니다.

| 단계 | 팀이 실제로 보는 것 |
| --- | --- |
| 사람이 먼저 보던 기준 | `최근 방문 수`, `결제 지연`, `문의 횟수`, `멤버십 등급` |
| 단일 트리의 한계 | 특정 예외 고객 몇 명이 첫 분기와 경계를 쉽게 흔든다 |
| 랜덤포레스트가 바꾸는 점 | 여러 트리가 서로 다른 고객 묶음과 다른 분기 후보를 본다 |
| 최종 판단 방식 | 한 트리의 과한 규칙보다 여러 트리의 합의를 본다 |
| 확인 가능한 결과 | 최고 점수뿐 아니라 시드별 흔들림과 남는 오류 사례를 함께 본다 |

확인 가능한 결과는 단일 트리와 랜덤포레스트의 test 점수뿐 아니라 여러 난수 시드에서의 흔들림을 함께 볼 때 드러납니다. 최고 한 번의 점수보다 평균적인 안정성이 더 좋아진다면, 랜덤포레스트의 장점이 `더 복잡한 규칙`이 아니라 `덜 흔들리는 합의`라는 점을 설명할 수 있습니다.

### 사례 2. 실무 장면에서 어떻게 읽을 수 있는가

랜덤포레스트는 특히 다음처럼 읽을 수 있습니다.

| 업무 장면 | 랜덤포레스트가 유리하게 느껴질 수 있는 이유 |
| --- | --- |
| 고객 이탈 예측 | 한 트리의 예외적 분기에 덜 끌리고, 표 형식 데이터에서 출발하기 쉽다 |
| 대출 심사 보조 | 비선형 관계를 잡으면서도 트리 계열의 감각을 유지한다 |
| 설비 이상 탐지 | 복잡한 센서 조합을 여러 트리로 나누어 볼 수 있다 |
| 마케팅 반응 예측 | 한두 개 특징에만 과하게 기대는 단일 트리보다 안정성을 얻기 쉽다 |

반대로, 해석 가능성이 최우선이어서 `왜 이런 예측이 나왔는지`를 개별 규칙으로 바로 설명해야 하는 상황에서는 단일 결정트리보다 불리하게 느껴질 수 있습니다. 숲 전체는 한 그루보다 훨씬 읽기 어렵기 때문입니다.

## 연습 및 예제

### Python 예제로 한 그루와 여러 그루를 비교하기

이번 예제는 같은 iris 분류 문제에서 결정트리 하나와 랜덤포레스트를 비교하는 작은 실습입니다.

- 문제 상황: 한 그루 트리와 여러 그루 숲의 차이를 본다.
- 입력(input): iris 특징 4개
- 정답(label): 품종 class
- 확인할 개념:
  - random forest는 여러 트리를 묶는다
  - 같은 데이터에서도 test 성능과 안정성이 달라질 수 있다
  - `n_estimators`가 숲의 크기와 연결된다

조작해 볼 값:

- `n_estimators`: 10, 50, 100처럼 숲의 크기를 바꾸어 점수와 계산 시간을 함께 봅니다.
- `random_state`: 단일 트리와 숲이 같은 시드 변화에 얼마나 다르게 흔들리는지 봅니다.
- `max_features`: 기본값과 `None`을 비교해 트리 다양성이 줄 때 어떤 차이가 생기는지 봅니다.

```python
# iris 분류에서 단일 결정트리와 랜덤포레스트의 점수와 구조를 나란히 비교하는 예제입니다.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

single_tree = DecisionTreeClassifier(random_state=42)
single_tree.fit(X_train, y_train)

forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
forest.fit(X_train, y_train)

print("single tree")
print("  train accuracy:", round(single_tree.score(X_train, y_train), 3))
print("  test accuracy :", round(single_tree.score(X_test, y_test), 3))
print("  depth         :", single_tree.get_depth())
print("  leaves        :", single_tree.get_n_leaves())
print()

print("random forest")
print("  train accuracy:", round(forest.score(X_train, y_train), 3))
print("  test accuracy :", round(forest.score(X_test, y_test), 3))
print("  trees         :", len(forest.estimators_))
print("  first depth   :", forest.estimators_[0].get_depth())
```

실행 결과 예시는 다음과 같습니다.

```text
single tree
  train accuracy: 1.0
  test accuracy : 0.911
  depth         : 5
  leaves        : 8

random forest
  train accuracy: 1.0
  test accuracy : 0.911
  trees         : 100
  first depth   : 4
```

이 작은 결과만 보면 둘이 비슷해 보일 수 있습니다. 그래서 한 번 더 봐야 할 것은 `random_state`를 바꾸었을 때의 흔들림입니다.

### Python 예제로 흔들림 차이 보기

이번 예제는 같은 데이터 분할을 여러 난수 시드로 반복하면서 단일 트리와 랜덤포레스트의 test 성능이 얼마나 흔들리는지 보는 실습입니다.

문제 상황:

- 모델 비교에서는 최고 점수보다 여러 분할에서 성능이 얼마나 흔들리는지도 함께 봐야 한다

입력(input):

- iris 데이터셋
- 단일 트리 모델
- 랜덤포레스트 모델
- 여러 난수 시드

기대 출력(output):

- 시드별 트리 점수와 랜덤포레스트 점수
- 두 모델의 평균 또는 흔들림 차이

확인할 개념:

- 랜덤포레스트의 장점은 최고점보다 `흔들림 감소`에서 더 잘 보일 수 있다
- 여러 시드 비교는 안정성을 읽는 가장 단순한 방법이다

조작해 볼 값:

- `range(10)`: 반복 시드 수를 5, 20처럼 바꾸어 평균이 얼마나 안정되는지 봅니다.
- `n_estimators`: 10과 100을 비교해 트리 수가 흔들림에 어떤 영향을 주는지 봅니다.
- `max_depth`: 단일 트리와 숲 안의 개별 트리 깊이를 제한했을 때 평균 점수가 어떻게 달라지는지 봅니다.

```python
# 여러 random_state에서 단일 트리와 랜덤포레스트의 test 점수 흔들림을 비교하는 예제입니다.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

tree_scores = []
forest_scores = []

for seed in range(10):
    tree = DecisionTreeClassifier(random_state=seed)
    tree.fit(X_train, y_train)
    tree_scores.append(tree.score(X_test, y_test))

    forest = RandomForestClassifier(n_estimators=100, random_state=seed)
    forest.fit(X_train, y_train)
    forest_scores.append(forest.score(X_test, y_test))

print("single tree test scores :", [round(s, 3) for s in tree_scores])
print("forest test scores      :", [round(s, 3) for s in forest_scores])
print("tree avg                :", round(sum(tree_scores) / len(tree_scores), 3))
print("forest avg              :", round(sum(forest_scores) / len(forest_scores), 3))
```

실행 결과 예시는 다음과 같습니다.

```text
single tree test scores : [0.978, 0.933, 0.911, 0.933, 0.911, 0.911, 0.933, 0.911, 0.911, 0.933]
forest test scores      : [0.978, 0.956, 0.933, 0.933, 0.933, 0.933, 0.956, 0.933, 0.933, 0.956]
tree avg                : 0.927
forest avg              : 0.944
```

이 예제가 보여 주는 것은 다음입니다.

1. 단일 트리도 어떤 시드에서는 잘 나올 수 있습니다.
2. 하지만 랜덤포레스트는 평균적으로 덜 흔들리고 더 안정적인 경우가 많습니다.
3. 랜덤포레스트의 가치는 `완전히 새로운 구조`라기보다 `불안정한 트리들을 평균내는 방식`에서 옵니다.

## 체크리스트

- 랜덤포레스트를 `여러 randomized decision tree의 집계 모델`로 설명할 수 있는가?
- 단일 트리보다 정말 흔들림이 줄었는지 같은 오류 사례 기준으로 보고 있는가?
- bootstrap과 feature 무작위 선택이 트리들을 서로 덜 닮게 만들기 위한 장치라는 점을 이해했는가?
- 여러 트리의 예측을 모아 단일 트리의 분산(variance)을 줄이려 한다는 점을 설명할 수 있는가?
- 랜덤포레스트의 장점을 최고 점수보다 평균적 안정성에서 읽고 있는가?
- 해석 가능성은 단일 트리보다 낮아질 수 있다는 점을 알고 있는가?
- `n_estimators`, `max_features`, `bootstrap` 중 무엇이 현재 더 중요한 손잡이인지 구분하고 있는가?

## 출처와 참고 자료

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, 확인 날짜: 2026-07-26. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `RandomForestClassifier`, scikit-learn API Reference, 확인 날짜: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
- Leo Breiman, `Random Forests`, Machine Learning, 45(1), 5-32, 2001. 확인 날짜: 2026-07-26. [https://doi.org/10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324){: target="_blank" rel="noopener noreferrer" }

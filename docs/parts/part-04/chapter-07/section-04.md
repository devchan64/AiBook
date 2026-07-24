# P4-7.4 보충학습: 특징 선택 방식 구분

> Section ID: `P4-7.4`
> Version: `v2026.07.24`

P4-7.1부터 P4-7.3까지에서는 특징을 고르고, 입력 표현 문제를 나누고, 전처리 기본 판단을 잡았습니다. 그런데 실제로는 독자가 곧 이런 이름을 만나게 됩니다.

- 통계 검정 기반 특징 선택
- 재귀적 특징 제거(recursive feature elimination, RFE)
- 차원 축소(dimensionality reduction)

이 이름들은 모두 `입력을 줄이거나 다시 표현한다`는 점에서 비슷해 보여도, 무엇을 기준으로 줄이는지와 무엇을 남기는지가 다릅니다.

## 보충학습: 필터(filter), 래퍼(wrapper), 차원 축소(dimensionality reduction)를 처음 구분하는 법에서 구분할 경계

이 절은 다음 질문에 답합니다.

- 필터(filter), 래퍼(wrapper), 임베디드(embedded) 특징 선택은 무엇이 다른가?
- 통계 검정 기반 특징 선택은 어떤 생각으로 동작하는가?
- 재귀적 특징 제거(RFE)는 무엇을 반복하는가?
- 차원 축소는 특징 선택과 무엇이 다른가?

이 절은 먼저 `입력을 줄이거나 다시 표현하는 이름들을 어떻게 구분할 것인가`를 닫습니다. 개별 차원 축소 알고리즘의 직관과 한계는 P4-18.1, P4-18.2에서 이어집니다.

## 보충학습: 필터(filter), 래퍼(wrapper), 차원 축소(dimensionality reduction)를 처음 구분하는 법에서 복구할 연결

- 특징 선택과 차원 축소를 같은 작업으로 섞지 않고 구분할 수 있습니다.
- 필터, 래퍼, 임베디드 접근이 무엇을 기준으로 특징을 줄이는지 설명할 수 있습니다.
- RFE가 `모델을 반복해서 돌리며 덜 중요한 특징을 줄여 가는 방식`이라는 점을 말할 수 있습니다.

## 큰 구도부터 잡기

다음 표로 시작합니다.

| 방식 | 무엇을 남기거나 바꾸는가 | 판단 기준 |
| --- | --- | --- |
| 필터(filter) | 원래 특징 중 일부를 고른다 | 통계량, 상관, 단변량 점수 |
| 래퍼(wrapper) | 원래 특징 부분집합을 반복 비교한다 | 모델 성능 |
| 임베디드(embedded) | 학습 과정 안에서 중요도를 함께 만든다 | 모델 내부 규칙 |
| 차원 축소(dimensionality reduction) | 원래 특징을 새 축으로 다시 표현한다 | 분산, 거리, 구조 보존 등 |

핵심은 이것입니다.

`특징 선택은 주로 원래 특징 중 무엇을 남길지 정하는 일이고, 차원 축소는 여러 특징을 더 적은 새 축으로 다시 표현하는 일이다.`

## 통계 검정 기반 특징 선택은 어디에 속하나

통계 검정 기반 특징 선택은 보통 필터 접근에 속합니다. 즉, 각 특징과 정답 사이의 관계를 점수화하거나 검정하고, 그 결과를 바탕으로 특징 후보를 줄입니다.

이 방식은 다음 장면에서 직관적입니다.

- 특징 수가 많아서 빠른 1차 정리가 필요할 때
- 복잡한 모델을 반복 학습하기 전에 후보를 줄이고 싶을 때
- 각 특징을 개별적으로 우선 점검하고 싶을 때

대신 이 방식은 보통 `특징 조합이 함께 만들어 내는 효과`를 충분히 반영하지 못할 수 있습니다. 그래서 이 절에서는 `빠른 1차 정리`에 가까운 접근으로 다룹니다.

## 재귀적 특징 제거(RFE)는 무엇을 반복하나

RFE는 래퍼(wrapper) 접근의 대표 예로 보면 됩니다. 아주 단순하게 말하면 다음 순서를 반복합니다.

1. 현재 특징 집합으로 모델을 학습합니다.
2. 중요도가 낮은 특징을 일부 제거합니다.
3. 남은 특징으로 다시 학습합니다.
4. 원하는 개수까지 줄어들 때까지 반복합니다.

즉, RFE는 `어떤 특징이 현재 모델 안에서 덜 도움이 되는가`를 반복적으로 확인하는 방식입니다.

필터 방식보다 계산 비용은 더 들 수 있지만, `현재 모델과 함께 봤을 때의 유용성`을 더 반영하기 쉽습니다.

## 차원 축소는 왜 별도 범주로 봐야 하나

차원 축소는 특징을 버리는 일처럼 보이지만, 실제로는 더 자주 `새 축을 만드는 일`입니다.

예를 들어:

- 특징 선택은 `age`, `income`, `visits` 중 두 개만 남길 수 있습니다.
- 차원 축소는 이 세 특징을 섞어서 `component_1`, `component_2` 같은 새 축으로 바꿀 수 있습니다.

그래서 차원 축소는 `원래 칼럼 이름을 유지한 채 줄이는 작업`과는 다르게 읽어야 합니다.

| 질문 | 특징 선택 | 차원 축소 |
| --- | --- | --- |
| 원래 특징 이름이 남는가 | 자주 남는다 | 보통 새 축으로 바뀐다 |
| 해석이 쉬운가 | 상대적으로 쉽다 | 더 어려워질 수 있다 |
| 목적 | 불필요한 특징 줄이기 | 표현 압축, 구조 요약, 시각화 |

차원 축소 자체의 목적과 한계는 P4-18.1, P4-18.2에서 더 자세히 다시 봅니다.

## 사례 및 예시

### 어떤 축소 방식을 먼저 떠올려야 하는가

방법 이름이 섞여 보일 때는 `원래 칼럼을 남길 것인가`, `모델 성능을 기준으로 줄일 것인가`, `새 축으로 다시 표현할 것인가`를 먼저 나누면 정리가 빨라집니다.

| 지금 필요한 판단 | 먼저 떠올릴 방식 | 이유 |
| --- | --- | --- |
| 많은 칼럼을 빠르게 1차 정리하고 싶다 | 필터(filter) | 통계량이나 단변량 점수로 빠르게 후보를 줄일 수 있기 때문 |
| 현재 모델 기준으로 도움이 적은 특징을 줄이고 싶다 | 래퍼(wrapper), 예: RFE | 모델 성능과 함께 특징 부분집합을 반복 비교하기 때문 |
| 학습 과정 안에서 중요도를 함께 얻고 싶다 | 임베디드(embedded) | 모델 내부 규칙으로 선택이 함께 일어나기 때문 |
| 해석보다 압축과 구조 요약이 더 중요하다 | 차원 축소(dimensionality reduction) | 원래 칼럼 대신 새 축으로 표현을 다시 만들기 때문 |

이 구분이 먼저 서야 `차원을 줄인다`는 한 문장 아래에 서로 다른 작업을 섞지 않게 됩니다.

### 사례 1. 고객 세분화 전에 특징을 줄이려는데 방법 이름이 섞여 보일 때

마케팅 팀이 고객 세분화를 준비하면서 입력 칼럼을 줄이려 합니다. 사람이 먼저 보던 기준은 `최근 방문`, `구매 금액`, `할인 반응`, `문의 패턴` 같은 행동 신호였습니다.

그런데 회의에서는 서로 다른 방법 이름이 한꺼번에 나옵니다. 어떤 사람은 상관이 낮은 칼럼을 먼저 빼자고 하고, 어떤 사람은 모델을 반복 돌려 중요도가 낮은 칼럼을 줄이자고 하며, 또 어떤 사람은 PCA로 축을 줄이자고 말합니다. 모두 `차원을 줄인다`는 말로 묶이지만 실제로는 무엇을 남기고 무엇을 바꾸는지가 다릅니다.

```mermaid
--8<-- "assets/part-04/chapter-07/p4-7-4-mermaid-01-ko.mmd"
```

여기서 구분이 필요합니다. 필터 방식은 원래 특징을 빠르게 점검해 1차 후보를 줄이는 데 가깝고, 래퍼 방식인 RFE는 현재 모델 성능을 기준으로 반복해서 특징을 줄입니다. 차원 축소는 원래 칼럼 일부를 고르는 것이 아니라 여러 특징을 섞어 새 축으로 다시 표현하는 쪽에 더 가깝습니다.

확인 가능한 결과도 다르게 읽어야 합니다. 필터와 RFE는 어떤 원래 칼럼이 남았는지 목록으로 볼 수 있지만, 차원 축소는 `component_1`, `component_2` 같은 새 축으로 바뀌어 해석 방식이 달라집니다. 그래서 같은 `입력을 줄인다`는 말이라도, 해석 가능성을 남길지 새 표현으로 압축할지 먼저 결정해야 합니다.

## 연습 및 예제

이번 예제는 같은 데이터에서 필터 방식, RFE, PCA가 각각 무엇을 남기는지 비교합니다.

- 문제 상황: 여섯 개 고객 행동 특징 중 세 개만 남기거나 세 개 축으로 줄이고 싶다
- 입력(input): scikit-learn이 만든 작은 분류 데이터
- 기대 출력(output): 남은 원래 특징 이름, 새 component 이름, 교차검증 점수와 입력 모양
- 확인할 개념:
  - 필터와 RFE는 원래 특징 중 일부를 고른다
  - PCA는 원래 특징 이름을 유지하지 않고 새 축으로 다시 표현한다
  - 점수가 비슷해 보여도 해석 가능성은 서로 다르다

```python
from sklearn.datasets import make_classification
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE, SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

feature_names = [
    "visit_count",
    "avg_order",
    "discount_click",
    "support_calls",
    "days_since_login",
    "newsletter_open",
]

X, y = make_classification(
    n_samples=180,
    n_features=6,
    n_informative=3,
    n_redundant=1,
    class_sep=1.1,
    random_state=7,
    shuffle=False,
)

filter_selector = SelectKBest(score_func=f_classif, k=3).fit(X, y)
filter_features = [
    name for name, keep in zip(feature_names, filter_selector.get_support()) if keep
]

base_model = LogisticRegression(max_iter=1000)
rfe_selector = RFE(base_model, n_features_to_select=3).fit(
    StandardScaler().fit_transform(X),
    y,
)
rfe_features = [
    name for name, keep in zip(feature_names, rfe_selector.support_) if keep
]

models = {
    "filter_selected": X[:, filter_selector.get_support()],
    "rfe_selected": X[:, rfe_selector.support_],
}

print("filter keeps:", filter_features)
print("rfe keeps   :", rfe_features)
print("pca output  :", ["component_1", "component_2", "component_3"])

for name, selected_X in models.items():
    score = cross_val_score(base_model, selected_X, y, cv=5).mean()
    print(name, "cv=", round(score, 3), "shape=", selected_X.shape)

pca_score = cross_val_score(
    make_pipeline(StandardScaler(), PCA(n_components=3), base_model),
    X,
    y,
    cv=5,
).mean()
print("pca_reduced cv=", round(pca_score, 3), "shape=", (X.shape[0], 3))
```

실행 결과는 다음과 같습니다.

```text
filter keeps: ['visit_count', 'discount_click', 'support_calls']
rfe keeps   : ['visit_count', 'avg_order', 'support_calls']
pca output  : ['component_1', 'component_2', 'component_3']
filter_selected cv= 0.817 shape= (180, 3)
rfe_selected cv= 0.828 shape= (180, 3)
pca_reduced cv= 0.617 shape= (180, 3)
```

이 출력에서 먼저 볼 것은 점수 순위가 아닙니다. 필터와 RFE는 서로 다른 원래 특징 목록을 남겼고, PCA는 같은 세 칸으로 줄였지만 원래 컬럼명이 사라졌습니다. 따라서 `세 개로 줄였다`는 말만으로는 충분하지 않습니다. 원래 특징을 남긴 선택인지, 새 표현으로 압축한 차원 축소인지까지 함께 읽어야 합니다.

## 체크리스트

- 지금 하려는 일이 원래 칼럼을 고르는 일인지, 새 축으로 다시 만드는 일인지 구분했는가?
- 빠른 1차 정리와 모델 기반 반복 비교를 같은 방식으로 말하고 있지 않은가?
- 해석 가능성이 중요할 때 차원 축소보다 특징 선택이 왜 더 나을 수 있는지 설명할 수 있는가?
- 통계 검정 기반 특징 선택은 보통 필터 접근으로, RFE는 모델을 반복 학습하며 특징을 줄이는 래퍼 접근으로 이해할 수 있는가
- 차원 축소가 특징 선택과 비슷해 보여도 원래 특징을 새 축으로 다시 표현하는 별도 문제라는 점을 설명할 수 있는가
- 필터, 래퍼, 임베디드, 차원 축소를 같은 방식의 해결책처럼 섞지 않고 구분할 수 있는가

## 출처와 참고 자료

- scikit-learn developers, [Feature selection](https://scikit-learn.org/stable/modules/feature_selection.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-01.
- scikit-learn developers, [Unsupervised dimensionality reduction](https://scikit-learn.org/stable/modules/unsupervised_reduction.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-01.
- Trevor Hastie, Robert Tibshirani, Jerome Friedman, [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-01.

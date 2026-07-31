# P4-12.3 k-NN을 사용할 때 무엇을 먼저 점검할까

> Section ID: `P4-12.3`
> Version: `v2026.07.31`

P4-12.1에서 k-NN의 직관을 보았고, P4-12.2에서 [거리(distance)](../../../reference/concept-glossary-parts/01-giyeok.md#distance)와 [특징 스케일(feature scale)](../../../reference/concept-glossary-parts/13-pieup.md#standardization)이 왜 결과를 바꾸는지 보았습니다. 이제 남는 질문은 이것입니다.

k-NN의 판단이 흔들릴 때는 무엇을 먼저 다시 봐야 하는가?

이 절의 목적은 전처리 일반론을 다시 설명하는 것이 아니라, k-NN을 읽을 때 `어디를 먼저 점검해야 하는가`를 정리하는 것입니다.

## k-NN을 사용할 때 무엇을 먼저 점검할까에서 닫을 질문

이 절은 다음 질문에 답합니다.

- 어떤 문제에서 k-NN을 먼저 후보로 올릴 수 있는가?
- 어떤 신호가 보이면 거리나 스케일 문제를 먼저 의심해야 하는가?
- `거리 규칙`, `k`, `데이터 표현` 중 무엇을 먼저 다시 봐야 하는가?
- 검토(review)가 필요한 query를 어떻게 읽어야 하는가?

## k-NN을 사용할 때 무엇을 먼저 점검할까에서 남길 판단 기준

- k-NN을 먼저 후보로 올릴 만한 문제를 설명할 수 있습니다.
- 거리나 스케일 문제를 의심해야 하는 신호를 설명할 수 있습니다.
- 결과가 흔들릴 때 무엇부터 다시 볼지 순서를 잡을 수 있습니다.

## k-NN을 먼저 후보로 올릴 수 있는 조건

k-NN은 모든 분류 문제의 기본 해답은 아닙니다. 하지만 `가까운 사례를 근거로 설명하는 방식`이 자연스러운 문제에서는 좋은 첫 비교 후보가 됩니다.

| 현재 문제 상태 | k-NN을 먼저 떠올릴 이유 |
| --- | --- |
| 비슷한 사례끼리 비슷한 결과가 나오는 경향이 있다 | 주변 이웃을 근거로 예측을 설명하기 쉽습니다. |
| 전역 규칙보다 지역 패턴이 더 중요해 보인다 | query 주변 사례를 직접 비교하기 좋습니다. |
| 모델의 식보다 예시 기반 판단을 먼저 보여 주고 싶다 | 어떤 이웃을 봤는지 자체가 설명 근거가 됩니다. |
| 데이터 수가 아주 크지 않고 비교 비용을 감당할 수 있다 | 예측 시 비교 작업이 현실적으로 가능합니다. |

핵심은 `식을 못 세워서 k-NN을 쓴다`가 아니라, `지역적 유사성을 먼저 보는 것이 자연스러운 문제에서 k-NN이 좋은 출발점이 될 수 있다`는 점입니다.

### 어떤 신호가 보이면 거리나 스케일 문제를 먼저 의심해야 하는가

거리 기반 모델에서는 성능이 이상할 때 모델 구조보다 먼저 `무슨 축이 거리를 거의 혼자 결정하고 있는가`를 의심해야 하는 경우가 많습니다.

| 보이는 신호 | 먼저 의심할 것 | 이유 |
| --- | --- | --- |
| 어떤 칼럼만 숫자 범위가 매우 크다 | 스케일 지배 | 큰 축이 거리를 독점할 수 있기 때문입니다. |
| 스케일 조정 전후 이웃이 크게 바뀐다 | 표현 의존성 | 가까움의 정의가 표현 변화에 민감하다는 뜻입니다. |
| 작은 범위 칼럼이 중요한데 예측에 잘 반영되지 않는다 | 큰 축에 의한 가림 | 중요한 정보가 거리 계산에서 묻힐 수 있습니다. |
| 같은 유형의 query가 반복해서 경계 근처에 몰린다 | 거리 규칙 또는 `k` 설정 | 이웃 순서가 쉽게 흔들리고 있다는 신호일 수 있습니다. |

이 표의 목적은 스케일 조정을 만능 해법으로 두는 것이 아니라, `가까움의 정의가 이미 흔들리고 있는지`를 먼저 확인하게 만드는 데 있습니다.

### 무엇을 먼저 다시 볼 것인가

결과가 흔들릴 때는 보통 다음 순서로 점검하는 편이 좋습니다.

1. 이 문제가 정말 `가까운 사례 비교`로 읽히는 문제인가
2. 거리 규칙이 현재 문제와 맞는가
3. `k`가 너무 작거나 너무 크지 않은가
4. 스케일이나 데이터 표현이 특정 축을 과하게 밀고 있지 않은가
5. 예측 시 비교 비용을 실제로 감당할 수 있는가

이 순서가 중요한 이유는 각 질문이 서로 다른 종류의 문제를 가리키기 때문입니다.

- 1번은 `모델 계열`의 문제입니다.
- 2번과 3번은 `판단 규칙`의 문제입니다.
- 4번은 `표현`의 문제입니다.
- 5번은 `운영 비용`의 문제입니다.

즉, `결과가 이상하다`는 한 문장 안에도 서로 다른 층위의 원인이 섞여 있을 수 있습니다.

특히 4번에서 실제로 스케일 문제나 표현 문제를 의심하게 되면, 전처리 일반론 자체는 이 절에서 다시 길게 풀지 않고 [P4-7.2 전처리(preprocessing)](../chapter-07/section-02.md)로 돌아가 기준을 다시 확인하는 편이 맞습니다.

### P4-12.1의 같은 query를 다시 읽어 보면

앞 절에서 본 query `(4.0, 4.2)`를 다시 가져오면, 점검 순서는 더 구체적으로 읽힙니다.

| 다시 볼 질문 | `(4.0, 4.2)`에서 실제로 보는 것 | 지금 내릴 판단 |
| --- | --- | --- |
| `k`가 너무 민감한가 | `k=1`에서는 class 1, `k=3`에서는 class 0으로 바뀐다 | 한 점 예외에 흔들릴 수 있으니 `k`를 다시 본다 |
| 이웃 구성이 갈리는가 | 가까운 이웃 label이 `1, 0, 0, 1, 0`처럼 섞여 있다 | 경계 근처 query일 가능성이 높다 |
| 거리 규칙을 바꾸면 달라질까 | 같은 좌표라도 거리 규칙에 따라 이웃 순서가 바뀔 수 있다 | `P4-12.2`의 거리 규칙 비교로 이어서 본다 |
| 스케일 문제까지 의심할 상황인가 | 지금 예시는 같은 좌표 축이라 스케일 문제는 약하다 | 숫자 범위가 다른 실제 데이터에서는 `P4-7.2`, `P4-12.2`를 다시 본다 |

이 표의 목적은 체크리스트를 외우게 하는 것이 아니라, `한 query를 붙잡고 어디서부터 다시 의심할지`를 순서대로 보여 주는 데 있습니다.

### 하나의 query를 끝까지 점검하는 작은 흐름

앞의 표를 실제 판단 순서로 다시 압축하면, `결과가 애매하다`는 말은 그냥 느낌이 아니라 `어느 단계에서 흔들렸는지`를 다시 찾는 일로 바뀝니다.

1. 먼저 이웃 구성이 한쪽으로 분명히 쏠리는지 봅니다.
2. 한두 점 차이로 갈리면 `k`를 바꿨을 때 해석이 유지되는지 봅니다.
3. `k`를 조금 바꿔도 계속 흔들리면 거리 규칙 자체가 현재 문제와 맞는지 봅니다.
4. 숫자 범위가 크게 다른 특징이 있으면, 마지막으로 스케일과 데이터 표현을 다시 봅니다.

즉, 검토(review) query는 `틀린 예측 한 건`이라기보다 `판단 규칙의 어느 층이 흔들리는지 보여 주는 관찰 지점`으로 읽는 편이 맞습니다.

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-3-mermaid-01-ko.mmd"
```

### 검토(review)가 필요한 query는 어떻게 읽어야 하는가

검토(review)가 필요한 query는 보통 `이웃 구성이 한쪽으로 확실히 쏠리지 않는 경우`입니다.

예를 들면 다음과 같습니다.

| query | nearest labels | 지금 읽기 |
| --- | --- | --- |
| `(4.0, 4.2)` | `[1, 0, 1]` | class 1 쪽이지만 경계 근처일 수 있음 |
| `(4.0, 4.2)` with `k=5` | `[1, 0, 1, 0, 0]` | `k`를 넓히자 해석이 바뀌는지 다시 확인 필요 |

이때 중요한 점은 `이웃이 갈렸다`는 사실이 곧 원인 설명의 끝은 아니라는 것입니다. 그것은 먼저 `어디를 다시 봐야 하는가`를 알려 주는 신호에 가깝습니다.

즉, 검토(review) query는 보통 다음 순서로 읽습니다.

1. 이웃 구성이 얼마나 갈렸는가
2. `k`를 바꾸면 해석이 유지되는가
3. 거리 규칙을 바꾸면 이웃이 달라지는가
4. 스케일 조정 전후에 어떤 이웃이 들어오고 나가는가

이 네 질문이 중요한 이유는, 각각이 서로 다른 원인을 겨누기 때문입니다.

- 1번은 `지금 query가 경계 근처인가`를 봅니다.
- 2번은 `한두 이웃 예외에 과민한가`를 봅니다.
- 3번은 `가까움의 정의가 현재 문제와 맞는가`를 봅니다.
- 4번은 `표현 방식이 판단을 왜곡하고 있는가`를 봅니다.

## 사례 및 예시

### 사례 1. 예측은 되지만 설명이 자꾸 흔들릴 때

구독 서비스 팀이 k-NN으로 이탈 가능성을 보고 있습니다. 점수 자체는 어느 정도 나오지만, 비슷해 보이는 고객 두 명이 서로 다른 예측을 받을 때가 반복됩니다.

이때 바로 `다른 모델로 갈아타야 하나`로 뛰기보다, 먼저 다음을 다시 봅니다.

- 이 문제가 지역적 유사성으로 읽히는지
- 거리 규칙이 현재 특징에 맞는지
- `k=1`처럼 너무 민감한 설정을 쓰고 있지 않은지
- 결제 금액 같은 큰 축이 다른 특징을 압도하고 있지 않은지

이 순서를 거치면 `모델 자체의 실패`와 `판단 기준의 흔들림`을 조금 더 분리해서 읽을 수 있습니다.

즉, 여기서 남길 기준은 `k-NN은 조심해서 써야 한다`는 막연한 결론이 아닙니다. 더 정확히는 `예측이 흔들릴 때도 어디를 먼저 다시 보면 되는지`를 독자가 스스로 말할 수 있게 만드는 것입니다.

## 연습 및 예제

이번 예제는 같은 query를 놓고 `k`와 스케일 조정 여부가 이웃 목록과 예측을 어떻게 바꾸는지 확인합니다.

- 문제 상황: 월 결제 금액과 문의 횟수로 이탈 여부를 k-NN으로 판단한다
- 입력(input): 고객별 `monthly_spend`, `support_tickets`, `churn`
- 기대 출력(output): `k`별 예측, 가까운 이웃 ID, 스케일 조정 후 이웃 변화
- 확인할 개념:
  - `k=1`은 가장 가까운 한 사례에 크게 흔들릴 수 있다
  - `k`를 키우면 주변 다수결이 바뀔 수 있다
  - 숫자 범위가 다른 특징은 스케일 조정 전후 이웃 순서를 바꿀 수 있다

조작해 볼 값:

- `query`의 `support_tickets`를 `2`, `5`, `9`로 바꾸면 검토가 필요한 query가 언제 생기는지 볼 수 있습니다.
- `n_neighbors`를 `2`, `4`처럼 짝수로 바꾸면 동률이나 근소한 다수결을 어떻게 기록해야 하는지도 확인할 수 있습니다.

```python
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

customers = pd.DataFrame(
    [
        {"id": "A", "monthly_spend": 30, "support_tickets": 0, "churn": 0},
        {"id": "B", "monthly_spend": 58, "support_tickets": 0, "churn": 0},
        {"id": "C", "monthly_spend": 61, "support_tickets": 0, "churn": 0},
        {"id": "D", "monthly_spend": 65, "support_tickets": 0, "churn": 0},
        {"id": "E", "monthly_spend": 40, "support_tickets": 8, "churn": 1},
        {"id": "F", "monthly_spend": 62, "support_tickets": 8, "churn": 1},
        {"id": "G", "monthly_spend": 90, "support_tickets": 9, "churn": 1},
    ]
)

X = customers[["monthly_spend", "support_tickets"]]
y = customers["churn"]
query = pd.DataFrame([{"monthly_spend": 63, "support_tickets": 7}])

for k in [1, 3, 5]:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X, y)
    distances, indices = model.kneighbors(query, n_neighbors=k)
    neighbor_ids = customers.iloc[indices[0]]["id"].tolist()
    print("raw k=", k, "prediction=", int(model.predict(query)[0]), "neighbors=", neighbor_ids)

scaled_model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
scaled_model.fit(X, y)
knn = scaled_model.named_steps["kneighborsclassifier"]
scaled_query = scaled_model.named_steps["standardscaler"].transform(query)
distances, indices = knn.kneighbors(scaled_query, n_neighbors=3)
neighbor_ids = customers.iloc[indices[0]]["id"].tolist()
print("scaled k= 3 prediction=", int(scaled_model.predict(query)[0]), "neighbors=", neighbor_ids)
```

실행 결과는 다음과 같습니다.

```text
raw k= 1 prediction= 1 neighbors= ['F']
raw k= 3 prediction= 0 neighbors= ['F', 'C', 'D']
raw k= 5 prediction= 0 neighbors= ['F', 'C', 'D', 'B', 'E']
scaled k= 3 prediction= 1 neighbors= ['F', 'E', 'G']
```

이 출력은 `k-NN이 틀렸다`고 바로 말하라는 뜻이 아닙니다. 같은 query라도 `k=1`에서는 가장 가까운 F 하나에 끌려가고, `k=3`에서는 C와 D가 들어오면서 예측이 바뀝니다. 또 스케일을 맞추면 문의 횟수가 거리 계산에서 더 분명히 반영되어 E와 G가 가까운 이웃으로 들어옵니다. 따라서 흔들리는 query를 보면 먼저 `k`, 이웃 구성, 스케일을 순서대로 다시 열어 봐야 합니다.

## 체크리스트

- k-NN이 지역적 유사성이 중요한 문제에서 좋은 첫 비교 후보가 될 수 있다는 점을 설명할 수 있는가?
- k-NN을 먼저 떠올릴 만한 문제와 아닌 문제를 구분할 수 있는가?
- 결과가 흔들릴 때는 모델 이름보다 `거리 규칙`, `k`, `데이터 표현`을 먼저 다시 보는 편이 맞다는 점을 이해했는가?
- 결과가 흔들릴 때 `거리 규칙`, `k`, `스케일`을 어떤 순서로 볼지 설명할 수 있는가?
- 검토(review) query를 `원인 확정`이 아니라 `재점검 신호`로 읽고 있는가?

## 출처와 참고 자료

- scikit-learn, *Nearest Neighbors*, scikit-learn User Guide, 확인 날짜: 2026-07-26. <https://scikit-learn.org/stable/modules/neighbors.html>{: target="_blank" rel="noopener noreferrer" }
- scikit-learn, *Importance of Feature Scaling*, scikit-learn Examples, 확인 날짜: 2026-07-26. <https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html>{: target="_blank" rel="noopener noreferrer" }

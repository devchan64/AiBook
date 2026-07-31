# P7-2.2 회고와 다음 질문 만들기

> Section ID: `P7-2.2`
> Version: `v2026.07.31`

기준점(baseline)과 모델을 나란히 두고 비교했다면, 다음으로 필요한 일은 그 차이를 회고와 다음 질문으로 넘기는 것입니다.

개선(improvement)은 무엇을 기준으로 말해야 하는가? 그 질문을 정리합니다. 개선은 점수가 올랐다는 말이 아니라, 같은 기준에서 기준점보다 무엇이 달라졌는지 설명하는 일입니다.

## 개선을 주장하는 기준

- 기준점(baseline) 대비 개선을 어떻게 문서화해야 하는가?
- 정확도(accuracy)만 적는 것보다 무엇을 더 같이 남겨야 하는가?
- 전처리(preprocessing)가 실제 예측 사례를 어떻게 바꾸는가?

핵심은 기준점 대비 개선을 `같은 기준에서 무엇이 달라졌는가`라는 기록으로 바꾸는 데 있습니다. 점수 상승만 적는 것이 아니라, 어떤 샘플이 왜 달라졌는지까지 남겨야 개선이 다음 반복의 판단 근거가 됩니다.

개선이라는 말을 어떤 비교 근거 위에서 써야 하는지 정리하는 자리입니다. `좋아졌다`는 말은 같은 평가 셋, 같은 비교 기준, 같은 사례 묶음 위에서만 써야 한다는 기준을 여기서 세웁니다.

Part 7에서 `기준선(baseline)`과 `평가(evaluation)`라는 말을 다시 섞어 쓰게 되면, 비교 기준을 먼저 고정한 이 절과 개념사전의 [기준선(baseline)](../../../reference/concept-glossary-parts/01-giyeok.md#baseline), [평가(evaluation)](../../../reference/concept-glossary-parts/13-pieup.md#evaluation-design) 항목으로 돌아오면 됩니다.

## 판단 기준

- 기준점과 개선 모델의 차이를 표와 문장으로 정리할 수 있습니다.
- 전처리가 왜 실제 예측 경로를 바꾸는지 설명할 수 있습니다.
- `잘 맞았다`보다 `왜 기준점보다 나아졌는가`를 우선 기록하는 습관을 만들 수 있습니다.

## 개선을 말하기 전에 남겨야 할 것

프로젝트에서 개선을 주장하려면 최소한 다음 네 가지가 같이 있어야 합니다.

| 항목 | 왜 필요한가 |
| --- | --- |
| 기준점(baseline) | 최소 기준점이 있어야 모델 개선의 의미를 읽을 수 있습니다. |
| 같은 평가 셋 | 비교 대상이 달라지면 점수 차이를 해석하기 어렵습니다. |
| 예측값 사례 | 숫자 하나만으로는 어떤 샘플에서 달라졌는지 알기 어렵습니다. |
| 한계 기록 | 제한된 데이터, synthetic 데이터, 우연한 결과 가능성을 남겨야 합니다. |

즉, 개선은 숫자 하나가 아니라 `비교 가능한 기록 묶음`입니다.

개선이라는 말을 쓰기 전에 붙들어야 할 비교 기준을 표로 고정하면 다음과 같습니다.

| 질문 | 짧은 답 |
| --- | --- |
| 개선을 주장하려면 무엇이 필요한가? | 같은 기준에서의 비교 |
| 무엇을 꼭 같이 남겨야 하는가? | 기준점, 같은 평가 셋, 예측 사례, 한계 |
| 그래서 프로젝트 문서가 하는 일은 무엇인가? | 성과를 과장하지 않고 비교 근거를 남기는 일 |

## 같은 결과를 표로 다시 읽기

P7-2.1의 결과를 같은 기록 구조로 정리하면 다음처럼 쓸 수 있습니다.

| 모델 | 설명 | 평가 정확도 |
| --- | --- | ---: |
| 기준점(baseline) | 모든 고객을 `유지`로만 예측 | 0.500 |
| raw 1-NN | 세 특징의 raw 거리를 그대로 사용 | 0.667 |

이 표만으로도 중요한 사실 하나가 드러납니다.

`이번 데이터에서는 특징을 실제로 사용하는 모델이 baseline보다 낫다.`

하지만 좋은 프로젝트 문서는 여기서 멈추지 않습니다.

## 예측 사례를 같이 읽기

숫자와 함께 샘플별 예측을 붙이면 차이가 더 분명해집니다.

| 평가 샘플 | 실제 정답 | baseline 예측 | raw 1-NN 예측 | 읽어야 할 점 |
| --- | ---: | ---: | ---: | --- |
| 평가-02 | 1 | 0 | 0 | 이탈 위험인데 high-usage retained 고객과 가까워져 놓쳤다 |
| 평가-03 | 1 | 0 | 1 | raw 1-NN이 baseline보다 한 단계 더 잡아냈다 |
| 평가-04 | 0 | 0 | 1 | 사용 시간이 비슷한 이탈 고객 쪽으로 끌려 잘못 분류했다 |
| 평가-05 | 1 | 0 | 1 | 문의 수와 미접속 일수 신호가 실제로 작동했다 |

이 표를 보면 raw 1-NN은 baseline보다 분명히 낫지만, 사용 시간(분) 스케일이 너무 커서 다른 특징보다 거리 계산을 더 많이 흔들고 있음을 짐작할 수 있습니다.

즉, 개선의 핵심은 단순히 점수가 오른 것이 아니라 `무엇이 여전히 잘못 읽히는가`까지 같이 남기는 데 있습니다.

예를 들어 `평가-02`를 빠르게 읽으면 `raw 1-NN도 결국 틀렸으니 별 차이 없는 모델`이라고 넘기기 쉽습니다. 하지만 실제로는 그렇지 않습니다. baseline은 모든 이탈 위험 고객을 놓치고 있고, raw 1-NN은 이미 `평가-03`, `평가-05` 같은 사례를 잡아내고 있습니다. 따라서 여기서 더 안전한 다음 판단은 `효과가 없었다`고 닫는 것이 아니라, `무엇이 아직 거리 계산을 흔드는가`를 찾아보는 것입니다. 그 흔들림은 사용 시간 축의 과도한 영향으로 드러나며, 그래서 다음 행동이 `정규화 전후를 같은 평가 셋에서 다시 비교한다`로 이어집니다.

```mermaid
--8<-- "assets/part-07/chapter-02/p7-2-2-raw-distance-risk-flow-ko.mmd"
```

## 전처리(preprocessing)를 실제로 비교하기

train 데이터의 평균과 표준편차를 이용해 z-score 정규화를 적용해 봅니다. 예제에서는 정확도 숫자만 한 줄로 끝내지 않고, `raw 1-NN`, `정규화 후 1-NN`, `샘플별 변화 여부`를 함께 남기겠습니다.

- 문제 상황: 같은 평가 셋에서 raw 거리와 정규화 후 거리를 비교한다.
- 입력: 미해결 문의 수, 최근 접속 후 경과 일수, 최근 30일 사용 시간
- 기대 출력: 정규화 전후 정확도, 최근접 학습 샘플, 예측 변화 여부
- 확인할 개념:
  - 개선은 같은 평가 셋에서 비교해야 읽을 수 있다
  - 전처리는 점수만이 아니라 최근접 이웃 선택 자체를 바꿀 수 있다
  - 샘플별 변화 여부를 남겨야 전처리 효과를 과장하지 않게 된다

같은 흐름에서 P7-2.1과 같은 [`p7-2-churn-dataset.csv`](../../../assets/part-07/chapter-02/p7-2-churn-dataset.csv){ .csv-preview }를 그대로 읽습니다. 이렇게 두면 `같은 데이터 파일` 위에서 기준점 비교와 전처리 개선을 연속해서 확인할 수 있습니다.

예제의 1-NN 모델과 정규화는 scikit-learn으로 실행합니다. `Pipeline`은 전처리와 모델을 하나의 실행 묶음으로 연결해, 평가 데이터에 같은 정규화 기준이 적용되도록 도와줍니다.

## 실행 기록 기준

- 정규화 전후가 같은 train/test 분리를 쓰는지 확인합니다.
- 정확도 변화와 예측 변화 샘플 수를 함께 적습니다.
- 예측이 바뀐 샘플에서 최근접 학습 샘플이 어떻게 달라졌는지 봅니다.
- 개선된 사례와 여전히 확인해야 할 한계를 같은 회고 문장 안에 남깁니다.

## Python 예제

```python
# scikit-learn 1-NN 모델에서 정규화 전후의 최근접 샘플과 예측 변화를 비교하는 예제입니다.
import csv
from pathlib import Path

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

data_path = Path("docs/assets/part-07/chapter-02/p7-2-churn-dataset.csv")
rows = list(csv.DictReader(data_path.open(encoding="utf-8")))

for row in rows:
    row["미해결 문의 수"] = int(row["unresolved_tickets"])
    row["최근 접속 후 경과 일수"] = int(row["days_since_login"])
    row["최근 30일 사용 시간"] = int(row["usage_minutes_30d"])
    row["정답"] = int(row["label"])
    row["샘플"] = row["sample_id"]

train_rows = [row for row in rows if row["split"] == "train"]
test_rows = [row for row in rows if row["split"] == "test"]

feature_columns = ["미해결 문의 수", "최근 접속 후 경과 일수", "최근 30일 사용 시간"]

X_train = np.array([
    [row[column] for column in feature_columns]
    for row in train_rows
], dtype=float)
y_train = np.array([row["정답"] for row in train_rows])

X_test = np.array([
    [row[column] for column in feature_columns]
    for row in test_rows
], dtype=float)
y_test = np.array([row["정답"] for row in test_rows])

raw_model = KNeighborsClassifier(n_neighbors=1)
raw_model.fit(X_train, y_train)

# 조작 변수: StandardScaler를 다른 전처리기로 바꾸면 최근접 이웃 선택이 어떻게 달라지는지 비교할 수 있습니다.
scaled_model = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=1)),
])
scaled_model.fit(X_train, y_train)

raw_knn_pred = raw_model.predict(X_test)
raw_neighbor_indices = raw_model.kneighbors(X_test, return_distance=False).ravel()
raw_nearest_ids = [train_rows[index]["샘플"] for index in raw_neighbor_indices]

scaled_knn_pred = scaled_model.predict(X_test)
scaled_test = scaled_model.named_steps["scaler"].transform(X_test)
scaled_neighbor_indices = scaled_model.named_steps["knn"].kneighbors(
    scaled_test,
    return_distance=False,
).ravel()
scaled_nearest_ids = [train_rows[index]["샘플"] for index in scaled_neighbor_indices]

train_mean = scaled_model.named_steps["scaler"].mean_
train_std = scaled_model.named_steps["scaler"].scale_

comparison_rows = []
for index, row in enumerate(test_rows):
    comparison_rows.append({
        "평가 샘플": row["샘플"],
        "실제 정답": row["정답"],
        "정규화 전 예측": int(raw_knn_pred[index]),
        "정규화 후 예측": int(scaled_knn_pred[index]),
        "정규화 전 정답 여부": "예" if raw_knn_pred[index] == y_test[index] else "아니오",
        "정규화 후 정답 여부": "예" if scaled_knn_pred[index] == y_test[index] else "아니오",
        "예측 변화 여부": "예" if raw_knn_pred[index] != scaled_knn_pred[index] else "아니오",
        "정규화 전 최근접 학습 샘플": raw_nearest_ids[index],
        "정규화 후 최근접 학습 샘플": scaled_nearest_ids[index],
    })

project_comparison = {
    "정규화 전 정확도": round(float((raw_knn_pred == y_test).mean()), 3),
    "정규화 후 정확도": round(float((scaled_knn_pred == y_test).mean()), 3),
    "예측 변화 샘플 수": sum(row["예측 변화 여부"] == "예" for row in comparison_rows),
    "정규화 전 실패 샘플": [
        row["평가 샘플"] for row in comparison_rows if row["정규화 전 정답 여부"] == "아니오"
    ],
    "정규화 후 실패 샘플": [
        row["평가 샘플"] for row in comparison_rows if row["정규화 후 정답 여부"] == "아니오"
    ],
}

print("학습 평균 =", np.round(train_mean, 2).tolist())
print("학습 표준편차 =", np.round(train_std, 2).tolist())
print("비교 요약 =", project_comparison)
print("읽은 파일 =", str(data_path))
print("샘플별 비교 =")
for row in comparison_rows:
    print(row)
```

실행 결과 예시는 다음과 같습니다.

```text
학습 평균 = [3.83, 12.83, 3158.33]
학습 표준편차 = [2.34, 8.52, 570.76]
비교 요약 = {'정규화 전 정확도': 0.667, '정규화 후 정확도': 1.0, '예측 변화 샘플 수': 2, '정규화 전 실패 샘플': ['평가-02', '평가-04'], '정규화 후 실패 샘플': []}
읽은 파일 = docs/assets/part-07/chapter-02/p7-2-churn-dataset.csv
샘플별 비교 =
{'평가 샘플': '평가-01', '실제 정답': 0, '정규화 전 예측': 0, '정규화 후 예측': 0, '정규화 전 정답 여부': '예', '정규화 후 정답 여부': '예', '예측 변화 여부': '아니오', '정규화 전 최근접 학습 샘플': '학습-03', '정규화 후 최근접 학습 샘플': '학습-03'}
{'평가 샘플': '평가-02', '실제 정답': 1, '정규화 전 예측': 0, '정규화 후 예측': 1, '정규화 전 정답 여부': '아니오', '정규화 후 정답 여부': '예', '예측 변화 여부': '예', '정규화 전 최근접 학습 샘플': '학습-02', '정규화 후 최근접 학습 샘플': '학습-08'}
{'평가 샘플': '평가-03', '실제 정답': 1, '정규화 전 예측': 1, '정규화 후 예측': 1, '정규화 전 정답 여부': '예', '정규화 후 정답 여부': '예', '예측 변화 여부': '아니오', '정규화 전 최근접 학습 샘플': '학습-09', '정규화 후 최근접 학습 샘플': '학습-09'}
{'평가 샘플': '평가-04', '실제 정답': 0, '정규화 전 예측': 1, '정규화 후 예측': 0, '정규화 전 정답 여부': '아니오', '정규화 후 정답 여부': '예', '예측 변화 여부': '예', '정규화 전 최근접 학습 샘플': '학습-11', '정규화 후 최근접 학습 샘플': '학습-04'}
{'평가 샘플': '평가-05', '실제 정답': 1, '정규화 전 예측': 1, '정규화 후 예측': 1, '정규화 전 정답 여부': '예', '정규화 후 정답 여부': '예', '예측 변화 여부': '아니오', '정규화 전 최근접 학습 샘플': '학습-11', '정규화 후 최근접 학습 샘플': '학습-11'}
{'평가 샘플': '평가-06', '실제 정답': 0, '정규화 전 예측': 0, '정규화 후 예측': 0, '정규화 전 정답 여부': '예', '정규화 후 정답 여부': '예', '예측 변화 여부': '아니오', '정규화 전 최근접 학습 샘플': '학습-05', '정규화 후 최근접 학습 샘플': '학습-06'}
```

## 결과를 어떻게 읽는가

이번 데이터에서는 정규화 후 정확도가 `0.667 -> 1.000`으로 바뀌었습니다. 이 변화는 숫자 하나보다 `어떤 샘플이 왜 뒤집혔는가`를 먼저 읽어야 합니다.

| 평가 샘플 | 정규화 전 | 정규화 후 | 읽어야 할 점 |
| --- | --- | --- | --- |
| 평가-02 | 유지(오답), 최근접 `학습-02` | 이탈 위험(정답), 최근접 `학습-08` | raw 거리에서는 사용 시간 4050분이 너무 강하게 작용해 retained 고객 쪽으로 끌렸다 |
| 평가-04 | 이탈 위험(오답), 최근접 `학습-11` | 유지(정답), 최근접 `학습-04` | 정규화 후에는 문의 수와 미접속 일수 차이가 더 제대로 반영됐다 |

즉, 전처리는 단순히 보기 좋은 수치 정리가 아니라, `모델이 누구를 가장 비슷한 고객으로 보느냐`를 실제로 바꿀 수 있습니다.

이 결과를 두 방향으로 읽을 수 있습니다.

- 좋은 점: 예제에서는 스케일 차이를 정리하자 최근접 이웃 선택이 더 합리적으로 바뀌었습니다.
- 남는 질문: 더 큰 데이터나 다른 특징 조합에서도 같은 개선이 유지되는지는 아직 확인이 더 필요합니다.

여기서 중요한 것은 `변화 있음`이 항상 성공이라는 뜻은 아니고, `변화 없음`이 항상 실패라는 뜻도 아니라는 점입니다. 핵심은 변화가 생겼다면 `어느 샘플이 왜 바뀌었는지`를 설명할 수 있어야 한다는 것입니다.

실행 결과는 다음 세 줄로 요약할 수 있습니다.

- 정규화는 예측 점수뿐 아니라 최근접 이웃 선택을 바꿨다.
- `평가-02`, `평가-04`는 raw 거리의 한계가 드러난 대표 사례다.
- 전처리 개선은 숫자 하나보다 샘플별 변화와 실패 목록으로 기록해야 한다.

## 결과 해석 기준

| 관찰 | 읽어야 할 뜻 |
| --- | --- |
| 정확도가 0.667에서 1.000으로 오른다 | 이번 평가 셋에서는 정규화가 분명한 개선을 만들었다 |
| 예측 변화 샘플 수는 2건이다 | 개선은 전체가 아니라 특정 경계 사례에서 생겼다 |
| `평가-02`의 최근접 이웃이 바뀐다 | 사용 시간 축이 raw 거리에서 과하게 작동했을 가능성이 있다 |
| 실패 샘플이 0건이 된다 | 그래도 synthetic 소규모 데이터라 일반화 단정은 아직 이르다 |

## 프로젝트 기록 예시

```text
비교 기준:
정규화 전 결과:
정규화 후 결과:
예측이 바뀐 샘플:
최근접 이웃 변화:
개선으로 볼 근거:
아직 단정하지 않을 한계:
다음 반복 질문:
```

## 회고 문장 예시

이 프로젝트의 회고는 다음처럼 정리할 수 있습니다.

> 이번 구독 고객 이탈 위험 예측 실습에서 baseline 정확도는 0.500, raw 1-NN 정확도는 0.667, 정규화 후 1-NN 정확도는 1.000이었다. raw 거리에서는 사용 시간(분) 축이 지나치게 크게 작용해 `평가-02`, `평가-04`에서 잘못된 최근접 이웃을 골랐지만, z-score 정규화 뒤에는 문의 수와 미접속 일수 정보가 함께 반영되며 두 샘플이 모두 정답으로 바뀌었다. 다만 데이터가 작고 synthetic이므로 이 개선을 일반화 성능 향상으로 바로 단정하기보다, 다음 단계에서는 더 많은 고객 구간과 다른 분할에서 같은 패턴이 유지되는지 다시 확인해야 한다.

이 문단에는 `숫자`, `해석`, `한계`, `다음 계획`이 모두 들어 있습니다.

- 숫자만 있으면 보고서가 약하고
- 해석만 있으면 근거가 약하며
- 한계가 없으면 과장되기 쉽고
- 다음 계획이 없으면 반복이 끊깁니다

## 직접 바꿔 보며 확인할 것

개선 효과를 샘플 단위로 확인하려면 다음 두 실험이 특히 유익합니다.

1. 정규화 대신 `usage_minutes_30d`만 임의로 작은 범위로 축소해 봅니다.
   관찰할 점: `평가-02`, `평가-04`가 둘 다 바뀌는가, 아니면 한 샘플만 바뀌는가?

2. 평가 셋에 raw와 normalized가 모두 틀리는 애매한 고객 한 행을 추가해 봅니다.
   관찰할 점: `정확도 개선`은 남아도 회고 문장에 `여전히 남는 실패`가 어떻게 추가되는가?

핵심 확인 기준은 `좋아졌다`는 결론이 아니라 `어떤 샘플은 좋아지고 어떤 샘플은 여전히 남는가`입니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 같은 평가 셋 | 정규화 전후 결과를 같은 평가 샘플에서 비교했는가? |
| 달라진 사례 | 정확도뿐 아니라 예측이 바뀐 샘플을 따로 적었는가? |
| 예측 경로 | 최근접 학습 샘플이 어떻게 바뀌었는지 확인했는가? |
| 한계 | 작은 synthetic 데이터에서 나온 개선임을 과장하지 않았는가? |
| 다음 질문 | 여전히 남는 실패나 더 모을 경계 사례를 적었는가? |

`좋아졌다`는 문장은 이 다섯 칸이 채워진 뒤에만 조심스럽게 쓸 수 있습니다. 개선은 점수 상승이 아니라, 같은 기준에서 어떤 사례가 달라졌고 무엇이 아직 남았는지 설명하는 기록입니다.

## 출처와 참고 자료

- NumPy Developers, `NumPy documentation`, 확인 날짜: 2026-06-29. [https://numpy.org/doc/stable/](https://numpy.org/doc/stable/){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Nearest Neighbors` and `Pipeline`, 확인 날짜: 2026-07-23. [https://scikit-learn.org/stable/modules/neighbors.html](https://scikit-learn.org/stable/modules/neighbors.html){: target="_blank" rel="noopener noreferrer" }, [https://scikit-learn.org/stable/modules/compose.html#pipeline](https://scikit-learn.org/stable/modules/compose.html#pipeline){: target="_blank" rel="noopener noreferrer" }

이 절의 데이터와 비교 예시는 개인정보가 없는 실습용 구독 고객 요약 예시를 위해 직접 구성한 synthetic 데이터입니다.

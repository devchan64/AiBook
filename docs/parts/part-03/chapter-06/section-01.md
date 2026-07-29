# P3-6.1 비교할 구조는 어떤 특징으로 남기는가

> Section ID: `P3-6.1`
> Version: `v2026.07.25`

특징을 처음 배울 때는 `열이 많을수록 좋은 것 아닐까`라고 받아들이곤 합니다. 하지만 [특징(feature)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature)은 단순히 많은 값을 넣는 일이 아닙니다. 특징은 샘플이 가진 구조를 비교와 예측에 쓸 수 있도록 다시 표현한 값입니다. 그래서 좋은 특징은 많기보다, `무엇을 보여 주려는가`가 분명해야 합니다. 앞 절에서 원시 로그를 [요약 표(summary table)](../../../reference/concept-glossary-parts/03-digeut.md#data-modeling)로 바꿨다면, 이제 그 요약 표 안에 어떤 구조를 남길지 정해야 합니다.

특징을 설계한다는 말은 요약 표 안의 숫자를 그대로 쓰는 일이 아니라, 비교하고 싶은 구조를 숫자 표현으로 다시 고르는 일입니다. 그래서 먼저 어떤 구조를 남길지 정한 뒤에야 평균, 기울기, 변동성 같은 특징 후보가 의미를 가집니다. 여기서 한 번 더 갈라지는 판단이 있습니다. 같은 구조를 평균, 차이, 기울기, 토큰, 비율처럼 다른 표현으로 바꾸는 일은 [변수변환(variable transformation)](../../../reference/concept-glossary-parts/13-pieup.md#glossary-variable-transformation)이고, 그렇게 바꾼 표현 중 실제로 남길 항목을 고르는 일은 [특징 선택(feature selection)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature-selection)입니다.

| 관점 | 지금 묻는 질문 | 대표 예 |
| --- | --- | --- |
| 변수변환 | 같은 구조를 어떤 표현으로 바꿀 것인가 | 평균, 구간 차이, 기울기, 비율, 토큰 |
| 특징 선택 | 바꾼 표현 중 무엇을 실제로 남길 것인가 | 전체 수준용 특징, 후반 붕괴 감지용 특징, 변동성 특징 |

자동으로 실행되는 동작 1회를 샘플로 본다고 하겠습니다. 이때 시점별 센서값 전체를 그대로 한 행에 넣을 수는 없습니다. 대신 우리는 동작의 중요한 면을 드러내는 요약값을 만들어야 합니다. 예를 들어 다음 값들은 자주 좋은 출발점이 됩니다.

- 평균(mean)
- 기울기(slope)
- 변동성(variability)
- 최대값이나 최소값
- 특정 구간의 변화율

왜 이런 값들이 자주 등장할까요. 첫째, 원시 곡선을 너무 거칠게 버리지 않으면서도 비교 가능한 숫자로 바꾸기 쉽기 때문입니다. 둘째, 사람이 읽었을 때도 `이번 동작은 평균은 비슷하지만 후반 하강이 더 가파르다`처럼 설명하기 쉽기 때문입니다. 셋째, 같은 평균이라도 변동성이나 기울기가 다르면 실제 구조 차이를 드러낼 수 있기 때문입니다.

즉 좋은 특징은 `많은 값`보다 `적절한 질문`에 더 가깝습니다. 평균은 전체 수준을, 기울기는 방향과 변화 속도를, 변동성은 흔들림의 크기를 보여 줍니다. 서로 다른 특징이 필요한 이유도 각 값이 드러내는 구조가 다르기 때문입니다. 같은 요약 표에서 어떤 변환을 먼저 만들고, 그중 무엇을 남길지 고르는 판단이 바로 변수변환과 특징 선택의 핵심입니다.

| 동작 | 평균 | 기울기 | 변동성 | 읽을 수 있는 구조 |
| --- | --- | --- | --- | --- |
| A | 비슷함 | 완만함 | 낮음 | 비교적 안정적 |
| B | 비슷함 | 급함 | 높음 | 불안정하거나 변화 큼 |

문제 상황: 두 동작의 전체 수준은 비슷하지만, 상승 폭과 흔들림 정도가 다를 때 어떤 특징을 남겨야 하는지 확인합니다.

입력(input): 구간별 평균만 남아 있는 동작 요약 표와 먼저 보고 싶은 구조 `feature_focus`

기대 출력(output): 같은 요약 표에서 수준, 구간 차이, 기울기, 변동성을 각각 계산한 특징 표. `feature_focus`를 바꾸면 어떤 특징을 우선 남길지도 달라진다.

확인할 개념: 특징은 이미 있던 열을 그대로 나열하는 것이 아니라, 비교하고 싶은 구조를 계산해 붙인 표현이다. 특징 선택은 질문 초점에 따라 달라진다.

```python
# 구간 요약값에서 비교 목적에 맞는 특징을 만들어 선택하는 예제입니다.
from statistics import mean, stdev

feature_focus = "change"

segment_summary = [
    {"event_id": "A", "early_flow_mean": 1.8, "mid_flow_mean": 2.2, "late_flow_mean": 2.6},
    {"event_id": "B", "early_flow_mean": 2.1, "mid_flow_mean": 2.2, "late_flow_mean": 2.3},
]

feature_table = []
for row in segment_summary:
    segment_values = [row["early_flow_mean"], row["mid_flow_mean"], row["late_flow_mean"]]
    late_minus_early = row["late_flow_mean"] - row["early_flow_mean"]
    feature_table.append(
        {
            **row,
            "overall_mean": mean(segment_values),
            "late_minus_early": late_minus_early,
            "early_to_late_slope": late_minus_early / 2,
            "segment_variability": stdev(segment_values),
        }
    )

focus_map = {
    "level": ["overall_mean"],
    "change": ["late_minus_early", "early_to_late_slope"],
    "stability": ["segment_variability"],
}
focus_columns = focus_map[feature_focus]

print("1) segment means before feature design")
print("  event_id  early_flow_mean  mid_flow_mean  late_flow_mean")
for index, row in enumerate(segment_summary):
    print(
        f"{index}        {row['event_id']}              {row['early_flow_mean']:.1f}"
        f"            {row['mid_flow_mean']:.1f}             {row['late_flow_mean']:.1f}"
    )
print()
print("2) designed features for comparison")
print(
    "  event_id  overall_mean  late_minus_early  early_to_late_slope"
    "  segment_variability"
)
for index, row in enumerate(feature_table):
    print(
        f"{index}        {row['event_id']}           {row['overall_mean']:.1f}"
        f"               {row['late_minus_early']:.1f}"
        f"                  {row['early_to_late_slope']:.1f}"
        f"                  {row['segment_variability']:.1f}"
    )
print()
print(f"3) selected features when feature_focus = {feature_focus}")
if focus_columns == ["overall_mean"]:
    print("  event_id  overall_mean")
    for index, row in enumerate(feature_table):
        print(f"{index}        {row['event_id']}           {row['overall_mean']:.1f}")
elif focus_columns == ["late_minus_early", "early_to_late_slope"]:
    print("  event_id  late_minus_early  early_to_late_slope")
    for index, row in enumerate(feature_table):
        print(
            f"{index}        {row['event_id']}               {row['late_minus_early']:.1f}"
            f"                  {row['early_to_late_slope']:.1f}"
        )
else:
    print("  event_id  segment_variability")
    for index, row in enumerate(feature_table):
        print(f"{index}        {row['event_id']}                  {row['segment_variability']:.1f}")
print()
print("4) feature_focus comparison")
for focus_name, columns in focus_map.items():
    print(f"- {focus_name}: {columns}")
```

예상 출력:

```text
1) segment means before feature design
  event_id  early_flow_mean  mid_flow_mean  late_flow_mean
0        A              1.8            2.2             2.6
1        B              2.1            2.2             2.3

2) designed features for comparison
  event_id  overall_mean  late_minus_early  early_to_late_slope  segment_variability
0        A           2.2               0.8                  0.4                  0.4
1        B           2.2               0.2                  0.1                  0.1

3) selected features when feature_focus = change
  event_id  late_minus_early  early_to_late_slope
0        A               0.8                  0.4
1        B               0.2                  0.1

4) feature_focus comparison
- level: ['overall_mean']
- change: ['late_minus_early', 'early_to_late_slope']
- stability: ['segment_variability']
```

출력의 1단계는 아직 구간 평균만 있는 요약 표입니다. 2단계에 가서야 `overall_mean`, `late_minus_early`, `early_to_late_slope`, `segment_variability`가 새로 붙습니다. `overall_mean`은 전체 수준을, `late_minus_early`는 초반 대비 후반 차이를, `early_to_late_slope`는 그 차이를 구간 거리로 나눈 단순 기울기 표현을, `segment_variability`는 구간별 흔들림 정도를 보여 줍니다. 여기서 조작할 값은 `feature_focus`입니다. `"change"`로 두면 변화 특징을 우선 남기고, `"level"`로 바꾸면 전체 수준 특징을, `"stability"`로 바꾸면 변동성 특징을 우선 남깁니다. 4단계는 같은 특징 표라도 질문 초점이 달라지면 실제로 남기는 열 묶음이 달라진다는 점을 보여 줍니다. 즉 특징은 원래 적혀 있던 값을 다시 보여 주는 것이 아니라, 같은 요약 표에서 비교하고 싶은 구조를 계산해 붙이고 현재 질문에 맞게 고른 결과입니다.

같은 차이는 실제 모델 입력에서도 드러납니다. 아래 예제는 전체 평균만 남긴 모델과 변화·변동성 특징까지 함께 남긴 모델을 비교합니다. 두 모델 모두 같은 결정트리(classifier)를 쓰지만, 어떤 특징을 입력으로 주느냐에 따라 테스트 예측이 달라집니다.

문제 상황: 평균은 비슷하지만 구간 변화가 다른 동작을 평균 특징만으로 볼 때와 구조 특징까지 함께 볼 때의 예측 차이를 확인합니다.

입력(input): `early`, `mid`, `late` 구간 평균과 `review_needed` 라벨이 있는 작은 동작 표.

기대 출력(output): `mean_only` 특징 묶음과 `structure_features` 특징 묶음의 정확도와 테스트 예측 비교.

확인할 개념: 특징 선택은 모델에 어떤 구조를 보이게 할지 정하는 일이며, 평균만 남기면 변화나 변동성 구조를 놓칠 수 있습니다.

```python
# 평균만 남긴 모델과 변화·변동성 특징까지 남긴 모델의 예측 차이를 비교합니다.
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

events = pd.DataFrame(
    [
        {"event_id": "A", "early": 1.8, "mid": 2.2, "late": 2.6, "review_needed": 1},
        {"event_id": "B", "early": 2.1, "mid": 2.2, "late": 2.3, "review_needed": 0},
        {"event_id": "C", "early": 2.5, "mid": 2.2, "late": 1.9, "review_needed": 1},
        {"event_id": "D", "early": 2.0, "mid": 2.2, "late": 2.4, "review_needed": 0},
        {"event_id": "E", "early": 1.7, "mid": 2.2, "late": 2.7, "review_needed": 1},
        {"event_id": "F", "early": 2.2, "mid": 2.2, "late": 2.2, "review_needed": 0},
        {"event_id": "G", "early": 2.6, "mid": 2.2, "late": 1.8, "review_needed": 1},
        {"event_id": "H", "early": 2.0, "mid": 2.1, "late": 2.3, "review_needed": 0},
    ]
)

segment_values = events[["early", "mid", "late"]]
events["overall_mean"] = segment_values.mean(axis=1)
events["late_minus_early"] = events["late"] - events["early"]
events["segment_variability"] = segment_values.std(axis=1)

train = events[events["event_id"].isin(["A", "B", "C", "D", "E", "F"])]
test = events[events["event_id"].isin(["G", "H"])]
feature_sets = {
    "mean_only": ["overall_mean"],
    "structure_features": ["overall_mean", "late_minus_early", "segment_variability"],
}

for name, columns in feature_sets.items():
    model = DecisionTreeClassifier(random_state=0, max_depth=2)
    model.fit(train[columns], train["review_needed"])
    predicted = model.predict(test[columns])
    comparison = [
        (event_id, int(prediction), int(actual))
        for event_id, prediction, actual in zip(test["event_id"], predicted, test["review_needed"])
    ]
    print(name, "accuracy:", accuracy_score(test["review_needed"], predicted))
    print(name, "predictions:", comparison)
```

예상 출력:

```text
mean_only accuracy: 0.5
mean_only predictions: [('G', 0, 1), ('H', 0, 0)]
structure_features accuracy: 1.0
structure_features predictions: [('G', 1, 1), ('H', 0, 0)]
```

`G`는 전체 평균만 보면 안정적인 동작과 구분하기 어렵지만, `late_minus_early`와 `segment_variability`를 함께 보면 후반으로 갈수록 내려가는 구조와 구간 흔들림이 드러납니다. 그래서 같은 모델이라도 평균만 볼 때는 `G`를 놓치고, 구조 특징을 함께 볼 때는 맞힙니다. 이 출력은 특징이 단순한 열 추가가 아니라, 모델이 볼 수 있는 구조를 정하는 선택이라는 점을 보여 줍니다.

이 특징들은 작은 층위로 나누어 읽으면 각 값이 맡는 역할이 더 분명해집니다.

| 특징 유형 | 대표 예 | 주로 보여 주는 것 |
| --- | --- | --- |
| 수준 특징 | 평균, 최댓값 | 전체 크기 |
| 변화 특징 | 구간 차이, 기울기 | 방향과 속도 |
| 안정성 특징 | 표준편차, 변동성 | 흔들림의 정도 |

이 표는 앞에서 말한 두 갈래를 다시 확인하게 합니다. 평균, 차이, 기울기, 변동성으로 바꾸는 단계가 변수변환이고, 그 가운데 어떤 값을 현재 질문에 남길지 고르는 단계가 특징 선택입니다. 숫자 특징은 구조를 요약하는 첫 단계이고, 토큰화된 표현은 그 구조를 좀 더 사람이 읽기 쉬운 [중간 표현(intermediate representation)](../../../reference/concept-glossary-parts/09-jieut.md#glossary-intermediate-representation)으로 바꾸는 다음 단계입니다.

특징을 설계할 때는 다음 질문을 계속 확인해야 합니다.

- 이 값은 동작의 어떤 면을 보여 주는가
- 평균만으로 놓치는 구조를 보완하는가
- 사람이 읽었을 때도 설명할 수 있는가
- 샘플 단위와 잘 맞는가

이 질문을 조금 더 실무적으로 줄이면, 어떤 구조에 어떤 특징을 먼저 붙일지 다음처럼 고를 수 있습니다.

| 먼저 보고 싶은 구조 | 우선 떠올릴 특징 |
| --- | --- |
| 전체 수준이 비슷한가 | 평균, 최댓값 |
| 초반과 후반이 얼마나 달라졌는가 | 구간 차이, 기울기 |
| 얼마나 흔들렸는가 | 표준편차, 변동성 |
| 특정 시점에서 급격히 변했는가 | 최대값 시점, 변화율 |

이 표의 핵심은 `특징 목록을 더 많이 외우자`가 아닙니다. 먼저 보고 싶은 구조를 정한 뒤에 그 구조를 가장 직접 드러내는 특징을 붙여야 한다는 점입니다.

여기서 한 번 더 막히는 지점은 `구조를 보고 특징을 고른다`는 말이 여전히 추상적으로 들린다는 점입니다. 그래서 실제 질문을 특징 설계로 옮기는 과정을 한 번 더 짧게 적어 보면 다음과 같습니다.

| 현장에서 먼저 나오는 질문 | 우선 만들 특징 | 그 특징이 먼저 필요한 이유 |
| --- | --- | --- |
| 이번 동작은 평소보다 전체 수준이 낮았는가 | 평균, 중앙값 | 가장 먼저 전체 규모 차이를 확인할 수 있기 때문 |
| 초반은 괜찮았는데 후반에 무너졌는가 | `late_minus_early`, 구간별 기울기 | 어느 구간에서 구조가 달라졌는지 바로 드러나기 때문 |
| 결과는 비슷해 보여도 과정이 더 흔들렸는가 | 표준편차, 구간별 변동성 | 평균이 가린 불안정성을 따로 볼 수 있기 때문 |
| 최고점이 너무 늦게 오거나 빨리 꺼졌는가 | 최대값 시점, 하강 시작 시점 | 타이밍 차이가 운영 의미를 크게 바꿀 수 있기 때문 |

즉 특징은 `열 후보 목록`에서 고르는 것이 아니라, `지금 무엇을 묻고 있는가`를 숫자 표현으로 옮기는 일입니다. 질문이 `전체 수준`에 있으면 수준 특징이 먼저 나오고, 질문이 `형태 변화`에 있으면 구간 차이와 기울기 같은 변화 특징이 먼저 나와야 합니다. 이 연결이 잡혀야 뒤의 기준선 비교에서도 `왜 하필 이 특징을 남겼는가`를 다시 설명할 수 있습니다.

이 절은 특징 목록 소개가 아니라, `구조를 수치 표현으로 옮기는 일(numeric representation of structure)`을 어떤 질문으로 할 것인가의 문제로 다시 볼 수 있습니다.

## 작은 도식으로 보기

이 절의 흐름은 `비교할 구조`를 먼저 정하고, 그 구조를 평균·차이·기울기·변동성 같은 표현으로 바꾼 뒤, 실제로 남길 특징을 고르는 순서입니다. 즉 특징은 열을 늘리는 일이 아니라 구조를 수치 표현으로 다시 고르는 과정입니다.

--8<-- "assets/part-03/chapter-06/p3-6-1-mermaid-01-ko.mmd"


따라서 특징은 `열을 더 많이 추가하는 일`이 아니라, 비교하고 싶은 구조를 수준, 변화, 안정성 같은 수치 표현으로 다시 옮기는 일입니다.

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `feature`. feature를 input variable used to make predictions라고 설명하므로, 어떤 구조를 보여 줄지를 먼저 정한 뒤 그 구조를 입력 변수로 옮겨야 한다는 근거가 됩니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`의 `feature engineering`. feature engineering을 model training에 helpful한 transformation을 결정하는 과정으로 설명하므로, 특징 설계는 원시 값을 그대로 두는 일이 아니라 구조를 비교 가능한 숫자 표현으로 바꾸는 일이라는 점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 기준 시점은 다른 시점과 비교하기 위한 reference라고 설명하므로, 수준/변화/안정성 특징도 결국 기준선 비교에서 읽히기 쉬운 구조를 남기는 방향으로 선택해야 한다는 일반 근거가 됩니다. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `Measures of Location`. 평균, 중앙값, 최빈값을 대표적인 위치 척도로 설명하고, 치우친 분포나 꼬리가 두꺼운 분포에서는 평균과 중앙값이 서로 다른 정보를 줄 수 있음을 보이므로, 전체 수준을 하나의 숫자로 남길 때도 어떤 구조를 보려는지 먼저 정해야 한다는 설명을 보강합니다. [https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm](https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `Measures of Scale`. 변동성(variability)이나 퍼짐(spread)을 설명하는 여러 수치 척도가 있고, 어떤 척도를 고를지는 중심 주변의 퍼짐과 꼬리의 퍼짐 중 무엇을 강조할지에 따라 달라진다고 정리하므로, 안정성 특징을 평균과 별도 구조로 남겨야 한다는 이 절의 설명을 뒷받침합니다. [https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20

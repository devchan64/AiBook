# P3-4.2 샘플 단위가 흔들리면 무엇이 함께 흔들리는가

> Section ID: `P3-4.2`
> Version: `v2026.07.25`

[샘플(sample)](../../../reference/concept-glossary-parts/07-siot.md#glossary-sample) 단위는 뒤에 나오는 거의 모든 개념의 기준점입니다. 따라서 측정값과 샘플을 혼동하면 단지 용어 하나를 잘못 쓰는 데서 끝나지 않습니다. [특징(feature)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature)의 뜻도 흔들리고, [지도학습 라벨(supervised learning label)](../../../reference/concept-glossary-parts/09-jieut.md#supervised-learning-label)의 뜻도 흔들리고, [평가(evaluation)](../../../reference/concept-glossary-parts/13-pieup.md#glossary-evaluation)가 무엇을 평가하는지도 같이 흔들립니다. 앞 절에서 샘플 한 건을 무엇으로 볼지 정했다면, 이제는 그 결정이 무엇을 함께 고정하고 무엇을 함께 흔드는지 봐야 합니다.

여기서는 샘플 단위 자체를 새로 정의하지 않습니다. 대신 앞 절에서 고정한 샘플 단위가 왜 뒤의 특징, 라벨, 분할, 평가까지 함께 흔드는지를 따라가는 데 집중합니다.

가장 흔한 혼동부터 살핍니다. 동작 중 1초 간격으로 측정된 시계열 표가 있다고 하겠습니다. 이 표의 한 행을 그대로 `샘플 1건`으로 받아들이는 경우가 많습니다. 이렇게 되면 압력, 유량, 온도 같은 현재 값들을 곧바로 특징(feature)처럼 붙이기 시작합니다. 하지만 우리가 실제로 알고 싶은 것이 `이번 동작이 평소와 다른 구조였는가`라면, 시점별 한 줄은 그 질문에 답하는 샘플이 아닙니다.

왜 문제가 생기는지 항목별로 정리합니다.

## 1. 특징의 뜻이 흔들린다

동작 1회를 샘플로 본다면 총 동작 시간, 초반 평균, 후반 하강률, 변동성 같은 값이 특징(feature)이 될 수 있습니다. 반면 시점별 한 줄을 샘플로 본다면 같은 열들은 아직 계산할 수 없거나, 계산하더라도 그 줄 하나만으로는 의미가 불완전합니다.

## 2. 라벨의 뜻이 흔들린다

어떤 운영 라벨이 `검토 필요`라면, 보통 그것은 개별 측정 한 점에 붙는 라벨이 아니라 동작 1회나 최근 구간에 붙는 라벨입니다. 그런데 시점별 한 줄을 샘플로 읽어 버리면, 그 라벨을 어느 줄에 붙여야 할지부터 애매해집니다.

## 3. 평가 단위가 흔들린다

동작 1회가 샘플이라면 학습과 평가도 동작 1회 단위로 해야 합니다. 그런데 시점별 한 줄을 샘플처럼 다루면, 같은 동작에서 나온 서로 가까운 행들이 훈련과 평가에 섞여 들어갈 수 있습니다.

## 4. 운영 해석이 흔들린다

운영자는 대개 `한 시점의 숫자`보다 `동작 전체가 어땠는가`를 알고 싶어 합니다. 그런데 측정값과 샘플을 혼동하면 운영 질문과 데이터 구조가 어긋납니다.

이 네 문제를 한 번에 보면 왜 샘플 단위가 단순한 용어 문제가 아닌지 더 분명해집니다.

짧은 운영 장면으로 다시 보면 더 분명합니다. 생산 라인에서 자동 세척 동작이 하루에 수백 번 반복된다고 하겠습니다. 운영자가 실제로 묻는 질문은 보통 `12시 03분 01초의 유량이 정상인가`가 아니라 `방금 끝난 세척 1회가 평소보다 불안정했는가`, `최근 30분 동안 같은 이상이 반복되는가`에 가깝습니다. 그런데 시점별 한 줄을 샘플로 잡아 버리면, 운영 질문은 동작 1회 단위인데 [데이터셋(dataset)](../../../reference/concept-glossary-parts/03-digeut.md#glossary-dataset)은 초 단위 기록을 가리키게 됩니다. 이 순간부터 특징은 너무 잘게 쪼개지고, 라벨은 반복 복사되고, 평가는 실제 운영 판단 단위와 어긋나기 시작합니다.

| 흔들리는 것 | 왜 같이 흔들리는가 |
| --- | --- |
| 특징(feature) | 무엇을 요약해야 하는지가 샘플 단위에 달려 있기 때문 |
| 라벨(label) | 어떤 결과가 한 건에 붙는지가 샘플 단위에 달려 있기 때문 |
| 분할과 평가 | 무엇을 훈련과 평가에 나눌지가 샘플 단위에 달려 있기 때문 |
| 운영 문장 | 사람이 무엇을 한 사례로 읽을지가 샘플 단위에 달려 있기 때문 |

여기서는 아래처럼 `잘못 붙인 질문`과 `다시 붙여야 할 질문`을 나눠 보면 샘플 단위의 어긋남이 더 분명해집니다.

| 잘못 붙인 질문 | 왜 어긋나는가 | 다시 붙여야 할 질문 |
| --- | --- | --- |
| 이 한 줄이 정상인가 | 한 줄은 시점 기록일 뿐이라 동작 전체를 대표하지 않을 수 있음 | 이 동작 1회 전체가 평소와 다른 구조인가 |
| 이 줄에 라벨을 붙이면 되나 | 라벨이 보통 동작 1회나 최근 구간에 붙기 때문 | 라벨이 붙는 대상은 한 시점인가, 한 동작인가 |
| 이 줄을 훈련 데이터 한 건으로 쓰면 되나 | 같은 동작의 가까운 줄들이 훈련/평가에 섞일 수 있음 | 분할 대상은 시점 행인가, 동작 단위 샘플인가 |

즉 샘플 단위는 Part 3의 한 절에서만 필요한 결정이 아니라, 특징 설계(feature engineering), [기준선(baseline)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-baseline) 비교, [검토 큐(review queue)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-review-queue), 예측용 입력 구조 해석까지 모두 기대는 바닥 구조입니다.

## 작은 도식으로 보기

앞 문단의 핵심은 하나입니다. 샘플 단위가 흔들리면 특징, 라벨, 분할, 평가, 운영 해석이 각자 따로 흔들리는 것이 아니라 같은 기준을 잃으면서 함께 어긋납니다.

--8<-- "assets/part-03/chapter-04/p3-4-2-mermaid-01-ko.mmd"

아래 예시는 같은 [원천데이터(source data)](../../../reference/concept-glossary-parts/08-ieung.md#glossary-source-data)를 `시점별 표`로 볼 때와 `동작 단위 표`로 볼 때 특징, 라벨, 분할 해석이 어떻게 달라지는지 보여 줍니다.

문제 상황: 같은 로그를 `시점별 표`로 읽을 때와 `동작 단위 표`로 읽을 때 특징, 라벨, train/test 분할이 어떻게 함께 흔들리는지 확인합니다.

입력(input): `event_id`별 시점 유량과 `review_needed`가 함께 들어 있는 원시 로그 표

기대 출력(output): `row` 단위와 `event` 단위가 서로 다른 샘플 수, 라벨 반복, 분할 안정성을 만든다는 비교 출력

확인할 개념: 샘플 단위가 바뀌면 feature, label, split 해석도 같은 단위 위에서 함께 다시 맞춰야 한다

```python
# 샘플 단위가 흔들릴 때 특징, 라벨, 기준선이 함께 달라지는지 확인하는 예제입니다.
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.5, "review_needed": 1},
        {"event_id": "A", "second": 1, "flow": 1.8, "review_needed": 1},
        {"event_id": "A", "second": 2, "flow": 1.1, "review_needed": 1},
        {"event_id": "B", "second": 0, "flow": 0.4, "review_needed": 0},
        {"event_id": "B", "second": 1, "flow": 1.1, "review_needed": 0},
        {"event_id": "B", "second": 2, "flow": 1.0, "review_needed": 0},
        {"event_id": "C", "second": 0, "flow": 0.6, "review_needed": 1},
        {"event_id": "C", "second": 1, "flow": 1.9, "review_needed": 1},
        {"event_id": "C", "second": 2, "flow": 1.3, "review_needed": 1},
    ]
)

per_row = raw[["event_id", "second", "flow", "review_needed"]]
per_event = (
    raw.groupby("event_id", as_index=False)
    .agg(
        flow_mean=("flow", "mean"),
        flow_max=("flow", "max"),
        late_drop=("flow", lambda s: s.iloc[-2] - s.iloc[-1]),
        review_needed=("review_needed", "max"),
    )
)

row_split = raw.assign(split=lambda df: df["second"].map({0: "train", 1: "train", 2: "test"}))
event_split = per_event.assign(split=lambda df: df["event_id"].map({"A": "train", "B": "train", "C": "test"}))

unit_summary = pd.DataFrame(
    [
        {
            "unit": "row",
            "sample_count": len(per_row),
            "feature_example": "flow at one second",
            "label_rows": per_row["review_needed"].sum(),
            "train_events": ",".join(sorted(row_split.loc[row_split["split"] == "train", "event_id"].unique())),
            "test_events": ",".join(sorted(row_split.loc[row_split["split"] == "test", "event_id"].unique())),
        },
        {
            "unit": "event",
            "sample_count": len(per_event),
            "feature_example": "flow_mean / flow_max / late_drop",
            "label_rows": per_event["review_needed"].sum(),
            "train_events": ",".join(sorted(event_split.loc[event_split["split"] == "train", "event_id"].unique())),
            "test_events": ",".join(sorted(event_split.loc[event_split["split"] == "test", "event_id"].unique())),
        },
    ]
)

print("1) sample counts change with the chosen unit")
print("row-level samples:", len(per_row))
print("event-level samples:", len(per_event))
print()
print("2) row-level labels are repeated because the label belongs to the whole event")
print(per_row.groupby("event_id", as_index=False)["review_needed"].sum())
print()
print("3) event-level features and labels line up on the same unit")
print(per_event)
print()
print("4) split stability differs by unit")
print(unit_summary)
```

예상 출력:

```text
1) sample counts change with the chosen unit
row-level samples: 9
event-level samples: 3

2) row-level labels are repeated because the label belongs to the whole event
  event_id  review_needed
0        A              3
1        B              0
2        C              3

3) event-level features and labels line up on the same unit
  event_id  flow_mean  flow_max  late_drop  review_needed
0        A   1.133333       1.8        0.7              1
1        B   0.833333       1.1        0.1              0
2        C   1.266667       1.9        0.6              1

4) split stability differs by unit
    unit  sample_count                    feature_example  label_rows train_events test_events
0    row             9                 flow at one second           6        A,B,C       A,B,C
1  event             3  flow_mean / flow_max / late_drop           2          A,B           C
```

이 출력은 세 가지를 한 번에 보여 줍니다. 첫째, `review_needed`는 동작 1회에 붙는 라벨인데 시점별 표에서는 A와 C에 대해 3번씩 반복됩니다. 둘째, `late_drop` 같은 특징은 동작 1회로 묶였을 때만 계산됩니다. 셋째, `unit summary`를 보면 시점별 분할에서는 같은 `event_id`가 훈련과 평가 양쪽에 동시에 나타날 수 있지만, 동작 단위 분할에서는 `C` 전체를 테스트로 떼어 낼 수 있습니다. 이 차이가 바로 특징(feature), 라벨(label), 분할(split), 평가(evaluation) 단위가 함께 흔들리는 이유입니다.

이 예제는 출력값 자체보다 다음 세 질문을 먼저 확인하면 샘플 단위가 왜 먼저 고정되어야 하는지 더 분명해집니다.

1. `review_needed`는 시점별 숫자에 붙는가, 동작 1회에 붙는가
2. `flow_mean`, `flow_max`는 한 줄에서 바로 읽은 값인가, 여러 줄을 묶어 만든 값인가
3. 훈련/평가 분할을 한다면 `per_row`를 나눌 것인가, `per_event`를 나눌 것인가

세 질문에 답해 보면 왜 `같은 원천데이터라도 샘플 단위를 먼저 정해야 한다`는 말이 반복되는지 더 분명해집니다.

같은 문제를 실제 모델 평가로도 축소해 볼 수 있습니다. 아래 예제는 `DecisionTreeClassifier`를 잘 쓰는 법을 가르치려는 코드가 아닙니다. 같은 동작의 행이 훈련과 평가에 동시에 들어가면 평가 점수가 좋아 보일 수 있고, 동작 단위로 떼어 내면 그 착시가 줄어든다는 점을 확인하는 코드입니다.

문제 상황: 같은 원시 로그를 행 단위로 나눈 평가와 동작 단위로 나눈 평가가 서로 다른 점수를 만들 수 있음을 확인합니다.

입력(input): `event_id`, `second`, `flow`, `review_needed`가 있는 작은 동작 로그.

기대 출력(output): 행 단위 분할에서 훈련과 평가에 동시에 들어간 `event_id`, 행 단위 평가 점수, 동작 단위 평가 점수.

확인할 개념: 같은 동작에서 나온 가까운 행이 훈련과 평가에 섞이면 모델이 새 동작을 맞힌 것이 아니라 이미 본 동작의 근처 값을 다시 맞힌 것처럼 보일 수 있습니다.

```python
# 같은 원시 로그라도 분할 단위가 평가 점수를 어떻게 바꾸는지 확인합니다.
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

raw_rows = []
labels = {"A": 1, "B": 0, "C": 1, "D": 0, "E": 1, "F": 0, "G": 0, "H": 1}
base_flow = {"A": 10, "B": 30, "C": 50, "D": 70, "E": 90, "F": 110, "G": 130, "H": 150}

for event_id, label in labels.items():
    for second, offset in enumerate([0.0, 0.2, -0.1]):
        raw_rows.append(
            {
                "event_id": event_id,
                "second": second,
                "flow": base_flow[event_id] + offset,
                "review_needed": label,
            }
        )

raw = pd.DataFrame(raw_rows)

# 행 단위 분할: 모든 event_id의 일부 행이 train/test 양쪽에 동시에 들어갑니다.
row_train = raw[raw["second"].isin([0, 1])]
row_test = raw[raw["second"].eq(2)]

# 동작 단위 분할: test event_id는 훈련에서 완전히 제외합니다.
event_train = raw[raw["event_id"].isin(["A", "B", "C", "D"])]
event_test = raw[raw["event_id"].isin(["E", "F", "G", "H"])]


def evaluate(train, test):
    model = DecisionTreeClassifier(random_state=0)
    model.fit(train[["flow"]], train["review_needed"])
    predictions = model.predict(test[["flow"]])
    return accuracy_score(test["review_needed"], predictions), [
        (event_id, int(prediction), int(actual))
        for event_id, prediction, actual in zip(test["event_id"], predictions, test["review_needed"])
    ]


row_accuracy, _ = evaluate(row_train, row_test)
event_accuracy, event_predictions = evaluate(event_train, event_test)
leaked_events = sorted(set(row_train["event_id"]) & set(row_test["event_id"]))

print("leaked events in row split:", leaked_events)
print("row split accuracy:", row_accuracy)
print("event split accuracy:", event_accuracy)
print("event split predictions:", event_predictions)
```

예상 출력:

```text
leaked events in row split: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
row split accuracy: 1.0
event split accuracy: 0.5
event split predictions: [('E', 0, 1), ('E', 0, 1), ('E', 0, 1), ('F', 0, 0), ('F', 0, 0), ('F', 0, 0), ('G', 0, 0), ('G', 0, 0), ('G', 0, 0), ('H', 0, 1), ('H', 0, 1), ('H', 0, 1)]
```

행 단위 분할에서는 모든 `event_id`가 훈련과 평가에 동시에 들어갑니다. 그래서 점수가 `1.0`으로 좋아 보입니다. 하지만 이것은 새 동작을 잘 맞혔다는 뜻보다, 같은 동작에서 나온 가까운 행을 다시 맞힌 것에 가깝습니다. 이런 착시는 [데이터 누수(data leakage)](../../../reference/concept-glossary-parts/03-digeut.md#glossary-data-leakage) 관점에서도 점검해야 합니다. 동작 단위 분할에서는 `E`, `F`, `G`, `H` 전체가 훈련에서 빠지므로 점수가 `0.5`로 내려갑니다. 이 차이는 샘플 단위가 평가 단위까지 함께 고정해야 한다는 사실을 모델 출력으로 보여 줍니다.

이 코드에서 바꿔 볼 값은 두 가지입니다. `event_train`과 `event_test`에 들어가는 `event_id` 묶음을 바꾸면 동작 단위 평가가 달라집니다. `features`를 늘려 `second` 같은 열을 함께 넣으면 모델이 무엇을 근거로 예측하는지도 달라질 수 있습니다. 중요한 것은 점수 자체가 아니라, `무엇을 한 샘플로 나누었는가`가 평가 결과의 뜻을 바꾼다는 점입니다.

여기에 한 줄만 더 붙이면 흔들림의 방향을 바로 읽을 수 있습니다.

- `review_needed`가 동작 1회 라벨이라면 `per_row` 분할은 라벨 단위를 잘못 자를 위험이 큽니다.
- `flow_mean`, `flow_max`가 여러 줄을 묶어 만든 특징이라면 시점별 한 줄을 샘플로 읽는 순간 특징 뜻도 바뀝니다.
- 따라서 샘플 단위가 흔들리면 특징, 라벨, 분할이 각자 따로 흔들리는 것이 아니라 함께 어긋납니다.

같은 내용을 더 짧게 정리하면 아래처럼 읽을 수 있습니다.

| 시점별 한 줄을 샘플로 잡으면 | 동작 1회를 샘플로 잡으면 |
| --- | --- |
| 라벨이 여러 줄에 반복 복사된다 | 라벨이 한 동작에 한 번 붙는다 |
| 동작 전체 특징을 바로 만들기 어렵다 | 요약 특징을 같은 방식으로 붙일 수 있다 |
| 같은 동작이 훈련/평가에 함께 섞일 수 있다 | 동작 단위로 분할할 수 있다 |
| 운영 질문과 데이터 단위가 어긋난다 | 운영 질문과 데이터 단위가 맞는다 |

따라서 샘플 단위가 흔들릴 때의 문제는 단순한 표기 혼동이 아니라, feature, label, split, evaluation이 서로 다른 단위를 가리키기 시작하는 정합성 붕괴로 봐야 합니다.

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. example는 features와 label이 같은 단위 위에 정렬되어 있어야 하므로, 샘플 단위가 흔들리면 feature와 label의 뜻도 함께 흔들린다는 근거가 됩니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`의 `label leakage`. feature가 label의 proxy가 되는 설계 결함을 설명하므로, 잘못된 단위에서 row-level feature와 event-level label을 섞으면 구조적 오류가 생길 수 있다는 점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- scikit-learn developers, `Cross-validation: evaluating estimator performance`. grouped data에서 같은 그룹의 의존 샘플이 훈련 fold와 검증 fold에 함께 나타나지 않게 해야 한다고 설명하므로, 시점별 행을 샘플처럼 나누면 같은 동작의 가까운 행이 훈련/평가에 섞일 수 있다는 이 절의 분할·평가 경고를 직접 보강합니다. [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. provenance framework가 reproducibility와 derivation을 지원해야 한다고 정리하므로, 어떤 단위에서 feature와 label이 만들어졌는지 재현 가능하게 남겨야 split/evaluation도 같은 기준을 유지할 수 있다는 상위 프레임을 보강합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20

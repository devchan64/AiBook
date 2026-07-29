# P3-3.1 원천데이터를 왜 곧바로 학습 문제로 읽으면 안 되는가

> Section ID: `P3-3.1`
> Version: `v2026.07.25`

원천데이터를 처음 받으면 많은 사람이 거의 반사적으로 `이걸로 무엇을 예측할까`부터 떠올립니다. 표가 있고 값이 많고 시간이 흐르며 측정된 기록도 보이니, 곧바로 어떤 학습 문제로 바꿀 수 있을 것처럼 느껴지기 때문입니다. 하지만 이 반응은 대개 너무 빠릅니다. 눈앞의 표는 아직 `학습용 데이터셋`이 아니라 [기록된 원천데이터(source data)](../../../reference/concept-glossary-parts/08-ieung.md#glossary-source-data)이거나, 많아야 [데이터셋 후보(dataset candidate)](../../../reference/concept-glossary-parts/03-digeut.md#glossary-dataset-candidate)일 가능성이 더 크기 때문입니다.

여기서는 `학습 문제의 틀`보다 [문제 표현 구조(problem-representation structure)](../../../reference/concept-glossary-parts/05-mieum.md#glossary-problem-representation-structure)가 먼저라는 점을 고정합니다. 아직 예측 문제, 분류 문제, 이상 징후 판별 문제처럼 학습 문제의 틀을 고르는 단계가 아니라는 경고를 먼저 분명히 해야 합니다.

이 장으로 들어오면 Chapter 2에서 만든 `데이터셋 후보` 관점이 한 번 더 좁혀집니다.

| 이전 Chapter에서 남긴 것 | 이번 Chapter에서 추가로 정하는 것 | 다음 Chapter로 넘길 구조 |
| --- | --- | --- |
| 저장 구조와 데이터셋 후보의 차이, 새 표를 읽는 첫 점검 | 원천데이터를 아직 학습 문제로 올리지 말아야 하는 이유 | 샘플 단위와 표 구조를 실제로 정하는 판단 |

자동으로 실행되는 동작 1회마다 제어 파라미터 시계열과 센서 시계열이 남는 상황을 보겠습니다. 이런 표를 보면 다음 같은 생각이 먼저 나옵니다.

- 센서 값이 있으니 이상 징후 판별 문제로 바꿀 수 있겠다.
- 동작 결과가 조금 다르니 분류 문제로 바꾸면 되겠다.
- 시계열이 길면 시계열 예측 문제로 바로 넘길 수 있을 것 같다.

이 생각들 자체가 틀린 것은 아닙니다. 문제는 `무엇을 한 건으로 볼지`, `무엇을 맞히려는지`, [지도학습 라벨(supervised learning label)](../../../reference/concept-glossary-parts/09-jieut.md#supervised-learning-label)이 실제로 있는지도 정하지 않은 상태에서 학습 문제의 틀이 먼저 등장한다는 점입니다. 이 상태에서는 아직 데이터 문제를 정의한 것이 아니라, 데이터보다 학습 문제 틀을 먼저 떠올린 것입니다.

이런 일이 자주 생기는 이유는 분명합니다. 첫째, 표가 보이면 사람은 `이미 정리된 데이터셋`이라고 곧바로 받아들이곤 합니다. 둘째, AI 학습 경험이 학습 문제 유형 중심으로 남아 있으면 문제 표현보다 예측 방식이 먼저 떠오릅니다. 셋째, 원천 시계열이 길고 복잡할수록 `이걸 그대로 학습 문제로 넘길 수 있지 않을까`라는 기대가 먼저 앞섭니다.

하지만 원천데이터를 곧바로 데이터셋처럼 읽으면 중요한 질문이 빠집니다.

| 먼저 떠올리기 쉬운 질문 | 실제로 더 먼저 필요한 질문 |
| --- | --- |
| 어떤 학습 문제로 읽을까 | 무엇을 한 건의 [샘플(sample)](../../../reference/concept-glossary-parts/07-siot.md#glossary-sample)로 볼까 |
| 라벨을 무엇으로 둘까 | 지금 라벨이 정말 안정적으로 있는가 |
| 정확도를 어떻게 올릴까 | 어떤 표로 다시 묶어야 비교가 가능한가 |

이 차이는 단순한 순서 문제가 아닙니다. 원천데이터를 처음 볼 때 필요한 일은 학습 문제 선택이 아니라 `표의 정체를 다시 묻는 일`입니다. 지금 보고 있는 것이 시점별 측정 기록인지, 동작 1회 요약인지, 최근 구간 집계인지에 따라 뒤의 [특징(feature)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature), [기준선(baseline)](../../../reference/concept-glossary-parts/01-giyeok.md#glossary-baseline), [목표 라벨(target)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-target) 설명이 모두 달라집니다.

예를 들어 다음처럼 원천데이터의 일부만 보고도 너무 빨리 학습 문제의 틀이 튀어나올 수 있습니다.

| event_id | second | pressure | flow |
| --- | --- | --- | --- |
| A | 0 | 1.0 | 0.0 |
| A | 1 | 2.0 | 1.4 |
| A | 2 | 2.4 | 1.6 |

이 표만 보면 `분류 문제`, `예측 문제`, `시계열 학습 문제` 같은 말을 쉽게 떠올릴 수 있습니다. 하지만 아직 이 표가 `한 시점 기록`인지, `동작 1회 표`인지조차 정하지 않았습니다. 따라서 여기서 바로 학습 문제 틀을 고르면 문제보다 문제 형식이 먼저 앞서게 됩니다.

## 작은 도식으로 보기

원천데이터를 바로 학습 문제로 올리면 어떤 질문이 비어 있는지, 아래처럼 `원천 기록 -> 빈 질문 확인 -> 샘플/라벨 후보 정리` 순서로 읽으면 더 분명합니다.

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-1-mermaid-01-ko.mmd"
```

문제 상황: 시점별 로그 표를 받았을 때, 이를 곧바로 학습 문제로 읽으면 어떤 핵심 질문이 비어 있는지 확인합니다.

입력(input): `event_id`별 여러 시점 측정값이 섞여 있는 원시 로그 표 [p3_3_1_source_operation_log.csv](../../../assets/part-03/chapter-03/p3_3_1_source_operation_log.csv)와 라벨 후보로 확인할 열 이름 `label_column_to_try`

입력 파일의 한 행은 한 동작(`event_id`) 안의 특정 초(`second`)에서 측정한 센서 기록입니다. `batch_id`, `recipe`, `pressure`, `flow`, `vibration`, `temperature`가 함께 있지만, 아직 이 중 무엇이 샘플 식별자이고 무엇이 라벨인지는 정하지 않은 상태입니다.

기대 출력(output): `지금 바로 분류 문제로 읽기`와 `먼저 비어 있는 질문 채우기`가 다른 결과를 만든다는 점이 드러납니다. `label_column_to_try`를 바꾸면 열 존재 여부와 라벨 후보 사용 가능 여부가 서로 다를 수 있다는 점도 드러납니다.

확인할 개념: 원천데이터를 학습 문제처럼 읽기 전에 `샘플 1건`, `라벨 후보`, `비교 표`가 무엇인지 먼저 정해야 한다. 학습 문제 판정은 고정 문장이 아니라 현재 표의 열과 묶음 기준에서 확인해야 한다.

```python
# 원천 로그를 바로 학습 문제로 읽지 않고 event 단위 요약표로 다시 보는 예제입니다.
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

raw_log_path = "docs/assets/part-03/chapter-03/p3_3_1_source_operation_log.csv"
label_column_to_try = "review_label"

column_unit = {
    "batch_id": "operation_context",
    "recipe": "operation_context",
    "pressure": "time_point_sensor_value",
    "flow": "time_point_sensor_value",
    "vibration": "time_point_sensor_value",
    "temperature": "time_point_sensor_value",
    "review_label": "event_label",
}

raw = pd.read_csv(raw_log_path)

print("1) raw input shape and first rows")
print("shape:", raw.shape)
print(raw.head())
print()

print("2) too-early reading")
print("- maybe this is a classification problem")
print("- label column:", "found" if label_column_to_try in raw.columns else "not found yet")
print("- one training sample:", "not decided yet")
print()

column_exists = label_column_to_try in raw.columns
candidate_unit = column_unit.get(label_column_to_try, "unknown")
same_unit_as_sample = column_exists and candidate_unit == "event_label"
stable_label_meaning_known = same_unit_as_sample
usable_label_candidate = column_exists and same_unit_as_sample and stable_label_meaning_known

print("3) label candidate check")
print("- column to try:", label_column_to_try)
print("- column exists:", column_exists)
print("- candidate unit:", candidate_unit)
print("- same unit as one event:", same_unit_as_sample)
print("- stable label meaning known:", stable_label_meaning_known)
print("- usable label candidate:", usable_label_candidate)
print()

event_summary = (
    raw.groupby("event_id", as_index=False)
    .agg(
        batch_id=("batch_id", "first"),
        recipe=("recipe", "first"),
        row_count=("second", "count"),
        duration_seconds=("second", "max"),
        max_pressure=("pressure", "max"),
        mean_flow=("flow", "mean"),
        max_vibration=("vibration", "max"),
        end_temperature=("temperature", "last"),
    )
)
print("4) questions that must be settled first")
print("- one sample: one event")
print("- candidate comparison table: one row per event")
print("- label candidate:", "usable" if usable_label_candidate else "still not decided")
print()

print("5) event-level table after defining the sample")
print(event_summary.round(2))
```

예상 출력:

```text
1) raw input shape and first rows
shape: (36, 8)
  event_id batch_id    recipe  second  pressure  flow  vibration  temperature
0        A     B-17  standard       0       1.0   0.0       0.02         24.1
1        A     B-17  standard       1       2.0   1.4       0.04         24.4
2        A     B-17  standard       2       2.4   1.6       0.07         24.8
3        A     B-17  standard       3       2.2   1.2       0.08         25.0
4        B     B-17  standard       0       1.1   0.1       0.03         24.0

2) too-early reading
- maybe this is a classification problem
- label column: not found yet
- one training sample: not decided yet

3) label candidate check
- column to try: review_label
- column exists: False
- candidate unit: event_label
- same unit as one event: False
- stable label meaning known: False
- usable label candidate: False

4) questions that must be settled first
- one sample: one event
- candidate comparison table: one row per event
- label candidate: still not decided

5) event-level table after defining the sample
  event_id batch_id     recipe  row_count  duration_seconds  max_pressure  mean_flow  max_vibration  end_temperature
0        A     B-17   standard          4                 3           2.4       1.05           0.08             25.0
1        B     B-17   standard          4                 3           1.9       0.78           0.06             24.7
2        C     B-18       fast          4                 3           2.8       1.05           0.22             26.8
3        D     B-18       fast          4                 3           2.6       1.02           0.16             26.2
4        E     B-19   standard          4                 3           2.1       0.90           0.07             24.8
5        F     B-19   standard          4                 3           2.5       1.12           0.09             25.3
6        G     B-20  high-load          4                 3           3.1       1.35           0.28             27.5
7        H     B-20  high-load          4                 3           2.9       1.30           0.24             27.0
8        I     B-21   standard          4                 3           2.3       0.98           0.08             25.1
```

이 예제의 핵심은 2단계와 3단계의 차이입니다. 2단계에서는 `분류 문제일지도 모른다`는 말만 먼저 나오지만, 실제로는 `label_column_to_try`로 지정한 `review_label` 열도 없고 샘플 1건도 아직 정해지지 않았습니다. 여기서 조작할 값은 `label_column_to_try`입니다. 값을 `"flow"`로 바꾸면 `column exists`는 `True`가 되지만, `candidate unit`은 `time_point_sensor_value`이고 `usable label candidate`는 여전히 `False`입니다. `flow`는 동작 1회에 붙은 안정 라벨이 아니라 시점별 센서값이기 때문입니다. 반대로 4단계에서는 먼저 `한 샘플은 동작 1회`, `비교 표는 동작별 1행`이라는 구조를 정합니다. 그 뒤에야 5단계처럼 `row_count`, `duration_seconds`, `max_pressure`, `mean_flow`, `max_vibration`, `end_temperature`를 가진 동작 단위 비교 표가 생깁니다. 즉 원천데이터를 너무 빨리 학습 문제로 읽으면, 아직 비어 있는 질문을 덮어 둔 채 문제 형식만 먼저 정하게 됩니다.

실제로 학습 문제의 틀이 먼저 떠오를 때 비어 있는 질문을 나란히 적어 보면 문제가 더 분명해집니다.

| 먼저 튀어나오기 쉬운 말 | 아직 비어 있는 질문 |
| --- | --- |
| `이상 징후 판별 문제` | 무엇을 이상이라고 부를 것인가 |
| `분류 문제` | 라벨이 실제로 안정적으로 있는가 |
| `시계열 학습 문제` | 한 샘플은 한 시점 묶음인가, 동작 1회인가 |

이 표의 핵심은 학습 문제의 이름이 틀렸다는 데 있지 않습니다. 문제는 그 틀보다 먼저 답해야 할 질문이 아직 비어 있다는 점입니다. 데이터 모델링은 바로 그 빈칸을 채우는 앞단 설계입니다.

즉 원천데이터를 처음 받았을 때 가장 흔한 실수는 `기록 구조`를 `학습 구조`로 착각하는 것입니다. 시점별 로그가 있다는 사실만으로 아직 예측 문제가 정해진 것은 아닙니다. 그 로그를 어떤 단위로 묶고, 무엇을 남기고, 무엇과 비교할지 정해야 비로소 데이터셋이라는 말을 쓸 수 있습니다. 학습 문제의 틀이 먼저 떠오르면 이 앞단 설계가 건너뛰어지기 쉽고, 뒤에서 샘플 단위와 표 구조를 다시 뜯어고치게 됩니다. 이 절을 `문제 승격(problem escalation)`의 시점을 관리하는 문제로 다시 보면, 핵심은 `모델 이름을 늦게 떠올리자`가 아니라 샘플 단위와 라벨 후보가 정리되기 전까지는 학습 문제로 성급히 승격하지 않는 판단에 있다는 점이 더 분명해집니다.

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. labeled example은 features와 label로 구성된다고 설명하므로, 아직 샘플 1건과 label이 정해지지 않은 원천데이터를 곧바로 학습 문제로 읽으면 안 된다는 근거가 됩니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`의 `label leakage`. feature가 label의 proxy가 되는 설계 결함을 설명하므로, 문제 틀을 먼저 고르면 아직 정리되지 않은 원천 열을 잘못된 학습 구조로 읽을 위험이 있다는 점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. provenance framework가 identifying an object와 representing derivation을 지원해야 한다고 정리하므로, 무엇을 한 대상(example)로 보고 어떤 변환을 거쳐 데이터셋 후보를 만들었는지 먼저 정리해야 한다는 상위 프레임을 보강합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20

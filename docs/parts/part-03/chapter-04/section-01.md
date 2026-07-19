# P3-4.1 비교 가능한 샘플 한 건은 어떻게 정하는가

> Section ID: `P3-4.1`
> Version: `v2026.07.20`

데이터를 읽을 때 가장 먼저 확인해야 할 것은 값의 크기보다 `한 행이 무엇을 뜻하는가`입니다. 이 질문이 먼저 정리되지 않으면, 뒤에서 특징(feature)을 만들 때도, 라벨(label)을 붙일 때도, 평가(evaluation) 결과를 읽을 때도 기준이 흔들립니다. 결국 이 질문은 `비교 가능한 샘플 한 건을 무엇으로 정할 것인가`라는 질문으로 이어집니다.

예를 들어 자동으로 실행되는 동작에서 제어 파라미터 시계열과 센서 시계열이 남는다고 하겠습니다. 어떤 표에서는 한 행이 `1초 시점의 압력과 유량 측정값`일 수 있습니다. 다른 표에서는 한 행이 `동작 1회 전체의 요약값`일 수 있습니다. 또 다른 표에서는 한 행이 `최근 30분 동안 수행된 여러 동작의 집계 결과`일 수 있습니다. 셋 다 같은 원천데이터에서 나왔지만, 한 행이 뜻하는 대상은 완전히 다릅니다.

| 구분 | 한 행이 뜻하는 것 | 주로 답하는 질문 |
| --- | --- | --- |
| 측정값 표 | 동작 중 한 시점의 센서 또는 제어 값 | 지금 이 시점의 값은 얼마인가 |
| 동작 단위 표 | 자동으로 실행된 동작 1회 전체 | 이번 동작의 전체 구조는 어땠는가 |
| 최근 구간 표 | 여러 동작을 묶은 최근 집계 | 최근 변화가 반복되고 있는가 |
| 기준선 표 | 평소 상태를 대표하는 비교 집계 | 평소와 비교하면 지금은 얼마나 다른가 |

이 표를 보면 같은 데이터라도 어떤 질문에 답하려는지에 따라 `행의 의미`가 달라진다는 점이 보입니다. 측정값 표는 현재 상태를 읽는 데 강하지만, 동작 전체의 구조를 바로 보여 주지는 못합니다. 반대로 동작 단위 표는 한 번의 동작을 비교하는 데 유리하지만, 시점별 순간 변화를 그대로 담지는 않습니다. 최근 구간 표와 기준선 표는 더 나아가 `한 건`이 아니라 `여러 건을 묶은 비교 구조`를 뜻합니다. 따라서 눈앞에 행이 보인다고 해서 그 행을 곧 샘플 1건이라고 놓으면 안 됩니다. 모델이 배워야 할 것이 `동작 전체의 패턴`이라면, 시점별 측정값 여러 행을 묶어 `동작 1회`라는 새로운 샘플을 다시 만들어야 하기 때문입니다.

여기서 `비교 가능한 샘플`이라고 부르려면 최소한 세 가지를 함께 만족해야 합니다.

1. 한 건의 경계가 분명해야 한다.
2. 같은 종류의 특징을 모든 건에 같은 방식으로 붙일 수 있어야 한다.
3. 나중에 붙일 라벨이나 비교 기준이 그 단위에 자연스럽게 연결되어야 한다.

이 세 가지를 기준으로 보면, 시점별 측정 행은 보통 1번은 만족하지만 2번과 3번이 약합니다. 반면 동작 1회 요약 표는 세 가지를 모두 만족하기 쉽습니다. 최근 구간 표는 3번의 비교 기준에는 강하지만, 개별 샘플 비교보다는 여러 샘플을 다시 묶은 해석 구조에 더 가깝습니다. 결국 이 절에서 정할 것은 `한 시점`, `동작 1회`, `최근 구간` 가운데 무엇을 비교 가능한 샘플 1건으로 볼 것인가입니다.

눈앞의 표를 받았을 때는 다음 순서로 읽으면 역할 구분이 더 분명해집니다.

1. 지금 표의 한 행이 `한 시점`인지 `동작 1회`인지 `여러 동작의 집계`인지 본다.
2. 그 한 행이 어떤 질문에 답하려고 만들어졌는지 본다.
3. 그 질문이 현재 우리가 풀려는 문제와 맞는지 확인한다.

이 순서를 거치면 `행이 있으니 샘플도 이미 있겠지`라는 자동 가정을 조금 늦출 수 있습니다. 그래야 원시 로그, 요약 표, 최근 구간 표를 같은 표처럼 섞어 읽지 않게 됩니다.

아래 작은 표를 보면 이 차이가 더 분명해집니다.

| event_id | elapsed_seconds | pressure | flow |
| --- | --- | --- | --- |
| A | 0 | 1.0 | 0.0 |
| A | 1 | 2.0 | 1.4 |
| A | 2 | 2.4 | 1.6 |
| B | 0 | 1.1 | 0.0 |
| B | 1 | 1.7 | 1.1 |
| B | 2 | 2.0 | 1.2 |

이 표에서 한 행은 `동작 1회`가 아니라 `동작 중 한 시점`입니다. 따라서 샘플 1건을 동작 1회로 보려면 같은 `event_id`를 가진 여러 행을 묶어야 합니다. 그런데 여기서 한 번 더 보면, 같은 원천데이터라도 `시점`, `동작 1회`, `최근 구간` 가운데 무엇을 한 건으로 읽느냐에 따라 샘플 수 자체가 달라질 뿐 아니라, 어떤 열이 그 단위에서만 의미를 갖는지도 함께 달라집니다.

이제 같은 예제를 앞의 세 기준으로 다시 읽어 보면 왜 `동작 1회`가 비교 가능한 샘플에 더 가깝다고 말하는지 분명해집니다.

| 후보 단위 | 경계가 분명한가 | 같은 특징을 붙이기 쉬운가 | 라벨/비교 기준을 붙이기 자연스러운가 |
| --- | --- | --- | --- |
| 측정 시점 1행 | 예 | 약함 | 약함 |
| 동작 1회 | 예 | 예 | 예 |
| 최근 구간 1묶음 | 예 | 일부만 가능 | 비교 기준에는 강하지만 개별 샘플 라벨에는 약함 |

즉 `동작 1회`를 샘플 1건으로 두면 `pressure_mean`, `pressure_rise`, `flow_mean` 같은 특징을 모든 건에 같은 방식으로 붙일 수 있고, 나중에 `검토 필요`, `정상`, `이상` 같은 결과도 그 단위에 자연스럽게 연결됩니다. 반대로 측정 시점 1행은 순간 관측값을 담는 데는 좋지만, 동작 전체 구조를 비교하는 특징과 라벨을 안정적으로 올리기 어렵습니다. 최근 구간 1묶음은 개별 동작 비교 샘플이라기보다 여러 동작을 다시 묶은 해석 단위에 가깝습니다.

그래서 실제로는 `어느 단위를 먼저 샘플로 잡아야 하는가`를 아래처럼 결정할 수 있습니다.

| 지금 답하려는 질문 | 먼저 잡을 샘플 단위 | 이유 |
| --- | --- | --- |
| 이번 동작이 다른 동작보다 이상했는가 | 동작 1회 | 비교 대상이 `동작 대 동작`이기 때문 |
| 어느 시점에서 압력이 급격히 올랐는가 | 측정 시점 | 질문 자체가 순간 변화 시점을 묻기 때문 |
| 최근 운영 상태가 평소보다 달라졌는가 | 최근 구간 1묶음 | 비교 대상이 개별 동작이 아니라 최근 묶음과 기준 묶음이기 때문 |
| 나중에 `검토 필요`를 예측할 입력 표를 만들 수 있는가 | 동작 1회 | 결과가 보통 동작 1회 단위에 붙고, 특징도 그 단위에서 안정적으로 계산되기 때문 |

즉 무엇을 샘플 1건으로 잡을지는 표 모양만 보고 정하는 것이 아니라, 지금 답하려는 질문이 `시점 비교`인지, `동작 비교`인지, `구간 비교`인지에 따라 먼저 정해야 합니다. 이 절의 예시에서는 `동작 전체의 패턴을 비교하려는 질문`을 놓고 있으므로, 동작 1회가 가장 자연스러운 샘플 단위가 됩니다.

## 작은 도식으로 보기

앞의 판단을 한 줄로 압축하면, 먼저 `지금 답할 질문`을 고르고 그 질문에 맞는 단위를 샘플로 삼아야 한다는 뜻입니다. 이 절의 예시에서는 `이번 동작이 이상했는가`를 묻고 있으므로 `동작 1회`가 비교 가능한 샘플로 이어집니다.

--8<-- "assets/part-03/chapter-04/p3-4-1-mermaid-01-ko.mmd"

문제 상황: 같은 원천 로그라도 `시점`, `동작 1회`, `최근 구간` 중 무엇을 샘플 1건으로 읽느냐에 따라 비교 가능한 표가 달라진다는 점을 확인합니다.

입력(input): `event_id`별 시점 기록 [p3_4_1_measurement_log.csv](../../../assets/part-03/chapter-04/p3_4_1_measurement_log.csv), `event_id` 단위 검토 결과 [p3_4_1_review_decisions.csv](../../../assets/part-03/chapter-04/p3_4_1_review_decisions.csv), 지금 답하려는 질문 후보 `question_focus_options`

첫 번째 CSV의 한 행은 동작 중 한 시점의 측정값입니다. 두 번째 CSV의 한 행은 동작 1회가 끝난 뒤 붙은 검토 결과입니다. 일부 이벤트는 시점 행 수가 부족하거나 검토 결과가 아직 없으므로, 코드가 먼저 샘플 단위를 다시 만들고 완전성과 라벨 결합 가능성을 따로 확인해야 합니다.

기대 출력(output): `measurement_row`, `event`, `window` 세 단위가 서로 다른 샘플 수와 특징 가능성을 만든다는 출력. 질문 초점과 이벤트 완전성 기준을 바꾸면 추천 단위와 유효 샘플 수도 함께 달라진다.

확인할 개념: 비교 가능한 샘플 1건은 눈앞의 행 수가 아니라 질문에 맞는 분석 단위에서 정해진다. 샘플 단위는 고정 정답이 아니라 질문과 특징·라벨 연결성에 따라 선택된다.

```python
import pandas as pd

measurement_log_path = "docs/assets/part-03/chapter-04/p3_4_1_measurement_log.csv"
review_decisions_path = "docs/assets/part-03/chapter-04/p3_4_1_review_decisions.csv"

question_focus_options = ["instant_value", "event_comparison", "recent_vs_baseline"]
selected_question_focus = "event_comparison"
expected_rows_per_event = 3

raw = pd.read_csv(measurement_log_path)
review_decisions = pd.read_csv(review_decisions_path)

row_counts = raw.groupby("event_id", as_index=False).size().rename(columns={"size": "measurement_rows"})

event_summary = (
    raw.groupby("event_id", as_index=False)
    .agg(
        total_duration_seconds=("elapsed_seconds", "max"),
        pressure_mean=("pressure", "mean"),
        pressure_rise=("pressure", lambda s: s.iloc[-1] - s.iloc[0]),
        flow_mean=("flow", "mean"),
        is_recent=("is_recent", "max"),
    )
    .merge(row_counts, on="event_id")
    .merge(review_decisions, on="event_id", how="left")
)
matched_review_decisions = review_decisions[
    review_decisions["event_id"].isin(event_summary["event_id"])
].reset_index(drop=True)
event_summary["is_complete_event_sample"] = (
    event_summary["measurement_rows"] >= expected_rows_per_event
)
event_summary["has_review_label"] = event_summary["review_needed"].notna()
event_summary["window_name"] = event_summary["is_recent"].map({0: "baseline", 1: "recent"})
event_summary["pressure_mean_for_complete"] = event_summary["pressure_mean"].where(
    event_summary["is_complete_event_sample"]
)
event_summary["flow_mean_for_complete"] = event_summary["flow_mean"].where(
    event_summary["is_complete_event_sample"]
)

window_summary = (
    event_summary.groupby("window_name", as_index=False)
    .agg(
        event_count=("event_id", "count"),
        complete_event_count=("is_complete_event_sample", "sum"),
        labeled_event_count=("has_review_label", "sum"),
        pressure_mean_complete=("pressure_mean_for_complete", "mean"),
        flow_mean_complete=("flow_mean_for_complete", "mean"),
    )
)

unit_check = pd.DataFrame(
    [
        {
            "unit_name": "measurement_row",
            "sample_count": len(raw),
            "valid_sample_count": len(raw),
            "can_use_pressure_rise": "no",
            "label_attaches_naturally": "weak",
            "feature_score": 1,
            "label_score": 0,
        },
        {
            "unit_name": "event",
            "sample_count": len(event_summary),
            "valid_sample_count": int(event_summary["is_complete_event_sample"].sum()),
            "can_use_pressure_rise": "yes",
            "label_attaches_naturally": "yes",
            "feature_score": 3,
            "label_score": 2,
        },
        {
            "unit_name": "window",
            "sample_count": len(window_summary),
            "valid_sample_count": len(window_summary),
            "can_use_pressure_rise": "partial",
            "label_attaches_naturally": "weak",
            "feature_score": 2,
            "label_score": 1,
        },
    ]
)
recommended_unit = {
    "instant_value": "measurement_row",
    "event_comparison": "event",
    "recent_vs_baseline": "window",
}[selected_question_focus]
unit_check["selected_for_question"] = unit_check["unit_name"] == recommended_unit
unit_check["question_match_score"] = unit_check["selected_for_question"].map({True: 2, False: 0})
unit_check["total_score"] = (
    unit_check["feature_score"] + unit_check["label_score"] + unit_check["question_match_score"]
)

focus_result = pd.DataFrame(
    [
        {
            "question_focus": focus,
            "recommended_unit": {
                "instant_value": "measurement_row",
                "event_comparison": "event",
                "recent_vs_baseline": "window",
            }[focus],
        }
        for focus in question_focus_options
    ]
)

print("1) raw input files")
print("measurement_log shape:", raw.shape)
print("review_decisions shape:", review_decisions.shape)
print()
print("2) first raw measurement rows")
print(raw.head(8).to_string(index=False))
print()
print("3) count rows under each candidate unit")
print("measurement rows:", len(raw))
print("event samples:", len(event_summary))
print("window aggregates:", len(window_summary))
print()
print("4) raw rows still mean per-time-step records")
print(row_counts.to_string(index=False))
print()
print("5) review labels arrive at event_id level")
print(matched_review_decisions.to_string(index=False))
print()
print("6) event-level summaries check completeness and labels")
print(
    event_summary[
        [
            "event_id",
            "total_duration_seconds",
            "measurement_rows",
            "is_complete_event_sample",
            "pressure_mean",
            "pressure_rise",
            "flow_mean",
            "review_needed",
            "has_review_label",
        ]
    ].round(3).to_string(index=False)
)
print()
print("7) window-level aggregates are for broader comparison, not single-sample judgment")
print(window_summary.round(3).to_string(index=False))
print()
print("8) question focus changes the recommended unit")
print(focus_result.to_string(index=False))
print()
print("9) unit check for selected_question_focus = event_comparison")
print(unit_check.to_string(index=False))
```

예상 출력:

```text
1) raw input files
measurement_log shape: (36, 5)
review_decisions shape: (36, 2)

2) first raw measurement rows
event_id  elapsed_seconds  pressure  flow  is_recent
     E01                0       1.0   0.0          1
     E01                1       2.0   1.4          1
     E01                2       2.4   1.6          1
     E02                0       1.1   0.0          0
     E02                1       1.7   1.1          0
     E02                2       2.0   1.2          0
     E03                0       1.2   0.1          1
     E03                1       2.3   1.5          1

3) count rows under each candidate unit
measurement rows: 36
event samples: 12
window aggregates: 2

4) raw rows still mean per-time-step records
event_id  measurement_rows
     E01                 3
     E02                 3
     E03                 3
     E04                 3
     E05                 3
     E06                 3
     E07                 3
     E08                 3
     E09                 3
     E10                 3
     E11                 3
     E12                 3

5) review labels arrive at event_id level
event_id  review_needed
     E01              1
     E02              0
     E03              1
     E04              0
     E05              0
     E06              0
     E07              1
     E08              0
     E09              1
     E10              0
     E11              1
     E12              0

6) event-level summaries check completeness and labels
event_id  total_duration_seconds  measurement_rows  is_complete_event_sample  pressure_mean  pressure_rise  flow_mean  review_needed  has_review_label
     E01                       2                 3                      True          1.800            1.4      1.000              1              True
     E02                       2                 3                      True          1.600            0.9      0.767              0              True
     E03                       2                 3                      True          2.067            1.5      1.133              1              True
     E04                       2                 3                      True          1.233            0.6      0.633              0              True
     E05                       2                 3                      True          1.667            1.2      0.767              0              True
     E06                       2                 3                      True          1.733            0.9      0.800              0              True
     E07                       2                 3                      True          1.900            1.4      0.933              1              True
     E08                       2                 3                      True          1.467            0.8      0.700              0              True
     E09                       2                 3                      True          2.200            1.6      1.200              1              True
     E10                       2                 3                      True          1.633            0.9      0.700              0              True
     E11                       2                 3                      True          2.000            1.4      1.067              1              True
     E12                       2                 3                      True          1.267            0.8      0.567              0              True

7) window-level aggregates are for broader comparison, not single-sample judgment
window_name  event_count  complete_event_count  labeled_event_count  pressure_mean_complete  flow_mean_complete
   baseline            6                     6                    6                   1.489               0.694
     recent            6                     6                    6                   1.939               1.017

8) question focus changes the recommended unit
    question_focus recommended_unit
     instant_value  measurement_row
  event_comparison            event
recent_vs_baseline           window

9) unit check for selected_question_focus = event_comparison
      unit_name  sample_count  valid_sample_count can_use_pressure_rise label_attaches_naturally  feature_score  label_score  selected_for_question  question_match_score  total_score
measurement_row            36                  36                    no                     weak              1            0                  False                     0            1
          event            12                  12                   yes                      yes              3            2                   True                     2            7
         window             2                   2               partial                     weak              2            1                  False                     0            3
```

출력에서 먼저 봐야 할 것은 `몇 건으로 세고 있는가`입니다. 원시 표에서는 측정 시점이 36건이고, `event_id` 기준으로 묶으면 동작 1회 후보가 12건이며, 다시 최근/기준선 구간으로 묶으면 비교용 집계는 2건이 됩니다. 그런데 그다음에 봐야 할 것은 `어떤 값이 어느 단위에서만 의미가 생기는가`입니다. 검토 결과는 원시 시점 행에 반복해서 붙는 것이 아니라 `event_id` 단위로 따로 도착한 뒤, 동작 1회 요약 표에 결합됩니다. 여기서 조작할 값은 `selected_question_focus`, `question_focus_options`, `expected_rows_per_event`입니다. `"event_comparison"`으로 두면 동작 1회가 추천 단위가 되지만, `"instant_value"`로 바꾸면 측정 시점 행이 더 자연스럽고, `"recent_vs_baseline"`으로 바꾸면 최근/기준선 구간 집계가 더 자연스럽습니다. `expected_rows_per_event`를 4로 높이면 현재 12개 이벤트가 모두 완전한 이벤트 샘플에서 빠집니다. 즉 같은 원천데이터라도 `한 시점`, `동작 1회`, `최근 구간` 중 무엇을 샘플 1건으로 읽느냐에 따라 행 수와 표의 의미, 그 위에 놓을 수 있는 열의 역할, 유효 샘플 수가 함께 바뀝니다.

여기서 `unit check` 출력은 이 절의 판단을 더 직접적으로 보여 줍니다. `measurement_row`는 샘플 수는 가장 많지만 `pressure_rise`를 바로 올릴 수 없고, `review_needed` 같은 결과도 자연스럽게 붙기 어렵습니다. `window`는 최근 상태 해석에는 쓸 수 있지만 개별 동작 비교 샘플로는 약합니다. 반면 `event`는 샘플 수, 요약 특징, 결과 열이 한 단위 위에 함께 놓여 있어 이 절의 질문인 `비교 가능한 샘플 한 건`에 가장 잘 맞습니다.

이 예제는 샘플 단위를 세는 법만 보여 주는 것이 아닙니다.

| 여기서 보이는 값 | 어느 단위에서 자연스러운가 | 이유 |
| --- | --- | --- |
| `pressure`, `flow` 한 시점 값 | 측정 시점 | 그 순간의 관측값이기 때문 |
| `pressure_mean`, `pressure_rise` | 동작 1회 | 여러 시점을 묶어야만 계산되는 요약값이기 때문 |
| `event_count`, 최근 평균 | 최근 구간 또는 기준선 구간 | 여러 동작을 다시 묶은 비교 집계이기 때문 |

이렇게 보면 `샘플 1건을 정한다`는 말은 단지 행 개수를 줄이는 일이 아니라, 어떤 열이 현재 단위에서 자연스럽게 읽히는지까지 함께 정하는 일입니다.

처음 표를 받았을 때 아래처럼 아주 짧게 판별해 볼 수도 있습니다. 이 빠른 판별은 데이터 생애주기의 단계도 함께 보여 줍니다. 측정값 표는 관측과 기록에 가깝고, 동작 단위 표는 비교 가능한 샘플 표현에 가깝고, 최근 구간 표와 기준선 표는 해석과 의사결정 준비에 더 가깝습니다.

| 지금 보는 표가 이렇다면 | 먼저 의심할 행 의미 |
| --- | --- |
| 시간 열이 있고 같은 `event_id`가 여러 번 반복된다 | 한 시점 기록일 가능성이 크다 |
| `event_id`마다 한 줄만 있고 평균, 최대, 기울기 같은 요약 열이 있다 | 동작 1회 샘플일 가능성이 크다 |
| 최근 20건 평균, 이전 200건 평균 같은 비교 열이 있다 | 여러 동작을 묶은 구간 집계일 가능성이 크다 |

이 판별표의 목적은 표 이름을 외우는 데 있지 않습니다. 지금 손에 있는 행이 `즉시 비교할 샘플`인지, 아니면 아직 `샘플로 다시 묶어야 할 기록`인지를 빠르게 가르는 데 있습니다.

동작 단위 요약 표가 생겨야 평균, 기울기, 변동성 같은 특징을 안정적으로 만들 수 있고, 그 다음에야 최근 구간과 기준선 비교도 같은 단위 위에서 읽을 수 있습니다. 따라서 `한 행이 무엇인가`라는 질문은 샘플 단위 하나를 정하는 데서 끝나지 않고, Part 3 전체의 후속 구조를 지탱하는 바닥 규칙이 됩니다.

비교 가능한 샘플은 데이터가 먼저 정해 주는 것이 아니라, 질문이 요구하는 비교 단위와 그 위에 올릴 특징·라벨 구조가 함께 정합니다. 따라서 `샘플 1건`을 정한다는 말은 행 개수를 다시 세는 일이 아니라, 관측 단위와 집계 단위 사이에서 어떤 대상을 비교 가능한 분석 단위(analytical unit)로 둘지 결정하는 일입니다.

## 출처와 참고 자료

- W3C, `PROV-Overview`. provenance framework가 identifying an object와 representing derivation을 지원해야 한다고 정리하므로, 시점 기록, 동작 1회, 최근 구간처럼 서로 다른 단위를 구분해 어떤 대상을 분석 단위로 삼았는지 설명 가능해야 한다는 일반 근거가 됩니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`의 `labeled example`. example는 features와 label이 자연스럽게 붙는 단위여야 하므로, 시점 행이 아니라 동작 1회처럼 특징과 결과가 함께 놓이는 단위를 샘플로 삼아야 한다는 점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 기준 시점은 다른 시점과 비교하기 위한 reference라고 설명하므로, 기준선 구간과 비교하려면 먼저 무엇을 비교 단위로 둘지 정해야 한다는 일반 근거가 됩니다. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20

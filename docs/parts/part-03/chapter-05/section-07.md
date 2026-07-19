# P3-5.7 같은 샘플 뒤의 여러 후속 사건은 표 구조에서 어떻게 접어야 하는가

> Section ID: `P3-5.7`
> Version: `v2026.07.19`

샘플 단위와 입력 창을 정한 뒤에도 표 구조에서 한 번 더 막히는 지점이 있습니다. 같은 샘플 뒤에 후속 사건이 여러 개 붙는 경우입니다. 예를 들어 동작 1회 뒤에 `재점검`, `경고`, `실패`, `재방문`이 차례로 남을 수 있습니다. 이때 이를 하나의 결과 열로 어떻게 접을지 정하지 않으면, 같은 샘플이 표마다 다른 뜻으로 바뀌기 쉽습니다.

후속 사건이 여러 개라면 어떤 규칙으로 하나의 표 구조에 접었는지 먼저 적어야 합니다.

보통 아래 같은 접기 규칙이 생깁니다.

| 접기 규칙 | 뜻 |
| --- | --- |
| `any` | 하나라도 발생했으면 1 |
| `first` | 가장 먼저 나온 후속 사건을 대표로 둠 |
| `worst` | 가장 심한 상태를 대표로 둠 |
| `count` | 발생 횟수 자체를 남김 |

예를 들어 같은 샘플 뒤에 아래처럼 후속 사건이 남았다고 해 보겠습니다.

| event_id | follow_up_events |
| --- | --- |
| A | review, failure |
| B | review |
| C | none |

이를 어떤 표로 접을지에 따라 결과 열의 뜻이 달라집니다.

| event_id | any_failure | first_event | event_count |
| --- | ---: | --- | ---: |
| A | 1 | review | 2 |
| B | 0 | review | 1 |
| C | 0 | none | 0 |

즉 같은 원천 사건을 보고 있어도 `무엇을 대표 결과로 둘 것인가`에 따라 표 구조가 달라집니다. 이 문제는 대표 결과를 어떤 규칙으로 접어 표에 남길지 먼저 정해야 하는 데이터 모델링 문제입니다.

아래 메모를 먼저 남겨 두면 이후 혼동이 줄어듭니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 어떤 후속 사건들을 한 묶음으로 보는가 | 표가 다루는 결과 범위를 고정하기 위해 |
| `any`, `first`, `worst`, `count` 중 무엇으로 접었는가 | 결과 열의 뜻을 다시 설명하기 위해 |
| 접은 결과가 보고용인지 예측 후보용인지 | 비교 리포트와 target 후보를 섞지 않기 위해 |

작은 예시:

문제 상황: 같은 샘플 뒤에 여러 후속 사건이 있을 때 `first`, `worst`, `count`, `any` 같은 서로 다른 접기 규칙이 다른 결과 열을 만든다는 점을 확인합니다.

입력(input): 샘플 명단 [p3_5_7_sample_roster.csv](../../../assets/part-03/chapter-05/p3_5_7_sample_roster.csv), 후속 사건 로그 [p3_5_7_follow_up_events.csv](../../../assets/part-03/chapter-05/p3_5_7_follow_up_events.csv), 사건 심각도 표 [p3_5_7_event_severity.csv](../../../assets/part-03/chapter-05/p3_5_7_event_severity.csv), 실패로 볼 심각도 기준 후보 `failure_severity_cutoffs`

첫 번째 CSV의 한 행은 최종 결과 표에 남아야 할 샘플 1건입니다. 두 번째 CSV의 한 행은 샘플 뒤에 실제로 발생한 후속 사건 1건입니다. 세 번째 CSV는 사건 이름을 심각도 숫자로 바꿔 `worst`와 `any_failure` 규칙을 계산하게 합니다.

기대 출력(output): 같은 원천 사건에서도 `first_event`, `worst_event`, `event_count`, `event_sequence`, `any_failure`가 다르게 만들어지는 출력. `failure_severity_cutoffs`를 바꾸면 실패 후보 샘플 수와 샘플 목록이 달라진다.

확인할 개념: 후속 사건 여러 개를 하나의 결과 열로 접을 때는 어떤 규칙과 기준으로 접었는지 먼저 명세해야 표 구조 뜻이 흔들리지 않는다

```python
import pandas as pd

sample_roster_path = "docs/assets/part-03/chapter-05/p3_5_7_sample_roster.csv"
follow_up_events_path = "docs/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv"
event_severity_path = "docs/assets/part-03/chapter-05/p3_5_7_event_severity.csv"

selected_failure_severity_cutoff = 4
failure_severity_cutoffs = [4, 3, 2]

sample_roster = pd.read_csv(sample_roster_path)
follow_ups = pd.read_csv(follow_up_events_path)
severity_table = pd.read_csv(event_severity_path)

follow_ups_with_severity = follow_ups.merge(severity_table, on="event_type", how="left")
ordered_events = follow_ups_with_severity.sort_values(["sample_id", "days_after_sample"])

first_events = (
    ordered_events.groupby("sample_id", as_index=False)
    .first()[["sample_id", "event_type"]]
    .rename(columns={"event_type": "first_event"})
)
worst_events = (
    ordered_events.sort_values(
        ["sample_id", "severity", "days_after_sample"],
        ascending=[True, False, True],
    )
    .groupby("sample_id", as_index=False)
    .first()[["sample_id", "event_type", "severity"]]
    .rename(columns={"event_type": "worst_event", "severity": "worst_severity"})
)
event_counts = (
    ordered_events.groupby("sample_id", as_index=False)
    .size()
    .rename(columns={"size": "event_count"})
)
event_sequences = (
    ordered_events.groupby("sample_id")["event_type"]
    .agg(lambda events: " > ".join(events))
    .reset_index(name="event_sequence")
)

folded = (
    sample_roster[["sample_id"]]
    .merge(first_events, on="sample_id", how="left")
    .merge(worst_events, on="sample_id", how="left")
    .merge(event_counts, on="sample_id", how="left")
    .merge(event_sequences, on="sample_id", how="left")
)
folded[["first_event", "worst_event", "event_sequence"]] = folded[
    ["first_event", "worst_event", "event_sequence"]
].fillna("none")
folded[["event_count", "worst_severity"]] = folded[
    ["event_count", "worst_severity"]
].fillna(0).astype(int)
folded["any_failure"] = (
    folded["worst_severity"] >= selected_failure_severity_cutoff
).astype(int)

cutoff_results = []
for cutoff in failure_severity_cutoffs:
    failed = folded[folded["worst_severity"] >= cutoff]
    cutoff_results.append(
        {
            "failure_severity_cutoff": cutoff,
            "failure_sample_count": len(failed),
            "failure_samples": ",".join(failed["sample_id"]) or "none",
        }
    )

print("1) raw follow-up events")
print(follow_ups.to_string(index=False))
print()
print("2) severity rule table")
print(severity_table.to_string(index=False))
print()
print("3) folded result when failure_severity_cutoff = 4")
print(folded.to_string(index=False))
print()
print("4) sensitivity by failure_severity_cutoff")
print(pd.DataFrame(cutoff_results).to_string(index=False))
```

예상 출력:

```text
1) raw follow-up events
sample_id  days_after_sample event_type source_system
        A                  1     review   human_queue
        A                  3    warning       monitor
        A                  5    failure   maintenance
        B                  2     review   human_queue
        B                  4    warning       monitor
        D                  1    warning       monitor
        E                  1    revisit       service
        E                  2     review   human_queue

2) severity rule table
event_type  severity
      none         0
   revisit         1
    review         2
   warning         3
   failure         4

3) folded result when failure_severity_cutoff = 4
sample_id first_event worst_event  worst_severity  event_count             event_sequence  any_failure
        A      review     failure               4            3 review > warning > failure            1
        B      review     warning               3            2           review > warning            0
        C        none        none               0            0                       none            0
        D     warning     warning               3            1                    warning            0
        E     revisit      review               2            2           revisit > review            0

4) sensitivity by failure_severity_cutoff
 failure_severity_cutoff  failure_sample_count failure_samples
                       4                     1               A
                       3                     3           A,B,D
                       2                     4         A,B,D,E
```

이 예시의 핵심은 같은 원천 사건을 보고도 `first_event`, `worst_event`, `event_count`, `event_sequence`, `any_failure`가 서로 다른 결과 열로 만들어질 수 있다는 점입니다. A는 첫 후속 사건이 `review`이지만 가장 심한 사건은 `failure`이고, B는 첫 사건이 `review`이지만 가장 심한 사건은 `warning`입니다. C처럼 후속 사건이 없는 샘플도 샘플 명단에는 있으므로 `none`과 0으로 접혀 최종 표에 남습니다. 여기서 조작할 값은 `selected_failure_severity_cutoff`와 `failure_severity_cutoffs`입니다. 기준을 4로 두면 `failure`가 있는 A만 실패 후보가 되지만, 3으로 낮추면 `warning`이 있는 B와 D도 실패 후보가 됩니다. 2로 낮추면 `review`가 가장 심한 E까지 포함됩니다. 즉 어떤 규칙과 기준으로 접었는지를 적지 않으면 같은 후속 사건 로그도 표마다 다른 뜻으로 읽히게 됩니다.

## 작은 도식으로 보기

이 절은 `여러 후속 사건`이 자동으로 하나의 결과 열이 되지 않는다는 점을 압축합니다. 같은 사건 목록도 `any`, `first`, `worst`, `count` 가운데 어떤 규칙으로 접느냐에 따라 다른 대표 결과 열로 바뀝니다.

--8<-- "assets/part-03/chapter-05/p3-5-7-mermaid-01-ko.mmd"

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `label`과 `labeled example`. result information이 어떤 example에 붙는지 먼저 정해져야 하므로, 후속 사건 여러 개를 하나의 결과 열로 접을 때도 `any`, `first`, `worst`, `count` 가운데 어떤 규칙을 썼는지 먼저 명세해야 한다는 이 절의 판단을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- Google for Developers, `Machine Learning Glossary`의 `label leakage`. 결과 열이 어떤 규칙으로 만들어졌는지 불분명하면 보고용 결과와 예측 후보용 결과를 섞어 읽기 쉬우므로, 접기 규칙을 먼저 적어 표 구조의 뜻을 고정해야 한다는 설명을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- W3C, `PROV-Overview`. provenance framework가 derivation과 activity context를 설명 가능하게 남겨야 한다고 정리하므로, 여러 후속 사건이 어떤 규칙을 거쳐 대표 결과 열로 접혔는지 추적 가능해야 한다는 상위 프레임을 제공합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08

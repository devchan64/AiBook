# P3-5.7 같은 샘플 뒤의 여러 후속 사건은 표 구조에서 어떻게 접어야 하는가

> Section ID: `P3-5.7`
> Version: `v2026.07.20`

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
# 같은 샘플 뒤의 여러 후속 사건을 표 구조에 맞게 접고 대표 라벨을 정하는 예제입니다.
import csv
from collections import defaultdict
from pathlib import Path

sample_roster_path = Path("docs/assets/part-03/chapter-05/p3_5_7_sample_roster.csv")
follow_up_events_path = Path("docs/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv")
event_severity_path = Path("docs/assets/part-03/chapter-05/p3_5_7_event_severity.csv")

selected_failure_severity_cutoff = 4
failure_severity_cutoffs = [4, 3, 2]
preview_row_count = 12


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


sample_roster = read_csv(sample_roster_path)
follow_ups = read_csv(follow_up_events_path)
severity_table = read_csv(event_severity_path)
severity_by_type = {row["event_type"]: int(row["severity"]) for row in severity_table}

for row in follow_ups:
    row["days_after_sample"] = int(row["days_after_sample"])
    row["severity"] = severity_by_type[row["event_type"]]

ordered_events = sorted(follow_ups, key=lambda row: (row["sample_id"], row["days_after_sample"]))
events_by_sample = defaultdict(list)
for row in ordered_events:
    events_by_sample[row["sample_id"]].append(row)

folded = []
for sample in sample_roster:
    sample_id = sample["sample_id"]
    events = events_by_sample.get(sample_id, [])
    if events:
        first_event = events[0]["event_type"]
        worst = sorted(events, key=lambda row: (-row["severity"], row["days_after_sample"]))[0]
        worst_event = worst["event_type"]
        worst_severity = worst["severity"]
        event_sequence = " > ".join(row["event_type"] for row in events)
    else:
        first_event = "none"
        worst_event = "none"
        worst_severity = 0
        event_sequence = "none"
    folded.append(
        {
            "sample_id": sample_id,
            "first_event": first_event,
            "worst_event": worst_event,
            "worst_severity": worst_severity,
            "event_count": len(events),
            "event_sequence": event_sequence,
            "any_failure": int(worst_severity >= selected_failure_severity_cutoff),
        }
    )

cutoff_results = []
for cutoff in failure_severity_cutoffs:
    failed = [row for row in folded if row["worst_severity"] >= cutoff]
    cutoff_results.append(
        {
            "failure_severity_cutoff": cutoff,
            "failure_sample_count": len(failed),
            "failure_samples": ",".join(row["sample_id"] for row in failed) or "none",
        }
    )

print("1) raw follow-up events")
print("sample_id  days_after_sample       event_type source_system")
for row in follow_ups[:preview_row_count]:
    print(
        f"{row['sample_id']:>9} {row['days_after_sample']:>18} "
        f"{row['event_type']:>16} {row['source_system']:>13}"
    )
print(f"... {len(follow_ups) - preview_row_count} more follow-up events")
print()
print("2) severity rule table")
print("      event_type  severity")
for row in severity_table[:preview_row_count]:
    print(f"{row['event_type']:>16} {int(row['severity']):>9}")
print(f"... {len(severity_table) - preview_row_count} more severity rules")
print()
print("3) folded result when failure_severity_cutoff = 4")
print(
    "sample_id      first_event      worst_event  worst_severity  event_count"
    "             event_sequence  any_failure"
)
for row in folded[:preview_row_count]:
    print(
        f"{row['sample_id']:>9} {row['first_event']:>16} {row['worst_event']:>16} "
        f"{row['worst_severity']:>15} {row['event_count']:>12} "
        f"{row['event_sequence']:>26} {row['any_failure']:>12}"
    )
print(f"... {len(folded) - preview_row_count} more folded samples")
print()
print("4) sensitivity by failure_severity_cutoff")
print(
    " failure_severity_cutoff  failure_sample_count"
    "                                                                     failure_samples"
)
for row in cutoff_results:
    print(
        f"{row['failure_severity_cutoff']:>24} {row['failure_sample_count']:>21} "
        f"{row['failure_samples']:>83}"
    )
```

예상 출력:

```text
1) raw follow-up events
sample_id  days_after_sample       event_type source_system
      S01                  1           review   human_queue
      S01                  3          warning       monitor
      S01                  5          failure   maintenance
      S02                  2           review   human_queue
      S02                  4          warning       monitor
      S03                  1          revisit       service
      S04                  1          warning       monitor
      S05                  1          revisit       service
      S05                  2           review   human_queue
      S06                  3 minor_adjustment      operator
      S07                  1          warning       monitor
      S07                  6          failure   maintenance
... 24 more follow-up events

2) severity rule table
      event_type  severity
            none         0
         revisit         1
minor_adjustment         1
      inspection         2
          review         2
         warning         3
         failure         4
critical_failure         5
    sensor_noise         0
   operator_note         1
     calibration         1
   slow_recovery         2
... 24 more severity rules

3) folded result when failure_severity_cutoff = 4
sample_id      first_event      worst_event  worst_severity  event_count             event_sequence  any_failure
      S01           review          failure               4            3 review > warning > failure            1
      S02           review          warning               3            2           review > warning            0
      S03          revisit          revisit               1            1                    revisit            0
      S04          warning          warning               3            1                    warning            0
      S05          revisit           review               2            2           revisit > review            0
      S06 minor_adjustment minor_adjustment               1            1           minor_adjustment            0
      S07          warning          failure               4            2          warning > failure            1
      S08           review           review               2            1                     review            0
      S09          revisit          revisit               1            1                    revisit            0
      S10          warning          warning               3            1                    warning            0
      S11       inspection       inspection               2            1                 inspection            0
      S12           review          warning               3            2           review > warning            0
... 24 more folded samples

4) sensitivity by failure_severity_cutoff
 failure_severity_cutoff  failure_sample_count                                                                     failure_samples
                       4                     5                                                                 S01,S07,S13,S19,S25
                       3                    12                                     S01,S02,S04,S07,S10,S12,S13,S16,S19,S22,S25,S28
                       2                    21 S01,S02,S04,S05,S07,S08,S10,S11,S12,S13,S16,S17,S18,S19,S21,S22,S24,S25,S26,S28,S29
```

이 예시의 핵심은 같은 원천 사건을 보고도 `first_event`, `worst_event`, `event_count`, `event_sequence`, `any_failure`가 서로 다른 결과 열로 만들어질 수 있다는 점입니다. S01은 첫 후속 사건이 `review`이지만 가장 심한 사건은 `failure`이고, S02는 첫 사건이 `review`이지만 가장 심한 사건은 `warning`입니다. S30처럼 후속 사건이 없는 샘플도 샘플 명단에는 있으므로 `none`과 0으로 접혀 최종 표에 남습니다. 여기서 조작할 값은 `selected_failure_severity_cutoff`와 `failure_severity_cutoffs`입니다. 기준을 4로 두면 `failure`가 있는 S01, S07, S13, S19, S25만 실패 후보가 되지만, 3으로 낮추면 `warning`이 가장 심한 샘플들도 실패 후보에 들어갑니다. 2로 낮추면 `review`나 `inspection`이 가장 심한 샘플까지 포함됩니다. 즉 어떤 규칙과 기준으로 접었는지를 적지 않으면 같은 후속 사건 로그도 표마다 다른 뜻으로 읽히게 됩니다.

## 작은 도식으로 보기

이 절은 `여러 후속 사건`이 자동으로 하나의 결과 열이 되지 않는다는 점을 압축합니다. 같은 사건 목록도 `any`, `first`, `worst`, `count` 가운데 어떤 규칙으로 접느냐에 따라 다른 대표 결과 열로 바뀝니다.

--8<-- "assets/part-03/chapter-05/p3-5-7-mermaid-01-ko.mmd"

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `label`과 `labeled example`. result information이 어떤 example에 붙는지 먼저 정해져야 하므로, 후속 사건 여러 개를 하나의 결과 열로 접을 때도 `any`, `first`, `worst`, `count` 가운데 어떤 규칙을 썼는지 먼저 명세해야 한다는 이 절의 판단을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Machine Learning Glossary`의 `label leakage`. 결과 열이 어떤 규칙으로 만들어졌는지 불분명하면 보고용 결과와 예측 후보용 결과를 섞어 읽기 쉬우므로, 접기 규칙을 먼저 적어 표 구조의 뜻을 고정해야 한다는 설명을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. provenance framework가 derivation과 activity context를 설명 가능하게 남겨야 한다고 정리하므로, 여러 후속 사건이 어떤 규칙을 거쳐 대표 결과 열로 접혔는지 추적 가능해야 한다는 상위 프레임을 제공합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20

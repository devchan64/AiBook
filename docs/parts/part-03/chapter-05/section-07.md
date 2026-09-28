# P3-5.7 여러 후속 사건을 접는 규칙

> Section ID: `P3-5.7`
> Version: `v2026.09.19`

_보조제목: 같은 샘플 뒤의 여러 사건은 어떤 규칙으로 하나의 표 구조에 접어야 하는가_

[샘플(sample)](../../../reference/concept-glossary-parts/07-siot.md#glossary-sample) 단위와 입력 창을 정한 뒤에도 표 구조에서 한 번 더 막히는 지점이 있습니다. 같은 샘플 뒤에 후속 사건이 여러 개 붙는 경우입니다. 예를 들어 동작 1회 뒤에 `재점검`, `경고`, `실패`, `재방문`이 차례로 남을 수 있습니다. 이때 이를 하나의 결과 열로 어떻게 접을지 정하지 않으면, 같은 샘플이 표마다 다른 뜻으로 바뀌기 쉽습니다.

후속 사건이 여러 개라면 어떤 [접기 규칙(folding rule)](../../../reference/concept-glossary-parts/03-digeut.md#data-modeling)으로 하나의 표 구조에 접었는지 먼저 적어야 합니다.

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

즉 같은 [원천 사건(source event)](../../../reference/concept-glossary-parts/08-ieung.md#glossary-source-data)을 보고 있어도 `무엇을 대표 결과로 둘 것인가`에 따라 표 구조가 달라집니다. 이 문제는 대표 결과를 어떤 규칙으로 접어 표에 남길지 먼저 정해야 하는 데이터 모델링 문제입니다.

아래 메모를 먼저 남겨 두면 이후 혼동이 줄어듭니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 어떤 후속 사건들을 한 묶음으로 보는가 | 표가 다루는 결과 범위를 고정하기 위해 |
| `any`, `first`, `worst`, `count` 중 무엇으로 접었는가 | 결과 열의 뜻을 다시 설명하기 위해 |
| 접은 결과가 보고용인지 예측 후보용인지 | 비교 리포트와 목표 라벨 후보(target candidate)를 섞지 않기 위해 |

최종 표에는 접기 규칙 자체도 추적 가능하게 남겨야 합니다. 예를 들어 `folding_rule`, `severity_cutoff`, `follow_up_window_days`, `source_event_count`, `target_candidate_name`을 메모로 남기면 `any_selected_event=1`이 어떤 사건 범위와 임계값에서 나온 결과인지 다시 설명할 수 있습니다. 같은 후속 사건 로그라도 `first_event`와 `worst_event`는 다른 열이므로, 한 열 이름만 보고 실제 목표 라벨처럼 고정하지 않아야 합니다.

사건을 접기 전에는 관측 기간과 중복 제거 규칙도 정해야 합니다. `7일 내 실패 여부`라면 9일째의 실패는 포함하지 않습니다. 전송 재시도로 같은 사건이 두 번 저장되었다면 `count`에서 두 번 세지 않도록 사건 식별자를 대조합니다. `first`는 발생 시각으로 정렬하고, 같은 시각의 사건이나 같은 심각도끼리의 우선순위도 정해 둡니다.

아래 예제는 샘플 명단 전체의 추적이 끝났고, 후속 사건 로그는 분석할 기간으로 이미 제한되었으며 중복이 없다고 가정합니다. 이 가정에서만 사건이 없는 S30에 0을 붙일 수 있습니다. 아직 관찰 중인 샘플은 사건이 없더라도 `pending`으로 남겨야 합니다.

작은 예시:

문제 상황: 같은 샘플 뒤에 여러 후속 사건이 있을 때 `first`, `worst`, `count`, `any` 같은 서로 다른 접기 규칙이 다른 결과 열을 만든다는 점을 확인합니다.

입력(input): 샘플 명단 [p3_5_7_sample_roster.csv](../../../assets/part-03/chapter-05/p3_5_7_sample_roster.csv){ .csv-preview }, 후속 사건 로그 [p3_5_7_follow_up_events.csv](../../../assets/part-03/chapter-05/p3_5_7_follow_up_events.csv){ .csv-preview }, 사건 심각도 표 [p3_5_7_event_severity.csv](../../../assets/part-03/chapter-05/p3_5_7_event_severity.csv){ .csv-preview }, 선택할 심각도 기준 후보 `severity_cutoffs`

첫 번째 CSV의 한 행은 최종 결과 표에 남아야 할 샘플 1건입니다. 두 번째 CSV의 한 행은 샘플 뒤에 실제로 발생한 후속 사건 1건입니다. 세 번째 CSV는 사건 이름을 심각도 숫자로 바꿔 `worst`와 `any_selected_event` 규칙을 계산하게 합니다.

기대 출력(output): 같은 원천 사건에서도 `first_event`, `worst_event`, `event_count`, `event_sequence`, `any_failure`, `any_selected_event`가 다르게 만들어지는 출력. `severity_cutoffs`를 바꾸면 선택 샘플 수와 샘플 목록이 달라진다.

확인할 개념: 후속 사건 여러 개를 하나의 결과 열로 접을 때는 어떤 접기 규칙과 [임계값(threshold)](../../../reference/concept-glossary-parts/08-ieung.md#glossary-threshold) 기준으로 접었는지 먼저 명세해야 표 구조 뜻이 흔들리지 않는다

## S01·S02·S30을 직접 접어 보기

이하 CSV는 자체 가상 자료입니다. 이 사례의 관측 기간은 샘플 뒤 1~7일(양 끝 포함)이며, 샘플 명단 36건 모두 추적을 마쳤다고 가정합니다. `days_after_sample`은 일 단위 위치이지 정확한 발생 시각이 아닙니다. CSV에는 추적 완료 표시와 개별 후속 사건 ID가 없으므로 완료·중복 없음은 이 자료만으로 검증할 수 없는 전제입니다.

| sample_id | 기간 내 후속 기록 | first_event | worst_event | event_count | any_failure |
| --- | --- | --- | --- | ---: | ---: |
| S01 | 1일 review → 3일 warning → 5일 failure | review | failure | 3 | 1 |
| S02 | 2일 review → 4일 warning | review | warning | 2 | 0 |
| S30 | 없음, 추적 완료 가정 | none | none | 0 | 0 |

`any_failure`는 사건 종류가 `failure` 또는 `critical_failure`인 기록이 하나라도 있는지 나타냅니다. 이 사례의 종류 매핑이며, 심각도 기준을 바꾸어도 정의는 바뀌지 않습니다. `count`는 실패 횟수가 아니라 기간 내 모든 후속 사건 수입니다. `first`는 뒤의 실패를 가리고, `worst`는 앞선 경고와 재점검 순서를 가리므로 필요하면 `event_sequence`도 보존합니다.

심각도는 이 사례에서 정한 순서 등급입니다. review=2, warning=3, failure=4는 크기 순서를 정할 뿐, 실패가 재점검보다 두 배 심하다는 뜻은 아닙니다. `any_selected_event`는 **선택한 심각도 이상 사건이 있는가**이며, `any_failure`와 다른 질문입니다. S02는 기준 4에서 0, 기준 3에서 1이 되지만 실패 기록은 여전히 없습니다.

예제는 1~7일만 포함하고 `first`를 일 번호 순으로 정합니다. 같은 날이면 CSV 행 순서를 사용하므로 실제 시간 순서로 단정하지 않습니다. `worst`는 심각도 내림차순, 일 번호 오름차순, 마지막으로 원본 행 순서입니다. 실제 운영에서는 더 정밀한 발생 시각과 사건 ID를 확보해 동률·중복 처리 규칙을 정해야 합니다.

```python
# 같은 샘플 뒤의 여러 후속 사건을 표 구조에 맞게 접고 대표 라벨을 정하는 예제입니다.
import csv
from collections import defaultdict
from pathlib import Path

sample_roster_path = Path("docs/assets/part-03/chapter-05/p3_5_7_sample_roster.csv")
follow_up_events_path = Path("docs/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv")
event_severity_path = Path("docs/assets/part-03/chapter-05/p3_5_7_event_severity.csv")

selected_severity_cutoff = 4
severity_cutoffs = [4, 3, 2]
follow_up_window_days = 7
failure_types = {"failure", "critical_failure"}
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

period_events = [row for row in follow_ups if 1 <= row["days_after_sample"] <= follow_up_window_days]
ordered_events = sorted(period_events, key=lambda row: (row["sample_id"], row["days_after_sample"]))
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
            "any_failure": int(any(row["event_type"] in failure_types for row in events)),
            "any_selected_event": int(any(row["severity"] >= selected_severity_cutoff for row in events)),
        }
    )

cutoff_results = []
for cutoff in severity_cutoffs:
    selected = [row for row in folded if row["event_count"] > 0 and row["worst_severity"] >= cutoff]
    cutoff_results.append(
        {
            "severity_cutoff": cutoff,
            "selected_sample_count": len(selected),
            "selected_samples": ",".join(row["sample_id"] for row in selected) or "none",
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
print(f"3) folded result when severity_cutoff = {selected_severity_cutoff}")
print(
    "sample_id      first_event      worst_event  worst_severity  event_count"
    "             event_sequence  any_failure  any_selected_event"
)
for row in folded[:preview_row_count]:
    print(
        f"{row['sample_id']:>9} {row['first_event']:>16} {row['worst_event']:>16} "
        f"{row['worst_severity']:>15} {row['event_count']:>12} "
        f"{row['event_sequence']:>26} {row['any_failure']:>12} {row['any_selected_event']:>19}"
    )
print(f"... {len(folded) - preview_row_count} more folded samples")
print()
print("4) sensitivity by severity_cutoff")
print(
    " severity_cutoff  selected_sample_count"
    "                                                                     selected_samples"
)
for row in cutoff_results:
    print(
        f"{row['severity_cutoff']:>24} {row['selected_sample_count']:>21} "
        f"{row['selected_samples']:>83}"
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

3) folded result when severity_cutoff = 4
sample_id      first_event      worst_event  worst_severity  event_count             event_sequence  any_failure  any_selected_event
      S01           review          failure               4            3 review > warning > failure            1                   1
      S02           review          warning               3            2           review > warning            0                   0
      S03          revisit          revisit               1            1                    revisit            0                   0
      S04          warning          warning               3            1                    warning            0                   0
      S05          revisit           review               2            2           revisit > review            0                   0
      S06 minor_adjustment minor_adjustment               1            1           minor_adjustment            0                   0
      S07          warning          failure               4            2          warning > failure            1                   1
      S08           review           review               2            1                     review            0                   0
      S09          revisit          revisit               1            1                    revisit            0                   0
      S10          warning          warning               3            1                    warning            0                   0
      S11       inspection       inspection               2            1                 inspection            0                   0
      S12           review          warning               3            2           review > warning            0                   0
... 24 more folded samples

4) sensitivity by severity_cutoff
 severity_cutoff  selected_sample_count                                                                     selected_samples
                       4                     5                                                                 S01,S07,S13,S19,S25
                       3                    12                                     S01,S02,S04,S07,S10,S12,S13,S16,S19,S22,S25,S28
                       2                    21 S01,S02,S04,S05,S07,S08,S10,S11,S12,S13,S16,S17,S18,S19,S21,S22,S24,S25,S26,S28,S29
```

기준별 선택 샘플 수는 4에서 5건, 3에서 12건, 2에서 21건입니다. 4→3으로 바꿀 때 새로 들어오는 **S02, S04, S10, S12, S16, S22, S28**은 가장 심한 기록이 warning인 7건입니다. 새 실패가 발생한 것이 아니라 선택 범위를 넓힌 결과입니다. 실제 실패 종류를 기록한 샘플 수는 계속 5건입니다.

실행 전에 `selected_severity_cutoff`를 3으로 바꾸면 S02의 두 표시가 어떻게 될지 예상해 보세요. 답은 `any_selected_event=1`, `any_failure=0`입니다. 이어서 S01의 failure가 5일이 아니라 9일에 발생했다고 가정하면 7일 내 결과는 first=review, worst=warning, count=2, any_failure=0입니다. 관측 기간 밖으로 빠진 것이지 원래 사건을 삭제한 것은 아닙니다.

S30의 추적이 아직 끝나지 않았다면 `none`과 0으로 확정할 수 없습니다. 이 코드는 완료된 가상 명단을 전제로 하므로, 실제 미완료 자료는 완료 상태를 추가해 `pending`으로 따로 처리해야 합니다. 샘플 시점의 예측 입력에 이 후속 결과를 섞어 넣지도 않습니다. 결과 열을 [지도학습 라벨](../../../reference/concept-glossary-parts/09-jieut.md#supervised-learning-label)로 쓸지는 예측 시점과 목표를 정한 뒤 판단합니다.


## 여러 후속 사건을 샘플별 결과로 묶기 {#_1}

이 절은 `여러 후속 사건`이 자동으로 하나의 결과 열이 되지 않는다는 점을 압축합니다. 같은 사건 목록도 `any`, `first`, `worst`, `count` 가운데 어떤 규칙으로 접느냐에 따라 다른 대표 결과 열로 바뀝니다.

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-7-mermaid-01-ko.mmd"
```

## 체크리스트

- S02에서 기준 4→3 변경이 실패 발생이 아니라 선택 범위 변경임을 설명하는가?

- 후속 사건의 관측 기간·중복 처리·대표 라벨 선택 규칙을 적었는가?
- 후속 사건 0건과 관측 미완료를 구분했는가?

## 출처와 참고 자료

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary#label){: target="_blank" rel="noopener noreferrer" }. label과 labeled example의 정의를 참고했습니다. any/first/worst/count, 심각도 등급과 실패 종류 매핑은 본문의 자체 사례 설계입니다. / 2026-09-19
- W3C, [PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }. 자료의 생성·파생 과정을 추적하는 일반 근거입니다. 본문의 집계 규칙을 직접 규정하는 자료는 아닙니다. / 2026-09-19

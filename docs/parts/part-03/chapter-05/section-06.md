# P3-5.6 겹치는 입력 창과 샘플 수

> Section ID: `P3-5.6`
> Version: `v2026.07.25`

_보조제목: 같은 사건을 여러 창으로 자르면 왜 샘플 수가 실제보다 커 보일 수 있는가_

[입력 창(input window)](../../../reference/concept-glossary-parts/05-mieum.md#model-input)을 정하고 나면 같은 [원천 시계열(source time series)](../../../reference/concept-glossary-parts/08-ieung.md#glossary-source-data)에서 여러 창을 만들 수 있습니다. 이때 자주 놓치는 문제가 있습니다. `창이 많아졌으니 샘플도 그만큼 늘었다`고 읽기 쉽다는 점입니다. 하지만 겹치는 창이 많아졌다는 것은 종종 `같은 사건을 여러 번 잘라 본다`는 뜻이지, 독립된 사건 수가 그만큼 늘었다는 뜻은 아닙니다.

입력 창 수와 [원천 사건(source event)](../../../reference/concept-glossary-parts/08-ieung.md#glossary-source-data) 수는 같은 숫자가 아닐 수 있습니다.

| 구분 | 뜻 |
| --- | --- |
| 원천 사건 수 | 실제로 있었던 동작 1회, 사건 1건의 수 |
| 입력 창 수 | 그 사건들에서 잘라 낸 학습 입력 조각 수 |

예를 들어 동작 1건에서 길이 30, stride 10으로 창을 자르면 하나의 사건이 여러 입력으로 늘어날 수 있습니다.

| event_id | 원천 길이 | 창 길이 | stride | 만들어진 창 수 |
| --- | ---: | ---: | ---: | ---: |
| A | 100 | 30 | 10 | 8 |
| B | 100 | 30 | 10 | 8 |

이 표를 보고 `샘플이 16건 있다`고만 말하면 절반만 맞습니다. 실제 사건은 2건이고, 입력 창은 16개입니다. 따라서 비교 리포트나 대표성 판단에서는 여전히 `2건의 사건`이라는 사실을 같이 적어야 합니다.

겹치는 창이 많을수록 아래 문제가 생기기 쉽습니다.

| 생기는 문제 | 왜 주의해야 하는가 |
| --- | --- |
| 샘플 수가 커 보인다 | 실제 사건 수보다 근거가 과장돼 보일 수 있다 |
| 비슷한 창이 반복된다 | 같은 사건의 패턴이 여러 번 나타나 독립성이 약해질 수 있다 |
| 최근 사건이 더 많이 잘린다 | 특정 사건의 영향이 표에서 과하게 커질 수 있다 |

지금 단계에서는 복잡한 평가 설계를 다루지 않아도 됩니다. 다만 아래 메모는 남겨 두는 편이 안전합니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 원천 사건 수 | 실제 근거 단위를 숨기지 않기 위해 |
| 입력 창 수 | 모델 입력 규모를 따로 보기 위해 |
| 창 길이와 stride | 어떤 규칙으로 창이 늘어났는지 다시 설명하기 위해 |

작은 예시를 보면 더 분명합니다.

문제 상황: 겹치는 입력 창이 많아졌을 때 창 수와 원천 사건 수를 같은 숫자로 읽으면 어떤 착시가 생기는지 확인합니다.

입력(input): 원천 사건 표 [p3_5_6_source_events.csv](/AiBook/assets/part-03/chapter-05/p3_5_6_source_events.csv)와 실험할 이동 간격 `stride_to_try`. 이 표의 한 행은 하나의 원천 사건이며, 사건 길이(`length`)와 창 길이(`window`)가 함께 들어 있습니다.

기대 출력(output): 각 사건이 몇 개 창으로 늘어나는지와 `source_event` 대비 `window` 수가 얼마나 커지는지 보여 주는 출력. `stride_to_try`를 바꾸면 창 수와 확장 비율이 달라진다.

확인할 개념: 입력 창 수는 파생 조각 수일 뿐이며 원천 사건 수와 같은 단위로 읽으면 안 된다

```python
# 겹치는 입력 창이 같은 사건을 반복해 세면서 샘플 수를 부풀리는지 확인하는 예제입니다.
import csv
from collections import defaultdict
from pathlib import Path

stride_to_try = 10
preview_event_count = 8
source_events_path = Path("docs/assets/part-03/chapter-05/p3_5_6_source_events.csv")

with source_events_path.open(newline="", encoding="utf-8") as file:
    events = []
    for row in csv.DictReader(file):
        length = int(row["length"])
        window = int(row["window"])
        window_count = ((length - window) // stride_to_try) + 1
        events.append(
            {
                "event_id": row["event_id"],
                "line_id": row["line_id"],
                "mode": row["mode"],
                "length": length,
                "window": window,
                "stride": stride_to_try,
                "window_count": window_count,
                "source_event_weight": 1,
            }
        )


def print_event_preview(rows):
    print("event_id line_id     mode  length  window  stride  window_count")
    for row in rows:
        print(
            f"{row['event_id']:>8} {row['line_id']:>7} {row['mode']:>8} "
            f"{row['length']:>7} {row['window']:>7} {row['stride']:>7} "
            f"{row['window_count']:>13}"
        )


def print_expansion_preview(rows):
    print("event_id  window_count")
    for row in rows:
        print(f"{row['event_id']:>8} {row['window_count']:>13}")

print("1) how many windows each source event creates")
print_event_preview(events[:preview_event_count])
print(f"... {len(events) - preview_event_count} more source events")
print()
print("2) source-event count vs window count")
print("          unit  count")
print(f"0  {'source_event':<12} {sum(row['source_event_weight'] for row in events):>5}")
print(f"1  {'window':>12} {sum(row['window_count'] for row in events):>5}")
print()
print("3) expansion per source event")
print_expansion_preview(events[:preview_event_count])
print(f"... {len(events) - preview_event_count} more source events")
print()
print("4) expansion summary by line and mode")
groups = defaultdict(lambda: {"source_event_count": 0, "window_count": 0})
for row in events:
    group = groups[(row["line_id"], row["mode"])]
    group["source_event_count"] += row["source_event_weight"]
    group["window_count"] += row["window_count"]

print("line_id     mode  source_event_count  window_count  mean_windows_per_event")
for line_id, mode in sorted(groups):
    group = groups[(line_id, mode)]
    mean_windows = group["window_count"] / group["source_event_count"]
    print(
        f"{line_id:>7} {mode:>8} {group['source_event_count']:>19} "
        f"{group['window_count']:>13} {mean_windows:>23.2f}"
    )
print()
print("5) expansion ratio")
print(round(sum(row["window_count"] for row in events) / len(events), 2))
```

예상 출력:

```text
1) how many windows each source event creates
event_id line_id     mode  length  window  stride  window_count
     E01      L1 baseline     100      30      10             8
     E02      L1 baseline      96      30      10             7
     E03      L1 baseline      92      30      10             7
     E04      L1 baseline      88      30      10             6
     E05      L1 baseline      84      30      10             6
     E06      L1 baseline      80      30      10             6
     E07      L1   recent     110      30      10             9
     E08      L1   recent     104      30      10             8
... 28 more source events

2) source-event count vs window count
          unit  count
0  source_event    36
1        window   237

3) expansion per source event
event_id  window_count
     E01             8
     E02             7
     E03             7
     E04             6
     E05             6
     E06             6
     E07             9
     E08             8
... 28 more source events

4) expansion summary by line and mode
line_id     mode  source_event_count  window_count  mean_windows_per_event
     L1 baseline                   6            40                    6.67
     L1   recent                   6            42                    7.00
     L2 baseline                   6            40                    6.67
     L2   recent                   6            43                    7.17
     L3 baseline                   6            34                    5.67
     L3   recent                   6            38                    6.33

5) expansion ratio
6.58
```

이 예제의 목적은 창 수를 계산하는 것보다 `창 수가 실제 사건 수를 얼마나 부풀려 보이게 하는가`를 확인하는 데 있습니다. 여기서 조작할 값은 `stride_to_try`입니다. `10`을 `20`으로 바꾸면 창 수와 확장 비율이 줄고, 더 작은 값으로 바꾸면 같은 원천 사건에서 더 많은 입력 조각이 생깁니다. 그런데 `source_event` 수는 계속 36건입니다. 그래서 겹치는 입력 창은 같은 사건을 여러 번 잘라 본 결과일 수 있으며, 창 수를 곧바로 사건 수처럼 읽으면 안 됩니다. 출력 4단계처럼 라인과 운영 모드별로 다시 묶어 보면, 원천 사건 수는 각 조건에서 6건씩 같아도 파생된 window 수는 길이와 창 설정에 따라 다르게 불어납니다.

## 작은 도식으로 보기

이 절의 핵심은 `창 수가 커진다`와 `원천 사건 수가 늘었다`를 분리하는 데 있습니다. 같은 두 사건에서 겹치는 창을 많이 만들면 입력 조각 수는 커지지만, 사건 수 자체는 그대로 남습니다.

--8<-- "assets/part-03/chapter-05/p3-5-6-mermaid-01-ko.mmd"

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `labeled example`. example는 features와 label이 붙는 단위를 전제로 하므로, 여러 입력 창이 생겼다고 해서 원천 사건 수 자체가 자동으로 늘어났다고 읽으면 안 된다는 이 절의 판단을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. provenance framework가 어떤 entity가 어떤 derivation을 거쳐 생성되었는지 추적해야 한다고 정리하므로, 각 입력 창이 어떤 원천 사건에서 파생되었는지 분리해 남겨야 창 수와 사건 수를 혼동하지 않는다는 상위 프레임을 제공합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Datasets: Dividing the original dataset`. 학습용 표본이 어떤 원천 데이터에서 어떤 규칙으로 만들어졌는지 구분해야 한다는 일반 관점을 제공하므로, 겹치는 창이 많을 때도 원천 사건 단위와 입력 조각 단위를 따로 적어야 한다는 이 절의 설명을 일반화하는 데 참고할 수 있습니다. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- scikit-learn developers, `Cross-validation: evaluating estimator performance`. 같은 원천 과정에서 나온 의존 샘플은 독립동일분포 가정이 깨질 수 있고, grouped data에서는 같은 그룹의 샘플이 훈련 fold와 검증 fold에 함께 나타나지 않게 해야 한다고 설명하므로, 겹치는 입력 창이 실제 사건 수를 늘린 것이 아니라 같은 사건에서 파생된 의존 조각일 수 있다는 이 절의 주의를 보강합니다. [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20

# P3-5.6 겹치는 입력 창과 샘플 수

> Section ID: `P3-5.6`
> Version: `v2026.09.19`

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

`stride`는 창 시작점을 몇 측정점씩 옮기는지 뜻합니다. 길이 100, 창 길이 30, 이동 간격 10이면 시작점은 0, 10, …, 70의 여덟 곳입니다. 끝에 남는 불완전 창을 버리는 규칙에서는 `창 수 = floor((원천 길이−창 길이)/이동 간격)+1`이고, 원천 길이가 창보다 짧으면 0개입니다. 여기서 `floor`는 소수점 아래를 버린다는 뜻입니다.

이 표를 보고 `샘플이 16건 있다`고만 말하면 절반만 맞습니다. 실제 사건은 2건이고, 입력 창은 16개입니다. 따라서 비교 리포트나 대표성 판단에서는 여전히 `2건의 사건`이라는 사실을 같이 적어야 합니다.

겹치는 창이 많을수록 아래 문제가 생기기 쉽습니다.

| 생기는 문제 | 왜 주의해야 하는가 |
| --- | --- |
| 샘플 수가 커 보인다 | 실제 사건 수보다 근거가 과장돼 보일 수 있다 |
| 비슷한 창이 반복된다 | 같은 사건의 패턴이 여러 번 나타나 독립성이 약해질 수 있다 |
| 길거나 더 촘촘하게 자른 사건이 더 많은 창을 만든다 | 특정 사건의 영향이 표에서 과하게 커질 수 있다 |

지금 단계에서는 복잡한 평가 설계를 다루지 않아도 됩니다. 다만 아래 메모는 남겨 두는 편이 안전합니다.

| 먼저 적을 메모 | 왜 필요한가 |
| --- | --- |
| 원천 사건 수 | 실제 근거 단위를 숨기지 않기 위해 |
| 입력 창 수 | 모델 입력 규모를 따로 보기 위해 |
| 창 길이와 stride | 어떤 규칙으로 창이 늘어났는지 다시 설명하기 위해 |

## 같은 관측점이 두 창에 들어간다

작은 가상 사건 A에 관측 순서대로 `[10, 11, 12, 13, 14, 15]`가 있다고 하겠습니다. 숫자는 측정값이고 위치 번호는 0부터 5입니다. 창 길이 4, 이동 간격 2에서 끝이 부족한 창은 버립니다. `[시작, 끝)` 표기는 시작 위치를 포함하고 끝 위치는 제외한다는 뜻입니다.

| source_event_id | window_id | 위치 범위 | 창에 들어간 값 |
| --- | --- | --- | --- |
| A | A-01 | [0, 4) | [10, 11, **12, 13**] |
| A | A-02 | [2, 6) | [**12, 13**, 14, 15] |

두 창에 든 12·13은 값만 우연히 같은 것이 아니라 **같은 위치 2·3의 관측**입니다. 창 안의 값은 합쳐 8칸이지만 서로 다른 원시 관측은 6개, 원천 사건은 1건입니다. 이동 간격을 1로 바꾸면 시작점 0·1·2에서 3개 창이 생기며, 새 사건이나 새 측정이 생기는 것은 아닙니다.

길이 100·창 30·이동 10의 앞 두 창도 [0, 30), [10, 40)으로, 위치 10~29의 관측 20개를 공유합니다. 여기서 길이와 이동 간격의 단위는 측정점 수입니다. 초 단위 길이로 바꾸려면 측정 간격을 알아야 합니다.

파생 창에는 `source_event_id`, `window_id`, `window_start`, `window_end`를 남기고, 창 길이·이동 간격·불완전 창 처리 규칙을 함께 기록합니다. 원천 표는 사건당 한 행인지 확인한 뒤 행 수를 세고, 창 표에서는 중복을 제거한 `source_event_id` 수를 세어야 합니다. 아래 예제는 사건 수를 직접 세므로 별도 사건 가중치 열이 필요하지 않습니다.

문제 상황: 겹치는 입력 창이 많아졌을 때 창 수와 원천 사건 수를 같은 숫자로 읽으면 어떤 착시가 생기는지 확인합니다.

입력(input): 원천 사건 표 [p3_5_6_source_events.csv](/AiBook/assets/part-03/chapter-05/p3_5_6_source_events.csv){ .csv-preview }와 실험할 이동 간격 `stride_to_try`. 이 표의 한 행은 하나의 원천 사건이며, 사건 길이(`length`)와 창 길이(`window`)가 함께 들어 있습니다.

기대 출력(output): 각 사건이 몇 개 창으로 늘어나는지와 `source_event` 대비 `window` 수가 얼마나 커지는지 보여 주는 출력. `stride_to_try`를 바꾸면 창 수와 확장 비율이 달라진다.

확인할 개념: 입력 창 수는 파생 조각 수일 뿐이며 원천 사건 수와 같은 단위로 읽으면 안 된다

```python
# 겹치는 입력 창이 같은 사건을 반복해 세면서 샘플 수를 부풀리는지 확인하는 예제입니다.
import csv
from collections import defaultdict
from pathlib import Path

stride_to_try = 10
if not isinstance(stride_to_try, int) or isinstance(stride_to_try, bool) or stride_to_try <= 0:
    raise ValueError("stride_to_try must be a positive integer")
preview_event_count = 8
source_events_path = Path("docs/assets/part-03/chapter-05/p3_5_6_source_events.csv")

with source_events_path.open(newline="", encoding="utf-8") as file:
    events = []
    for row in csv.DictReader(file):
        length = int(row["length"])
        window = int(row["window"])
        if length < 0 or window <= 0:
            raise ValueError("length must be nonnegative and window positive")
        window_count = max(0, ((length - window) // stride_to_try) + 1)
        events.append(
            {
                "event_id": row["event_id"],
                "line_id": row["line_id"],
                "mode": row["mode"],
                "length": length,
                "window": window,
                "stride": stride_to_try,
                "window_count": window_count,
            }
        )


if not events:
    raise ValueError("source-event table must not be empty")
if len({row["event_id"] for row in events}) != len(events):
    raise ValueError("event_id must be unique in the source-event table")

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
print(f"... {max(0, len(events) - preview_event_count)} more source events")
print()
print("2) source-event count vs window count")
print("          unit  count")
print(f"0  {'source_event':<12} {len(events):>5}")
print(f"1  {'window':>12} {sum(row['window_count'] for row in events):>5}")
print()
print("3) expansion per source event")
print_expansion_preview(events[:preview_event_count])
print(f"... {max(0, len(events) - preview_event_count)} more source events")
print()
print("4) expansion summary by line and mode")
groups = defaultdict(lambda: {"source_event_count": 0, "window_count": 0})
for row in events:
    group = groups[(row["line_id"], row["mode"])]
    group["source_event_count"] += 1
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

## 6.58의 분모는 원천 사건 36건이다

기본 출력의 **237개 창 ÷ 36건 사건 ≈ 6.58개/사건**은 사건당 평균 창 수입니다. 새 정보가 6.58배 생겼거나 독립 사건이 237건이라는 뜻이 아닙니다. 짧아서 창을 못 만드는 사건이 있더라도 이 계산의 분모는 입력 원천 표 전체의 사건 수이며, 창이 하나 이상 생긴 사건 수와 구분해야 합니다.

| stride: 측정점 수 | 입력 원천 사건 수: 건 | 창 수: 개 | 사건당 평균 창 수: 개/사건 |
| ---: | ---: | ---: | ---: |
| 5 | 36 | 453 | 12.58 |
| 10 | 36 | 237 | 6.58 |
| 20 | 36 | 129 | 3.58 |

실행 전에 이동 간격을 20으로 바꾸면 무엇이 바뀔지 예상하고, 실행 후 표와 비교해 보세요. 답은 창 129개, 사건당 약 3.58개이며 사건 수는 36건 그대로입니다. E01만 계산해도 시작점 0·20·40·60의 4개 창이 됩니다. 70에서 시작하는 창을 임의로 추가하지 않는 규칙입니다.

조건별 출력에서 L2 recent와 L3 baseline은 각각 사건 6건이지만 창은 43개와 34개입니다. 창마다 같은 비중을 주면 두 조건은 43:34로 기여하고, 사건을 같은 비중으로 비교하면 6:6입니다. 어느 단위를 같은 비중으로 볼지 질문에 맞게 정해야 합니다. 최근이라는 이름 자체가 창을 늘리는 것은 아니며, 이 자료의 길이와 창 설정이 건수 차이를 만듭니다.

## 사건 ID가 달라도 독립성은 확인해야 한다

36개의 서로 다른 사건 ID는 36개의 독립적인 실험을 보증하지 않습니다. 같은 장비·날짜·작업 묶음에서 연속으로 나온 사건이면 공통 조건의 영향을 받을 수 있습니다. 반대로 겹치는 창이 쓸모없다는 뜻도 아닙니다. 한 사건의 서로 다른 위치를 입력으로 보여 주는 데 쓸 수 있지만, 새로운 사건을 수집한 것과는 구분합니다.

새 사건에서의 성능을 확인할 때 A-01을 학습에, A-02를 평가에 넣으면 같은 원시 관측이 양쪽에 들어갑니다. 원천 사건별로 나누는 것은 이 중복을 막는 한 방법이며, 새 장비나 미래 기간에 대한 평가라면 더 큰 묶음이나 시간 순서도 확인해야 합니다. 그래서 파생 창에서 원천 사건 ID를 지우지 않습니다.


## 입력 창 수와 원천 사건 수 구분하기 {#_1}

이 절의 핵심은 `창 수가 커진다`와 `원천 사건 수가 늘었다`를 분리하는 데 있습니다. 같은 두 사건에서 겹치는 창을 많이 만들면 입력 조각 수는 커지지만, 사건 수 자체는 그대로 남습니다.

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-6-mermaid-01-ko.mmd"
```

## 체크리스트

- 237개, 36건, 6.58개/사건을 서로 다른 단위로 해석하는가?
- 두 창이 공유하는 관측 위치를 짚고, stride 20에서 129개 창을 확인했는가?
- 원천 사건 수가 통계적 독립성을 보증하지 않는 이유를 설명하는가?

- 입력 길이와 이동 간격으로 생성 창 수를 계산했는가?
- 겹친 창 수가 독립적인 사건 수와 같지 않은 이유를 설명했는가?

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`, `example`, `labeled example`. example는 라벨이 없을 수도 있고, labeled example은 특징과 라벨을 함께 포함합니다. 중첩 창 수와 원천 사건 수를 따로 세는 것은 이 절의 사례에서 확인하는 구분입니다. [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-15
- W3C, `PROV-Overview`. provenance framework가 어떤 entity가 어떤 derivation을 거쳐 생성되었는지 추적해야 한다고 정리하므로, 각 입력 창이 어떤 원천 사건에서 파생되었는지 분리해 남겨야 창 수와 사건 수를 혼동하지 않는다는 상위 프레임을 제공합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google for Developers, `Datasets: Dividing the original dataset`. 학습용 표본이 어떤 원천 데이터에서 어떤 규칙으로 만들어졌는지 구분해야 한다는 일반 관점을 제공하므로, 겹치는 창이 많을 때도 원천 사건 단위와 입력 조각 단위를 따로 적어야 한다는 이 절의 설명을 일반화하는 데 참고할 수 있습니다. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- scikit-learn developers, `Cross-validation: evaluating estimator performance`. 같은 원천 과정에서 나온 의존 샘플은 독립동일분포 가정이 깨질 수 있고, grouped data에서는 같은 그룹의 샘플이 훈련 fold와 검증 fold에 함께 나타나지 않게 해야 한다고 설명하므로, 겹치는 입력 창이 실제 사건 수를 늘린 것이 아니라 같은 사건에서 파생된 의존 조각일 수 있다는 이 절의 주의를 보강합니다. [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-19

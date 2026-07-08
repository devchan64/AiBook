# P3-4.3 한 행, 샘플 1건, 최근 구간 1개는 어떻게 다른가

> Section ID: `P3-4.3`
> Version: `v2026.07.07`

`한 행`, `샘플 1건`, `최근 구간 1개`는 모두 데이터 표를 보며 떠오르지만 같은 층위가 아닙니다. 원천데이터 표에서는 행이 먼저 보이고, 동작 1회 비교에서는 샘플이 중심이 되며, 기준선 비교에서는 최근 구간이 또 다른 비교 단위로 등장합니다.

세 단위를 한 번에 구분해야 하는 이유는 특징, 기준선 비교, 검토 문장이 서로 다른 층위에 붙기 때문입니다. 행을 샘플로 착각하거나 구간을 샘플 한 건처럼 읽는 순간, 뒤에서 만드는 표와 비교 구조도 함께 흔들리기 시작합니다.

세 층위를 다시 나누면 다음과 같습니다.

- `한 행`은 지금 표 안에서 보이는 한 줄입니다.
- `샘플 1건`은 비교하거나 학습할 기본 단위입니다.
- `최근 구간 1개`는 샘플 여러 개를 다시 묶은 비교 단위입니다.

이 셋은 서로 포함될 수는 있어도 같은 뜻이 아닙니다.

| 지금 보는 대상 | 가장 자연스러운 질문 | 이 절에서의 층위 |
| --- | --- | --- |
| 시점별 로그 한 줄 | 지금 이 시점에 무엇이 측정되었는가 | 행 |
| 동작 1회 전체 | 이번 동작은 평소와 다른 구조였는가 | 샘플 |
| 최근 20건 묶음 | 최근 상태가 평소 구간과 달라졌는가 | 구간 |

이 표를 보면 `한 줄이 있다`와 `샘플 1건이 있다`와 `비교할 최근 구간이 있다`가 각각 다른 질문에 답한다는 점이 드러납니다. Part 3에서 자꾸 헷갈리는 이유는 세 질문이 모두 데이터 표를 보며 시작되기 때문이지, 실제로 같은 층위라서가 아닙니다.

## 한 장면을 세 층위로 다시 보기

자동으로 실행되는 동작 데이터를 다시 보겠습니다.

| event_id | second | flow |
| --- | ---: | ---: |
| A | 0 | 0.8 |
| A | 1 | 1.5 |
| A | 2 | 1.1 |
| B | 0 | 0.7 |
| B | 1 | 1.2 |
| B | 2 | 1.0 |

이 표를 처음 보면 여섯 줄이 보입니다. 하지만 이 여섯 줄은 아직 샘플 여섯 건이 아닐 수 있습니다. 여기서 `A`라는 동작 1회가 샘플이라면, 위 표의 세 줄은 샘플 한 건을 구성하는 시점 기록입니다.

그다음 여러 동작을 묶어 `최근 20건 평균`을 만들면, 이제는 `A`나 `B` 같은 개별 샘플도 다시 한 단계 아래로 내려갑니다. 최근 구간은 샘플 여러 건을 모아 만든 집계 단위이기 때문입니다.

같은 장면을 세 층위로 놓으면 다음처럼 읽을 수 있습니다.

| 층위 | 무엇이 한 건인가 | 예시 |
| --- | --- | --- |
| 행 | 시점 기록 한 줄 | `A, second=1, flow=1.5` |
| 샘플 | 동작 1회 | `event_id=A` 전체 |
| 구간 | 샘플 여러 건 묶음 | 최근 20건의 평균과 변동성 |

즉 `A, second=1`은 샘플이 아니라 샘플을 이루는 한 조각일 수 있고, `최근 20건`은 샘플 20건을 다시 묶은 더 큰 비교 단위일 수 있습니다.

이 장면을 문장으로 다시 풀면 더 또렷합니다.

- 운영자가 `1초 시점의 유량이 얼마였는가`를 묻고 있다면 보고 싶은 것은 행입니다.
- 운영자가 `A 동작 1회가 평소보다 흔들렸는가`를 묻고 있다면 보고 싶은 것은 샘플입니다.
- 운영자가 `최근 20건 전체가 지난주 기준선보다 나빠졌는가`를 묻고 있다면 보고 싶은 것은 구간입니다.

질문이 달라질 때마다 같은 원천데이터가 다른 층위로 다시 읽힌다는 점이 핵심입니다. 헷갈림은 보통 데이터가 복잡해서가 아니라, 지금 내가 어느 질문을 붙이고 있는지 적지 않은 상태에서 표를 보기 시작할 때 생깁니다.

## 왜 이 구분이 필요한가

이 구분이 필요한 이유는 뒤 개념이 각기 다른 층위에 붙기 때문입니다.

| 개념 | 주로 붙는 층위 | 이유 |
| --- | --- | --- |
| 원시 측정값 | 행 | 한 시점의 실제 관측값이기 때문 |
| 특징(feature) | 샘플 | 동작 1회 구조를 설명하는 값이기 때문 |
| 기준선 비교 | 구간 또는 샘플 대 구간 | 최근 상태를 평소와 비교해야 하기 때문 |
| 검토 문장 | 구간 또는 샘플 | 사람이 읽는 판단 단위이기 때문 |

예를 들어 `late_drop_rate` 같은 특징은 시점 한 줄에 바로 붙지 않고, 동작 1회 샘플을 만든 뒤에야 계산할 수 있습니다. 반면 `recent_count=20` 같은 값은 개별 샘플 특징이 아니라 최근 구간 집계에 더 가깝습니다. 그래서 층위를 섞어 읽으면 특징, 기준선, 출력 구조가 모두 추상적으로 느껴집니다.

## 한눈에 비교하는 작은 코드 예시

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.8},
        {"event_id": "A", "second": 1, "flow": 1.5},
        {"event_id": "A", "second": 2, "flow": 1.1},
        {"event_id": "B", "second": 0, "flow": 0.7},
        {"event_id": "B", "second": 1, "flow": 1.2},
        {"event_id": "B", "second": 2, "flow": 1.0},
        {"event_id": "C", "second": 0, "flow": 0.9},
        {"event_id": "C", "second": 1, "flow": 1.6},
        {"event_id": "C", "second": 2, "flow": 1.2},
    ]
)

per_event = (
    raw.groupby("event_id", as_index=False)
    .agg(
        flow_mean=("flow", "mean"),
        flow_max=("flow", "max"),
    )
    .assign(window=lambda df: df["event_id"].map({"A": "recent", "B": "baseline", "C": "recent"}))
)

per_window = (
    per_event.groupby("window", as_index=False)
    .agg(
        event_count=("event_id", "count"),
        flow_mean=("flow_mean", "mean"),
    )
)

print("1) counts change by level")
print("row count:", len(raw))
print("sample count:", len(per_event))
print("window count:", len(per_window))
print()
print("2) one row still means one time-step record")
print(raw.loc[[1], ["event_id", "second", "flow"]])
print()
print("3) one sample means one whole event")
print(per_event.loc[per_event["event_id"] == "A", ["event_id", "flow_mean", "flow_max"]])
print()
print("4) one window means multiple samples regrouped")
print(per_window)
```

예상 출력:

```text
1) counts change by level
row count: 9
sample count: 3
window count: 2

2) one row still means one time-step record
  event_id  second  flow
1        A       1   1.5

3) one sample means one whole event
  event_id  flow_mean  flow_max
0        A   1.133333       1.5

4) one window means multiple samples regrouped
     window  event_count  flow_mean
0  baseline            1   0.966667
1    recent            2   1.183333
```

여기서 봐야 할 것은 숫자 자체보다 `무엇을 세고 있는가`입니다.

- `row count: 9`는 시점 기록 아홉 줄입니다.
- `sample count: 3`는 동작 세 건입니다.
- `window count: 2`는 `recent`, `baseline` 두 구간입니다.

그리고 바로 아래 세 출력은 각 층위의 대표 모양을 눈으로 보여 줍니다.

- `one row example`은 `A, second=1, flow=1.5`처럼 시점 한 줄입니다.
- `one sample example`은 `A` 동작 1회의 평균과 최대값처럼 샘플 한 건입니다.
- `window summary`는 이렇게 만든 샘플 표를 다시 `recent`, `baseline`으로 묶은 구간 집계입니다.

행 수가 줄어드는 것은 단순 압축이 아니라, `무엇을 한 건으로 볼지`가 바뀐 결과입니다.

이 예제를 한 문장으로 요약하면 다음과 같습니다. `A, second=1`은 지금 무슨 일이 있었는지 보여 주고, `event_id=A`는 한 동작이 전체적으로 어땠는지 보여 주며, `recent`는 이렇게 만든 샘플 여러 건을 다시 묶은 상태 비교를 보여 줍니다. 같은 데이터에서도 질문이 바뀌면 바로 이 세 층위 사이를 오가게 됩니다.

## 지금 표를 받을 때 빠르게 묻는 질문

실제로는 아래 세 질문만 먼저 적어도 혼동이 크게 줄어듭니다.

1. 지금 표의 한 줄은 시점 기록인가, 동작 1회인가, 최근 구간 집계인가
2. 내가 지금 읽으려는 대상은 한 줄인가, 한 동작인가, 최근 상태 전체인가
3. 지금 붙이려는 값이 특징인가, 비교 열인가, 검토 문장 후보인가

이 세 질문은 각각 `행`, `샘플`, `구간`을 다시 분리하는 역할을 합니다.

이 절은 용어 구분표가 아니라, `표현 층위(levels of representation)`를 동시에 읽는 문제로 다시 볼 수 있습니다.


따라서 `한 행`, `샘플 1건`, `최근 구간 1개`는 이름이 비슷한 세 객체가 아니라, 서로 다른 질문에 답하기 위해 같은 원천데이터를 다른 층위로 다시 표현한 결과로 읽어야 합니다.

## 출처와 참고 자료

- W3C, `PROV-Overview`. provenance framework가 identifying an object와 representing derivation을 지원해야 한다고 정리하므로, row-level record, event-level sample, window-level aggregate가 서로 다른 표현 층위라는 점을 구분해 남겨야 한다는 일반 근거가 됩니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- U.S. Bureau of Labor Statistics, `Base period`. 기준 시점은 다른 시점과 비교하기 위한 reference라고 설명하므로, 최근 구간과 기준 구간 같은 집계 수준 표현은 sample-level 표현과 다른 비교 층위를 가진다는 점을 보강합니다. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- Google for Developers, `Machine Learning Glossary`의 `labeled example`. example는 sample-level 구조를 전제로 하므로, row-level record와 window-level aggregate를 sample-level example와 섞어 읽지 말아야 한다는 점을 뒷받침합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08

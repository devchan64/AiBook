# P3-4.1 비교 가능한 샘플 한 건은 어떻게 정하는가

> Section ID: `P3-4.1`
> Version: `v2026.07.07`

데이터를 읽을 때 가장 먼저 확인해야 할 것은 값의 크기보다 `한 행이 무엇을 뜻하는가`입니다. 이 질문이 먼저 정리되지 않으면, 뒤에서 특징(feature)을 만들 때도, 라벨(label)을 붙일 때도, 평가(evaluation) 결과를 읽을 때도 기준이 흔들립니다. 결국 이 질문은 `비교 가능한 샘플 한 건을 무엇으로 정할 것인가`라는 질문으로 이어집니다.

한 행과 샘플 1건을 구분해야 하는 이유는 뒤의 특징, 라벨, 비교 기준이 모두 그 단위 위에 올라가기 때문입니다. 눈앞의 표에 행이 보인다고 해서 그것이 곧 비교 가능한 샘플 1건은 아닐 수 있습니다.

예를 들어 자동으로 실행되는 동작에서 제어 파라미터 시계열과 센서 시계열이 남는다고 하겠습니다. 어떤 표에서는 한 행이 `1초 시점의 압력과 유량 측정값`일 수 있습니다. 다른 표에서는 한 행이 `동작 1회 전체의 요약값`일 수 있습니다. 또 다른 표에서는 한 행이 `최근 30분 동안 수행된 여러 동작의 집계 결과`일 수 있습니다. 셋 다 같은 원천데이터에서 나왔지만, 한 행이 뜻하는 대상은 완전히 다릅니다.

| 구분 | 한 행이 뜻하는 것 | 주로 답하는 질문 |
| --- | --- | --- |
| 측정값 표 | 동작 중 한 시점의 센서 또는 제어 값 | 지금 이 시점의 값은 얼마인가 |
| 동작 단위 표 | 자동으로 실행된 동작 1회 전체 | 이번 동작의 전체 구조는 어땠는가 |
| 최근 구간 표 | 여러 동작을 묶은 최근 집계 | 최근 변화가 반복되고 있는가 |
| 기준선 표 | 평소 상태를 대표하는 비교 집계 | 평소와 비교하면 지금은 얼마나 다른가 |

이 표를 보면 같은 데이터라도 어떤 질문에 답하려는지에 따라 `행의 의미`가 달라진다는 점이 보입니다. 측정값 표는 현재 상태를 읽는 데 강하지만, 동작 전체의 구조를 바로 보여 주지는 못합니다. 반대로 동작 단위 표는 한 번의 동작을 비교하는 데 유리하지만, 시점별 순간 변화를 그대로 담지는 않습니다. 최근 구간 표와 기준선 표는 더 나아가 `한 건`이 아니라 `여러 건을 묶은 비교 구조`를 뜻합니다.

여기서 먼저 고정해야 할 문장은 다음과 같습니다. 원시 시계열의 한 행은 측정 시점 하나일 뿐이고, 비교 대상은 그 행들이 모인 동작 1회일 수 있습니다. 따라서 눈앞에 행이 보인다고 해서 그 행이 곧 샘플 1건이라고 가정하면 안 됩니다.

여기서 중요한 점은 데이터 생애주기의 단계도 함께 달라진다는 사실입니다. 측정값 표는 관측과 기록에 가깝고, 동작 단위 표는 비교 가능한 샘플 표현에 가깝고, 최근 구간 표와 기준선 표는 해석과 의사결정 준비에 더 가깝습니다. 따라서 `한 행이 무엇인가`를 묻는 질문은 단지 표 설명이 아니라, 지금 데이터 작업이 어느 단계에 있는지를 묻는 질문이기도 합니다.

이 차이는 다음 순서로 읽으면 표의 역할 구분이 더 분명해집니다.

1. 지금 표의 한 행이 `한 시점`인지 `동작 1회`인지 `여러 동작의 집계`인지 본다.
2. 그 한 행이 어떤 질문에 답하려고 만들어졌는지 본다.
3. 그 질문이 현재 우리가 풀려는 문제와 맞는지 확인한다.

이 순서를 거치면 `행이 있으니 샘플도 이미 있겠지`라는 자동 가정을 조금 늦출 수 있습니다. 여기서 중요한 것은 샘플의 뜻을 한 번 더 길게 정의하는 일이 아니라, 어떤 표가 어떤 질문에 답하려고 만들어졌는지 먼저 구분하는 일입니다. 그래야 원시 로그, 요약 표, 최근 구간 표를 같은 표처럼 섞어 읽지 않게 됩니다.

이제 중요한 질문이 나옵니다. AI 문제를 만들 때 우리는 무엇을 샘플 1건으로 볼 것인가? 눈앞의 표에 행이 있다고 해서 그 행을 그대로 샘플이라고 놓을 수는 없습니다. 한 행이 시점별 측정값이라면, 그것은 아직 우리가 원하는 샘플 단위가 아닐 수 있습니다. 모델이 배워야 할 것이 `동작 전체의 패턴`이라면, 시점별 측정값 여러 행을 묶어 `동작 1회`라는 새로운 샘플을 다시 만들어야 합니다. 즉 샘플을 정한다는 말은 행을 세는 일이 아니라, 어떤 대상을 비교 가능한 한 건으로 묶을지 정하는 일입니다.

여기서 `비교 가능한 샘플`이라고 부르려면 최소한 세 가지를 함께 만족해야 합니다.

1. 한 건의 경계가 분명해야 한다.
2. 같은 종류의 특징을 모든 건에 같은 방식으로 붙일 수 있어야 한다.
3. 나중에 붙일 라벨이나 비교 기준이 그 단위에 자연스럽게 연결되어야 한다.

이 세 가지를 기준으로 보면, 시점별 측정 행은 보통 1번은 만족하지만 2번과 3번이 약합니다. 반면 동작 1회 요약 표는 세 가지를 모두 만족하기 쉽습니다. 최근 구간 표는 3번의 비교 기준에는 강하지만, 개별 샘플 비교보다는 여러 샘플을 다시 묶은 해석 구조에 더 가깝습니다.

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

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "elapsed_seconds": 0, "pressure": 1.0, "flow": 0.0, "is_recent": 1, "review_needed": 1},
        {"event_id": "A", "elapsed_seconds": 1, "pressure": 2.0, "flow": 1.4, "is_recent": 1, "review_needed": 1},
        {"event_id": "A", "elapsed_seconds": 2, "pressure": 2.4, "flow": 1.6, "is_recent": 1, "review_needed": 1},
        {"event_id": "B", "elapsed_seconds": 0, "pressure": 1.1, "flow": 0.0, "is_recent": 0, "review_needed": 0},
        {"event_id": "B", "elapsed_seconds": 1, "pressure": 1.7, "flow": 1.1, "is_recent": 0, "review_needed": 0},
        {"event_id": "B", "elapsed_seconds": 2, "pressure": 2.0, "flow": 1.2, "is_recent": 0, "review_needed": 0},
        {"event_id": "C", "elapsed_seconds": 0, "pressure": 1.2, "flow": 0.1, "is_recent": 1, "review_needed": 1},
        {"event_id": "C", "elapsed_seconds": 1, "pressure": 2.3, "flow": 1.5, "is_recent": 1, "review_needed": 1},
        {"event_id": "C", "elapsed_seconds": 2, "pressure": 2.7, "flow": 1.8, "is_recent": 1, "review_needed": 1},
    ]
)

event_summary = (
    raw.groupby("event_id", as_index=False)
    .agg(
        total_duration_seconds=("elapsed_seconds", "max"),
        pressure_mean=("pressure", "mean"),
        pressure_rise=("pressure", lambda s: s.iloc[-1] - s.iloc[0]),
        flow_mean=("flow", "mean"),
        is_recent=("is_recent", "max"),
        review_needed=("review_needed", "max"),
    )
)

window_summary = (
    event_summary.groupby("is_recent", as_index=False)
    .agg(
        event_count=("event_id", "count"),
        pressure_mean=("pressure_mean", "mean"),
        flow_mean=("flow_mean", "mean"),
    )
    .assign(window_name=lambda df: df["is_recent"].map({0: "baseline", 1: "recent"}))
    [["window_name", "event_count", "pressure_mean", "flow_mean"]]
)

unit_check = pd.DataFrame(
    [
        {
            "unit_name": "measurement_row",
            "sample_count": len(raw),
            "can_use_pressure_rise": "no",
            "label_attaches_naturally": "weak",
        },
        {
            "unit_name": "event",
            "sample_count": len(event_summary),
            "can_use_pressure_rise": "yes",
            "label_attaches_naturally": "yes",
        },
        {
            "unit_name": "window",
            "sample_count": len(window_summary),
            "can_use_pressure_rise": "partial",
            "label_attaches_naturally": "weak",
        },
    ]
)

print("1) count rows under each candidate unit")
print("measurement rows:", len(raw))
print("event samples:", len(event_summary))
print("window aggregates:", len(window_summary))
print()
print("2) raw rows still mean per-time-step records")
print(raw.groupby("event_id").size().reset_index(name="measurement_rows"))
print()
print("3) event-level summaries can hold comparison features and labels")
print(
    event_summary[
        [
            "event_id",
            "total_duration_seconds",
            "pressure_mean",
            "pressure_rise",
            "flow_mean",
            "review_needed",
        ]
    ]
)
print()
print("4) window-level aggregates are for broader comparison, not single-sample judgment")
print(window_summary)
print()
print("5) unit check for comparable-sample suitability")
print(unit_check)
```

예상 출력:

```text
1) count rows under each candidate unit
measurement rows: 9
event samples: 3
window aggregates: 2

2) raw rows still mean per-time-step records
  event_id  measurement_rows
0        A                 3
1        B                 3
2        C                 3

3) event-level summaries can hold comparison features and labels
  event_id  total_duration_seconds  pressure_mean  pressure_rise  flow_mean  review_needed
0        A                       2       1.800000            1.4   1.000000              1
1        B                       2       1.600000            0.9   0.766667              0
2        C                       2       2.066667            1.5   1.133333              1

4) window-level aggregates are for broader comparison, not single-sample judgment
  window_name  event_count  pressure_mean  flow_mean
0    baseline            1       1.600000   0.766667
1      recent            2       1.933333   1.066667

5) unit check for comparable-sample suitability
         unit_name  sample_count can_use_pressure_rise label_attaches_naturally
0  measurement_row             9                    no                      weak
1            event             3                   yes                       yes
2           window             2               partial                      weak
```

출력에서 먼저 봐야 할 것은 `몇 건으로 세고 있는가`입니다. 원시 표에서는 측정 시점이 9건이고, `event_id` 기준으로 묶으면 동작 1회 샘플이 3건이며, 다시 최근/기준선 구간으로 묶으면 비교용 집계는 2건이 됩니다. 그런데 그다음에 봐야 할 것은 `어떤 값이 어느 단위에서만 의미가 생기는가`입니다. `pressure_rise`처럼 시작점과 끝점의 차이를 보는 열은 시점 한 줄에서는 만들 수 없고, 동작 1회로 묶였을 때 비로소 뜻이 생깁니다. 반대로 `window_summary`는 개별 동작 비교용 표가 아니라 여러 동작을 묶은 비교 해석용 표입니다. 즉 같은 원천데이터라도 `한 시점`, `동작 1회`, `최근 구간` 중 무엇을 샘플 1건으로 읽느냐에 따라 행 수와 표의 의미, 그리고 그 위에 놓을 수 있는 열의 역할이 함께 바뀝니다.

여기서 `unit check` 출력은 이 절의 판단을 더 직접적으로 보여 줍니다. `measurement_row`는 샘플 수는 가장 많지만 `pressure_rise`를 바로 올릴 수 없고, `review_needed` 같은 결과도 자연스럽게 붙기 어렵습니다. `window`는 최근 상태 해석에는 쓸 수 있지만 개별 동작 비교 샘플로는 약합니다. 반면 `event`는 샘플 수, 요약 특징, 결과 열이 한 단위 위에 함께 놓여 있어 이 절의 질문인 `비교 가능한 샘플 한 건`에 가장 잘 맞습니다.

이 예제는 샘플 단위를 세는 법만 보여 주는 것이 아닙니다.

| 여기서 보이는 값 | 어느 단위에서 자연스러운가 | 이유 |
| --- | --- | --- |
| `pressure`, `flow` 한 시점 값 | 측정 시점 | 그 순간의 관측값이기 때문 |
| `pressure_mean`, `pressure_rise` | 동작 1회 | 여러 시점을 묶어야만 계산되는 요약값이기 때문 |
| `event_count`, 최근 평균 | 최근 구간 또는 기준선 구간 | 여러 동작을 다시 묶은 비교 집계이기 때문 |

이렇게 보면 `샘플 1건을 정한다`는 말은 단지 행 개수를 줄이는 일이 아니라, 어떤 열이 현재 단위에서 자연스럽게 읽히는지까지 함께 정하는 일입니다.

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

처음 표를 받았을 때 아래처럼 아주 짧게 판별해 볼 수도 있습니다.

| 지금 보는 표가 이렇다면 | 먼저 의심할 행 의미 |
| --- | --- |
| 시간 열이 있고 같은 `event_id`가 여러 번 반복된다 | 한 시점 기록일 가능성이 크다 |
| `event_id`마다 한 줄만 있고 평균, 최대, 기울기 같은 요약 열이 있다 | 동작 1회 샘플일 가능성이 크다 |
| 최근 20건 평균, 이전 200건 평균 같은 비교 열이 있다 | 여러 동작을 묶은 구간 집계일 가능성이 크다 |

이 판별표의 목적은 표 이름을 외우는 데 있지 않습니다. 지금 손에 있는 행이 `즉시 비교할 샘플`인지, 아니면 아직 `샘플로 다시 묶어야 할 기록`인지를 빠르게 가르는 데 있습니다.

여기서 한 걸음 더 나가면 뒤 장과의 연결도 보입니다. 동작 단위 요약 표가 생겨야 평균, 기울기, 변동성 같은 특징을 안정적으로 만들 수 있고, 그 다음에야 최근 구간과 기준선 비교도 같은 단위 위에서 읽을 수 있습니다. 즉 `한 행이 무엇인가`라는 질문은 샘플 단위 하나를 정하는 데서 끝나지 않고, Part 3 전체의 나머지 장을 지탱하는 바닥 규칙이 됩니다.

이 절을 읽고 실제로 남겨야 할 가장 짧은 판단은 다음 한 줄입니다. `비교 가능한 샘플은 데이터가 먼저 정해 주는 것이 아니라, 질문이 요구하는 비교 단위와 그 위에 올릴 특징·라벨 구조가 함께 정한다.` 이 기준이 잡혀야 다음 절에서 샘플 단위가 흔들릴 때 왜 후속 구조 전체가 같이 흔들리는지도 자연스럽게 이어집니다.

## 짧은 점검

- 같은 `event_id`가 여러 줄 반복되는 표를 왜 곧바로 샘플 표라고 부르면 안 되는가
- 요약 열이 있는 표가 왜 동작 1회 샘플 표에 더 가까운가
- 최근 구간 비교 열이 보이면 왜 `한 건의 동작`보다 더 큰 집계 단위를 의심해야 하는가
- `행 수가 줄었다`는 사실이 왜 샘플 단위 재설계의 힌트가 되는가

한 행이 보인다고 해서 그것이 곧 샘플 1건은 아니다. 먼저 눈앞의 표가 시점별 측정표인지, 동작 단위 표인지, 최근 구간 집계표인지 구분해야 합니다. 그 다음에야 특징(feature), 라벨(label), 기준선(baseline), 평가(evaluation)가 무엇을 뜻하는지 안정적으로 읽을 수 있습니다. 다음 절에서는 샘플 단위가 흔들릴 때 왜 후속 구조 전체가 함께 흔들리는지 바로 이어서 봅니다.

다음 절에서는 이 구분이 흔들릴 때 특징과 라벨, 평가 단위가 왜 함께 흔들리는지 더 직접적으로 다룹니다.

## 언제 이 관점을 먼저 떠올려야 하는가

- 눈앞의 한 행이 곧바로 샘플 1건이라고 가정하기 쉬운 순간에 `한 행이 무엇을 뜻하는가`를 먼저 묻는 관점을 떠올립니다.
- 시점 기록, 동작 1회 요약, 최근 구간 집계 중 지금 표가 어느 층위인지 구분해야 할 때 이 절로 돌아옵니다.
- 뒤에서 특징, 라벨, 기준선, 평가를 읽기 전에 샘플 단위부터 다시 고정해야 할 때 이 절이 기준이 됩니다.

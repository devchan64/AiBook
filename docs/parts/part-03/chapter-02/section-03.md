# P3-2.3 새 표를 처음 받으면 무엇부터 적어야 하는가

> Section ID: `P3-2.3`
> Version: `v2026.07.19`

새 표를 처음 받으면 많은 경우 바로 평균, 분포, 모델 후보부터 떠올리기 쉽습니다. 하지만 그보다 먼저 적어야 하는 것은 `이 표의 한 행은 무엇인가`, `무엇을 묶을 수 있는가`, `무엇이 아직 빠져 있는가`입니다. 이 세 가지가 정리되어야 지금 손에 있는 것이 바로 비교할 샘플 표인지, 아니면 다시 묶어야 할 원시 기록인지 구분할 수 있습니다. 새 표를 보자마자 `학습용 데이터셋인가`를 먼저 결정하기보다, 이 세 가지를 메모해 두는 편이 해석에 도움이 됩니다. 이렇게 적어 두면 뒤의 샘플 설계와 데이터셋 재설계도 훨씬 덜 추상적으로 바뀝니다.

여기서 먼저 붙잡아야 하는 관점은 `데이터 형식 정합성(format consistency)`과 `데이터 품질의 첫 점검(first quality check)`입니다. 형식 정합성은 같은 대상을 가리키는 키가 같은 형식으로 적혀 있는지, 시간 열이 실제 순서를 읽을 수 있는 형태인지, 같은 의미의 값이 열마다 다른 단위나 문자열 규칙으로 섞여 있지 않은지를 먼저 보는 일입니다. 첫 품질 점검은 그다음 단계로, 빠진 값, 끊긴 순서, 중복 행, 묶이지 않는 고아 행처럼 비교 구조를 바로 무너뜨리는 문제가 있는지를 초기에 확인하는 일입니다.

새 표를 처음 읽을 때는 `한 행은 무엇인가`, `무엇을 묶을 수 있는가`, `무엇이 아직 빠져 있는가`를 먼저 적어 두는 편이 안전합니다. `한 행은 무엇인가`라는 질문은 통계와 데이터 정리에서 말하는 `observation` 단위 확인과 이어지고, `무엇을 묶을 수 있는가`는 시간 데이터에서 `key`와 `index`를 먼저 드러내야 한다는 원리와 이어집니다. `원시 근거`를 남겨 두는 항목도 data provenance와 traceability를 확보해야 나중에 품질과 신뢰성을 다시 판단할 수 있다는 원리와 연결됩니다.

같은 다섯 줄 메모를 형식과 품질 관점으로 다시 읽으면 다음처럼 정리할 수 있습니다.

| 점검 관점 | 먼저 확인하는 것 | 초기에 잡아야 하는 이유 |
| --- | --- | --- |
| 형식 정합성 | 키 형식이 일정한가, 시간 열이 정렬 가능한가, 단위와 표기 규칙이 섞이지 않았는가 | 같은 대상을 다른 것으로 읽거나 시간 순서를 잘못 읽으면 뒤의 모든 비교가 흔들리기 때문 |
| 첫 품질 점검 | 결측, 중복, 끊긴 순서, 묶이지 않는 행이 있는가 | 샘플 재구성 전에 이미 비교 불가 사례를 따로 표시해야 하기 때문 |

## 가장 먼저 적는 다섯 가지

새 표를 처음 읽을 때는 아래 다섯 가지 질문을 먼저 적어 두는 편이 안전합니다. 이는 `행 단위`, `묶음 기준`, `시간 구조`, `비교 가능성`, `원시 근거`를 빠뜨리지 않게 해 주는 최소 확인 항목입니다.

1. 한 행은 무엇을 뜻하는가
2. 같은 대상을 묶어 주는 식별자는 무엇인가
3. 시간 순서나 진행 순서를 나타내는 열이 있는가
4. 지금 바로 비교 가능한 단위인가, 다시 묶어야 하는가
5. 이상해 보이면 다시 돌아갈 원시 근거는 무엇인가

이 다섯 가지를 표로 줄이면 다음과 같습니다.

| 먼저 적을 항목 | 왜 필요한가 |
| --- | --- |
| 행 의미 | 시점 기록인지, 동작 1회인지, 최근 구간 집계인지 구분해야 하기 때문 |
| 식별자 | 여러 줄이 같은 샘플에 속하는지 묶어 볼 수 있어야 하기 때문 |
| 시간/순서 열 | 시계열 구조인지, 정적 표인지 판단해야 하기 때문 |
| 비교 가능성 | 지금 바로 샘플 비교가 가능한지, 요약 표가 먼저 필요한지 결정해야 하기 때문 |
| 원시 근거 위치 | 나중에 이상 사례를 다시 추적할 수 있어야 하기 때문 |

이 다섯 항목만 먼저 적어도 저장 구조와 문제 표현 구조를 훨씬 덜 섞어 읽게 됩니다.

다섯 항목을 읽는 순서도 중요합니다. `행 의미`, `식별자`, `시간/순서 열`은 형식 정합성을 먼저 확인하는 축이고, `비교 가능성`, `원시 근거 위치`는 첫 품질 점검으로 넘어가는 축입니다. 이렇게 적어 두면 막연히 `품질이 나빠 보인다`고 말하는 대신, `형식이 먼저 안 맞는지`, `형식은 맞지만 비교를 무너뜨리는 품질 문제가 있는지`를 차례로 가를 수 있습니다.

## 잘못된 시작과 더 나은 시작

| 표를 보자마자 하기 쉬운 일 | 왜 너무 빠른가 | 더 나은 첫 행동 |
| --- | --- | --- |
| 평균, 최대값부터 계산해 본다 | 아직 한 행과 샘플 단위가 다를 수 있다 | 행 의미와 식별자부터 적는다 |
| 분류/회귀 문제를 떠올린다 | 라벨이 붙는 단위가 아직 안 보일 수 있다 | 비교 가능한 단위인지 먼저 본다 |
| 시계열 딥러닝을 생각한다 | 시간 열이 있어도 샘플 경계는 아직 안 정해졌을 수 있다 | 시간/순서 열과 묶음 기준을 먼저 본다 |
| 이상한 값 한 줄에 바로 의미를 붙인다 | 그 한 줄이 샘플 전체를 대표하지 않을 수 있다 | 원시 근거와 요약 후보 구조를 함께 적는다 |

즉 첫 단계는 `계산`보다 `정체 확인`에 가깝습니다.

## 작은 도식으로 보기

새 표를 처음 읽을 때는 아래처럼 `행 의미 확인 -> 묶음 기준 확인 -> 형식/품질 점검 -> 재묶음 여부 판단` 순서로 닫아 보는 편이 안전합니다.

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-3-mermaid-01-ko.mmd"
```

## 아주 짧은 표 읽기 메모

아래처럼 다섯 줄로 먼저 적어 두면, 표의 정체와 비교 가능성을 빠르게 가를 수 있습니다.

- 한 행은 `_____`를 뜻한다.
- 같은 대상을 묶는 키는 `_____`다.
- 시간/진행 순서를 나타내는 열은 `_____`다.
- 지금 표는 바로 비교 가능하다 / 아직 다시 묶어야 한다.
- 이상 사례를 다시 확인할 원시 근거는 `_____`다.

예를 들어 자동 동작 로그라면 이렇게 적을 수 있습니다.

- 한 행은 `동작 중 한 시점의 측정값`을 뜻한다.
- 같은 대상을 묶는 키는 `event_id`다.
- 시간 열은 `elapsed_seconds`다.
- 지금 표는 바로 비교 가능한 샘플 표가 아니라 다시 묶어야 한다.
- 이상 사례를 다시 확인할 원시 근거는 `event_id`별 원시 로그다.

이 다섯 줄 메모가 있으면 Chapter 3에서 `질문에 맞는 데이터셋을 다시 설계한다`는 말도 훨씬 덜 추상적으로 읽힙니다.

여기서 한 걸음만 더 나가면 형식 정합성과 첫 품질 점검을 따로 적을 수 있습니다.

- 형식 정합성: `event_id`가 같은 동작을 같은 형식으로 묶어 주고, `elapsed_seconds`가 시간 순서를 읽게 해 주는지 먼저 본다.
- 첫 품질 점검: 어떤 `event_id`는 행이 비정상적으로 적거나 많지 않은지, 시간이 거꾸로 가거나 빠진 구간은 없는지, 비교 전에 따로 표시해야 할 결측이 없는지 본다.

## 작은 코드 예시

문제 상황: 새 로그 표를 받았을 때, 이 표를 바로 샘플 비교 표로 읽어도 되는지 확인합니다.

입력(input): `event_id`별 여러 시점 기록이 섞여 있는 원시 로그 표와 비교 가능한 사건으로 볼 최소 행 수 `minimum_rows_per_event`

기대 출력(output): 같은 표라도 `행 의미`, `묶음 기준`, `시간/순서 열`을 먼저 확인해야 아직 바로 비교할 수 없는 표라는 점이 드러납니다. `minimum_rows_per_event`를 바꾸면 어떤 사건이 충분한 기록을 가진 후보인지도 달라집니다.

확인할 개념: 표를 처음 읽을 때는 계산보다 먼저 `이 행이 샘플 1건인가, 아니면 샘플의 일부 기록인가`를 확인해야 한다. 반복 행 수 기준을 함께 두면 구조 점검이 단순 출력이 아니라 비교 가능성 판단으로 이어진다.

```python
import pandas as pd

minimum_rows_per_event = 3

table = pd.DataFrame(
    [
        {"event_id": "A", "elapsed_seconds": 0, "flow": 0.8, "pressure": 1.0},
        {"event_id": "A", "elapsed_seconds": 1, "flow": 1.5, "pressure": 2.0},
        {"event_id": "A", "elapsed_seconds": 2, "flow": 0.9, "pressure": 1.4},
        {"event_id": "B", "elapsed_seconds": 0, "flow": 0.7, "pressure": 1.1},
        {"event_id": "B", "elapsed_seconds": 1, "flow": 0.8, "pressure": 1.2},
    ]
)

print("1) raw table")
print(table)
print()

row_check = pd.DataFrame(
    [
        {"check_item": "row_count", "value": len(table)},
        {"check_item": "event_id_count", "value": table["event_id"].nunique()},
        {"check_item": "has_time_order", "value": "yes"},
    ]
)
print("2) quick structural check")
print(row_check)
print()

rows_per_event = table.groupby("event_id", as_index=False).size().rename(columns={"size": "row_count"})
rows_per_event["enough_rows_for_event_sample"] = (
    rows_per_event["row_count"] >= minimum_rows_per_event
)
print("3) repeated rows per event")
print(rows_per_event)
print()

wrong_reading = table[["event_id", "elapsed_seconds", "flow"]]
print("4) if we compare rows as if each row were a sample")
print(wrong_reading)
print()

event_summary = (
    table.groupby("event_id", as_index=False)
    .agg(
        duration_seconds=("elapsed_seconds", "max"),
        mean_flow=("flow", "mean"),
        peak_pressure=("pressure", "max"),
    )
)
event_summary = event_summary.merge(rows_per_event, on="event_id")
print("5) after regrouping into one row per event")
print(event_summary)
```

예상 출력:

```text
1) raw table
  event_id  elapsed_seconds  flow  pressure
0        A                0   0.8       1.0
1        A                1   1.5       2.0
2        A                2   0.9       1.4
3        B                0   0.7       1.1
4        B                1   0.8       1.2

2) quick structural check
      check_item  value
0      row_count      5
1  event_id_count      2
2  has_time_order    yes

3) repeated rows per event
  event_id  row_count  enough_rows_for_event_sample
0        A          3                          True
1        B          2                         False

4) if we compare rows as if each row were a sample
  event_id  elapsed_seconds  flow
0        A                0   0.8
1        A                1   1.5
2        A                2   0.9
3        B                0   0.7
4        B                1   0.8

5) after regrouping into one row per event
  event_id  duration_seconds  mean_flow  peak_pressure  row_count  enough_rows_for_event_sample
0        A                 2   1.066667            2.0          3                          True
1        B                 1   0.750000            1.2          2                         False
```

이 예시가 보여 주는 핵심은 단순히 `event_id`와 `elapsed_seconds`라는 열 이름을 찾는 일이 아닙니다. 2단계와 3단계에서 먼저 보이는 것은 `행 수 5`보다 `event_id 수 2`가 작고, 같은 `event_id`가 여러 줄 반복된다는 사실입니다. 여기서 조작할 값은 `minimum_rows_per_event`입니다. 값을 `3`으로 두면 A는 충분한 기록을 가진 후보가 되지만 B는 부족한 후보로 남습니다. 값을 `2`로 낮추면 B도 후보가 되지만, 더 짧은 기록에서 만든 평균을 같은 무게로 비교해도 되는지는 다시 검토해야 합니다. 이 신호를 읽어야만 `현재 한 행은 샘플 1건이 아니라 샘플의 일부 기록`이라는 해석에 도달할 수 있습니다. 그래서 4단계처럼 각 행을 바로 비교하면 아직 `A 동작 전체`와 `B 동작 전체`를 비교하는 표가 되지 못합니다. 반대로 5단계처럼 `event_id`로 다시 묶어야 비로소 동작 1회가 한 행이 되고, 그 위에서 평균 흐름이나 최대 압력 같은 비교 가능한 열을 만들 수 있습니다.

같은 결과를 형식과 품질 관점으로 다시 읽으면 더 분명해집니다. `event_id`가 반복된다는 사실은 형식 정합성 차원에서 `한 샘플을 묶을 키가 있다`는 뜻이고, `rows per event`가 서로 다르다는 사실은 첫 품질 점검 차원에서 `샘플마다 기록 길이가 다르다`는 신호입니다. 이 차이를 초기에 적어 두어야 나중에 평균을 비교할 때도 `왜 어떤 샘플은 더 적은 근거 위에 서 있는가`를 함께 읽을 수 있습니다.

형식 정합성과 첫 품질 점검을 먼저 적는 이유는, 새 표를 받자마자 평균이나 모델 이름부터 붙이지 않고 `지금 손에 든 행이 무엇이며, 무엇이 아직 비교를 막고 있는가`를 먼저 보게 하기 위해서입니다. 키 형식, 시간 순서, 반복 길이, 결측과 고아 행이 초기에 정리되어 있어야만 그다음에 샘플을 다시 묶고 비교 가능한 열을 만들 때도 같은 표를 흔들리지 않는 기준으로 읽을 수 있습니다.

## 출처와 참고 자료

- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. 변수, 관측치, 표 구조를 구분해 설명하므로, `한 행은 무엇인가`를 먼저 적어 두어야 한다는 이 절의 출발점을 뒷받침합니다. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- E. Wang, D. L. Cook, R. J. Hyndman, and R. Wickham, `A Grammar of Spatiotemporal Data Transformation`, *Journal of Computational and Graphical Statistics* 27(2), 2018. key와 index를 분리해 시간 데이터를 읽는 원리를 제공하므로, `무엇을 묶을 수 있는가`, `시간/순서 열이 있는가`를 먼저 점검해야 한다는 판단을 보강합니다. [https://doi.org/10.1080/10618600.2017.1371377](https://doi.org/10.1080/10618600.2017.1371377){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08
- W3C, `PROV-Overview`. provenance와 traceability를 함께 다루므로, 이상 사례가 보일 때 다시 돌아갈 원시 근거를 초기에 적어 두어야 한다는 이 절의 마지막 점검 항목을 지지합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-08

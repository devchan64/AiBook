# P3-2.3 새 표를 처음 받으면 무엇부터 적어야 하는가

> Section ID: `P3-2.3`
> Version: `v2026.09.19`

새 표를 처음 받으면 많은 경우 바로 평균, 분포, 모델 후보부터 떠올리기 쉽습니다. 하지만 그보다 먼저 적어야 하는 것은 `이 표의 한 행은 무엇인가`, `무엇을 묶을 수 있는가`, `무엇이 아직 빠져 있는가`입니다. 이 세 가지가 정리되어야 지금 손에 있는 것이 바로 비교할 샘플 표인지, 아니면 다시 묶어야 할 원시 기록인지 구분할 수 있습니다. 새 표를 보자마자 `학습용 데이터셋인가`를 먼저 결정하기보다, 이 세 가지를 메모해 두는 편이 해석에 도움이 됩니다. 이렇게 적어 두면 뒤의 샘플 설계와 데이터셋 재설계도 훨씬 덜 추상적으로 바뀝니다.

여기서 먼저 붙잡아야 하는 관점은 [데이터 형식 정합성(format consistency)](../../../reference/concept-glossary-parts/03-digeut.md#data-modeling)과 [데이터 품질의 첫 점검(data quality check)](../../../reference/concept-glossary-parts/03-digeut.md#data-modeling)입니다. 형식 정합성은 같은 대상을 가리키는 키가 같은 형식으로 적혀 있는지, 시간 열이 실제 순서를 읽을 수 있는 형태인지, 같은 의미의 값이 열마다 다른 단위나 문자열 규칙으로 섞여 있지 않은지를 먼저 보는 일입니다. 첫 품질 점검은 그다음 단계로, 빠진 값, 끊긴 순서, 중복 행, 묶이지 않는 고아 행처럼 비교 구조를 바로 무너뜨리는 문제가 있는지를 초기에 확인하는 일입니다.

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
| [비교 가능성(comparability)](../../../reference/concept-glossary-parts/13-pieup.md#glossary-comparability) | 지금 바로 샘플 비교가 가능한지, 요약 표가 먼저 필요한지 결정해야 하기 때문 |
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

## 행 의미에서 비교 가능성까지 점검하기 {#_3}

새 표를 처음 읽을 때는 아래처럼 `행 의미 확인 -> 묶음 기준 확인 -> 형식/품질 점검 -> 재구성 또는 원문 확인 판단` 순서로 닫아 보는 편이 안전합니다.

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-3-mermaid-01-ko.mmd"
```

## 아주 짧은 표 읽기 메모

아래처럼 다섯 줄로 먼저 적어 두면, 표의 정체와 비교 가능성을 빠르게 가를 수 있습니다.

- 한 행은 `_____`를 뜻한다.
- 같은 대상을 묶는 키는 `_____`다.
- 시간/진행 순서를 나타내는 열은 `_____`다.
- 비교하려는 질문은 `_____`이며, 필요한 재구성과 아직 확인하지 못한 조건은 `_____`다.
- 이상 사례를 다시 확인할 원시 근거는 `_____`다.

예를 들어 아래 CSV로 동작별 평균 유량을 비교하려 한다면 이렇게 적을 수 있습니다.

- 한 행은 `동작 중 한 시점의 측정값`을 뜻한다.
- 같은 대상을 묶는 키는 `event_id`다.
- 시간 열은 `elapsed_seconds`다.
- 동작별 평균을 비교하려면 `event_id`로 묶어야 하며, 동작 전체 관측 여부와 운전 조건 일치는 아직 확인하지 못했다.
- 이상 사례를 다시 확인할 원시 근거는 `event_id`별 원시 로그다.

이 다섯 줄 메모가 있으면 Chapter 3에서 `질문에 맞는 데이터셋을 다시 설계한다`는 말도 훨씬 덜 추상적으로 읽힙니다.

여기서 한 걸음만 더 나가면 형식 정합성과 첫 품질 점검을 따로 적을 수 있습니다.

- 형식 정합성: `event_id`가 같은 동작을 같은 형식으로 묶어 주고, `elapsed_seconds`가 시간 순서를 읽게 해 주는지 먼저 본다.
- 첫 품질 점검: 어떤 `event_id`는 행이 비정상적으로 적거나 많지 않은지, 시간이 거꾸로 가거나 빠진 구간은 없는지, 비교 전에 따로 표시해야 할 결측이 없는지 본다.

## 순서 오류와 원문 확인이 필요한 오류

아래는 뒤의 CSV에서 A의 처음 세 기록을 복사해 바꾼 대조입니다. 원래 `(시간, 유량)`은 `(0, 0.80), (1, 0.92), (2, 1.05)`이며, 시간은 초, 유량은 L/min입니다. 이 작은 구간은 1초 간격으로 측정된다고 가정합니다. 원본 CSV는 바꾸지 않습니다.

| 복사본에서 바꾼 것 | 무엇이 달라졌는가 | 다음 행동 |
| --- | --- | --- |
| 없음: 0→1→2초 | 순서와 간격이 이 구간의 가정에 맞음 | 다른 품질 항목도 계속 점검 |
| 행 순서만 2→1→0초로 뒤집음 | 시각·측정값은 같고 저장 순서만 다름 | 시각 의미가 맞음을 확인한 뒤 복사본 정렬 |
| 1초 기록을 그대로 한 번 더 붙임 | 같은 사건·시각·측정값이 반복됨 | 중복 수집인지 원문 확인 후 처리 규칙 결정 |
| 1초 유량을 9.00으로 바꾼 행을 추가 | 같은 사건·시각에 0.92와 9.00이 충돌함 | 해당 사건의 요약을 보류하고 원문 확인 |
| 1초 기록을 제거: 0→2초 | 순서는 증가하지만 예상 간격에 빈 구간이 생김 | 누락인지 원문 확인, 임의로 0을 채우지 않음 |

`event_id`의 반복은 한 사건의 여러 시점 기록을 묶는 데 필요합니다. 여기서 중복을 의심하는 기준은 `(event_id, elapsed_seconds)`의 반복입니다. 실제 로그가 여러 센서를 함께 담는다면 센서 식별자까지 필요한지 먼저 확인해야 합니다. 정렬은 순서만 바꾸므로 충돌값을 고르거나 빠진 측정값을 복원하지 않습니다.

원시 근거 메모에는 파일 경로·버전 또는 수집 시각, 원본 행 번호와 사건 식별자를 남깁니다. 파생 표에는 어떤 행을 정렬·제외·보류했는지와 이유를 기록합니다. 예를 들어 A의 1초 값이 충돌하면 원본 CSV의 데이터 행 2(헤더 포함 파일 줄 3)와 추가한 충돌 행을 함께 확인합니다. 원본을 덮어쓰지 않아야 처리 전후를 다시 비교할 수 있습니다.

## 행 수·시간 순서·중복을 나누어 점검하기 {#_5}

문제 상황: 새 로그 표를 받았을 때, 이 표를 바로 샘플 비교 표로 읽어도 되는지 확인합니다.

입력(input): [p3_2_3_first_table_log.csv](../../../assets/part-03/chapter-02/p3_2_3_first_table_log.csv)에 저장된 원시 로그 표와 관측점 수 조건으로 사용할 최소 행 수 `minimum_rows_per_event`

기대 출력(output): 사건별 행 수 조건의 통과 여부를 확인하고, 같은 세 기록의 순서·중복·값·누락을 바꾸었을 때 정렬할지 원문을 확인할지 구분합니다.

확인할 개념: 한 행과 한 사건은 다를 수 있다. 행 수 조건 통과는 전체 동작의 완전성이나 비교 가능성을 인증하지 않으며, 시간 순서가 맞아도 중복·누락·조건 차이를 별도로 확인해야 한다.

```python
# 행 수 조건과 시간 순서를 확인하고, 복사본의 중복·충돌·누락에 따른 다음 행동을 비교합니다.
import csv
from collections import defaultdict
from pathlib import Path

minimum_rows_per_event = 12
preview_row_count = 8

input_path = Path("docs/assets/part-03/chapter-02/p3_2_3_first_table_log.csv")

with input_path.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

for row in rows:
    row["elapsed_seconds"] = int(row["elapsed_seconds"])
    row["flow"] = float(row["flow"])
    row["pressure"] = float(row["pressure"])

events = defaultdict(list)
for row in rows:
    events[row["event_id"]].append(row)

print("1) quick structural check")
print(f"row_count: {len(rows)}")
print(f"event_id_count: {len(events)}")
has_time_order = all(
    all(a["elapsed_seconds"] < b["elapsed_seconds"]
        for a, b in zip(event_rows, event_rows[1:]))
    for event_rows in events.values()
)
print(f"has_time_order: {'yes' if has_time_order else 'no'}")
print()

print("2) repeated rows per event")
for event_id, event_rows in sorted(events.items()):
    enough_rows = len(event_rows) >= minimum_rows_per_event
    print(f"{event_id}: row_count={len(event_rows)}, enough_rows={enough_rows}")
print()

print("3) if we compare rows as if each row were a sample")
for row in rows[:preview_row_count]:
    print(
        f"{row['event_id']} at {row['elapsed_seconds']}s: "
        f"flow={row['flow']:.1f}"
    )
print(f"... {len(rows) - preview_row_count} more time-point rows")
print()

print("4) after regrouping into one row per event")
for event_id, event_rows in sorted(events.items()):
    times = [row["elapsed_seconds"] for row in event_rows]
    observed_span = max(times) - min(times)
    mean_flow = sum(row["flow"] for row in event_rows) / len(event_rows)
    peak_pressure = max(row["pressure"] for row in event_rows)
    enough_rows = len(event_rows) >= minimum_rows_per_event
    print(
        f"{event_id}: observed_span={observed_span}s, mean_flow={mean_flow:.2f}, "
        f"peak_pressure={peak_pressure:.1f}, enough_rows={enough_rows}"
    )

print()
print("5) controlled changes to A's first three records")
base_records = [dict(row) for row in events["A"][:3]]
cases = {
    "original": base_records,
    "reversed": list(reversed(base_records)),
    "duplicate": base_records + [dict(base_records[1])],
    "conflict": base_records + [dict(base_records[1], flow=9.0)],
    "missing": [base_records[0], base_records[2]],
}
for name, records in cases.items():
    times = [row["elapsed_seconds"] for row in records]
    ordered = all(a < b for a, b in zip(times, times[1:]))
    same_time = defaultdict(set)
    for row in records:
        same_time[row["elapsed_seconds"]].add((row["flow"], row["pressure"]))
    duplicate_time = len(times) != len(same_time)
    conflicting_values = any(len(values) > 1 for values in same_time.values())
    unique_times = sorted(same_time)
    gap = any(b - a != 1 for a, b in zip(unique_times, unique_times[1:]))
    if conflicting_values or duplicate_time or gap:
        next_action = "check_source"
    elif not ordered:
        next_action = "sort_copy"
    else:
        next_action = "continue_checks"
    print(
        f"{name}: ordered={ordered}, duplicate_time={duplicate_time}, "
        f"conflict={conflicting_values}, gap={gap}, next={next_action}"
    )
```

예상 출력:

```text
1) quick structural check
row_count: 36
event_id_count: 3
has_time_order: yes

2) repeated rows per event
A: row_count=18, enough_rows=True
B: row_count=12, enough_rows=True
C: row_count=6, enough_rows=False

3) if we compare rows as if each row were a sample
A at 0s: flow=0.8
A at 1s: flow=0.9
A at 2s: flow=1.1
A at 3s: flow=1.2
A at 4s: flow=1.3
A at 5s: flow=1.4
A at 6s: flow=1.5
A at 7s: flow=1.6
... 28 more time-point rows

4) after regrouping into one row per event
A: observed_span=17s, mean_flow=1.25, peak_pressure=2.0, enough_rows=True
B: observed_span=11s, mean_flow=0.88, peak_pressure=1.5, enough_rows=True
C: observed_span=5s, mean_flow=0.98, peak_pressure=1.5, enough_rows=False

5) controlled changes to A's first three records
original: ordered=True, duplicate_time=False, conflict=False, gap=False, next=continue_checks
reversed: ordered=False, duplicate_time=False, conflict=False, gap=False, next=sort_copy
duplicate: ordered=False, duplicate_time=True, conflict=False, gap=False, next=check_source
conflict: ordered=False, duplicate_time=True, conflict=True, gap=False, next=check_source
missing: ordered=True, duplicate_time=False, conflict=False, gap=True, next=check_source
```

1·2단계의 `has_time_order`는 **파일에서 읽은 순서가 각 사건 안에서 엄격히 증가하는지**만 검사합니다. 같은 시각이 반복되거나 역순이면 `no`가 되지만 두 원인은 다릅니다. 0→2초처럼 중간 기록이 빠져도 증가 조건은 통과합니다.

`minimum_rows_per_event`를 12로 두면 A·B가, 6으로 낮추면 A·B·C가 행 수 조건을 통과합니다. `enough_rows=True`는 이 조건 하나의 결과입니다. 중복 행도 개수에는 포함되므로 충분한 고유 관측점이나 동작 전체 관측을 뜻하지 않습니다. 사건 시작·종료 기록과 측정 간격·운전 조건은 별도로 확인해야 합니다.

4단계의 `observed_span`은 마지막 관측 시각에서 첫 관측 시각을 뺀 길이입니다. A의 `17s`는 0~17초를 관측했다는 뜻이며 실제 동작이 17초 만에 끝났다는 뜻은 아닙니다. 평균 유량과 최대 압력도 현재 기록의 요약일 뿐, 바로 비교 가능하다는 판정은 아닙니다.

5단계는 A의 처음 세 기록만 복사한 실험입니다. `reversed`는 순서만 바뀌므로 `sort_copy`, 중복·충돌·누락 사례는 `check_source`가 됩니다. 충돌 사례는 원문을 확인할 때까지 요약을 보류합니다. `gap`은 이 실험의 1초 간격 가정을 검사하며, 시작 전·끝난 뒤 누락이나 셀의 결측값까지 검사하지 않습니다. `continue_checks`도 전체 품질 검수 통과를 뜻하지 않습니다.

직접 점검하려면 `conflict`에 추가한 유량을 9.0에서 원래 값 0.92로 바꿔 보세요. `conflict`는 False로 바뀌어도 `duplicate_time`은 True이므로 여전히 원문 확인이 필요합니다. 이어 `missing`에 빠진 1초 기록을 복구하면 `gap`은 False가 됩니다. 이처럼 같은 `순서 이상` 신호라도 원인과 다음 행동을 나누어 적어야 합니다.

## 체크리스트

- 새 표의 행 의미·식별자·시간 열·비교 조건·원시 근거를 다섯 줄로 적었는가?
- 사건 식별자의 반복과 같은 사건·시각의 중복을 구분할 수 있는가?
- 역순·충돌값·누락 사례에 대해 정렬·요약 보류·원문 확인 중 다음 행동과 이유를 설명할 수 있는가?
- 행 수 조건 통과와 관측 구간 길이를 전체 동작 관측의 증거로 오해하지 않는가?
- 수정 전 기록을 찾을 파일·행 위치와 파생 표의 처리 이력을 남겼는가?

## 출처와 참고 자료

- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. 변수, 관측치, 표 구조를 구분해 설명하므로, `한 행은 무엇인가`를 먼저 적어 두어야 한다는 이 절의 출발점을 뒷받침합니다. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Earo Wang, Dianne Cook, Rob J. Hyndman, `A New Tidy Data Structure to Support Exploration and Modeling of Temporal Data`, *Journal of Computational and Graphical Statistics* 29(3), 2020. key와 index를 분리해 시간 데이터를 읽는 원리를 제공하므로, `무엇을 묶을 수 있는가`, `시간/순서 열이 있는가`를 먼저 점검해야 한다는 판단을 보강합니다. [https://robjhyndman.com/publications/tsibble/](https://robjhyndman.com/publications/tsibble/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, `PROV-Overview`. provenance와 traceability를 함께 다루므로, 이상 사례가 보일 때 다시 돌아갈 원시 근거를 초기에 적어 두어야 한다는 이 절의 마지막 점검 항목을 지지합니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20

# P2-12.2 선택, 필터링, 집계

> Section ID: `P2-12.2`
> Version: `v2026.09.08`

## 학생 점수표

네 학생의 이름·점수·합격 여부·지역을 표로 만듭니다. 각 학생은 한 행에 들어가며, 점수와 지역을 기준으로 행을 선택하거나 평균을 계산할 수 있습니다.

```python
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Kim", "Park", "Lee", "Choi"],
        "score": [82, 45, 90, 73],
        "passed": ["yes", "no", "yes", "yes"],
        "region": ["Seoul", "Busan", "Seoul", "Busan"],
    }
)

print(df)
```

출력은 다음처럼 읽을 수 있습니다.

```text
   name  score passed region
0   Kim     82    yes  Seoul
1  Park     45     no  Busan
2   Lee     90    yes  Seoul
3  Choi     73    yes  Busan
```

```mermaid
--8<-- "assets/part-02/chapter-12/table-reading-flow-ko.mmd"
```

## Series와 DataFrame

`df["score"]`는 점수 열을 인덱스가 붙은 1차원 값 묶음인 `Series`로 반환합니다.

```python
print(df["score"])
```

출력은 대략 다음처럼 보입니다.

```text
0    82
1    45
2    90
3    73
Name: score, dtype: int64
```

여기서 중요한 점은 결과가 `DataFrame`이 아니라 `Series`라는 것입니다. `Series`는 한 줄짜리 표가 아니라, 인덱스가 붙은 1차원 값 열로 읽을 수 있습니다.

```python
print(df[["name", "score"]])
```

결과는 이름과 점수를 담은 4행 2열 DataFrame입니다. `df[["score"]]`처럼 열 이름 하나를 목록으로 주면 4행 1열 DataFrame을 유지합니다.

```text
   name  score
0   Kim     82
1  Park     45
2   Lee     90
3  Choi     73
```

```python
print(type(df["score"]).__name__)
print(type(df[["name", "score"]]).__name__)
```

출력은 대략 다음처럼 읽힙니다.

```text
Series
DataFrame
```

## 라벨 선택과 위치 선택

Pandas 공식 문서는 `.loc`를 라벨 기반(label-based) 선택으로, `.iloc`를 정수 위치 기반(integer position-based) 선택으로 설명합니다.

```python
print(df.loc[1])
print(df.iloc[1])
```

두 코드는 모두 Park의 행을 출력합니다. 현재 인덱스 라벨 1과 두 번째 위치가 같은 행을 가리키기 때문입니다.

하지만 인덱스를 이름으로 바꾸면 차이가 더 분명해집니다.

```python
named = df.set_index("name")

print(named.loc["Lee"])
print(named.iloc[2])
```

이때:

- `named.loc["Lee"]`는 `Lee`라는 라벨을 찾습니다.
- `named.iloc[2]`는 세 번째 위치의 행을 찾습니다.

## 조건에 맞는 행 선택

점수가 80 이상인 학생을 고르면 Kim과 Lee의 행이 남습니다. 원본 점수는 바뀌지 않습니다.

```python
print(df[df["score"] >= 80])
```

출력은 대략 다음처럼 보입니다.

```text
  name  score passed region
0  Kim     82    yes  Seoul
2  Lee     90    yes  Seoul
```

이 코드는 두 단계로 읽을 수 있습니다.

1. `df["score"] >= 80`이 각 행마다 `True` 또는 `False`를 만든다.
2. `True`인 행만 남긴다.

중간 결과를 직접 보면 더 분명합니다.

```python
mask = df["score"] >= 80
print(mask)
```

```text
0     True
1    False
2     True
3    False
Name: score, dtype: bool
```

이런 불리언 결과를 종종 `mask`라고 부릅니다. 필터링은 `각 행에 질문을 던져서, 맞다(True)고 대답한 행만 남기는 일`로 읽으면 됩니다.

점수 70 이상과 Busan 지역 조건을 `&`로 결합하면 Choi만 남습니다. 각 조건은 괄호로 감쌉니다.

```python
print(df[(df["score"] >= 70) & (df["region"] == "Busan")])
```

이 코드는 점수가 70 이상이면서 지역이 Busan인 행만 남깁니다.

## 평균·최댓값·개수

집계(aggregation)는 여러 값을 요약값으로 바꾸는 계산입니다. 점수 `[82, 45, 90, 73]`의 평균은 72.5, 최댓값은 90, 값의 개수는 4입니다.

```python
print(df["score"].mean())
print(df["score"].max())
print(df["score"].count())
```

`agg`에 집계 이름 목록을 전달하면 세 결과를 한 번에 묶을 수 있습니다. `count`는 결측치를 제외한 값의 개수를 셉니다.

```python
print(df["score"].agg(["mean", "max", "count"]))
```

출력은 대략 다음처럼 보일 수 있습니다.

```text
mean     72.5
max      90.0
count     4.0
Name: score, dtype: float64
```

이 결과는 `score` 열 하나를 여러 방식으로 요약한 작은 표처럼 읽을 수 있습니다.

## 지역별 평균

Pandas 공식 문서는 `groupby`를 데이터를 어떤 기준으로 나눈 뒤, 각 그룹에 함수를 적용해 결합하는 흐름으로 설명합니다. 지역별 점수 평균을 구할 때는 같은 `region` 값을 가진 행끼리 묶습니다.

Busan은 Park 45점과 Choi 73점의 평균인 59점, Seoul은 Kim 82점과 Lee 90점의 평균인 86점입니다.

```python
print(df.groupby("region")["score"].mean())
```

출력은 대략 다음처럼 보일 수 있습니다.

```text
region
Busan    59.0
Seoul    86.0
Name: score, dtype: float64
```

이 코드는 이렇게 읽습니다.

1. `region` 값이 같은 행끼리 묶는다.
2. 각 묶음에서 `score` 열만 본다.
3. 각 묶음의 평균을 계산한다.

## 동작별 센서 기록 요약

동작 A-01과 B-02를 각각 세 시점에 측정한 기록입니다. 동작별로 묶으면 기록 마지막 시각, 평균 신호, 마지막으로 측정한 신호를 한 행에 담을 수 있습니다.

| event_id | elapsed_seconds | progress_fraction | signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 0.0 | 0.00 | 0.8 |
| A-01 | 1.0 | 0.20 | 1.4 |
| A-01 | 2.0 | 0.40 | 1.9 |
| B-02 | 0.0 | 0.00 | 0.7 |
| B-02 | 1.0 | 0.25 | 1.3 |
| B-02 | 2.0 | 0.50 | 1.5 |

| event_id | last_recorded_seconds | signal_a_mean | last_recorded_signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 2.0 | 1.37 | 1.9 |
| B-02 | 2.0 | 1.17 | 1.5 |

```python
log_df = pd.DataFrame(
    {
        "event_id": ["A-01", "A-01", "A-01", "B-02", "B-02", "B-02"],
        "elapsed_seconds": [0.0, 1.0, 2.0, 0.0, 1.0, 2.0],
        "progress_fraction": [0.00, 0.20, 0.40, 0.00, 0.25, 0.50],
        "signal_a": [0.8, 1.4, 1.9, 0.7, 1.3, 1.5],
    }
)

summary = (
    log_df.sort_values(["event_id", "elapsed_seconds"]).groupby("event_id")
    .agg(
        last_recorded_seconds=("elapsed_seconds", "max"),
        signal_a_mean=("signal_a", "mean"),
        last_recorded_signal_a=("signal_a", "last"),
    )
    .reset_index()
)

print(summary.round(2).to_string(index=False))
```

출력은 다음과 같습니다.

```text
event_id  last_recorded_seconds  signal_a_mean  last_recorded_signal_a
    A-01                    2.0           1.37                     1.9
    B-02                    2.0           1.17                     1.5
```

경과 시간으로 정렬했으므로 `last`는 이 예제에서 가장 늦게 기록한 신호를 반환합니다. 정렬하지 않으면 현재 행 순서의 마지막 값이 선택됩니다. 두 동작 모두 마지막 기록은 2초이지만 진행 비율은 각각 0.40과 0.50입니다. 따라서 이 값은 전체 동작의 완료 시간이 아니라 관측된 마지막 시각입니다.

## 사례 1. 임계값과 지역 변경

입력 파일은 [`student-progress-samples.csv`](../../../assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview }입니다. 한 행은 학생 한 명의 학습 기록이고, 핵심 열은 `region`, `study_hours`, `absences`, `practice_quizzes`, `score`, `passed`입니다. 점수 기준 75와 Busan 조건을 적용하면 S010, S013, S016, S018 네 학생이 선택됩니다.

```python
from pathlib import Path
import pandas as pd

csv_path = Path("docs/assets/part-02/chapter-12/student-progress-samples.csv")
df = pd.read_csv(csv_path)

pass_threshold = 75
focus_region = "Busan"

selected = df.loc[
    (df["score"] >= pass_threshold) & (df["region"] == focus_region),
    ["student_id", "region", "score", "passed"],
]

summary = (
    df.assign(over_threshold=df["score"] >= pass_threshold)
    .groupby("region")
    .agg(
        sample_count=("student_id", "count"),
        mean_score=("score", "mean"),
        over_threshold_count=("over_threshold", "sum"),
        mean_absences=("absences", "mean"),
    )
    .round(2)
)

print(selected)
print(summary)
```

같은 계산은 [`p2_12_2_filter_aggregate_threshold.py`](../../../assets/part-02/chapter-12/p2_12_2_filter_aggregate_threshold.py)로도 실행할 수 있습니다. `pass_threshold`를 `70`, `75`, `80`으로 바꾸면 임계값 이상 학생 수가 바뀌고, `focus_region`을 다른 지역으로 바꾸면 선택된 행 목록이 달라집니다.

```mermaid
--8<-- "assets/part-02/chapter-12/table-processing-flow-ko.mmd"
```

점수 기준을 80으로 올리면 Busan의 선택 결과에서 77점인 S016이 빠져 세 학생이 남습니다. 지역별 집계는 `selected`가 아니라 전체 `df`를 사용하므로 평균 점수와 학생 수는 그대로이고, 기준 이상 학생 수만 달라집니다. `focus_region`만 Seoul로 바꾸면 선택한 학생 목록이 바뀌지만 지역별 집계는 전혀 바뀌지 않습니다.

CSV의 `passed`는 저장된 합격 여부입니다. `pass_threshold`를 바꿔도 이 열을 다시 계산하지 않으므로 임계값 이상 여부와 동일한 뜻으로 사용해서는 안 됩니다.

## 체크리스트

- 한 열 선택과 여러 열 선택의 차이를 설명할 수 있는가?
- `loc`와 `iloc`가 각각 무엇을 기준으로 고르는지 말할 수 있는가?
- 불리언 조건이 행을 남기거나 버리는 방식임을 설명할 수 있는가?
- 평균, 개수, 최댓값 같은 집계가 왜 필요한지 설명할 수 있는가?
- `groupby`를 `묶고 나서 요약한다`는 흐름으로 설명할 수 있는가?
- 임계값과 지역 조건을 바꿀 때 선택 결과와 전체 지역별 집계 중 무엇이 달라지는지 설명할 수 있는가?

## 출처와 참고 자료

- pandas Developers, [Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation, 확인 날짜: 2026-07-20. 열 선택, `loc`/`iloc`, 불리언 인덱싱과 행 필터링 설명 확인에 사용했다.
- pandas Developers, [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation, 확인 날짜: 2026-07-20. `groupby`를 split-apply-combine 흐름으로 설명하는 근거로 사용했다.
- pandas Developers, [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation, 확인 날짜: 2026-07-20. DataFrame 생성, 선택, 요약 통계, 기본 표 조작 예시 확인에 사용했다.

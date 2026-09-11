# P2-12.1 Pandas DataFrame은 무엇을 표현하는가

> Section ID: `P2-12.1`
> Version: `v2026.09.08`

## 행과 열이 있는 표

Pandas의 DataFrame은 행과 열에 라벨이 붙은 2차원 표 형식 데이터 구조입니다. 학생 점수표라면 한 행에 한 학생의 이름·점수·합격 여부를 담고, 열 이름으로 각 값의 의미를 구분할 수 있습니다. 같은 표 안에서도 점수 열은 숫자, 이름 열은 문자열을 담습니다.

`dict`의 키를 열 이름으로, 값 목록을 해당 열의 데이터로 넣으면 세 학생의 표가 만들어집니다.

```python
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Kim", "Park", "Lee"],
        "score": [82, 45, 90],
        "passed": ["yes", "no", "yes"],
    }
)

print(df)
```

```text
   name  score passed
0   Kim     82    yes
1  Park     45     no
2   Lee     90    yes
```

왼쪽의 `0, 1, 2`는 행 라벨인 인덱스(index)입니다. `name`, `score`, `passed`는 열 라벨입니다. 인덱스를 제외한 데이터 영역은 3행 3열이며, 1번 행에는 Park의 점수 45와 합격 여부 `no`가 들어 있습니다.

```mermaid
--8<-- "assets/part-02/chapter-12/dataframe-structure-flow-ko.mmd"
```

## 열 묶음과 행 묶음

학생 한 명의 정보를 하나의 `dict`로 묶은 리스트도 DataFrame으로 만들 수 있습니다. 다음 코드는 앞과 같은 표를 출력합니다.

```python
rows = [
    {"name": "Kim", "score": 82, "passed": "yes"},
    {"name": "Park", "score": 45, "passed": "no"},
    {"name": "Lee", "score": 90, "passed": "yes"},
]

df = pd.DataFrame(rows)
print(df)
```

첫 방식은 `score` 열에 `[82, 45, 90]`을 넣습니다. 둘째 방식은 Kim의 기록에 `score: 82`를 넣습니다. 입력을 묶는 방향이 달라도 완성된 표의 행과 열은 같습니다.

## 행 라벨 지정

인덱스를 지정하지 않으면 기본적으로 `0, 1, 2, ...`인 `RangeIndex`가 붙습니다. 이름을 인덱스로 지정하면 번호 대신 Kim, Park, Lee가 행 라벨이 됩니다.

```python
named = pd.DataFrame(
    {
        "score": [82, 45, 90],
        "passed": ["yes", "no", "yes"],
    },
    index=["Kim", "Park", "Lee"],
)

print(named)
```

```text
      score passed
Kim      82    yes
Park     45     no
Lee      90    yes
```

이 표의 데이터 열은 `score`, `passed` 두 개입니다. 이름은 인덱스에 있으므로 `named.shape`는 `(3, 2)`입니다. 앞서 만든 `df`는 이름도 데이터 열에 들어 있어 `(3, 3)`입니다. 인덱스가 숫자라고 해서 항상 현재 행 위치와 같지는 않으며, 라벨이 중복될 수도 있습니다.

## 열별 타입과 표 구조

앞서 만든 `df`의 크기, 열 이름, 인덱스, 열별 타입, 앞 두 행을 출력합니다. `score`가 수치 타입인지 확인하면 점수 평균 같은 계산에 바로 쓸 수 있는지 판단할 수 있습니다.

```python
print(df.shape)
print(df.columns)
print(df.index)
print(df.dtypes)
print(df.head(2))
```

`shape`는 `(3, 3)`, `columns`에는 `name`, `score`, `passed`가 나옵니다. `index`는 `RangeIndex(start=0, stop=3, step=1)`이며, `head(2)`는 Kim과 Park의 행만 보여 줍니다.

| 확인 항목 | 이 표에서 확인할 내용 |
| --- | --- |
| `shape` | 학생 3명, 데이터 열 3개 |
| `columns` | 이름·점수·합격 여부의 열 이름 |
| `index` | 각 행에 붙은 라벨 |
| `dtypes` | 점수 열의 숫자 타입과 나머지 열의 문자열 타입 |
| `head(2)` | 첫 두 학생의 실제 값 |

문자열 열의 타입 표시는 Pandas 버전과 설정에 따라 `str` 또는 `object` 등으로 보일 수 있습니다. `passed`의 `yes`, `no`는 여기서는 문자열 값이며, 자동으로 참·거짓 값이 되는 것은 아닙니다.

NumPy 배열은 배열 전체에 하나의 `dtype`을 사용하고, DataFrame은 열마다 `dtype`을 가집니다. 이름이 붙은 열을 선택하고 정리할 때 DataFrame을 쓰고, 숫자 열을 배열로 옮겨 벡터·행렬 계산을 할 수 있습니다.

## 한 행과 분석 단위

한 행이 언제나 최종 분석 대상 하나를 뜻하지는 않습니다. 다음 센서 기록은 동작 A-01과 B-02를 각각 세 시점에 측정한 표입니다. 한 행은 측정 시점 하나이고, 동작 하나에는 여러 행이 속합니다.

```python
import pandas as pd

raw = pd.DataFrame(
    [
        ["A-01", 0.0, 0.00, 0.8],
        ["A-01", 1.0, 0.20, 1.4],
        ["A-01", 2.0, 0.40, 1.9],
        ["B-02", 0.0, 0.00, 0.7],
        ["B-02", 1.0, 0.25, 1.3],
        ["B-02", 2.0, 0.50, 1.5],
    ],
    columns=["action_id", "elapsed_seconds", "progress_fraction", "signal_a"],
)

print("rows =", len(raw))
print("actions =", raw["action_id"].nunique())
print(raw.groupby("action_id").size())
```

```text
rows = 6
actions = 2
action_id
A-01    3
B-02    3
dtype: int64
```

`len(raw)`는 측정 기록 6개를 셉니다. `nunique()`는 서로 다른 동작 ID 2개를 세고, `groupby("action_id").size()`는 동작마다 기록이 3개씩 있음을 보여 줍니다. `elapsed_seconds`는 동작 시작 후 경과 시간, `progress_fraction`은 진행 비율, `signal_a`는 측정값입니다.

A-01의 측정 행을 하나 더 추가하면 전체 기록은 7개, A-01의 기록은 4개가 되지만 동작 수는 여전히 2개입니다. 같은 코드를 실행해도 무엇을 세느냐에 따라 결과가 달라집니다. 동작별 평균 신호를 비교하려면 측정 행들을 `action_id`로 묶어 계산해야 합니다.

고객 목록에서는 한 행이 고객 한 명일 수 있고, 주문 목록에서는 같은 고객의 주문이 여러 행에 걸쳐 있을 수 있습니다. 따라서 행 수를 고객 수로 사용할 수 있는지는 표의 기록 단위에 달려 있습니다.

## 사례 1. 학생 CSV의 행과 열 확인

[`student-progress-samples.csv`](../../../assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview }에는 학생 36명의 학습 기록이 있습니다. 첫 학생 S001은 Seoul 지역이며 공부 시간 8.0, 결석 1회, 연습 퀴즈 9회, 점수 86, 합격 여부 `yes`로 기록되어 있습니다.

저장소 루트에서 다음 코드를 실행하면 `(36, 7)`과 일곱 열의 이름, 인덱스, 열별 타입, 첫 세 행을 확인할 수 있습니다.

```python
from pathlib import Path
import pandas as pd

csv_path = Path("docs/assets/part-02/chapter-12/student-progress-samples.csv")
df = pd.read_csv(csv_path)

print("shape:", df.shape)
print("columns:", list(df.columns))
print("index:", df.index)
print(df.dtypes)
print(df.head(3))
```

`student_id`는 데이터 열이고, 왼쪽 인덱스는 별도의 `0`부터 `35`까지 번호입니다. `study_hours`는 소수를 포함하며, `region`과 `passed`는 문자열입니다. 모든 열이 숫자는 아니므로 표 전체를 그대로 수치 계산에 넣을 수는 없습니다.

예를 들어 점수를 예측하려면 `score`는 예측 대상 후보이고, 공부 시간·결석 수·퀴즈 수는 입력 후보입니다. `student_id`는 학생을 구분하는 식별자입니다. 이처럼 열 이름과 실제 값을 함께 확인해야 열의 역할을 정할 수 있습니다.

CSV에서 S001의 점수만 86에서 96으로 바꾸면 `shape`와 열 이름은 그대로이고 `head(3)`의 점수만 달라집니다. 학생 행 하나를 추가하면 행 수가 37로 늘어납니다. 구조 확인과 값 확인은 서로 다른 변화를 잡아냅니다.

같은 파일 점검은 [`p2_12_1_dataframe_first_check.py`](../../../assets/part-02/chapter-12/p2_12_1_dataframe_first_check.py)로도 실행할 수 있습니다.

## 체크리스트

- 행, 열, 인덱스의 역할을 각각 말할 수 있는가?
- DataFrame이 숫자와 문자열 열을 함께 담는 방식을 설명할 수 있는가?
- 이름을 데이터 열에 둘 때와 인덱스에 둘 때 `shape`가 어떻게 다른지 설명할 수 있는가?
- 측정 행 수와 동작 수가 다른 이유를 설명할 수 있는가?
- `shape`, `columns`, `index`, `dtypes`, `head()`가 각각 어떤 변화를 보여 주는지 설명할 수 있는가?

## 출처와 참고 자료

- pandas Developers, [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.5 documentation, 확인 날짜: 2026-09-08. DataFrame을 labeled axes를 가진 2차원 tabular data structure로 설명하는 근거로 사용했다.
- pandas Developers, [Package overview](https://pandas.pydata.org/docs/getting_started/overview.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation, 확인 날짜: 2026-07-20. pandas가 tabular, time series, matrix data를 다루는 도구라는 설명을 DataFrame 입문 배경으로 사용했다.
- pandas Developers, [Migration guide for the new string data type](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.5 documentation, 확인 날짜: 2026-09-08. 버전과 설정에 따른 문자열 열의 타입 표시 차이를 확인했다.

# P2-12.1 Pandas DataFrame은 무엇을 표현하는가

> Section ID: `P2-12.1`
> Version: `v2026.07.31`

Part 2 Chapter 11에서는 NumPy 배열(array)로 벡터(vector), 행렬(matrix), 축(axis), 브로드캐스팅(broadcasting)을 다뤘습니다. 그 흐름은 수치 계산에는 강하지만, 표(table)처럼 생긴 데이터셋(dataset)을 읽을 때는 질문이 조금 바뀝니다.

현실의 데이터는 종종 이런 모양으로 옵니다.

| name | score | passed |
| --- | ---: | --- |
| Kim | 82 | yes |
| Park | 45 | no |
| Lee | 90 | yes |

이 표를 보면 우리는 위치(position)보다 `누가`, `어떤 열(column)`, `어떤 값(value)`인가를 먼저 읽습니다. Pandas의 DataFrame은 바로 이런 표 형식 데이터를 다루기 위한 중심 구조입니다.

여기서는 `DataFrame`, `행(row)`, `열(column)`, `인덱스(index)`의 기본 구분을 설명합니다. 앞 장의 NumPy가 그 값을 실제 계산에 쓸 수 있는 벡터와 행렬 모양으로 어떻게 다룰지를 다뤘다면, 여기서는 그 숫자 묶음이 어떤 사례와 변수의 표로 읽혀야 하는지 살핍니다. 다음 장에서는 이 표에서 바로 안 보이는 변화와 관계를 그래프로 확인합니다. 이후 표 선택, 집계, 데이터셋 준비로 이어질 때도 이 절의 표 구조 설명을 기준점으로 삼습니다.

## 핵심 기준: Pandas DataFrame은 무엇을 표현하는가

- DataFrame을 라벨(label)이 붙은 2차원 표 형식 데이터 구조로 설명할 수 있습니다.
- 행, 열, 인덱스가 각각 무엇을 식별하는지 설명할 수 있습니다.
- DataFrame이 같은 표 안에 숫자와 문자열 같은 서로 다른 타입(type)을 함께 담을 수 있음을 설명할 수 있습니다.
- 머신러닝 데이터셋에서 한 행은 하나의 사례(case) 또는 샘플(sample), 한 열은 하나의 변수(variable) 또는 특징(feature)으로 읽을 수 있음을 설명할 수 있습니다.
- DataFrame을 처음 받았을 때 `shape`, `columns`, `index`, `dtypes`, `head()`를 왜 먼저 확인하는지 설명할 수 있습니다.

## 세 가지 기준

| 기준 | 왜 중요한가 | 이 절에서 필요한 이해 수준 |
| --- | --- | --- |
| DataFrame이 무엇인가 | Pandas를 단순 저장 도구가 아니라 표 의미를 드러내는 구조로 읽게 해 줍니다. | 이름표가 붙은 2차원 표로 이해합니다. |
| 배열과 무엇이 다른가 | NumPy 배열과 DataFrame의 역할을 섞지 않게 해 줍니다. | 행과 열 이름, 서로 다른 타입의 열을 함께 다루기 쉽다는 점을 잡습니다. |
| 어떻게 읽기 시작해야 하나 | 이후 선택, 집계, 데이터셋 준비의 출발점을 만들어 줍니다. | 한 행은 한 사례, 한 열은 한 변수라는 관점부터 잡습니다. |

| 용어 | 이 절에서 먼저 잡을 뜻 |
| --- | --- |
| DataFrame | 행과 열 이름이 붙은 2차원 표 형식 데이터 구조입니다. |
| 행(row) | 표에서 한 사례나 한 관측 단위를 나타내는 가로줄입니다. |
| 열(column) | 표에서 하나의 변수나 속성을 나타내는 세로줄입니다. |
| 인덱스(index) | 각 행을 식별하기 위한 라벨입니다. |
| 라벨(label) | 위치 번호 대신 행이나 열에 붙어 있는 이름표입니다. |

## DataFrame은 라벨이 붙은 2차원 표다

Pandas 공식 문서는 `DataFrame`을 2차원(two-dimensional), 크기 변경 가능(size-mutable), 잠재적으로 서로 다른 타입을 함께 담을 수 있는(potentially heterogeneous) 표 형식(tabular) 데이터라고 설명합니다. 또한 행과 열에 라벨이 붙어 있고, 연산은 이 라벨을 기준으로 정렬(alignment)될 수 있다고 설명합니다.

여기서는 DataFrame을 `행과 열 이름이 붙어 있는 표이며, 각 열이 서로 다른 의미와 타입을 가질 수 있는 데이터 구조`로 이해합니다.

NumPy 배열이 위치 기반 계산에 강하다면, DataFrame은 `표의 의미`를 드러내는 데 강합니다.

| 구조 | 먼저 보는 것 | 잘 맞는 질문 |
| --- | --- | --- |
| NumPy array | 위치, shape, axis | 몇 번째 값인가, 어느 방향으로 계산하는가 |
| Pandas DataFrame | 행 이름, 열 이름, 열의 의미 | 어떤 사례인가, 어떤 변수인가, 어떤 열을 비교할 것인가 |

NumPy가 계산 가능한 숫자 모양을 다뤘다면, 여기서는 그 숫자 묶음을 `한 행은 무엇을 뜻하는가`, `한 열은 어떤 변수를 뜻하는가`라는 표 해석 관점으로 다시 읽습니다. 이 관점은 다음 절의 선택과 집계, 다음 장의 시각화, 뒤의 기록 정리까지 이어집니다. 지금 절에서 먼저 끝내야 하는 일은 한 행을 한 사례로, 한 열을 한 변수로 읽는 표 감각을 만드는 것입니다.

가장 단순한 생성 예는 `dict`로 열을 넣는 방식입니다.

문제 상황: 열 이름이 붙은 가장 작은 표를 직접 만들어 DataFrame의 기본 모양을 보고 싶습니다.
입력(input): `name`, `score`, `passed` 세 열을 담은 `dict`.
기대 출력(output): 세 학생 정보를 담은 3행 3열 표가 출력됩니다.
확인할 개념: DataFrame은 열 이름이 있는 2차원 표 형식 구조입니다.

```python
# Pandas DataFrame으로 행과 열이 있는 표 데이터를 만들고 구조를 확인하는 예제입니다.
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

하지만 현실의 원시 데이터는 종종 `행` 중심으로도 옵니다. 예를 들어 JSON 응답이나 기록 묶음은 다음처럼 `dict`의 리스트(list of dictionaries)로 들어올 수 있습니다.

문제 상황: 같은 표라도 원본이 열 묶음이 아니라 행 묶음 형태로 들어올 수 있습니다.
입력(input): 각 학생을 하나의 `dict`로 담은 리스트.
기대 출력(output): 앞선 예제와 같은 구조의 DataFrame.
확인할 개념: DataFrame은 열 중심 입력과 행 중심 입력을 모두 표 구조로 바꿀 수 있습니다.

```python
# Pandas DataFrame으로 행과 열이 있는 표 데이터를 만들고 구조를 확인하는 예제입니다.
rows = [
    {"name": "Kim", "score": 82, "passed": "yes"},
    {"name": "Park", "score": 45, "passed": "no"},
    {"name": "Lee", "score": 90, "passed": "yes"},
]

df = pd.DataFrame(rows)
print(df)
```

두 방식 모두 같은 표를 만들 수 있습니다. 여기서는 이렇게 구분합니다.

- 열 중심 입력: `각 열에 어떤 값 묶음이 들어가는가`를 먼저 생각한다.
- 행 중심 입력: `각 사례가 어떤 속성 묶음으로 들어오는가`를 먼저 생각한다.

입력 형식이 열 중심이든 행 중심이든, 그것만으로 `무엇이 샘플 1건인가`가 자동으로 정해지지는 않습니다.

다만 여기서 한 가지를 더 조심해야 합니다. DataFrame에서 `한 행 = 완성된 사례 1건`이라고 바로 단정할 수는 없습니다. 원시 시계열처럼 시간 순서대로 쌓인 표에서는 한 행이 동작 전체가 아니라 `동작 중 한 시점의 기록`일 수도 있습니다.

원시 시계열의 한 행은 측정 시점 하나일 뿐이고, 실제로 비교하려는 대상은 그 행들이 모인 동작 1회일 수 있습니다.

| action_id | elapsed_seconds | progress_fraction | signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 0.0 | 0.00 | 0.8 |
| A-01 | 1.0 | 0.20 | 1.4 |
| A-01 | 2.0 | 0.40 | 1.9 |
| B-02 | 0.0 | 0.00 | 0.7 |
| B-02 | 1.0 | 0.25 | 1.3 |
| B-02 | 2.0 | 0.50 | 1.5 |

이런 표에서는 한 행이 한 동작이 아니라 `한 시점`을 뜻하고, `action_id` 같은 식별자 열이 여러 행을 하나의 동작으로 묶어 주는 기준이 됩니다. 즉, DataFrame을 읽을 때는 `한 행이 곧 한 최종 사례인가`, 아니면 `여러 행이 함께 한 사례를 이루는가`를 먼저 구분해야 합니다.

바로 다음처럼 보면 이 차이가 더 분명합니다.

| 읽기 단위 | 지금 표에서 무엇을 뜻하는가 |
| --- | --- |
| 한 행 | 센서가 기록된 한 시점 |
| `action_id` 하나 | 동작 1회 |
| 여러 `action_id` 묶음 | 여러 동작을 모은 데이터셋 |

이 구분이 중요한 이유는, 같은 DataFrame이라도 질문이 달라지면 읽는 단위도 달라지기 때문입니다. 원시 시계열을 그대로 읽을 때는 한 행이 중요하지만, 동작 전체를 비교하려면 여러 행을 묶어 하나의 동작 1회 요약 행으로 다시 만들어야 할 수도 있습니다.

즉, DataFrame은 표 구조를 제공하지만 `분석 단위`를 대신 결정해 주지는 않습니다. 표를 받았을 때는 `행과 열이 어떻게 보이는가`를 먼저 읽고, 그다음에 `실제로 비교할 샘플 1건이 무엇인가`를 따로 판단해야 합니다.

예를 들어 `action_id`별 행 수만 세어도 벌써 `한 행`에서 `동작 1회`로 읽기 단위가 바뀝니다.

문제 상황: 원시 로그 여러 행이 실제로 몇 개의 동작으로 묶이는지 가장 짧은 코드로 확인하고 싶습니다.
입력(input): `action_id`, `elapsed_seconds`, `progress_fraction`, `signal_a` 열이 들어 있는 작은 원시 시계열 표.
기대 출력(output): 전체 행 수, 고유 `action_id` 수, 각 `action_id`별 행 수.
확인할 개념: DataFrame에서 한 행은 한 시점일 수 있고, `groupby`를 통해 여러 행을 하나의 동작 단위로 다시 읽을 수 있습니다.

```python
# Pandas DataFrame으로 행과 열이 있는 표 데이터를 만들고 구조를 확인하는 예제입니다.
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

출력은 대략 다음처럼 읽을 수 있습니다.

```text
rows = 6
actions = 2
action_id
A-01    3
B-02    3
dtype: int64
```

이 출력에서 중요한 것은 계산 결과보다 관점입니다.

- 전체 DataFrame은 6행이다.
- 하지만 실제 동작은 2건이다.
- 즉, 여러 행이 함께 한 사례를 이루는 표도 DataFrame으로 자연스럽게 다룰 수 있다.

이 표는 원천 데이터의 구조를 보여 줄 뿐이고, 아직 품질 판단이나 원인 확정을 말해 주지는 않습니다.

이 관점은 다음 절의 필터링과 집계뿐 아니라, 뒤에서 특징(feature)이나 요약 표를 만들 때도 다시 쓰입니다.

## 행, 열, 인덱스를 따로 읽는다

DataFrame을 처음 보면 표 전체만 보이기 쉽지만, 실제로는 세 층을 함께 읽어야 합니다.

1. 행(row): 사례(case), 샘플(sample), 관측(observation)
2. 열(column): 변수(variable), 특징(feature), 속성(attribute)
3. 인덱스(index): 행을 식별하는 라벨(label)

아래 작은 예를 봅니다.

문제 상황: 행, 열, 인덱스를 설명하려면 먼저 가장 단순한 표를 다시 눈으로 확인해야 합니다.
입력(input): 이름, 점수, 합격 여부를 담은 작은 `DataFrame`.
기대 출력(output): 기본 번호 인덱스가 붙은 표 출력.
확인할 개념: 한 행은 한 사례이고, 열 이름과 인덱스가 함께 표 구조를 이룹니다.

```python
# Pandas DataFrame으로 행과 열이 있는 표 데이터를 만들고 구조를 확인하는 예제입니다.
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

출력은 다음처럼 읽을 수 있습니다.

```text
   name  score passed
0   Kim     82    yes
1  Park     45     no
2   Lee     90    yes
```

여기서:

- 왼쪽의 `0, 1, 2`는 인덱스(index)입니다.
- `name`, `score`, `passed`는 열 이름(column labels)입니다.
- 각 가로줄은 한 사람에 대한 한 행(row)입니다.

도식으로 보면 더 분명합니다.

```mermaid
--8<-- "assets/part-02/chapter-12/dataframe-structure-flow-ko.mmd"
```

이 도식의 핵심은 인덱스가 데이터 값 자체가 아니라 `행을 가리키는 기준`이라는 점입니다.

## 인덱스는 단순 번호일 수도 있고, 의미 있는 라벨일 수도 있다

Pandas 공식 문서는 인덱스를 따로 주지 않으면 `RangeIndex`를 기본으로 쓴다고 설명합니다. 그래서 처음 만든 DataFrame에는 `0, 1, 2, ...` 같은 번호가 자주 보입니다.

하지만 인덱스는 꼭 번호일 필요가 없습니다.

문제 상황: 표 왼쪽 번호 대신 의미 있는 라벨을 인덱스로 둘 수도 있음을 확인하고 싶습니다.
입력(input): `score`, `passed` 열과 이름 목록을 인덱스로 준 `DataFrame`.
기대 출력(output): `Kim`, `Park`, `Lee`가 왼쪽 행 라벨로 보이는 표.
확인할 개념: 인덱스는 단순 번호가 아니라 행을 식별하는 별도 구조입니다.

```python
# Pandas DataFrame으로 행과 열이 있는 표 데이터를 만들고 구조를 확인하는 예제입니다.
df = pd.DataFrame(
    {
        "score": [82, 45, 90],
        "passed": ["yes", "no", "yes"],
    },
    index=["Kim", "Park", "Lee"],
)

print(df)
```

출력은 다음처럼 바뀝니다.

```text
      score passed
Kim      82    yes
Park     45     no
Lee      90    yes
```

이제 `Kim`, `Park`, `Lee`가 행 라벨이 됩니다. 여기서는 이렇게 기억합니다.

- 번호 인덱스: 기본 순서를 가리킨다.
- 라벨 인덱스: 행의 이름이나 식별자를 가리킨다.

이 차이는 다음 절에서 선택(select)과 필터링(filtering)을 배울 때 중요해집니다.

작은 실험으로 보면 더 분명합니다.

문제 상황: 현재 DataFrame이 어떤 인덱스 구조를 쓰는지 객체 형태로 직접 확인하고 싶습니다.
입력(input): 앞에서 만든 `df`.
기대 출력(output): `RangeIndex(...)` 또는 `Index([...])` 형태의 인덱스 정보.
확인할 개념: 인덱스는 표에 보이는 장식이 아니라 Pandas가 행을 관리하는 구조입니다.

```python
# Pandas DataFrame으로 행과 열이 있는 표 데이터를 만들고 구조를 확인하는 예제입니다.
print(df.index)
```

번호 인덱스를 쓴 경우 출력은 다음처럼 읽힙니다.

```text
RangeIndex(start=0, stop=3, step=1)
```

반대로 식별자 라벨을 인덱스로 주면 다음처럼 읽힐 수 있습니다.

```text
Index(['Kim', 'Park', 'Lee'], dtype='object')
```

즉, 인덱스는 표 왼쪽에 보이는 장식이 아니라, 행을 가리키는 또 하나의 구조입니다.

## DataFrame은 서로 다른 타입의 열을 함께 담는다

NumPy 배열은 보통 같은 타입(dtype)의 숫자를 한꺼번에 계산하는 데 강합니다. 반면 표 데이터는 한 열은 숫자이고, 다른 열은 문자열일 수 있습니다.

위 예제에서도:

- `name` 열은 문자열(string)입니다.
- `score` 열은 숫자(number)입니다.
- `passed` 열은 범주(categorical)처럼 읽을 수 있는 문자열입니다.

그래서 DataFrame은 `열마다 의미가 다를 수 있다`는 현실 데이터를 더 자연스럽게 담습니다.

이 점은 머신러닝 데이터셋을 준비할 때 중요합니다. 실제 데이터는 숫자 열만 있지 않고, 날짜(date), 문자열(text), 범주(category), 결측치(missing value)가 섞여 있는 경우가 많기 때문입니다.

예를 들어 다음처럼 타입을 확인할 수 있습니다.

문제 상황: 각 열이 숫자인지 문자열인지 먼저 알아야 뒤의 선택과 전처리 판단이 쉬워집니다.
입력(input): 이름, 점수, 합격 여부가 들어 있는 `df`.
기대 출력(output): 열마다 `object`, `int64` 같은 타입 정보가 출력됩니다.
확인할 개념: DataFrame은 전체가 아니라 열별로 서로 다른 타입을 가질 수 있습니다.

```python
# Pandas DataFrame으로 행과 열이 있는 표 데이터를 만들고 구조를 확인하는 예제입니다.
print(df.dtypes)
```

출력은 대략 다음처럼 보일 수 있습니다.

```text
name      object
score      int64
passed    object
dtype: object
```

여기서 중요한 것은 `DataFrame 전체의 타입`이 아니라 `열마다 타입이 따로 보인다`는 점입니다.

- `score`는 수치 계산에 바로 쓰기 쉬운 열입니다.
- `name`, `passed`는 그대로는 수치 계산보다 식별과 구분에 더 가까운 열입니다.

이 감각이 있어야 나중에 `어떤 열을 모델 입력으로 쓸 것인가`, `어떤 열은 먼저 변환해야 하는가`를 판단할 수 있습니다.

## 한 행은 하나의 사례, 한 열은 하나의 변수라고 먼저 가정해 본다

학습용 표 데이터를 처음 읽을 때 가장 중요한 습관은 `한 행은 하나의 사례, 한 열은 하나의 변수라고 먼저 가정해 보는 것`입니다.

예를 들어 고객 데이터가 있다면:

| customer_id | age | region | purchased |
| --- | ---: | --- | --- |
| C001 | 29 | Seoul | yes |
| C002 | 41 | Busan | no |
| C003 | 35 | Seoul | yes |

이 표는 이렇게 읽을 수 있습니다.

- 각 행(row): 한 명의 고객
- `age`, `region`: 입력 변수 또는 특징(feature)
- `purchased`: 예측하고 싶은 대상(target) 후보

아직 모델을 학습하지 않더라도, 이 읽기 방식이 잡혀 있어야 나중에 `feature`, `label`, `target`, `split` 같은 말이 헷갈리지 않습니다.

다만 이 문장은 `항상 참`인 규칙이 아니라 `가장 먼저 시험해 볼 기본 읽기 방식`에 가깝습니다.

| 표 유형 | 한 행이 바로 샘플 1건인가 |
| --- | --- |
| 고객 목록, 주문 목록, 학생 명단 같은 사례 표 | 대체로 그렇다 |
| 시간 순서대로 쌓인 원시 시계열 표 | 아닐 수 있다 |
| 이미 집계된 요약 표 | 집계 단위가 곧 샘플일 수 있다 |

물론 모든 표가 반드시 이 구조를 따르는 것은 아닙니다. 어떤 표는 시간 순서 기록(log)일 수도 있고, 어떤 표는 요약 집계 결과일 수도 있습니다. 그래도 `행은 사례, 열은 변수`라는 기본 가정을 먼저 두는 편이 도움이 됩니다.

## DataFrame은 배열과 경쟁하는 구조가 아니라 역할이 다르다

DataFrame과 NumPy 배열을 둘 중 하나만 써야 하는 경쟁 관계로 볼 필요는 없습니다.

두 구조는 자주 함께 씁니다.

| 작업 | 더 자연스러운 구조 |
| --- | --- |
| 표 데이터 읽기, 열 이름 보기, 데이터셋 정리 | DataFrame |
| 수치 배열 계산, 벡터화, 선형대수 계산 | NumPy array |
| 모델 입력 직전 숫자 배열로 바꾸기 | DataFrame에서 array로 이동 |

실무와 실습에서는 이런 흐름이 흔합니다.

1. CSV를 읽어 DataFrame으로 확인한다.
2. 필요한 열만 고른다.
3. 결측치와 타입을 정리한다.
4. 숫자 중심 계산이 필요하면 NumPy 배열이나 모델 입력 형태로 넘긴다.

즉, DataFrame은 데이터를 `설명 가능한 표`로 다루는 단계에 강하고, NumPy는 `배열 계산` 단계에 강합니다.

## DataFrame을 처음 받으면 무엇부터 확인하는가

처음 받은 DataFrame에서 바로 복잡한 조작부터 할 필요는 없습니다. 먼저 구조를 확인해야 합니다.

문제 상황: 새로 받은 표를 다루기 전에 크기, 열 이름, 인덱스, 타입, 앞부분 모양을 빠르게 점검해야 합니다.
입력(input): `df`.
기대 출력(output): `shape`, `columns`, `index`, `dtypes`, `head()` 결과.
확인할 개념: DataFrame 첫 점검은 구조를 한 번에 훑는 일입니다.

```python
# Pandas DataFrame으로 행과 열이 있는 표 데이터를 만들고 구조를 확인하는 예제입니다.
print(df.shape)
print(df.columns)
print(df.index)
print(df.dtypes)
print(df.head())
```

각 항목은 다음 질문에 답합니다.

| 확인 항목 | 질문 |
| --- | --- |
| `shape` | 몇 행 몇 열인가 |
| `columns` | 어떤 열들이 있는가 |
| `index` | 행을 무엇으로 식별하는가 |
| `dtypes` | 각 열은 어떤 타입으로 읽히는가 |
| `head()` | 앞부분 몇 줄은 어떤 모양인가 |

이 다섯 가지는 DataFrame의 `첫 인상 점검표`라고 볼 수 있습니다.

특히 `dtypes`는 중요합니다. 눈으로 보기에는 숫자처럼 보여도 문자열로 들어와 있는 경우가 있기 때문입니다. 이 문제는 다음 절에서 필터링과 집계를 할 때 바로 영향을 줍니다.

작은 예로 한 번에 보면 이런 식입니다.

문제 상황: 구조 점검 다섯 가지를 한 번에 실행했을 때 실제 출력이 어떤 모습인지 확인하고 싶습니다.
입력(input): `df`.
기대 출력(output): 표 크기, 열 목록, 인덱스 구조, 열 타입, 앞 두 행이 순서대로 출력됩니다.
확인할 개념: 구조 점검 코드는 표의 전체 윤곽을 아주 짧은 출력으로 요약해 줍니다.

```python
# Pandas DataFrame으로 행과 열이 있는 표 데이터를 만들고 구조를 확인하는 예제입니다.
print(df.shape)
print(df.columns)
print(df.index)
print(df.dtypes)
print(df.head(2))
```

출력은 대략 다음처럼 읽을 수 있습니다.

```text
(3, 3)
Index(['name', 'score', 'passed'], dtype='object')
RangeIndex(start=0, stop=3, step=1)
name      object
score      int64
passed    object
dtype: object
   name  score passed
0   Kim     82    yes
1  Park     45     no
```

이 다섯 줄은 DataFrame의 구조를 빠르게 훑는 기본 점검에 가깝습니다.

- `shape`: 표의 크기
- `columns`: 열 이름 목록
- `index`: 행 라벨 구조
- `dtypes`: 열 타입
- `head(2)`: 실제 앞부분 모습

아직 조작을 시작하지 않아도, 이 확인만으로도 “이 표가 어떤 종류의 데이터인가”를 훨씬 빨리 파악할 수 있습니다.

같은 점검을 파일에서 읽은 표에도 적용해 볼 수 있습니다. P2-12.2와 P2-12.3에서 이어서 사용할 입력 파일은 [`student-progress-samples.csv`](../../../assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview }입니다. 한 행은 학생 한 명의 학습 기록이고, `region`, `study_hours`, `absences`, `practice_quizzes`, `score`, `passed` 같은 열을 가집니다.

문제 상황: CSV 파일을 처음 읽었을 때 바로 계산하지 않고 표 구조부터 확인하고 싶습니다.
입력(input): 36행 학생 진행도 CSV.
기대 출력(output): 표 크기, 열 이름, 인덱스, 열 타입, 앞부분 세 행.
확인할 개념: DataFrame 첫 점검은 파일을 읽은 직후 표의 크기와 열 역할을 빠르게 파악하는 일입니다.

```python
# Pandas DataFrame으로 행과 열이 있는 표 데이터를 만들고 구조를 확인하는 예제입니다.
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

같은 코드는 [`p2_12_1_dataframe_first_check.py`](../../../assets/part-02/chapter-12/p2_12_1_dataframe_first_check.py)로 실행할 수 있습니다. 이 파일은 다음 절의 필터링과 집계로 넘어가기 전에, 표가 몇 행 몇 열인지와 각 열이 어떤 타입으로 읽혔는지 먼저 확인하게 해 줍니다.

## Pandas DataFrame은 무엇을 표현하는가: 확인할 판단 기준

이 사례 절은 다음 질문으로 중심축을 확인한다.

- 오픈체크리스트의 중심축 문장인 "DataFrame이 표 형태 데이터를 다루는 기본 구조라는 점을 설명해야 합니다."를 본문 사례에서 어느 대목으로 확인할 수 있는가?
- 표, 코드, 도식, 체크리스트 중 어떤 장치가 이 판단을 다시 검토하게 만드는가?

### 사례 1. 출석부 표를 처음 받았을 때 어디부터 읽어야 하는가

학습자가 학급 점수표를 받았다고 해 보겠습니다. 표에는 이름, 지역, 결석 수, 점수, 합격 여부가 함께 들어 있습니다. 사람은 표를 보자마자 `누가 몇 점을 받았는지`부터 읽을 수 있지만, 모델 관점에서는 먼저 `한 행이 누구를 나타내는가`, `각 열이 무엇을 뜻하는가`를 다시 정리해야 합니다.

이때 DataFrame은 단순히 숫자를 담은 상자가 아니라, `name`, `score`, `passed`처럼 이름표가 붙은 표로 읽힙니다. 한 행은 한 학생 사례가 되고, 한 열은 점수나 결석 수처럼 각각 다른 의미를 가진 변수 자리가 됩니다. 인덱스는 값 자체보다 행을 가리키는 기준이라는 점도 함께 드러납니다.

이 사례가 중요한 이유는, 이후 선택과 필터링, 학습용 데이터셋 준비가 모두 이 읽기 방식 위에서 시작되기 때문입니다. 표를 받았을 때 바로 계산식부터 쓰기보다 `shape`, `columns`, `dtypes`, `head()`를 먼저 확인하는 습관이 필요한 이유도 여기에 있습니다.

즉 DataFrame 입문은 문법보다 관점의 전환에 가깝습니다. `엑셀처럼 보이는 표`를 `행과 열의 역할이 정리된 데이터 구조`로 읽기 시작해야 뒤의 Pandas 조작과 머신러닝 준비가 자연스럽게 이어집니다.

## 체크리스트

- DataFrame을 `행과 열 이름이 있는 표`로 설명할 수 있는가?
- 행, 열, 인덱스의 역할을 각각 말할 수 있는가?
- DataFrame이 숫자와 문자열 열을 함께 담을 수 있음을 설명할 수 있는가?
- 머신러닝 데이터셋에서 한 행과 한 열을 어떻게 읽는지 설명할 수 있는가?
- `shape`, `columns`, `index`, `dtypes`, `head()`를 왜 먼저 확인하는지 설명할 수 있는가?
- DataFrame을 라벨이 붙은 2차원 표 형식 데이터 구조로 설명할 수 있는가?

## 출처와 참고 자료

- pandas Developers, [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation, 확인 날짜: 2026-07-20. DataFrame을 labeled axes를 가진 2차원 tabular data structure로 설명하는 근거로 사용했다.
- pandas Developers, [Package overview](https://pandas.pydata.org/docs/getting_started/overview.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation, 확인 날짜: 2026-07-20. pandas가 tabular, time series, matrix data를 다루는 도구라는 설명을 DataFrame 입문 배경으로 사용했다.

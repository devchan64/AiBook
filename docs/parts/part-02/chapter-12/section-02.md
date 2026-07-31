# P2-12.2 선택, 필터링, 집계

> Section ID: `P2-12.2`
> Version: `v2026.07.31`

P2-12.1에서는 Pandas `DataFrame`을 행(row), 열(column), 인덱스(index)가 있는 표 형식 데이터 구조로 봤습니다. 이제 질문이 하나 더 생깁니다.

표를 받았다고 해서 필요한 정보가 바로 보이는 것은 아닙니다. 실제로는 다음과 같은 일을 계속 하게 됩니다.

- 특정 열만 고른다.
- 특정 행만 본다.
- 조건에 맞는 행만 남긴다.
- 숫자 열의 평균이나 개수를 확인한다.
- 범주별로 나누어 요약한다.

Pandas에서 선택(select), 필터링(filtering), 집계(aggregation)는 바로 이 흐름을 다룹니다.

여기서는 `Series`, `필터링(filtering)`, `집계(aggregation)`, `groupby`, `loc`, `iloc`의 기본 구분을 설명합니다. `DataFrame` 자체의 대표 설명은 P2-12.1에 두고, 여기서는 그 표에서 무엇을 읽고 무엇을 남기고 무엇을 요약할지 설명합니다.

## 핵심 기준: 선택, 필터링, 집계

- 한 열 선택과 여러 열 선택의 결과가 어떻게 다른지 설명할 수 있습니다.
- `loc`는 라벨(label), `iloc`는 위치(position)를 기준으로 읽는다고 설명할 수 있습니다.
- 불리언(Boolean) 조건으로 행을 거른다는 뜻을 설명할 수 있습니다.
- 집계는 원래 표 전체를 더 작은 요약값으로 바꾸는 과정이라고 설명할 수 있습니다.
- `groupby`를 같은 범주끼리 먼저 묶고 나서 요약하는 방식으로 설명할 수 있습니다.

## 세 가지 기준

| 기준 | 왜 중요한가 | 이 절에서 필요한 이해 수준 |
| --- | --- | --- |
| 열 선택과 행 필터의 차이 | 읽을 대상과 남길 대상을 섞지 않게 해 줍니다. | 하나는 무엇을 읽을지 고르고, 다른 하나는 무엇을 남길지 고른다고 이해합니다. |
| `loc`와 `iloc`가 왜 나뉘는가 | 라벨 기준과 위치 기준을 혼동하지 않게 해 줍니다. | `loc`는 라벨, `iloc`는 위치를 기준으로 읽는다고 이해합니다. |
| `groupby`가 무엇을 하는가 | 표 전체를 범주별 요약으로 바꾸는 흐름을 분명하게 해 줍니다. | 같은 범주끼리 묶은 뒤 요약값을 계산하는 방식으로 이해합니다. |

| 용어 | 이 절에서 먼저 잡을 뜻 |
| --- | --- |
| Series | 인덱스가 붙은 1차원 값 열입니다. |
| 필터링(filtering) | 조건에 맞는 행만 남기는 선택 방식입니다. |
| 집계(aggregation) | 여러 값을 평균, 합, 개수 같은 더 작은 요약값으로 바꾸는 과정입니다. |
| `groupby` | 같은 범주끼리 먼저 묶은 뒤 각 묶음별 요약을 계산하는 방식입니다. |
| `loc` / `iloc` | 각각 라벨 기준, 위치 기준으로 행과 열을 고르는 도구입니다. |

이 절 다음 흐름도 단순합니다.

- `P2-12.3`에서는 지금 선택하고 요약한 표가 실제 데이터셋 준비와 누수 방지 문맥에서 어떻게 이어지는지 봅니다.
- 이후 Pandas 실습과 모델 입력 준비 구간에서는 같은 질문이 `어떤 열을 남기고 어떤 요약을 만들 것인가`로 반복됩니다.

## 예제 표를 먼저 고정한다

이 절에서는 다음 작은 표를 계속 사용합니다.

문제 상황: 선택, 필터링, 집계 예제를 같은 표로 이어서 보려면 기준이 되는 작은 DataFrame을 먼저 만들어야 합니다.
입력(input): 이름, 점수, 합격 여부, 지역을 담은 네 열.
기대 출력(output): 네 학생이 들어 있는 예제 표가 출력됩니다.
확인할 개념: 이후의 모든 선택과 필터링은 같은 표를 기준으로 질문만 달리하는 흐름입니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
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

이 표를 보고 우리는 “전체를 다 보는 것”에서 시작하지만, 곧바로 “어느 열?”, “어느 행?”, “어떤 조건?”이라는 질문으로 이동합니다.

도식으로 보면 이 절의 흐름은 다음과 같습니다.

```mermaid
--8<-- "assets/part-02/chapter-12/table-reading-flow-ko.mmd"
```

## 한 열을 고르면 Series가 된다

Pandas에서는 한 열을 고를 수 있습니다.

문제 상황: 점수 열 하나만 꺼내면 결과가 표가 아니라 어떤 형태로 바뀌는지 확인하고 싶습니다.
입력(input): `df["score"]`.
기대 출력(output): 점수만 담긴 1차원 `Series` 출력.
확인할 개념: 한 열 선택은 보통 `DataFrame`이 아니라 `Series`를 돌려줍니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
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

여기서는 다음 차이를 먼저 기억해 두면 됩니다.

- `df["score"]`: 한 열을 꺼낸다. 결과는 보통 `Series`
- `df[["name", "score"]]`: 여러 열을 고른다. 결과는 `DataFrame`

예를 들어:

문제 상황: 이름과 점수를 함께 남기면 한 열 선택과 결과 형태가 어떻게 달라지는지 비교하고 싶습니다.
입력(input): `df[["name", "score"]]`.
기대 출력(output): 두 열이 유지된 작은 `DataFrame`.
확인할 개념: 여러 열을 고르면 원래 표 구조의 일부가 남습니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
print(df[["name", "score"]])
```

출력은 여전히 표 모양입니다.

```text
   name  score
0   Kim     82
1  Park     45
2   Lee     90
3  Choi     73
```

즉, 한 열을 고르면 값 열 하나를 읽는 느낌이 강해지고, 여러 열을 고르면 원래 표의 일부를 떼어 보는 느낌이 남습니다.

같은 차이를 표로 보면 더 분명합니다.

| 코드 | 결과 형태 | 읽는 질문 |
| --- | --- | --- |
| `df["score"]` | `Series` | 점수 열 값만 보고 싶은가 |
| `df[["name", "score"]]` | `DataFrame` | 이름과 점수를 함께 비교하고 싶은가 |

작은 점검 코드도 useful합니다.

문제 상황: 한 열 선택과 여러 열 선택의 반환 타입을 직접 확인하고 싶습니다.
입력(input): `df["score"]`와 `df[["name", "score"]]`.
기대 출력(output): `Series`, `DataFrame`이라는 타입 이름 두 줄.
확인할 개념: 같은 선택처럼 보여도 반환 객체는 달라질 수 있습니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
print(type(df["score"]).__name__)
print(type(df[["name", "score"]]).__name__)
```

출력은 대략 다음처럼 읽힙니다.

```text
Series
DataFrame
```

## `loc`는 라벨, `iloc`는 위치를 기준으로 읽는다

Pandas 공식 문서는 `.loc`를 라벨 기반(label-based) 선택으로, `.iloc`를 정수 위치 기반(integer position-based) 선택으로 설명합니다.

여기서는 다음처럼 구분합니다.

- `loc`: 이름표를 보고 고른다.
- `iloc`: 몇 번째 위치인지 보고 고른다.

예를 들어 현재 기본 인덱스가 `0, 1, 2, 3`일 때:

문제 상황: 기본 숫자 인덱스에서는 `loc`와 `iloc`가 비슷해 보여 차이를 놓치기 쉽습니다.
입력(input): `df.loc[1]`, `df.iloc[1]`.
기대 출력(output): 둘 다 두 번째 학생 행을 가리키는 출력.
확인할 개념: 지금 결과가 같아 보여도 기준은 라벨과 위치로 다릅니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
print(df.loc[1])
print(df.iloc[1])
```

둘 다 두 번째 행을 가리키는 것처럼 보일 수 있습니다. 지금은 인덱스 라벨도 숫자이고 위치도 숫자이기 때문입니다.

하지만 인덱스를 이름으로 바꾸면 차이가 더 분명해집니다.

문제 상황: 라벨 기준 선택과 위치 기준 선택의 차이를 더 분명하게 보고 싶습니다.
입력(input): `name`을 인덱스로 바꾼 `named`, 그리고 `loc`/`iloc` 호출.
기대 출력(output): `Lee` 라벨과 세 번째 위치가 각각 선택됩니다.
확인할 개념: `loc`는 이름표를 보고, `iloc`는 순서를 보고 고릅니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
named = df.set_index("name")

print(named.loc["Lee"])
print(named.iloc[2])
```

이때:

- `named.loc["Lee"]`는 `Lee`라는 라벨을 찾습니다.
- `named.iloc[2]`는 세 번째 위치의 행을 찾습니다.

이 구분은 매우 중요합니다. 표를 읽을 때 “이름으로 고르는가, 순서로 고르는가”가 다르기 때문입니다.

작은 표로 정리하면:

| 코드 | 기준 | 의미 |
| --- | --- | --- |
| `df.loc[1]` | 라벨 | 인덱스 라벨이 1인 행 |
| `df.iloc[1]` | 위치 | 두 번째 위치의 행 |
| `named.loc["Lee"]` | 라벨 | 이름이 `Lee`인 행 |
| `named.iloc[2]` | 위치 | 세 번째 위치의 행 |

## 조건 필터는 행을 남기거나 버린다

표를 읽을 때 가장 자주 하는 일 중 하나는 조건에 맞는 행만 남기는 것입니다.

문제 상황: 점수가 80 이상인 학생만 남기고 싶습니다.
입력(input): `df["score"] >= 80` 조건을 적용한 표.
기대 출력(output): Kim과 Lee만 남은 부분 표.
확인할 개념: 조건 필터는 행 값을 바꾸는 것이 아니라 남길 행을 고르는 일입니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
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

문제 상황: 필터가 내부적으로 어떤 `True`/`False` 목록을 만드는지 먼저 보고 싶습니다.
입력(input): `df["score"] >= 80`에서 만든 `mask`.
기대 출력(output): 각 행마다 조건 충족 여부가 적힌 불리언 `Series`.
확인할 개념: 필터링은 먼저 행별 판단 결과를 만들고, 그다음 `True`만 남깁니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
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

조건은 여러 개를 함께 쓸 수도 있습니다.

문제 상황: 점수와 지역 조건을 동시에 만족하는 행만 남기고 싶습니다.
입력(input): 점수 70 이상이면서 `region == "Busan"`인 복합 조건.
기대 출력(output): 조건을 둘 다 만족하는 Choi 행만 남은 표.
확인할 개념: 불리언 조건은 `&` 같은 연산자로 결합할 수 있습니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
print(df[(df["score"] >= 70) & (df["region"] == "Busan")])
```

이 코드는 점수가 70 이상이면서 지역이 Busan인 행만 남깁니다.

필터 전후를 표로 보면 다음처럼 읽을 수 있습니다.

| 단계 | 남는 행 |
| --- | --- |
| 원본 표 | Kim, Park, Lee, Choi |
| `df["score"] >= 80` | Kim, Lee |
| `(df["score"] >= 70) & (df["region"] == "Busan")` | Choi |

즉, 필터는 값을 바꾸기보다 `남길 행을 고르는 일`에 가깝습니다.

## 선택과 필터링은 질문 방식이 다르다

처음 배울 때는 선택과 필터링이 비슷해 보일 수 있습니다. 하지만 질문이 다릅니다.

| 작업 | 질문 |
| --- | --- |
| 열 선택 | 어떤 변수만 볼 것인가 |
| 행 선택 | 몇 번째 사례, 어떤 라벨의 사례를 볼 것인가 |
| 조건 필터 | 어떤 조건을 만족하는 사례만 남길 것인가 |

예를 들어:

문제 상황: 열 선택, 한 행 선택, 조건 필터가 표를 서로 다르게 좁힌다는 점을 한 번에 비교하고 싶습니다.
입력(input): `df[["name", "score"]]`, `df.loc[2]`, `df[df["passed"] == "yes"]`.
기대 출력(output): 열만 줄인 표, 한 행 출력, 조건에 맞는 여러 행 출력.
확인할 개념: 표를 좁히는 동작이라도 질문 방식에 따라 결과 형태가 달라집니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
print(df[["name", "score"]])
print(df.loc[2])
print(df[df["passed"] == "yes"])
```

이 세 코드는 모두 표를 좁히지만, 좁히는 기준이 서로 다릅니다.

- 첫 번째는 열을 줄입니다.
- 두 번째는 한 행을 집어 봅니다.
- 세 번째는 조건에 맞는 여러 행을 남깁니다.

이 차이를 구분해야 나중에 코드가 길어져도 무엇을 하고 있는지 놓치지 않습니다.

하나의 질문을 세 방식으로 읽어 보면 더 분명합니다.

문제 상황: 같은 데이터라도 열 선택, 행 선택, 조건 필터 후 열 선택이 어떻게 이어지는지 보고 싶습니다.
입력(input): 세 가지 다른 Pandas 선택 코드.
기대 출력(output): 목적에 따라 서로 다른 범위로 좁혀진 결과들.
확인할 개념: Pandas 코드는 질문을 작은 단계로 쪼개어 표 범위를 줄이는 방식입니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
print(df[["name", "score"]])
print(df.loc[2])
print(df[df["passed"] == "yes"][["name", "score"]])
```

이 세 줄은 각각 다음을 보여 줍니다.

- 열을 줄여서 본 표
- 한 사례만 떼어 본 행
- 조건에 맞는 사례만 남긴 뒤 필요한 열만 다시 본 표

## 집계는 표를 더 작은 요약으로 바꾼다

집계(aggregation)는 원래 표를 요약값으로 바꾸는 과정입니다.

예를 들어:

문제 상황: 전체 점수 열을 숫자 몇 개로 요약해 보고 싶습니다.
입력(input): `score` 열에 대한 평균, 최댓값, 개수 집계.
기대 출력(output): 점수 분포를 요약하는 세 개의 숫자.
확인할 개념: 집계는 여러 행을 더 작은 요약 결과로 압축합니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
print(df["score"].mean())
print(df["score"].max())
print(df["score"].count())
```

출력은 각각 다음 질문에 답합니다.

- 평균(mean): 점수의 중심은 어디쯤인가
- 최댓값(max): 가장 큰 값은 무엇인가
- 개수(count): 값이 몇 개 있는가

표 전체를 그대로 보는 대신, 숫자 몇 개로 요약하는 것이 집계의 핵심입니다.

이 절에서는 집계를 “통계를 계산한다”보다 더 넓게 봅니다. 집계는 `많은 행을 더 작은 수의 결과로 압축하는 일`로 이해하면 됩니다.

작은 예를 보면:

문제 상황: 평균 하나만 따로 출력하면 집계가 표를 어떻게 단순화하는지 더 쉽게 볼 수 있습니다.
입력(input): `df["score"].mean()`.
기대 출력(output): 점수 평균 하나.
확인할 개념: 집계 결과는 표 전체를 대체하지 않지만 중심을 빠르게 보여 줍니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
print(df["score"].mean())
```

```text
72.5
```

이 숫자 하나는 표 전체를 대체하지는 못합니다. 하지만 빠르게 중심값을 보는 데는 유용합니다.

집계를 한 번에 묶어 보면 다음처럼 읽을 수도 있습니다.

문제 상황: 평균, 최댓값, 개수를 한 번에 점검하고 싶습니다.
입력(input): `df["score"].agg(["mean", "max", "count"])`.
기대 출력(output): 여러 집계 결과가 묶인 작은 요약 출력.
확인할 개념: 하나의 열도 여러 집계 기준으로 동시에 읽을 수 있습니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
print(df["score"].agg(["mean", "max", "count"]))
```

출력은 대략 다음처럼 보일 수 있습니다.

```text
mean     72.5
max      90.0
count     4.0
dtype: float64
```

이 결과는 `score` 열 하나를 여러 방식으로 요약한 작은 표처럼 읽을 수 있습니다.

## `groupby`는 같은 범주끼리 묶고 나서 요약한다

Pandas 공식 문서는 `groupby`를 데이터를 어떤 기준으로 나눈 뒤, 각 그룹에 함수를 적용해 결합하는 흐름으로 설명합니다. 여기서는 `groupby`를 같은 값을 가진 행들끼리 먼저 묶고, 그 묶음마다 집계를 하는 방식으로 읽으면 됩니다.

예를 들어 지역별 평균 점수를 보고 싶다면:

문제 상황: 개별 학생 점수 대신 지역별 평균 점수로 질문 단위를 바꾸고 싶습니다.
입력(input): `region`으로 묶고 `score` 평균을 계산하는 `groupby` 코드.
기대 출력(output): Busan과 Seoul의 평균 점수가 따로 나온 요약 결과.
확인할 개념: `groupby`는 개별 행을 범주별 묶음으로 바꾼 뒤 그 묶음마다 집계합니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
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

즉, `groupby`는 단순 평균보다 “어떤 기준으로 나누어 본 평균인가”를 드러내는 도구입니다.

원래 표와 groupby 결과를 나란히 놓고 보면 변화가 더 잘 보입니다.

| 원래 표의 질문 | groupby 이후 질문 |
| --- | --- |
| 각 학생의 점수는 얼마인가 | 지역별 평균 점수는 얼마인가 |
| 행이 몇 개인가 | 범주가 몇 개인가 |
| 개별 사례를 본다 | 범주 요약을 본다 |

이 점이 중요합니다. `groupby`는 데이터를 정렬하는 기능이 아니라, `읽는 단위`를 개별 행에서 범주별 묶음으로 바꾸는 기능에 가깝습니다.

표를 읽을 때는 한 행이 곧바로 하나의 완성 사례가 아닐 수도 있습니다. 예를 들어 동작 중 기록된 원시 로그에서는 여러 행이 함께 하나의 동작 기록을 이루기도 합니다. 이때는 먼저 동작 식별자 열로 묶고, 그 안에서 길이, 구간 평균, 마지막 값 같은 정보를 요약해 동작 단위 표를 다시 만드는 편이 더 자연스럽습니다.

| event_id | elapsed_seconds | progress_fraction | signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 0.0 | 0.00 | 0.8 |
| A-01 | 1.0 | 0.20 | 1.4 |
| A-01 | 2.0 | 0.40 | 1.9 |
| B-02 | 0.0 | 0.00 | 0.7 |
| B-02 | 1.0 | 0.25 | 1.3 |
| B-02 | 2.0 | 0.50 | 1.5 |

| event_id | total_duration_seconds | signal_a_mean | end_signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 2.0 | 1.37 | 1.9 |
| B-02 | 2.0 | 1.17 | 1.5 |

문제 상황: 여러 행으로 기록된 원시 로그를 동작 단위 요약 표로 다시 바꾸고 싶습니다.
입력(input): `event_id`로 묶은 뒤, 시간 길이와 센서 값 요약을 계산하는 코드.
기대 출력(output): 각 `event_id`마다 한 행만 남는 요약 `DataFrame`.
확인할 개념: `groupby`는 같은 범주끼리 묶는 기능일 뿐 아니라, 여러 행을 한 사례 단위로 다시 읽게 만드는 도구이기도 합니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
log_df = pd.DataFrame(
    {
        "event_id": ["A-01", "A-01", "A-01", "B-02", "B-02", "B-02"],
        "elapsed_seconds": [0.0, 1.0, 2.0, 0.0, 1.0, 2.0],
        "progress_fraction": [0.00, 0.20, 0.40, 0.00, 0.25, 0.50],
        "signal_a": [0.8, 1.4, 1.9, 0.7, 1.3, 1.5],
    }
)

summary = (
    log_df.groupby("event_id")
    .agg(
        total_duration_seconds=("elapsed_seconds", "max"),
        signal_a_mean=("signal_a", "mean"),
        end_signal_a=("signal_a", "last"),
    )
    .reset_index()
)

print(summary)
```

출력은 다음처럼 읽을 수 있습니다.

```text
  event_id  total_duration_seconds  signal_a_mean  end_signal_a
0     A-01                     2.0       1.366667           1.9
1     B-02                     2.0       1.166667           1.5
```

## 임계값을 바꾸면 필터와 집계가 함께 움직인다

앞의 작은 표는 Pandas 문법을 읽기 위한 설명형 예제입니다. 하지만 실제 표에서는 조건값을 바꾸면 남는 행과 집계가 함께 달라지는지 확인해야 합니다.

입력 파일은 [`student-progress-samples.csv`](../../../assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview }입니다. 한 행은 학생 한 명의 학습 기록이고, 핵심 열은 `region`, `study_hours`, `absences`, `practice_quizzes`, `score`, `passed`입니다. 여기서는 `pass_threshold`와 `focus_region`을 바꾸며 어떤 행이 남고 지역별 요약이 어떻게 달라지는지 봅니다.

문제 상황: 점수 임계값과 지역 조건을 바꾸면 필터 결과와 지역별 요약이 함께 달라지는지 확인하고 싶습니다.
입력(input): 36행 학생 진행도 CSV, `pass_threshold`, `focus_region`.
기대 출력(output): 조건에 맞는 행 목록과 지역별 평균 점수, 임계값 이상 학생 수.
확인할 개념: 조건 필터와 `groupby` 집계는 고정 정답을 확인하는 코드가 아니라, 기준값을 바꿀 때 남는 행과 요약이 어떻게 움직이는지 관찰하는 도구입니다.

```python
# DataFrame에서 열, 행, 조건을 선택하고 점수 데이터를 집계하는 예제입니다.
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

같은 코드는 [`p2_12_2_filter_aggregate_threshold.py`](../../../assets/part-02/chapter-12/p2_12_2_filter_aggregate_threshold.py)로도 실행할 수 있습니다. `pass_threshold`를 `70`, `75`, `80`으로 바꾸면 임계값 이상 학생 수가 바뀌고, `focus_region`을 다른 지역으로 바꾸면 선택된 행 목록이 달라집니다.

## 표를 읽는 흐름을 도식으로 보면

선택, 필터링, 집계는 대개 다음 흐름으로 이어집니다.

```mermaid
--8<-- "assets/part-02/chapter-12/table-processing-flow-ko.mmd"
```

실제 작업에서는 이 순서가 항상 고정되지는 않습니다. 그래도 “표를 그대로 들고 있기보다, 질문에 맞게 점점 좁히고 요약한다”는 흐름은 계속 중요합니다.

## 선택, 필터링, 집계: 확인할 판단 기준

이 사례 절은 다음 질문으로 중심축을 확인한다.

- 오픈체크리스트의 중심축 문장인 "선택, 필터링, 집계가 데이터 읽기의 기본 조작이라는 점을 잡아야 합니다."를 본문 사례에서 어느 대목으로 확인할 수 있는가?
- 표, 코드, 도식, 체크리스트 중 어떤 장치가 이 판단을 다시 검토하게 만드는가?

### 사례 1. 불합격 학생만 다시 보고 싶은 성적표

교사가 성적표를 보고 `누가 불합격했는지`, `불합격 학생의 점수와 지역만 다시 보고 싶은지`, `지역별 평균 점수는 어떤지`를 확인한다고 해 보겠습니다. 사람은 머릿속으로 표를 훑으며 필요한 부분만 다시 볼 수 있지만, 데이터 작업에서는 그 과정을 선택, 필터링, 집계로 명시해야 합니다.

먼저 `passed` 열로 불합격 학생만 남기면 어떤 행을 볼지 정한 셈입니다. 그다음 `name`과 `score`만 다시 고르면 무엇을 읽을지 정한 셈입니다. 마지막으로 `groupby("region")["score"].mean()`을 하면 개별 학생 표를 지역별 요약으로 압축하게 됩니다.

이 사례는 세 동작의 차이를 한 번에 보여 줍니다. 열 선택은 `어떤 변수만 볼 것인가`, 행 선택과 필터링은 `어떤 사례를 남길 것인가`, 집계는 `전체를 어떤 요약값으로 읽을 것인가`를 정합니다. 표를 다루는 일은 단순히 코드를 외우는 것이 아니라, 질문을 더 작은 단계로 나누는 일에 가깝습니다.

그래서 Pandas 코드는 짧아 보여도 질문 구조를 함께 읽어야 합니다. 같은 성적표라도 `한 학생만 보기`, `조건에 맞는 여러 학생 보기`, `범주별 평균 보기`는 서로 다른 읽기 동작이며, 이 차이를 구분해야 이후 데이터셋 준비와 모델 입력 구성도 헷갈리지 않습니다.

## 체크리스트

- 한 열 선택과 여러 열 선택의 차이를 설명할 수 있는가?
- `loc`와 `iloc`가 각각 무엇을 기준으로 고르는지 말할 수 있는가?
- 불리언 조건이 행을 남기거나 버리는 방식임을 설명할 수 있는가?
- 평균, 개수, 최댓값 같은 집계가 왜 필요한지 설명할 수 있는가?
- `groupby`를 `묶고 나서 요약한다`는 흐름으로 설명할 수 있는가?
- 한 열 선택은 `Series`, 여러 열 선택은 `DataFrame`으로 읽는 경우가 많다는 점을 설명할 수 있는가?

## 출처와 참고 자료

- pandas Developers, [Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation, 확인 날짜: 2026-07-20. 열 선택, `loc`/`iloc`, 불리언 인덱싱과 행 필터링 설명 확인에 사용했다.
- pandas Developers, [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation, 확인 날짜: 2026-07-20. `groupby`를 split-apply-combine 흐름으로 설명하는 근거로 사용했다.
- pandas Developers, [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation, 확인 날짜: 2026-07-20. DataFrame 생성, 선택, 요약 통계, 기본 표 조작 예시 확인에 사용했다.

# P2-8.2 리스트(list): 순서가 있는 값 묶음

> Section ID: `P2-8.2`
> Version: `v2026.09.08`

## 순서와 인덱스

리스트(list)는 여러 값을 순서대로 담는 자료구조(data structure)입니다. 점수 목록, 문장 목록, 파일 목록에서 위치(index)로 특정 값을 꺼낼 수 있습니다.

점수 네 개 `82, 75, 91, 68`을 대괄호로 묶고 `scores`라는 이름을 붙입니다. 다음 코드는 `[82, 75, 91, 68]`과 타입 `<class 'list'>`를 출력합니다.

```python
scores = [82, 75, 91, 68]

print(scores)
print(type(scores))
```

Python 리스트 안의 각 값은 항목(item) 또는 원소(element)라고 부를 수 있습니다.

Python 리스트는 순서가 있으므로 위치(index)로 값을 꺼낼 수 있습니다.

리스트의 첫 번째 위치 번호는 `0`입니다. 다음 코드는 인덱스 `0`과 `1`의 값인 `82`, `75`를 차례로 출력합니다.

```python
scores = [82, 75, 91, 68]

print(scores[0])
print(scores[1])
```

음수 인덱스는 끝에서부터 셉니다. `-1`은 마지막 항목입니다.

| 표현 | 의미 | 값 |
| --- | --- | --- |
| `scores[0]` | 첫 번째 항목 | `82` |
| `scores[1]` | 두 번째 항목 | `75` |
| `scores[-1]` | 마지막 항목 | `68` |

## 리스트와 배열

다른 언어를 먼저 배운 사람은 리스트(list)를 배열(array)로 바로 이해할 수 있습니다. 둘 다 순서가 있고 위치(index)로 값을 꺼낼 수 있기 때문입니다.

Python 리스트는 여러 값을 담고 순서대로 다루는 일반 목적 컨테이너(container)에 가깝습니다. 반면 AI 수치 계산에서 말하는 배열(array)은 보통 같은 종류의 숫자를 일정한 구조로 놓고 빠르게 계산하기 위한 자료구조를 가리킵니다.

Python 공식 문서도 이 구분을 뒷받침합니다. `list`는 변경 가능한 시퀀스(mutable sequence)로 설명되고, 표준 라이브러리의 `array` 모듈은 숫자값을 효율적으로 담는 배열을 따로 제공합니다. `array`는 리스트처럼 동작하는 부분이 있지만, 담을 수 있는 값의 타입이 생성 시점의 type code로 제한됩니다.

혼동은 다차원 배열을 볼 때 더 커질 수 있습니다. Python에서도 리스트 안에 리스트를 넣으면 표처럼 보이는 구조를 만들 수 있습니다.

두 행 `[1, 2, 3]`, `[4, 5, 6]`을 리스트 하나에 넣으면 중첩 리스트(nested list)가 됩니다. 다음 코드는 전체 구조와 두 번째 행의 첫 값 `4`를 출력합니다.

```python
rows = [
    [1, 2, 3],
    [4, 5, 6],
]

print(rows)
print(rows[1][0])
```

이 모양은 행렬(matrix)이나 2차원 배열(two-dimensional array)처럼 보입니다. 하지만 이것은 여전히 “리스트 안에 리스트가 들어 있는 구조”입니다. NumPy의 다차원 배열(`ndarray`)은 shape, axis, dtype 같은 정보를 가진 계산 구조이며, NumPy 문서도 `ndarray`를 N차원 배열로 설명합니다. 따라서 “중첩 리스트가 행렬처럼 보인다”와 “중첩 리스트가 수치 계산용 다차원 배열이다”는 구분해야 합니다.

| 관점 | Python 리스트(list) | 수치 계산에서의 배열(array) 관점 |
| --- | --- | --- |
| 중심 생각 | 순서가 있는 값 묶음 | 같은 종류의 수치를 구조적으로 담는 계산 대상 |
| 주된 용도 | 샘플 목록, 파일 이름, 텍스트 목록처럼 여러 대상을 보관 | 벡터, 행렬, 모델 입력처럼 숫자 계산을 수행 |
| 값의 종류 | 서로 다른 타입도 담을 수 있지만, 보통 같은 목적의 값을 묶음 | 보통 같은 수치 타입을 기대함 |
| 변경 방식 | 값을 추가하거나 줄이기 쉬움 | 크기, 축(axis), 연산 방식이 더 중요해짐 |

## 자료구조의 선택

Python 리스트의 설계는 “순서가 있는 값을 담고, 필요하면 끝에 추가하거나 꺼내며, 반복해서 처리하기 쉬운 변경 가능한 시퀀스(mutable sequence)”로 이해할 수 있습니다. Python 공식 튜토리얼도 리스트 메서드, 스택(stack)처럼 쓰는 방식, 큐(queue)로 쓸 때의 한계, 딕셔너리(dictionary), 집합(set), 튜플(tuple)을 분리해서 설명합니다.

즉 리스트는 모든 묶음을 대신하는 구조가 아닙니다. 무엇을 기준으로 값을 다룰지에 따라 다른 구조를 선택합니다.

| 구조 | 중심 질문 | 리스트와의 차이 |
| --- | --- | --- |
| 리스트(list) | 순서대로 여러 값을 담고 하나씩 처리할 것인가? | 위치(index)와 순서가 중요하고, 값을 추가하거나 바꿀 수 있음 |
| 튜플(tuple) | 바뀌지 않는 묶음으로 둘 것인가? | 튜플은 immutable sequence로, 고정된 값 묶음에 더 가깝게 쓰임 |
| 딕셔너리(dictionary) | 이름이나 키(key)로 값을 찾을 것인가? | 위치가 아니라 키로 값에 접근함 |
| 집합(set) | 중복 없는 원소와 포함 여부가 중요한가? | 순서보다 유일성과 membership test가 중요함 |
| 덱(deque) | 양쪽 끝에서 자주 넣고 뺄 것인가? | 큐처럼 앞에서 자주 꺼내야 하면 리스트보다 `collections.deque`가 더 적합함 |
| 배열(array) | 같은 종류의 수치를 구조적으로 계산할 것인가? | 수치 타입, shape, axis, 계산 방식이 중요함 |

## 항목 변경과 참조

리스트는 항목을 추가하거나 바꿀 수 있는 변경 가능한 시퀀스(mutable sequence)입니다.

점수 목록 끝에 `68`을 추가하고 두 번째 점수를 `75`에서 `77`로 바꿉니다. 결과는 `[82, 77, 91, 68]`입니다.

```python
scores = [82, 75, 91]

scores.append(68)
scores[1] = 77

print(scores)
```

`append()`는 리스트 끝에 값을 추가합니다. `scores[1] = 77`은 두 번째 항목을 바꿉니다.

`other_scores = scores`는 리스트를 복사하지 않고 같은 리스트에 이름을 하나 더 붙입니다. `other_scores`로 `68`을 추가하면 두 출력 모두 `[82, 75, 91, 68]`이 됩니다.

```python
scores = [82, 75, 91]
other_scores = scores

other_scores.append(68)

print(scores)
print(other_scores)
```

`scores`와 `other_scores`는 서로 다른 리스트를 복사한 것이 아니라 같은 리스트를 가리킵니다. 그래서 한쪽 이름으로 값을 추가하면 다른 이름으로 봐도 같은 변경이 보입니다.

## 연결·슬라이스·삭제

Python 리스트를 읽다 보면 함수 이름보다 기호와 대괄호 문법이 먼저 보일 때가 많습니다. 다른 언어에서 `concat`, `join`, `slice`, `splice` 같은 이름으로 만났던 동작이 Python에서는 연산자(operator), 슬라이스(slice), 대입문(assignment), `del` 문으로 표현되기도 합니다.

### 연결

두 리스트를 붙여 새 리스트를 만들 때는 `+`를 사용할 수 있습니다. 이미 있는 리스트 끝에 다른 값을 이어 붙이고 싶다면 `extend()`를 사용할 수 있습니다.

`[1, 2] + [3, 4]`는 새 리스트 `[1, 2, 3, 4]`를 만들고 `front`는 `[1, 2]`로 남습니다. 반면 `extend()`는 기존 `scores`를 `[82, 75, 91, 68]`로 바꿉니다.

```python
front = [1, 2]
back = [3, 4]

combined = front + back
print("combined:", combined)
print("front after +:", front)

scores = [82, 75]

scores.extend([91, 68])
print("scores after extend:", scores)
```

`+`는 붙인 결과를 새로 만들고, `extend()`는 기존 리스트를 바꿉니다.

### 슬라이스

리스트의 일부 구간만 꺼낼 때는 슬라이스(slice)를 사용합니다.

점수 다섯 개에서 중간 구간, 앞 두 개, 뒤쪽 구간을 꺼냅니다. 다음 코드는 `[75, 91, 68]`, `[82, 75]`, `[68, 88]`을 차례로 출력합니다.

```python
scores = [82, 75, 91, 68, 88]

print(scores[1:4])
print(scores[:2])
print(scores[3:])
```

`scores[1:4]`는 인덱스 1부터 4 바로 앞까지 꺼냅니다. 그래서 결과는 `[75, 91, 68]`입니다. 끝 인덱스 `4`의 값 `88`은 포함되지 않습니다.

리스트의 슬라이스는 선택한 항목을 담은 새 리스트를 만듭니다.

### 삭제와 구간 교체

다른 언어의 `splice`처럼 리스트의 중간 구간을 지우거나 바꾸는 동작은 Python에서 별도 `splice()` 메서드로 제공되지 않습니다. 비슷한 목적은 `del`, `insert()`, 슬라이스 대입(slice assignment)으로 표현합니다.

`["A", "B", "C", "D"]`에서 인덱스 `1`부터 `3` 직전까지 삭제하면 `['A', 'D']`가 출력됩니다.

```python
items = ["A", "B", "C", "D"]

del items[1:3]

print(items)
```

`del items[1:3]`은 인덱스 1부터 3 바로 앞까지 지웁니다. 결과는 `["A", "D"]`입니다.

구간을 다른 값으로 바꿀 수도 있습니다.

가운데 두 항목 `"B"`, `"C"`를 세 항목 `"X"`, `"Y"`, `"Z"`로 바꿉니다. 결과는 `['A', 'X', 'Y', 'Z', 'D']`이며 길이가 4에서 5로 늘어납니다.

```python
items = ["A", "B", "C", "D"]

items[1:3] = ["X", "Y", "Z"]

print(items)
```

결과는 `["A", "X", "Y", "Z", "D"]`입니다. 구간을 같은 길이로만 바꿔야 하는 것은 아닙니다.

### 문자열 연결: join

`join`은 Python에서 자주 보이지만, 리스트 메서드가 아닙니다. 문자열(str)이 문자열 목록을 하나의 문자열로 연결할 때 사용하는 메서드입니다.

문자열 목록 `["AI", "needs", "data"]`를 공백으로 연결하면 `AI needs data`가 출력됩니다. `" ".join(words)`에서 공백 문자열이 구분자입니다.

```python
words = ["AI", "needs", "data"]

sentence = " ".join(words)

print(sentence)
```

결과는 `"AI needs data"`입니다. 여기서 동작의 주체는 리스트가 아니라 `" "`라는 문자열입니다. 이 문자열이 `words` 안의 문자열들을 사이에 공백을 넣어 이어 붙입니다.

따라서 Python에서 리스트를 읽을 때는 다음처럼 구분하는 편이 안전합니다.

| 하고 싶은 일 | Python에서 자주 보이는 표현 | 주의할 점 |
| --- | --- | --- |
| 리스트 두 개를 붙인다 | `front + back` | 새 리스트를 만듦 |
| 기존 리스트 끝에 이어 붙인다 | `items.extend(values)` | 기존 리스트를 바꿈 |
| 일부 구간을 읽는다 | `items[1:4]` | 끝 인덱스는 포함하지 않음 |
| 일부 구간을 지운다 | `del items[1:4]` | 기존 리스트를 바꿈 |
| 일부 구간을 바꾼다 | `items[1:4] = values` | 길이가 달라도 바꿀 수 있음 |
| 문자열 목록을 하나의 문자열로 합친다 | `" ".join(words)` | `join()`은 문자열 메서드임 |

## 리스트 초기화

초기화(initialize)는 자료구조를 처음 만드는 일입니다. 값이 준비되어 있는지, 나중에 모을지에 따라 시작 형태를 고릅니다.

### 이미 값을 알고 있을 때

처음부터 들어갈 값을 알고 있다면 대괄호(`[]`) 안에 값을 적습니다.

들어갈 값을 이미 알고 있다면 대괄호 안에 직접 적습니다. 다음 코드는 점수, 라벨, 참거짓 목록을 각각 입력한 순서대로 출력합니다.

```python
scores = [82, 75, 91, 68]
labels = ["positive", "negative", "neutral"]
flags = [True, False, True]

print(scores)
print(labels)
print(flags)
```

이 방식은 학습용 예시나 작은 설정 목록을 만들 때 값의 구성을 가장 직접적으로 드러냅니다.

### 빈 리스트로 시작할 때

값이 없지만 나중에 값을 담을 예정이라면 빈 리스트로 시작할 수 있습니다.

빈 리스트 `[]`에 점수 `82`, `75`를 하나씩 추가하면 `[82, 75]`가 출력됩니다. 수집할 값이 생길 때마다 `append()`를 실행하는 방식입니다.

```python
passed_scores = []

passed_scores.append(82)
passed_scores.append(75)

print(passed_scores)
```

이 예시는 리스트가 만든 뒤에도 값을 추가할 수 있음을 보여 줍니다. 실제 데이터 처리에서는 반복(loop)을 사용해 조건에 맞는 값을 빈 리스트에 모으는 일이 많습니다.

### 같은 값으로 길이를 맞춰 시작할 때

필요한 길이를 알고 있고, 일단 같은 값으로 채워 두고 싶을 때도 있습니다.

기본값 `0`을 다섯 번 나열하려면 `[0] * 5`로 시작할 수 있습니다. 출력은 `[0, 0, 0, 0, 0]`입니다.

```python
predictions = [0] * 5

print(predictions)
```

이 코드는 `[0, 0, 0, 0, 0]`을 만듭니다. 다만 이 방식은 숫자나 문자열처럼 단순한 값에는 이해하기 쉽지만, 리스트 안에 리스트를 넣는 경우에는 조심해야 합니다.

`[[]] * 3`은 안쪽 빈 리스트 하나를 세 위치에서 가리킵니다. 첫 위치의 리스트에 `"A"`를 추가하면 출력은 `[['A'], ['A'], ['A']]`입니다.

```python
rows = [[]] * 3

rows[0].append("A")

print(rows)
```

세 행을 따로 바꾸려면 안쪽 리스트도 각각 만들어야 합니다. `rows = [[], [], []]`로 바꿔 실행하면 결과는 `[['A'], [], []]`입니다. 첫 행만 바뀝니다.

## 점수·문장·파일 목록

리스트는 같은 목적이나 맥락의 값들이 순서대로 모여 있고, 위치나 순서가 의미를 가질 때 사용합니다.

### 점수 여러 개

점수 `[82, 75, 91, 68]`의 최댓값은 `91`, 최솟값은 `68`, 평균은 `79.0`입니다. `sum()`은 합계, `len()`은 항목 수를 구하므로 두 결과를 나누면 평균이 됩니다.

```python
scores = [82, 75, 91, 68]

print(max(scores))
print(min(scores))
print(sum(scores) / len(scores))
```

점수 목록은 순서가 있을 수도 있고, 전체를 모아 평균을 낼 수도 있습니다.

### 문장 여러 개

문장 세 개를 리스트에 담고 `for`로 순서대로 꺼냅니다. `text`는 각 문장을 차례로 가리키며, 세 문장이 한 줄씩 출력됩니다.

```python
texts = [
    "AI is useful.",
    "Data quality matters.",
    "Models can fail.",
]

for text in texts:
    print(text)
```

LLM이나 텍스트 분류 실습에서는 문장 목록을 자주 만납니다.

### 모델 출력 여러 개

모델 점수 `[0.92, 0.31, 0.77, 0.12]`를 기준 `0.8`과 비교합니다. 첫 값만 기준 이상이므로 `above threshold` 한 번과 `check` 세 번이 출력됩니다.

```python
probabilities = [0.92, 0.31, 0.77, 0.12]

for probability in probabilities:
    if probability >= 0.8:
        print("above threshold")
    else:
        print("check")
```

기준을 `0.7`로 바꾸면 세 번째 값 `0.77`도 통과하여 `above threshold`가 두 번 출력됩니다. 이 표시는 설정한 기준을 통과했다는 뜻이며 예측의 정확성을 보증하지는 않습니다.

### 파일 이름 여러 개

다음 코드는 파일 이름 세 개를 리스트에서 하나씩 꺼내 `train.csv`, `valid.csv`, `test.csv`를 차례로 출력합니다. 파일 자체를 읽는 코드는 아닙니다.

```python
file_names = [
    "train.csv",
    "valid.csv",
    "test.csv",
]

for file_name in file_names:
    print(file_name)
```

프로젝트 실습에서는 여러 파일을 같은 방식으로 처리해야 하는 경우가 많습니다.

## 사례: 세 번째 예측 점수 확인

네 입력의 예측 점수를 입력 순서대로 `[0.92, 0.31, 0.77, 0.12]`에 담았다고 하겠습니다. 세 번째 입력의 점수는 인덱스 `2`의 값 `0.77`입니다. 새 입력의 점수 `0.85`를 끝에 추가하면 기존 네 값의 위치는 유지되고 항목 수가 `5`가 됩니다.

```python
probabilities = [0.92, 0.31, 0.77, 0.12]
print(probabilities[2])

probabilities.append(0.85)
print(probabilities)
print(len(probabilities))
```

출력은 `0.77`, `[0.92, 0.31, 0.77, 0.12, 0.85]`, `5`입니다. 입력과 예측 결과를 위치로 대응시킨다면 한쪽 목록만 순서를 바꾸지 않아야 합니다. 예측 점수만 크기순으로 재배열하면 세 번째 위치의 점수가 더 이상 세 번째 입력의 결과를 뜻하지 않을 수 있습니다.

## 체크리스트

- 리스트(list)를 순서가 있는 값 묶음으로 설명할 수 있다.
- `scores[0]`, `scores[-1]`의 의미를 설명할 수 있다.
- 이미 값을 알고 시작하는 리스트, 빈 리스트, 같은 값으로 채운 리스트를 구분할 수 있다.
- `append()`로 값을 추가하는 흐름을 읽을 수 있다.
- `+`, `extend()`, 슬라이스(slice), `del`, 슬라이스 대입의 차이를 대략적으로 구분할 수 있다.
- `join()`은 리스트 메서드가 아니라 문자열(str) 메서드임을 설명할 수 있다.
- Python 리스트에는 JavaScript식 `splice()` 메서드가 없으며, 비슷한 작업은 `del`, `insert()`, 슬라이스 대입으로 표현함을 설명할 수 있다.
- 같은 리스트를 여러 이름이 가리킬 수 있음을 설명할 수 있다.
- 중첩 리스트를 같은 값 반복으로 만들 때 주의가 필요함을 설명할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 리스트 메서드, 리스트를 스택처럼 쓰는 예, 리스트 컴프리헨션과 중첩 리스트 예시 확인에 사용했다.
- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 시퀀스 타입과 mutable sequence 연산, 인덱싱·슬라이싱 동작 확인에 사용했다.
- Python Software Foundation, [array — Efficient arrays of numeric values](https://docs.python.org/3/library/array.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Python 표준 라이브러리의 `array`가 같은 기본 타입의 값을 효율적으로 저장하는 구조라는 설명 확인에 사용했다.
- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual, 확인 날짜: 2026-07-20. NumPy 배열이 Python 리스트와 다르게 빠르고 많은 숫자 데이터를 다루는 핵심 구조라는 설명 확인에 사용했다.

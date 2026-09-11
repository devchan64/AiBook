# P2-8.4 반복(loop): 이터러블(iterable)을 하나씩 처리하기

> Section ID: `P2-8.4`
> Version: `v2026.09.08`

점수 네 개에 같은 기준을 적용하려면 각 점수를 꺼내 비교해야 합니다. 반복(loop)은 이 처리를 항목마다 실행하여 결과를 출력하거나, 필요한 값만 모으거나, 합계와 개수를 계산합니다.

## for와 항목 처리

`for score in scores:`는 `scores`에서 값을 하나씩 꺼내 `score`라는 이름으로 사용합니다. 콜론(`:`) 아래 들여쓴 코드가 각 항목에 적용되는 처리입니다. 다음 코드는 `82`, `75`, `91`, `68`을 한 줄씩 출력합니다.

```python
scores = [82, 75, 91, 68]

for score in scores:
    print(score)
```

`print(score)`가 네 번 실행되므로 출력도 네 줄입니다. 들여쓰기는 반복에 포함되는 코드의 범위를 정합니다.

위치 번호로도 같은 값을 꺼낼 수 있습니다. `len(scores)`는 항목 수 `4`이고, `range(4)`는 `0`부터 `3`까지의 번호를 차례로 제공합니다. 아래 출력은 앞의 코드와 같습니다.

```python
scores = [82, 75, 91, 68]

for i in range(len(scores)):
    print(scores[i])
```

값만 필요하면 `for score in scores`로 직접 꺼낼 수 있습니다. 위치와 값이 모두 필요할 때는 `enumerate()`를 사용합니다.

## 위치·키·두 목록의 대응

### 위치와 값: enumerate

`enumerate(scores)`는 위치 번호와 값을 함께 제공합니다. 다음 출력은 `0 82`, `1 75`, `2 91`, `3 68`입니다.

```python
scores = [82, 75, 91, 68]

for index, score in enumerate(scores):
    print(index, score)
```

`index, score`는 한 쌍으로 나온 두 값을 각각 받습니다. 오류가 난 샘플의 위치를 기록할 때처럼 값과 위치를 함께 확인하는 데 사용합니다.

### 키와 값: items

딕셔너리의 `.items()`는 키와 값을 함께 제공합니다. 다음 코드는 지표 이름과 값을 `accuracy 0.91`, `loss 0.32`로 출력합니다.

```python
metrics = {"accuracy": 0.91, "loss": 0.32}

for name, value in metrics.items():
    print(name, value)
```

`for name in metrics`라고 쓰면 키만 하나씩 받습니다. `.items()`를 사용하면 연결된 값까지 함께 받습니다.

### 두 목록: zip

`zip()`은 여러 반복 대상에서 항목을 하나씩 받아 한 쌍으로 묶습니다. 다음 코드는 문장과 라벨을 `good positive`, `bad negative`, `great positive`로 출력합니다.

```python
texts = ["good", "bad", "great"]
labels = ["positive", "negative", "positive"]

for text, label in zip(texts, labels):
    print(text, label)
```

두 목록은 같은 위치끼리 대응합니다. `zip()`은 문장 내용에 맞는 라벨을 찾아 주지 않습니다.

기본 `zip()`은 짧은 목록이 끝나면 멈춥니다. 위 `labels`를 `["positive", "negative"]`로 줄이면 앞의 두 쌍만 출력되고 `great`는 처리되지 않습니다. 길이가 같아야 하는 데이터라면 `zip(texts, labels, strict=True)`로 바꿀 수 있습니다. 이 경우 앞의 두 쌍을 처리한 뒤 길이 차이를 만나면 `ValueError`가 발생합니다.

## 이터러블과 이터레이터

이터러블(iterable)은 반복 가능한 객체입니다. 리스트와 문자열뿐 아니라 딕셔너리, 파일 객체, 값을 필요할 때 생성하는 생성기(generator)도 반복 대상이 될 수 있습니다. 파일은 줄을, 딕셔너리는 키를 내보내므로 모든 반복 대상에 정수 인덱스가 필요한 것은 아닙니다.

이터레이터(iterator)는 다음 항목을 제공하며 반복이 어디까지 진행됐는지를 유지하는 객체입니다. `iter()`로 이터레이터를 만들고 `next()`로 다음 값을 받습니다. 다음 코드는 리스트 `[82, 75]`에서 `82`, `75`를 차례로 꺼낸 뒤, 더 꺼낼 값이 없으면 지정한 기본값 `end`를 출력합니다.

```python
scores = [82, 75]
iterator = iter(scores)

print(next(iterator))
print(next(iterator))
print(next(iterator, "end"))
```

기본값 없이 다시 `next(iterator)`를 호출하면 `StopIteration`이 발생합니다. `for` 문은 이터레이터에서 값을 받고, 값이 끝났다는 신호를 만나면 반복을 마칩니다.

| 용어 | 역할 | 예시 |
| --- | --- | --- |
| 이터러블 | 반복 대상 | `scores` |
| 이터레이터 | 다음 값을 제공하고 진행 상태를 유지 | `iter(scores)`의 결과 |
| 반복문 | 받은 값에 처리를 적용 | `for score in scores` |

2001년에 작성된 PEP 234는 객체가 반복 방식을 제공하는 인터페이스를 제안했습니다. Python 2.2 시기의 이 제안은 시퀀스 중심 반복을 넘어 여러 객체를 같은 `for` 문으로 처리하는 배경이 되었습니다.

## 필터링과 변환

### 조건에 맞는 값 선택

다음 데이터에서는 `0`을 미입력 점수로 기록했다고 가정합니다. `score != 0`은 점수가 0이 아닌지 검사합니다. 조건을 만족하는 값만 빈 리스트에 추가하면 `[82, 75, 91]`이 출력됩니다.

```python
scores = [82, 0, 75, 0, 91]
valid_scores = []

for score in scores:
    if score != 0:
        valid_scores.append(score)

print(valid_scores)
```

`if` 아래 들여쓴 `append()`는 조건이 참인 경우에만 실행됩니다. 실제 0점이 가능한 데이터라면 이 조건은 정상 점수까지 제거하므로 미입력을 구분할 다른 표시가 필요합니다.

### 모든 값에 같은 변환 적용

100점 만점 점수를 100으로 나누면 0부터 1 사이의 값으로 표현할 수 있습니다. `[82, 75, 91, 68]`을 변환한 출력은 `[0.82, 0.75, 0.91, 0.68]`입니다.

```python
scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(score / 100)

print(normalized_scores)
```

원본 점수는 그대로 두고 변환 결과를 `normalized_scores`에 모읍니다. 이처럼 같은 규칙을 적용하는 반복은 문자열을 소문자로 바꾸거나 앞뒤 공백을 지울 때도 사용합니다.

## 컴프리헨션

컴프리헨션(comprehension)은 반복으로 새 자료구조를 만드는 축약 표현입니다. `[결과 표현식 for 변수 in 반복 대상]`의 형태로 새 리스트를 만듭니다.

`range(5)`에서 나온 `0`부터 `4`까지 각 수를 제곱하면 `[0, 1, 4, 9, 16]`이 출력됩니다.

```python
squares = [number * number for number in range(5)]

print(squares)
```

끝에 조건을 붙이면 해당 항목만 새 리스트에 넣습니다. 다음 출력은 앞의 미입력 점수 필터링과 같은 `[82, 75, 91]`입니다.

```python
scores = [82, 0, 75, 0, 91]

valid_scores = [score for score in scores if score != 0]

print(valid_scores)
```

점수를 100으로 나누는 반복도 줄일 수 있습니다. 아래 코드는 `[82, 75, 91]`을 변환해 `[0.82, 0.75, 0.91]`을 출력합니다.

```python
scores = [82, 75, 91]

normalized_scores = [score / 100 for score in scores]

print(normalized_scores)
```

| 부분 | 의미 |
| --- | --- |
| `scores` | 입력 목록 |
| `score` | 하나씩 꺼낸 점수 |
| `score / 100` | 새 리스트에 넣을 값 |

중괄호 안에 `키: 값`을 쓰면 딕셔너리를 만들 수 있습니다. 다음 결과는 `{'negative': 0, 'positive': 1, 'neutral': 2}`입니다.

```python
labels = ["negative", "positive", "neutral"]

label_to_id = {label: index for index, label in enumerate(labels)}

print(label_to_id)
```

조건과 중간 계산을 분리해서 설명해야 한다면 일반 `for` 문을 사용할 수 있습니다. 아래 입력에서 `82`와 `91`만 기준 `60`을 통과하므로 `[0.82, 0.91]`이 출력됩니다.

```python
items = [{"score": 82}, {"score": 55}, {"score": 91}]
results = []

for item in items:
    if item["score"] >= 60:
        normalized_score = item["score"] / 100
        results.append(normalized_score)

print(results)
```

## 합계와 키별 개수

### 합계 누적

누적(accumulation)은 현재까지의 결과에 새 값을 반영하는 계산입니다. 점수 `[82, 75, 91, 68]`을 `total = 0`부터 더하면 최종 합계 `316`이 출력됩니다.

```python
scores = [82, 75, 91, 68]
total = 0

for score in scores:
    total = total + score

print(total)
```

`total = total + score`는 이전 합계에 현재 점수를 더한 값을 다시 `total`에 할당합니다.

| 현재 점수 | 더하기 전 total | 더한 뒤 total |
| --- | --- | --- |
| 82 | 0 | 82 |
| 75 | 82 | 157 |
| 91 | 157 | 248 |
| 68 | 248 | 316 |

### 조건별 분리

점수 `[82, 55, 91, 42, 68]`을 기준 `60` 이상과 미만으로 나눕니다. 출력은 통과 목록 `[82, 91, 68]`과 미통과 목록 `[55, 42]`입니다.

```python
scores = [82, 55, 91, 42, 68]
passed = []
failed = []

for score in scores:
    if score >= 60:
        passed.append(score)
    else:
        failed.append(score)

print(passed)
print(failed)
```

`if`의 조건이 거짓이면 `else` 아래 처리를 실행합니다. 기준을 `70`으로 올리면 `68`이 미통과 목록으로 이동하여 결과는 `[82, 91]`과 `[55, 42, 68]`이 됩니다.

### 라벨별 개수

라벨별 등장 횟수를 딕셔너리에 쌓을 수 있습니다. 아래 목록에는 `positive`가 3개, `negative`와 `neutral`이 각각 1개 있습니다. 출력은 `{'positive': 3, 'negative': 1, 'neutral': 1}`입니다.

```python
labels = ["positive", "negative", "positive", "neutral", "positive"]
label_counts = {}

for label in labels:
    label_counts[label] = label_counts.get(label, 0) + 1

print(label_counts)
```

처음 만난 라벨은 `get(label, 0)`에서 `0`을 받아 개수를 `1`로 저장합니다. 같은 라벨을 다시 만나면 기존 개수에 `1`을 더합니다.

## 사례: 통과한 학생 이름 모으기

학생 Kim은 82.5점, Lee는 55점, Park은 91점입니다. 학생 정보는 딕셔너리로, 세 학생의 목록은 리스트로 표현합니다. 기준 `60` 이상인 학생의 이름만 모으면 `['Kim', 'Park']`가 출력됩니다.

```python
students = [
    {"name": "Kim", "score": 82.5},
    {"name": "Lee", "score": 55.0},
    {"name": "Park", "score": 91.0},
]

passed_students = []

for student in students:
    if student["score"] >= 60:
        passed_students.append(student["name"])

print(passed_students)
```

반복문은 학생 딕셔너리를 하나씩 받고, `student["score"]`로 점수를 확인한 뒤, 조건에 맞는 학생의 `"name"`을 결과에 추가합니다. 기준을 `90`으로 바꾸면 `['Park']`만 남습니다.

## 반복 중 항목 삭제

리스트를 순회하면서 항목을 삭제하면 뒤의 항목이 앞으로 이동하여 일부 항목을 건너뛸 수 있습니다. 다음 코드는 0을 모두 지우려 하지만, 연속한 두 0 중 하나가 남아 `[82, 0, 91]`을 출력합니다.

```python
scores = [82, 0, 0, 91]

for score in scores:
    if score == 0:
        scores.remove(score)

print(scores)
```

첫 0을 지우면 다음 0이 그 자리로 당겨집니다. 반복은 다음 위치로 진행하므로 당겨진 0은 검사하지 않습니다. 원본을 보존하고 결과를 새로 모으면 이 문제를 피할 수 있습니다. 다음 코드는 같은 입력에서 `[82, 91]`을 출력합니다.

```python
scores = [82, 0, 0, 91]
filtered_scores = []

for score in scores:
    if score != 0:
        filtered_scores.append(score)

print(filtered_scores)
print(scores)
```

두 번째 출력인 원본은 `[82, 0, 0, 91]`로 유지됩니다. 0을 미입력으로 사용하는 데이터라는 가정은 필터링 예제와 같습니다.

## 문장 길이 계산

문장 목록의 각 항목에 `len()`을 적용하면 문자 수 목록을 만들 수 있습니다. 아래 예시에서는 공백을 포함하여 `[12, 15, 12]`가 출력됩니다.

```python
texts = ["AI is useful", "Models can fail", "Data matters"]
lengths = []

for text in texts:
    lengths.append(len(text))

print(lengths)
```

입력 문장 순서와 출력 길이 순서는 같습니다. `lengths[1]`의 `15`는 두 번째 문장 `"Models can fail"`의 길이입니다.

## 체크리스트

- `for item in items` 반복을 읽고 실행 흐름을 설명할 수 있다.
- 이터러블(iterable)과 이터레이터(iterator)를 입문 수준에서 구분할 수 있다.
- iterable이라는 표현이 시퀀스뿐 아니라 딕셔너리, 파일, generator처럼 값을 하나씩 내보낼 수 있는 대상을 포괄하기 위한 말임을 설명할 수 있다.
- 위치가 필요할 때 `enumerate()`를 사용할 수 있음을 설명할 수 있다.
- 딕셔너리의 키와 값을 함께 볼 때 `.items()`를 사용할 수 있음을 설명할 수 있다.
- 두 묶음을 나란히 볼 때 `zip()`을 만날 수 있음을 설명할 수 있다.
- 항목 반복, 변환 반복, 누적 반복, 조건 분리 반복을 구분할 수 있다.
- 리스트 컴프리헨션과 딕셔너리 컴프리헨션을 반복으로 새 자료구조를 만드는 표현으로 읽을 수 있다.
- 컴프리헨션이 복잡해지면 일반 `for` 문이 더 적합할 수 있음을 설명할 수 있다.
- 반복 중 원본 데이터를 직접 바꾸는 일이 문제를 만들 수 있음을 설명할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. `for`, `range()`, 함수 정의 예시와 제어 흐름 설명을 반복 문법의 공식 근거로 사용했다.
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 리스트 컴프리헨션, 딕셔너리 순회, `items()` 예시와 반복 중 컬렉션 수정 주의 설명 확인에 사용했다.
- Python Software Foundation, [Glossary: iterable, iterator](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. iterable과 iterator 용어를 입문 수준으로 구분하는 근거로 사용했다.
- Python Software Foundation, [The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. `for` 문이 이터러블 표현식의 이터레이터에서 항목을 하나씩 대입한다는 설명 확인에 사용했다.
- Ka-Ping Yee, Guido van Rossum, [PEP 234 -- Iterators](https://peps.python.org/pep-0234/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals, 2001, 확인 날짜: 2026-07-20. Python 반복 인터페이스가 시퀀스 중심 반복을 넘어 객체가 반복 방식을 제공하는 방향으로 정리된 역사적 배경 확인에 사용했다.

- Python Software Foundation, [Built-in Functions: iter, next, zip](https://docs.python.org/3/library/functions.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, 확인 날짜: 2026-09-08. 이터레이터의 종료와 기본값, zip의 길이 차이 처리 및 strict 옵션을 확인했다.

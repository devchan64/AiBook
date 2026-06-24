# P2-8.4 반복(loop): 이터러블(iterable)을 하나씩 처리하기

P2-8.2에서는 리스트(list)를, P2-8.3에서는 딕셔너리(dictionary)를 봤습니다. 이제 이런 묶음을 하나씩 처리하는 반복(loop)을 분리해서 봅니다.

Python의 반복은 “몇 번 반복한다”보다 “무엇에서 무엇을 하나씩 꺼내는가”로 읽을 때 구조가 분명해집니다. 이 절에서는 이터러블(iterable), 이터레이터(iterator), 반복 패턴을 기본 개념 수준에서 정리합니다.

반복은 Python에만 있는 문법이 아닙니다. 데이터 처리, 통계 계산, 모델 평가에서는 거의 항상 여러 항목을 같은 기준으로 차례대로 처리합니다. Python의 `for`는 그 일반 흐름을 읽기 쉬운 형태로 보여 주는 예시입니다.

## 이 절의 범위

이 절은 Python에서 자주 보이는 반복 구조를 다룹니다. 중심 질문은 “묶음에서 값을 하나씩 꺼내 무엇을 만들거나 확인하는가”입니다.

여기서는 다음 질문에 답합니다.

- Python의 `for` 반복은 왜 항목 중심으로 읽는가?
- 이터러블(iterable)과 이터레이터(iterator)는 어떤 감각을 주는가?
- 항목 반복, 위치 반복, 키-값 반복, 병렬 반복, 필터링 반복은 어떻게 다른가?
- 반복하면서 새 리스트나 딕셔너리를 만드는 패턴은 어떻게 읽는가?
- Python은 왜 반복을 리스트나 딕셔너리 정의 안에 넣는 표현을 자주 쓰는가?
- P2-8.2에서 본 빈 리스트와 P2-8.3에서 본 딕셔너리가 반복과 만나면 어떤 모양이 되는가?
- 반복 중 원본을 바꾸는 코드는 왜 조심해야 하는가?

함수(function)로 반복되는 처리를 재사용하는 방법은 P2-8.5에서 이어서 봅니다.

## 이 절의 목표

- `for item in items` 반복을 읽을 수 있습니다.
- 이터러블(iterable)과 이터레이터(iterator)를 입문 수준에서 구분할 수 있습니다.
- `iterable`이라는 표현이 시퀀스뿐 아니라 딕셔너리, 파일, generator처럼 값을 하나씩 내보낼 수 있는 대상을 포괄하기 위한 말임을 설명할 수 있습니다.
- `enumerate()`, `.items()`, `zip()`이 어떤 반복 패턴인지 설명할 수 있습니다.
- 필터링, 변환, 누적, 조건 분리 반복을 구분할 수 있습니다.
- 리스트 컴프리헨션(list comprehension)과 딕셔너리 컴프리헨션(dictionary comprehension)을 “반복으로 새 자료구조를 만드는 표현”으로 읽을 수 있습니다.
- 빈 리스트에 결과를 모으는 패턴과 딕셔너리에 키별 값을 누적하는 패턴을 읽을 수 있습니다.
- 반복 중 원본 컬렉션을 직접 바꾸는 일이 문제를 만들 수 있음을 설명할 수 있습니다.

## 반복은 같은 처리를 여러 값에 적용하는 방식이다

일반적으로 반복(loop)은 데이터 묶음을 하나씩 처리하는 방법입니다. 같은 규칙을 여러 항목에 적용하고, 그 결과를 출력하거나 새 묶음으로 만들거나 누적값으로 모읍니다.

Python의 `for` 반복은 “묶음에서 항목을 하나씩 꺼내 처리한다”는 관점을 잘 드러냅니다.

```python
scores = [82, 75, 91, 68]

for score in scores:
    print(score)
```

이 코드는 `scores` 리스트에서 값을 하나씩 꺼내 `score`라는 이름으로 사용합니다.

다른 언어를 먼저 배운 사람은 반복을 숫자 인덱스 중심으로 떠올릴 수 있습니다.

```python
scores = [82, 75, 91, 68]

for i in range(len(scores)):
    print(scores[i])
```

이 방식도 동작합니다. 다만 항목을 하나씩 처리하는 목적이라면 `for score in scores`처럼 항목 중심으로 쓰는 형태가 의도를 더 분명히 드러냅니다.

Python 공식 튜토리얼도 `for` 문이 C나 Pascal에서 익숙한 숫자 진행 방식과 조금 다르며, 리스트나 문자열 같은 시퀀스(sequence)의 항목을 순서대로 순회한다고 설명합니다.

| 관점 | 일반적인 설명 | Python에서는 |
| --- | --- | --- |
| 반복(loop) | 묶음의 값을 하나씩 처리하는 절차 | `for item in items` 형태가 자주 쓰임 |
| 반복 대상 | 값을 하나씩 꺼낼 수 있는 묶음 | 이터러블(iterable)이라고 부름 |
| 반복 결과 | 출력, 새 묶음, 누적값, 분리된 묶음 | `print`, `append`, 누적 변수, 딕셔너리 누적 등으로 나타남 |

## 왜 이터러블이라고 부르는가

`iterable`은 “반복할 수 있는 대상”이라는 뜻입니다. 한국어로는 이터러블, 반복 가능 객체, 반복 가능한 대상처럼 옮길 수 있습니다. 이 표현이 필요한 이유는 Python의 반복이 리스트(list) 같은 시퀀스(sequence)에만 묶여 있지 않기 때문입니다.

초기 프로그래밍 언어를 배웠던 기억에서는 반복을 다음처럼 떠올리기 쉽습니다.

- 숫자 변수를 하나씩 증가시킵니다.
- 배열의 0번, 1번, 2번 위치를 차례로 접근합니다.
- 끝 위치에 도달하면 반복을 멈춥니다.

이 방식은 배열(array)이나 리스트(list)를 다룰 때 자연스럽습니다. 하지만 모든 반복 대상이 “정수 인덱스로 접근할 수 있는 배열”은 아닙니다. 딕셔너리는 키(key)를 기준으로 값을 찾고, 파일은 줄(line)을 하나씩 읽고, 생성기(generator)는 값을 필요할 때 하나씩 만들어 냅니다. 이런 대상들을 모두 `for` 문으로 다루려면 “인덱스가 있는가”보다 “값을 하나씩 내보낼 수 있는가”가 더 중요합니다.

이 흐름은 Python의 역사에서도 확인됩니다. PEP 234는 2001년에 작성된 제안으로, 객체가 `for` 루프의 동작을 제어할 수 있는 반복 인터페이스(iteration interface)를 제안했습니다. 이 제안은 Python 2.2 시기의 반복 구조와 연결되며, `for` 문이 기존의 시퀀스 중심 반복을 넘어 반복 가능한 여러 종류의 객체를 일관된 방식으로 다루게 하는 흐름을 보여 줍니다.

PEP 234의 핵심은 다음과 같이 일반화할 수 있습니다.

| 이전에 떠올리기 쉬운 반복 | Python의 iterable 관점 |
| --- | --- |
| 몇 번째 위치를 꺼낼 것인가? | 다음 값을 하나씩 받을 수 있는가? |
| 배열이나 리스트처럼 인덱스가 필요한가? | 리스트가 아니어도 반복 흐름을 만들 수 있는가? |
| 반복문이 구조 내부를 알아야 하는가? | 객체가 자기 반복 방식을 제공할 수 있는가? |

Python 공식 용어에서 이터러블(iterable)은 구성원을 한 번에 하나씩 반환할 수 있는 객체입니다. 리스트, 문자열, 튜플 같은 시퀀스뿐 아니라 딕셔너리, 파일 객체, 직접 만든 클래스도 이터러블이 될 수 있습니다. 그리고 `for` 문은 이터러블에서 이터레이터(iterator)를 만들고, 그 이터레이터가 주는 값을 하나씩 처리합니다.

이 관점은 초심자에게 중요합니다. `for item in items`를 볼 때 `items`가 반드시 리스트라고 가정하면 안 됩니다. `items`는 리스트일 수도 있고, 딕셔너리의 `.items()` 결과일 수도 있고, 파일일 수도 있고, 나중에 보게 될 generator일 수도 있습니다. 이름은 다르지만 공통 질문은 같습니다.

이 대상은 값을 하나씩 내보낼 수 있는가?

## 이터러블과 이터레이터 감각

Python 코드를 읽다 보면 다양한 반복 패턴을 만납니다.

```python
for score in scores:
    print(score)
```

```python
for index, score in enumerate(scores):
    print(index, score)
```

```python
for name, value in metrics.items():
    print(name, value)
```

겉모양은 다르지만 공통점이 있습니다. Python의 `for`는 “반복 가능한 대상”에서 값을 하나씩 꺼내 처리합니다.

공식 용어로는 반복 가능한 대상을 이터러블(iterable)이라고 부릅니다. 이터러블은 구성원을 한 번에 하나씩 돌려줄 수 있는 객체입니다. 리스트(list), 문자열(str), 튜플(tuple), 딕셔너리(dict), 파일 객체(file object) 등이 이터러블의 예입니다.

이터레이터(iterator)는 값의 흐름(stream)을 실제로 하나씩 꺼내는 객체입니다. 이 절에서는 `iter()`와 `next()`의 세부 사용법보다, `for`가 내부적으로 이런 반복 흐름을 만들어 준다는 감각을 먼저 둡니다.

아주 단순화하면 다음처럼 볼 수 있습니다.

| 용어 | 입문용 설명 | 예시 |
| --- | --- | --- |
| 이터러블(iterable) | 하나씩 꺼낼 수 있는 대상 | 리스트, 문자열, 딕셔너리, 파일 |
| 이터레이터(iterator) | 실제로 다음 값을 하나씩 내보내는 흐름 | `iter(scores)`로 얻는 객체 |
| 반복(loop) | 그 값을 하나씩 받아 처리하는 코드 | `for score in scores` |

이 구조 때문에 Python에서는 여러 반복 패턴이 같은 원리로 이어집니다. 중요한 것은 “무엇을 반복하는가”와 “반복 결과로 무엇을 만들 것인가”입니다.

## 반복 구조의 주요 유형

Python 반복은 하나의 문법만 외우기보다 패턴으로 구분해서 읽습니다.

이 절에서는 반복 패턴을 다음 순서로 봅니다. 먼저 항목을 하나씩 꺼내는 기본형을 보고, 그 다음 위치, 키-값, 두 묶음의 연결을 봅니다. 그 뒤에는 반복 결과로 새 리스트를 만들거나, 값을 누적하거나, 조건에 따라 분리하는 흐름을 봅니다.

| 흐름 | 중심 질문 |
| --- | --- |
| 항목 반복 | 무엇을 하나씩 꺼내는가? |
| 위치와 함께 반복 | 몇 번째 값인지도 필요한가? |
| 키-값 반복 | 이름과 값을 함께 봐야 하는가? |
| 결과 만들기 | 새 리스트나 딕셔너리를 만드는가? |
| 누적과 분리 | 값을 쌓거나 조건에 따라 나누는가? |

### 항목을 하나씩 처리한다

가장 기본적인 반복입니다.

```python
scores = [82, 75, 91, 68]

for score in scores:
    print(score)
```

읽는 법은 단순합니다.

`scores`에서 `score`를 하나씩 꺼내 처리한다.

AI 실습에서는 샘플(sample), 문장(sentence), 파일 이름, 예측 결과를 하나씩 볼 때 자주 씁니다.

### 위치와 항목을 함께 본다

몇 번째 항목인지도 필요하면 `enumerate()`를 씁니다.

```python
scores = [82, 75, 91, 68]

for index, score in enumerate(scores):
    print(index, score)
```

읽는 법은 다음과 같습니다.

`scores`에서 위치와 값을 함께 꺼내 처리한다.

오류가 난 샘플 번호를 확인하거나, 앞의 몇 개 결과만 점검할 때 유용합니다.

### 딕셔너리의 키와 값을 함께 본다

딕셔너리에서는 `.items()`를 자주 씁니다.

```python
metrics = {"accuracy": 0.91, "loss": 0.32}

for name, value in metrics.items():
    print(name, value)
```

읽는 법은 다음과 같습니다.

`metrics`에서 지표 이름과 값을 함께 꺼내 처리한다.

설정값(config), 평가 지표(metric), API 응답(response)을 확인할 때 자주 보입니다.

### 두 묶음을 나란히 본다

두 리스트를 같은 위치끼리 묶어 보고 싶을 때는 `zip()`을 만날 수 있습니다.

```python
texts = ["good", "bad", "great"]
labels = ["positive", "negative", "positive"]

for text, label in zip(texts, labels):
    print(text, label)
```

읽는 법은 다음과 같습니다.

`texts`와 `labels`를 같은 순서끼리 묶어 하나씩 처리한다.

입력 문장과 라벨(label), 예측값과 정답값, 파일 이름과 경로를 함께 다룰 때 이런 패턴이 보입니다.

### 조건에 맞는 값만 새로 모은다

P2-8.2에서 빈 리스트를 먼저 만들 수 있다고 했습니다. 반복에서는 그 빈 리스트가 결과를 모으는 그릇으로 자주 쓰입니다.

반복하면서 조건을 만족하는 값만 새 리스트로 만들 수 있습니다.

```python
scores = [82, 0, 75, 0, 91]
valid_scores = []

for score in scores:
    if score != 0:
        valid_scores.append(score)

print(valid_scores)
```

읽는 법은 다음과 같습니다.

`scores`를 하나씩 보고, 조건을 만족하는 값만 `valid_scores`에 모은다.

결측치 제거, 기준 이하 값 제외, 특정 라벨만 선택 같은 전처리(preprocessing)에서 자주 쓰입니다.

### 값을 바꿔 새 묶음을 만든다

반복은 기존 값을 다른 값으로 바꾸는 데도 쓰입니다.

```python
scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(score / 100)

print(normalized_scores)
```

읽는 법은 다음과 같습니다.

`scores`를 하나씩 보고, 각 값을 0과 1 사이의 값처럼 바꿔 새 리스트에 담는다.

정규화(normalization), 소문자 변환, 문자열 앞뒤 공백 제거처럼 “모든 항목에 같은 처리”를 할 때 이 패턴이 보입니다.

### 리스트 컴프리헨션으로 새 리스트를 만든다

반복 규칙이 짧고 결과가 새 리스트라면 리스트 컴프리헨션(list comprehension)을 만날 수 있습니다.

```python
squares = [number * number for number in range(5)]

print(squares)
```

이 코드는 `0`부터 `4`까지의 제곱값 목록을 만듭니다.

조건이 붙으면 필터링과 변환을 한 줄에 함께 쓸 수도 있습니다.

```python
scores = [82, 0, 75, 0, 91]

valid_scores = [score for score in scores if score != 0]

print(valid_scores)
```

읽는 법은 다음과 같습니다.

`scores`에서 `score`를 하나씩 보고, `0`이 아닌 값만 새 리스트로 만든다.

이 절에서는 긴 `for` 문으로 구조를 먼저 확인한 뒤, 짧은 표현을 읽는 순서로 둡니다.

### Python은 반복을 자료구조 정의 안에 넣기도 한다

Python 코드에서는 반복문이 리스트나 딕셔너리를 정의하는 문법 안에 들어간 것처럼 보이는 패턴을 자주 만납니다. 이것을 컴프리헨션(comprehension)이라고 부릅니다.

컴프리헨션(comprehension)은 기존 이터러블(iterable)의 항목을 하나씩 처리해 새 컬렉션(collection)을 만드는 표현입니다. Python 공식 튜토리얼은 리스트 컴프리헨션(list comprehension)을 새 리스트를 만드는 간결한 방법으로 설명합니다. 이 절에서는 그 관점을 조금 넓혀, 리스트나 딕셔너리처럼 새 자료구조를 만들기 위한 반복 표현으로 이해합니다.

정의적으로는 다음 세 요소를 함께 봅니다.

| 요소 | 질문 | 예시 |
| --- | --- | --- |
| 입력 이터러블 | 무엇에서 하나씩 꺼내는가? | `scores` |
| 반복 변수 | 꺼낸 값을 어떤 이름으로 부르는가? | `score` |
| 결과 표현식 | 꺼낸 값으로 무엇을 만들어 넣는가? | `score / 100` |

그래서 `[score / 100 for score in scores]`는 다음처럼 읽습니다.

`scores`에서 `score`를 하나씩 꺼내고, 각 `score`를 `score / 100`으로 바꾼 새 리스트를 만든다.

긴 `for` 문으로 쓰면 다음과 같습니다.

```python
scores = [82, 75, 91]
normalized_scores = []

for score in scores:
    normalized_scores.append(score / 100)

print(normalized_scores)
```

같은 의도를 리스트 컴프리헨션으로 쓰면 다음처럼 짧아집니다.

```python
scores = [82, 75, 91]

normalized_scores = [score / 100 for score in scores]

print(normalized_scores)
```

이 표현은 “`scores`에서 `score`를 하나씩 꺼내고, 각 값을 `score / 100`으로 바꿔 새 리스트를 만든다”는 뜻입니다. 반복을 감춘 것이 아니라, 반복의 목적이 새 리스트 생성임을 문법 모양으로 드러낸 것입니다.

딕셔너리도 같은 방식으로 만들 수 있습니다.

```python
labels = ["negative", "positive", "neutral"]

label_to_id = {label: index for index, label in enumerate(labels)}

print(label_to_id)
```

이 코드는 라벨 이름을 키(key)로, 위치 번호를 값(value)으로 갖는 딕셔너리를 만듭니다.

컴프리헨션이 선호되는 이유는 다음과 같습니다.

| 이유 | 설명 |
| --- | --- |
| 의도 | 새 리스트나 딕셔너리를 만든다는 목적이 바로 보임 |
| 간결함 | 빈 리스트를 만들고 `append()`하는 절차를 줄임 |
| 일관성 | “무엇을 꺼내서 무엇으로 바꾸는가”가 한 줄에 모임 |
| 데이터 처리 | 필터링, 변환, 매핑처럼 자주 쓰는 패턴을 짧게 표현함 |

하지만 컴프리헨션이 항상 더 좋은 것은 아닙니다. 조건이 길거나, 중첩 반복이 많거나, 중간 계산에 이름을 붙여야 하면 일반 `for` 문이 더 읽기 쉽습니다.

```python
results = []

for item in items:
    if item["score"] >= 60:
        normalized_score = item["score"] / 100
        results.append(normalized_score)
```

이런 코드는 여러 단계가 보이는 편이 낫습니다. 따라서 이 절에서는 다음 기준을 둡니다.

- 반복 결과가 새 리스트나 딕셔너리이고 규칙이 짧으면 컴프리헨션을 읽을 수 있습니다.
- 처리 과정이 길거나 설명이 필요하면 일반 `for` 문을 사용합니다.
- 컴프리헨션을 “고급 문법”으로 외우기보다 “반복으로 새 자료구조를 만드는 표현”으로 이해합니다.

### 누적값을 계산한다

반복은 값을 하나씩 누적하는 데도 쓰입니다.

```python
scores = [82, 75, 91, 68]
total = 0

for score in scores:
    total = total + score

print(total)
```

읽는 법은 다음과 같습니다.

`scores`를 하나씩 보고, `total`에 계속 더한다.

합계, 개수, 등장 횟수, 손실(loss)의 누적처럼 반복해서 쌓아 가는 계산에서 이런 구조가 보입니다.

### 조건에 따라 분리한다

하나의 묶음을 두 묶음으로 나눌 수도 있습니다.

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

읽는 법은 다음과 같습니다.

`scores`를 하나씩 보고, 조건에 따라 다른 리스트에 담는다.

학습 데이터와 테스트 데이터 분리, 정상 데이터와 이상 데이터 분리, 라벨별 데이터 분리로 이어지는 기본 감각입니다.

### 딕셔너리에 누적한다

P2-8.3에서는 딕셔너리를 키로 값을 찾는 구조로 봤습니다. 반복과 함께 쓰면 “키별로 값을 쌓는 구조”가 됩니다.

반복과 딕셔너리를 함께 쓰면 키별 집계가 가능합니다.

```python
labels = ["positive", "negative", "positive", "neutral", "positive"]
label_counts = {}

for label in labels:
    label_counts[label] = label_counts.get(label, 0) + 1

print(label_counts)
```

읽는 법은 다음과 같습니다.

`labels`를 하나씩 보고, 같은 라벨이 몇 번 나왔는지 딕셔너리에 누적한다.

분류 데이터에서 라벨 분포(label distribution)를 확인할 때 이런 패턴을 자주 사용합니다.

## 작은 데이터 처리 예시

다음 예시는 여러 학생의 점수를 보고, 기준을 넘은 학생만 통과 목록에 넣습니다.

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

여기에는 세 가지 구조가 함께 나옵니다.

| 코드 | 의미 |
| --- | --- |
| `students` | 학생 정보를 담은 리스트 |
| `{"name": "Kim", "score": 82.5}` | 학생 한 명을 표현한 딕셔너리 |
| `for student in students` | 학생 정보를 하나씩 꺼내는 반복 |

이 예시는 작지만 AI 실습의 기본 구조와 닮아 있습니다.

- 데이터셋(dataset)은 여러 샘플(sample)의 묶음입니다.
- 샘플 하나는 여러 필드(field)를 가질 수 있습니다.
- 반복문은 샘플을 하나씩 확인합니다.
- 조건문은 필요한 샘플을 고르거나 처리 방식을 바꿉니다.

## 반복 중에 원본을 바꾸는 것은 조심한다

반복하면서 같은 리스트나 딕셔너리를 직접 바꾸면 예상과 다른 결과가 생길 수 있습니다.

예를 들어 목록을 돌면서 동시에 항목을 지우는 코드는 조심해야 합니다.

```python
scores = [82, 0, 75, 0, 91]
filtered_scores = []

for score in scores:
    if score != 0:
        filtered_scores.append(score)

print(filtered_scores)
```

이 예시는 원본 `scores`를 직접 지우지 않고, 새 리스트 `filtered_scores`를 만듭니다. Python 공식 튜토리얼도 컬렉션(collection)을 반복하면서 같은 컬렉션을 수정하는 코드는 까다로울 수 있고, 복사본을 돌거나 새 컬렉션을 만드는 방식이 더 명확할 수 있다고 설명합니다.

데이터 전처리에서도 이 원칙은 유용합니다.

- 원본 데이터는 보존합니다.
- 필터링 결과는 새 이름에 담습니다.
- 어떤 기준으로 걸렀는지 코드에 남깁니다.

## 예시를 읽는 공통 질문

리스트, 딕셔너리, 반복 예시가 많아지면 문법만 따라가다 길을 잃을 수 있습니다. 그럴 때는 다음 질문으로 코드를 읽습니다.

1. 무엇이 묶음인가?
2. 그 묶음은 순서가 중요한가, 키가 중요한가?
3. 반복은 무엇을 하나씩 꺼내는가?
4. 꺼낸 값으로 무엇을 하는가?
5. 결과는 새 리스트인가, 새 딕셔너리인가, 출력인가, 누적값인가?

예를 들어 다음 코드를 봅니다.

```python
texts = ["AI is useful", "Models can fail", "Data matters"]
lengths = []

for text in texts:
    lengths.append(len(text))

print(lengths)
```

이 코드는 이렇게 읽습니다.

| 질문 | 답 |
| --- | --- |
| 무엇이 묶음인가? | `texts` |
| 순서가 중요한가, 키가 중요한가? | 문장 목록이므로 순서가 있는 리스트 |
| 무엇을 하나씩 꺼내는가? | 문장 하나씩 |
| 꺼낸 값으로 무엇을 하는가? | 길이를 계산 |
| 결과는 무엇인가? | 길이 목록 `lengths` |

이 질문은 이후 NumPy, Pandas, 머신러닝 데이터 처리 코드를 읽을 때도 그대로 쓸 수 있습니다. 도구가 바뀌어도 “묶음, 하나씩 꺼낸 값, 처리, 결과”라는 구조는 유지됩니다.

## 이 절에서 기억할 관점

반복은 묶음에서 값을 하나씩 꺼내 처리하는 방식입니다. Python에서는 반복 가능한 대상(iterable)을 `for`가 받아서, 값의 흐름을 하나씩 소비하는 구조로 읽으면 다양한 반복 패턴이 이해됩니다.

일반화하면 반복은 데이터 묶음을 결과 묶음, 누적값, 분리된 묶음, 출력으로 바꾸는 절차입니다. 문법보다 먼저 입력 묶음과 결과 형태를 확인합니다.

반복 코드를 읽을 때는 다음 질문을 사용합니다.

1. 무엇이 이터러블(iterable)인가?
2. 반복마다 어떤 값이 하나씩 나오는가?
3. 위치가 필요한가, 값만 필요한가?
4. 결과는 새 리스트인가, 새 딕셔너리인가, 누적값인가?
5. 원본을 직접 바꾸고 있지는 않은가?
6. 새 자료구조를 만드는 짧은 규칙이라면 컴프리헨션으로 쓰였는가?

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

- Python Software Foundation, [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Glossary: iterable, iterator](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-25.
- Python Software Foundation, [The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-25.
- Ka-Ping Yee, Guido van Rossum, [PEP 234 -- Iterators](https://peps.python.org/pep-0234/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals, 2001, 확인 날짜: 2026-06-25.

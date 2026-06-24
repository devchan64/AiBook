# P2-8.2 리스트(list), 딕셔너리(dictionary), 반복(loop)

P2-8.1에서는 Python의 값(value), 변수(variable), 타입(type)을 봤습니다. 하나의 값에 이름을 붙이고, 그 값의 타입을 확인하는 감각을 만들었습니다.

하지만 AI 실습에서 다루는 데이터는 보통 값 하나가 아닙니다.

점수 여러 개, 문장 여러 개, 열 이름 여러 개, 설정값 여러 개, 모델 출력 여러 개를 함께 다룹니다. 그래서 Python에서는 값을 묶어 담는 방법과, 그 묶음을 하나씩 처리하는 방법이 중요합니다.

이 절에서는 리스트(list), 딕셔너리(dictionary), 반복(loop)을 봅니다.

## 이 절의 범위

이 절은 Python에서 데이터 묶음을 다루는 최소 문법을 다룹니다.

여기서는 다음 질문에 답합니다.

- 리스트(list)는 어떤 데이터 묶음에 어울리는가?
- 딕셔너리(dictionary)는 어떤 데이터 묶음에 어울리는가?
- Python의 `for` 반복은 왜 인덱스보다 항목 중심으로 읽는가?
- 이터러블(iterable)과 이터레이터(iterator)는 반복을 이해할 때 어떤 감각을 주는가?
- Python에서 자주 보이는 반복 패턴에는 어떤 유형이 있는가?
- 리스트와 딕셔너리를 AI 실습에서 어떻게 만나는가?
- 반복문을 쓸 때 무엇을 조심해야 하는가?

이 절은 함수(function), 클래스(class), 고급 리스트 컴프리헨션(list comprehension), 제너레이터(generator), 성능 최적화를 깊게 다루지 않습니다. 함수는 P2-8.3에서 이어서 봅니다.

## 이 절의 목표

- 리스트(list)를 순서가 있는 값 묶음으로 설명할 수 있습니다.
- 딕셔너리(dictionary)를 키(key)와 값(value)의 묶음으로 설명할 수 있습니다.
- `for item in items` 형태의 반복을 읽을 수 있습니다.
- 이터러블(iterable)과 이터레이터(iterator)를 입문 수준에서 구분할 수 있습니다.
- 항목 반복, 인덱스 반복, 키-값 반복, 병렬 반복, 필터링 반복의 차이를 설명할 수 있습니다.
- `enumerate()`와 `.items()`가 왜 자주 쓰이는지 설명할 수 있습니다.
- AI 실습에서 데이터 목록, 설정값, 결과 묶음을 Python 구조로 읽을 수 있습니다.

## 리스트는 순서가 있는 값 묶음이다

리스트(list)는 여러 값을 순서대로 담는 자료구조(data structure)입니다.

```python
scores = [82, 75, 91, 68]

print(scores)
print(type(scores))
```

리스트 안의 각 값은 항목(item) 또는 원소(element)라고 부를 수 있습니다.

리스트는 순서가 있으므로 위치(index)로 값을 꺼낼 수 있습니다.

```python
scores = [82, 75, 91, 68]

print(scores[0])
print(scores[1])
```

Python의 인덱스(index)는 보통 0부터 시작합니다. 그래서 `scores[0]`은 첫 번째 값입니다.

| 표현 | 의미 | 값 |
| --- | --- | --- |
| `scores[0]` | 첫 번째 항목 | `82` |
| `scores[1]` | 두 번째 항목 | `75` |
| `scores[-1]` | 마지막 항목 | `68` |

처음에는 이 0부터 시작하는 규칙이 낯설 수 있습니다. 하지만 문자열, 리스트, 배열, NumPy 인덱싱에서 계속 반복되므로 일찍 익숙해지는 편이 좋습니다.

## 리스트가 어울리는 상황들

리스트는 “같은 성격의 값들이 순서대로 모여 있다”는 느낌이 강할 때 어울립니다.

### 점수 여러 개

```python
scores = [82, 75, 91, 68]

print(max(scores))
print(min(scores))
print(sum(scores) / len(scores))
```

점수 목록은 순서가 있을 수도 있고, 전체를 모아 평균을 낼 수도 있습니다.

### 문장 여러 개

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

```python
probabilities = [0.92, 0.31, 0.77, 0.12]

for probability in probabilities:
    if probability >= 0.8:
        print("high confidence")
    else:
        print("check")
```

모델이 여러 입력에 대해 확률 점수(probability score)를 냈다면, 그 결과도 리스트로 볼 수 있습니다.

### 파일 이름 여러 개

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

## 리스트는 값을 추가하고 바꿀 수 있다

리스트는 바뀔 수 있는 값(mutable value)입니다.

```python
scores = [82, 75, 91]

scores.append(68)
scores[1] = 77

print(scores)
```

`append()`는 리스트 끝에 값을 추가합니다. `scores[1] = 77`은 두 번째 항목을 바꿉니다.

P2-8.1에서 “변수는 값에 붙인 이름”이라고 했습니다. 리스트에서는 이 관점이 더 중요해집니다.

```python
scores = [82, 75, 91]
other_scores = scores

other_scores.append(68)

print(scores)
print(other_scores)
```

`scores`와 `other_scores`는 서로 다른 리스트를 복사한 것이 아니라 같은 리스트를 가리킵니다. 그래서 한쪽 이름으로 값을 추가하면 다른 이름으로 봐도 같은 변경이 보입니다.

입문 단계에서는 이 정도만 기억합니다.

- 숫자나 문자열 하나를 바꾸는 감각과 리스트를 바꾸는 감각은 다를 수 있습니다.
- 리스트를 다른 이름에 대입했다고 해서 자동으로 새 복사본이 생기는 것은 아닙니다.
- 데이터 전처리에서 원본을 보존해야 하면 복사 여부를 조심해야 합니다.

얕은 복사(shallow copy)와 깊은 복사(deep copy)는 여기서 깊게 다루지 않습니다. 이후 데이터 처리에서 필요할 때 다시 봅니다.

## 딕셔너리는 이름표가 붙은 값 묶음이다

딕셔너리(dictionary)는 키(key)와 값(value)을 한 쌍으로 담는 자료구조입니다.

```python
student = {
    "name": "Kim",
    "score": 82.5,
    "passed": True,
}

print(student["name"])
print(student["score"])
```

리스트가 위치로 값을 찾는다면, 딕셔너리는 키로 값을 찾습니다.

| 구조 | 값을 찾는 기준 | 예시 |
| --- | --- | --- |
| 리스트(list) | 위치(index) | `scores[0]` |
| 딕셔너리(dictionary) | 키(key) | `student["score"]` |

딕셔너리는 AI 실습에서 자주 보입니다.

- 설정값 묶음: `{"learning_rate": 0.01, "epochs": 10}`
- 데이터 한 행: `{"text": "hello", "label": "positive"}`
- API 응답 일부: `{"model": "example", "tokens": 120}`
- 모델 평가 결과: `{"accuracy": 0.91, "loss": 0.32}`

딕셔너리는 “순서대로 몇 번째 값인가”보다 “어떤 이름의 값인가”가 중요할 때 어울립니다.

## 딕셔너리는 범용적인 맵 구조로 자주 쓰인다

딕셔너리는 단순히 “여러 값을 예쁘게 묶는 문법”이 아닙니다. Python 공식 문서에서는 딕셔너리를 매핑 타입(mapping type)으로 설명합니다. 매핑(mapping)은 어떤 키(key)를 어떤 값(value)에 연결하는 구조입니다.

입문 단계에서는 딕셔너리를 이렇게 이해하면 좋습니다.

딕셔너리는 키를 주면 값을 빠르게 찾기 위한 범용적인 맵(map)입니다.

```python
label_name = {
    0: "negative",
    1: "positive",
}

prediction = 1
print(label_name[prediction])
```

위 예시에서 `prediction`이 `1`이면 딕셔너리는 `1`이라는 키에 연결된 `"positive"`를 찾아 줍니다. 리스트처럼 “몇 번째 칸을 뒤져야 하는가”를 사람이 직접 생각하기보다, 키를 기준으로 값을 꺼냅니다.

이 감각은 실무와 AI 실습에서 자주 나타납니다.

| 상황 | 딕셔너리로 보는 방법 |
| --- | --- |
| 라벨 번호를 사람이 읽는 이름으로 바꾸기 | `{0: "negative", 1: "positive"}` |
| 설정 이름으로 설정값 찾기 | `{"batch_size": 32, "learning_rate": 0.001}` |
| 사용자 ID로 사용자 정보 찾기 | `{"u001": {"name": "Kim"}}` |
| 단어로 등장 횟수 찾기 | `{"AI": 3, "model": 5}` |
| 컬럼 이름으로 데이터 의미 찾기 | `{"score": "시험 점수", "label": "정답 라벨"}` |

“맵 성능”이라는 경험은 보통 이런 상황에서 생깁니다. 키가 있으면 값을 바로 찾을 수 있고, 키가 없으면 없다는 사실을 확인할 수 있습니다.

```python
word_count = {
    "AI": 3,
    "model": 5,
    "data": 8,
}

word = "model"

if word in word_count:
    print(word_count[word])
```

다만 성능을 말할 때는 조심해야 합니다. 딕셔너리는 일반적으로 키 기반 조회에 매우 유용하고 빠른 구조로 쓰이지만, 모든 상황에서 항상 최선이라는 뜻은 아닙니다. 키는 해시 가능(hashable)해야 하고, 데이터의 순서 자체가 중요한 문제라면 리스트나 다른 구조가 더 자연스러울 수 있습니다.

여기서는 다음 정도만 기억합니다.

- 리스트는 순서와 위치가 중요할 때 자연스럽습니다.
- 딕셔너리는 키로 값을 찾는 일이 중요할 때 자연스럽습니다.
- 딕셔너리는 설정값, 라벨 맵, 카운트, 메타데이터처럼 “이름으로 찾는 데이터”에 강합니다.

## 딕셔너리가 어울리는 상황들

딕셔너리는 “무엇을 기준으로 값을 찾을 것인가”가 분명할 때 강합니다.

### 설정값 묶음

```python
config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 10,
}

print(config["learning_rate"])
```

설정값은 순서보다 이름이 중요합니다. `learning_rate`라는 이름으로 값을 찾는 편이 `config[1]`처럼 위치로 찾는 것보다 안전합니다.

### 라벨 번호를 이름으로 바꾸기

```python
label_map = {
    0: "negative",
    1: "positive",
    2: "neutral",
}

predicted_label = 2

print(label_map[predicted_label])
```

모델 출력이 숫자 라벨일 때, 사람이 읽을 수 있는 이름으로 바꾸는 데 딕셔너리를 사용할 수 있습니다.

### 단어 개수 세기

```python
words = ["AI", "model", "AI", "data", "model", "AI"]
counts = {}

for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)
```

딕셔너리는 “이 단어가 지금까지 몇 번 나왔는가”처럼 키별 누적값을 관리할 때 유용합니다.

### 샘플 ID로 데이터 찾기

```python
samples_by_id = {
    "s001": {"text": "good product", "label": "positive"},
    "s002": {"text": "bad service", "label": "negative"},
}

sample_id = "s001"

print(samples_by_id[sample_id]["text"])
```

데이터가 많아지면 “몇 번째 데이터인가”보다 “어떤 ID의 데이터인가”가 중요해질 수 있습니다. 이때 딕셔너리는 ID에서 샘플로 가는 맵처럼 쓰입니다.

### 컬럼 이름으로 의미 붙이기

```python
column_description = {
    "text": "입력 문장",
    "label": "정답 라벨",
    "score": "모델 점수",
}

print(column_description["score"])
```

데이터셋을 읽을 때 컬럼 이름의 의미를 따로 정리해 두면, 이후 전처리와 문서화가 쉬워집니다.

## 키가 없을 수 있다는 점을 조심한다

딕셔너리에서 없는 키를 바로 꺼내면 오류가 날 수 있습니다.

```python
student = {"name": "Kim", "score": 82.5}

print(student["label"])
```

`"label"`이라는 키가 없기 때문에 이 코드는 실패합니다.

키가 없을 수도 있는 상황에서는 `get()`을 사용할 수 있습니다.

```python
student = {"name": "Kim", "score": 82.5}

print(student.get("label"))
print(student.get("label", "unknown"))
```

데이터 파일이나 API 응답을 다룰 때는 항상 모든 키가 있다고 가정하면 위험합니다. 실제 데이터에는 빠진 값, 이름이 다른 값, 예상과 다른 타입이 섞일 수 있습니다.

## 반복은 묶음을 하나씩 처리하는 방식이다

반복(loop)은 데이터 묶음을 하나씩 처리하는 방법입니다.

Python의 `for` 반복은 특히 Python의 특징이 잘 드러납니다.

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

이 방식도 동작합니다. 하지만 Python에서는 단순히 항목을 하나씩 처리할 때 첫 번째 방식이 더 자연스럽습니다.

Python 공식 튜토리얼도 `for` 문이 C나 Pascal에서 익숙한 숫자 진행 방식과 조금 다르며, 리스트나 문자열 같은 시퀀스(sequence)의 항목을 순서대로 순회한다고 설명합니다.

## 이터러블과 이터레이터 감각

사용자가 Python 코드를 읽다 보면 다양한 반복 패턴을 만납니다.

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

이터레이터(iterator)는 값의 흐름(stream)을 실제로 하나씩 꺼내는 객체입니다. 입문 단계에서 직접 `iter()`와 `next()`를 자주 쓸 필요는 없습니다. 중요한 것은 `for`가 내부적으로 이런 반복 흐름을 만들어 준다는 감각입니다.

아주 단순화하면 다음처럼 볼 수 있습니다.

| 용어 | 입문용 설명 | 예시 |
| --- | --- | --- |
| 이터러블(iterable) | 하나씩 꺼낼 수 있는 대상 | 리스트, 문자열, 딕셔너리, 파일 |
| 이터레이터(iterator) | 실제로 다음 값을 하나씩 내보내는 흐름 | `iter(scores)`로 얻는 객체 |
| 반복(loop) | 그 값을 하나씩 받아 처리하는 코드 | `for score in scores` |

이 구조 때문에 Python에서는 여러 반복 패턴이 자연스럽게 보입니다. 중요한 것은 “무엇을 반복하는가”입니다.

## 반복 구조의 주요 유형

Python 반복은 하나의 문법만 외우기보다 패턴으로 보는 편이 좋습니다.

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

### 짧은 표현으로 새 리스트를 만든다

위 패턴은 리스트 컴프리헨션(list comprehension)으로 짧게 쓰일 수 있습니다.

```python
scores = [82, 0, 75, 0, 91]

valid_scores = [score for score in scores if score != 0]

print(valid_scores)
```

읽는 법은 다음과 같습니다.

`scores`에서 `score`를 하나씩 보고, `0`이 아닌 값만 새 리스트로 만든다.

처음에는 긴 `for` 문으로 이해한 뒤, 짧은 표현을 읽는 순서가 안전합니다.

## 위치도 필요하면 enumerate를 쓴다

항목뿐 아니라 위치도 필요할 때가 있습니다.

예를 들어 몇 번째 점수인지 함께 출력하고 싶다면 `enumerate()`를 사용할 수 있습니다.

```python
scores = [82, 75, 91, 68]

for index, score in enumerate(scores):
    print(index, score)
```

`enumerate()`는 위치와 값을 함께 줍니다.

| 반복에서 받는 값 | 의미 |
| --- | --- |
| `index` | 현재 위치 |
| `score` | 현재 항목 |

AI 실습에서는 데이터의 위치가 필요한 경우가 있습니다.

- 몇 번째 샘플(sample)에서 오류가 났는지 확인한다.
- 출력 결과와 원본 입력을 같은 순서로 비교한다.
- 일부 데이터만 확인하기 위해 앞의 몇 개 항목을 출력한다.

하지만 위치가 필요하지 않다면 굳이 `range(len(...))`부터 쓰지 않아도 됩니다.

## 딕셔너리를 반복할 때는 items를 자주 쓴다

딕셔너리는 키와 값을 함께 꺼내는 경우가 많습니다.

```python
metrics = {
    "accuracy": 0.91,
    "loss": 0.32,
    "precision": 0.88,
}

for name, value in metrics.items():
    print(name, value)
```

`.items()`는 키와 값을 함께 꺼내 줍니다.

| 이름 | 값 |
| --- | --- |
| `accuracy` | `0.91` |
| `loss` | `0.32` |
| `precision` | `0.88` |

모델 평가 결과나 설정값을 출력할 때 이런 패턴을 자주 만납니다.

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

## 리스트 컴프리헨션은 짧은 반복 표현이다

Python에서는 리스트를 만드는 짧은 표현으로 리스트 컴프리헨션(list comprehension)을 자주 봅니다.

```python
scores = [82, 75, 91, 68]

passed = [score for score in scores if score >= 60]

print(passed)
```

이 코드는 다음 반복문과 비슷한 일을 합니다.

```python
scores = [82, 75, 91, 68]
passed = []

for score in scores:
    if score >= 60:
        passed.append(score)

print(passed)
```

입문 단계에서는 리스트 컴프리헨션을 반드시 능숙하게 쓸 필요는 없습니다. 다만 Python 예제 코드에서 자주 보이므로 읽을 수는 있어야 합니다.

처음에는 긴 반복문으로 이해하고, 익숙해진 뒤 짧은 표현을 읽는 순서가 안전합니다.

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

이 질문은 이후 NumPy, Pandas, 머신러닝 데이터 처리 코드를 읽을 때도 그대로 쓸 수 있습니다.

## 이 절에서 기억할 관점

리스트, 딕셔너리, 반복은 Python 문법의 장식이 아닙니다. 데이터가 여러 개가 되는 순간 필요한 기본 도구입니다.

- 리스트(list)는 순서가 있는 값 묶음입니다.
- 딕셔너리(dictionary)는 키(key)로 값을 찾는 묶음입니다.
- 딕셔너리는 키를 값에 연결하는 매핑(mapping) 구조이며, 이름으로 값을 찾는 데이터에 강합니다.
- 반복(loop)은 묶음에서 값을 하나씩 꺼내 처리하는 방식입니다.
- 이터러블(iterable)은 하나씩 꺼낼 수 있는 대상이고, 이터레이터(iterator)는 그 값을 실제로 하나씩 내보내는 흐름입니다.

AI 실습에서는 데이터셋, 샘플, 설정값, 평가 결과가 대부분 이런 구조로 표현됩니다. 따라서 문법을 외우기보다 “이 데이터는 순서가 중요한가, 이름표가 중요한가, 하나씩 처리해야 하는가”를 먼저 묻는 편이 좋습니다.

## 체크리스트

- 리스트(list)를 순서가 있는 값 묶음으로 설명할 수 있다.
- 딕셔너리(dictionary)를 키(key)와 값(value)의 묶음으로 설명할 수 있다.
- 딕셔너리를 범용적인 매핑(mapping) 구조로 설명할 수 있다.
- `for item in items` 반복을 읽고 실행 흐름을 설명할 수 있다.
- 이터러블(iterable)과 이터레이터(iterator)를 입문 수준에서 구분할 수 있다.
- 항목 반복, 인덱스 반복, 키-값 반복, 병렬 반복, 필터링 반복을 구분할 수 있다.
- 위치가 필요할 때 `enumerate()`를 사용할 수 있음을 설명할 수 있다.
- 딕셔너리의 키와 값을 함께 볼 때 `.items()`를 사용할 수 있음을 설명할 수 있다.
- 반복 중 원본 데이터를 직접 바꾸는 일이 위험할 수 있음을 설명할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Glossary: iterable, iterator](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.

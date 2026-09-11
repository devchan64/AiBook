# P2-8.3 딕셔너리(dictionary): 키(key)로 값을 찾는 구조

> Section ID: `P2-8.3`
> Version: `v2026.09.08`

## 키와 값

일반적으로 매핑(mapping)은 어떤 기준을 값에 연결하는 구조입니다. 그 기준을 키(key)라고 부르고, 키에 연결된 대상을 값(value)이라고 부를 수 있습니다.

Python에서는 이런 매핑 구조를 딕셔너리(dictionary)로 자주 표현합니다.

학생 이름 `"Kim"`, 점수 `82.5`, 통과 여부 `True`를 각각 `"name"`, `"score"`, `"passed"` 키에 연결합니다. 다음 코드는 이름과 점수를 찾아 `Kim`, `82.5`를 출력합니다.

```python
student = {
    "name": "Kim",
    "score": 82.5,
    "passed": True,
}

print(student["name"])
print(student["score"])
```

리스트가 위치로 값을 찾는다면, Python 딕셔너리는 키로 값을 찾습니다.

| 구조 | 값을 찾는 기준 | 예시 |
| --- | --- | --- |
| 리스트(list) | 위치(index) | `scores[0]` |
| 딕셔너리(dictionary) | 키(key) | `student["score"]` |

딕셔너리는 AI 실습에서 자주 보입니다.

- 설정값 묶음: `{"learning_rate": 0.01, "epochs": 10}`
- 데이터 한 행: `{"text": "hello", "label": "positive"}`
- API 응답 일부: `{"model": "example", "tokens": 120}`
- 모델 평가 결과: `{"accuracy": 0.91, "loss": 0.32}`

딕셔너리는 “순서대로 몇 번째 값인가”보다 “어떤 이름의 값인가”가 중요할 때 사용합니다.

| 관점 | 일반적인 설명 | Python에서는 |
| --- | --- | --- |
| 매핑(mapping) | 어떤 기준을 값에 연결하는 구조 | 딕셔너리(dictionary)를 사용함 |
| 키(key) | 값을 찾는 기준 | 문자열, 숫자 등 해시 가능한 값이 될 수 있음 |
| 값(value) | 키에 연결된 대상 | 숫자, 문자열, 리스트, 딕셔너리 등 다양한 값이 올 수 있음 |

## 라벨 대응과 키 확인

라벨 번호 `0`은 `"negative"`, `1`은 `"positive"`에 연결되어 있습니다. 예측값 `1`을 키로 조회하면 `positive`가 출력됩니다.

```python
label_name = {
    0: "negative",
    1: "positive",
}

prediction = 1
print(label_name[prediction])
```

위 예시에서 `prediction`이 `1`이면 딕셔너리는 `1`이라는 키에 연결된 `"positive"`를 찾아 줍니다. 숫자 키 `1`은 두 번째 위치라는 뜻이 아니라, 연결할 값을 찾는 식별자입니다.

라벨뿐 아니라 설정 이름, ID, 컬럼 이름도 키로 사용할 수 있습니다.

| 상황 | 딕셔너리로 보는 방법 |
| --- | --- |
| 라벨 번호를 사람이 읽는 이름으로 바꾸기 | `{0: "negative", 1: "positive"}` |
| 설정 이름으로 설정값 찾기 | `{"batch_size": 32, "learning_rate": 0.001}` |
| 사용자 ID로 사용자 정보 찾기 | `{"u001": {"name": "Kim"}}` |
| 컬럼 이름으로 데이터 의미 찾기 | `{"score": "시험 점수", "label": "정답 라벨"}` |

`키 in 딕셔너리`는 그 키가 있는지 확인하는 비교입니다.

설정에 `"learning_rate"` 키가 있는지 `in`으로 확인하고, 있으면 그 값을 출력합니다. 아래 설정에서는 `0.001`이 출력되며, `name`을 없는 키 `"dropout"`으로 바꾸면 아무것도 출력되지 않습니다.

```python
config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 10,
}

name = "learning_rate"

if name in config:
    print(config[name])
```

## 해시 가능한 키

Python 공식 문서는 딕셔너리를 매핑 타입(mapping type)으로 설명합니다. 매핑은 키와 값의 연결이고, 해시(hash)는 조회를 구현하는 데 쓰이는 방식입니다. 딕셔너리의 키는 해시 가능(hashable)해야 합니다.

문자열과 숫자는 키로 쓸 수 있습니다. 튜플은 안의 원소들도 모두 해시 가능할 때 키로 쓸 수 있습니다. 리스트는 해시 가능하지 않아 키로 쓸 수 없습니다.

이름 `"Kim"`을 키로 조회하면 연결된 점수 `82`가 출력됩니다.

```python
scores_by_name = {
    "Kim": 82,
    "Lee": 91,
}

print(scores_by_name["Kim"])
```

딕셔너리는 키를 넣은 순서를 보존합니다. 키의 크기나 글자 순서로 자동 정렬하는 것은 아닙니다. 다음 코드에서 `"Lee"`를 먼저 넣었으므로 키 목록은 `['Lee', 'Kim']`입니다.

```python
scores_by_name = {"Lee": 91, "Kim": 82}
print(list(scores_by_name))
```

`list(딕셔너리)`는 키들을 리스트로 만듭니다. 값을 조회하는 `scores_by_name["Kim"]`과 구분해야 합니다.

## 같은 키의 값 교체

같은 키에 새 값을 저장하면 기존 값은 새 값으로 바뀝니다.

빈 딕셔너리의 `"Kim"` 키에 `82`를 저장한 뒤 `91`을 저장합니다. 출력은 `{'Kim': 91}`이며 기존 점수를 덮어씁니다.

```python
scores = {}

scores["Kim"] = 82
scores["Kim"] = 91

print(scores)
```

이 코드는 `"Kim"`이라는 키에 두 점수를 모두 보관하지 않습니다. 마지막 값인 `91`만 남습니다. 한 키에 여러 값을 모으고 싶다면 값(value) 쪽에 리스트 같은 묶음을 넣을 수 있습니다.

한 사람의 점수 두 개를 보관하려면 값으로 리스트를 사용할 수 있습니다. 아래에서 `"Kim"` 키를 조회한 결과는 `[82, 91]`입니다.

```python
scores = {
    "Kim": [82, 91],
}

print(scores["Kim"])
```

## 설정·라벨·ID 조회

딕셔너리는 “무엇을 기준으로 값을 찾을 것인가”가 분명할 때 적합합니다.

### 설정값 묶음

설정 딕셔너리에서 학습률을 나타내는 `"learning_rate"`를 조회하면 `0.001`이 출력됩니다.

```python
config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 10,
}

print(config["learning_rate"])
```

`config[1]`은 두 번째 설정을 찾는 코드가 아닙니다. 정수 키 `1`을 찾는 코드이며, 위 딕셔너리에는 그 키가 없어 `KeyError`가 발생합니다.

### 라벨 번호를 이름으로 바꾸기

숫자 라벨 `2`를 감성 이름에 대응시키면 `neutral`이 출력됩니다.

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

### 샘플 ID로 데이터 찾기

`"s001"` 키에 연결된 값은 샘플 정보를 담은 딕셔너리입니다. 거기에서 다시 `"text"`를 조회하면 `good product`가 출력됩니다.

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

컬럼 이름과 설명을 연결해 두면 `"score"`를 조회하여 `모델 점수`라는 설명을 얻을 수 있습니다.

```python
column_description = {
    "text": "입력 문장",
    "label": "정답 라벨",
    "score": "모델 점수",
}

print(column_description["score"])
```

데이터셋을 읽을 때 컬럼 이름의 의미를 따로 정리해 두면, 이후 전처리와 문서화가 쉬워집니다.

## 딕셔너리와 객체

딕셔너리는 Python 객체(object)의 한 종류입니다. 숫자, 문자열, 리스트, 함수도 객체이며, 딕셔너리는 그중 키와 값을 연결하는 매핑입니다. 중괄호를 사용하는 모양은 JSON 객체와 비슷하지만, Python의 객체 전체를 딕셔너리라고 부를 수는 없습니다.

딕셔너리의 키 접근과 객체의 속성(attribute) 접근도 다릅니다. 위 학생 정보의 이름은 `student["name"]`으로 읽습니다. 같은 딕셔너리에 `student.name`을 사용하면 이름을 읽을 수 없고 `AttributeError`가 발생합니다.

## 없는 키와 기본값

딕셔너리에서 없는 키를 바로 꺼내면 오류가 날 수 있습니다.

`student`에는 `"name"`과 `"score"`만 있습니다. 없는 키 `"label"`을 대괄호로 조회하면 `KeyError`가 발생합니다.

```python
student = {"name": "Kim", "score": 82.5}

print(student["label"])
```

`KeyError`는 요청한 키가 없다는 뜻입니다.

키가 없을 수도 있는 상황에서는 `get()`을 사용할 수 있습니다.

`get()`은 키가 없으면 지정한 기본값을 반환합니다. 다음 코드는 기본값을 생략한 결과 `None`과 기본값을 지정한 결과 `unknown`을 출력합니다.

```python
student = {"name": "Kim", "score": 82.5}

print(student.get("label"))
print(student.get("label", "unknown"))
```

기본값을 사용해도 딕셔너리에 그 키가 추가되지는 않습니다. 필수 항목이 빠졌다면 오류를 확인해 입력을 고쳐야 하고, 생략 가능한 항목이라면 `get()`으로 기본값을 정할 수 있습니다.

## 사례: 연속되지 않은 라벨 번호

감성 분류 결과가 `10`, `20`, `90`이라는 번호를 사용한다고 하겠습니다. 번호를 리스트 위치로 쓰면 빈 자리를 많이 만들어야 하지만, 딕셔너리에는 필요한 번호와 이름만 연결하면 됩니다. 다음 코드는 예측 번호 `90`에 해당하는 `neutral`과, 대응표에 없는 `30`에 대한 기본값 `unknown`을 출력합니다.

```python
label_map = {10: "negative", 20: "positive", 90: "neutral"}
prediction = 90

print(label_map[prediction])
print(label_map.get(30, "unknown"))
```

`prediction`을 `20`으로 바꾸면 첫 출력은 `positive`가 됩니다. `30`으로 바꾸면 첫 조회에서 `KeyError`가 발생하여 다음 출력까지 실행되지 않습니다. 번호와 라벨 이름의 대응, 누락된 번호를 처리하는 방식은 따로 정해야 합니다.

## 체크리스트

- 딕셔너리(dictionary)를 키와 값의 묶음으로 설명할 수 있다.
- 딕셔너리를 매핑(mapping) 구조로 설명할 수 있다.
- 딕셔너리를 사용 관점에서는 매핑(mapping), 구현 관점에서는 해시 기반 구조로 설명할 수 있다.
- 리스트는 위치로, 딕셔너리는 키로 값을 찾는다는 차이를 설명할 수 있다.
- `get()`이 키가 없을 수 있는 상황에서 유용함을 설명할 수 있다.
- 라벨 맵, 설정값, 샘플 ID 조회, 컬럼 설명 예시를 읽을 수 있다.
- 키가 없을 수 있는 상황에서 조회 방식을 구분할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 딕셔너리 생성, 키로 값에 접근, `items()`를 이용한 순회 예시 확인에 사용했다.
- Python Software Foundation, [Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. `dict`가 mutable mapping type이며 키를 통해 값을 찾는 구조라는 설명 확인에 사용했다.
- Python Software Foundation, [Glossary: dictionary, hashable](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. dictionary와 hashable 용어 정의를 확인하는 근거로 사용했다.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 객체의 identity/type/value와 hash 가능성 설명을 딕셔너리 키 제약의 배경으로 확인하는 근거로 사용했다.

# P2-8.6 보충학습: 클래스(class)와 객체(object)를 처음 만날 때

> Section ID: `P2-8.6`
> Version: `v2026.09.08`

`text.lower()`는 문자열을 소문자로 바꾸고, `scores.append(91)`은 리스트에 값을 추가합니다. 점(`.`) 앞에는 대상 객체가, 뒤에는 호출할 메서드(method)의 이름이 있습니다. 사용할 수 있는 동작은 대상의 타입에 따라 다릅니다.

## 객체와 타입

Python 객체(object)는 정체성(identity), 타입(type), 값(value)을 가집니다. 숫자, 문자열, 리스트, 딕셔너리도 객체입니다. 다음 코드는 네 값의 타입을 `<class 'int'>`, `<class 'str'>`, `<class 'list'>`, `<class 'dict'>`로 출력합니다.

```python
score = 82
text = "AI"
scores = [82, 75, 91]
student = {"name": "Kim", "score": 82}

print(type(score))
print(type(text))
print(type(scores))
print(type(student))
```

문자열 객체는 `strip()`과 `lower()`를 제공합니다. 입력 `" AI is Useful "`에 각각 적용하면 `AI is Useful`과 양끝 공백이 남은 ` ai is useful `이 출력됩니다.

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

두 메서드는 처리한 새 문자열을 반환하며 원래 `text`를 바꾸지 않습니다. 반면 리스트의 `append()`는 원래 리스트를 바꿉니다. `[82, 75]`에 `91`을 추가하면 `[82, 75, 91]`이 출력됩니다.

```python
scores = [82, 75]

scores.append(91)

print(scores)
```

`text.append(91)`은 문자열이 제공하지 않는 메서드를 요청하므로 `AttributeError`가 발생합니다.

## 클래스와 인스턴스

클래스(class)는 어떤 종류의 객체가 어떤 데이터와 동작을 가질지 정하는 정의입니다. 그 클래스로 만든 개별 객체를 인스턴스(instance)라고 합니다.

| 객체 예시 | 클래스 | 제공하는 메서드 예시 |
| --- | --- | --- |
| `"AI"` | `str` | `.lower()`, `.strip()` |
| `[1, 2, 3]` | `list` | `.append()`, `.extend()` |
| `{"a": 1}` | `dict` | `.get()`, `.items()` |

직접 정의한 `Sample` 클래스로 텍스트와 라벨을 가진 객체를 만들 수 있습니다. 다음 출력은 `AI is useful`, `positive`입니다.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

sample = Sample("AI is useful", "positive")

print(sample.text)
print(sample.label)
```

`Sample`은 클래스이고, `sample`은 만들어진 인스턴스를 가리키는 이름입니다. `sample.text`와 `sample.label`은 그 객체의 속성(attribute)을 읽습니다.

`__init__()`은 새 인스턴스를 초기화할 때 호출됩니다. 전달받은 `text`, `label`을 `self.text`, `self.label`에 저장하여 객체가 가진 데이터로 만듭니다.

## self와 개별 객체의 상태

`self`는 메서드를 실행하는 대상 인스턴스를 가리키는 관례적인 매개변수 이름입니다. `sample.method()`처럼 호출하면 대상 객체가 자동으로 전달되므로 호출할 때 `self`를 따로 쓰지 않습니다.

같은 클래스로 만든 두 객체도 각자 다른 값을 가질 수 있습니다. 다음 코드는 첫 객체의 라벨만 `positive`로 바꿉니다. 출력은 `positive`, `None`입니다.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

first = Sample("good product", None)
second = Sample("new review", None)
first.label = "positive"

print(first.label)
print(second.label)
```

첫 객체를 초기화할 때 `self`는 첫 객체를, 두 번째 객체를 초기화할 때는 두 번째 객체를 가리킵니다. 바깥에서 `first.label`로 읽는 속성이 그 객체의 메서드 안에서는 `self.label`입니다.

## 딕셔너리의 키와 객체의 속성

텍스트와 라벨은 딕셔너리로도 표현할 수 있습니다. 아래 코드는 키로 두 값을 찾아 `AI is useful`, `positive`를 출력합니다.

```python
sample = {
    "text": "AI is useful",
    "label": "positive",
}

print(sample["text"])
print(sample["label"])
```

앞의 `Sample` 객체는 `sample.text`로, 딕셔너리는 `sample["text"]`로 읽습니다. 딕셔너리도 객체의 한 종류이지만 키와 속성은 서로 다른 접근 방식입니다.

| 관점 | 딕셔너리 | 직접 정의한 Sample 인스턴스 |
| --- | --- | --- |
| 데이터 접근 | `sample["text"]` | `sample.text` |
| 데이터 저장 | 키에 값을 연결 | 속성에 값을 저장 |
| 처리 정의 | 별도 함수와 함께 사용 가능 | 클래스에 메서드를 정의 가능 |
| 예시 용도 | 설정값, JSON에서 읽은 데이터 | 데이터와 전용 동작을 가진 샘플 |

클래스 이름은 대상의 의미를 드러내지만, 이름만으로 속성의 타입이나 값이 자동 검증되지는 않습니다.

## 상태와 메서드

상태(state)는 객체가 현재 가진 값이고, 동작(behavior)은 그 값을 읽거나 바꾸는 처리입니다. `TextSample`은 텍스트와 라벨을 저장하고, `is_labeled()`로 라벨이 `None`인지 검사합니다. 다음 출력은 `AI is useful`, `True`입니다.

```python
class TextSample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

    def is_labeled(self):
        return self.label is not None

sample = TextSample("AI is useful", "positive")

print(sample.text)
print(sample.is_labeled())
```

`sample.label`을 `None`으로 바꾼 뒤 `sample.is_labeled()`를 다시 호출하면 `False`가 됩니다. 이 메서드는 현재 라벨이 `None`이 아닌지만 검사합니다. 빈 문자열 `""`도 `True`이므로 라벨 내용의 적절성까지 확인하는 검사는 아닙니다.

함수와 딕셔너리로도 같은 검사를 표현할 수 있습니다. 다음 코드는 딕셔너리의 라벨 `"positive"`를 검사하여 `True`를 출력합니다.

```python
def is_labeled(sample):
    return sample["label"] is not None

sample = {"text": "AI is useful", "label": "positive"}

print(is_labeled(sample))
```

`is_labeled(sample)`은 샘플을 함수에 전달하고, `sample.is_labeled()`는 샘플 객체에서 메서드를 찾아 호출합니다. 데이터를 키로 조회하는 작업에는 딕셔너리를, 상태와 전용 동작을 함께 정의하려는 작업에는 클래스를 사용할 수 있습니다.

## 함수 호출과 메서드 호출

문자열 `" AI "`를 정리하는 함수는 내부에서 문자열 메서드를 호출할 수 있습니다. 다음 출력은 `function: ai`, `method: AI`입니다.

```python
def clean_text(text):
    return text.strip().lower()

text = " AI "

print("function:", clean_text(text))
print("method:", text.strip())
```

`clean_text(text)`는 공백 제거와 소문자 변환을 함께 실행합니다. `text.strip()`은 공백만 제거하므로 대문자는 남습니다.

| 표현 | 대상과 동작 |
| --- | --- |
| `clean_text(text)` | 함수에 문자열을 전달 |
| `text.strip()` | 문자열 객체의 공백 제거 메서드 호출 |
| `sample.is_labeled()` | 샘플 객체의 라벨 검사 메서드 호출 |
| `model.predict(test_data)` | 모델 객체의 예측 메서드에 데이터 전달 |

## 사례: 학습 전후의 모델 상태

모델 객체는 설정값과 학습으로 얻은 값을 보관하고, 메서드는 그 상태를 바꾸거나 사용합니다. 다음 `SimplePassModel`은 통과한 점수 중 최솟값을 기준으로 저장하는 교육용 클래스입니다. 실제 머신러닝 라이브러리의 학습 알고리즘을 구현한 것은 아닙니다.

입력 `[(62, False), (75, True), (83, True)]`의 각 쌍은 점수와 통과 여부입니다. `fit()`은 통과 점수 `75`, `83` 중 최솟값 `75`를 저장하고, `predict()`는 확인할 점수 `[70, 78]`을 그 기준과 비교합니다.

```python
class SimplePassModel:
    def __init__(self):
        self.threshold = None

    def fit(self, train_data):
        # fit()은 학습 데이터를 읽고 객체 안의 상태를 저장합니다.
        passed_scores = [score for score, passed in train_data if passed]
        self.threshold = min(passed_scores)

    def predict(self, test_data):
        # predict()는 fit()이 저장한 상태를 사용합니다.
        if self.threshold is None:
            raise ValueError("fit()을 먼저 호출해야 합니다.")
        return [score >= self.threshold for score in test_data]


train_data = [(62, False), (75, True), (83, True)]
test_data = [70, 78]

model = SimplePassModel()

print("before fit:", model.threshold)
model.fit(train_data)
print("after fit:", model.threshold)
predictions = model.predict(test_data)
print("predictions:", predictions)
```

출력은 다음과 같습니다.

```text
before fit: None
after fit: 75
predictions: [False, True]
```

학습 전에는 `model.threshold`가 `None`이고, `fit()` 실행 후에는 `75`입니다. `predict()`는 저장된 기준을 읽으므로 같은 `model` 객체를 계속 사용해야 합니다. 새 객체를 만들고 바로 `predict()`를 호출하면 기준이 없어 코드에 정의한 `ValueError`가 발생합니다.

학습 입력의 `(75, True)`를 `(68, True)`로 바꾸어 실행하면 기준은 `68`, 예측 결과는 `[True, True]`가 됩니다. 확인할 점수는 그대로인데 모델에 저장된 상태가 바뀌어 판정도 달라집니다.

이 예제는 통과 점수가 하나 이상 있는 입력을 전제로 합니다. 통과 항목이 없으면 `min()`을 적용할 값이 없어 `ValueError`가 발생합니다. 또한 미통과 점수는 기준 계산에 사용하지 않으므로, 복잡한 실제 분류 문제에 그대로 적용할 수 있는 학습 규칙은 아닙니다.

## 체크리스트

- 객체(object)를 Python이 다루는 값의 실제 대상으로 설명할 수 있다.
- 클래스(class)를 객체를 만들기 위한 정의로 설명할 수 있다.
- 메서드(method)를 객체에 붙어 호출되는 함수 형태로 설명할 수 있다.
- 딕셔너리와 클래스 기반 객체의 차이를 입문 수준에서 설명할 수 있다.
- 상태(state)와 동작(behavior)을 함께 묶는다는 말을 예시로 설명할 수 있다.
- `function(value)`와 `value.method()`의 호출 중심 차이를 설명할 수 있다.
- `self`를 객체 자신을 가리키는 이름으로 설명할 수 있다.
- 클래스가 항상 필요한 것은 아니며, 함수와 딕셔너리로 충분한 경우도 있음을 설명할 수 있다.
- AI 라이브러리의 `model.fit()`, `model.predict()`를 객체와 메서드 관점으로 읽을 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [Classes](https://docs.python.org/3/tutorial/classes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 클래스 객체, 인스턴스 객체, 속성 참조, 메서드 객체 설명을 클래스·객체·메서드 입문 설명의 공식 근거로 사용했다.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 객체가 identity, type, value를 가진다는 설명과 타입별 동작 차이의 배경 근거로 사용했다.
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. `value.method()` 호출을 객체에 붙은 함수 형태로 읽는 설명 확인에 사용했다.

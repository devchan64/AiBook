# P2-8.6 보충학습: 클래스(class)와 객체(object)를 처음 만날 때

P2-8.5에서는 함수(function)를 작은 재사용 단위로 봤습니다. 함수는 입력을 받고, 처리하고, 결과를 돌려줍니다. 그런데 Python 코드를 읽다 보면 함수 호출과 비슷하지만 조금 다른 표현을 자주 만납니다.

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

`strip()`과 `lower()`는 함수처럼 괄호로 호출되지만, 앞에 `text.`가 붙어 있습니다. 이런 표현을 이해하려면 객체(object), 메서드(method), 클래스(class)를 아주 가볍게 알아야 합니다.

이 절은 보충학습입니다. 클래스의 전체 문법을 배우는 절이 아닙니다. 이후 라이브러리 코드를 읽을 때 `value.method()`, `model.fit()`, `dataset.map()` 같은 표현을 보고 멈추지 않도록 최소한의 기준을 잡는 것이 목적입니다.

보충학습이므로 설명은 조금 자세히 둡니다. 다만 목표는 클래스를 자유롭게 설계하는 것이 아니라, 앞으로 만날 Python 라이브러리 코드의 모양을 읽는 것입니다.

## 이 절의 범위

이 절은 Python 객체와 클래스의 입문용 감각만 다룹니다.

여기서는 다음 질문에 답합니다.

- 객체(object)는 무엇인가?
- 클래스(class)는 무엇인가?
- 메서드(method)는 함수(function)와 어떻게 다른가?
- Python에서 값(value), 타입(type), 클래스(class)는 어떻게 연결되는가?
- 왜 라이브러리 코드에서 `model.fit()` 같은 표현이 자주 보이는가?

이 절은 상속(inheritance), 캡슐화(encapsulation), 다형성(polymorphism), 매직 메서드(magic method), 클래스 변수(class variable), 인스턴스 변수(instance variable)의 상세 규칙을 다루지 않습니다.

## 이 절의 목표

- 객체(object)를 값과 동작을 함께 가진 대상으로 설명할 수 있습니다.
- 클래스(class)를 객체를 만들기 위한 정의로 설명할 수 있습니다.
- 메서드(method)를 객체에 붙어 호출되는 함수 형태로 읽을 수 있습니다.
- `function(value)`와 `value.method()`의 차이를 입문 수준에서 설명할 수 있습니다.
- AI 라이브러리에서 보이는 `model.fit()`, `model.predict()` 같은 표현을 클래스와 메서드 관점으로 읽을 수 있습니다.

## Python에서는 많은 것이 객체다

Python 공식 문서는 객체(object)를 identity, type, value를 가진 대상으로 설명합니다. 입문 단계에서는 다음처럼 이해해도 충분합니다.

객체는 Python이 다루는 값의 실제 대상입니다.

숫자, 문자열, 리스트, 딕셔너리도 모두 객체로 볼 수 있습니다.

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

여기서 중요한 것은 `type()`입니다. 값마다 타입(type)이 있고, Python에서는 그 타입이 어떤 동작을 제공할지에 영향을 줍니다.

예를 들어 문자열은 문자열에 맞는 메서드를 제공합니다.

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

리스트는 리스트에 맞는 메서드를 제공합니다.

```python
scores = [82, 75]

scores.append(91)

print(scores)
```

문자열에는 `strip()`이 있고, 리스트에는 `append()`가 있습니다. 값의 타입이 다르기 때문에 사용할 수 있는 동작도 다릅니다.

## 클래스는 객체를 만들기 위한 정의다

클래스(class)는 객체를 만들기 위한 정의입니다. 조금 더 쉽게 말하면, 어떤 종류의 객체가 어떤 데이터와 동작을 가질지 정하는 틀입니다.

Python의 기본 타입도 이런 관점으로 볼 수 있습니다.

| 값 | 타입 또는 클래스 | 자주 쓰는 동작 |
| --- | --- | --- |
| `"AI"` | `str` | `.lower()`, `.strip()` |
| `[1, 2, 3]` | `list` | `.append()`, `.extend()` |
| `{"a": 1}` | `dict` | `.get()`, `.items()` |

사용자가 직접 클래스를 만들 수도 있습니다.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

sample = Sample("AI is useful", "positive")

print(sample.text)
print(sample.label)
```

이 코드는 `Sample`이라는 클래스를 정의하고, `sample`이라는 객체를 만듭니다. `sample.text`와 `sample.label`은 객체가 가진 값입니다.

이 절에서는 `__init__`의 자세한 규칙을 외울 필요가 없습니다. 핵심은 클래스가 객체를 만들기 위한 정의이고, 객체는 자기 데이터를 가질 수 있다는 점입니다.

## 딕셔너리와 클래스는 어떻게 다르게 느껴지는가

P2-8.3에서 딕셔너리(dictionary)는 키(key)로 값을 찾는 구조라고 했습니다. 사실 작은 데이터 한 건은 딕셔너리로도 표현할 수 있습니다.

```python
sample = {
    "text": "AI is useful",
    "label": "positive",
}

print(sample["text"])
print(sample["label"])
```

같은 데이터를 클래스로 표현하면 다음처럼 보입니다.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

sample = Sample("AI is useful", "positive")

print(sample.text)
print(sample.label)
```

두 코드는 모두 텍스트와 라벨을 담습니다. 하지만 읽는 감각은 다릅니다.

| 관점 | 딕셔너리(dictionary) | 클래스(class)로 만든 객체 |
| --- | --- | --- |
| 중심 생각 | 키로 값을 찾는다 | 어떤 종류의 대상을 만든다 |
| 접근 방식 | `sample["text"]` | `sample.text` |
| 구조의 명시성 | 키 이름이 실행 중에 확인됨 | 클래스 이름이 대상의 의미를 드러냄 |
| 동작 추가 | 별도 함수와 함께 사용 | 메서드(method)를 객체 안에 둘 수 있음 |
| 적합한 상황 | 간단한 데이터, JSON, 설정값 | 상태와 동작을 함께 다루는 대상 |

초반에는 딕셔너리가 더 쉽습니다. 실제 데이터 파일이나 API 응답도 딕셔너리처럼 읽히는 경우가 많습니다. 그래서 이 책도 먼저 딕셔너리를 배웠습니다.

클래스가 필요해지는 순간은 “데이터만 있는 것이 아니라, 그 데이터와 함께 실행할 동작도 묶고 싶을 때”입니다.

## 상태(state)와 동작(behavior)을 함께 묶는다

객체를 설명할 때 상태(state)와 동작(behavior)이라는 말을 자주 씁니다.

상태(state)는 객체가 현재 가지고 있는 값입니다.

동작(behavior)은 그 객체가 할 수 있는 일입니다.

다음 예시는 텍스트 샘플이 자기 상태를 가지고, 자기 상태를 검사하는 동작도 가집니다.

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

여기서 `sample.text`와 `sample.label`은 객체의 상태입니다. `sample.is_labeled()`는 객체의 동작입니다.

함수로도 같은 일을 할 수 있습니다.

```python
def is_labeled(sample):
    return sample["label"] is not None

sample = {"text": "AI is useful", "label": "positive"}

print(is_labeled(sample))
```

둘 중 무엇이 항상 더 좋다고 말할 수는 없습니다. 중요한 것은 구조의 목적입니다.

| 목적 | 단순한 접근 |
| --- | --- |
| JSON 같은 데이터를 그대로 읽는다 | 딕셔너리 |
| 여러 값을 키로 빠르게 찾는다 | 딕셔너리 |
| 데이터와 동작을 하나의 대상으로 묶는다 | 클래스 |
| 라이브러리가 상태를 가진 대상을 제공한다 | 클래스 기반 객체 |

AI 실습 초반에는 딕셔너리와 함수만으로도 충분한 경우가 많습니다. 하지만 라이브러리를 사용하다 보면 모델, 데이터셋, 토크나이저, 옵티마이저 같은 대상이 객체로 제공되는 경우가 많습니다. 이런 대상은 내부 상태를 가지고 있고, 그 상태를 바탕으로 메서드를 실행합니다.

## 메서드는 객체에 붙어 호출되는 함수처럼 보인다

함수(function)는 보통 다음처럼 호출합니다.

```python
def clean_text(text):
    return text.strip().lower()

print(clean_text(" AI "))
```

메서드(method)는 객체에 붙어 호출됩니다.

```python
text = " AI "

print(text.strip())
```

두 표현은 모두 동작을 실행합니다. 하지만 호출의 중심이 다릅니다.

| 표현 | 호출의 중심 | 읽는 법 |
| --- | --- | --- |
| `clean_text(text)` | 함수 이름 | `text`를 함수에 넣어 처리한다 |
| `text.strip()` | 객체 `text` | `text` 객체가 제공하는 `strip()` 동작을 호출한다 |

직접 만든 클래스에도 메서드를 넣을 수 있습니다.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

    def has_label(self):
        return self.label is not None

sample = Sample("AI is useful", "positive")

print(sample.has_label())
```

`sample.has_label()`은 `sample` 객체에 붙어 호출되는 메서드입니다. 함수처럼 보이지만, 호출 대상 객체가 앞에 있습니다.

메서드를 읽을 때는 다음 질문이 도움이 됩니다.

1. 점(`.`) 앞의 대상은 무엇인가?
2. 그 대상은 어떤 상태를 가지고 있는가?
3. 점 뒤의 메서드는 그 상태를 읽거나 바꾸는가?
4. 괄호 안에 추가로 넘기는 값은 무엇인가?

예를 들어 `model.predict(test_data)`를 보면 이렇게 읽을 수 있습니다.

| 질문 | 답 |
| --- | --- |
| 점 앞의 대상 | `model` |
| 대상의 의미 | 학습된 모델 객체일 가능성이 있음 |
| 점 뒤의 메서드 | `predict()` |
| 넘기는 값 | `test_data` |
| 전체 해석 | 모델 객체가 테스트 데이터에 대해 예측 동작을 수행함 |

## self는 객체 자신을 가리키는 이름이다

Python 클래스 예제에서 `self`라는 이름을 자주 봅니다.

```python
class Sample:
    def __init__(self, text):
        self.text = text
```

입문 단계에서는 `self`를 “지금 만들어지거나 사용되는 객체 자신”으로 이해하면 됩니다. `self.text = text`는 이 객체 안에 `text`라는 값을 저장한다는 뜻입니다.

다른 언어를 먼저 배운 사람은 `this`와 비슷한 역할로 이해할 수 있습니다. 다만 Python에서는 메서드 정의에 `self`를 명시적으로 적는다는 점이 눈에 띕니다.

이 절에서는 다음 정도만 기억합니다.

- `self`는 관례적인 이름입니다.
- 메서드 안에서 객체 자신의 값을 읽거나 바꿀 때 사용합니다.
- `sample.has_label()`처럼 호출할 때는 `self`를 직접 넘기지 않습니다.

`self`가 낯설다면 다음 두 줄을 비교해 볼 수 있습니다.

```python
sample = Sample("AI is useful", "positive")

print(sample.label)
```

`sample.label`은 `sample` 객체 안에 저장된 `label` 값을 읽는 표현입니다. 클래스 안에서는 그 객체를 `self`라는 이름으로 부릅니다.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label
```

즉 바깥에서 볼 때는 `sample.label`이고, 클래스 안에서 볼 때는 `self.label`입니다. 처음에는 이 정도의 대응만 기억해도 충분합니다.

## 클래스는 항상 필요한가

아닙니다. Python을 배운다고 해서 모든 코드를 클래스로 만들어야 하는 것은 아닙니다.

입문 단계에서는 다음 기준이 더 실용적입니다.

| 상황 | 먼저 고려할 방식 |
| --- | --- |
| 값 하나를 계산한다 | 함수 |
| 여러 값을 순서대로 다룬다 | 리스트 |
| 이름으로 값을 찾는다 | 딕셔너리 |
| 반복해서 같은 처리를 한다 | 반복문과 함수 |
| 상태와 동작을 함께 가진 대상을 만든다 | 클래스 |

클래스는 강력하지만, 너무 일찍 사용하면 구조가 무거워질 수 있습니다. 반대로 라이브러리 코드를 읽을 때는 클래스와 객체를 피할 수 없습니다. 따라서 이 절의 목표는 “모든 것을 클래스로 만들기”가 아니라, “클래스로 만들어진 코드를 읽을 수 있기”입니다.

## AI 라이브러리에서 왜 클래스와 메서드가 자주 보이는가

AI 실습에서는 다음과 같은 코드를 자주 보게 됩니다.

```python
model.fit(train_data)
predictions = model.predict(test_data)
```

이 코드는 실제 라이브러리마다 다르지만, 읽는 방식은 비슷합니다.

| 표현 | 입문용 해석 |
| --- | --- |
| `model` | 모델 객체 |
| `.fit()` | 학습을 수행하는 메서드 |
| `.predict()` | 예측을 수행하는 메서드 |
| `train_data`, `test_data` | 메서드에 넘기는 데이터 |

왜 이런 방식이 쓰일까요? 모델은 단순한 함수 하나가 아니라 여러 상태를 가질 수 있기 때문입니다. 학습된 파라미터, 설정값, 내부 구성, 전처리 정보가 객체 안에 함께 있을 수 있습니다. 그래서 라이브러리는 모델을 객체로 만들고, 그 객체에 `fit()`, `predict()`, `save()` 같은 메서드를 붙여 사용하게 합니다.

이 관점은 이후 머신러닝 라이브러리나 딥러닝 프레임워크를 읽을 때 중요합니다.

- 함수는 하나의 처리를 이름으로 분리합니다.
- 객체는 상태와 동작을 함께 묶을 수 있습니다.
- 클래스는 그런 객체를 만들기 위한 정의입니다.
- 메서드는 객체에 붙어 호출되는 동작입니다.

다음처럼 읽으면 됩니다.

```python
model.fit(train_data)
```

`model`이라는 객체가 있고, 그 객체가 `fit()`이라는 메서드를 실행합니다. 이때 `fit()`은 단순 계산만 하는 것이 아니라, 모델 객체 안의 상태를 바꿀 수 있습니다. 예를 들어 학습된 파라미터가 객체 내부에 저장될 수 있습니다.

```python
predictions = model.predict(test_data)
```

`predict()`는 이미 학습된 모델 객체의 상태를 사용해 예측 결과를 만듭니다. 그래서 함수 하나만 보는 것보다, 객체가 어떤 상태를 가지고 있는지 함께 생각해야 합니다.

이 관점은 이후 머신러닝에서 중요해집니다.

- 학습 전 모델과 학습 후 모델은 같은 객체처럼 보여도 내부 상태가 달라질 수 있습니다.
- `fit()`은 상태를 바꾸는 메서드일 수 있습니다.
- `predict()`는 상태를 사용해 결과를 만드는 메서드일 수 있습니다.
- `save()`는 상태를 파일로 저장하는 메서드일 수 있습니다.

## 이 절에서 기억할 관점

클래스는 어려운 문법으로 시작하지 않는 편이 좋습니다. 먼저 Python 코드에서 보이는 호출 모양을 구분합니다.

`function(value)`는 값을 함수에 넣는 모양입니다.

`value.method()`는 값 또는 객체가 제공하는 동작을 호출하는 모양입니다.

AI 라이브러리에서 `model.fit()` 같은 표현을 만나면 “모델 객체가 학습 메서드를 호출한다”라고 읽을 수 있습니다. 이것만으로도 많은 코드를 처음 읽을 때 멈추지 않을 수 있습니다.

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

- Python Software Foundation, [Classes](https://docs.python.org/3/tutorial/classes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-25.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-25.
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-25.

# P2-8.6 보충학습: 클래스(class)와 객체(object)를 처음 만날 때

> Section ID: `P2-8.6`
> Version: `v2026.07.12`

P2-8.5에서는 함수(function)를 작은 재사용 단위로 봤습니다. 함수는 입력을 받고, 처리하고, 결과를 돌려줍니다. 그런데 Python 코드를 읽다 보면 함수 호출과 비슷하지만 조금 다른 표현을 자주 만납니다.

여기서는 `클래스(class)`, `객체(object)`, `메서드(method)`를 읽는 기본 보충 설명을 제공합니다. 이 보충학습은 `value.method()`와 `model.fit()` 같은 호출 모양을 읽는 기준을 정리합니다. `값(value)`, `타입(type)`, `딕셔너리(dictionary)` 자체의 대표 설명은 P2-8.1, P2-8.3과 [개념사전](../../../reference/concept-glossary.md)에 두고, 여기서는 그 위에 클래스와 객체를 얹어 읽습니다.

문제 상황: 점(`.`)이 붙은 호출이 일반 함수 호출과 어떻게 다른지 가장 작은 예로 보고 싶습니다.
입력(input): 문자열 `text = " AI is Useful "`.
기대 출력(output): 공백이 제거된 문자열과 소문자로 바뀐 문자열.
확인할 개념: `value.method()` 형태는 값이나 객체가 제공하는 동작을 호출하는 모양입니다.

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

`strip()`과 `lower()`는 함수처럼 괄호로 호출되지만, 앞에 `text.`가 붙어 있습니다. 이런 표현을 이해하려면 객체(object), 메서드(method), 클래스(class)를 아주 가볍게 알아야 합니다.

여기서는 클래스의 전체 문법을 배우지 않습니다. 이후 라이브러리 코드를 읽을 때 `value.method()`, `model.fit()`, `dataset.map()` 같은 표현을 보고 멈추지 않도록 최소한의 기준을 잡습니다.

여기서는 `왜 문자열은 .lower()를 쓰고, 리스트는 .append()를 쓰지` 같은 질문을 `객체가 자기 타입에 맞는 동작을 메서드 형태로 제공한다`는 기준으로 정리합니다.

보충학습이므로 설명은 조금 자세히 둡니다. 다만 목표는 클래스를 자유롭게 설계하는 것이 아니라, 앞으로 만날 Python 라이브러리 코드의 모양을 읽는 것입니다.

| 용어 | 이 절에서 먼저 잡을 뜻 |
| --- | --- |
| 객체(object) | 값과 그 값에 연결된 동작을 함께 가진 다루는 대상입니다. |
| 클래스(class) | 그런 객체를 만들기 위한 정의 또는 틀입니다. |
| 메서드(method) | 객체에 붙어 호출되는 함수 형태의 동작입니다. |
| 속성(attribute) | 객체가 가지고 있는 값이나 이름표입니다. |
| `value.method()` | 특정 값이나 객체가 제공하는 동작을 호출하는 모양입니다. |

## 이 보충학습의 범위

여기서는 Python 객체와 클래스의 입문용 감각만 다룹니다. 값·타입·함수의 기본 설명은 P2-8.1과 P2-8.5를 기준으로 다시 연결하고, 참조와 복사처럼 객체 공유가 만드는 효과는 P2-8.7에서 따로 회수합니다.

여기서 먼저 해결할 질문은 이것입니다. `함수 호출처럼 보이지만 앞에 점(.)이 붙은 표현을 어떤 기준으로 읽어야 하는가`입니다.

그래서 이 보충학습은 다음 질문에 답합니다.

- 객체(object)는 무엇인가?
- 클래스(class)는 무엇인가?
- 메서드(method)는 함수(function)와 어떻게 다른가?
- Python에서 값(value), 타입(type), 클래스(class)는 어떻게 연결되는가?
- 왜 라이브러리 코드에서 `model.fit()` 같은 표현이 자주 보이는가?

여기서는 상속(inheritance), 캡슐화(encapsulation), 다형성(polymorphism), 매직 메서드(magic method), 클래스 변수(class variable), 인스턴스 변수(instance variable)의 상세 규칙을 다루지 않습니다.

이 절 다음 흐름도 단순합니다.

- `P2-8.7`에서는 객체 공유와 참조가 만드는 효과를 다시 보게 됩니다.
- 이후 AI 라이브러리에서 `model.fit()`, `dataset.map()`, `tokenizer.encode()` 같은 표현을 읽을 때 같은 기준이 반복됩니다.

## 이 보충학습의 목표

- 객체(object)를 값과 동작을 함께 가진 대상으로 설명할 수 있습니다.
- 클래스(class)를 객체를 만들기 위한 정의로 설명할 수 있습니다.
- 메서드(method)를 객체에 붙어 호출되는 함수 형태로 읽을 수 있습니다.
- `function(value)`와 `value.method()`의 차이를 입문 수준에서 설명할 수 있습니다.
- AI 라이브러리에서 보이는 `model.fit()`, `model.predict()` 같은 표현을 클래스와 메서드 관점으로 읽을 수 있습니다.

## 먼저 붙잡을 기준

이 보충학습에서 가장 먼저 붙잡아야 할 기준은 `점(.)이 붙은 호출은 객체가 제공하는 동작`이라는 점입니다.

| 표현 | 먼저 읽는 방식 |
| --- | --- |
| `text.lower()` | 문자열 객체가 제공하는 동작 |
| `scores.append(91)` | 리스트 객체가 제공하는 동작 |
| `model.fit(X, y)` | 모델 객체가 학습 동작을 제공하는 형태 |
| `sample.text` | 객체가 가진 값이나 속성(attribute) |

즉 이 절의 핵심은 클래스를 자유롭게 설계하는 것이 아니라, `value.method()`와 `object.attribute`를 보고 멈추지 않는 기준을 만드는 일입니다.

## 세 가지 기준

| 기준 | 왜 중요한가 | 이 절에서 필요한 이해 수준 |
| --- | --- | --- |
| 객체는 값과 동작을 함께 가진 하나의 다루는 대상이다 | `value.method()` 같은 호출 모양을 읽는 출발점이 된다 | 값과 메서드를 함께 가진 대상으로 이해한다 |
| 클래스는 그런 객체를 만들기 위한 정의다 | 속성과 메서드가 왜 한 묶음으로 보이는지 설명해 준다 | 설계도 같은 정의라고 설명할 수 있다 |
| AI 라이브러리에서 이런 표현이 자주 보이는 이유는 모델과 데이터셋을 한 묶음으로 다루기 좋기 때문이다 | `model.fit()` 같은 코드를 문법보다 구조로 읽게 해 준다 | 모델, 데이터셋, 설정을 객체처럼 다룬다고 이해한다 |

## Python에서는 많은 것이 객체다

Python 공식 문서는 객체(object)를 identity, type, value를 가진 대상으로 설명합니다. 여기서는 다음처럼 이해하면 됩니다.

객체는 Python이 다루는 값의 실제 대상입니다.

숫자, 문자열, 리스트, 딕셔너리도 모두 객체로 볼 수 있습니다.

문제 상황: 서로 다른 값들이 모두 Python 객체로 다뤄진다는 점을 타입 출력으로 확인하고 싶습니다.
입력(input): 정수, 문자열, 리스트, 딕셔너리 값.
기대 출력(output): 각 값의 타입이 차례대로 출력됩니다.
확인할 개념: Python에서는 다양한 값이 모두 객체이며, 타입이 그 성격을 드러냅니다.

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

문제 상황: 문자열 객체가 제공하는 메서드가 어떤 식으로 호출되는지 보고 싶습니다.
입력(input): 공백과 대문자가 섞인 문자열 `text`.
기대 출력(output): `strip()`과 `lower()` 결과.
확인할 개념: 객체는 자기 타입에 맞는 동작을 메서드 형태로 제공합니다.

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

리스트는 리스트에 맞는 메서드를 제공합니다.

문제 상황: 리스트 객체도 자기 타입에 맞는 메서드를 가진다는 점을 확인하고 싶습니다.
입력(input): 리스트 `scores = [82, 75]`와 추가할 값 `91`.
기대 출력(output): 값이 추가된 리스트.
확인할 개념: 타입이 다르면 사용할 수 있는 메서드도 달라집니다.

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

독자가 직접 클래스를 만들 수도 있습니다.

문제 상황: 클래스를 정의하고 그 클래스로 객체를 만드는 가장 작은 예를 보고 싶습니다.
입력(input): 텍스트와 라벨 값 `"AI is useful"`, `"positive"`.
기대 출력(output): 객체의 `text`, `label` 속성이 출력됩니다.
확인할 개념: 클래스는 객체를 만들기 위한 정의이고, 객체는 자기 데이터를 가질 수 있습니다.

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

여기서는 `__init__`의 자세한 규칙을 외울 필요가 없습니다. 핵심은 클래스가 객체를 만들기 위한 정의이고, 객체는 자기 데이터를 가질 수 있다는 점입니다.

## 딕셔너리와 클래스는 어떻게 다르게 느껴지는가

P2-8.3에서 딕셔너리(dictionary)는 키(key)로 값을 찾는 구조라고 했습니다. 사실 작은 데이터 한 건은 딕셔너리로도 표현할 수 있습니다.

문제 상황: 텍스트와 라벨이 들어 있는 작은 데이터를 딕셔너리로 표현한 예를 보고 싶습니다.
입력(input): `text`, `label` 키를 가진 `sample` 딕셔너리.
기대 출력(output): `sample["text"]`, `sample["label"]` 값이 출력됩니다.
확인할 개념: 딕셔너리는 키로 값을 찾는 가장 직접적인 데이터 표현입니다.

```python
sample = {
    "text": "AI is useful",
    "label": "positive",
}

print(sample["text"])
print(sample["label"])
```

같은 데이터를 클래스로 표현하면 다음처럼 보입니다.

문제 상황: 바로 앞의 같은 데이터를 클래스 기반 객체로 표현했을 때 모양이 어떻게 달라지는지 비교하고 싶습니다.
입력(input): `Sample` 클래스와 생성 인자 `"AI is useful"`, `"positive"`.
기대 출력(output): `sample.text`, `sample.label` 값이 출력됩니다.
확인할 개념: 클래스 기반 객체는 키 조회 대신 속성 접근으로 데이터를 읽을 수 있습니다.

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

문제 상황: 객체가 값과 동작을 함께 가진다는 점을 클래스 예제로 확인하고 싶습니다.
입력(input): 텍스트와 라벨을 가진 `TextSample` 객체.
기대 출력(output): 객체의 `text` 값과 `is_labeled()` 결과.
확인할 개념: 상태는 객체가 가진 값이고, 동작은 그 객체가 제공하는 메서드입니다.

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

문제 상황: 같은 라벨 존재 검사도 함수와 딕셔너리 조합으로 표현할 수 있음을 보고 싶습니다.
입력(input): `label` 키를 가진 샘플 딕셔너리.
기대 출력(output): `is_labeled(sample)` 결과 `True`.
확인할 개념: 클래스가 아니어도 함수와 딕셔너리로 비슷한 처리 구조를 만들 수 있습니다.

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

문제 상황: 독립 함수 호출이 어떤 모양인지 먼저 보고 메서드 호출과 비교하고 싶습니다.
입력(input): 문자열 `" AI "`.
기대 출력(output): 정리된 문자열.
확인할 개념: `function(value)`는 값을 함수에 넣어 처리하는 호출 형태입니다.

```python
def clean_text(text):
    return text.strip().lower()

print(clean_text(" AI "))
```

메서드(method)는 객체에 붙어 호출됩니다.

문제 상황: 같은 문자열 정리도 메서드 호출로는 어떤 모양인지 보고 싶습니다.
입력(input): 문자열 `text = " AI "`.
기대 출력(output): `text.strip()` 결과.
확인할 개념: 메서드는 점 앞의 객체를 중심으로 호출됩니다.

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

문제 상황: 직접 만든 객체도 자기 메서드를 가질 수 있음을 확인하고 싶습니다.
입력(input): `Sample` 객체와 메서드 `has_label()`.
기대 출력(output): `sample.has_label()` 결과 `True`.
확인할 개념: 메서드는 사용자 정의 클래스 안에도 둘 수 있습니다.

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

문제 상황: 클래스 안에서 `self`가 어떤 자리를 차지하는지 가장 작은 예로 보고 싶습니다.
입력(input): `Sample` 클래스의 `__init__` 메서드와 입력 `text`.
기대 출력(output): 객체 내부에 `self.text`를 저장하는 클래스 정의.
확인할 개념: `self`는 메서드 안에서 객체 자신을 가리키는 관례적 이름입니다.

```python
class Sample:
    def __init__(self, text):
        self.text = text
```

여기서는 `self`를 “지금 만들어지거나 사용되는 객체 자신”으로 이해하면 됩니다. `self.text = text`는 이 객체 안에 `text`라는 값을 저장한다는 뜻입니다.

다른 언어를 먼저 배운 사람은 `this`와 비슷한 역할로 이해할 수 있습니다. 다만 Python에서는 메서드 정의에 `self`를 명시적으로 적는다는 점이 눈에 띕니다.

여기서는 아래 기준만 먼저 기억합니다.

- `self`는 관례적인 이름입니다.
- 메서드 안에서 객체 자신의 값을 읽거나 바꿀 때 사용합니다.
- `sample.has_label()`처럼 호출할 때는 `self`를 직접 넘기지 않습니다.

`self`가 낯설다면 다음 두 줄을 비교해 볼 수 있습니다.

문제 상황: 클래스 밖에서 보는 속성 접근과 클래스 안에서의 `self` 대응을 연결해 보고 싶습니다.
입력(input): `Sample("AI is useful", "positive")`로 만든 객체 `sample`.
기대 출력(output): `sample.label` 값이 출력됩니다.
확인할 개념: 바깥에서는 `sample.label`, 클래스 안에서는 같은 자리를 `self.label`로 읽습니다.

```python
sample = Sample("AI is useful", "positive")

print(sample.label)
```

`sample.label`은 `sample` 객체 안에 저장된 `label` 값을 읽는 표현입니다. 클래스 안에서는 그 객체를 `self`라는 이름으로 부릅니다.

문제 상황: 클래스 안에서 속성을 저장할 때 `self.label`처럼 쓰는 정의를 다시 확인하고 싶습니다.
입력(input): `Sample` 클래스의 `__init__` 메서드.
기대 출력(output): `self.text`, `self.label`을 저장하는 클래스 정의.
확인할 개념: 클래스 내부에서는 객체 자신의 속성을 `self`를 통해 다룹니다.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label
```

즉 바깥에서 볼 때는 `sample.label`이고, 클래스 안에서 볼 때는 `self.label`입니다. 우선 이 대응만 정확히 잡아 두면 됩니다.

## 클래스는 항상 필요한가

아닙니다. Python을 배운다고 해서 모든 코드를 클래스로 만들어야 하는 것은 아닙니다.

여기서는 다음 기준이 더 실용적입니다.

| 상황 | 먼저 고려할 방식 |
| --- | --- |
| 값 하나를 계산한다 | 함수 |
| 여러 값을 순서대로 다룬다 | 리스트 |
| 이름으로 값을 찾는다 | 딕셔너리 |
| 반복해서 같은 처리를 한다 | 반복문과 함수 |
| 상태와 동작을 함께 가진 대상을 만든다 | 클래스 |

클래스는 강력하지만, 너무 일찍 사용하면 구조가 무거워질 수 있습니다. 반대로 라이브러리 코드를 읽을 때는 클래스와 객체를 피할 수 없습니다. 여기서는 “모든 것을 클래스로 만들기”보다 “클래스로 만들어진 코드를 읽을 수 있기”에 집중합니다.

## AI 라이브러리에서 왜 클래스와 메서드가 자주 보이는가

AI 실습에서는 다음과 같은 코드를 자주 보게 됩니다.

문제 상황: AI 라이브러리에서 자주 보이는 메서드 호출 모양을 가장 단순하게 보고 싶습니다.
입력(input): `model`, `train_data`, `test_data`.
기대 출력(output): `model.fit(...)`, `model.predict(...)` 호출 예시.
확인할 개념: 라이브러리 객체는 상태와 동작을 함께 가지므로 메서드 호출 형태가 자주 나타납니다.

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

여기서는 다음처럼 읽습니다.

문제 상황: `fit()` 메서드 호출을 한 줄짜리 예시로 다시 고정해 보고 싶습니다.
입력(input): `model`, `train_data`.
기대 출력(output): `model.fit(train_data)` 호출 예시.
확인할 개념: 메서드 호출은 객체가 자기 상태를 바꾸거나 활용하는 동작일 수 있습니다.

```python
model.fit(train_data)
```

`model`이라는 객체가 있고, 그 객체가 `fit()`이라는 메서드를 실행합니다. 이때 `fit()`은 단순 계산만 하는 것이 아니라, 모델 객체 안의 상태를 바꿀 수 있습니다. 예를 들어 학습된 파라미터가 객체 내부에 저장될 수 있습니다.

문제 상황: 예측 메서드는 학습된 객체 상태를 사용한다는 점을 한 줄 예로 보고 싶습니다.
입력(input): `model`, `test_data`.
기대 출력(output): `predictions = model.predict(test_data)` 호출 예시.
확인할 개념: 메서드는 객체 상태를 활용해 결과를 만들 수 있습니다.

```python
predictions = model.predict(test_data)
```

`predict()`는 이미 학습된 모델 객체의 상태를 사용해 예측 결과를 만듭니다. 그래서 함수 하나만 보는 것보다, 객체가 어떤 상태를 가지고 있는지 함께 생각해야 합니다.

이 관점은 이후 머신러닝에서 중요해집니다.

- 학습 전 모델과 학습 후 모델은 같은 객체처럼 보여도 내부 상태가 달라질 수 있습니다.
- `fit()`은 상태를 바꾸는 메서드일 수 있습니다.
- `predict()`는 상태를 사용해 결과를 만드는 메서드일 수 있습니다.
- `save()`는 상태를 파일로 저장하는 메서드일 수 있습니다.

## 사례 및 예시

### 사례 1. `model.fit()`은 왜 일반 함수처럼 보이지 않는가

한 학습자가 머신러닝 예제에서 `model.fit(train_data)`와 `model.predict(test_data)`를 처음 봤다고 하겠습니다. 사람은 `fit(model, train_data)`처럼 함수 형태를 기대했다가, 점(`.`)이 붙은 호출 모양에서 멈출 수 있습니다.

이때 중요한 것은 문법을 외우는 것이 아니라 호출의 중심을 읽는 일입니다. `model`은 어떤 상태를 가진 객체일 가능성이 있고, `fit()`은 그 객체의 상태를 바꾸는 동작일 수 있으며, `predict()`는 그 상태를 사용해 결과를 만드는 동작일 수 있습니다.

그래서 클래스와 객체를 처음 만날 때는 `객체가 값과 동작을 함께 가진다`, `메서드는 그 객체에 붙어 호출된다`는 기준을 먼저 잡아야 합니다. 문자열의 `text.strip()`와 모델의 `model.fit()`은 복잡도는 다르지만 같은 호출 모양을 공유합니다.

확인 가능한 결과는 호출 앞의 대상이 바뀌면 동작도 달라진다는 점입니다. `text.lower()`는 문자열을 다루고, `scores.append(91)`은 리스트를 바꾸며, `model.predict(test_data)`는 모델 상태를 사용합니다. 점 앞의 대상이 무엇인지 읽을 수 있으면 코드 해석이 훨씬 쉬워집니다.

## 체크리스트

- 객체를 `값과 동작을 함께 가진 대상`으로 설명할 수 있는가?
- 클래스와 객체의 차이를 말할 수 있는가?
- `function(value)`와 `value.method()`를 구분할 수 있는가?
- `model.fit()` 같은 호출을 보고 왜 클래스와 메서드 관점이 필요한지 설명할 수 있는가?
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

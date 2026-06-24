# P2-8.5 함수(function)와 작은 재사용

P2-8.1에서는 값(value), 변수(variable), 타입(type)을 봤습니다. P2-8.2부터 P2-8.4까지는 리스트(list), 딕셔너리(dictionary), 반복(loop)으로 여러 값을 처리하는 방법을 봤습니다.

이제 남는 질문은 이것입니다.

같은 처리를 여러 번 써야 한다면 어떻게 해야 할까요?

Python에서는 함수(function)를 사용합니다. 함수는 반복되는 처리에 이름을 붙이고, 필요한 값을 받아 계산한 뒤, 결과를 돌려주는 구조입니다.

이 절의 목적은 함수 문법을 모두 외우는 것이 아닙니다. 수식의 함수와 Python 함수가 어떻게 닮고 다른지 보고, 작은 데이터 처리 코드를 재사용 가능한 단위로 나누는 감각을 만드는 것입니다.

일반화하면 함수는 “입력, 처리, 출력”을 하나의 단위로 묶는 방법입니다. Python 문법은 그 단위를 표현하는 한 방식이고, 같은 관점은 수학의 함수, 모델 함수, API 함수, 라이브러리 함수에도 이어집니다.

## 이 절의 범위

이 절은 Python 함수의 가장 기본적인 사용만 다룹니다. 중심 질문은 “반복되는 처리를 어떤 이름의 단위로 분리할 것인가”입니다.

여기서는 다음 질문에 답합니다.

- 함수(function)는 왜 필요한가?
- 수학의 함수와 Python 함수는 어떻게 닮고 다른가?
- 매개변수(parameter), 인자(argument), 반환값(return value)은 무엇인가?
- Python 함수가 기존 C/Java식 함수와 다르게 보일 수 있는 지점은 무엇인가?
- 반복되는 데이터 처리를 함수로 어떻게 분리하는가?
- 함수가 너무 커지거나 많은 일을 하면 왜 읽기 어려운가?

이 절은 람다(lambda), 데코레이터(decorator), 클래스 메서드(method), 제너레이터(generator), 타입 힌트(type hint), 예외 처리(exception handling)를 깊게 다루지 않습니다.

## 이 절의 목표

- `def`로 함수를 정의하는 기본 형태를 읽을 수 있습니다.
- 매개변수(parameter)와 인자(argument)를 구분할 수 있습니다.
- `return`이 함수의 결과를 돌려주는 문법임을 설명할 수 있습니다.
- 반복되는 계산과 데이터 처리를 작은 함수로 분리할 수 있습니다.
- 수식의 함수와 Python 함수의 차이를 설명할 수 있습니다.
- Python 함수가 값처럼 변수에 담기고 다른 함수에 전달될 수 있음을 설명할 수 있습니다.
- 함수(function)와 메서드(method)의 호출 모양이 다를 수 있음을 입문 수준에서 구분할 수 있습니다.

## 함수는 처리 단위를 이름으로 분리하는 방법이다

일반적으로 함수(function)는 입력을 받아 어떤 처리를 하고 결과를 돌려주는 단위입니다. 수학에서는 입력과 출력의 관계를 강조하고, 프로그래밍에서는 그 관계를 실제 실행 가능한 코드로 표현합니다.

Python에서는 `def`로 함수에 이름을 붙이고, 필요한 입력 이름을 매개변수(parameter)로 적습니다.

다음 코드는 점수를 기준으로 통과 여부를 판단합니다.

```python
score = 82

if score >= 60:
    result = "pass"
else:
    result = "fail"

print(result)
```

이 판단을 한 번만 쓴다면 그대로 둘 수 있습니다. 하지만 점수 여러 개에 대해 계속 같은 판단을 해야 한다면 코드가 반복됩니다.

함수를 쓰면 이 처리에 이름을 붙일 수 있습니다.

```python
def pass_or_fail(score):
    if score >= 60:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(55))
```

`pass_or_fail`은 함수 이름입니다. `score`는 함수 안에서 사용할 입력 이름입니다. `return`은 결과를 함수 밖으로 돌려줍니다.

이 절에서는 함수를 다음 기준으로 이해합니다.

함수는 입력을 받아, 처리하고, 결과를 돌려주는 이름 붙은 코드입니다.

| 관점 | 일반적인 설명 | Python에서는 |
| --- | --- | --- |
| 함수(function) | 입력, 처리, 출력을 묶는 단위 | `def`로 정의함 |
| 입력 | 함수가 처리할 값 | 매개변수(parameter)와 인자(argument)로 구분함 |
| 출력 | 다음 계산에 넘길 결과 | `return`으로 돌려줌 |

## 수학의 함수와 Python 함수

수학에서 함수는 보통 입력과 출력의 관계로 설명합니다.

$$
f(x) = x + 1
$$

Python으로 쓰면 다음처럼 볼 수 있습니다.

```python
def f(x):
    return x + 1

print(f(3))
```

이 둘은 닮았습니다. 입력 `x`가 있고, 결과가 있습니다.

하지만 완전히 같지는 않습니다.

| 관점 | 수학의 함수 | Python 함수 |
| --- | --- | --- |
| 중심 관심 | 입력과 출력의 관계 | 실행되는 코드와 결과 |
| 표현 | \(f(x) = x + 1\) | `def f(x): return x + 1` |
| 부작용(side effect) | 보통 순수한 관계로 다룸 | 출력, 파일 저장, 리스트 변경 같은 동작을 할 수 있음 |
| 오류 | 정의역 밖이면 수학적으로 다룸 | 타입 오류, 키 오류, 실행 오류가 날 수 있음 |

AI 실습에서는 두 관점이 모두 필요합니다.

- 손실 함수(loss function)는 수학적 관계로 이해해야 합니다.
- Python 함수는 그 계산을 코드로 재사용하게 해 줍니다.
- 라이브러리 함수는 내부 구현을 몰라도 입력과 출력 계약을 믿고 사용할 수 있게 해 줍니다.

## 매개변수와 인자 구분

수학의 함수와 Python 함수가 모두 입력을 받는다는 점을 봤다면, 이제 Python 문서에서 자주 만나는 용어를 구분할 수 있습니다. 함수를 배울 때 매개변수(parameter)와 인자(argument)라는 표현이 나옵니다.

```python
def add_bonus(score, bonus):
    return score + bonus

result = add_bonus(80, 5)

print(result)
```

이 코드에서 `score`와 `bonus`는 매개변수(parameter)입니다. 함수가 받을 값을 함수 정의 안에서 부르는 이름입니다.

`80`과 `5`는 인자(argument)입니다. 함수를 호출할 때 실제로 넘긴 값입니다.

| 구분 | 위치 | 예시 |
| --- | --- | --- |
| 매개변수(parameter) | 함수를 정의할 때 쓰는 이름 | `score`, `bonus` |
| 인자(argument) | 함수를 호출할 때 넣는 실제 값 | `80`, `5` |
| 반환값(return value) | 함수가 돌려주는 결과 | `85` |

이 구분은 이후 모델 함수, 손실 함수, API 함수, 라이브러리 함수 문서를 읽을 때 계속 등장합니다.

## return은 결과를 돌려준다

`return`은 함수가 계산한 결과를 호출한 자리로 돌려주는 문법입니다.

```python
def normalize_score(score):
    return score / 100

normalized = normalize_score(82)

print(normalized)
```

`normalize_score(82)`가 실행되면 `0.82`가 결과로 돌아옵니다. 그 결과를 `normalized`라는 이름에 붙였습니다.

`print()`와 `return`은 다릅니다.

```python
def show_score(score):
    print(score)

result = show_score(82)

print(result)
```

이 함수는 화면에 `82`를 출력하지만, 돌려주는 값은 없습니다. Python에서는 명시적으로 돌려주는 값이 없으면 보통 `None`을 결과로 봅니다.

이 절에서는 다음을 구분합니다.

- `print()`는 사람에게 보여주는 출력입니다.
- `return`은 다음 계산에 쓸 결과를 돌려주는 동작입니다.

## 반복되는 계산을 함수로 분리한다

반복되는 계산에 이름을 붙이면 코드의 의도가 드러납니다.

```python
def normalize_score(score):
    return score / 100

scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(normalize_score(score))

print(normalized_scores)
```

이제 `score / 100`이라는 계산보다 “정규화한다”는 의도가 먼저 보입니다.

계산식이 간단할 때는 굳이 함수로 나누지 않아도 됩니다. 하지만 같은 계산을 여러 곳에서 쓰거나, 이름을 붙이면 의도가 더 분명해질 때 함수가 유용합니다.

## 데이터 한 건을 처리하는 함수

AI 실습에서는 데이터 한 건(sample)을 처리하는 함수를 자주 만들 수 있습니다.

```python
def is_valid_sample(sample):
    return "text" in sample and "label" in sample

sample = {"text": "AI is useful", "label": "positive"}

print(is_valid_sample(sample))
```

이 함수는 샘플에 `text`와 `label` 키가 있는지 확인합니다.

여러 샘플에 대해 사용할 수 있습니다.

```python
def is_valid_sample(sample):
    return "text" in sample and "label" in sample

samples = [
    {"text": "AI is useful", "label": "positive"},
    {"text": "missing label"},
    {"text": "Models can fail", "label": "negative"},
]

valid_samples = []

for sample in samples:
    if is_valid_sample(sample):
        valid_samples.append(sample)

print(valid_samples)
```

이 구조는 작지만 중요합니다.

- 반복문은 여러 샘플을 하나씩 꺼냅니다.
- 함수는 샘플 하나를 검사합니다.
- 조건문은 검사 결과에 따라 처리 방식을 바꿉니다.

이런 작은 조합이 이후 데이터 전처리(preprocessing), 평가(evaluation), 필터링(filtering) 코드의 기본 모양이 됩니다.

## 기본값을 줄 수 있다

함수 매개변수에는 기본값(default value)을 줄 수 있습니다.

```python
def pass_or_fail(score, threshold=60):
    if score >= threshold:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(82, threshold=90))
```

첫 번째 호출은 기준값을 따로 주지 않았으므로 `60`을 사용합니다. 두 번째 호출은 `threshold=90`을 직접 지정합니다.

AI 도구와 라이브러리에서도 이런 형태를 자주 봅니다.

- `batch_size=32`
- `learning_rate=0.001`
- `shuffle=True`
- `max_tokens=100`

기본값은 편리하지만, 기본값이 무엇인지 모르고 쓰면 코드의 행동을 오해할 수 있습니다. 그래서 라이브러리 문서에서 기본값을 확인하는 습관이 필요합니다.

## Python 함수는 값처럼 다룰 수 있다

C 언어나 Java 같은 언어를 먼저 배운 사람에게 Python 함수는 조금 다르게 보일 수 있습니다. Python에서는 함수도 객체(object)입니다. 그래서 함수 이름은 단순한 코드 위치 표시가 아니라, 함수 객체를 가리키는 이름으로 볼 수 있습니다.

예를 들어 함수를 다른 이름에 담을 수 있습니다.

```python
def normalize_score(score):
    return score / 100

normalize = normalize_score

print(normalize(82))
```

`normalize`는 새 계산을 만든 것이 아니라 `normalize_score` 함수 객체를 다른 이름으로 가리킨 것입니다. 이 감각은 처음에는 낯설지만, Python 라이브러리 코드에서 자주 등장합니다.

함수를 다른 함수에 인자로 넘길 수도 있습니다.

```python
def normalize_score(score):
    return score / 100

def apply_to_scores(scores, function):
    results = []
    for score in scores:
        results.append(function(score))
    return results

scores = [82, 75, 91]

print(apply_to_scores(scores, normalize_score))
```

이 예시에서 `apply_to_scores()`는 점수 목록과 함수를 함께 받습니다. 그리고 각 점수에 그 함수를 적용합니다. 여기서 함수는 “실행할 코드 조각”이 아니라 “전달할 수 있는 값”처럼 쓰입니다.

이런 방식은 이후 데이터 처리와 AI 라이브러리에서 자주 보입니다.

- 정렬 기준을 함수로 넘깁니다.
- 전처리 함수를 반복 처리에 넘깁니다.
- 평가 함수(metric function)를 학습 코드에 넘깁니다.
- 콜백(callback) 함수로 특정 시점의 동작을 지정합니다.

이 절에서는 고급 함수형 프로그래밍(functional programming)을 다루지 않습니다. 다만 Python에서는 함수가 값처럼 전달될 수 있다는 점을 알아 두면, 라이브러리 API를 읽을 때 덜 낯설어집니다.

## 함수와 메서드는 호출의 중심이 다르다

Python 코드를 읽다 보면 `function(value)`처럼 호출하는 코드와 `value.method()`처럼 호출하는 코드가 함께 보입니다. 이 절에서는 클래스(class)의 상세 개념으로 들어가지 않고, 함수(function)와 메서드(method)의 호출 모양만 구분합니다.

함수(function)는 독립적으로 정의된 처리 단위입니다.

```python
def clean_text(text):
    return text.strip().lower()
```

메서드(method)는 어떤 객체(object)에 붙어 호출되는 함수처럼 보입니다.

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

여기서 `strip()`과 `lower()`는 문자열 객체가 제공하는 메서드입니다. 함수처럼 괄호를 붙여 호출하지만, 앞에 대상 객체가 있습니다.

이 절에서는 다음 정도만 기억합니다.

| 표현 | 입문용 설명 | 예시 |
| --- | --- | --- |
| 함수(function) | 이름 붙은 독립 처리 단위 | `clean_text(text)` |
| 메서드(method) | 값 또는 객체에 붙어 호출되는 함수 형태 | `text.strip()` |

클래스(class)와 객체(object)는 P2-8.6 보충학습에서 따로 봅니다. 지금은 Python 코드에서 `function(value)`와 `value.method()`가 모두 “동작을 호출한다”는 점은 닮았지만, 호출의 중심이 다르다는 정도를 구분하면 충분합니다.

## 함수가 너무 많은 일을 하면 나누어 본다

작은 함수는 입력, 처리, 출력이 분명합니다. 반대로 함수 하나가 너무 많은 일을 하면 코드의 책임 범위가 흐려집니다.

예를 들어 다음 작업이 한 함수에 모두 들어 있다고 생각해 봅니다.

1. 파일을 읽는다.
2. 비어 있는 행을 제거한다.
3. 점수를 숫자로 바꾼다.
4. 평균을 계산한다.
5. 결과를 저장한다.

이런 함수는 처음에는 간단해 보이지만, 나중에 일부만 고치기 어렵습니다.

이 절에서는 함수를 나눌 때 다음 질문을 사용합니다.

- 이 함수는 한 가지 일을 하는가?
- 함수 이름이 실제 동작을 잘 설명하는가?
- 입력과 출력이 분명한가?
- 화면 출력과 결과 반환이 섞여 있지는 않은가?
- 같은 처리를 여러 곳에서 반복하고 있지는 않은가?

AI 실습에서도 이 기준은 유용합니다. 데이터 불러오기, 전처리, 모델 실행, 평가를 조금씩 나누면 오류를 찾기 쉬워집니다.

## 작은 재사용 예시

다음 예시는 텍스트 샘플을 간단히 정리하고, 비어 있지 않은 샘플만 남깁니다.

```python
def clean_text(text):
    return text.strip().lower()

def is_not_empty(text):
    return len(text) > 0

texts = [" AI is Useful ", "", " Models can FAIL "]
cleaned_texts = []

for text in texts:
    cleaned = clean_text(text)
    if is_not_empty(cleaned):
        cleaned_texts.append(cleaned)

print(cleaned_texts)
```

이 코드는 Python 문법으로는 단순합니다. 하지만 데이터 처리의 중요한 흐름을 보여줍니다.

- `clean_text()`는 텍스트 하나를 정리합니다.
- `is_not_empty()`는 텍스트 하나를 검사합니다.
- 반복문은 여러 텍스트에 같은 처리를 적용합니다.
- 결과는 새 리스트에 담습니다.

이런 작은 함수들이 모이면 이후 Pandas, NumPy, 머신러닝 라이브러리 코드를 읽는 데 도움이 됩니다.

## 이 절에서 기억할 관점

함수는 코드를 꾸미기 위한 장식이 아닙니다. 반복되는 처리에 이름을 붙이고, 입력과 출력을 분명하게 만들기 위한 도구입니다.

수학의 함수는 입력과 출력의 관계를 이해하는 데 도움을 줍니다. Python 함수는 그 관계를 실제 코드로 실행하고 재사용하게 해 줍니다.

일반화하면 함수는 복잡한 작업을 작게 나누는 경계입니다. 데이터 하나를 처리하는 함수, 여러 데이터를 반복하는 코드, 결과를 평가하는 함수가 분리되면 이후 프로젝트 코드도 읽기 쉬워집니다.

이 절의 핵심은 다음입니다.

- 함수는 처리에 이름을 붙입니다.
- 매개변수(parameter)는 함수가 받을 값의 이름입니다.
- 인자(argument)는 함수를 호출할 때 넣는 실제 값입니다.
- `return`은 다음 계산에 사용할 결과를 돌려줍니다.
- Python 함수는 객체이므로 변수에 담거나 다른 함수에 인자로 넘길 수 있습니다.
- 메서드(method)는 객체에 붙어 호출되는 함수 형태로 읽을 수 있습니다.
- 작은 함수는 반복되는 데이터 처리의 입력과 출력을 분명하게 만듭니다.

## 체크리스트

- `def`로 시작하는 함수 정의를 읽을 수 있다.
- 매개변수(parameter)와 인자(argument)를 구분할 수 있다.
- `print()`와 `return`의 차이를 설명할 수 있다.
- 반복되는 계산을 함수로 분리할 수 있다.
- 데이터 한 건을 처리하는 함수를 만들고, 반복문에서 재사용할 수 있다.
- Python 함수가 변수에 담기고 다른 함수에 인자로 전달될 수 있음을 설명할 수 있다.
- 함수(function)와 메서드(method)의 호출 모양 차이를 설명할 수 있다.
- 함수 이름이 코드 의도를 드러내야 함을 설명할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [More Control Flow Tools: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [More Control Flow Tools: Default Argument Values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-24.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-25.
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-06-25.

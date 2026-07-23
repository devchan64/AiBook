# P2-8.5 함수(function)와 작은 재사용

> Section ID: `P2-8.5`
> Version: `v2026.07.23`

P2-8.1에서는 값(value), 변수(variable), 타입(type)을 봤습니다. P2-8.2부터 P2-8.4까지는 리스트(list), 딕셔너리(dictionary), 반복(loop)으로 여러 값을 처리하는 방법을 봤습니다.

이제 남는 질문은 이것입니다.

같은 처리를 여러 번 써야 한다면 어떻게 해야 할까요?

Python에서는 함수(function)를 사용합니다. 함수는 반복되는 처리에 이름을 붙이고, 필요한 값을 받아 계산한 뒤, 결과를 돌려주는 구조입니다.

여기서는 `함수(function)`, `매개변수(parameter)`, `인자(argument)`, `반환값(return value)`의 기본 구분을 설명합니다. `값(value)`, `변수(variable)`, `반복(loop)`의 대표 설명은 P2-8.1, P2-8.4와 [개념사전](../../../reference/concept-glossary.md)에 두고, 여기서는 입력-처리-출력 계약을 작은 재사용 단위로 읽는 데 집중합니다.

이 절에서는 함수 문법을 모두 외우기보다, 수식의 함수와 Python 함수가 어떻게 닮고 다른지 보고 작은 데이터 처리 코드를 재사용 가능한 단위로 나누는 감각을 만듭니다.

일반화하면 함수는 “입력, 처리, 출력”을 하나의 단위로 묶는 방법입니다. Python 문법은 그 단위를 표현하는 한 방식이고, 같은 관점은 수학의 함수, 모델 함수, API 함수, 라이브러리 함수에도 이어집니다.

여기서는 함수 문법을 고급 기능까지 배우기보다, 앞 절의 반복과 자료구조 처리를 작은 재사용 단위로 묶습니다. 리스트, 딕셔너리, 반복을 각각 따로 읽었다면, 여기서는 그 처리 흐름에 이름을 붙여 다시 쓸 수 있게 만드는 지점으로 넘어갑니다. 이 손잡이를 먼저 잡아 두면, 뒤에서 라이브러리 함수나 모델 API를 볼 때도 `문법`보다 `입력-처리-출력 계약`을 먼저 읽기 쉬워집니다.

| 용어 | 이 절에서 먼저 잡을 뜻 |
| --- | --- |
| 함수(function) | 입력을 받아 처리하고 결과를 돌려주는 이름 붙은 코드 단위입니다. |
| 매개변수(parameter) | 함수를 정의할 때 적는 입력 이름입니다. |
| 인자(argument) | 함수를 실제로 호출할 때 넘기는 값입니다. |
| 반환값(return value) | 함수가 계산 뒤 바깥으로 돌려주는 결과입니다. |
| 메서드(method) | 어떤 값이나 객체에 붙어 호출되는 함수 형태입니다. |

## 핵심 기준: 함수(function)와 작은 재사용

- `def`로 함수를 정의하는 기본 형태를 읽을 수 있습니다.
- 매개변수(parameter)와 인자(argument)를 구분할 수 있습니다.
- `return`이 함수의 결과를 돌려주는 문법임을 설명할 수 있습니다.
- 반복되는 계산과 데이터 처리를 작은 함수로 분리할 수 있습니다.
- 수식의 함수와 Python 함수의 차이를 설명할 수 있습니다.
- Python 함수가 값처럼 변수에 담기고 다른 함수에 전달될 수 있음을 설명할 수 있습니다.
- 함수(function)와 메서드(method)의 호출 모양이 다를 수 있음을 입문 수준에서 구분할 수 있습니다.

## 학습 배경

여기서는 함수 문법보다 `반복되는 처리를 이름 붙여 다시 쓰는 방법`을 먼저 봅니다. 아래 세 가지 기준이 뒤에서 라이브러리 함수와 메서드를 읽는 바탕이 됩니다.

| 기준 | 왜 중요한가 | 이 절에서 필요한 이해 수준 |
| --- | --- | --- |
| 함수는 입력, 처리, 출력을 한 단위로 묶는다 | 수학의 함수와 코드의 함수를 같은 큰 틀에서 읽게 해 준다 | 값을 받아 결과를 돌려주는 이름 붙은 코드라고 이해한다 |
| 같은 처리가 반복되면 함수로 분리하는 편이 읽기 쉽다 | 작은 데이터 처리 코드가 왜 재사용 구조로 바뀌는지 이해하게 해 준다 | 점수 판정이나 정규화 같은 계산을 함수로 묶어 읽는다 |
| `print`와 `return`은 역할이 다르다 | 코드 실행 결과와 계산 결과를 구분하는 데 중요하다 | 화면에 보여 주는 것과 다음 계산에 돌려주는 것은 다르다고 설명할 수 있다 |

## 주요 학습내용

### 함수는 처리 단위를 이름으로 분리하는 방법이다

일반적으로 함수(function)는 입력을 받아 어떤 처리를 하고 결과를 돌려주는 단위입니다. 수학에서는 입력과 출력의 관계를 강조하고, 프로그래밍에서는 그 관계를 실제 실행 가능한 코드로 표현합니다.

Python에서는 `def`로 함수에 이름을 붙이고, 필요한 입력 이름을 매개변수(parameter)로 적습니다.

다음 코드는 점수를 기준으로 통과 여부를 판단합니다.

문제 상황: 함수로 나누기 전에 점수 하나를 바로 판정하는 코드를 먼저 보고 싶습니다.
입력(input): 점수 값 `82`.
기대 출력(output): 통과 여부 문자열 `pass`.
확인할 개념: 반복되는 판단은 일반 조건문으로도 먼저 표현할 수 있습니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
score = 82

if score >= 60:
    result = "pass"
else:
    result = "fail"

print(result)
```

이 판단을 한 번만 쓴다면 그대로 둘 수 있습니다. 하지만 점수 여러 개에 대해 계속 같은 판단을 해야 한다면 코드가 반복됩니다.

함수를 쓰면 이 처리에 이름을 붙일 수 있습니다.

문제 상황: 같은 통과 판정을 여러 번 재사용할 수 있도록 함수로 묶은 예를 보고 싶습니다.
입력(input): 함수 `pass_or_fail`과 점수 `82`, `55`.
기대 출력(output): 각 점수에 대한 `pass`, `fail`.
확인할 개념: 함수는 반복되는 처리에 이름을 붙여 다시 쓸 수 있게 합니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
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

### 수학의 함수와 Python 함수

수학에서 함수는 보통 입력과 출력의 관계로 설명합니다.

$$
f(x) = x + 1
$$

Python으로 쓰면 다음처럼 볼 수 있습니다.

문제 상황: 수학의 함수 \(f(x)=x+1\)를 Python 함수로 옮긴 가장 작은 예를 보고 싶습니다.
입력(input): 입력값 `3`.
기대 출력(output): `4`.
확인할 개념: 수학의 입력-출력 관계를 Python에서도 함수 형태로 표현할 수 있습니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
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

### 매개변수와 인자 구분

수학의 함수와 Python 함수가 모두 입력을 받는다는 점을 봤다면, 이제 Python 문서에서 자주 만나는 용어를 구분할 수 있습니다. 함수를 배울 때 매개변수(parameter)와 인자(argument)라는 표현이 나옵니다.

문제 상황: 매개변수와 인자를 실제 호출 예로 구분해 보고 싶습니다.
입력(input): 함수 `add_bonus(score, bonus)`와 호출 인자 `80`, `5`.
기대 출력(output): 더해진 결과 `85`.
확인할 개념: 함수 정의 쪽 이름은 매개변수이고, 호출 시 넘기는 실제 값은 인자입니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
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

### return은 결과를 돌려준다

`return`은 함수가 계산한 결과를 호출한 자리로 돌려주는 문법입니다.

문제 상황: 함수가 계산한 결과를 다음 계산에서 다시 쓰는 예를 보고 싶습니다.
입력(input): 점수 `82`.
기대 출력(output): 정규화 결과 `0.82`.
확인할 개념: `return`은 함수 결과를 호출한 쪽으로 돌려줍니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
def normalize_score(score):
    return score / 100

normalized = normalize_score(82)

print(normalized)
```

`normalize_score(82)`가 실행되면 `0.82`가 결과로 돌아옵니다. 그 결과를 `normalized`라는 이름에 붙였습니다.

`print()`와 `return`은 다릅니다.

문제 상황: 화면에 보여 주는 것과 실제 반환값이 다르다는 점을 비교하고 싶습니다.
입력(input): 점수 `82`.
기대 출력(output): 함수 안에서는 `82`를 출력하지만, 바깥 변수 `result`에는 `None`이 들어갑니다.
확인할 개념: `print()`는 출력이고 `return`은 계산 결과 전달입니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
def show_score(score):
    print(score)

result = show_score(82)

print(result)
```

이 함수는 화면에 `82`를 출력하지만, 돌려주는 값은 없습니다. Python에서는 명시적으로 돌려주는 값이 없으면 보통 `None`을 결과로 봅니다.

이 절에서는 다음을 구분합니다.

- `print()`는 사람에게 보여주는 출력입니다.
- `return`은 다음 계산에 쓸 결과를 돌려주는 동작입니다.

## 세부 학습내용

### 반복되는 계산을 함수로 분리한다

반복되는 계산에 이름을 붙이면 코드의 의도가 드러납니다.

문제 상황: 점수 정규화 계산을 함수로 분리해 반복문에서 재사용하는 예를 보고 싶습니다.
입력(input): 점수 리스트 `scores`.
기대 출력(output): 정규화된 점수 리스트 `normalized_scores`.
확인할 개념: 반복문 안의 같은 계산은 함수로 분리하면 의도가 더 잘 보입니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
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

### 데이터 한 건을 처리하는 함수

AI 실습에서는 데이터 한 건(sample)을 처리하는 함수를 자주 만들 수 있습니다.

문제 상황: 샘플 하나가 필요한 키를 모두 갖췄는지 검사하는 함수를 보고 싶습니다.
입력(input): `text`, `label` 키를 가진 샘플 딕셔너리.
기대 출력(output): 유효 여부 `True`.
확인할 개념: 함수는 데이터 한 건에 대한 검사 규칙을 캡슐화할 수 있습니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
def is_valid_sample(sample):
    return "text" in sample and "label" in sample

sample = {"text": "AI is useful", "label": "positive"}

print(is_valid_sample(sample))
```

이 함수는 샘플에 `text`와 `label` 키가 있는지 확인합니다.

여러 샘플에 대해 사용할 수 있습니다.

문제 상황: 방금 만든 샘플 검사 함수를 여러 샘플에 반복 적용하는 예를 보고 싶습니다.
입력(input): 샘플 딕셔너리 리스트 `samples`.
기대 출력(output): 유효한 샘플만 남긴 `valid_samples`.
확인할 개념: 데이터 한 건을 처리하는 함수는 반복문과 결합될 때 재사용 가치가 커집니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
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

### 기본값을 줄 수 있다

함수 매개변수에는 기본값(default value)을 줄 수 있습니다.

문제 상황: 기준값을 자주 바꾸지 않는 함수에서 기본값이 어떻게 동작하는지 보고 싶습니다.
입력(input): `score`, 기본값 `threshold=60`, 그리고 명시적으로 준 `threshold=90`.
기대 출력(output): 같은 점수라도 기준값에 따라 다른 판정 결과.
확인할 개념: 기본값 매개변수는 인자를 생략해도 기본 행동을 유지하게 해 줍니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
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

### Python 함수는 값처럼 다룰 수 있다

C 언어나 Java 같은 언어를 먼저 배운 사람에게 Python 함수는 조금 다르게 보일 수 있습니다. Python에서는 함수도 객체(object)입니다. 그래서 함수 이름은 단순한 코드 위치 표시가 아니라, 함수 객체를 가리키는 이름으로 볼 수 있습니다.

예를 들어 함수를 다른 이름에 담을 수 있습니다.

문제 상황: 함수도 값처럼 다른 변수 이름에 담아 호출할 수 있다는 점을 확인하고 싶습니다.
입력(input): 함수 `normalize_score`와 새 이름 `normalize`.
기대 출력(output): `normalize(82)` 결과 `0.82`.
확인할 개념: Python 함수는 객체라서 변수에 담아 다른 이름으로 참조할 수 있습니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
def normalize_score(score):
    return score / 100

normalize = normalize_score

print(normalize(82))
```

`normalize`는 새 계산을 만든 것이 아니라 `normalize_score` 함수 객체를 다른 이름으로 가리킨 것입니다. 이 감각은 낯설 수 있지만, Python 라이브러리 코드에서 자주 등장합니다.

함수를 다른 함수에 인자로 넘길 수도 있습니다.

문제 상황: 함수 하나를 다른 함수의 인자로 넘겨 공통 반복 로직에 적용하는 예를 보고 싶습니다.
입력(input): 점수 리스트 `scores`와 함수 `normalize_score`.
기대 출력(output): `apply_to_scores`가 만든 정규화 점수 리스트.
확인할 개념: Python에서는 함수도 다른 값처럼 전달할 수 있습니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
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

이 절에서는 고급 함수형 프로그래밍(functional programming)을 다루지 않습니다. 현재 본편에서 함수형 프로그래밍 자체를 따로 확장하지는 않고, 여기서 필요한 범위는 `함수를 값처럼 전달할 수 있다`는 감각까지로 둡니다. 다만 Python에서는 함수가 값처럼 전달될 수 있다는 점을 알아 두면, 라이브러리 API를 읽을 때 덜 낯설어집니다.

### 함수와 메서드는 호출의 중심이 다르다

Python 코드를 읽다 보면 `function(value)`처럼 호출하는 코드와 `value.method()`처럼 호출하는 코드가 함께 보입니다. 이 절에서는 클래스(class)의 상세 개념으로 들어가지 않고, 함수(function)와 메서드(method)의 호출 모양만 구분합니다.

함수(function)는 독립적으로 정의된 처리 단위입니다. 메서드(method)는 어떤 객체(object)에 붙어 호출되는 함수처럼 보입니다.

문제 상황: 독립 함수 호출과 문자열 메서드 호출의 모양을 한 번에 비교하고 싶습니다.
입력(input): 문자열 `text = " AI is Useful "`.
기대 출력(output): `clean_text(text)`, `text.strip()`, `text.lower()` 결과가 각각 출력됩니다.
확인할 개념: 함수는 독립 이름으로 호출하고, 메서드는 값이나 객체에 붙어 호출합니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
def clean_text(text):
    return text.strip().lower()

text = " AI is Useful "

print(clean_text(text))
print(text.strip())
print(text.lower())
```

여기서 `clean_text(text)`는 독립 함수 호출이고, `strip()`과 `lower()`는 문자열 객체가 제공하는 메서드입니다. 함수처럼 괄호를 붙여 호출하지만, 메서드 앞에는 대상 객체가 있습니다.

이 절에서는 다음 정도만 기억합니다.

| 표현 | 입문용 설명 | 예시 |
| --- | --- | --- |
| 함수(function) | 이름 붙은 독립 처리 단위 | `clean_text(text)` |
| 메서드(method) | 값 또는 객체에 붙어 호출되는 함수 형태 | `text.strip()` |

클래스(class)와 객체(object)는 P2-8.6 보충학습에서 따로 봅니다. 여기서는 Python 코드에서 `function(value)`와 `value.method()`가 모두 “동작을 호출한다”는 점은 닮았지만, 호출의 중심이 다르다는 정도를 구분합니다.

### 함수가 너무 많은 일을 하면 나누어 본다

작은 함수는 입력, 처리, 출력이 분명합니다. 반대로 함수 하나가 너무 많은 일을 하면 코드의 책임 범위가 흐려집니다.

예를 들어 다음 작업이 한 함수에 모두 들어 있다고 생각해 봅니다.

1. 파일을 읽는다.
2. 비어 있는 행을 제거한다.
3. 점수를 숫자로 바꾼다.
4. 평균을 계산한다.
5. 결과를 저장한다.

이런 함수는 간단해 보여도, 나중에 일부만 고치기 어렵습니다.

이 절에서는 함수를 나눌 때 다음 질문을 사용합니다.

- 이 함수는 한 가지 일을 하는가?
- 함수 이름이 실제 동작을 잘 설명하는가?
- 입력과 출력이 분명한가?
- 화면 출력과 결과 반환이 섞여 있지는 않은가?
- 같은 처리를 여러 곳에서 반복하고 있지는 않은가?

AI 실습에서도 이 기준은 유용합니다. 데이터 불러오기, 전처리, 모델 실행, 평가를 조금씩 나누면 오류를 찾기 쉬워집니다.

## 사례 및 예시

### 작은 재사용 예시

다음 예시는 텍스트 샘플을 간단히 정리하고, 비어 있지 않은 샘플만 남깁니다.

문제 상황: 작은 함수 두 개를 조합해 여러 텍스트를 정리하고 거르는 예를 보고 싶습니다.
입력(input): 공백과 빈 문자열이 섞인 텍스트 리스트 `texts`.
기대 출력(output): 정리되고 비어 있지 않은 텍스트만 남은 `cleaned_texts`.
확인할 개념: 함수는 작은 처리 단위를 만들고, 반복문은 그 단위를 여러 데이터에 적용합니다.

```python
# 이 예제는 함수를 작은 재사용 단위로 만들어 입력과 출력을 연결하는 방식을 확인합니다.
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

### 사례 1. 같은 정규화 계산을 왜 계속 복사해 쓰면 안 되는가

한 학습자가 점수 정규화 코드를 노트북 여러 셀에 복사해 넣었다고 하겠습니다. 빨리 진행되는 것처럼 보여도, 나중에 정규화 기준을 바꿔야 할 때는 모든 셀을 다시 찾아 고쳐야 합니다.

사람이 먼저 쓰는 기준은 `짧으니 그냥 한 번 더 쓰자`일 수 있습니다. 하지만 같은 처리가 반복되기 시작하면, 계산식보다 `이 처리가 어떤 이름의 작업인가`를 분리하는 편이 더 읽기 쉽고 수정도 쉬워집니다.

함수는 바로 이 지점에서 필요해집니다. 입력, 처리, 출력을 한 단위로 묶고 이름을 붙여 두면, 같은 계산을 다시 쓸 때 코드 중복을 줄이고 의도를 더 분명하게 드러낼 수 있습니다. `print`와 `return`을 구분하는 이유도 사람이 보는 출력과 다음 계산에 넘길 결과를 나누기 위해서입니다.

확인 가능한 결과는 수정 지점의 수로 드러납니다. 정규화 기준을 바꿀 때 함수 하나만 고치면 모든 호출 결과가 함께 바뀐다면, 반복 코드를 그대로 복사해 두는 것보다 재사용 구조가 더 잘 잡힌 것입니다.

## 연습 및 예제

다음 정도의 작은 연습으로 현재 절의 핵심을 다시 확인할 수 있습니다.

- 점수 하나를 받아 등급을 돌려주는 함수를 만들고, 여러 점수에 반복 적용해 봅니다.
- `print()`만 사용하는 함수와 `return`을 사용하는 함수를 각각 만든 뒤 결과 차이를 비교해 봅니다.
- 문자열 하나를 정리하는 함수와 비어 있는지 검사하는 함수를 나눈 뒤, 여러 텍스트를 걸러 봅니다.

## 체크리스트

- `def`로 시작하는 함수 정의를 읽을 수 있다.
- 매개변수(parameter)와 인자(argument)를 구분할 수 있다.
- `print()`와 `return`의 차이를 설명할 수 있다.
- 반복되는 계산을 함수로 분리할 수 있다.
- 데이터 한 건을 처리하는 함수를 만들고, 반복문에서 재사용할 수 있다.
- Python 함수가 변수에 담기고 다른 함수에 인자로 전달될 수 있음을 설명할 수 있다.
- 함수(function)와 메서드(method)의 호출 모양 차이를 설명할 수 있다.
- 함수 이름이 코드 의도를 드러내야 함을 설명할 수 있다.
- 함수가 반복되는 처리를 이름 붙은 재사용 단위로 바꾸는 이유를 설명할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [More Control Flow Tools: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. `def`, 매개변수, `return`, 함수 호출 예시의 공식 근거로 사용했다.
- Python Software Foundation, [More Control Flow Tools: Default Argument Values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 기본값 매개변수 예시와 mutable default 주의 설명 확인에 사용했다.
- Python Software Foundation, [Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 함수 정의 문법, 매개변수 목록, 함수 객체 생성 설명 확인에 사용했다.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Python에서 함수가 객체로 다뤄질 수 있다는 설명의 배경 근거로 사용했다.
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. 함수 호출과 메서드 호출 모양을 입문 수준에서 구분하는 근거로 사용했다.

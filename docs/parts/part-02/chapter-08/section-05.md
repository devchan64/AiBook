# P2-8.5 함수(function)와 작은 재사용

> Section ID: `P2-8.5`
> Version: `v2026.09.08`

## 함수 정의와 호출

일반적으로 함수(function)는 입력을 받아 어떤 처리를 하고 결과를 돌려주는 단위입니다. 수학에서는 입력과 출력의 관계를 강조하고, 프로그래밍에서는 그 관계를 실제 실행 가능한 코드로 표현합니다.

Python에서는 `def`로 함수에 이름을 붙이고, 필요한 입력 이름을 매개변수(parameter)로 적습니다.

다음 코드는 점수를 기준으로 통과 여부를 판단합니다.

점수 `82`가 기준 `60` 이상인지 판단하면 `pass`가 출력됩니다. 아래 코드는 함수 없이 조건문으로 판정합니다.

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

통과 판정에 `pass_or_fail`이라는 이름을 붙이면 점수만 바꿔 호출할 수 있습니다. 아래 출력은 `pass`, `fail`입니다.

```python
def pass_or_fail(score):
    if score >= 60:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(55))
```

`pass_or_fail`은 함수 이름입니다. `score`는 함수 안에서 사용할 입력 이름입니다. `return`은 결과를 호출한 자리로 돌려주고 현재 함수 실행을 끝냅니다. 따라서 `82`를 넣으면 `"pass"`를 반환한 뒤 아래의 `return "fail"`은 실행하지 않습니다.

### 수학의 함수와 Python 함수

수학에서 함수는 보통 입력과 출력의 관계로 설명합니다.

$$
f(x) = x + 1
$$

Python으로 쓰면 다음처럼 볼 수 있습니다.

수학의 함수 \(f(x)=x+1\)를 Python으로 표현하면 다음과 같습니다. 인자 `3`을 전달하면 `4`가 출력됩니다.

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

### 매개변수와 인자

매개변수(parameter)는 함수 정의에서 입력을 부르는 이름이고, 인자(argument)는 호출할 때 전달하는 값입니다.

점수 `80`에 보너스 `5`를 더하면 반환값은 `85`입니다. 함수 정의의 `score`, `bonus`는 매개변수이고 호출에 넣은 `80`, `5`는 인자입니다.

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

### 반환과 출력

`return`은 함수가 계산한 결과를 호출한 자리로 돌려주는 문법입니다.

100점 만점 점수 `82`를 100으로 나누어 반환합니다. 호출한 쪽에서 받은 `0.82`를 `normalized`에 저장하고 출력합니다.

```python
def normalize_score(score):
    return score / 100

normalized = normalize_score(82)

print(normalized)
```

`normalize_score(82)`가 실행되면 `0.82`가 결과로 돌아옵니다. 그 결과를 `normalized`라는 이름에 붙였습니다.

`print()`와 `return`은 다릅니다.

`show_score(82)`는 화면에 `82`를 출력합니다. 하지만 `return`이 없으므로 함수의 반환값은 `None`이며, `print(result)`는 `None`을 출력합니다.

```python
def show_score(score):
    print(score)

result = show_score(82)

print(result)
```

함수가 `return` 없이 끝나면 `None`을 반환합니다. 화면에 나타난 `82`가 `result`에 저장되는 것은 아닙니다. `result + 1`을 계산하면 `None`과 정수를 더할 수 없어 `TypeError`가 발생합니다.

## 반복 계산의 재사용

반복되는 계산에 이름을 붙이면 코드의 의도가 드러납니다.

점수 네 개에 `normalize_score()`를 적용하면 `[0.82, 0.75, 0.91, 0.68]`이 출력됩니다. 반복문은 점수를 하나씩 꺼내고 함수는 각 점수를 100으로 나눕니다.

```python
def normalize_score(score):
    return score / 100

scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(normalize_score(score))

print(normalized_scores)
```

함수 이름은 100점 만점 점수를 비율로 바꾸는 작업을 나타냅니다.

계산식이 간단할 때는 굳이 함수로 나누지 않아도 됩니다. 하지만 같은 계산을 여러 곳에서 쓰거나, 이름을 붙이면 의도가 더 분명해질 때 함수가 유용합니다.

### 데이터 한 건을 처리하는 함수

AI 실습에서는 데이터 한 건(sample)을 처리하는 함수를 자주 만들 수 있습니다.

샘플에 `"text"`와 `"label"` 키가 모두 있는지 검사합니다. 아래 입력은 두 키가 있으므로 `True`가 출력됩니다.

```python
def has_required_keys(sample):
    return "text" in sample and "label" in sample

sample = {"text": "AI is useful", "label": "positive"}

print(has_required_keys(sample))
```

이 함수는 키 존재 여부만 검사합니다. `{"text": "", "label": None}`도 두 키가 있으므로 `True`입니다. 텍스트가 비어 있는지, 라벨이 허용된 값인지까지 검사하는 함수는 아닙니다.

여러 샘플에 대해 사용할 수 있습니다.

샘플 세 개에 같은 키 검사를 적용합니다. 두 번째 샘플에는 `"label"` 키가 없으므로 첫 번째와 세 번째 딕셔너리만 결과 리스트에 남습니다.

```python
def has_required_keys(sample):
    return "text" in sample and "label" in sample

samples = [
    {"text": "AI is useful", "label": "positive"},
    {"text": "missing label"},
    {"text": "Models can fail", "label": "negative"},
]

samples_with_keys = []

for sample in samples:
    if has_required_keys(sample):
        samples_with_keys.append(sample)

print(samples_with_keys)
```

### 매개변수 기본값

함수 매개변수에는 기본값(default value)을 줄 수 있습니다.

기본 기준 `60`을 사용하면 점수 `82`는 `pass`이고, `threshold=90`을 지정하면 `fail`입니다. 다음 두 호출은 기준값만 다릅니다.

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

### 함수 객체 전달

Python 함수도 객체(object)이며, 함수 이름은 그 객체를 가리킵니다.

예를 들어 함수를 다른 이름에 담을 수 있습니다.

`normalize = normalize_score`는 함수 객체에 이름을 하나 더 붙입니다. `normalize(82)`의 출력도 `0.82`입니다.

```python
def normalize_score(score):
    return score / 100

normalize = normalize_score

print(normalize(82))
```

`normalize`는 새 계산을 만든 것이 아니라 `normalize_score` 함수 객체를 다른 이름으로 가리킨 것입니다. `normalize_score`는 함수 객체이고, `normalize_score(82)`는 함수를 실행한 결과라는 차이가 있습니다.

함수를 다른 함수에 인자로 넘길 수도 있습니다.

점수 `[82, 75, 91]`과 처리 함수 `normalize_score`를 함께 전달합니다. `apply_to_scores()`는 각 점수에 전달받은 함수를 적용하여 `[0.82, 0.75, 0.91]`을 반환하고, 바깥 `print()`가 이를 출력합니다.

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

이 예시에서 `apply_to_scores()`는 점수 목록과 함수를 함께 받습니다. 그리고 각 점수에 그 함수를 적용합니다. `function(score)`를 실행할 때 전달받은 함수가 호출됩니다.

이런 방식은 이후 데이터 처리와 AI 라이브러리에서 자주 보입니다.

- 정렬 기준을 함수로 넘깁니다.
- 전처리 함수를 반복 처리에 넘깁니다.
- 평가 함수(metric function)를 학습 코드에 넘깁니다.
- 콜백(callback) 함수로 특정 시점의 동작을 지정합니다.

### 함수와 메서드

`function(value)`는 함수 이름으로 호출하고, `value.method()`는 객체에서 메서드를 찾아 호출합니다.

함수(function)는 독립적으로 정의된 처리 단위입니다. 메서드(method)는 어떤 객체(object)에 붙어 호출되는 함수처럼 보입니다.

문자열 `" AI is Useful "`에 공백 제거와 소문자 변환을 적용합니다. `clean_text(text)`는 `ai is useful`, `text.strip()`은 `AI is Useful`, `text.lower()`는 양끝 공백이 남은 ` ai is useful `을 출력합니다.

```python
def clean_text(text):
    return text.strip().lower()

text = " AI is Useful "

print(clean_text(text))
print(text.strip())
print(text.lower())
```

여기서 `clean_text(text)`는 독립 함수 호출이고, `strip()`과 `lower()`는 문자열 객체가 제공하는 메서드입니다. 함수처럼 괄호를 붙여 호출하지만, 메서드 앞에는 대상 객체가 있습니다.

| 표현 | 입문용 설명 | 예시 |
| --- | --- | --- |
| 함수(function) | 이름 붙은 독립 처리 단위 | `clean_text(text)` |
| 메서드(method) | 값 또는 객체에 붙어 호출되는 함수 형태 | `text.strip()` |

### 처리 단계 분리

작은 함수는 입력, 처리, 출력이 분명합니다. 반대로 함수 하나가 너무 많은 일을 하면 코드의 책임 범위가 흐려집니다.

예를 들어 다음 작업이 한 함수에 모두 들어 있다고 생각해 봅니다.

1. 파일을 읽는다.
2. 비어 있는 행을 제거한다.
3. 점수를 숫자로 바꾼다.
4. 평균을 계산한다.
5. 결과를 저장한다.

이런 함수는 간단해 보여도, 나중에 일부만 고치기 어렵습니다.

## 사례: 공백 정리 후 빈 텍스트 제외

다음 예시는 텍스트 샘플을 간단히 정리하고, 비어 있지 않은 샘플만 남깁니다.

입력 `[" AI is Useful ", "", " Models can FAIL "]`에서 텍스트를 정리한 뒤 빈 문자열을 제외합니다. 출력은 `['ai is useful', 'models can fail']`입니다.

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

`clean_text()`는 문자열 하나를 정리하고, `is_not_empty()`는 정리된 문자열에 글자가 남았는지 검사합니다. 입력에 공백 세 개짜리 문자열 `"   "`을 추가해도 정리 후 빈 문자열이 되므로 출력은 같습니다. 빈 값 검사를 정리보다 먼저 하면 공백 문자열은 길이가 3이어서 통과합니다. 함수의 호출 순서가 결과에 영향을 줍니다.

## 사례: 만점 기준 변경

점수를 100으로 나누는 코드를 두 곳에 복사한 상태에서 시험 만점을 50점으로 바꿨다고 하겠습니다. 한 곳만 `/ 50`으로 고치면 같은 40점이 한쪽에서는 `0.8`, 다른 쪽에서는 `0.4`가 됩니다.

만점을 매개변수로 받으면 같은 함수에 점수와 만점을 전달할 수 있습니다. 다음 코드는 100점 만점의 80점과 50점 만점의 40점을 모두 `0.8`로 반환합니다.

```python
def score_ratio(score, maximum):
    return score / maximum

print(score_ratio(80, 100))
print(score_ratio(40, 50))
```

두 번째 호출의 만점을 `100`으로 바꾸면 결과는 `0.4`입니다. 함수로 묶으면 계산식을 한곳에서 관리할 수 있지만, 호출하는 쪽도 해당 시험의 만점을 정확히 전달해야 합니다. 이 함수는 만점이 양수이고 점수가 0부터 만점 사이인 입력을 전제로 합니다.

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

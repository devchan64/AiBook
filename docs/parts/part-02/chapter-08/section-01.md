# P2-8.1 값(value), 변수(variable), 타입(type)

> Section ID: `P2-8.1`
> Version: `v2026.09.08`

`82`와 `"82"`는 화면에서 비슷해 보이지만 계산 결과는 다릅니다. `82 + 3`은 `85`이고, `"82" + 3`은 오류가 납니다. 숫자와 문자열은 타입(type)이 다르기 때문입니다.

| 기준 | 왜 중요한가 |
| --- | --- |
| 값(value)은 계산이 다루는 데이터다 | 숫자, 텍스트, 참거짓을 연산의 입력으로 사용한다 |
| 변수(variable)는 값을 가리키는 이름이다 | 같은 값을 이름으로 다시 사용하고 다른 값으로 바꿀 수 있다 |
| 타입(type)은 값의 종류다 | 값에 적용할 수 있는 연산을 구분한다 |

## 값과 연산

숫자 `3`, `3.14`, 문자열 `"AI"`, 참거짓 `True`, `False`는 모두 값입니다. 연산(operation)은 이 값에 적용하는 처리입니다.

숫자 `3`과 `2`를 더하면 `5`가 되고, 문자열 `"AI"`와 `"Book"`을 더하면 `AIBook`이 됩니다. 다음 코드는 두 결과를 차례로 출력합니다.

```python
print(3 + 2)
print("AI" + "Book")
```

같은 `+`라도 숫자에서는 덧셈을, 문자열에서는 이어 붙이기를 수행합니다.

## 변수와 할당

Python에서는 `=`으로 이름과 값을 연결합니다. 이 동작을 할당(assignment)이라고 합니다.

가로 `20`, 세로 `45`인 직사각형의 넓이를 계산하면 `900`입니다. 다음 코드에서 `width`와 `height`는 길이를, `area`는 곱한 결과를 가리킵니다.

```python
width = 20
height = 45
area = width * height
print(area)
```

수학의 등식은 양쪽이 같다는 관계를 나타냅니다. Python의 할당문은 오른쪽을 계산한 뒤 그 결과에 왼쪽 이름을 연결합니다. `area = width * height`는 넓이와 두 길이 사이의 관계를 계속 유지하는 공식이 아닙니다. 나중에 `width`를 바꿔도 `area`가 자동으로 다시 계산되지는 않습니다.

같은 이름에 새 값을 할당할 수도 있습니다. 아래에서는 `score`가 `10`을 가리키다가 `12`를 가리키게 되어 `12`가 출력됩니다.

```python
score = 10
score = 12
print(score)
```

변수를 “상자”라고 설명하기도 하지만, Python에서는 “값을 가리키는 이름”으로 이해하는 편이 정확합니다. 두 이름이 같은 객체를 가리킬 수 있기 때문입니다.

## 기본 타입

타입은 값의 종류이며, 어떤 연산이 가능한지를 정합니다. `type()`에 값을 넣으면 그 타입을 확인할 수 있습니다.

다음 코드는 `3`, `3.14`, `"AI"`, `True`의 타입을 차례로 출력합니다. 결과는 `<class 'int'>`, `<class 'float'>`, `<class 'str'>`, `<class 'bool'>`입니다.

```python
print(type(3))
print(type(3.14))
print(type("AI"))
print(type(True))
```

| 타입 | 읽는 법 | 예시 | 의미 |
| --- | --- | --- | --- |
| `int` | integer | `3`, `100` | 정수 |
| `float` | floating-point number | `3.14`, `0.5` | 부동소수점 수 |
| `str` | string | `"AI"`, `"42"` | 문자열 |
| `bool` | boolean | `True`, `False` | 참 또는 거짓 |

`float`은 소수 부분이 있는 수를 계산할 때 자주 사용합니다. `3.0`처럼 소수 부분이 0인 값도 `float`으로 표현할 수 있습니다.

## 재할당과 타입

Python에서는 같은 이름이 다른 타입의 값을 가리킬 수 있습니다. 아래에서 `score`에 정수 `82`를 할당한 뒤 문자열 `"82"`를 할당하면, 타입 출력이 `<class 'int'>`에서 `<class 'str'>`로 바뀝니다.

```python
score = 82
print(type(score))

score = "82"
print(type(score))
```

타입을 갖는 것은 이름이 가리키는 값입니다. 이름에 타입을 미리 선언하지 않아도 되지만, 연산에는 타입별 규칙이 적용됩니다. 다음처럼 문자열 `"82"`와 정수 `3`을 더하면 `TypeError`가 발생합니다.

```python
score = "82"
bonus = 3

print(score + bonus)
```

문자열과 정수를 `+`로 바로 더할 수 없다는 오류입니다. 점수에 보너스 3점을 더하려는 계산이라면 먼저 점수를 숫자로 변환해야 합니다.

## Python의 언어 특성

타입을 검사하는 시점, 코드를 실행하는 방식, 주로 사용하는 용도는 서로 다른 분류 기준입니다.

| 구분 | 의미 | 예시 |
| --- | --- | --- |
| 정적 타입(static typing) | 실행 전에 타입을 검사한다 | Java, C, C++에서는 `int score`처럼 타입을 선언하는 코드를 볼 수 있다 |
| 동적 타입(dynamic typing) | 실행 중 값의 타입에 따라 연산을 처리한다 | Python에서 `score`가 정수를 가리키다가 문자열을 가리킬 수 있다 |
| 컴파일(compilation) | 코드를 다른 실행 형태로 변환한다 | C/C++에서는 실행 파일을 만들기 위한 컴파일 단계가 드러난다 |
| 인터프리터(interpreter) | 코드를 읽고 실행하는 프로그램이다 | Python 인터프리터에서 대화형 입력이나 스크립트를 실행한다 |
| 스크립팅·글루(scripting/glue) | 파일과 기존 도구를 연결하는 용도다 | Python으로 데이터 파일을 읽고 분석 라이브러리에 전달한다 |

이 분류들은 서로 배타적이지 않습니다. Python 공식 요약은 Python을 고수준(high-level), 인터프리터 방식(interpreted), 동적 의미론(dynamic semantics)을 가진 언어로 설명합니다.

## 숫자와 문자열

숫자 `30`에 숫자 `1`을 더하면 `31`입니다. 문자열 `"30"`에 문자열 `"1"`을 더하면 `301`이 출력됩니다.

```python
age_number = 30
age_text = "30"

print(age_number + 1)
print(age_text + "1")
```

CSV나 엑셀에서 읽은 값도 읽는 방식과 데이터 내용에 따라 문자열로 들어올 수 있습니다. 수량이나 점수 계산에 사용하려면 실제 타입을 확인해야 합니다.

| 원본 데이터 | 사람이 보는 의미 | 확인할 점 |
| --- | --- | --- |
| `"100"` | 수량 100 | 문자열인지 숫자인지 |
| `"0.92"` | 확률 점수 0.92 | 수치 계산 전에 `float` 변환이 필요한지 |
| `"True"` | 참처럼 보이는 텍스트 | 실제 `bool`인지 |
| `"2026-06-24"` | 날짜 | 문자열인지 날짜 타입인지 |

## 비교와 불리언

비교(comparison)의 결과는 참(`True`) 또는 거짓(`False`)인 불리언 값입니다. 점수 `92`가 기준 `60` 이상인지 비교하면 `True`가 됩니다. 다음 코드는 그 결과와 타입 `<class 'bool'>`을 출력합니다.

```python
score = 92
passed = score >= 60

print(passed)
print(type(passed))
```

`>=`는 왼쪽 값이 오른쪽 값보다 크거나 같은지 비교합니다. 예측 점수가 임계값(threshold) 이상인지, 데이터에 결측치가 있는지 같은 판단도 불리언으로 표현할 수 있습니다.

## 사례: 문자열 점수의 통과 여부

학생 Kim의 점수 `82.5`가 통과 기준 `60.0` 이상인지 판단한다고 하겠습니다. 이름은 문자열, 점수와 기준은 숫자, 판단 결과는 불리언으로 다룹니다. 다음 코드는 `Kim`, `82.5`, `True`를 차례로 출력합니다.

```python
student_name = "Kim"
score = 82.5
threshold = 60.0

passed = score >= threshold

print(student_name)
print(score)
print(passed)
```

하지만 점수가 파일에서 문자열 `"82.5"`로 들어왔다면 같은 비교를 할 수 없습니다. 아래 코드는 `str`과 `float` 사이에 `>=`를 적용할 수 없어 `TypeError`가 발생합니다.

```python
score = "82.5"
threshold = 60.0

print(score >= threshold)
```

문자열에 적힌 수를 숫자로 바꾸려면 `float()`을 사용할 수 있습니다. 다음 코드는 변환 전후 타입인 `<class 'str'>`, `<class 'float'>`과 통과 여부 `True`를 출력합니다.

```python
score_text = "82.5"
score = float(score_text)
threshold = 60.0

print(type(score_text))
print(type(score))
print(score >= threshold)
```

`score_text`는 원래 문자열을, `score`는 변환한 숫자를 가리킵니다. 마지막 코드의 `threshold`를 `90.0`으로 바꾸면 통과 여부는 `False`가 됩니다. 점수의 타입을 맞춰야 비교를 실행할 수 있고, 비교 기준을 바꾸면 판단 결과가 달라집니다.

## 체크리스트

- 값(value), 변수(variable), 타입(type)을 구분할 수 있다.
- Python의 `=`이 이름에 값을 할당(assign)하는 문법임을 설명할 수 있다.
- `int`, `float`, `str`, `bool`의 기본 차이를 설명할 수 있다.
- 숫자처럼 보이는 문자열과 실제 숫자를 구분할 수 있다.
- `type()`으로 값의 타입을 확인할 수 있다.
- 타입 오류가 났을 때 데이터 상태를 먼저 확인해야 함을 설명할 수 있다.
- 화면에는 숫자처럼 보여도 실제 타입을 먼저 확인해야 하는 이유를 설명할 수 있다.

## 출처와 참고 자료

- Python Software Foundation, [What is Python? Executive Summary](https://www.python.org/doc/essays/blurb/){: target="_blank" rel="noopener noreferrer" }, Python.org, 확인 날짜: 2026-07-20. Python의 동적 의미론(dynamic semantics), 동적 타이핑(dynamic typing), 고수준 내장 자료구조 설명 확인에 사용했다.
- Python Software Foundation, [An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Python 대화형 예제에서 프롬프트, 숫자, 문자열, 리스트가 어떻게 소개되는지 확인하는 근거로 사용했다.
- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. `int`, `float`, `str`, `bool` 등 기본 타입과 타입별 연산 차이를 확인하는 근거로 사용했다.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 확인 날짜: 2026-07-20. Python에서 객체가 정체성(identity), 타입(type), 값(value)을 가진다는 설명 확인에 사용했다.

# P2-2.1 변수(variable), 함수(function), 식(expression) 다시 읽기

P2-1.2에서는 수식(formula), 코드(code), 데이터(data)가 같은 계산을 서로 다른 방식으로 보여 준다는 관점을 잡았습니다. 이제 수식을 읽을 때 가장 먼저 만나는 기본 표기를 복구합니다.

\[
x
\]

\[
y = f(x)
\]

\[
\mathrm{loss} = f(\mathrm{prediction}, \mathrm{target})
\]

이런 표기는 오래전에 배운 수학에서는 너무 기본이라 지나쳤을 수 있습니다. 하지만 AI 문서에서는 변수(variable), 함수(function), 식(expression)을 읽지 못하면 모델(model), 입력(input), 출력(output), 손실(loss), 파라미터(parameter)의 위치를 잡기 어렵습니다.

이 절의 목표는 수학을 증명하는 것이 아닙니다. 수식 안의 기호가 “어떤 값”, “어떤 관계”, “어떤 계산”을 가리키는지 읽는 습관을 만드는 것입니다.

## 이 절의 범위

이 절은 변수(variable), 함수(function), 식(expression)을 AI 문서 독해에 필요한 수준으로 다룹니다. 시그마(sigma)를 사용한 반복 계산은 P2-2.2에서, 극한(limit)과 변화의 직관은 P2-2.3에서 다룹니다.

여기서는 다음 질문에 집중합니다.

```text
변수는 무엇을 담는 이름인가?
함수는 무엇을 무엇으로 바꾸는 관계인가?
식은 어떤 계산을 표현하는가?
코드의 변수와 수학의 변수는 어떻게 닮고 다른가?
```

## 이 절의 목표

- 변수(variable)를 값이나 데이터에 붙인 이름으로 읽을 수 있습니다.
- 함수(function)를 입력을 출력으로 바꾸는 관계로 읽을 수 있습니다.
- 식(expression)을 계산 가능한 관계나 절차의 압축 표현으로 볼 수 있습니다.
- `y = f(x)`를 모델 실행(inference)의 가장 단순한 형태로 해석할 수 있습니다.
- 코드의 변수와 수학 표기의 변수를 혼동하지 않고 연결할 수 있습니다.

## 변수는 값을 가리키는 이름이다

변수(variable)는 값을 가리키는 이름입니다. 수학에서는 보통 `x`, `y`, `n`, `w`처럼 짧은 기호를 씁니다.

\[
x = 3,\quad y = 2,\quad n = 4
\]

여기서 `x`, `y`, `n`은 값 자체가 아니라 값을 가리키는 이름입니다. AI 문서에서는 변수 이름이 더 많은 의미를 품습니다.

```text
x: 입력 데이터(input data)
y: 정답 또는 목표값(target)
w: 가중치(weight)
b: 편향(bias)
ŷ: 모델이 만든 예측값(prediction)
L: 손실(loss)
```

기호는 문서마다 달라질 수 있습니다. 그래서 수식을 볼 때는 “이 글에서 이 기호를 무엇으로 정의했는가?”를 먼저 찾아야 합니다. 같은 `x`라도 어떤 문서에서는 하나의 값이고, 어떤 문서에서는 벡터(vector)이며, 어떤 문서에서는 데이터셋(dataset) 전체일 수 있습니다.

## 코드의 변수와 수학의 변수

Python 코드에서도 변수를 씁니다.

```python
x = 3
y = 2
total = x + y
```

수학의 변수와 코드의 변수는 닮았습니다. 둘 다 어떤 값을 이름으로 가리킵니다. 하지만 완전히 같지는 않습니다.

| 관점 | 수학의 변수 | 코드의 변수 |
| --- | --- | --- |
| 주된 역할 | 관계를 간결하게 표현 | 값을 저장하고 실행 중 참조 |
| 값의 변화 | 문맥에 따라 고정 또는 변화 | 실행 흐름에서 재할당 가능 |
| 자료형 | 보통 문맥으로 추정 | 정수, 실수, 문자열, 배열 등 구체적 타입(type)이 있음 |
| 오류 | 정의가 모호하면 해석이 어려움 | 타입, shape, 이름 오류가 실행 중 발생 |

이 차이는 중요합니다. 수식에서는 `x`가 벡터라고만 설명해도 충분할 수 있지만, 코드에서는 `x`가 실제로 어떤 shape인지, 어떤 타입인지, 비어 있지는 않은지 확인해야 합니다.

```python
import numpy as np

x = np.array([1, 2, 3])

print(x)
print(x.shape)
print(x.dtype)
```

이 예시는 수학 표기의 `x`를 코드에서 확인 가능한 값으로 바꾸는 최소 예시입니다.

## 함수는 입력을 출력으로 바꾸는 관계다

함수(function)는 입력(input)을 받아 출력(output)을 만드는 관계입니다.

\[
y = f(x)
\]

이 식은 다음처럼 읽습니다.

```text
x가 들어간다.
f라는 관계 또는 규칙을 지난다.
y가 나온다.
```

AI 문맥에서는 `f`가 사람이 직접 만든 규칙일 수도 있고, 학습된 모델(model)일 수도 있습니다.

```text
규칙 기반 함수:
나이가 19 이상이면 성인으로 분류한다.

학습된 모델:
입력 특징을 바탕으로 구매 가능성을 예측한다.
```

코드에서는 둘 다 함수처럼 호출될 수 있습니다.

```python
def is_adult(age):
    return age >= 19

print(is_adult(20))
```

모델도 넓게 보면 입력을 받아 출력을 만드는 함수처럼 다룰 수 있습니다.

```python
prediction = model(input_data)
```

다만 머신러닝 모델은 단순한 규칙 함수와 다릅니다. 모델 내부에는 학습된 파라미터(parameter)가 있고, 같은 함수 구조라도 학습 후 파라미터 값에 따라 출력이 달라집니다.

## 식은 계산 관계를 표현한다

식(expression)은 값, 변수, 연산자(operator), 함수가 모여 계산 관계를 표현한 것입니다.

\[
x + y
\]

\[
2x + 1
\]

\[
f(x)
\]

\[
(\mathrm{prediction} - \mathrm{target})^2
\]

수학 문서에서는 식이 짧게 나오지만, 그 안에는 계산 순서가 들어 있습니다.

\[
(\mathrm{prediction} - \mathrm{target})^2
\]

이 식은 다음처럼 읽을 수 있습니다.

```text
예측값에서 목표값을 뺀다.
그 차이를 제곱한다.
오차의 크기를 양수로 만든다.
```

코드로는 다음처럼 쓸 수 있습니다.

```python
prediction = 2.8
target = 3.0
error = prediction - target
squared_error = error ** 2

print(squared_error)
```

여기서 중요한 것은 식이 단순한 기호 놀이가 아니라는 점입니다. 식은 어떤 값을 비교하고, 어떤 값을 크게 보거나 작게 보며, 어떤 결과를 만들지 정합니다.

## AI에서 자주 만나는 기본 관계

AI 문서에서 자주 만나는 관계를 아주 단순화하면 다음과 같습니다.

```text
prediction = model(input)
loss = compare(prediction, target)
updated_parameters = update(parameters, loss)
```

이 표현은 실제 학습 알고리즘을 정확히 적은 것이 아닙니다. 그러나 변수, 함수, 식의 위치를 잡는 데는 도움이 됩니다.

- `input`: 모델에 들어가는 데이터입니다.
- `model`: 입력을 출력으로 바꾸는 함수 또는 시스템입니다.
- `prediction`: 모델이 만든 출력입니다.
- `target`: 비교 기준이 되는 값입니다.
- `loss`: prediction과 target의 차이를 숫자로 표현한 값입니다.
- `parameters`: 학습 과정에서 조정되는 값입니다.
- `update`: loss를 줄이도록 parameters를 바꾸는 절차입니다.

이 구조를 알면 뒤에서 만나는 수식이 조금 덜 낯설어집니다. 복잡한 수식도 결국 어떤 값에 이름을 붙이고, 어떤 관계로 변환하고, 어떤 계산 결과를 비교하는 방식으로 읽을 수 있습니다.

## 이름은 이해를 돕지만 보장하지 않는다

변수 이름은 이해를 돕습니다. `x`, `y`보다 `input_data`, `target`, `prediction` 같은 이름이 더 읽기 쉽습니다. 하지만 이름만 믿으면 안 됩니다.

```python
prediction = [0, 1, 1, 0]
target = [0, 1, 0, 0]
```

이 코드는 이름만 보면 prediction과 target이 무엇인지 알 것 같습니다. 그러나 실제로는 더 확인해야 합니다.

```text
각 값은 클래스 번호인가?
확률인가?
참/거짓인가?
데이터 개수는 같은가?
순서는 맞는가?
```

AI에서 오류는 수식보다 데이터와 코드의 연결 지점에서 자주 생깁니다. 변수 이름이 그럴듯해도, 값의 모양(shape), 타입(type), 의미(meaning), 단위(unit)를 확인해야 합니다.

## 이 절에서 기억할 관점

변수, 함수, 식은 수학의 기초 표기이지만 AI 문서에서는 모델 계산을 읽는 출발점입니다.

```text
변수(variable): 값이나 데이터에 붙인 이름
함수(function): 입력을 출력으로 바꾸는 관계
식(expression): 값과 관계를 이용해 계산을 표현한 것
```

이 셋을 읽을 때는 항상 코드와 데이터로 되돌아갑니다.

```text
이 변수는 실제로 어떤 값인가?
이 함수는 무엇을 입력받고 무엇을 출력하는가?
이 식은 무엇을 비교하거나 계산하는가?
코드에서는 어떤 타입과 shape으로 나타나는가?
```

## 체크리스트

- 변수(variable)를 값이나 데이터에 붙인 이름으로 설명할 수 있다.
- 함수(function)를 입력(input)을 출력(output)으로 바꾸는 관계로 설명할 수 있다.
- 식(expression)을 계산 가능한 관계의 압축 표현으로 설명할 수 있다.
- `y = f(x)`를 AI 모델 실행의 기본 구조로 읽을 수 있다.
- 코드의 변수와 수학의 변수가 닮았지만 타입(type), shape, 재할당 같은 차이가 있음을 설명할 수 있다.
- 변수 이름만 믿지 않고 값의 의미, 타입, shape을 확인해야 함을 설명할 수 있다.

## 출처와 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/), Cambridge University Press, 2020, 확인 날짜: 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/), MIT Press, 2016, 확인 날짜: 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256), Nature, 2020, 확인 날짜: 2026-06-24.

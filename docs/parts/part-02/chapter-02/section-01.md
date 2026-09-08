# P2-2.1 변수(variable), 함수(function), 식(expression) 다시 읽기

> Section ID: `P2-2.1`
> Version: `v2026.09.08`

수식에서는 `x`처럼 값을 가리키는 기호와 `y = f(x)`처럼 입력과 출력의 관계를 나타내는 표기를 사용합니다.

\[
x
\]

\[
y = f(x)
\]

\[
\mathrm{loss} = f(\mathrm{prediction}, \mathrm{target})
\]

## 변수, 함수, 식의 역할

| 기준 | 왜 중요한가 |
| --- | --- |
| 변수는 값 자체가 아니라 값을 가리키는 이름이라는 점 | 기호를 실체와 바로 혼동하지 않게 해 줍니다. |
| 함수는 입력을 출력으로 바꾸는 관계라는 점 | 모델과 규칙을 같은 구조 안에서 읽게 해 줍니다. |
| 식은 계산이나 관계를 짧게 적은 표현이라는 점 | 손실, 예측, 오차 수식이 무엇을 하는지 해석하는 출발점이 됩니다. |

## 변수: 값의 이름

변수(variable)는 값을 가리키는 이름입니다. 수학에서는 보통 `x`, `y`, `n`, `w`처럼 짧은 기호를 씁니다.

\[
x = 3,\quad y = 2,\quad n = 4
\]

여기서 `x`, `y`, `n`은 값 자체가 아니라 값을 가리키는 이름입니다. AI 문서에서는 변수 이름이 더 많은 의미를 품습니다. 예를 들어 `x`는 입력 데이터(input data), `y`는 정답 또는 목표값(target), `w`는 가중치(weight), `b`는 편향(bias), `ŷ`는 모델이 만든 예측값(prediction), `L`은 손실(loss)로 자주 쓰입니다.

기호는 문서마다 달라질 수 있습니다. 그래서 수식을 볼 때는 “이 글에서 이 기호를 무엇으로 정의했는가?”를 먼저 찾아야 합니다. 같은 `x`라도 어떤 문서에서는 하나의 값이고, 어떤 문서에서는 벡터(vector)이며, 어떤 문서에서는 데이터셋(dataset) 전체일 수 있습니다.

## 수학 변수와 코드 변수

정수 `3`과 `2`에 각각 `x`, `y`라는 이름을 붙이고, 두 값의 합을 `total`로 가리킵니다.

```python
# x와 y는 계산에 이름을 붙인 값입니다.
x = 3
y = 2

# total은 두 값을 더한 식의 결과입니다.
total = x + y
```

실행 후 `x`는 `3`, `y`는 `2`, `total`은 `5`를 가리킵니다. 이 상태에서 `x`를 `10`으로 바꾸면 `total`도 `12`로 바뀔까요?

```python
x = 10
print(total)

total = x + y
print(total)
```

실행 결과:

```text
5
12
```

`total = x + y`는 그 줄이 실행될 때의 합을 계산합니다. `x`를 바꿔도 이미 계산된 `total`은 `5`이고, 덧셈과 대입을 다시 실행해야 `12`가 됩니다.

수학의 변수와 코드의 변수는 닮았습니다. 둘 다 어떤 값을 이름으로 가리킵니다. 하지만 완전히 같지는 않습니다.

| 관점 | 수학의 변수 | 코드의 변수 |
| --- | --- | --- |
| 주된 역할 | 관계를 간결하게 표현 | 값을 저장하고 실행 중 참조 |
| 값의 변화 | 문맥에 따라 고정 또는 변화 | 실행 흐름에서 재할당 가능 |
| 자료형 | 보통 문맥으로 추정 | 정수, 실수, 문자열, 배열 등 구체적 타입(type)이 있음 |
| 오류 | 정의가 모호하면 해석이 어려움 | 타입, shape, 이름 오류가 실행 중 발생 |

수식에서는 `x`가 벡터라고만 설명해도 충분할 수 있지만, 코드에서는 `x`가 실제로 어떤 shape인지, 어떤 타입인지, 비어 있지는 않은지 확인해야 합니다.

`x = [1, 2, 3]`을 NumPy 배열로 만들면 값뿐 아니라 배열의 모양인 `shape`와 원소의 자료형인 `dtype`도 확인할 수 있습니다.

```python
import numpy as np

# x는 여러 숫자를 담은 배열 변수입니다.
x = np.array([1, 2, 3])

print(x)

# shape는 각 축의 길이, dtype은 배열 원소의 자료형입니다.
print(x.shape)
print(x.dtype)
```

실행 결과 예시:

```text
[1 2 3]
(3,)
int64
```

`(3,)`은 원소가 3개인 1차원 배열이라는 뜻이고, 이 출력의 `int64`는 원소가 64비트 정수라는 뜻입니다.

## 함수: 입력과 출력의 관계

함수(function)는 입력(input)을 받아 출력(output)을 만드는 관계입니다.

\[
y = f(x)
\]

이 식은 `x가 들어가고, f라는 관계 또는 규칙을 지나, y가 나온다`고 읽습니다.

AI 문맥에서는 `f`가 사람이 직접 만든 규칙일 수도 있고, 학습된 모델(model)일 수도 있습니다. 예를 들어 규칙 기반 함수라면 `나이가 19 이상이면 성인으로 분류한다`고 읽을 수 있고, 학습된 모델이라면 `입력 특징을 바탕으로 구매 가능성을 예측한다`고 읽을 수 있습니다. 고객 정보가 입력이라면 `x`는 방문 횟수나 구매 횟수 같은 특징, `f`는 학습된 모델, `y`는 모델이 반환하는 예측값입니다.

`is_adult`는 입력 나이가 19 이상인지 비교해 `True` 또는 `False`를 반환합니다. 입력이 `20`이면 결과는 `True`입니다.

```python
def is_adult(age):
    # age는 판단할 입력값이고, True/False가 함수의 출력입니다.
    return age >= 19

print(is_adult(20))
```

실행 결과 예시:

```text
True
```

`is_adult(20)`의 입력을 `18`로 바꾸면 결과는 `False`, `19`로 바꾸면 `True`입니다. 이 함수에서는 `age >= 19`가 출력이 바뀌는 경계를 정합니다.

모델도 입력을 받아 출력을 만드는 함수처럼 호출할 수 있습니다.

`model`이 이미 정의되어 있다면, 다음 호출은 `input_data`를 모델에 넣고 반환된 예측값을 `prediction`에 연결합니다.

```python
# input_data는 모델에 넣는 입력이고, prediction은 모델이 돌려주는 예측값입니다.
prediction = model(input_data)
```

다만 머신러닝 모델은 단순한 규칙 함수와 다릅니다. 모델 내부에는 학습된 파라미터(parameter)가 있고, 같은 함수 구조라도 학습 후 파라미터 값에 따라 출력이 달라집니다.

## 식: 계산 순서

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

마지막 식은 예측값에서 목표값을 뺀 뒤 그 차이를 제곱하는 순서입니다. 차이가 `0`이면 제곱한 값도 `0`이고, 차이가 양수이거나 음수이면 제곱한 값은 양수가 됩니다.

예측값이 `2.8`, 목표값이 `3.0`일 때, 두 값의 차이를 구한 뒤 제곱합니다.

```python
# prediction은 모델의 예측값, target은 비교할 실제값입니다.
prediction = 2.8
target = 3.0

# error와 squared_error는 예측이 실제값에서 얼마나 벗어났는지 보는 값입니다.
error = prediction - target
squared_error = error ** 2

print(squared_error)
```

실행 결과 예시:

```text
0.04000000000000007
```

예측값은 목표값보다 `0.2` 작고, 제곱 오차는 약 `0.04`입니다. `prediction`을 `3.0`으로 바꿔 실행하면 차이가 없어져 제곱 오차도 `0.0`이 됩니다.

## AI의 입력·예측·손실·갱신

AI 문서에서 자주 만나는 관계를 아주 단순화하면 다음과 같습니다.

```text
prediction = model(input)
loss = compare(prediction, target)
updated_parameters = update(parameters, loss)
```

아래 이름들은 예측, 손실 계산, 파라미터 조정의 역할을 나타냅니다. 위 코드는 각 함수의 구현을 생략한 의사 코드입니다.

- `input`: 모델에 들어가는 데이터입니다.
- `model`: 입력을 출력으로 바꾸는 함수 또는 시스템입니다.
- `prediction`: 모델이 만든 출력입니다.
- `target`: 비교 기준이 되는 값입니다.
- `loss`: prediction과 target의 차이를 숫자로 표현한 값입니다.
- `parameters`: 학습 과정에서 조정되는 값입니다.
- `update`: loss를 줄이도록 parameters를 바꾸는 절차입니다.

## 변수 이름과 실제 값

변수 이름은 이해를 돕습니다. `x`, `y`보다 `input_data`, `target`, `prediction` 같은 이름이 더 읽기 쉽습니다. 하지만 이름만 믿으면 안 됩니다.

다음 두 리스트에는 예측과 정답을 뜻하는 이름이 붙어 있습니다.

```python
# prediction과 target은 여러 샘플의 예측값과 실제값을 나란히 비교하기 위한 목록입니다.
prediction = [0, 1, 1, 0]
target = [0, 1, 0, 0]
```

두 목록이 같은 네 학생을 같은 순서로 담고 있고, `1`은 합격, `0`은 불합격을 뜻한다고 가정합니다. 어느 학생의 예측이 실제 결과와 다를까요?

세 번째 학생입니다. `prediction`의 세 번째 값은 `1`, `target`의 세 번째 값은 `0`이므로, 합격으로 예측했지만 실제로는 불합격입니다. 나머지 세 학생은 예측과 실제 결과가 같습니다.

이 비교는 두 목록의 순서와 숫자의 뜻이 같다는 조건에서 성립합니다. 한 목록이 이름순이고 다른 목록이 성적순이라면 같은 위치의 값이 다른 학생을 가리킬 수 있습니다. 따라서 변수 이름뿐 아니라 각 값의 의미와 어느 대상에 대응하는지도 확인해야 합니다.

## 체크리스트

- 변수(variable)를 값이나 데이터에 붙인 이름으로 설명할 수 있다.
- 함수(function)를 입력(input)을 출력(output)으로 바꾸는 관계로 설명할 수 있다.
- 식(expression)을 계산 가능한 관계의 압축 표현으로 설명할 수 있다.
- `y = f(x)`를 AI 모델 실행의 기본 구조로 읽을 수 있다.
- 코드의 변수와 수학의 변수가 닮았지만 타입(type), shape, 재할당 같은 차이가 있음을 설명할 수 있다.
- 변수 이름만 믿지 않고 값의 의미, 타입, shape을 확인해야 함을 설명할 수 있다.
- 변수, 함수, 식을 읽을 때 값의 의미, 입력과 출력, 타입과 shape를 함께 확인할 수 있다.

## 출처와 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, 확인 날짜: 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, 확인 날짜: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 확인 날짜: 2026-07-19.
- Python Software Foundation, [Assignment statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements){: target="_blank" rel="noopener noreferrer" }, Python Language Reference, 확인 날짜: 2026-07-19. 코드 변수와 재할당 설명을 확인하는 직접 참고 자료입니다.
- NumPy Developers, [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, 확인 날짜: 2026-07-19. 배열 변수의 `shape`와 `dtype` 확인 예제를 뒷받침하는 공식 참고 자료입니다.

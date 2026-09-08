# P2-15.1 수식을 코드로 옮기는 작은 절차

> Section ID: `P2-15.1`
> Version: `v2026.09.08`

## 기호와 계산 순서

수식의 기호가 입력값 하나인지 여러 값의 묶음인지 구분하고, 각 값에 적용할 계산과 전체를 합칠 계산을 나눕니다.

```mermaid
--8<-- "assets/part-02/chapter-15/formula-to-code-flow-ko.mmd"
```

## 평균 제곱 오차

평균 제곱 오차(mean squared error, MSE)는 예측값과 실제값의 차이를 제곱해 평균낸 값입니다.

\[
\mathrm{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2
\]

각 기호는 다음 값을 가리킵니다.

| 기호 | 의미 |
| --- | --- |
| \(n\) | 데이터 개수 |
| \(y_i\) | i번째 실제값 |
| \(\hat{y}_i\) | i번째 예측값 |
| \(y_i - \hat{y}_i\) | i번째 오차 |
| \((y_i - \hat{y}_i)^2\) | 오차를 제곱한 값 |
| \(\sum\) | 모든 데이터에 대해 더한다 |
| \(\frac{1}{n}\) | 더한 값을 데이터 개수로 나누어 평균낸다 |

이 수식은 “각 샘플의 오차를 계산하고, 제곱하고, 모두 더한 뒤, 개수로 나눈다”로 읽을 수 있습니다.

## 반복문 계산

실제값 `[3.0, 5.0, 7.0]`과 예측값 `[2.5, 5.5, 8.0]`을 같은 위치끼리 짝짓습니다. 오차는 `[0.5, -0.5, -1.0]`, 제곱 오차는 `[0.25, 0.25, 1.0]`이고, 합 1.5를 3으로 나누면 MSE는 0.5입니다.

```python
actual = [3.0, 5.0, 7.0]
predicted = [2.5, 5.5, 8.0]

squared_errors = []

for y, y_hat in zip(actual, predicted):
    error = y - y_hat
    squared_errors.append(error ** 2)

mse = sum(squared_errors) / len(squared_errors)
print(mse)
```

이 코드는 수식의 각 부분을 거의 그대로 따라갑니다.

| 수식의 부분 | 코드의 부분 |
| --- | --- |
| \(y_i\), \(\hat{y}_i\) | `y`, `y_hat` |
| \(y_i - \hat{y}_i\) | `error = y - y_hat` |
| \((y_i - \hat{y}_i)^2\) | `error ** 2` |
| \(\sum\) | `sum(squared_errors)` |
| \(\frac{1}{n}\) | `/ len(squared_errors)` |

두 목록은 같은 샘플 순서와 같은 길이를 가져야 하며 비어 있으면 안 됩니다. `zip`은 기본적으로 짧은 목록 길이까지만 짝짓기 때문에 길이가 다르면 일부 값이 계산에서 빠질 수 있습니다.

## NumPy 배열 계산

NumPy 배열에서도 같은 입력으로 오차·제곱·평균을 계산하면 0.5가 나옵니다.

```python
import numpy as np

actual = np.array([3.0, 5.0, 7.0])
predicted = np.array([2.5, 5.5, 8.0])

errors = actual - predicted
squared_errors = errors ** 2
mse = np.mean(squared_errors)

print(mse)
```

두 배열이 모두 `(3,)`이므로 같은 위치의 값끼리 뺍니다. 같은 연산을 배열 전체에 적용하는 벡터화(vectorization) 표현입니다.

## 오차와 제곱 오차

MSE는 최종적으로 숫자 하나가 됩니다. 하지만 계산 과정을 확인할 때는 중간값도 함께 보는 것이 좋습니다.

```python
print(errors)
print(squared_errors)
print(mse)
```

출력은 다음과 같습니다.

```text
[ 0.5 -0.5 -1. ]
[0.25 0.25 1.  ]
0.5
```

오차(error)는 방향을 가집니다. 실제값보다 작게 예측했는지, 크게 예측했는지에 따라 부호가 달라집니다. 하지만 제곱 오차(squared error)는 음수가 되지 않습니다. 그래서 MSE는 오차의 크기를 평균적으로 보는 지표가 됩니다.

## 샘플별 차이

같은 샘플 위치에서 실제값과 예측값의 세로 간격을 비교합니다. 첫 두 샘플의 간격은 0.5이고 마지막 샘플은 1.0입니다. 이 예제의 연결선은 점들을 구분해 보기 위한 것이며 샘플 사이의 연속 변화를 뜻하지 않습니다.

```python
import matplotlib.pyplot as plt

index = np.arange(len(actual))

fig, ax = plt.subplots()
ax.plot(index, actual, marker="o", label="actual")
ax.plot(index, predicted, marker="o", label="predicted")
ax.set_xlabel("sample index")
ax.set_ylabel("value")
ax.set_title("Actual and predicted values")
ax.legend()
plt.show()
```

출력 이미지는 다음처럼 실제값과 예측값의 간격을 샘플별로 보여 줍니다.

![실제값과 예측값의 차이를 보여 주는 선 그래프](../../../assets/part-02/chapter-15/actual-predicted-mse.png)

이 절의 반복문 계산, NumPy 계산, 그래프 저장 흐름은 [`p2_15_1_formula_to_code_mse.py`](../../../assets/part-02/chapter-15/p2_15_1_formula_to_code_mse.py)로 한 번에 다시 실행할 수 있습니다. 이 스크립트는 `loop mse`, `errors`, `squared errors`, `numpy mse`를 출력하고, 같은 자산 폴더에 `actual-predicted-mse.png`를 저장합니다.

이 그래프는 MSE를 대신 계산하지 않습니다. 대신 숫자 하나로 압축되기 전의 차이를 눈으로 확인하게 도와줍니다.

## 사례 1. 마지막 예측값만 바꾸기

마지막 예측값을 8.0에서 실제값과 같은 7.0으로 바꾸면 제곱 오차가 `[0.25, 0.25, 0.0]`이 됩니다. MSE는 `0.5 / 3`, 약 0.167로 줄고 그래프의 마지막 두 점은 겹칩니다.

반대로 마지막 예측값을 9.0으로 바꾸면 마지막 오차는 −2, 제곱 오차는 4입니다. MSE는 `(0.25 + 0.25 + 4) / 3 = 1.5`가 됩니다. 오차 크기가 1에서 2로 두 배가 되면 해당 샘플의 제곱 오차는 1에서 4로 네 배가 됩니다.

반복문과 NumPy 코드의 입력을 각각 바꾸어 실행하면 같은 결과가 나와야 합니다. 결과가 다르면 입력 순서·길이·배열 모양과 평균을 낸 축을 확인합니다. 특히 `(3,)` 배열을 `(3, 1)`로 바꾸면 브로드캐스팅으로 모든 조합의 차이를 계산할 수 있으므로, 같은 샘플끼리 비교하는 원래 MSE와 달라집니다.

## 체크리스트

- 수식을 코드로 옮길 때 기호, 데이터 모양, 계산 절차를 먼저 나눠 읽을 수 있는가?
- MSE 수식에서 \(y_i\), \(\hat{y}_i\), \(n\), \(\sum\)이 무엇을 뜻하는지 설명할 수 있는가?
- 시그마를 반복 계산 또는 배열 계산으로 옮길 수 있다는 점을 설명할 수 있는가?
- 같은 계산을 Python 반복문과 NumPy 배열 계산으로 각각 쓸 수 있는가?
- 실제값과 예측값의 순서·길이·배열 모양을 맞춰야 하는 이유를 설명할 수 있는가?
- `errors`, `squared_errors`, `mse`의 차이를 설명할 수 있는가?
- 최종 숫자뿐 아니라 중간값도 확인해야 계산을 이해할 수 있다는 점을 설명할 수 있는가?
- 그래프가 계산을 대신하지 않고 수식 결과 해석을 돕는 보조 도구라는 점을 설명할 수 있는가?

## 출처와 참고 자료

- Python Software Foundation, `An Informal Introduction to Python`, Python documentation, 확인 날짜: 2026-07-20. [https://docs.python.org/3/tutorial/introduction.html](https://docs.python.org/3/tutorial/introduction.html){: target="_blank" rel="noopener noreferrer" } Python의 숫자, 리스트, 기본 계산 표현을 수식-코드 변환 예제의 기반으로 확인했습니다.
- NumPy Developers, `NumPy: the absolute basics for beginners`, NumPy documentation, 확인 날짜: 2026-07-20. [https://numpy.org/doc/stable/user/absolute_beginners.html](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" } 배열 생성, 배열 연산, `np.mean`을 이용한 벡터화 계산 설명의 근거입니다.
- Matplotlib Developers, `Quick start guide`, Matplotlib documentation, 확인 날짜: 2026-07-20. [https://matplotlib.org/stable/users/explain/quick_start.html](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" } `Figure`, `Axes`, `plot`, 라벨, 범례를 이용해 계산 결과를 그래프로 확인하는 예제의 기준입니다.

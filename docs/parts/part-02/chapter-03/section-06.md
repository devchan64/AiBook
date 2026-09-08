# P2-3.6 선형대수를 NumPy로 확인하기

> Section ID: `P2-3.6`
> Version: `v2026.09.08`

NumPy(넘파이)는 Python에서 배열(array)을 만들고 계산하는 라이브러리입니다. 배열의 `shape`는 각 축의 길이를 나타내고, `*`는 위치별 곱, `@`는 행렬 곱을 계산합니다.

## 실행 환경

이 절의 코드는 NumPy가 설치된 파이썬 환경에서 실행할 수 있습니다.

실행 환경은 먼저 P2-3.5의 [명령의 실행 위치](section-05.md#_2)를 기준으로 확인합니다. 파이썬을 아직 설치하지 않았다면 Google Colab 코드 셀에서 실행할 수 있고, 로컬 PC를 사용한다면 개인 PC 터미널에서 실행할 수 있습니다.

Colab 코드 셀에서는 다음처럼 NumPy를 준비할 수 있습니다.

```python
# Colab/Jupyter 코드 셀에서 NumPy를 설치하는 명령입니다.
%pip install numpy
```

로컬 PC 터미널에서는 다음 명령을 사용합니다.

```bash
python -m pip install numpy
```

그다음 파이썬 코드에서는 NumPy를 다음처럼 불러옵니다.

```python
# 설치된 NumPy를 Python 코드에서 np라는 짧은 이름으로 불러옵니다.
import numpy as np
```

여기서 `np`는 NumPy를 짧게 부르기 위한 관례적인 별칭(alias)입니다.

이 절의 전체 예제 코드는 다음 파일로도 받을 수 있습니다.

- [p2_3_6_numpy_linear_algebra.py](../../../assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)

프로젝트 루트에서 실행한다면 개인 PC의 터미널에서 다음 명령을 사용할 수 있습니다.

```bash
python docs/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py
```

이 파일은 본문에 나오는 벡터 덧셈, 스칼라배, 위치별 곱, 행렬 곱, 배치 계산을 한 번에 출력합니다.

## 벡터와 행렬 만들기

벡터(vector)는 값의 목록으로 만들 수 있습니다.

```python
import numpy as np

# x는 두 성분을 가진 입력 벡터입니다.
x = np.array([2, 3])

print(x)

# shape는 이 벡터가 성분 2개짜리 1차원 배열임을 확인하게 합니다.
print(x.shape)
```

출력은 다음처럼 볼 수 있습니다.

```text
[2 3]
(2,)
```

`(2,)`는 값이 2개인 1차원 배열이라는 뜻입니다. 수식으로 쓰면 다음 벡터와 대응됩니다.

\[
\mathbf{x} = [2,\ 3]
\]

행렬(matrix)은 행(row)과 열(column)을 가진 2차원 배열로 만들 수 있습니다.

```python
# W는 입력 벡터를 다른 출력으로 바꾸는 2x2 가중치 행렬입니다.
W = np.array([
    [4, 1],
    [5, 2],
])

print(W)

# W의 shape는 행렬 곱에서 차원이 맞는지 확인하는 기준입니다.
print(W.shape)
```

출력은 다음처럼 볼 수 있습니다.

```text
[[4 1]
 [5 2]]
(2, 2)
```

`(2, 2)`는 2행 2열이라는 뜻입니다.

\[
W =
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

## shape과 곱셈 조건

AI 코드에서 계산이 맞지 않을 때는 값보다 shape을 먼저 확인해야 할 때가 많습니다.

`x @ W`에서는 벡터 `x`의 길이가 행렬 `W`의 행 수와 같아야 합니다.

```python
# x는 입력 벡터, W는 그 입력에 곱할 가중치 행렬입니다.
x = np.array([2, 3])
W = np.array([
    [4, 1],
    [5, 2],
])

# 두 shape를 나란히 보면 x @ W가 가능한지 먼저 판단할 수 있습니다.
print("x shape:", x.shape)
print("W shape:", W.shape)
```

출력은 다음과 같습니다. `x shape: (2,)`, `W shape: (2, 2)`입니다.

이 정보는 `x는 값이 몇 개인가`, `W는 몇 개 입력을 받아 몇 개 출력을 만드는가`, `이 둘은 곱할 수 있는 모양인가`라는 질문에 답하게 해 줍니다.

`x`는 입력값 2개를 가진 벡터이고 `W`는 입력 2개를 받아 출력 2개를 만드는 가중치 행렬(weight matrix)입니다.

## 벡터 덧셈과 스칼라배

벡터 덧셈(vector addition)은 같은 위치의 값끼리 더합니다.

```python
# a와 b는 같은 shape를 가진 두 벡터입니다.
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 같은 위치의 성분끼리 더해지는지 확인합니다.
print(a + b)
```

출력은 다음과 같습니다.

```text
[5 7 9]
```

수식으로는 다음과 같습니다.

\[
[1,\ 2,\ 3] + [4,\ 5,\ 6] = [5,\ 7,\ 9]
\]

스칼라배(scalar multiplication)는 배열의 각 값에 같은 숫자를 곱합니다.

```python
# 앞에서 만든 벡터 a의 각 성분에 같은 스칼라 2를 곱합니다.
print(2 * a)
```

출력은 다음과 같습니다.

```text
[2 4 6]
```

수식으로는 다음과 같습니다.

\[
2[1,\ 2,\ 3] = [2,\ 4,\ 6]
\]

## `*`: 위치별 곱

NumPy에서 배열끼리 `*`를 사용하면 보통 위치별 곱(element-wise multiplication)이 됩니다.

```python
# a와 b는 위치별 곱을 비교할 두 벡터입니다.
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# *는 같은 위치의 성분끼리 곱하는 연산입니다.
print(a * b)
```

출력은 다음과 같습니다.

```text
[ 4 10 18]
```

수식으로는 다음과 같습니다.

\[
[1,\ 2,\ 3] \odot [4,\ 5,\ 6] = [4,\ 10,\ 18]
\]

여기서 중요한 점은 `*`가 행렬 곱이 아니라는 것입니다. 같은 위치끼리 곱하는 계산입니다. 즉 `*`는 위치별 곱이고 `@`는 행렬 곱입니다.

## `@`: 행렬 곱

NumPy에서 `@`는 행렬 곱(matrix multiplication)에 사용합니다.

```python
# x는 입력 벡터이고, W는 출력 성분을 만드는 가중치 행렬입니다.
x = np.array([2, 3])
W = np.array([
    [4, 1],
    [5, 2],
])

# y는 x와 W의 행렬 곱으로 만들어진 출력 벡터입니다.
y = x @ W

print(y)
print(y.shape)
```

출력은 다음과 같습니다.

```text
[23  8]
(2,)
```

이 계산은 P2-3.3에서 본 가중합과 같습니다.

\[
[2,\ 3]
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
=
[23,\ 8]
\]

첫 번째 출력은 다음 계산입니다.

\[
2 \times 4 + 3 \times 5 = 23
\]

두 번째 출력은 다음 계산입니다.

\[
2 \times 1 + 3 \times 2 = 8
\]

즉 `@`는 “곱하고 더해서 새 벡터를 만드는 계산”입니다.

## 배치 행렬 계산

여러 입력 샘플(sample)을 행렬로 묶으면 같은 가중치 행렬을 한 번에 적용할 수 있습니다.

```python
# X는 두 샘플을 행으로 가진 입력 행렬입니다.
X = np.array([
    [2, 3],
    [1, 4],
])

# W는 각 입력 샘플을 출력 벡터로 바꾸는 가중치 행렬입니다.
W = np.array([
    [4, 1],
    [5, 2],
])

# Y는 배치 입력 X 전체에 W를 적용한 출력 행렬입니다.
Y = X @ W

print(X.shape)
print(W.shape)
print(Y)
print(Y.shape)
```

출력은 다음과 같습니다.

```text
(2, 2)
(2, 2)
[[23  8]
 [24  9]]
(2, 2)
```

수식으로는 다음과 같습니다.

\[
X =
\begin{bmatrix}
2 & 3 \\
1 & 4
\end{bmatrix}
\]

\[
W =
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

\[
XW =
\begin{bmatrix}
23 & 8 \\
24 & 9
\end{bmatrix}
\]

여기서 첫 번째 행은 첫 번째 샘플의 출력이고, 두 번째 행은 두 번째 샘플의 출력입니다. 즉 입력 샘플 2개가 있고, 각 샘플은 값 2개를 가지며, 같은 `W`를 적용한 뒤, 출력 샘플도 2개가 되고 각 출력은 값 2개를 가집니다.

이것이 배치(batch) 계산의 가장 작은 예시입니다.

## 입력 길이 불일치

다음 계산은 바로 맞지 않습니다.

```python
# bad_x는 성분이 3개라서 2행짜리 W와 행렬 곱 차원이 맞지 않습니다.
bad_x = np.array([2, 3, 4])
W = np.array([
    [4, 1],
    [5, 2],
])

bad_y = bad_x @ W
```

`bad_x`의 shape은 `(3,)`이고, `W`의 shape은 `(2, 2)`입니다. 입력값은 3개인데 가중치 행렬은 입력 2개를 받는 모양입니다. 즉 `bad_x shape: (3,)`, `W shape: (2, 2)`입니다.

따라서 어떤 입력값과 어떤 가중치를 곱해야 하는지 맞지 않습니다. 실제 NumPy는 이런 경우 shape이 맞지 않는다는 오류를 냅니다.

세 번째 입력도 계산에 사용하려면 `W`에 그 입력에 대응하는 가중치 행이 필요합니다. 출력 두 개를 유지한다면 `W`의 shape은 `(3, 2)`가 되어야 합니다. 입력값을 임의로 삭제해 shape만 맞추면 모델에 넣는 데이터의 의미가 달라집니다.

## 체크리스트

- NumPy 배열(array)로 벡터와 행렬을 만들 수 있다.
- `.shape`로 벡터와 행렬의 모양을 확인할 수 있다.
- 벡터 덧셈과 스칼라배를 코드와 수식으로 연결할 수 있다.
- NumPy의 `*`가 위치별 곱(element-wise multiplication)임을 설명할 수 있다.
- NumPy의 `@`가 행렬 곱(matrix multiplication)임을 설명할 수 있다.
- `x @ W`에서 입력 shape, 가중치 shape, 출력 shape을 읽을 수 있다.
- 여러 샘플을 행렬로 묶어 같은 가중치 행렬을 적용하는 배치(batch) 계산을 설명할 수 있다.
- NumPy에서 문법 자체보다 수식, shape, 출력이 서로 맞는지 함께 보는 습관을 설명할 수 있다.
- `*`와 `@`를 구분하고, 값보다 shape를 먼저 보는 기준을 적용할 수 있다.

## 출처와 참고 자료

- 이 절의 예제 코드: [p2_3_6_numpy_linear_algebra.py](../../../assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)
- NumPy Developers, [NumPy documentation](https://numpy.org/doc/){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-19.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-19.
- NumPy Developers, [`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html){: target="_blank" rel="noopener noreferrer" }, 배열 생성 API의 인자와 예제를 확인할 수 있습니다. 확인 날짜: 2026-07-19.
- NumPy Developers, [`numpy.ndarray.shape`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html){: target="_blank" rel="noopener noreferrer" }, 배열 차원을 튜플로 확인하는 `shape` 속성을 확인할 수 있습니다. 확인 날짜: 2026-07-19.
- NumPy Developers, [`numpy.matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html){: target="_blank" rel="noopener noreferrer" }, 행렬 곱과 shape 불일치 오류 조건을 확인할 수 있습니다. 확인 날짜: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 확인 날짜: 2026-07-19.

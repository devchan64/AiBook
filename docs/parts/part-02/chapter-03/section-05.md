# P2-3.5 선형대수를 NumPy로 확인하기

P2-3.1에서는 스칼라(scalar), 벡터(vector), 행렬(matrix)의 모양을 봤습니다. P2-3.2에서는 벡터 공간(vector space)과 위치(position)의 직관을 봤고, P2-3.3에서는 행렬 곱(matrix multiplication)을 가중합(weighted sum)의 재사용으로 읽었습니다. P2-3.4에서는 파이썬 실행 환경을 Google Colab과 로컬 PC로 나누어 봤습니다.

이제 같은 내용을 작은 코드로 확인합니다. 여기서는 NumPy(넘파이)를 사용합니다. NumPy는 파이썬(Python)에서 배열(array)을 만들고 계산하는 대표적인 라이브러리입니다.

```text
수식으로 본다.
-> 배열로 만든다.
-> shape을 확인한다.
-> 계산 결과를 확인한다.
```

이 절의 목표는 NumPy 문법을 많이 외우는 것이 아닙니다. 선형대수 기호가 코드에서 어떤 모양으로 나타나는지 확인하는 것입니다.

## 이 절의 범위

이 절은 NumPy 배열(array), shape, 벡터 덧셈(vector addition), 스칼라배(scalar multiplication), 위치별 곱(element-wise multiplication), 행렬 곱(matrix multiplication)을 작은 예제로 확인합니다. 큰 데이터 처리, 성능 최적화, 브로드캐스팅(broadcasting)의 세부 규칙, GPU 계산은 다루지 않습니다.

여기서는 다음 질문에 집중합니다.

```text
벡터와 행렬은 NumPy에서 어떻게 생겼는가?
shape은 코드에서 어떻게 확인하는가?
위치별 계산과 행렬 곱은 코드에서 어떻게 구분하는가?
배치 계산은 어떤 모양으로 보이는가?
```

## 이 절의 목표

- NumPy 배열(array)로 벡터와 행렬을 만들 수 있습니다.
- `.shape`로 데이터 모양을 확인할 수 있습니다.
- 벡터 덧셈과 스칼라배를 코드로 확인할 수 있습니다.
- `*`와 `@`의 차이를 설명할 수 있습니다.
- 여러 샘플을 행렬로 묶어 같은 가중치 행렬을 적용하는 계산을 읽을 수 있습니다.
- 수식, shape, 코드 결과를 함께 보는 습관을 만들 수 있습니다.

## 실행 환경

이 절의 코드는 NumPy가 설치된 파이썬 환경에서 실행할 수 있습니다.

실행 환경은 먼저 P2-3.4의 [실행 환경을 먼저 구분한다](section-04.md#_2)를 기준으로 확인합니다. 파이썬을 아직 설치하지 않았다면 Google Colab 코드 셀에서 실행할 수 있고, 로컬 PC를 사용한다면 개인 PC 터미널에서 실행할 수 있습니다.

Colab 코드 셀에서는 다음처럼 NumPy를 준비할 수 있습니다.

```python
%pip install numpy
```

로컬 PC 터미널에서는 다음 명령을 사용합니다.

```bash
python -m pip install numpy
```

그다음 파이썬 코드에서는 NumPy를 다음처럼 불러옵니다.

```python
import numpy as np
```

여기서 `np`는 NumPy를 짧게 부르기 위한 관례적인 별칭(alias)입니다.

이 절의 전체 예제 코드는 다음 파일로도 받을 수 있습니다.

- [p2_3_5_numpy_linear_algebra.py](../../../assets/part-02/chapter-03/p2_3_5_numpy_linear_algebra.py)

레포지토리 루트에서 실행한다면 개인 PC의 터미널에서 다음 명령을 사용할 수 있습니다.

```bash
python docs/assets/part-02/chapter-03/p2_3_5_numpy_linear_algebra.py
```

이 파일은 본문에 나오는 벡터 덧셈, 스칼라배, 위치별 곱, 행렬 곱, 배치 계산을 한 번에 출력합니다.

## 벡터와 행렬 만들기

벡터(vector)는 값의 목록으로 만들 수 있습니다.

```python
import numpy as np

x = np.array([2, 3])

print(x)
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
W = np.array([
    [4, 1],
    [5, 2],
])

print(W)
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

## shape을 먼저 확인한다

AI 코드에서 계산이 맞지 않을 때는 값보다 shape을 먼저 확인해야 할 때가 많습니다.

```python
x = np.array([2, 3])
W = np.array([
    [4, 1],
    [5, 2],
])

print("x shape:", x.shape)
print("W shape:", W.shape)
```

출력은 다음과 같습니다.

```text
x shape: (2,)
W shape: (2, 2)
```

이 정보는 다음 질문에 답하게 해 줍니다.

```text
x는 값이 몇 개인가?
W는 몇 개 입력을 받아 몇 개 출력을 만드는가?
이 둘은 곱할 수 있는 모양인가?
```

P2-3.3의 관점으로 읽으면, `x`는 입력값 2개를 가진 벡터이고 `W`는 입력 2개를 받아 출력 2개를 만드는 가중치 행렬(weight matrix)입니다.

## 벡터 덧셈과 스칼라배 확인하기

벡터 덧셈(vector addition)은 같은 위치의 값끼리 더합니다.

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

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

이 두 계산은 P2-3.2에서 말한 벡터 공간의 최소 계산과 연결됩니다.

## `*`는 위치별 곱이다

NumPy에서 배열끼리 `*`를 사용하면 보통 위치별 곱(element-wise multiplication)이 됩니다.

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

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

여기서 중요한 점은 `*`가 행렬 곱이 아니라는 것입니다. 같은 위치끼리 곱하는 계산입니다.

```text
*  : 위치별 곱
@  : 행렬 곱
```

## `@`는 행렬 곱이다

NumPy에서 `@`는 행렬 곱(matrix multiplication)에 사용합니다.

```python
x = np.array([2, 3])
W = np.array([
    [4, 1],
    [5, 2],
])

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

## 여러 샘플을 한꺼번에 계산하기

여러 입력 샘플(sample)을 행렬로 묶으면 같은 가중치 행렬을 한 번에 적용할 수 있습니다.

```python
X = np.array([
    [2, 3],
    [1, 4],
])

W = np.array([
    [4, 1],
    [5, 2],
])

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

여기서 첫 번째 행은 첫 번째 샘플의 출력이고, 두 번째 행은 두 번째 샘플의 출력입니다.

```text
입력 샘플 2개
각 샘플은 값 2개
같은 W를 적용
출력 샘플 2개
각 출력은 값 2개
```

이것이 배치(batch) 계산의 가장 작은 예시입니다.

## shape 오류를 의도적으로 생각해 보기

다음 계산은 바로 맞지 않습니다.

```python
bad_x = np.array([2, 3, 4])
W = np.array([
    [4, 1],
    [5, 2],
])

bad_y = bad_x @ W
```

`bad_x`의 shape은 `(3,)`이고, `W`의 shape은 `(2, 2)`입니다. 입력값은 3개인데 가중치 행렬은 입력 2개를 받는 모양입니다.

```text
bad_x shape: (3,)
W shape:     (2, 2)
```

따라서 어떤 입력값과 어떤 가중치를 곱해야 하는지 맞지 않습니다. 실제 NumPy는 이런 경우 shape이 맞지 않는다는 오류를 냅니다.

오류 메시지를 외우는 것보다 중요한 것은 다음 질문입니다.

```text
왼쪽의 마지막 크기와 오른쪽의 입력 방향 크기가 맞는가?
내가 곱하려는 것이 위치별 곱인가, 행렬 곱인가?
출력 shape은 무엇이 되어야 하는가?
```

## 이 절에서 기억할 관점

NumPy는 선형대수를 코드로 확인하게 해 주는 도구입니다. 중요한 것은 문법 자체보다 수식, shape, 출력이 서로 맞는지 함께 보는 습관입니다.

```text
수식: xW
shape: (2,) @ (2, 2)
출력: (2,)
의미: 입력 2개를 받아 출력 2개를 만든다.
```

행렬 곱을 볼 때는 `*`와 `@`를 구분합니다. `*`는 위치별 곱이고, `@`는 행렬 곱입니다. 이 구분만 확실해도 AI 코드에서 많은 혼란을 줄일 수 있습니다.

## 체크리스트

- NumPy 배열(array)로 벡터와 행렬을 만들 수 있다.
- `.shape`로 벡터와 행렬의 모양을 확인할 수 있다.
- 벡터 덧셈과 스칼라배를 코드와 수식으로 연결할 수 있다.
- NumPy의 `*`가 위치별 곱(element-wise multiplication)임을 설명할 수 있다.
- NumPy의 `@`가 행렬 곱(matrix multiplication)임을 설명할 수 있다.
- `x @ W`에서 입력 shape, 가중치 shape, 출력 shape을 읽을 수 있다.
- 여러 샘플을 행렬로 묶어 같은 가중치 행렬을 적용하는 배치(batch) 계산을 설명할 수 있다.

## 출처와 참고 자료

- 이 절의 예제 코드: [p2_3_5_numpy_linear_algebra.py](../../../assets/part-02/chapter-03/p2_3_5_numpy_linear_algebra.py)
- NumPy Developers, [NumPy documentation](https://numpy.org/doc/){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-06-24.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 확인 날짜: 2026-06-24.

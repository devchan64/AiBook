# P2-3.6 선형대수를 NumPy로 확인하기

> Section ID: `P2-3.6`
> Version: `v2026.09.14`

NumPy(넘파이)는 Python에서 배열을 만들고 계산하는 라이브러리입니다. 앞 절의 벡터 비교를 코드로 계산하고, 입력과 가중치의 모양을 바꾸어 출력이 어떻게 달라지는지 확인할 수 있습니다. 배열의 `shape`는 각 축의 길이를 나타냅니다.

## 실행 환경

설치 위치는 [P2-3.5의 실행 환경](section-05.md#_2)을 따릅니다. Colab/Jupyter에서는 코드 셀에 다음 명령을 입력합니다.

```text title="IPython · 노트북 코드 셀"
%pip install numpy
```

로컬 PC에서는 터미널에 다음 명령을 입력합니다.

```bash
python -m pip install numpy
```

아래 Python 블록은 위에서부터 같은 세션에서 실행합니다. 뒤의 블록은 앞에서 만든 변수와 `np`를 사용합니다. 전체 코드를 한 번에 실행하려면 다음 파일을 사용합니다.

[p2_3_6_numpy_linear_algebra.py](../../../assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py)

저장소 루트에서 실행하는 명령입니다. 파일만 다운로드했다면 저장한 폴더에서 `python p2_3_6_numpy_linear_algebra.py`로 실행합니다.

```bash
python docs/assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py
```

## 배열의 shape과 출력

`import numpy as np`는 NumPy를 `np`라는 짧은 이름으로 불러옵니다. `np.array`에 값의 목록을 넣으면 1차원 배열을, 행별 목록을 넣으면 2차원 배열을 만듭니다.

```python
import numpy as np

x = np.array([2, 3])
W = np.array([[4, 1], [5, 2]])
print(x.shape)
print(W.shape)
print(x @ W)
```

```text title="텍스트 · 실행 결과"
(2,)
(2, 2)
[23  8]
```

`x.shape`의 `(2,)`는 성분이 2개인 1차원 배열입니다. `(1, 2)`처럼 한 행을 가진 2차원 배열과는 구분합니다. `W.shape`의 `(2, 2)`는 2행 2열입니다. `x @ W`는 `x`와 `W`의 각 열을 곱하고 더하므로 출력은 `[2×4+3×5, 2×1+3×2] = [23, 8]`입니다.

## `*`와 `@`의 차이

같은 shape의 배열에서 `+`와 `*`는 같은 위치의 성분끼리 계산합니다. 숫자 하나를 곱하면 모든 성분에 같은 숫자를 곱합니다. 1차원 벡터끼리 `@`를 쓰면 곱한 성분들을 더한 내적 값 하나가 나옵니다.

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)
print(2 * a)
print(a * b)
print(a @ b)
```

```text title="텍스트 · 실행 결과"
[5 7 9]
[2 4 6]
[ 4 10 18]
32
```

`a * b`는 `[4, 10, 18]`을 남기지만 `a @ b`는 `4+10+18=32`로 합칩니다. 앞의 `x @ W`는 벡터를, 여기의 `a @ b`는 숫자 하나를 반환합니다. `@`의 결과 모양은 입력 배열의 차원에 따라 달라집니다. shape이 다른 배열의 `*`에는 브로드캐스팅 규칙도 적용되므로, 위치별 곱이라고 해서 반드시 같은 shape만 허용하는 것은 아닙니다.

## 구매량 벡터 비교

P2-3.4에서 사용한 `[커피 구매량, 차 구매량]` 벡터를 그대로 계산합니다. `np.linalg.norm(v)`는 이 1차원 벡터의 2-노름을 구합니다. `v-q`는 두 구매량의 차이이고, 그 노름이 유클리드 거리입니다.

```python
q = np.array([1, 1])
candidates = {
    "a": np.array([2, 2]),
    "b": np.array([1, 0]),
    "c": np.array([10, 10]),
}
for name, v in candidates.items():
    dot = q @ v
    norm = np.linalg.norm(v)
    distance = np.linalg.norm(v - q)
    cosine = dot / (np.linalg.norm(q) * norm)
    print(f"{name}: dot={dot}, norm={norm:.3f}, "
          f"distance={distance:.3f}, cosine={cosine:.3f}")
```

```text title="텍스트 · 실행 결과"
a: dot=4, norm=2.828, distance=1.414, cosine=1.000
b: dot=1, norm=1.000, distance=1.000, cosine=0.707
c: dot=20, norm=14.142, distance=12.728, cosine=1.000
```

`dot`, `norm`, `distance`, `cosine`은 각각 내적·길이·거리·코사인 유사도입니다. 출력의 `:.3f`는 소수점 아래 세 자리까지 표시하라는 뜻이며 계산 자체를 세 자리로 제한하지 않습니다. 거리로는 `b`가 가장 가깝고, 코사인 유사도로는 `a`와 `c`가 같습니다. 내적은 구매량이 많은 `c`에서 가장 큽니다. 이 코사인 계산은 두 벡터의 길이가 0이 아닐 때만 사용할 수 있습니다.

`candidates`의 `a`를 `[4, 4]`로 바꾸고 다시 실행해 보세요. 내적은 `8`, 길이는 약 `5.657`, 거리는 약 `4.243`으로 바뀌지만 코사인 유사도는 `1.000`으로 유지됩니다. 구매 비율은 같고 구매량만 늘어난 결과입니다.

## 샘플 수·입력 수·출력 수

입력 3개를 행으로 묶고, 각 입력의 성분 2개를 출력 성분 4개로 바꿉니다. 아래 가중치는 계산을 확인하기 위해 직접 정한 예시이며, 학습으로 얻은 값은 아닙니다.

```python
X = np.array([
    [2, 3],
    [1, 4],
    [0, 1],
])
W = np.array([
    [4, 1, 1, 0],
    [5, 2, 0, 1],
])
Y = X @ W
print(X.shape, W.shape, Y.shape)
print(Y)
```

```text title="텍스트 · 실행 결과"
(3, 2) (2, 4) (3, 4)
[[23  8  2  3]
 [24  9  1  4]
 [ 5  2  0  1]]
```

| 배열 | shape | 행과 열의 의미 |
| --- | --- | --- |
| `X` | `(3, 2)` | 샘플 3개, 샘플당 입력 성분 2개 |
| `W` | `(2, 4)` | 입력 성분 2개에 대한 가중치, 출력 성분 4개 |
| `Y` | `(3, 4)` | 샘플 3개, 샘플당 출력 성분 4개 |

`(3, 2) @ (2, 4) → (3, 4)`에서 가운데의 `2`가 일치해야 계산할 수 있습니다. 결과에는 샘플 수 `3`과 출력 성분 수 `4`가 남습니다. `W`의 첫 두 열은 앞의 `[23, 8]` 계산을 유지하고, 뒤 두 열은 입력의 첫째·둘째 성분을 각각 그대로 출력합니다. 같은 `W`를 각 샘플에 적용하므로 출력 한 행은 입력 한 행에 대응합니다.

## 차원 오류와 가중치 행 추가

성분이 3개인 입력을 현재의 2행짜리 `W`에 곱하면 오류가 납니다. 아래 코드는 오류를 잡아 입력 성분 수와 가중치 행 수를 출력합니다. 전체 오류 메시지는 NumPy 버전에 따라 다를 수 있습니다.

```python
bad_x = np.array([2, 3, 4])
try:
    bad_x @ W
except ValueError:
    print("ValueError: input components = 3, weight rows = 2")
```

```text title="텍스트 · 실행 결과"
ValueError: input components = 3, weight rows = 2
```

세 번째 입력을 사용하려면 그 입력에 대응하는 가중치 행이 필요합니다. 입력을 임의로 삭제해 모양만 맞추면 데이터의 의미가 바뀝니다. 세 번째 입력이 첫째·넷째 출력에 각각 1배씩 더해지도록 `[1, 0, 0, 1]`을 새 행으로 추가합니다. `np.vstack`은 배열을 행 방향으로 쌓습니다.

```python
W_fixed = np.vstack([W, [1, 0, 0, 1]])
print(W_fixed.shape)
print(bad_x @ W_fixed)
```

```text title="텍스트 · 실행 결과"
(3, 4)
[27  8  2  7]
```

원래 `[2, 3]`의 출력 `[23, 8, 2, 3]`에 세 번째 입력 `4`가 `[4, 0, 0, 4]`를 더해 `[27, 8, 2, 7]`이 됩니다. shape을 맞추는 일과 새 입력의 역할을 정하는 일은 함께 이루어져야 합니다.

## 연습: 샘플을 하나 더 넣으면

배치 계산의 `X` 마지막에 `[2, 0]` 행을 추가하고 `W`는 바꾸지 않습니다. 실행 전에 `X`와 `Y`의 shape, 새 출력 행을 예상해 보세요.

??? note "계산과 해설"
    `X.shape`은 `(4, 2)`, `Y.shape`은 `(4, 4)`가 됩니다. 새 출력 행은 `[8, 2, 2, 0]`입니다. 샘플 수가 늘어도 각 샘플의 입력 성분 수는 2개이므로 `W`를 바꿀 필요가 없습니다. 앞선 세 출력 행도 그대로 유지됩니다.

## 체크리스트

- `(2,)`와 `(1, 2)`가 다른 배열 모양임을 설명할 수 있는가?
- 벡터끼리 `*`와 `@`를 적용했을 때 배열과 숫자 하나로 결과가 갈리는 이유를 설명할 수 있는가?
- 내적·노름·거리·코사인 유사도의 계산을 앞 절의 구매량 비교와 연결할 수 있는가?
- `(3, 2) @ (2, 4)`의 결과 shape을 실행 전에 예상할 수 있는가?
- 샘플 수를 늘리는 것과 입력 성분 수를 늘리는 것이 가중치에 미치는 차이를 설명할 수 있는가?

## 출처와 참고 자료

- NumPy Developers, [NumPy documentation](https://numpy.org/doc/){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-19.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-19.
- NumPy Developers, [`numpy.array`](https://numpy.org/doc/stable/reference/generated/numpy.array.html){: target="_blank" rel="noopener noreferrer" }, 배열 생성 API의 인자와 예제를 확인할 수 있습니다. 확인 날짜: 2026-07-19.
- NumPy Developers, [`numpy.ndarray.shape`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html){: target="_blank" rel="noopener noreferrer" }, 배열 차원을 튜플로 확인하는 `shape` 속성을 확인할 수 있습니다. 확인 날짜: 2026-07-19.
- NumPy Developers, [`numpy.matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html){: target="_blank" rel="noopener noreferrer" }, 행렬 곱과 shape 불일치 오류 조건을 확인할 수 있습니다. 확인 날짜: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 확인 날짜: 2026-07-19.
- [numpy.linalg.norm](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-09-14.
- [cosine_similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-09-14.
- [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-09-14.

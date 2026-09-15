# P2-11.4 보충학습: NumPy에서 모양(shape)과 원본 공유를 함께 읽는 법

> Section ID: `P2-11.4`
> Version: `v2026.09.15`

## 슬라이스와 원본 공유

NumPy 배열의 기본 슬라이싱은 원본과 데이터를 공유하는 뷰(view)를 만듭니다. `scores[1:4]`로 얻은 배열의 첫 값을 999로 바꾸면 원본의 1번 위치도 999가 됩니다.

```python
import numpy as np

scores = np.array([82, 75, 45, 90, 61])
middle = scores[1:4]

middle[0] = 999

print(scores)
print(middle)
```

출력은 다음과 같습니다.

```text
[ 82 999  45  90  61]
[999  45  90]
```

## 위치·조건 선택과 복사

위치 목록으로 선택하는 팬시 인덱싱(fancy indexing)과 참·거짓 배열로 선택하는 불리언 마스크(boolean mask)는 데이터를 복사합니다. 다음 코드에서 `picked`의 첫 값을 500으로, `high_scores`의 첫 값을 700으로 바꿔도 원본은 `[82, 75, 45, 90, 61]`로 남습니다.

```python
scores = np.array([82, 75, 45, 90, 61])

picked = scores[[1, 3, 4]]
high_scores = scores[scores >= 80]

picked[0] = 500
high_scores[0] = 700

print(scores)
print(picked)
print(high_scores)
```

출력은 다음과 같습니다.

```text
[82 75 45 90 61]
[500  90  61]
[700  90]
```

여기서 `scores[[1, 3, 4]]`는 1번, 3번, 4번 위치 값을 따로 모읍니다. 이런 방식을 팬시 인덱싱이라고 부릅니다.

`scores[scores >= 80]`는 조건이 참인 값만 고릅니다. 이런 방식은 불리언 마스크라고 부릅니다.

## 길이 1인 축 추가

`np.newaxis`는 지정한 위치에 길이 1인 축을 추가합니다. 점수 세 개를 담은 `(3,)` 배열을 `(3, 1)` 또는 `(1, 3)`으로 볼 수 있습니다. 이 선택 결과도 원본과 데이터를 공유합니다.

```python
scores = np.array([82, 75, 45])

print(scores.shape)
print(scores[:, np.newaxis].shape)
print(scores[np.newaxis, :].shape)
```

출력은 다음과 같습니다.

```text
(3,)
(3, 1)
(1, 3)
```

세 배열의 값은 같지만 차원과 모양이 다릅니다.

| 표현 | shape | 읽는 법 |
| --- | --- | --- |
| `scores` | `(3,)` | 길이 3인 1차원 배열 |
| `scores[:, np.newaxis]` | `(3, 1)` | 3행 1열 열 벡터처럼 보기 |
| `scores[np.newaxis, :]` | `(1, 3)` | 1행 3열 행 벡터처럼 보기 |

즉 `np.newaxis`는 숫자를 새로 만드는 것이 아니라, 배열을 어느 방향으로 계산에 맞출지 정리하는 표기입니다.

## 모든 조합의 차이 계산

`[10, 20, 30]` 각각에서 1과 2를 뺀 결과를 모두 구하려면 3행 2열 배열이 필요합니다. 첫 배열을 `(3, 1)`, 둘째 배열을 `(1, 2)`로 바꾸면 브로드캐스팅으로 여섯 조합을 계산할 수 있습니다.

```python
a = np.array([10, 20, 30])
b = np.array([1, 2])

diff = a[:, np.newaxis] - b[np.newaxis, :]

print(a[:, np.newaxis].shape)
print(b[np.newaxis, :].shape)
print(diff)
```

출력은 다음과 같습니다.

```text
(3, 1)
(1, 2)
[[ 9  8]
 [19 18]
 [29 28]]
```

첫 행 `[9, 8]`은 10에서 1과 2를 뺀 결과입니다. 마지막 행 `[29, 28]`은 30에서 두 값을 뺀 결과입니다. `b`를 `[1, 5]`로 바꾸면 둘째 열만 `[5, 15, 25]`로 바뀝니다. 축을 추가하지 않고 `a - b`를 계산하면 `(3,)`과 `(2,)`이 호환되지 않아 오류가 납니다.

## reshape와 전치

`reshape`는 원소를 새 모양으로 묶고, 2차원 배열의 `.T`는 행 축과 열 축을 바꿉니다. 같은 `(3, 2)` 모양을 만들어도 값의 배치는 다릅니다.

```python
matrix = np.array([[10, 11, 12], [20, 21, 22]])
print(matrix.reshape(3, 2))
print(matrix.T)
```

```text
[[10 11]
 [12 20]
 [21 22]]
[[10 20]
 [11 21]
 [12 22]]
```

원래 행이 학생이라면 전치한 배열의 열이 학생을 나타냅니다. `reshape(3, 2)`는 이 의미를 알아서 보존하지 않습니다. 또한 `(3,)`인 1차원 배열의 `.T`는 여전히 `(3,)`입니다. 열 벡터 모양이 필요하면 `[:, np.newaxis]`로 축을 추가합니다.

`reshape`는 가능하면 뷰를 반환하지만 메모리 배치에 따라 복사할 수도 있습니다. 다음 예제는 작은 배열에서 실제 데이터 공유 여부를 확인합니다.

```python
matrix = np.array([[10, 11, 12], [20, 21, 22]])
reshaped = matrix.reshape(3, 2)
transposed_flat = matrix.T.reshape(-1)

print(np.shares_memory(matrix, reshaped))
print(np.shares_memory(matrix, transposed_flat))
```

출력은 `True`, `False`입니다. `-1`은 원소 수에 맞춰 해당 축의 길이를 추론하라는 뜻입니다. 이 전치 배열을 기본 순서로 평탄화할 때는 복사가 필요합니다. 모든 `reshape`가 뷰이거나 모든 `reshape`가 복사라고 외우지 않습니다. 원본을 보존한 채 수정할 목적이면 `.copy()`로 의도를 명시합니다.

## 사례: 선택한 점수만 보정하기

원본 점수 `[82, 75, 45, 90, 61]`에서 1번부터 3번 위치만 골라 10점씩 더한다고 합시다. 슬라이스를 그대로 수정하면 원본도 바뀝니다. 원본과 보정 결과를 비교하려면 선택한 구간을 `.copy()`로 복사해야 합니다.

```python
scores = np.array([82, 75, 45, 90, 61])
adjusted = scores[1:4].copy()
adjusted += 10

print(scores)
print(adjusted)
```

```text
[82 75 45 90 61]
[ 85  55 100]
```

`.copy()`를 지우고 코드 전체를 다시 실행하면 원본도 `[82, 85, 55, 100, 61]`로 바뀝니다. 보정 전후 평균을 비교하려는데 원본까지 바뀌면 비교 기준인 보정 전 데이터가 훼손됩니다.

조건 선택의 결과가 복사본이라는 설명은 값을 **읽어 새 변수에 담는 경우**에 해당합니다. `scores[scores < 60] = 60`처럼 선택한 위치에 직접 대입하면 원본의 해당 점수가 바뀝니다. 반면 `low = scores[scores < 60]`으로 따로 담은 뒤 `low[:] = 60`을 실행하면 원본은 바뀌지 않습니다.

```mermaid
--8<-- "assets/part-02/chapter-11/shape-view-broadcast-flow-ko.mmd"
```

## 예제 코드 파일

선택 방식에 따른 원본 변경과 `shape` 변화를 순서대로 실행해 비교합니다.

- [p2_11_4_views_shapes.py](../../../assets/part-02/chapter-11/p2_11_4_views_shapes.py)

```bash
python docs/assets/part-02/chapter-11/p2_11_4_views_shapes.py
```

## 체크리스트

- `x[1:4]`와 `x[[1, 3, 4]]`의 차이를 설명할 수 있는가?
- 불리언 마스크가 무엇을 고르는지 설명할 수 있는가?
- `(3,)`, `(3, 1)`, `(1, 3)`의 차이를 설명할 수 있는가?
- `np.newaxis`가 broadcasting과 왜 연결되는지 설명할 수 있는가?
- 원본 보존이 중요할 때 `.copy()` 여부를 먼저 점검해야 한다는 점을 기억하는가?
- NumPy 코드를 읽을 때 값만이 아니라 `shape`와 원본 공유 여부를 함께 봐야 한다는 점을 설명할 수 있는가?
- `reshape`와 전치의 값 배치를 구분하고 `np.shares_memory`로 원본 공유를 확인할 수 있는가?

## 출처와 참고 자료

- NumPy Developers, [Copies and views](https://numpy.org/doc/stable/user/basics.copies.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, 확인 날짜: 2026-09-08. view와 copy의 차이, 기본 인덱싱 view, advanced indexing copy, `.base` 확인 설명의 근거로 사용했다.
- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, 확인 날짜: 2026-09-08. 선택 방식에 따라 shape와 원본 공유 여부가 달라지는 설명 확인에 사용했다.
- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, 확인 날짜: 2026-07-20. `np.newaxis`와 shape 조정이 broadcasting 이해와 연결되는 설명의 근거로 사용했다.
- NumPy Developers, [numpy.shares_memory](https://numpy.org/doc/stable/reference/generated/numpy.shares_memory.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual, 확인 날짜: 2026-09-15. 작은 배열 예제의 메모리 공유 판별.

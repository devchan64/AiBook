# P2-11.4 보충학습: NumPy에서 모양(shape)과 원본 공유를 함께 읽는 법

> Section ID: `P2-11.4`
> Version: `v2026.09.08`

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

## 사례 1. 선택한 점수만 보정하기

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

`.copy()`를 지우고 코드 전체를 다시 실행하면 원본도 `[82, 85, 55, 100, 61]`로 바뀝니다. 보정 전후 평균을 비교하려는데 원본까지 바뀌면 두 평균을 같은 데이터에서 계산하게 됩니다.

조건 선택의 결과가 복사본이라는 설명은 값을 **읽어 새 변수에 담는 경우**에 해당합니다. `scores[scores < 60] = 60`처럼 선택한 위치에 직접 대입하면 원본의 해당 점수가 바뀝니다. 반면 `low = scores[scores < 60]`으로 따로 담은 뒤 `low[:] = 60`을 실행하면 원본은 바뀌지 않습니다.

```mermaid
--8<-- "assets/part-02/chapter-11/shape-view-broadcast-flow-ko.mmd"
```

## 체크리스트

- `x[1:4]`와 `x[[1, 3, 4]]`의 차이를 설명할 수 있는가?
- 불리언 마스크가 무엇을 고르는지 설명할 수 있는가?
- `(3,)`, `(3, 1)`, `(1, 3)`의 차이를 설명할 수 있는가?
- `np.newaxis`가 broadcasting과 왜 연결되는지 설명할 수 있는가?
- 원본 보존이 중요할 때 `.copy()` 여부를 먼저 점검해야 한다는 점을 기억하는가?
- NumPy 코드를 읽을 때 값만이 아니라 `shape`와 원본 공유 여부를 함께 봐야 한다는 점을 설명할 수 있는가?

## 출처와 참고 자료

- NumPy Developers, [Copies and views](https://numpy.org/doc/stable/user/basics.copies.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual, 확인 날짜: 2026-09-08. view와 copy의 차이, 기본 인덱싱 view, advanced indexing copy, `.base` 확인 설명의 근거로 사용했다.
- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual, 확인 날짜: 2026-09-08. 선택 방식에 따라 shape와 원본 공유 여부가 달라지는 설명 확인에 사용했다.
- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, NumPy v2.5 Manual, 확인 날짜: 2026-07-20. `np.newaxis`와 shape 조정이 broadcasting 이해와 연결되는 설명의 근거로 사용했다.

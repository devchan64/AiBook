# P2-2.2 시그마(sigma)와 반복 계산

> Section ID: `P2-2.2`
> Version: `v2026.09.08`

시그마(sigma)는 여러 값을 더하는 계산을 압축한 표기입니다.

\[
\sum
\]

시그마(sigma)는 낯설어 보이지만, 핵심은 단순합니다. 여러 값을 반복해서 더하라는 뜻입니다. AI 문서에서는 데이터 여러 개의 합, 평균(mean), 손실(loss)의 합, 배치(batch) 단위 계산을 설명할 때 자주 등장합니다.

## 반복 범위와 더할 값

| 기준 | 왜 중요한가 |
| --- | --- |
| 시그마는 같은 모양의 덧셈을 반복하라는 압축 표기라는 점 | 낯선 기호를 계산 구조로 다시 읽게 해 줍니다. |
| 인덱스는 몇 번째 값을 더하는지 구분하는 이름이라는 점 | 반복 위치를 놓치지 않게 해 줍니다. |
| 시그마가 AI 문서에 자주 나오는 이유는 여러 데이터를 모아 합·평균·손실을 계산하기 때문이라는 점 | 통계와 손실 집계가 왜 같은 표기를 공유하는지 보여 줍니다. |

## 시그마의 구성

시그마에는 반복 범위와 더할 항을 함께 적습니다.

\[
\sum_{i=1}^{n}x_i
\]

이 한 줄에는 네 가지 정보가 들어 있습니다.

- 큰 기호 \(\sum\): 더하라는 명령입니다.
- 아래 \(i=1\): 어디서 시작할지 알려 줍니다.
- 위 \(n\): 어디까지 반복할지 알려 줍니다.
- 오른쪽 \(x_i\): 반복할 때마다 무엇을 더할지 알려 줍니다.

이렇게 나누어 보면 시그마는 갑자기 등장한 어려운 기호가 아니라, 반복 덧셈을 짧게 적는 문장처럼 읽을 수 있습니다.

1. i를 1에서 시작합니다.
2. i가 n이 될 때까지 반복합니다.
3. 매번 `x_i`를 더합니다.

즉 시그마는 “합”이라는 결과만 말하는 기호가 아닙니다. 무엇을 어떤 순서와 범위로 모을지 함께 적는 표기입니다. 이 관점은 코드의 반복문(loop)을 떠올릴 때도 유용합니다.

다만 시그마가 코드의 반복문과 완전히 같다는 뜻은 아닙니다. 수학 표기는 계산 구조를 압축해 보여 주고, 코드는 그 계산을 실제 실행 절차로 풀어 씁니다.

## 간단한 시그마 풀이

시그마는 짧은 식을 직접 풀어 써 보면서 읽습니다.

\[
\sum_{i=1}^{3} i
\]

이 식은 \(i\)를 1부터 3까지 바꾸며 \(i\) 자체를 더하라는 뜻입니다.

```text
i = 1일 때 더할 값: 1
i = 2일 때 더할 값: 2
i = 3일 때 더할 값: 3
```

따라서 다음처럼 풀어 쓸 수 있습니다.

\[
\sum_{i=1}^{3} i = 1 + 2 + 3 = 6
\]

조금 더 AI 문서에 가까운 형태로 보면 다음과 같습니다.

\[
\sum_{i=1}^{3}x_i
\]

만약 \(x_1=2\), \(x_2=4\), \(x_3=6\)이라면 다음처럼 계산합니다.

\[
\sum_{i=1}^{3}x_i = x_1 + x_2 + x_3 = 2 + 4 + 6 = 12
\]

평균까지 계산하면 다음과 같습니다.

\[
\frac{1}{3}\sum_{i=1}^{3}x_i = \frac{1}{3}(2 + 4 + 6) = 4
\]

## 인덱스와 반복문

시그마에서 `i`는 인덱스(index)입니다. 인덱스는 지금 몇 번째 값을 보고 있는지 나타내는 이름입니다.

\[
\sum_{i=1}^{n}x_i
\]

여기서 각 부분은 다음처럼 읽습니다.

- `i`: 반복 위치를 나타내는 인덱스(index)
- `1`: 시작 위치
- `n`: 끝 위치
- `xi`: i번째 값
- `Σ`: i를 바꾸며 값을 더하라는 표시

코드로는 다음과 비슷합니다.

값 네 개가 들어 있는 리스트 `values`입니다. 전체 합 `10`이 출력됩니다.

```python
# values는 반복해서 더할 값들의 목록입니다.
values = [1, 2, 3, 4]

# total은 반복문이 지나가며 합을 누적하는 변수입니다.
total = 0

for value in values:
    total = total + value

print(total)
```

실행 결과 예시:

```text
10
```

수식의 `i`와 코드의 `value`가 완전히 같은 것은 아닙니다. 하지만 둘 다 반복 중 현재 보고 있는 대상을 가리킨다는 점에서 연결됩니다.

## 합과 평균

평균(mean)은 시그마를 이해하기 좋은 예입니다. 여러 값을 모두 더하고, 그 개수로 나누면 평균입니다.

\[
\mathrm{mean} = \frac{x_1 + x_2 + x_3 + x_4}{4}
\]

시그마로 쓰면 다음처럼 압축됩니다.

\[
\mathrm{mean} = \frac{1}{n}\sum_{i=1}^{n}x_i
\]

이 식은 다음처럼 읽습니다.

1. i를 1부터 n까지 바꾸며 `x_i`를 모두 더합니다.
2. 그 합을 n으로 나눕니다.

코드로는 다음처럼 쓸 수 있습니다.

값 네 개가 들어 있는 리스트 `values`입니다. 평균값 `2.5`가 출력됩니다.

```python
# values는 평균을 낼 데이터이고, mean은 그 요약값입니다.
values = [1, 2, 3, 4]
mean = sum(values) / len(values)

print(mean)
```

실행 결과 예시:

```text
2.5
```

NumPy 배열(array)을 쓰면 더 짧게 쓸 수 있습니다.

값 네 개를 담은 NumPy 배열 `values`입니다. 평균값 `2.5`가 출력됩니다.

```python
import numpy as np

# values는 NumPy 배열로 바꾼 반복 계산 대상입니다.
values = np.array([1, 2, 3, 4])

# mean은 배열 전체를 하나의 평균값으로 집계합니다.
mean = values.mean()

print(mean)
```

실행 결과 예시:

```text
2.5
```

여기서 `values.mean()`은 내부적으로 평균 계산을 수행합니다. 수식의 시그마를 직접 쓰지는 않지만, 여러 값을 모아 계산한다는 구조는 같습니다.

## 샘플별 손실과 평균 손실

머신러닝에서 손실(loss)은 모델 출력과 기준값 사이의 차이를 숫자로 표현합니다. 데이터가 하나라면 손실도 하나만 계산하면 됩니다.

\[
\mathrm{loss} = (\mathrm{prediction} - \mathrm{target})^2
\]

하지만 실제 학습에서는 데이터가 여러 개입니다. 각 데이터마다 예측(prediction)과 목표값(target)이 있고, 각 데이터마다 손실이 생깁니다.

\[
\mathrm{loss}_1,\ \mathrm{loss}_2,\ \mathrm{loss}_3,\ \cdots,\ \mathrm{loss}_n
\]

전체 손실(total loss)을 단순히 더하면 다음과 같습니다.

\[
\mathrm{total\_loss} = \mathrm{loss}_1 + \mathrm{loss}_2 + \cdots + \mathrm{loss}_n
\]

시그마로 쓰면 다음과 같습니다.

\[
\mathrm{total\_loss} = \sum_{i=1}^{n}\mathrm{loss}_i
\]

평균 손실(mean loss)은 이 합을 데이터 개수로 나눈 것입니다.

\[
\mathrm{mean\_loss} = \frac{1}{n}\sum_{i=1}^{n}\mathrm{loss}_i
\]

코드로는 다음처럼 볼 수 있습니다.

예측값 리스트 `predictions`와 정답 리스트 `targets`입니다. 각 샘플 손실의 평균값이 출력됩니다.

```python
# predictions와 targets는 각 샘플의 예측값과 실제값을 짝으로 비교하기 위한 목록입니다.
predictions = [2.8, 4.1, 5.0]
targets = [3.0, 4.0, 4.5]

# losses에는 샘플별 제곱 오차가 차례로 쌓입니다.
losses = []
for prediction, target in zip(predictions, targets):
    loss = (prediction - target) ** 2
    losses.append(loss)

# mean_loss는 여러 샘플의 손실을 하나로 요약한 평균 손실입니다.
mean_loss = sum(losses) / len(losses)
print(mean_loss)
```

실행 결과 예시:

```text
0.09999999999999999
```

이 예시는 실제 딥러닝 학습 코드를 단순화한 것입니다. 핵심은 데이터가 여러 개라서 같은 계산이 반복되고, 그 반복 결과를 합치거나 평균 낸다는 점입니다.

## 배치의 손실 집계

딥러닝에서는 데이터를 하나씩 처리하기보다 여러 개를 묶어 배치(batch)로 처리하는 일이 많습니다. 배치 안에는 여러 샘플(sample)이 있고, 모델은 각 샘플에 대해 출력을 만듭니다. 여기서 `batch`는 여러 입력 데이터 묶음이고, `prediction`은 각 입력에 대한 모델 출력이며, `loss`는 각 출력과 기준값의 차이이고, `mean_loss`는 배치 안 손실의 평균입니다.

이때도 시그마의 관점은 유지됩니다. 즉 배치 안의 각 샘플을 보고, 각 샘플의 손실을 계산한 뒤, 그 손실들을 더하거나 평균 냅니다.

## 반복문과 배열 연산

앞의 세 샘플에서 제곱 오차는 각각 약 `0.04`, `0.01`, `0.25`이고, 평균은 `(0.04 + 0.01 + 0.25) / 3 = 0.1`입니다. NumPy에서는 뺄셈과 제곱을 배열의 각 위치에 적용하고 `mean()`으로 평균을 구합니다.

예측 배열 `predictions`와 정답 배열 `targets`입니다. 평균 손실값이 출력됩니다.

```python
import numpy as np

# predictions와 targets는 배열 계산으로 한 번에 비교할 예측값과 실제값입니다.
predictions = np.array([2.8, 4.1, 5.0])
targets = np.array([3.0, 4.0, 4.5])

# losses는 샘플별 제곱 오차 배열이고, mean_loss는 그 평균입니다.
losses = (predictions - targets) ** 2
mean_loss = losses.mean()

print(mean_loss)
```

실행 결과 예시:

```text
0.09999999999999999
```

반복문이 보이지 않지만 반복 계산이 사라진 것은 아닙니다. 배열 계산이 여러 값을 한 번에 다루도록 표현을 바꾼 것입니다.

## 체크리스트

- 시그마(sigma)를 반복 덧셈의 압축 표기로 설명할 수 있다.
- 인덱스(index), 시작 위치, 끝 위치, 더할 항(term)을 구분할 수 있다.
- 평균(mean)을 시그마 표기와 코드로 모두 설명할 수 있다.
- 여러 데이터의 손실(loss)을 더하거나 평균 내는 흐름을 설명할 수 있다.
- 반복문(loop)과 배열 계산(array computation)이 시그마 표기와 연결될 수 있음을 설명할 수 있다.
- 시그마가 나오면 “무엇을 몇 번 더하는가?”라는 질문으로 풀어 읽을 수 있다.
- 시그마가 이후 통계(statistics), 손실 계산(loss calculation), 배치 계산(batch calculation), 최적화(optimization)를 읽는 데 도움이 되는 이유를 설명할 수 있다.
- 간단한 시그마 식을 항(term)별로 펼쳐 쓰고 합 또는 평균을 계산할 수 있다.
- 평균, 손실, 배치 계산이 같은 집계 구조라는 점을 시그마와 코드로 연결해 설명할 수 있다.

## 출처와 참고 자료

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, 확인 날짜: 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, 확인 날짜: 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 확인 날짜: 2026-07-19.
- NumPy Developers, [numpy.sum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, 확인 날짜: 2026-07-19. 배열 원소의 합과 축 기준 합 계산을 설명하는 공식 참고 자료입니다.
- NumPy Developers, [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, 확인 날짜: 2026-07-19. 평균 계산과 `mean()` 예제를 뒷받침하는 공식 참고 자료입니다.

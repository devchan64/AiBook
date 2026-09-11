# P2-13.1 그래프(plot)는 무엇을 드러내는가

> Section ID: `P2-13.1`
> Version: `v2026.09.08`

## 손실값의 변화

학습을 반복하며 기록한 손실값입니다. 표에서는 세 번째 값이 1.12라는 사실을 정확히 읽을 수 있고, 선 그래프에서는 감소 폭이 점차 작아지는 모양을 볼 수 있습니다.

| epoch | loss |
| ---: | ---: |
| 1 | 2.40 |
| 2 | 1.65 |
| 3 | 1.12 |
| 4 | 0.86 |
| 5 | 0.79 |

첫 구간의 감소 폭은 `2.40 - 1.65 = 0.75`, 마지막 구간은 `0.86 - 0.79 = 0.07`입니다. 다음 코드는 순서가 있는 다섯 손실값을 점으로 찍고 선으로 연결합니다.

```python
import matplotlib.pyplot as plt

epochs = [1, 2, 3, 4, 5]
loss = [2.40, 1.65, 1.12, 0.86, 0.79]

fig, ax = plt.subplots()
ax.plot(epochs, loss, marker="o")
ax.set_xlabel("epoch")
ax.set_ylabel("loss")
ax.set_title("Loss decreases over epochs")
plt.show()
```

위 코드를 실행하면 다음처럼 epoch가 늘어날수록 loss가 내려가는 모양을 확인할 수 있습니다.

![에폭이 늘수록 손실이 감소하는 선 그래프](../../../assets/part-02/chapter-13/pyplot-loss-line-ko.svg)

이 책의 자산 폴더에는 같은 예제를 파일로 다시 만들 수 있는 저장형 스크립트도 함께 둡니다. 화면에서 바로 확인할 때는 위처럼 `plt.show()`를 쓰고, 문서에 넣을 PNG를 다시 만들 때는 [`p2_13_1_plot_questions.py`](../../../assets/part-02/chapter-13/p2_13_1_plot_questions.py)를 실행합니다.

## 같은 평균, 다른 변화

동작 A의 구간별 값은 `[1.0, 2.0, 2.0, 1.0]`, 동작 B는 `[1.5, 1.5, 1.5, 1.5]`입니다. 두 평균은 모두 1.5지만 A는 중간에 높아지고 B는 일정합니다. 평균 하나를 그리면 이 차이가 사라지므로 구간별 값을 비교합니다.

```python
import matplotlib.pyplot as plt

steps = [1, 2, 3, 4]
action_a = [1.0, 2.0, 2.0, 1.0]
action_b = [1.5, 1.5, 1.5, 1.5]

fig, ax = plt.subplots()
ax.plot(steps, action_a, marker="o", label="action A")
ax.plot(steps, action_b, marker="o", label="action B")
ax.set_xlabel("segment")
ax.set_ylabel("signal level")
ax.set_title("Same mean, different pattern")
ax.legend()
plt.show()
```

## 변화·관계·분포·이상값

그래프는 값의 변화, 변수 사이 관계, 값이 몰린 구간, 다른 값들과 떨어진 관측을 보여 줍니다.

| 질문 | 그래프가 도와주는 것 | 예시 |
| --- | --- | --- |
| 변화(trend) | 시간이나 순서에 따라 값이 어떻게 움직이는지 본다 | 학습 epoch별 loss |
| 관계(relationship) | 두 값이 함께 움직이는지 본다 | 공부 시간과 점수 |
| 분포(distribution) | 값이 어디에 몰려 있는지 본다 | 점수 분포, 오차 분포 |
| 이상값(outlier) | 유난히 튀는 값이 있는지 본다 | 다른 측정값과 크게 떨어진 센서 값 |

## 공부 시간과 점수의 관계

예를 들어 학생 네 명의 데이터를 다시 봅니다.

| name | study_hours | score |
| --- | ---: | ---: |
| Kim | 2 | 62 |
| Park | 4 | 71 |
| Lee | 6 | 82 |
| Choi | 8 | 88 |

이 표에서 값 자체를 보려면 표로 읽을 수 있습니다. 하지만 “공부 시간이 늘수록 점수도 함께 높아지는가?”를 보려면 산점도(scatter plot)가 더 자연스럽습니다.

```python
import matplotlib.pyplot as plt

study_hours = [2, 4, 6, 8]
scores = [62, 71, 82, 88]

fig, ax = plt.subplots()
ax.scatter(study_hours, scores)
ax.set_xlabel("study hours")
ax.set_ylabel("score")
ax.set_title("Study hours and score")
plt.show()
```

점 하나는 학생 한 명입니다. Kim은 `(2, 62)`, Choi는 `(8, 88)`에 찍힙니다. 네 학생의 기록에서는 공부 시간이 긴 학생일수록 점수가 높습니다.

![공부 시간과 점수의 관계를 보여 주는 산점도](../../../assets/part-02/chapter-13/pyplot-study-scatter-ko.svg)

이 그래프는 원인을 증명하지 않습니다. 다만 두 값이 함께 움직이는 모양을 빠르게 확인하게 해 줍니다.

## Figure와 Axes

Matplotlib 공식 문서는 데이터를 `Figure` 위에 그래프로 그린다고 설명합니다. `Figure`는 전체 그림이고, 그 안에는 하나 이상의 `Axes`가 들어갈 수 있습니다. `Axes`는 실제 데이터가 그려지는 좌표 영역입니다.

| 용어 | 직관 |
| --- | --- |
| `Figure` | 그림 전체 종이 |
| `Axes` | 실제 좌표와 데이터가 그려지는 칸 |
| `plot`, `scatter`, `hist` | Axes 위에 데이터를 어떤 방식으로 그릴지 정하는 함수 |

`plt.subplots()`로 그림과 좌표 영역을 만들고 `(1, 2)`, `(2, 4)`, `(3, 3)`을 선으로 연결합니다.

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [2, 4, 3])
plt.show()
```

`plt.subplots()`는 `Figure`와 하나의 `Axes`를 함께 만듭니다. 그다음 `ax.plot(...)`처럼 `Axes`에 데이터를 그립니다.

`ax.set_xlabel(...)`은 이 좌표 영역의 x축 이름을, `ax.set_title(...)`은 제목을 설정합니다. 한 Figure에 여러 Axes를 두면 같은 화면에서 여러 그래프를 비교할 수 있습니다.

## 질문에 따른 그래프 선택

Matplotlib 공식 문서는 여러 plot type을 제공합니다. 선 그래프(`plot`), 산점도(`scatter`), 막대 그래프(`bar`), 히스토그램(`hist`) 같은 기본 형태가 대표적입니다.

순서에 따른 변화인지, 범주 사이 비교인지에 따라 표현 방법을 고릅니다.

| 먼저 할 질문 | 자주 어울리는 그래프 |
| --- | --- |
| 순서에 따른 변화를 보고 싶은가 | 선 그래프(line plot) |
| 두 값의 관계를 보고 싶은가 | 산점도(scatter plot) |
| 범주별 크기를 비교하고 싶은가 | 막대 그래프(bar chart) |
| 값이 어디에 몰렸는지 보고 싶은가 | 히스토그램(histogram) |

이 표는 규칙이 아니라 출발점입니다. 실제 그래프 선택은 데이터의 모양, 독자의 질문, 전달하려는 메시지에 따라 달라질 수 있습니다.

## 축 범위와 해석

그래프는 많은 숫자를 한 화면에 압축합니다. 같은 데이터라도 축 범위와 표현 방식에 따라 인상이 달라집니다.

예를 들어:

- 축 범위(axis range)를 바꾸면 변화가 커 보이거나 작아 보일 수 있습니다.
- 점이 적은데 선으로 연결하면 실제보다 연속적인 변화처럼 보일 수 있습니다.
- 색상이나 면적을 과하게 쓰면 중요하지 않은 차이가 커 보일 수 있습니다.
- 평균만 그리면 분포나 이상값이 사라질 수 있습니다.

그래프를 볼 때는 항상 다음 질문을 같이 둡니다.

1. x축과 y축은 무엇인가?
2. 한 점 또는 한 선은 무엇을 의미하는가?
3. 빠진 값이나 숨겨진 범위가 있는가?
4. 그래프가 보여 주는 것은 관찰인가, 해석인가?

## 점수 분포

점수 `[45, 62, 71, 73, 82, 88, 90]`을 다섯 구간으로 나누어 개수를 셉니다. 평균만으로 알 수 없는 값의 몰림과 퍼짐을 히스토그램으로 확인합니다.

```python
import matplotlib.pyplot as plt

scores = [45, 62, 71, 73, 82, 88, 90]

fig, ax = plt.subplots()
ax.hist(scores, bins=5)
ax.set_xlabel("score")
ax.set_ylabel("count")
ax.set_title("Score distribution")
plt.show()
```

출력 결과는 점수 값이 어느 구간에 몰려 있는지 보여 줍니다.

![점수 분포를 보여 주는 히스토그램](../../../assets/part-02/chapter-13/pyplot-score-hist-ko.svg)

이 코드는 점수의 평균을 계산하지 않습니다. 대신 점수들이 어디에 몰려 있는지 확인합니다.

## 사례 1. 손실이 튄 구간 찾기

첫 예제의 손실 `[2.40, 1.65, 1.12, 0.86, 0.79]`에서 세 번째 값만 `2.10`으로 바꿔 다시 그려 봅니다. 처음과 마지막 값은 그대로지만, 두 번째에서 세 번째 구간은 0.45만큼 올라가고 다음 구간은 1.24만큼 내려갑니다. 선 그래프에는 세 번째 지점이 봉우리로 나타납니다.

전체 감소량 `2.40 - 0.79 = 1.61`만 기록하면 중간 상승을 놓칩니다. 그래프는 해당 구간을 다시 확인할 이유를 보여 줍니다. 다만 상승 원인이 데이터 배치, 학습 설정, 기록 오류 중 무엇인지는 그래프만으로 결정할 수 없습니다. 해당 반복의 입력과 설정 기록을 함께 확인해야 합니다.

이 그래프가 학습 데이터의 손실이라면 감소 추세만으로 새 데이터에 대한 성능을 판단할 수도 없습니다. 검증 데이터의 손실이나 평가 지표를 별도로 확인해야 합니다.

## 체크리스트

- 그래프는 숫자 표에서 바로 보이지 않는 모양, 변화, 관계, 분포를 드러내는 도구라고 설명할 수 있는가?
- 표는 정확한 값에 강하고, 그래프는 패턴 확인에 강하다는 차이를 말할 수 있는가?
- `Figure`는 그림 전체, `Axes`는 데이터가 그려지는 좌표 영역이라고 구분할 수 있는가?
- 차트 종류를 먼저 외우기보다 데이터에 어떤 질문을 던지는지 먼저 정해야 한다는 점을 설명할 수 있는가?
- 선 그래프, 산점도, 막대 그래프, 히스토그램이 각각 어떤 질문에 자주 쓰이는지 말할 수 있는가?
- 그래프를 볼 때 축, 점의 의미, 숨겨진 범위, 해석 과잉 여부를 함께 점검할 수 있는가?
- 그래프가 판단의 시작점이지 원인이나 결론을 자동으로 증명하지는 않는다는 점을 기억하고 있는가?

## 출처와 참고 자료

- Matplotlib Developers, `Quick start guide`, Matplotlib documentation, 확인 날짜: 2026-07-20. [https://matplotlib.org/stable/users/explain/quick_start.html](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" } `Figure`, `Axes`, `plt.subplots()`를 구분해 설명하는 기준으로 확인했습니다.
- Matplotlib Developers, `Plot types`, Matplotlib documentation, 확인 날짜: 2026-07-20. [https://matplotlib.org/stable/plot_types/index.html](https://matplotlib.org/stable/plot_types/index.html){: target="_blank" rel="noopener noreferrer" } 선 그래프, 산점도, 막대 그래프, 히스토그램을 질문별 기본 차트로 분류하는 부분의 참고 자료입니다.
- Matplotlib Developers, `matplotlib.pyplot`, Matplotlib API reference, 확인 날짜: 2026-07-20. [https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html){: target="_blank" rel="noopener noreferrer" } `pyplot` 기반 예제가 Matplotlib 입문 코드에서 어떻게 쓰이는지 확인하는 참고 자료입니다.

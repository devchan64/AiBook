# P2-15.2 Part 3로 넘어가기 전 점검

> Section ID: `P2-15.2`
> Version: `v2026.09.08`

## 데이터와 계산의 연결

수식은 계산 규칙을, Python은 실행 절차를 표현합니다. NumPy는 배열 계산을, Pandas는 표의 선택과 집계를, Matplotlib은 값의 변화와 분포 확인을 담당합니다. Git에는 코드와 설명을 어떤 이유로 바꾸었는지 기록할 수 있습니다.

```mermaid
--8<-- "assets/part-02/chapter-15/part2-learning-map-flow-ko.mmd"
```

## 사례 1. 학생 네 명의 입력과 정답

시험 전에 학생의 점수를 예측한다고 합시다. 공부 시간·결석 수·연습 퀴즈 수는 예측 시점까지의 기록이며, 시험 점수는 나중에 확인한 정답입니다.

| 학생 | 공부 시간 | 결석 수 | 퀴즈 수 | 시험 점수 |
| --- | ---: | ---: | ---: | ---: |
| A | 2 | 5 | 3 | 50 |
| B | 4 | 3 | 5 | 65 |
| C | 6 | 1 | 7 | 80 |
| D | 8 | 0 | 9 | 90 |

입력 `X`에는 공부 시간·결석 수·퀴즈 수의 세 열을 넣고, 정답 `y`에는 시험 점수를 넣습니다. 학생이 행이고 특징이 열이므로 `X.shape`는 `(4, 3)`, `y.shape`는 `(4,)`입니다. 첫 입력 `[2, 5, 3]`은 정답 50과 짝을 이룹니다.

시험 점수까지 `X`에 넣으면 `(4, 4)`가 되지만 시험 전에 알 수 없는 정답을 제공하는 문제가 생깁니다. 열 수가 맞고 코드가 실행된다는 사실만으로 입력 구성이 올바른 것은 아닙니다.

퀴즈 수를 입력에서 빼면 `X.shape`는 `(4, 2)`가 되고 `y.shape`는 그대로입니다. 학생 D의 기록을 제외한다면 `X`와 `y` 양쪽에서 같은 학생을 제거해야 합니다.

## 학습과 예측 표현

scikit-learn에서는 학습 기능을 가진 객체를 estimator라고 부릅니다. 지도학습 예제의 `fit(X_train, y_train)`은 학습용 입력과 정답으로 모델을 학습시키는 호출입니다. `predict(X_test)`는 학습된 모델에 테스트 입력을 넣어 예측값을 구하는 호출입니다.

| 표현 | 의미 |
| --- | --- |
| sample | 데이터 한 건; 위 표에서는 학생 한 명 |
| feature | 입력 속성; 위 표에서는 공부 시간·결석 수·퀴즈 수 |
| target, `y` | 맞혀야 할 정답; 위 표에서는 시험 점수 |
| train data | 모델을 학습시키는 데이터 |
| test data | 학습과 모델 선택에 사용하지 않고 최종 평가에 남겨 둔 데이터 |
| `fit` | 데이터에서 모델의 규칙을 배우는 동작 |
| `predict` | 학습된 모델로 입력의 예측값을 구하는 동작 |

```mermaid
--8<-- "assets/part-02/chapter-15/ml-reading-flow-ko.mmd"
```

테스트 정답은 `predict`의 입력으로 주지 않습니다. 예측이 끝난 뒤 예측값과 실제 정답을 비교하는 데 사용합니다.

## 사례 2. 오차·손실·평가값 구분

실제 점수가 `[50, 65, 80, 90]`, 예측 점수가 `[55, 60, 80, 85]`라고 합시다. 실제값에서 예측값을 뺀 오차는 `[-5, 5, 0, 5]`입니다. 이 오차의 평균은 1.25지만, 양수와 음수가 상쇄되므로 오차 크기를 그대로 나타내지 않습니다.

제곱 오차는 `[25, 25, 0, 25]`이며 MSE는 `75 / 4 = 18.75`입니다. 절댓값 오차를 평균내는 MAE는 `15 / 4 = 3.75`입니다. 같은 예측 결과도 어떤 계산으로 요약하느냐에 따라 값과 의미가 달라집니다.

손실은 학습 과정에서 줄이려는 값이고, 평가 지표는 결과를 평가하는 기준입니다. MSE처럼 같은 계산이 두 역할에 쓰일 수도 있습니다. 어떤 데이터에서 계산했고 무엇을 결정하는 데 쓰는지 함께 밝혀야 합니다.

예측값을 `[50, 65, 80, 90]`으로 바꾸면 모든 오차와 MSE·MAE가 0이 됩니다. 계산을 점검할 때 사용할 수 있는 작은 확인 사례입니다.

## 변경 조건 기록

입력 특징이나 분할 조건을 바꾸었다면 결과와 함께 기록합니다. `결과 개선`만 적으면 무엇을 비교했는지 알 수 없습니다.

| 기록 항목 | 구체적인 예 |
| --- | --- |
| 입력 변경 | 퀴즈 수 제외, 특징 3개에서 2개로 변경 |
| 유지 조건 | 같은 학습·테스트 학생과 같은 모델 설정 사용 |
| 비교 결과 | 변경 전후 테스트 MSE와 예측값 표 기록 |
| 생성 근거 | 코드·데이터 버전과 실행 명령 기록 |

여러 조건을 한꺼번에 바꾸면 결과 차이가 어느 변경에서 왔는지 구분하기 어렵습니다. 비교 목적에 맞게 변경 조건을 정하고 기록해야 합니다.

## 개념별 참고 위치

| 확인할 내용 | 관련 본문 |
| --- | --- |
| 변수와 함수 | [P2-2.1](../chapter-02/section-01.md) |
| 벡터와 행렬 | [P2-3.1](../chapter-03/section-01.md) |
| 평균과 분산 | [P2-5.2](../chapter-05/section-02.md) |
| 손실 함수 | [P2-6.1](../chapter-06/section-01.md) |
| 경사하강법 | [P2-6.3](../chapter-06/section-03.md) |
| 배열 모양과 축 | [P2-11.2](../chapter-11/section-02.md) |
| 입력·정답·데이터 분할 | [P2-12.3](../chapter-12/section-03.md) |
| 그래프 해석 | [P2-13.1](../chapter-13/section-01.md) |
| MSE 계산 | [P2-15.1](section-01.md) |

## 체크리스트

- 학생 표의 입력 열과 정답 열을 구분할 수 있는가?
- 특징 하나를 빼거나 학생 한 명을 제외할 때 `X`, `y`의 모양이 어떻게 달라지는지 설명할 수 있는가?
- `fit`과 `predict`에 어떤 데이터를 전달하는지 구분할 수 있는가?
- 오차 평균·MSE·MAE를 위 예측값에서 계산할 수 있는가?
- 학습 손실과 테스트 평가값의 역할을 구분할 수 있는가?
- 입력이나 분할을 바꾸었을 때 유지 조건과 결과를 함께 기록할 수 있는가?

## 출처와 참고 자료

- scikit-learn developers, `Getting Started`, scikit-learn documentation, 확인 날짜: 2026-07-20. [https://scikit-learn.org/stable/getting_started.html](https://scikit-learn.org/stable/getting_started.html){: target="_blank" rel="noopener noreferrer" } estimator, `fit`, `predict`, `X`, `y`의 입문 흐름을 확인하는 직접 참고 자료입니다.
- scikit-learn developers, `Glossary of Common Terms and API Elements`, scikit-learn documentation, 확인 날짜: 2026-07-20. [https://scikit-learn.org/stable/glossary.html](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" } sample, feature, target, training/test data 같은 Part 3 진입 용어의 기준입니다.
- NumPy Developers, `NumPy: the absolute basics for beginners`, NumPy documentation, 확인 날짜: 2026-07-20. [https://numpy.org/doc/stable/user/absolute_beginners.html](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" } `shape`, 차원, 배열 모양을 `X`와 `y`의 데이터 구조로 연결하는 부분의 참고 자료입니다.

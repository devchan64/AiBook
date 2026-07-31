# P4-8.3 보충학습: 문제 유형에 따라 baseline을 처음 세우는 법

> Section ID: `P4-8.3`
> Version: `v2026.07.31`

P4-8.2에서 [baseline이 왜 필요한지](../../../reference/concept-glossary-parts/01-giyeok.md#baseline-model) 봤다면, 이제 다음 질문이 바로 나옵니다.

그래서 baseline은 실제로 어떻게 세우는가?

이 보충학습은 그 질문에 답합니다. 목표는 baseline 이름을 많이 외우는 것이 아니라, 문제 유형을 보고 `가장 단순하지만 비교 의미가 있는 기준`을 직접 고를 수 있게 만드는 것입니다.

처음 baseline을 세울 때는 `problem_type`, `simple_rule`, `metric`, `known_easy_case`, `known_hard_case`를 먼저 적습니다. 분류, 회귀, 시계열은 서로 다른 baseline 후보를 갖지만, 공통 목적은 복잡한 모델을 보기 전에 쉬운 기준과 대표 실패 장면을 같은 표에 올리는 것입니다.

## baseline을 세울 때 갈라지는 문제 유형

이 절은 [분류](../../../reference/concept-glossary-parts/06-bieup.md#classification), [회귀](../../../reference/concept-glossary-parts/14-hieut.md#regression), 시계열 문제에서 대표적인 baseline을 처음 세우는 법을 다룹니다.

- baseline을 세우기 전에 무엇을 먼저 고정해야 하는가?
- 문제 유형에 따라 어떤 baseline을 먼저 떠올릴 수 있는가?
- baseline을 세운 뒤 어떤 예시와 예제로 비교를 시작해야 하는가?
- baseline 점수를 본 뒤 다음으로 무엇을 확인해야 하는가?

이 절은 먼저 `문제 유형에 따라 가장 단순하지만 비교 의미가 있는 baseline을 어떻게 세울 것인가`를 닫습니다. 교차검증, 모델 비교 절차, 더 복잡한 튜닝 기법은 P4-9 이후에서 이어집니다.

## 문제 유형별 기준선에서 남길 판단

- 분류, 회귀, 시계열에서 대표적인 baseline 후보를 구분할 수 있습니다.
- baseline 설정 절차를 `문제 유형 고정 -> 가장 단순한 규칙 선택 -> 같은 지표로 측정 -> 오류 확인 -> 다음 비교 결정` 순서로 설명할 수 있습니다.
- baseline 설명 뒤에 사례와 예제가 왜 바로 붙어야 하는지 설명할 수 있습니다.
- baseline 점수를 본 뒤 어떤 다음 질문으로 이어가야 하는지 말할 수 있습니다.

## 먼저 baseline 설정 절차를 잡는다

baseline은 감으로 정하는 임시 규칙이 아니라, `현재 문제에서 가장 단순하지만 비교 의미가 있는 기준`을 고르는 절차로 세우는 편이 안전합니다.

가장 짧은 절차는 아래 순서로 잡을 수 있습니다.

1. 문제 유형을 먼저 고정한다.
2. 특징을 거의 쓰지 않는 가장 단순한 규칙을 고른다.
3. 후보 모델과 같은 지표로 baseline을 측정한다.
4. 점수만 보지 말고 대표 오류 장면도 같이 본다.
5. baseline보다 얼마나 나아졌는지 해석한 뒤에만 튜닝이나 후보 교체로 간다.

이 순서를 표로 다시 묶으면 다음과 같습니다.

| baseline 설계 순서 | 지금 해야 할 질문 | 왜 필요한가 |
| --- | --- | --- |
| 1. 문제 유형 고정 | 분류인가, 회귀인가, 시계열인가 | baseline 형태 자체가 여기서 달라지기 때문입니다. |
| 2. 가장 단순한 규칙 선택 | 다수 클래스인가, 평균/중앙값인가, 직전값인가 | 특징을 거의 안 쓴 최소 기준을 먼저 세워야 하기 때문입니다. |
| 3. 같은 지표로 측정 | accuracy, recall, MAE, MAPE 중 무엇으로 볼 것인가 | 후보 모델과 baseline을 같은 [평가 지표](../../../reference/concept-glossary-parts/05-mieum.md#model-score)로 비교해야 하기 때문입니다. |
| 4. 오류 장면 확인 | 무엇을 특히 놓치고 있거나 크게 틀리고 있는가 | 점수 차이만으로는 개선 방향을 읽기 어렵기 때문입니다. |
| 5. 해석 후 다음 단계 결정 | 튜닝할지, 후보를 바꿀지, 특징을 다시 볼지 | baseline도 못 넘는 후보를 오래 붙잡지 않기 위해서입니다. |

즉, baseline 방법론의 핵심은 `가장 쉬운 규칙을 만든다`가 아니라, `가장 쉬운 규칙을 같은 비교 틀 안에 올린다`에 있습니다.

## 문제 유형별 대표 baseline 지도

대표 baseline은 문제 유형에 따라 출발점이 달라집니다.

| 문제 유형 | 가장 먼저 떠올릴 baseline | 왜 자주 먼저 쓰는가 |
| --- | --- | --- |
| 분류(classification) | 다수 클래스 예측 | 높은 정확도 착시를 가장 빨리 드러낼 수 있기 때문입니다. |
| 분류(classification) | 클래스 비율 기반 dummy 예측 | 단순 분포 추종과 실제 학습을 구분할 수 있기 때문입니다. |
| 회귀(regression) | 평균값 예측 | 입력 특징이 없어도 나오는 기본 오차를 볼 수 있기 때문입니다. |
| 회귀(regression) | 중앙값 예측 | 극단값이 많은 데이터에서 더 안정적인 기준이 될 수 있기 때문입니다. |
| 시계열(time series) | naive 예측 | 직전값을 그대로 쓰는 가장 단순한 시간 순서 기준이기 때문입니다. |
| 시계열(time series) | seasonal naive 예측 | 계절성이 강한 데이터에서 같은 계절의 직전값을 기준으로 둘 수 있기 때문입니다. |

이 표는 baseline의 정답 목록이 아니라, `무엇을 먼저 비교선으로 둘까`를 빠르게 정리하는 지도입니다. 시계열 쪽의 naive, seasonal naive는 Hyndman 등의 공개 교재가 `simple forecasting methods`의 대표 예로 직접 설명하는 방법들입니다.

## 분류에서 baseline을 어떻게 세우는가

분류에서는 다음 같은 baseline을 먼저 생각할 수 있습니다.

| baseline 형태 | 의미 | 먼저 쓰기 좋은 장면 |
| --- | --- | --- |
| 가장 자주 나오는 클래스만 예측 | 다수 클래스 기준 | 클래스 불균형이 큰 문제 |
| 클래스 비율대로 무작위 예측 | 분포 수준 기준 | 분포를 따라간 것과 학습한 것을 구분하고 싶을 때 |
| 항상 같은 클래스 예측 | 정말 최소한의 바닥선 | 지표 해석 자체를 처음 잡을 때 |

고객 이탈 예측에서 이탈이 드문 경우를 생각해 보겠습니다. `항상 비이탈`을 말하는 baseline은 정확도는 높게 나올 수 있습니다. 하지만 이탈 재현율은 0이 될 수 있습니다. 따라서 분류 baseline의 첫 역할은 `점수가 높은가`보다 `무슨 착시가 생기고 있는가`를 먼저 드러내는 일입니다.

## 문제 유형에 따라 baseline을 처음 세우는 법: 확인할 판단 기준

이 사례 절은 다음 질문으로 중심축을 확인한다.

- 오픈체크리스트의 중심축 문장인 "문제 유형별 baseline을 어떻게 처음 세울지 보충해야 합니다."를 본문 사례에서 어느 대목으로 확인할 수 있는가?
- 표, 코드, 도식, 체크리스트 중 어떤 장치가 이 판단을 다시 검토하게 만드는가?

### 사례 1. 고객 이탈 예측에서 다수 클래스 baseline을 먼저 두는 이유

구독 서비스 팀이 다음 달 고객 이탈을 예측하려고 합니다. 데이터에서 비이탈 고객이 90%, 이탈 고객이 10%라고 해 보겠습니다.

이때 baseline으로 `항상 비이탈`을 예측하면 정확도는 90%가 나올 수 있습니다. 하지만 중요한 것은 이탈 고객을 전혀 잡지 못한다는 점입니다. 그래서 baseline 없이 실제 모델의 정확도 91%만 보면 `1%포인트 좋아졌다`라고 말하게 되지만, baseline을 같이 놓으면 `여전히 중요한 고객을 거의 못 잡고 있는가`를 먼저 묻게 됩니다.

| 항목 | 내용 |
| --- | --- |
| 문제 | 다음 달 고객 이탈 여부 예측 |
| 클래스 분포 | 비이탈 90%, 이탈 10% |
| baseline | 항상 `비이탈` 예측 |
| 먼저 볼 지표 | 정확도, [재현율(recall)](../../../reference/concept-glossary-parts/09-jieut.md#recall), F1 |
| 바로 확인할 오류 | 실제 이탈 고객을 놓친 사례 |

```mermaid
--8<-- "assets/part-04/chapter-08/p4-8-3-mermaid-01-ko.mmd"
```

이 사례의 핵심은 baseline이 낮은 모델이어서 중요한 것이 아니라, `정확도 착시를 바로 드러내는 기준`이어서 중요하다는 점입니다.

### 작은 예제. 분류 baseline을 숫자로 읽기

다음처럼 같은 데이터에서 baseline과 실제 모델을 나란히 놓으면 baseline의 역할이 더 분명해집니다.

| 모델 | accuracy | recall | F1 | 읽기 |
| --- | ---: | ---: | ---: | --- |
| baseline: 항상 비이탈 | 0.90 | 0.00 | 0.00 | 정확도는 높아 보여도 중요한 고객을 하나도 못 잡습니다. |
| 후보 모델 | 0.94 | 0.50 | 0.63 | baseline보다 실제 이탈을 더 잡기 시작했는지 읽을 수 있습니다. |

이 표를 읽을 때의 질문은 단순합니다.

- 정확도 차이가 실제로 의미 있는가?
- recall과 F1이 baseline보다 얼마나 달라졌는가?
- 여전히 놓치는 이탈 고객은 어떤 사례인가?

## 회귀에서 baseline을 어떻게 세우는가

회귀에서는 다음 같은 baseline을 먼저 둘 수 있습니다.

| baseline 형태 | 의미 | 먼저 쓰기 좋은 장면 |
| --- | --- | --- |
| 모든 샘플에 평균값 예측 | 가장 기본적인 중심값 기준 | 입력 특징이 정말 도움 되는지 처음 볼 때 |
| 모든 샘플에 중앙값 예측 | 극단값에 덜 민감한 기준 | 이상치가 많을 때 |
| 특정 상수값 예측 | 도메인 고정 기준 | 현업에서 이미 쓰는 기준선이 있을 때 |

회귀 baseline의 핵심은 `입력이 없을 때도 이 정도 오차는 난다`는 출발점을 먼저 만드는 데 있습니다.

### 사례 2. 배송 시간 예측에서 평균 baseline을 먼저 두는 이유

물류 팀이 배송 시간을 예측하려고 합니다. 지역, 거리, 물량, 날씨 정보를 넣은 모델을 만들기 전에 먼저 `평균 배송 시간만 예측하는 baseline`을 둡니다.

이 baseline의 목적은 평균 예측이 훌륭해서가 아닙니다. 입력 특징을 넣은 모델이 평균 기준보다 실제로 얼마나 오차를 줄였는지 확인하기 위해서입니다.

| 항목 | 내용 |
| --- | --- |
| 문제 | 배송 시간 예측 |
| baseline | 모든 주문에 평균 배송 시간 예측 |
| 먼저 볼 지표 | MAE, RMSE |
| 바로 확인할 오류 | 장거리 배송, 악천후 배송 같은 큰 오차 구간 |

예를 들어 평균 baseline의 MAE가 18분이고 후보 모델의 MAE가 15분이라면, 다음 질문은 `3분 감소가 운영상 의미 있는가`입니다. 그 답을 위해서는 전체 평균만 보지 말고 어떤 주문군에서 오차가 실제로 줄었는지 같이 봐야 합니다.

### 작은 예제. 회귀 baseline을 숫자로 읽기

| 모델 | MAE | RMSE | 읽기 |
| --- | ---: | ---: | --- |
| baseline: 평균 배송 시간 | 18.0 | 24.5 | 입력을 보지 않은 출발점입니다. |
| 후보 모델 | 15.0 | 20.8 | baseline보다 오차를 줄였지만, 어떤 주문군에서 줄었는지 더 봐야 합니다. |

이 표를 읽을 때는 다음을 같이 적어 두는 편이 안전합니다.

- 큰 오차가 줄어든 주문군은 무엇인가?
- 평균만 좋아진 것이 아니라 중요한 구간에서도 좋아졌는가?
- baseline보다 낮아진 오차가 운영 비용 절감으로 이어지는가?

## 시계열에서 baseline을 어떻게 세우는가

시계열 문제에서는 시간 순서를 완전히 지우기보다, 시간 구조를 최소한으로 반영한 단순 기준이 더 자연스러운 경우가 많습니다.

| baseline 형태 | 의미 | 먼저 쓰기 좋은 장면 |
| --- | --- | --- |
| naive | 직전값을 다음 값으로 예측 | 변화가 느린 시계열 |
| seasonal naive | 지난 주 같은 요일, 지난 해 같은 달 값을 사용 | 계절성, 주기성이 있는 시계열 |
| mean method | 전체 평균을 다음 값의 기준으로 둠 | 시간 구조가 약한 단순 비교 출발점이 필요할 때 |

### 사례 3. 일일 방문자 수 예측에서 seasonal naive를 먼저 두는 이유

전자상거래 팀이 일일 방문자 수를 예측하려고 합니다. 월요일과 주말 패턴 차이가 크다면, 단순 평균보다 `지난주 같은 요일 값`을 다음 기준으로 두는 편이 더 자연스럽습니다.

| 항목 | 내용 |
| --- | --- |
| 문제 | 내일 방문자 수 예측 |
| baseline 후보 | naive, seasonal naive |
| 먼저 볼 지표 | MAE, MAPE |
| 바로 확인할 오류 | 공휴일, 행사일, 프로모션 기간 |

예를 들어 어제 방문자 수를 그대로 쓰는 naive baseline보다, 지난주 같은 요일 값을 쓰는 seasonal naive가 더 낮은 오차를 낸다면, 그 시계열에서는 `요일 주기`가 최소 기준선에 들어가야 한다는 뜻입니다.

### 작은 예제. 시계열 baseline을 비교해 읽기

| 모델 | MAE | 읽기 |
| --- | ---: | --- |
| naive | 320 | 직전값만 따라간 기준입니다. |
| seasonal naive | 180 | 요일 패턴을 반영한 최소 기준이 더 낫습니다. |
| 후보 모델 | 150 | 계절성 기준보다 추가 개선이 있는지 읽을 수 있습니다. |

이 장면에서는 baseline 자체가 하나가 아닐 수 있습니다. 시계열에서는 `직전값 기준`과 `주기 기준` 중 무엇이 더 적절한 바닥선인지 먼저 비교한 뒤, 그 위에서 복잡한 모델을 보는 편이 자연스럽습니다.

## 연습 및 예제

### Python 예제로 분류 baseline과 후보 모델을 비교해 보기

아래 예제는 scikit-learn의 `DummyClassifier`와 간단한 분류 모델을 비교하는 아주 작은 실습입니다.

문제 상황:

- 새 모델이 정말 도움이 되는지 보려면 최소 기준선과 나란히 놓고 비교해야 한다

입력(input):

- `make_classification`으로 만든 불균형 분류 데이터
- `DummyClassifier`
- `LogisticRegression`

기대 출력(output):

- baseline과 실제 모델의 accuracy, recall, F1

확인할 개념:

- baseline은 복잡한 모델이 최소한 넘어야 할 비교 기준이다
- 불균형 데이터에서는 accuracy만이 아니라 recall과 F1도 함께 봐야 한다

조작해 볼 값:

- `weights=[0.9, 0.1]`에서 양성 클래스 비율을 `0.2`나 `0.05`로 바꾸면 baseline accuracy와 recall, F1 해석이 달라집니다.
- `DummyClassifier(strategy="most_frequent")`를 `DummyClassifier(strategy="stratified")`로 바꾸면 다수 클래스만 예측하는 기준과 클래스 분포를 따라 무작위 예측하는 기준의 차이를 볼 수 있습니다.

```python
# 문제 유형별 baseline과 후보 모델 성능을 비교해 기준선을 세우는 예제입니다.
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

X, y = make_classification(
    n_samples=400,
    n_features=6,
    n_informative=3,
    n_redundant=0,
    weights=[0.9, 0.1],
    random_state=42,
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)
baseline_pred = baseline.predict(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
model_pred = model.predict(X_test)

print("baseline accuracy :", round(accuracy_score(y_test, baseline_pred), 3))
print("baseline recall   :", round(recall_score(y_test, baseline_pred), 3))
print("baseline f1       :", round(f1_score(y_test, baseline_pred), 3))
print()
print("model accuracy    :", round(accuracy_score(y_test, model_pred), 3))
print("model recall      :", round(recall_score(y_test, model_pred), 3))
print("model f1          :", round(f1_score(y_test, model_pred), 3))
```

실행 결과 예시는 다음과 같습니다.

```text
baseline accuracy : 0.9
baseline recall   : 0.0
baseline f1       : 0.0

model accuracy    : 0.942
model recall      : 0.5
model f1          : 0.632
```

이 예제에서 꼭 읽어야 할 것은 숫자 하나가 아닙니다.

- accuracy는 baseline도 이미 높을 수 있습니다.
- recall과 F1은 중요한 소수 class를 실제로 잡는지 더 잘 보여 줄 수 있습니다.
- 따라서 baseline 비교는 `어느 지표에서 개선되었는가`와 `어떤 오류가 남았는가`를 같이 보게 만듭니다.

### Python 예제로 회귀 baseline을 실제로 비교해 보기

아래 예제는 아주 작은 목표값 배열을 가지고 평균 baseline과 중앙값 baseline을 실제로 비교해 보는 예제입니다.

문제 상황:

- 배송 시간 예측 문제에서 평균 baseline과 중앙값 baseline 중 무엇이 더 자연스러운 출발점인지 보고 싶다

입력(input):

- 간단한 학습용 목표값과 평가용 목표값
- 평균 baseline, 중앙값 baseline

기대 출력(output):

- 평균 baseline과 중앙값 baseline의 예측값과 MAE

확인할 개념:

- baseline도 실제 데이터 장면에 따라 더 자연스러운 출발점이 달라질 수 있다

조작해 볼 값:

- `y_train`의 큰 값 `120`을 `60`이나 `200`으로 바꾸면 평균 baseline은 크게 움직이고 중앙값 baseline은 덜 움직입니다.
- `y_test`에 큰 지연값을 하나 더 추가하면 어떤 baseline의 MAE가 더 안정적인지 다시 비교할 수 있습니다.

```python
# 문제 유형별 baseline과 후보 모델 성능을 비교해 기준선을 세우는 예제입니다.
y_train = [32, 35, 31, 120, 33]
y_test = [34, 36, 30, 90]

mean_value = sum(y_train) / len(y_train)
median_value = sorted(y_train)[len(y_train) // 2]

mean_pred = [mean_value] * len(y_test)
median_pred = [median_value] * len(y_test)

def mae(y_true, y_pred):
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)

print("mean baseline")
print("  prediction :", [round(v, 1) for v in mean_pred])
print("  MAE        :", round(mae(y_test, mean_pred), 2))
print()
print("median baseline")
print("  prediction :", [round(v, 1) for v in median_pred])
print("  MAE        :", round(mae(y_test, median_pred), 2))
```

실행 결과 예시는 다음과 같습니다.

```text
mean baseline
  prediction : [50.2, 50.2, 50.2, 50.2]
  MAE        : 22.6

median baseline
  prediction : [33, 33, 33, 33]
  MAE        : 16.0
```

이 예제는 왜 평균 baseline과 중앙값 baseline을 둘 다 떠올려야 하는지 보여 줍니다. 학습용 목표값에 큰 값 `120`이 하나 들어 있으면 평균은 크게 끌려가지만, 중앙값은 더 안정적으로 남습니다. 즉, 이런 장면에서는 `평균이 기본 기준선인가`, `중앙값이 더 자연스러운 기준선인가`를 실제 숫자로 먼저 확인하는 편이 안전합니다.

## 체크리스트

- 지금 문제 유형에 맞는 대표 baseline 후보를 최소 하나 이상 적어 두었는가?
- baseline과 후보 모델을 같은 지표로 비교하고 있는가?
- 점수 차이만이 아니라 대표 오류 장면도 함께 보고 있는가?
- baseline을 넘지 못한 후보를 튜닝으로 오래 끌고 가지 않고 있는가?
- baseline이 `먼저 지는 모델`이 아니라 `먼저 비교해야 할 기준`이라는 점을 설명할 수 있는가
- 대표 baseline 방법은 문제 유형에 따라 다르게 잡아야 한다는 점을 설명할 수 있는가
- baseline보다 나은 후보가 생겼는지 확인한 뒤에야 튜닝으로 가는 편이 안전하다는 점을 설명할 수 있는가

## 출처와 참고 자료

- scikit-learn developers, [`DummyClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, 확인 날짜: 2026-07-26.
- scikit-learn developers, [`DummyRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, 확인 날짜: 2026-07-26.
- scikit-learn developers, [`Cross-validation: evaluating estimator performance`](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn User Guide, 확인 날짜: 2026-07-26.
- Rob J Hyndman, George Athanasopoulos, [`Forecasting: Principles and Practice (3rd ed), 5.2 Some simple forecasting methods`](https://otexts.com/fpp3/simple-methods.html){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-26.
- Trevor Hastie, Robert Tibshirani, Jerome Friedman, [*The Elements of Statistical Learning*](https://hastie.su.domains/ElemStatLearn/){: target="_blank" rel="noopener noreferrer" }, 확인 날짜: 2026-07-26.
- Sebastian Raschka, [`Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning`](https://arxiv.org/abs/1811.12808){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, 확인 날짜: 2026-07-26.

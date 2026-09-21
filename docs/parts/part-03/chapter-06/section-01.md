# P3-6.1 비교할 구조는 어떤 특징으로 남기는가

> Section ID: `P3-6.1`
> Version: `v2026.09.19`

특징을 처음 배울 때는 `열이 많을수록 좋은 것 아닐까`라고 받아들이곤 합니다. 하지만 [특징(feature)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature)은 단순히 많은 값을 넣는 일이 아닙니다. 특징은 샘플이 가진 구조를 비교와 예측에 쓸 수 있도록 다시 표현한 값입니다. 그래서 좋은 특징은 많기보다, `무엇을 보여 주려는가`가 분명해야 합니다. 앞 절에서 원시 로그를 [요약 표(summary table)](../../../reference/concept-glossary-parts/03-digeut.md#data-modeling)로 바꿨다면, 이제 그 요약 표 안에 어떤 구조를 남길지 정해야 합니다.

특징을 설계한다는 말은 요약 표 안의 숫자를 그대로 쓰는 일이 아니라, 비교하고 싶은 구조를 숫자 표현으로 다시 고르는 일입니다. 그래서 먼저 어떤 구조를 남길지 정한 뒤에야 평균, 기울기, 변동성 같은 특징 후보가 의미를 가집니다. 여기서 한 번 더 갈라지는 판단이 있습니다. 같은 구조를 평균, 차이, 기울기, 토큰, 비율처럼 다른 표현으로 바꾸는 일은 [변수변환(variable transformation)](../../../reference/concept-glossary-parts/13-pieup.md#glossary-variable-transformation)이고, 그렇게 바꾼 표현 중 실제로 남길 항목을 고르는 일은 [특징 선택(feature selection)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature-selection)입니다.


원시 측정값 자체도 특징으로 사용할 수 있습니다. 여기서는 요약값에서 비교할 정보를 골라 표현하는 경우를 다룹니다.

## 평균 세 개에서 계산한 특징의 대상과 단위

다음은 자체 가상 동작 A·B의 구간 평균이며 단위는 L/min입니다. **계산 대상은 원시 측정 전체가 아니라 초반·중반·후반 평균 세 개**입니다. 구간마다 관측 수나 길이가 다르면 이 세 평균의 단순 평균은 전체 관측 평균이나 시간 평균과 다를 수 있습니다.

| 동작 | 초반 평균 | 중반 평균 | 후반 평균 |
| --- | ---: | ---: | ---: |
| A | 1.8 | 2.2 | 2.6 |
| B | 2.1 | 2.2 | 2.3 |

초반·중반·후반에 인덱스 0·1·2를 붙이겠습니다. 초반에서 후반까지의 인덱스 간격은 `2−0=2`입니다. 따라서 A의 차이 `2.6−1.8=0.8 L/min`을 2로 나눈 기울기는 **0.4 L/min/인덱스 간격**이며 초당 변화량이 아닙니다. 실제 대표 시각의 간격이 20초라면 시간 기울기는 `0.8/20=0.04 L/min/s`입니다. 시각 정보 없이 20초를 가정할 수는 없습니다.

| 동작 | 세 구간 평균의 평균: L/min | 후반−초반: L/min | 인덱스당 기울기 | 세 구간 평균의 표준편차: L/min |
| --- | ---: | ---: | ---: | ---: |
| A | 2.2 | 0.8 | 0.4 | 0.4 |
| B | 2.2 | 0.2 | 0.1 | 0.1 |

표준편차는 평균에서 각 값이 얼마나 떨어져 있는지 요약한 수입니다. 여기서는 표본 표준편차, 즉 세 값의 제곱 편차 합을 `3−1=2`로 나누고 제곱근을 취하는 규칙을 씁니다. A는 평균 2.2에서의 차이가 −0.4·0·0.4이므로 `sqrt((0.16+0+0.16)/2)=0.4`입니다. B도 같은 방식으로 0.1입니다. 이 계산 규칙을 썼다는 사실이 세 평균의 통계적 독립성을 보증하지는 않습니다.

## 구간 평균의 퍼짐과 구간 안 흔들림은 다르다

매 구간에서 X는 `[2, 2]`, Y는 `[0, 4]`를 측정했다고 해 보겠습니다. 두 동작 모두 구간 평균은 `[2, 2, 2]`이고 **그 세 평균의 표준편차는 0**입니다. 하지만 각 구간 안의 최댓값−최솟값은 X가 0, Y가 4입니다. 구간 평균만 남기면 이 차이를 복원할 수 없습니다.

따라서 위 표에서 A의 표준편차가 더 크다는 것은 구간 평균끼리 더 벌어졌다는 뜻입니다. A가 센서 잡음이 크거나 운영상 불안정하다고 판정한 것이 아닙니다. 초반과 후반을 뒤집어도 표준편차는 같으므로, 상승·하강 방향은 부호가 있는 차이를 함께 읽어야 합니다.

질문이 “세 구간의 수준이 비슷한가”라면 평균을, “초반에서 후반으로 얼마나 변했는가”라면 후반−초반을 골라 보세요. 두 질문의 답은 각각 A/B 모두 2.2, A=0.8·B=0.2입니다. 인덱스 간격을 항상 2로 고정하면 기울기는 차이의 절반이므로 두 열을 함께 넣어도 독립적인 새 정보를 더하지 않습니다. 구간 안 흔들림이 질문이면 원시 값이나 구간 내 퍼짐을 추가 확보해야 합니다.

## 특징 묶음을 바꾸는 작은 예측 실험

동작 A~H의 구간 평균으로 같은 결정트리에 서로 다른 특징 묶음을 입력합니다. 아래 `overall_mean`은 세 구간 평균의 단순 평균이고, `segment_variability`는 앞에서 계산한 표본 표준편차입니다. pandas와 scikit-learn이 설치된 Python 환경에서 실행합니다.

이것은 입력 정보 손실을 보여 주도록 만든 8건의 가상 실험입니다. `review_needed`는 예제에 부여한 값이며 실제 점검 기준의 검증 자료가 아닙니다. 학습 A~F 6건은 모두 세 구간 평균의 평균이 2.2여서 평균 하나로는 서로 다른 라벨을 구분하기 어렵습니다. 테스트는 G·H 단 두 건이므로 정확도 0.5와 1.0은 각각 1/2와 2/2를 맞혔다는 뜻입니다. 특징을 늘리면 일반적으로 성능이 좋아진다는 근거로 읽지 않습니다.

입력 묶음을 `overall_mean`과 `late_minus_early` 두 열로 바꾸어 실행해 보세요. 이 설정에서도 테스트 두 건을 모두 맞히지만, 더 많은 자료에 대한 성능은 별도 확인이 필요합니다. 구간 내 흔들림을 구분하려면 이 예제의 어떤 특징을 추가하더라도 원시 정보가 필요하다는 점도 같습니다.

```python
# 평균만 남긴 모델과 변화·변동성 특징까지 남긴 모델의 예측 차이를 비교합니다.
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

events = pd.DataFrame(
    [
        {"event_id": "A", "early": 1.8, "mid": 2.2, "late": 2.6, "review_needed": 1},
        {"event_id": "B", "early": 2.1, "mid": 2.2, "late": 2.3, "review_needed": 0},
        {"event_id": "C", "early": 2.5, "mid": 2.2, "late": 1.9, "review_needed": 1},
        {"event_id": "D", "early": 2.0, "mid": 2.2, "late": 2.4, "review_needed": 0},
        {"event_id": "E", "early": 1.7, "mid": 2.2, "late": 2.7, "review_needed": 1},
        {"event_id": "F", "early": 2.2, "mid": 2.2, "late": 2.2, "review_needed": 0},
        {"event_id": "G", "early": 2.6, "mid": 2.2, "late": 1.8, "review_needed": 1},
        {"event_id": "H", "early": 2.0, "mid": 2.1, "late": 2.3, "review_needed": 0},
    ]
)

segment_values = events[["early", "mid", "late"]]
events["overall_mean"] = segment_values.mean(axis=1)
events["late_minus_early"] = events["late"] - events["early"]
events["segment_variability"] = segment_values.std(axis=1)

train = events[events["event_id"].isin(["A", "B", "C", "D", "E", "F"])]
test = events[events["event_id"].isin(["G", "H"])]
feature_sets = {
    "mean_only": ["overall_mean"],
    "structure_features": ["overall_mean", "late_minus_early", "segment_variability"],
}

for name, columns in feature_sets.items():
    model = DecisionTreeClassifier(random_state=0, max_depth=2)
    model.fit(train[columns], train["review_needed"])
    predicted = model.predict(test[columns])
    comparison = [
        (event_id, int(prediction), int(actual))
        for event_id, prediction, actual in zip(test["event_id"], predicted, test["review_needed"])
    ]
    print(name, "accuracy:", accuracy_score(test["review_needed"], predicted))
    print(name, "predictions:", comparison)
```

```text
mean_only accuracy: 0.5
mean_only predictions: [('G', 0, 1), ('H', 0, 0)]
structure_features accuracy: 1.0
structure_features predictions: [('G', 1, 1), ('H', 0, 0)]
```

## 비교 질문에 맞는 특징 남기기 {#_1}

```mermaid
--8<-- "assets/part-03/chapter-06/p3-6-1-mermaid-01-ko.mmd"
```

## 체크리스트

- 기울기의 분모 2와 실제 시간 간격을 구분하는가?
- 표준편차를 계산한 세 값과 그 단위를 적을 수 있는가?
- 평균 [2, 2, 2]에서 구간 내 변동을 복원할 수 없는 이유를 설명하는가?
- 두 테스트 사건의 정확도를 일반 성능으로 확대하지 않는가?

## 출처와 참고 자료

- Google for Developers, `Machine Learning Glossary`의 `feature`. feature를 input variable used to make predictions라고 설명하므로, 어떤 구조를 보여 줄지를 먼저 정한 뒤 그 구조를 입력 변수로 옮겨야 한다는 근거가 됩니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-19
- Google for Developers, `Machine Learning Glossary`의 `feature engineering`. feature engineering을 model training에 helpful한 transformation을 결정하는 과정으로 설명하므로, 특징 설계는 원시 값을 그대로 두는 일이 아니라 구조를 비교 가능한 숫자 표현으로 바꾸는 일이라는 점을 보강합니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-19
- NIST/SEMATECH e-Handbook of Statistical Methods, `Measures of Location`. 평균, 중앙값, 최빈값을 대표적인 위치 척도로 설명하고, 치우친 분포나 꼬리가 두꺼운 분포에서는 평균과 중앙값이 서로 다른 정보를 줄 수 있음을 보이므로, 전체 수준을 하나의 숫자로 남길 때도 어떤 구조를 보려는지 먼저 정해야 한다는 설명을 보강합니다. [https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm](https://www.itl.nist.gov/div898/handbook/eda/section3/eda351.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-19
- NIST/SEMATECH e-Handbook of Statistical Methods, `Measures of Scale`. 변동성(variability)이나 퍼짐(spread)을 설명하는 여러 수치 척도가 있고, 어떤 척도를 고를지는 중심 주변의 퍼짐과 꼬리의 퍼짐 중 무엇을 강조할지에 따라 달라진다고 정리하므로, 안정성 특징을 평균과 별도 구조로 남겨야 한다는 이 절의 설명을 뒷받침합니다. [https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm](https://www.itl.nist.gov/div898/handbook/eda/section3/eda356.htm){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-19

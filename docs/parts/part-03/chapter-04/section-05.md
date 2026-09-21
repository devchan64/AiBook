# P3-4.5 지금 모은 샘플은 전체 운영 상황을 얼마나 대표하는가

> Section ID: `P3-4.5`
> Version: `v2026.09.19`

샘플을 동작 1회로 정확히 세었더라도, 그 묶음이 적용 대상 운영을 충분히 담았는지는 별도 질문입니다. **대표성은 조건별 건수가 같은지보다, 사용할 환경의 분포와 수집 과정이 자료에 어떻게 반영되었는지를 묻는 문제**입니다. 전체 건수, 조건별 최소 건수, 모델 정확도는 각각 다른 정보를 줍니다.

## 운영 비중과 수집 비중을 나란히 읽기 {#_4}

[가상 동작 샘플 CSV](../../../assets/part-03/chapter-04/p3_4_5_sample_coverage.csv)는 E01~E36의 36개 동작을 담습니다. 한 행이 동작 1회이며, `shift`는 주·야간, `load_mode`는 부하 모드, `machine_id`는 장비, `maintenance_phase`는 안정 운영·정비 직후 조건입니다. 실제 운영 통계가 아니라 수집 범위와 평가를 살피는 자체 사례입니다.

적용 대상 운영이 주간 80%, 야간 20%라고 **가정**해 보겠습니다. 이 비율은 CSV에서 알아낸 값이 아니라 비교를 위해 별도로 정한 목표 운영 분포입니다.

| shift | 가정한 운영 비중 | 수집 동작 수 | 수집 비중 |
| --- | ---: | ---: | ---: |
| day | 80% | 26 | 26/36 ≈ 72.2% |
| night | 20% | 10 | 10/36 ≈ 27.8% |

주간 건수가 더 많다는 사실만으로 편향이라고 판정할 수는 없습니다. 이 가정에서는 오히려 야간 비중이 목표 운영보다 약 7.8%포인트 높습니다. 그러나 작은 표의 비율 차이만으로 대표성 합격·불합격을 정하지도 않습니다. 어떻게 뽑았는지, 어떤 기간·장비·조건을 빠뜨렸는지 함께 확인해야 합니다.

야간 성능을 따로 확인하려면 야간 자료를 더 모을 수도 있습니다. 이때 조건별 평가에는 도움이 될 수 있지만, 바뀐 수집 비율을 그대로 전체 운영 비율이라고 보고하면 안 됩니다. CSV에는 수집 시각이 없으므로 계절이나 기간에 대한 대표성은 현재 열만으로 확인할 수 없습니다.

## 최소 9건이라는 규칙이 실제로 세는 것

`minimum_count = 9`를 설명용 관찰 기준으로 두고, **건수가 9보다 적은 조건**을 표시해 보겠습니다. 이 값은 표준적인 충분 표본 수가 아니며 대표성을 인증하는 임계값도 아닙니다.

| 집계 열 | 조건별 동작 수 | 등장한 조건 종류 수 | 9건 미만인 조건 |
| --- | --- | ---: | --- |
| shift | day 26, night 10 | 2 | 없음: 0개 |
| load_mode | normal 25, high 6, low 5 | 3 | high, low: 2개 |
| machine_id | M1 22, M2 7, M3 7 | 3 | M2, M3: 2개 |
| maintenance_phase | stable 28, after-maintenance 8 | 2 | after-maintenance: 1개 |

`shift`의 부족 조건 수가 0인 이유는 `26 < 9`와 `10 < 9`가 모두 거짓이기 때문입니다. “두 조건이 기준을 넘었다”와 “목표 운영을 대표한다”는 같은 결론이 아닙니다. 이 표의 2·3 같은 조건 종류 수도 동작 수나 모델이 맞힌 수가 아닙니다.

기준을 10으로 올려도 야간 10건은 부족 조건이 아닙니다. 11로 올리면 야간이 포함됩니다. 반대로 기준을 5로 낮추면 위 네 열 모두 부족 조건이 0개가 됩니다. 이 조작은 표시 규칙을 바꿀 뿐 새 자료를 추가하지 않습니다.

## 0건과 조건 조합은 별도로 찾아야 한다

위 표는 CSV에 등장한 값만 셉니다. 적용 대상에 M4도 있다고 별도로 정했다면, M4는 **0건**으로 추가해야 합니다. M4가 실제 대상인지 확인하지 않고 임의로 부족 장비를 만들지는 않습니다. 대상 조건 목록과 수집 값 목록을 대조하는 이유입니다.

개별 조건이 모두 있어도 조합은 비어 있을 수 있습니다. 다음은 같은 CSV에서 `night`인 동작만 골라 장비와 부하를 함께 센 표입니다.

| 야간 동작 | normal | high | low |
| --- | ---: | ---: | ---: |
| M1 | 3 | 1 | 0 |
| M2 | 1 | 0 | 1 |
| M3 | 2 | 1 | 1 |

전체 자료에는 야간 10건, M2 7건, 고부하 6건이 있지만 **야간·M2·고부하 조합은 0건**입니다. 운영에서 이 조합이 발생할 수 있고 평가 대상이라면 공백으로 남깁니다. 원래 불가능한 조합이라면 추가 수집 대상이 아닙니다. 모든 조합을 무조건 같은 건수로 채우는 것이 목표는 아닙니다.

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-5-mermaid-01-ko.mmd"
```

## 모델 점수도 조건별 분모와 함께 읽는다 {#_6}

같은 CSV로 모델을 실행하되, `needs_review`를 **`high` 부하 또는 `after-maintenance`이면 1, 그 외에는 0**인 가상 규칙으로 만듭니다. 입력 조건에서 만든 연습 라벨이므로 실제 고장 예측 능력을 측정하지 않습니다. 알려진 규칙을 모델이 학습 자료에서 얼마나 재현하는지 보는 실험입니다.

E01~E24를 학습, E25~E36을 평가로 고정합니다. ID 구간으로 나눈 사례이며 실제 시간 순서라고 가정하지 않습니다. 부하별 건수는 다음과 같습니다.

| load_mode | 학습 동작 수 | 평가 동작 수 |
| --- | ---: | ---: |
| high | 4 | 2 |
| low | 0 | 5 |
| normal | 20 | 5 |
| 합계 | 24 | 12 |

`dummy`는 학습에서 더 흔한 라벨 0을 항상 내는 비교 기준입니다. `tree`는 입력 조건에 따라 가지를 나누어 예측하는 결정트리입니다. `OneHotEncoder`는 범주를 0/1 열로 바꾸고, 학습에서 못 본 범주는 해당 특징의 열을 모두 0으로 표시합니다. 실행이 가능해졌다고 그 조건을 배운 것은 아닙니다.

아래 코드는 저장소 루트에서 실행합니다. `features`로 입력 열을 바꾸고, 전체 맞힌 수와 부하별 `test_events`·`errors`를 함께 봅니다. 범주 변환과 모델 학습은 학습 묶음으로만 수행합니다.

```python
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

samples = pd.read_csv("docs/assets/part-03/chapter-04/p3_4_5_sample_coverage.csv")
samples["needs_review"] = (
    samples["load_mode"].eq("high")
    | samples["maintenance_phase"].eq("after-maintenance")
).astype(int)
train = samples[samples["event_id"].between("E01", "E24")]
test = samples[samples["event_id"].between("E25", "E36")]
# 입력 열을 바꾸고 평가 건수와 오류 수를 함께 확인합니다.
features = ["shift", "load_mode", "machine_id", "maintenance_phase"]
models = {
    "dummy": DummyClassifier(strategy="most_frequent"),
    "tree": DecisionTreeClassifier(random_state=0, max_depth=3),
}
results = {}
for name, estimator in models.items():
    model = make_pipeline(OneHotEncoder(handle_unknown="ignore"), estimator)
    model.fit(train[features], train["needs_review"])
    result = test[["event_id", "load_mode", "needs_review"]].copy()
    result["prediction"] = model.predict(test[features])
    result["error"] = result["prediction"].ne(result["needs_review"])
    correct = int((~result["error"]).sum())
    print(f"{name}: correct={correct}/{len(result)}, accuracy={correct / len(result):.3f}")
    print(result.groupby("load_mode").agg(
        test_events=("error", "size"), errors=("error", "sum")
    ).to_string())
    results[name] = result
```

```text
dummy: correct=5/12, accuracy=0.417
           test_events  errors
load_mode
high                 2       2
low                  5       2
normal               5       3
tree: correct=9/12, accuracy=0.750
           test_events  errors
load_mode
high                 2       0
low                  5       3
normal               5       0
```

기준선은 12동작 중 5건을 맞혀 `5/12 ≈ 41.7%`, 결정트리는 9건을 맞혀 `9/12 = 75%`입니다. 후자의 오류 세 건은 모두 `low`에 있으므로 저부하 정확도는 `(5−3)/5 = 2/5 = 40%`입니다. 고부하는 2/2, 보통 부하는 5/5이지만 작은 평가 묶음에서의 결과이며 미래 성능을 보장하지 않습니다.

이 실행에서 저부하 오류는 E27·E28·E29입니다. 세 동작은 `stable`이므로 가상 정답은 0인데 모델은 1을 냅니다. 학습에 `low`가 없었다는 점을 확인하되, “못 본 조건은 반드시 틀린다”거나 “미관측 조건만이 오류 원인이다”라고 일반화하지 않습니다. 입력 표현과 학습된 분기에도 결과가 달려 있습니다.

`features = ["load_mode"]`로 바꾸어 정비 정보를 뺀 경우를 실행해 보세요. 결정트리는 `6/12 = 50%`가 되고 부하별 오류는 high 0/2, low 3/5, normal 3/5입니다. 정비 직후인 보통 부하 E25·E26·E34의 라벨을 구별할 입력이 없어집니다. 수집 범위와 입력 정보가 함께 결과를 좌우한다는 뜻입니다. 이 연습의 평가 점수를 보며 입력을 고른 뒤, 같은 묶음을 최종 성능 검증에 다시 사용하는 것은 피해야 합니다.

## 적용 범위와 남은 공백을 문장으로 남기기

“최소 건수 기준을 통과했고 정확도가 75%이므로 전체 운영에 충분하다”를 고쳐 보세요. 답은 “주·야간은 설명용 9건 기준을 넘었지만 목표 운영 비중·수집 경로와 추가 조건을 확인해야 한다. 이 가상 규칙 실험은 12동작 중 9건을 맞혔고, 학습에 없던 저부하는 5건 중 2건을 맞혔다. 야간·M2·고부하와 수집 기간에 대한 근거는 남아 있지 않다”입니다.

실제 자료에는 수집 기간과 방법, 대상 조건 목록, 0건·소수인 중요 조합, 추가 수집할 대상이나 적용을 보류할 범위를 남깁니다. 총건수나 정확도 한 값으로 이 기록을 대신하지 않습니다.

## 체크리스트

- 목표 운영 80/20과 수집 비중 26/36·10/36을 서로 다른 근거로 구분하는가?
- 9건 기준에서 shift의 부족 조건 수가 0인 이유를 계산했는가?
- 기준을 낮춰 경고가 사라져도 자료가 늘지 않았음을 설명할 수 있는가?
- 대상 목록의 0건 조건과 야간·M2·고부하 같은 교차 공백을 확인했는가?
- 전체 9/12와 저부하 2/5를 함께 읽고 가상 라벨의 한계를 밝혔는가?
- 관측 기간 등 현재 CSV로 확인할 수 없는 범위를 남겼는가?

## 출처와 참고 자료

- Google for Developers, [Deep Learning Tuning Playbook: Additional guidance](https://developers.google.com/machine-learning/guides/deep-learning-tuning-playbook/additional-guidance){: target="_blank" rel="noopener noreferrer" }. 실제 운영을 대표하는 자료에서 평가 지표를 확인해야 한다는 일반 근거입니다. 80/20 비율과 최소 9건은 이 절의 가상 설정입니다. / 확인일: 2026-09-19
- scikit-learn developers, [OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html){: target="_blank" rel="noopener noreferrer" }. 범주 변환과 `handle_unknown="ignore"`의 미관측 범주 처리 근거입니다. / 확인일: 2026-09-19

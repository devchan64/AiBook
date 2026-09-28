# P3-4.2 샘플 단위가 흔들리면 무엇이 함께 흔들리는가

> Section ID: `P3-4.2`
> Version: `v2026.09.19`

[샘플(sample)](../../../reference/concept-glossary-parts/07-siot.md#glossary-sample)을 동작 1회로 정했다면, 시점별 기록·특징·결과가 어느 동작을 가리키는지 맞춰야 합니다. 그러나 **사건별로 학습·평가를 나누는 것**과 **사건당 한 번 평가하는 것**은 별개의 결정입니다. 이 절에서는 새 동작의 검토 결과를 예측하려는 가상 실험으로 그 차이를 확인합니다.

## 관측 행·분석 대상·분할 그룹·채점 단위

| 구분 | 이 실험에서 뜻하는 것 |
| --- | --- |
| 관측 행 | 한 동작 안의 한 시점에서 기록한 유량 |
| 분석 대상 | 검토 결과가 붙는 동작 1회 |
| 모델 입력 한 건 | 한 시점의 `flow` 값 |
| 분할 그룹 | 함께 학습 또는 평가 쪽에 두려는 `event_id` |
| 채점 단위 | 예측을 실제 결과와 대조하는 시점 행 1개 |

모델은 시점마다 예측하지만 목표값 `review_needed`는 동작에 붙은 0 또는 1을 각 행에 반복한 것입니다. 이는 모델 입력과 목표의 구성을 살펴보기 위한 실험이며, 실제 고장 판정 자료가 아닙니다. 같은 동작의 18행에 1을 붙여도 검토 대상 동작은 18건이 아니라 1건입니다.

특징의 계산 범위도 적어야 합니다. 아래 CSV의 A는 16초 유량이 10.2, 17초 유량이 9.9입니다. `late_drop = 앞값−뒷값 = 0.3 L/min`은 이 구간의 하강량입니다. 반면 시간당 기울기는 `(9.9−10.2)/(17−16) = −0.3 L/min/s`입니다. 부호와 단위가 다르며, 둘 다 한 시점 값만으로 계산할 수 없습니다. 시점 입력에 구간 특징을 덧붙이는 것도 가능하지만 어떤 관측 구간으로 계산했는지 밝혀야 합니다.

## 정확도의 분모부터 읽기

이 실험의 **정확도(accuracy)는 맞힌 평가 행 수 ÷ 전체 평가 행 수**입니다. 예를 들어 12개 평가 행 중 6개를 맞히면 `6/12 = 0.5`, 즉 50%입니다. 사건 하나가 여러 행을 가지면 이 계산에서 여러 번 채점됩니다.

| 분할 방식 | 학습에 넣는 기록 | 평가에 넣는 기록 | 같은 사건이 양쪽에 있는가 |
| --- | --- | --- | --- |
| 행 분할 | A~H 각 사건의 0~11초 | A~H 각 사건의 12~17초 | 있음: A~H |
| 사건 분할 | A~D의 모든 시점 | E~H의 모든 시점 | 없음 |

첫 분할은 이미 본 사건의 다른 시점에 대한 평가이고, 두 번째는 학습에서 보지 못한 사건의 행에 대한 평가입니다. 어느 쪽도 자동으로 사건당 한 번씩 채점하지 않습니다. 새 사건에 대한 성능이 질문이라면 첫 분할의 높은 점수만으로 답할 수 없습니다.

## 분할을 바꾸며 모델 출력 확인하기

입력은 [가상 로그 CSV](../../../assets/part-03/chapter-04/p3_4_2_split_log.csv)입니다. A~H의 8개 사건마다 18개 시점이 있어 총 144행입니다. 유량은 L/min으로 읽습니다. 사건별 중심값 10·30·…·150에 `0.0, +0.2, −0.1`의 작은 변화를 반복했습니다. 같은 사건의 값은 서로 매우 비슷하며, 반복 관측이 독립된 새 사건을 늘리지는 않습니다. [생성 코드](../../../assets/part-03/chapter-04/p3_4_2_make_split_log.py)로 같은 파일을 재현할 수 있습니다.

결정트리 `DecisionTreeClassifier`는 입력값을 기준으로 나누어 0/1을 예측하는 모델입니다. 여기서는 성능을 높이는 방법보다, 같은 모델을 두 분할에서 실행했을 때 평가 대상이 어떻게 달라지는지 봅니다. `features`는 입력 열, `train_event_ids`는 사건 분할에서 학습할 사건입니다. 두 값을 바꾸어 겹치는 사건 목록·맞힌 행 수·분모를 확인합니다.

```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

raw = pd.read_csv("docs/assets/part-03/chapter-04/p3_4_2_split_log.csv")
# 입력 열과 학습 사건을 바꾸고, 맞힌 행 수와 평가 행 수를 함께 봅니다.
features = ["flow"]
train_event_ids = ["A", "B", "C", "D"]
row_train_end = 12

row_train = raw[raw["second"] < row_train_end]
row_test = raw[raw["second"] >= row_train_end]
event_train = raw[raw["event_id"].isin(train_event_ids)]
event_test = raw[~raw["event_id"].isin(train_event_ids)]


def evaluate(name, train, test):
    if train.empty or test.empty:
        raise ValueError("Both training and evaluation need records.")
    model = DecisionTreeClassifier(random_state=0)
    model.fit(train[features], train["review_needed"])
    result = test[["event_id", "review_needed"]].copy()
    result["prediction"] = model.predict(test[features])
    result["correct"] = result["prediction"].eq(result["review_needed"])
    overlap = sorted(set(train["event_id"]) & set(test["event_id"]))
    correct = int(result["correct"].sum())
    total = len(result)
    print(f"{name}: train_rows={len(train)}, test_rows={total}, overlap={overlap}")
    print(f"row_accuracy: {correct}/{total} = {correct / total:.3f}")
    print(result.groupby("event_id").agg(
        test_rows=("correct", "size"), correct_rows=("correct", "sum")
    ).to_string())
    return result


row_result = evaluate("row_split", row_train, row_test)
print()
event_result = evaluate("event_split", event_train, event_test)
```

```text
row_split: train_rows=96, test_rows=48, overlap=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
row_accuracy: 48/48 = 1.000
          test_rows  correct_rows
event_id
A                 6             6
B                 6             6
C                 6             6
D                 6             6
E                 6             6
F                 6             6
G                 6             6
H                 6             6

event_split: train_rows=72, test_rows=72, overlap=[]
row_accuracy: 36/72 = 0.500
          test_rows  correct_rows
event_id
E                18             0
F                18            18
G                18            18
H                18             0
```

기본 실행에서 행 분할은 **48/48 = 1.0**, 사건 분할은 **36/72 = 0.5**입니다. 후자는 E·H의 36행을 틀리고 F·G의 36행을 맞힌 결과입니다. 분모 72는 네 사건의 시점 행 수이며 사건 수 4가 아닙니다.

행 분할에서는 같은 사건의 유량값이 양쪽에 반복되어, 사건마다 떨어진 값 구간을 학습하기 쉽습니다. 사건 분할에서는 평가 유량 90 이상이 학습 범위 10~70 부근을 벗어나고 모델이 모두 0으로 예측합니다. 두 실험은 학습·평가 행 수와 값 분포도 다르므로 **점수 차이 전부를 사건 겹침 하나의 효과로 분리한 실험은 아닙니다**. 사건을 분리하면 항상 점수가 내려간다는 법칙도 아닙니다.

다음으로 `train_event_ids`를 `['A', 'B', 'C', 'E']`로 바꿔 보세요. 평가 사건은 D·F·G·H가 되며, 이 자료와 모델에서는 H의 18행만 맞혀 `18/72 = 0.25`가 됩니다. `features = ['flow', 'second']`도 실행해 보세요. 기본 사건 분할에서는 점수가 여전히 0.5입니다. 열을 더 넣는다고 점수가 반드시 바뀌거나 좋아지지는 않습니다. 이 값들은 실험용 검증 예이며 가장 높은 평가 점수가 나오는 분할을 골라 성능으로 보고하지 않습니다.

## 사건별 점수에는 별도 규칙이 필요하다 {#_1}

사건당 한 번 평가하려면 시점별 예측을 사건 결과 하나로 묶는 규칙이 필요합니다. 예를 들어 18개 예측의 다수결을 사용하고 동률이면 보류한다고 정할 수 있습니다. 기본 사건 분할은 사건마다 예측이 모두 0이므로 F·G만 맞혀 `2/4 = 0.5`입니다. 행 정확도와 숫자는 같아도 분모가 다릅니다. 사건별 기록 수가 다르거나 예측이 섞이면 두 점수는 달라질 수 있습니다.

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-2-mermaid-01-ko.mmd"
```

연습으로 “사건 분할 정확도 0.5”를 더 정확한 문장으로 고쳐 보세요. 답은 “A~D로 학습하고 새 사건 E~H의 72개 시점 행 중 36개를 맞혔다”입니다. 사건당 한 번 채점했다면 다수결 등 결합 규칙과 `2/4`를 별도로 적어야 합니다.

## 체크리스트

- 관측 행·분석 대상·분할 그룹·채점 단위를 각각 말할 수 있는가?
- 사건별 라벨 반복을 새로운 독립 사건으로 세지 않는가?
- 하강량 0.3 L/min과 기울기 −0.3 L/min/s를 구분하는가?
- 1.0과 0.5를 맞힌 행 수와 전체 평가 행 수로 풀어 썼는가?
- 새 사건으로 나누었다는 것과 사건당 한 번 채점했다는 것을 구분하는가?

## 출처와 참고 자료

같은 사건의 관측을 분리하지 않는 그룹 분할과 정확도 정의의 근거입니다.

- scikit-learn developers, `Cross-validation: evaluating estimator performance`, grouped data. [공식 문서](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-19
- scikit-learn developers, `accuracy_score`. [공식 문서](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-09-19

# P3-9.7 입력과 결과는 어떤 조건이 닫혀야 예측 문제로 읽을 수 있는가

> Section ID: `P3-9.7`
> Version: `v2026.07.25`

문제를 예측 문제로 올리기로 했다면, 이제는 그 구조가 실제 [예측 계약(prediction contract)](../../../reference/concept-glossary-parts/08-ieung.md#glossary-prediction-contract)을 만족하는지 닫아야 합니다. 중요한 것은 긴 이론이 아니라 네 가지 확인입니다. 어떤 열이 입력인지, 어떤 열이 결과 후보인지, 예측 시점 이후 정보가 섞이지 않았는지, 그리고 어디까지의 정보를 보고 언제의 결과를 맞히는지입니다.

이 절에서는 입력/결과 구분, 누수 방지, 운영 시점 재현성, 시간 경계를 먼저 닫아 둡니다.

| 먼저 닫아 둘 것 | 질문으로 바꾸면 |
| --- | --- |
| 입력과 결과 구분 | 어떤 열이 [특징(feature)](../../../reference/concept-glossary-parts/12-tieut.md#glossary-feature)이고 어떤 열이 목표 후보(target candidate)인가 |
| 미래 정보 누수 방지 | 예측 시점에 아직 모르는 값이 섞이는 [데이터 누수(data leakage)](../../../reference/concept-glossary-parts/03-digeut.md#glossary-data-leakage)가 없는가 |
| 운영 시점 재현성 | 학습 때 만든 입력을 운영에서도 같은 규칙으로 다시 만들 수 있는가 |
| cutoff / horizon | 어디까지의 정보를 보고 언제의 결과를 맞히는가 |

## 한 장면으로 보기

같은 사건 표라도 아래처럼 `예측 전에 알 수 있는 열`과 `예측 뒤에 생기는 열`이 섞이면 문제 구조가 바로 깨집니다.

| event_id | recent_diff | repeatability | review_result | target_candidate |
| --- | --- | --- | --- | --- |
| A | -0.32 | high | manual_reviewed | review_needed |
| B | -0.06 | low | skipped | normal |

여기서 `recent_diff`와 `repeatability`는 예측 전에 만들 수 있는 열입니다. 반면 `review_result`는 사람이 이미 검토를 끝낸 뒤에야 생기는 열입니다. 그런데 이 열을 입력에 같이 두면, 표 모양만 보면 멀쩡해 보여도 실제로는 `정답을 보고 입력을 만든 구조`가 됩니다. 이렇게 되면 학습 시점에는 높은 점수가 나와도, 실제 예측 시점에는 존재하지 않는 정보를 써서 맞힌 셈이므로 같은 문제로 볼 수 없습니다.

아래 예제는 이 차이를 실제 모델 출력으로 확인합니다. `available_at_cutoff`는 예측 시점에 만들 수 있는 열만 사용하고, `leaky_after_review`는 예측 뒤에 생기는 `review_result_code`만 사용합니다. 두 번째 모델의 점수가 좋아 보여도, 운영 시점에는 쓸 수 없는 열이므로 예측 계약이 깨진 예입니다.

문제 상황: 예측 시점에 사용 가능한 입력과 예측 뒤에 생기는 누수 입력이 모델 점수를 어떻게 다르게 보이게 하는지 확인합니다.

입력(input): `recent_diff`, `repeatability`, `review_result_code`, `target`.

기대 출력(output): feature set별 사용 열, 테스트 정확도, 예측/실제 비교.

확인할 개념: 예측 뒤에 생기는 열을 입력에 넣으면 점수는 좋아 보일 수 있지만 실제 운영 예측 문제로는 성립하지 않습니다.

```python
# 예측 시점에 쓸 수 있는 열과 예측 뒤에 생기는 누수 열의 차이를 확인합니다.
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

records = pd.DataFrame(
    [
        {"event_id": "A", "recent_diff": -0.32, "repeatability": 3, "review_result_code": 1, "target": 1},
        {"event_id": "B", "recent_diff": -0.06, "repeatability": 1, "review_result_code": 0, "target": 0},
        {"event_id": "C", "recent_diff": -0.28, "repeatability": 2, "review_result_code": 1, "target": 1},
        {"event_id": "D", "recent_diff": -0.04, "repeatability": 1, "review_result_code": 0, "target": 0},
        {"event_id": "E", "recent_diff": -0.18, "repeatability": 1, "review_result_code": 1, "target": 1},
        {"event_id": "F", "recent_diff": -0.12, "repeatability": 3, "review_result_code": 0, "target": 0},
    ]
)

train = records.iloc[:4]
test = records.iloc[4:]
feature_sets = {
    "available_at_cutoff": ["recent_diff", "repeatability"],
    "leaky_after_review": ["review_result_code"],
}

for name, columns in feature_sets.items():
    model = DecisionTreeClassifier(random_state=0, max_depth=2)
    model.fit(train[columns], train["target"])
    predicted = model.predict(test[columns])
    comparison = [
        (event_id, int(prediction), int(actual))
        for event_id, prediction, actual in zip(test["event_id"], predicted, test["target"])
    ]
    print(name, "features:", columns)
    print(name, "accuracy:", accuracy_score(test["target"], predicted))
    print(name, "predictions:", comparison)
```

예상 출력:

```text
available_at_cutoff features: ['recent_diff', 'repeatability']
available_at_cutoff accuracy: 0.0
available_at_cutoff predictions: [('E', 0, 1), ('F', 1, 0)]
leaky_after_review features: ['review_result_code']
leaky_after_review accuracy: 1.0
leaky_after_review predictions: [('E', 1, 1), ('F', 0, 0)]
```

`leaky_after_review`는 정확도가 `1.0`이지만, 이 결과를 좋은 예측 문제라고 읽으면 안 됩니다. `review_result_code`는 사람이 이미 검토한 뒤에 생기는 열이기 때문입니다. 실제 운영 시점에는 이 값을 아직 모릅니다. 따라서 이 예제의 핵심은 높은 점수를 얻는 모델을 찾는 것이 아니라, `이 열을 예측 시점에 실제로 만들 수 있는가`를 먼저 닫아야 한다는 점입니다.

## 작은 도식으로 보기

입력과 결과 계약은 `열을 나눈다`에서 끝나지 않고, 예측 시점에 실제로 쓸 수 있는 값만 남는지까지 아래 순서로 닫혀야 합니다.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-7-mermaid-01-ko.mmd"
```

즉 입력/결과 계약을 닫는다는 것은 `열 이름을 나누는 일`만이 아니라, 각 열이 `언제 생기는가`까지 함께 적는 일입니다. 샘플 입력 한 줄이 성립하려면 그 줄 안의 값들이 모두 같은 예측 시점에서 실제로 만들 수 있어야 합니다.

같은 샘플 경계를 유지하더라도 입력 표현은 하나로만 고정되지 않습니다. 어떤 경우에는 한 줄 특징 벡터가 더 자연스럽고, 어떤 경우에는 시간 순서를 남긴 입력 묶음이 더 자연스러울 수 있습니다. 중요한 점은 표현 방식이 달라도 `예측 시점에 실제로 쓸 수 있는 입력인가`, `결과 후보와 시간 경계가 닫혀 있는가`라는 계약이 먼저 맞아야 한다는 사실입니다. 즉 여기서 다루는 것은 `아무 표`가 아니라, 샘플 경계와 시간 경계가 닫힌 입력 구조입니다. 핵심은 `표를 전달하는 일`이 아니라 `예측 시점에 성립하는 입력/결과 계약을 닫는 일`입니다. 더 넓게 보면 여기서 닫아 두는 것은 `입력 정의`, `결과 정의`, `시점 가용성`, `재현 가능성`이 함께 맞는 예측 계약입니다.

## 출처와 참고 자료

- Google, *Machine Learning Glossary*, `feature`, `label`, `label leakage`. 특징이 모델의 입력 변수이며, 라벨 누수가 라벨의 대리값이 특징에 섞이는 설계 결함이라는 용어 기준을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- Google, *Datasets: Dividing the original dataset*. 훈련·검증·테스트 분리, 같은 특징 변환을 실제 운영 데이터에도 적용해야 한다는 설명, 테스트/검증 데이터가 실제 데이터와 맞아야 한다는 관점을 확인하는 데 참고했습니다. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. 처리 단계, 재현 가능성, 버전 관리, 파생 관계를 provenance 관점에서 남기는 기준을 확인하는 데 참고했습니다. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 확인일: 2026-07-20

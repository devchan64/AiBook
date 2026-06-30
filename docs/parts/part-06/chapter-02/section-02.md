# P6-2.2 기준 모델과 개선

P6-2.1에서는 baseline과 1-NN 분류기를 나란히 두고 비교했습니다. 이제 같은 프로젝트를 한 단계 더 정리해 보겠습니다.

개선(improvement)은 무엇을 기준으로 말해야 하는가?

이 절은 그 질문에 답합니다.

개선은 점수가 올랐다는 말이 아니라, 같은 기준에서 baseline보다 무엇이 달라졌는지 설명하는 일이다.

## 이 절의 범위

이 절은 다음 질문에 답합니다.

- baseline 대비 개선을 어떻게 문서화해야 하는가?
- 정확도(accuracy)만 적는 것보다 무엇을 더 같이 남겨야 하는가?
- 작은 실습에서도 전처리(preprocessing)와 비교 기준이 왜 중요한가?

이 절은 다음 내용은 깊게 다루지 않습니다.

- 정밀도(precision), 재현율(recall), F1의 심화 비교
- 교차검증(cross-validation)
- 하이퍼파라미터 탐색 자동화

이 절에서는 baseline 대비 개선을 어떻게 문서화할지에 집중합니다. 더 다양한 평가 축을 함께 적는 감각은 뒤의 P6-4.2 토큰화와 평가, P6-5.2 검색 품질과 답변 검증에서 다시 이어지며, 교차검증과 자동 탐색 절차 전부는 현재 본편 범위 밖으로 둡니다.

## 이 절의 목표

- baseline과 개선 모델의 차이를 표와 문장으로 정리할 수 있습니다.
- 작은 분류 프로젝트에서도 전처리와 비교 기준의 역할을 설명할 수 있습니다.
- `잘 맞았다`보다 `왜 baseline보다 나은가`를 우선 기록하는 습관을 만들 수 있습니다.

## 개선을 말하기 전에 남겨야 할 것

프로젝트에서 개선을 주장하려면 최소한 다음 네 가지가 같이 있어야 합니다.

| 항목 | 왜 필요한가 |
| --- | --- |
| baseline | 최소 기준점이 있어야 모델 개선의 의미를 읽을 수 있습니다. |
| 같은 test 셋 | 비교 대상이 달라지면 점수 차이를 해석하기 어렵습니다. |
| 예측값 사례 | 숫자 하나만으로는 어떤 샘플에서 달라졌는지 알기 어렵습니다. |
| 한계 기록 | 작은 데이터, 쉬운 분할, 우연한 결과 가능성을 남겨야 합니다. |

즉, 개선은 숫자 하나가 아니라 `비교 가능한 기록 묶음`입니다.

먼저 다음 세 질문으로 읽으면 좋습니다.

| 질문 | 짧은 답 |
| --- | --- |
| 개선을 주장하려면 무엇이 필요한가? | 같은 기준에서의 비교 |
| 무엇을 꼭 같이 남겨야 하는가? | baseline, 같은 test 셋, 예측 사례, 한계 |
| 그래서 프로젝트 문서가 하는 일은 무엇인가? | 성과를 과장하지 않고 비교 근거를 남기는 일 |

## 앞 절 결과를 표로 다시 읽기

P6-2.1의 결과를 프로젝트 문서 형식으로 정리하면 다음처럼 쓸 수 있습니다.

| 모델 | 설명 | test accuracy |
| --- | --- | ---: |
| baseline | 학습 데이터에서 더 많은 라벨 하나만 계속 예측 | 0.500 |
| 1-NN | 가장 가까운 학습 샘플의 라벨을 사용 | 1.000 |

이 표만으로도 중요한 사실 하나가 드러납니다.

`이번 데이터에서는 입력 특징을 실제로 사용하는 모델이, 아무 특징도 보지 않는 baseline보다 분명히 낫다.`

하지만 좋은 프로젝트 문서는 여기서 멈추지 않습니다.

## 예측 사례를 같이 읽기

숫자와 함께 샘플별 예측을 붙이면 차이가 더 분명해집니다.

| test sample | true label | baseline | 1-NN |
| --- | ---: | ---: | ---: |
| [4.5, 68.0] | 0 | 0 | 0 |
| [5.5, 78.0] | 1 | 0 | 1 |
| [7.5, 87.0] | 1 | 0 | 1 |
| [3.5, 66.0] | 0 | 0 | 0 |

이 표를 보면 baseline은 모든 샘플을 0으로만 보았고, 1-NN은 중간 영역의 합격 샘플 두 개를 더 잘 분리했습니다.

즉, 개선의 핵심은 단순히 점수가 오른 것이 아니라 `입력 특징이 실제로 구분에 쓰였다는 점`입니다.

이 해석은 중요합니다. 프로젝트 문서에서는 `accuracy가 올랐다`보다 `무엇을 이용해 더 잘 구분했는가`가 더 좋은 설명이기 때문입니다.

## 전처리(preprocessing)를 짧게 확인하기

이번 예제는 비교적 단순해서 그대로도 잘 맞았습니다. 그래도 프로젝트 문서에는 `전처리를 해 보면 결과가 어떻게 달라지는가`를 한 번쯤 기록해 둘 가치가 있습니다.

이번 절에서는 train 데이터의 평균과 표준편차를 이용해 간단한 z-score 정규화를 적용해 봅니다. 이번에도 정확도 숫자만 한 줄로 끝내지 않고, `정규화 전 모델`, `정규화 후 모델`, `샘플별 변화 여부`를 함께 남기겠습니다.

```python
import numpy as np

train_rows = [
    {"student_id": "train-01", "hours": 2.0, "attendance": 60.0, "label": 0},
    {"student_id": "train-02", "hours": 3.0, "attendance": 65.0, "label": 0},
    {"student_id": "train-03", "hours": 4.0, "attendance": 70.0, "label": 0},
    {"student_id": "train-04", "hours": 5.0, "attendance": 72.0, "label": 0},
    {"student_id": "train-05", "hours": 6.0, "attendance": 80.0, "label": 1},
    {"student_id": "train-06", "hours": 7.0, "attendance": 85.0, "label": 1},
    {"student_id": "train-07", "hours": 8.0, "attendance": 88.0, "label": 1},
    {"student_id": "train-08", "hours": 9.0, "attendance": 92.0, "label": 1},
]

test_rows = [
    {"student_id": "test-01", "hours": 4.5, "attendance": 68.0, "label": 0},
    {"student_id": "test-02", "hours": 5.5, "attendance": 78.0, "label": 1},
    {"student_id": "test-03", "hours": 7.5, "attendance": 87.0, "label": 1},
    {"student_id": "test-04", "hours": 3.5, "attendance": 66.0, "label": 0},
]

X_train = np.array([[row["hours"], row["attendance"]] for row in train_rows])
y_train = np.array([row["label"] for row in train_rows])

X_test = np.array([[row["hours"], row["attendance"]] for row in test_rows])
y_test = np.array([row["label"] for row in test_rows])

def predict_1nn(train_x, train_y, test_x):
    predictions = []
    nearest_train_ids = []
    for x in test_x:
        distances = np.linalg.norm(train_x - x, axis=1)
        nearest_index = int(np.argmin(distances))
        predictions.append(int(train_y[nearest_index]))
        nearest_train_ids.append(train_rows[nearest_index]["student_id"])
    return np.array(predictions), nearest_train_ids

train_mean = X_train.mean(axis=0)
train_std = X_train.std(axis=0)

X_train_z = (X_train - train_mean) / train_std
X_test_z = (X_test - train_mean) / train_std

raw_knn_pred, raw_nearest_ids = predict_1nn(X_train, y_train, X_test)
scaled_knn_pred, scaled_nearest_ids = predict_1nn(X_train_z, y_train, X_test_z)

comparison_rows = []
for index, row in enumerate(test_rows):
    comparison_rows.append({
        "student_id": row["student_id"],
        "true_label": row["label"],
        "raw_knn_pred": int(raw_knn_pred[index]),
        "scaled_knn_pred": int(scaled_knn_pred[index]),
        "raw_correct": bool(raw_knn_pred[index] == y_test[index]),
        "scaled_correct": bool(scaled_knn_pred[index] == y_test[index]),
        "prediction_changed": bool(raw_knn_pred[index] != scaled_knn_pred[index]),
        "raw_nearest_train_id": raw_nearest_ids[index],
        "scaled_nearest_train_id": scaled_nearest_ids[index],
    })

project_comparison = {
    "raw_knn_accuracy": round(
        sum(row["raw_correct"] for row in comparison_rows) / len(comparison_rows), 3
    ),
    "scaled_knn_accuracy": round(
        sum(row["scaled_correct"] for row in comparison_rows) / len(comparison_rows), 3
    ),
    "prediction_changed_count": sum(
        row["prediction_changed"] for row in comparison_rows
    ),
    "raw_nearest_ids": raw_nearest_ids,
    "scaled_nearest_ids": scaled_nearest_ids,
}

print("train_mean =", np.round(train_mean, 2).tolist())
print("train_std =", np.round(train_std, 2).tolist())
print("project_comparison =", project_comparison)
print("comparison_rows =")
for row in comparison_rows:
    print(row)
```

실행 결과 예시는 다음과 같습니다.

```text
train_mean = [5.5, 76.5]
train_std = [2.29, 10.75]
project_comparison = {'raw_knn_accuracy': 1.0, 'scaled_knn_accuracy': 1.0, 'prediction_changed_count': 0, 'raw_nearest_ids': ['train-03', 'train-05', 'train-07', 'train-02'], 'scaled_nearest_ids': ['train-03', 'train-05', 'train-07', 'train-02']}
comparison_rows =
{'student_id': 'test-01', 'true_label': 0, 'raw_knn_pred': 0, 'scaled_knn_pred': 0, 'raw_correct': True, 'scaled_correct': True, 'prediction_changed': False, 'raw_nearest_train_id': 'train-03', 'scaled_nearest_train_id': 'train-03'}
{'student_id': 'test-02', 'true_label': 1, 'raw_knn_pred': 1, 'scaled_knn_pred': 1, 'raw_correct': True, 'scaled_correct': True, 'prediction_changed': False, 'raw_nearest_train_id': 'train-05', 'scaled_nearest_train_id': 'train-05'}
{'student_id': 'test-03', 'true_label': 1, 'raw_knn_pred': 1, 'scaled_knn_pred': 1, 'raw_correct': True, 'scaled_correct': True, 'prediction_changed': False, 'raw_nearest_train_id': 'train-07', 'scaled_nearest_train_id': 'train-07'}
{'student_id': 'test-04', 'true_label': 0, 'raw_knn_pred': 0, 'scaled_knn_pred': 0, 'raw_correct': True, 'scaled_correct': True, 'prediction_changed': False, 'raw_nearest_train_id': 'train-02', 'scaled_nearest_train_id': 'train-02'}
```

## 이 결과를 어떻게 해석할까

이번 데이터에서는 정규화 후에도 결과가 그대로 유지되었습니다. 이 사실은 두 방향으로 읽을 수 있습니다.

- 좋은 점: 현재 데이터에서는 특징 스케일 차이가 아주 치명적이지 않았습니다.
- 남는 질문: 더 큰 데이터나 다른 특징 조합에서는 전처리 차이가 더 크게 나타날 수 있습니다.

즉, 전처리를 했는데 점수가 그대로라는 사실도 프로젝트 문서에는 의미 있는 결과입니다. `project_comparison`에서 `prediction_changed_count`가 0이라는 점은, 이번 test 셋에서는 정규화가 예측 자체를 바꾸지 않았다는 뜻입니다.

샘플별 행(`comparison_rows`)을 같이 보면 더 좋은 이유가 있습니다.

- 점수만 같아진 것이 아니라 샘플별 예측도 모두 같았습니다.
- 가장 가까운 train 샘플 ID도 그대로 유지되었습니다.
- 따라서 이번 데이터에서는 `정규화가 의미 없었다`가 아니라, `정규화 여부보다 현재 경계 구조가 더 강하게 작동했다`고 해석하는 편이 더 정확합니다.

여기서 `변화 없음`도 결과라는 점을 익혀 두는 편이 좋습니다. 프로젝트는 항상 dramatic improvement만 기록하는 문서가 아닙니다.

## 회고 문장 예시

이 프로젝트의 회고를 한 문단으로 적는다면 다음처럼 쓸 수 있습니다.

> 이번 장난감 데이터에서는 baseline accuracy가 0.500이었고, 1-NN 모델은 1.000을 기록했다. 입력 특징이 실제 분류에 도움이 된다는 점은 확인되었지만, test 샘플 수가 4개로 매우 작아 일반화 성능을 단정할 수는 없다. 정규화 후에도 결과가 유지되었으므로 현재 데이터에서는 스케일 차이보다 라벨 경계 자체가 더 크게 작동했을 가능성이 있다. 다음 단계에서는 더 많은 샘플과 다른 분할을 적용해 결과 안정성을 확인해야 한다.

이 정도면 `숫자`, `해석`, `한계`, `다음 계획`이 모두 들어갑니다.

프로젝트 문서 관점에서는 이 네 요소가 빠지지 않는지가 더 중요합니다.

- 숫자만 있으면 보고서가 약하고
- 해석만 있으면 근거가 약하며
- 한계가 없으면 과장되기 쉽고
- 다음 계획이 없으면 반복이 끊깁니다

## 다음 프로젝트와의 연결

이 절까지 오면 Part 6의 첫 두 프로젝트가 연결됩니다.

- P6-1에서는 질문과 요약을 먼저 남겼습니다.
- P6-2에서는 baseline과 모델 비교를 붙였습니다.

이 다음에 이어질 딥러닝 프로젝트와 LLM 프로젝트에서도 같은 질문이 반복됩니다.

- 기준점은 무엇인가?
- 무엇이 실제로 좋아졌는가?
- 무엇이 아직 불안정한가?

즉, 개선을 읽는 태도는 알고리즘이 바뀌어도 그대로 남습니다.

이 절의 역할을 한 줄로 줄이면 다음과 같습니다.

`Part 6의 이후 프로젝트에서 무엇이 좋아졌다고 쓸 때, 그 문장을 더 조심스럽고 재사용 가능하게 만드는 기준을 마련하는 절이다.`

## 이 절에서 기억할 관점

- 개선은 baseline 대비 차이로 읽어야 합니다.
- 정확도만이 아니라 예측 사례와 한계를 함께 남겨야 합니다.
- 전처리 결과가 바뀌지 않았다는 사실도 의미 있는 기록입니다.
- 작은 프로젝트라도 회고 문장은 다음 반복의 출발점이 됩니다.

## 체크리스트

- baseline과 개선 모델을 같은 test 셋에서 비교했는가?
- 숫자와 함께 샘플별 예측값도 기록했는가?
- 전처리나 입력 변경의 결과를 짧게라도 남겼는가?
- 성과와 한계를 한 문단으로 동시에 요약할 수 있는가?

## 출처와 참고 자료

- NumPy Developers, `NumPy documentation`, 확인 날짜: 2026-06-29. [https://numpy.org/doc/stable/](https://numpy.org/doc/stable/){: target="_blank" rel="noopener noreferrer" }

이 절의 데이터와 비교 예시는 프로젝트 실습을 위해 만든 자체 장난감 데이터입니다.

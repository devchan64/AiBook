# P7-2.3 비교 실험 연습

> Section ID: `P7-2.3`
> Version: `v2026.07.19`

여러 비교 실험을 한 줄로 붙여 놓으면 `무엇이 전처리 문제이고 무엇이 데이터 경계 문제인가`가 더 직접 보입니다. 그 차이를 손으로 구분하는 연습입니다.

같은 학습 데이터 위에서 여러 비교 실험을 한 번에 읽으면 `정확도 한 줄`보다 `어떤 샘플은 전처리로 해결되고 어떤 샘플은 여전히 남는가`가 먼저 보입니다.

## 비교 실험에서 갈라야 할 실패

- baseline, raw 1-NN, 부분 스케일 조정, z-score 정규화를 한 화면에서 어떻게 비교할까?
- 어떤 실패는 전처리(preprocessing) 문제이고 어떤 실패는 더 많은 경계 사례나 특징이 필요한 문제인가?
- 실험 결과를 `사실 -> 해석 -> 다음 질문`으로 어떻게 다시 묶을까?

핵심은 같은 평가 셋 위에 여러 비교 실험을 나란히 올려 두고 `현재 실패가 어느 종류인가`를 구분하는 데 있습니다. 더 복잡한 모델로 넘어가기 전에, 지금 보이는 실패가 전처리 문제인지 경계 데이터 부족인지부터 갈라야 다음 행동이 선명해집니다.

## 판단 기준

- 여러 실험 설정을 같은 평가 셋에서 나란히 비교할 수 있습니다.
- `전처리로 해결된 실패`와 `여전히 남는 경계 실패`를 구분해 적을 수 있습니다.
- 비교 실험 뒤에 무엇을 더 모으고 무엇을 더 전처리할지 판단할 수 있습니다.

## 왜 비교 실험 연습이 필요한가

P7-2.2까지 읽으면 보통 `정규화하면 좋아진다`는 인상을 받기 쉽습니다. 하지만 실제 프로젝트에서는 그 다음 질문이 더 중요합니다.

- 좋아진 것은 어떤 샘플인가?
- 좋아지지 않은 샘플은 왜 남는가?
- 전처리를 더 하면 되는가, 아니면 학습 데이터 경계가 비어 있는가?

이 차이를 먼저 표로 고정하면 다음과 같습니다.

| 실패 유형 | 흔한 신호 | 다음 행동 |
| --- | --- | --- |
| 전처리 문제 | raw는 틀리고 정규화 후 맞음 | 스케일, 인코딩, 누락값 처리 다시 보기 |
| 경계 데이터 부족 | raw도 틀리고 정규화 후도 틀림 | 더 많은 경계 사례 수집, 특징 보강 검토 |
| 애매한 경계 사례 | 설정마다 예측이 서로 엇갈림 | 현재 특징만으로 충분한지 다시 보기 |

예를 들어 `z-score 정확도 0.75`가 가장 높고 `scaled 1-NN`도 같다면, 빠르게는 `둘 중 아무거나 쓰고 넘어가면 된다`고 적고 싶어질 수 있습니다. 하지만 더 안전한 다음 판단은 최고 점수 한 줄로 닫는 것이 아니라, `stress-01`처럼 전처리로 해결된 샘플이 무엇인지, `stress-02`처럼 어떤 설정에서도 남는 샘플이 무엇인지, `stress-03`처럼 설정마다 갈리는 샘플이 무엇인지를 먼저 나누는 것입니다. 그렇게 읽어야 `점수가 같은 두 설정`과 `실패 해석이 같은 두 설정`을 섞지 않게 됩니다.

```mermaid
--8<-- "assets/part-07/chapter-02/p7-2-3-preprocessing-case-flow-ko.mmd"
```

즉, 비교 실험의 목적은 `이 설정이 최고다`를 선언하는 것이 아니라 `실패의 종류를 좁히는 것`입니다.

## 입력 파일

- 학습/기본 평가 파일: [`p7-2-churn-dataset.csv`](../../../assets/part-07/chapter-02/p7-2-churn-dataset.csv)
- 추가 스트레스 평가 파일: [`p7-2-stress-test.csv`](../../../assets/part-07/chapter-02/p7-2-stress-test.csv)
- 기본 파일의 한 행 의미: `한 명의 구독 고객 기록`
- 스트레스 파일의 한 행 의미: `경계와 실패 해석을 확인하기 위한 추가 평가 사례`

학습 데이터와 추가 평가 사례를 분리해 두고, 비교 실험을 한 화면에서 나란히 읽습니다. 이렇게 하면 `설정이 달라질 때 무엇이 전처리 문제로 풀리고 무엇이 경계 사례로 남는가`를 더 또렷하게 읽을 수 있습니다.

## 연습 흐름

```mermaid
--8<-- "assets/part-07/chapter-02/p7-2-3-experiment-compare-flow-ko.mmd"
```

이 흐름에서 중요한 점은 `가장 높은 점수`보다 `어느 샘플이 왜 달라졌는가`를 먼저 읽는 것입니다.

## 실행 기록 기준

1. baseline, raw 1-NN, 부분 스케일 조정 1-NN, 정규화 1-NN을 같은 평가 셋에서 비교합니다.
2. 샘플별로 `전처리로 해결됨`, `여전히 남음`, `경계가 애매함`을 분류합니다.
3. 전처리를 더 할지, 경계 사례를 더 모을지 회고 문장으로 정리합니다.

## Python 예제

예제는 `비교 실험을 여러 줄로 붙여 놓으면 실패 해석이 어떻게 달라지는가`를 바로 확인하는 것입니다.

- 문제 상황: 어떤 실패는 전처리로 해결되고, 어떤 실패는 데이터 경계 자체가 비어 있어 남는다.
- 입력:
  - 기존 학습 데이터 12건
  - 스트레스 평가 사례 4건
- 비교 설정:
  - baseline
  - raw 1-NN
  - `usage_minutes_30d`만 60으로 나눈 부분 스케일 조정 1-NN
  - z-score 정규화 1-NN
- 기대 출력:
  - 설정별 정확도
  - 샘플별 예측 비교
  - 실패 진단 분류
- 확인할 개념:
  - 전처리 효과는 샘플별 변화로 읽어야 한다
  - 모든 실패가 전처리 문제는 아니다
  - 경계 데이터가 비어 있으면 더 많은 사례나 더 적절한 특징이 필요하다

```python
import csv
import numpy as np
from pathlib import Path

train_path = Path("docs/assets/part-07/chapter-02/p7-2-churn-dataset.csv")
stress_path = Path("docs/assets/part-07/chapter-02/p7-2-stress-test.csv")

train_rows = list(csv.DictReader(train_path.open(encoding="utf-8")))
stress_rows = list(csv.DictReader(stress_path.open(encoding="utf-8")))

for row in train_rows:
    row["unresolved_tickets"] = int(row["unresolved_tickets"])
    row["days_since_login"] = int(row["days_since_login"])
    row["usage_minutes_30d"] = int(row["usage_minutes_30d"])
    row["label"] = int(row["label"])

for row in stress_rows:
    row["unresolved_tickets"] = int(row["unresolved_tickets"])
    row["days_since_login"] = int(row["days_since_login"])
    row["usage_minutes_30d"] = int(row["usage_minutes_30d"])
    row["label"] = int(row["label"])

train_only = [row for row in train_rows if row["split"] == "train"]

def to_matrix(rows):
    return np.array([
        [row["unresolved_tickets"], row["days_since_login"], row["usage_minutes_30d"]]
        for row in rows
    ], dtype=float)

X_train = to_matrix(train_only)
y_train = np.array([row["label"] for row in train_only])
X_test = to_matrix(stress_rows)
y_test = np.array([row["label"] for row in stress_rows])

def predict_1nn(train_x, train_y, test_x):
    predictions = []
    nearest_ids = []
    for x in test_x:
        distances = np.linalg.norm(train_x - x, axis=1)
        nearest_index = int(np.argmin(distances))
        predictions.append(int(train_y[nearest_index]))
        nearest_ids.append(train_only[nearest_index]["sample_id"])
    return np.array(predictions), nearest_ids

baseline_class = int(np.bincount(y_train).argmax())
baseline_pred = np.full(len(y_test), baseline_class, dtype=int)

raw_pred, raw_nearest = predict_1nn(X_train, y_train, X_test)

X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()
X_train_scaled[:, 2] = X_train_scaled[:, 2] / 60.0
X_test_scaled[:, 2] = X_test_scaled[:, 2] / 60.0
scaled_pred, scaled_nearest = predict_1nn(X_train_scaled, y_train, X_test_scaled)

train_mean = X_train.mean(axis=0)
train_std = X_train.std(axis=0)
X_train_z = (X_train - train_mean) / train_std
X_test_z = (X_test - train_mean) / train_std
z_pred, z_nearest = predict_1nn(X_train_z, y_train, X_test_z)

comparison_rows = []
for i, row in enumerate(stress_rows):
    model_errors = {
        "baseline": int(baseline_pred[i] != y_test[i]),
        "raw_1nn": int(raw_pred[i] != y_test[i]),
        "scaled_1nn": int(scaled_pred[i] != y_test[i]),
        "zscore_1nn": int(z_pred[i] != y_test[i]),
    }

    if model_errors["raw_1nn"] and not model_errors["zscore_1nn"]:
        diagnosis = "전처리로 해결됨"
    elif all(model_errors[name] for name in ["raw_1nn", "scaled_1nn", "zscore_1nn"]):
        diagnosis = "경계 사례 추가 또는 특징 보강 필요"
    elif len({int(raw_pred[i]), int(scaled_pred[i]), int(z_pred[i])}) > 1:
        diagnosis = "설정에 따라 갈리는 경계 사례"
    else:
        diagnosis = "현재 비교 실험에서는 안정적"

    comparison_rows.append({
        "샘플": row["sample_id"],
        "focus": row["focus"],
        "정답": row["label"],
        "baseline": int(baseline_pred[i]),
        "raw_1nn": int(raw_pred[i]),
        "scaled_1nn": int(scaled_pred[i]),
        "zscore_1nn": int(z_pred[i]),
        "raw_nearest": raw_nearest[i],
        "z_nearest": z_nearest[i],
        "failure_diagnosis": diagnosis,
    })

summary = {
    "baseline 정확도": round(float((baseline_pred == y_test).mean()), 3),
    "raw 1-NN 정확도": round(float((raw_pred == y_test).mean()), 3),
    "부분 스케일 조정 1-NN 정확도": round(float((scaled_pred == y_test).mean()), 3),
    "z-score 1-NN 정확도": round(float((z_pred == y_test).mean()), 3),
    "전처리로 해결된 샘플": [
        row["샘플"] for row in comparison_rows if row["failure_diagnosis"] == "전처리로 해결됨"
    ],
    "여전히 남는 샘플": [
        row["샘플"] for row in comparison_rows if row["failure_diagnosis"] == "경계 사례 추가 또는 특징 보강 필요"
    ],
}

print("비교 실험 요약 =", summary)
print("학습 파일 =", str(train_path))
print("스트레스 평가 파일 =", str(stress_path))
print("샘플별 비교 =")
for row in comparison_rows:
    print(row)
```

실행 결과 예시는 다음처럼 읽을 수 있습니다.

```text
비교 실험 요약 = {'baseline 정확도': 0.25, 'raw 1-NN 정확도': 0.5, '부분 스케일 조정 1-NN 정확도': 0.75, 'z-score 1-NN 정확도': 0.75, '전처리로 해결된 샘플': ['stress-01'], '여전히 남는 샘플': ['stress-02']}
학습 파일 = docs/assets/part-07/chapter-02/p7-2-churn-dataset.csv
스트레스 평가 파일 = docs/assets/part-07/chapter-02/p7-2-stress-test.csv
샘플별 비교 =
{'샘플': 'stress-01', 'focus': 'raw 거리에서는 retained 고객과 가까워 보이지만 전처리 후에는 churn 신호가 살아나는 사례', '정답': 1, 'baseline': 0, 'raw_1nn': 0, 'scaled_1nn': 1, 'zscore_1nn': 1, 'raw_nearest': '학습-01', 'z_nearest': '학습-08', 'failure_diagnosis': '전처리로 해결됨'}
{'샘플': 'stress-02', 'focus': '현재 학습 데이터 경계가 비어 있어 전처리만으로는 해결되지 않는 경계 사례', '정답': 1, 'baseline': 0, 'raw_1nn': 0, 'scaled_1nn': 0, 'zscore_1nn': 0, 'raw_nearest': '학습-04', 'z_nearest': '학습-04', 'failure_diagnosis': '경계 사례 추가 또는 특징 보강 필요'}
{'샘플': 'stress-03', 'focus': '질문 수와 미접속 일수는 높지만 실제로는 유지 고객인 애매한 retained 사례', '정답': 0, 'baseline': 0, 'raw_1nn': 0, 'scaled_1nn': 1, 'zscore_1nn': 1, 'raw_nearest': '학습-06', 'z_nearest': '학습-11', 'failure_diagnosis': '설정에 따라 갈리는 경계 사례'}
{'샘플': 'stress-04', 'focus': '대부분의 비교 실험에서 일관되게 churn으로 잡혀야 하는 명확한 사례', '정답': 1, 'baseline': 0, 'raw_1nn': 1, 'scaled_1nn': 1, 'zscore_1nn': 1, 'raw_nearest': '학습-09', 'z_nearest': '학습-09', 'failure_diagnosis': '현재 비교 실험에서는 안정적'}
```

## 결과를 어떻게 읽는가

이번 연습에서 먼저 읽어야 할 것은 `z-score가 제일 높다`가 아니라 `어떤 실패가 왜 남는가`입니다.

| 샘플 | 읽어야 할 점 | 다음 행동 |
| --- | --- | --- |
| `stress-01` | raw 거리에서는 틀렸지만 전처리 후 맞았다 | 스케일과 전처리 점검을 우선한다 |
| `stress-02` | 모든 비교 실험에서 여전히 틀렸다 | 경계 사례 수집이나 특징 보강을 검토한다 |
| `stress-03` | 설정에 따라 retained/churn이 갈린다 | 현재 특징만으로 충분한지 다시 본다 |
| `stress-04` | 대부분의 실험에서 안정적으로 맞는다 | 현재 구조의 기준 사례로 남긴다 |

이 차이를 통해 독자는 두 가지를 잡아야 합니다.

- `전처리로 해결된 실패`는 설정을 더 다듬을 가치가 있다는 신호입니다.
- `여전히 남는 실패`는 데이터 경계나 특징 자체를 다시 봐야 한다는 신호입니다.

즉, 비교 실험의 결론은 `무조건 z-score`가 아니라 `현재 실패가 어느 종류인가`입니다.

## 결과 해석 기준

- raw는 틀리고 정규화는 맞는 샘플이 실제로 얼마나 있는가?
- 정규화 뒤에도 틀리는 샘플은 현재 학습 데이터의 어떤 빈 구간을 보여 주는가?
- 설정마다 예측이 엇갈리는 샘플은 왜 애매한가?
- 다음 반복에서 먼저 할 일은 전처리 보강인가, 경계 사례 수집인가?

## 프로젝트 기록 예시

실습 뒤에는 다음 형식으로 짧게 기록해 두는 편이 좋습니다.

| 항목 | 적을 내용 |
| --- | --- |
| 비교 설정 | baseline, raw, scaled, z-score 중 무엇을 돌렸는가 |
| 전처리로 해결된 샘플 | 어떤 실패가 설정 변경으로 사라졌는가 |
| 여전히 남는 샘플 | 어떤 실패는 전처리 뒤에도 남는가 |
| 해석 | 전처리 문제인지, 데이터 경계 문제인지 |
| 다음 질문 | 더 모을 사례와 더 바꿀 특징은 무엇인가 |

한 문단으로 쓰면 예를 들어 다음처럼 정리할 수 있습니다.

> `stress-01`은 raw 거리에서는 retained 쪽으로 잘못 붙었지만, 사용 시간 스케일을 줄이거나 z-score 정규화를 적용하자 churn으로 바로잡혔다. 반면 `stress-02`는 모든 비교 실험에서 retained로 남아, 지금 문제는 전처리보다도 `4건 안팎의 문의 수와 10일대 미접속 구간`에 해당하는 churn 사례가 학습 데이터에 거의 없다는 점에 더 가깝다. 따라서 다음 반복에서는 전처리 튜닝만 더 하는 대신 경계 구간 고객 사례를 추가 수집하고, 필요하면 결제 실패 횟수 같은 새 특징도 검토하는 편이 적절하다.

## 동작 단위 센서 비교 실험 확장

동작 단위 합성 데이터에서는 같은 동작 요약을 세 가지 방식으로 비교해 볼 수 있습니다.

| 비교 설정 | 판단 방식 | 실패 해석 |
| --- | --- | --- |
| 원시 tracking 오류만 보기 | `tracking_error_mean`이 큰 동작만 잡음 | 단발 튐에는 민감하지만 반복 drift를 놓칠 수 있음 |
| 구간 특징 보기 | 중반 평균 하락 또는 후반 하강 증가를 함께 봄 | 반복되는 패턴 변화를 더 잘 잡음 |
| 기준선 차이 보기 | 기준선 평균과의 차이를 함께 계산 | 현재 신호가 평소 수준에서 얼마나 벗어났는지 설명하기 좋음 |

```python
import csv
from pathlib import Path

summary_path = Path("docs/assets/part-07/chapter-01/p7-action-unit-summary.csv")
rows = list(csv.DictReader(summary_path.open(encoding="utf-8")))

for row in rows:
    row["event_order"] = int(row["event_order"])
    row["mid_flow_mean"] = float(row["mid_flow_mean"])
    row["late_drop_rate"] = float(row["late_drop_rate"])
    row["tracking_error_mean"] = float(row["tracking_error_mean"])

baseline_rows = [row for row in rows if row["period"] == "baseline"]
recent_rows = [row for row in rows if row["period"] == "recent"]
baseline_mid = sum(row["mid_flow_mean"] for row in baseline_rows) / len(baseline_rows)
baseline_late = sum(row["late_drop_rate"] for row in baseline_rows) / len(baseline_rows)

comparison = []
for row in recent_rows:
    raw_flag = row["tracking_error_mean"] > 0.12
    segment_flag = row["mid_flow_mean"] < 2.10 or row["late_drop_rate"] > 0.15
    baseline_gap_flag = (
        row["mid_flow_mean"] - baseline_mid < -0.20
        or row["late_drop_rate"] - baseline_late > 0.05
    )

    if segment_flag and not raw_flag:
        diagnosis = "원시 오류만 보면 놓치지만 구간 특징으로 잡힘"
    elif raw_flag and not segment_flag:
        diagnosis = "단발 튐 가능성이 있어 재현 확인 필요"
    elif segment_flag and baseline_gap_flag:
        diagnosis = "반복 drift 후보"
    else:
        diagnosis = "현재 비교에서는 낮은 우선순위"

    comparison.append({
        "event_id": row["event_id"],
        "raw_tracking_flag": raw_flag,
        "segment_feature_flag": segment_flag,
        "baseline_gap_flag": baseline_gap_flag,
        "diagnosis": diagnosis,
    })

for row in comparison:
    print(row)
```

실행 결과는 다음처럼 읽을 수 있습니다.

```text
{'event_id': 'E009', 'raw_tracking_flag': False, 'segment_feature_flag': True, 'baseline_gap_flag': True, 'diagnosis': '원시 오류만 보면 놓치지만 구간 특징으로 잡힘'}
{'event_id': 'E010', 'raw_tracking_flag': True, 'segment_feature_flag': False, 'baseline_gap_flag': False, 'diagnosis': '단발 튐 가능성이 있어 재현 확인 필요'}
{'event_id': 'E011', 'raw_tracking_flag': False, 'segment_feature_flag': True, 'baseline_gap_flag': True, 'diagnosis': '원시 오류만 보면 놓치지만 구간 특징으로 잡힘'}
{'event_id': 'E012', 'raw_tracking_flag': False, 'segment_feature_flag': True, 'baseline_gap_flag': True, 'diagnosis': '원시 오류만 보면 놓치지만 구간 특징으로 잡힘'}
```

이 비교에서는 `E010`처럼 한 번 튄 동작과 `E009`, `E011`, `E012`처럼 구간 구조가 반복해서 달라진 동작이 갈립니다. 따라서 다음 반복의 우선순위는 원시 오류 임계값을 더 세게 만드는 것이 아니라, 구간 특징과 기준선 차이를 함께 기록하는 쪽에 가깝습니다.

## 선택 실험: 절대 시간축과 진행도축

길이가 다른 동작을 비교할 때는 같은 5초 구간을 비교할지, 전체 동작의 10%, 20%, 30%처럼 진행도 구간을 비교할지 먼저 정해야 합니다. 절대 시간축은 실제 시각 차이를 보존하지만, 동작 길이가 다르면 서로 다른 단계가 한 칸에 섞일 수 있습니다. 진행도축은 `초반`, `중반`, `후반`처럼 같은 단계끼리 비교하기 쉽지만, 실제로 몇 초가 걸렸는지는 약해집니다.

| 비교 축 | 잘 보이는 것 | 조심할 점 |
| --- | --- | --- |
| 절대 시간축 | 몇 초 뒤에 신호가 달라졌는가 | 짧은 동작과 긴 동작의 단계가 섞일 수 있음 |
| 진행도축 | 같은 진행 단계에서 패턴이 달라졌는가 | 실제 소요 시간 차이를 놓칠 수 있음 |

이 선택 실험은 별도 모델을 더하는 일이 아닙니다. 같은 동작 요약을 읽기 전에 `지금 질문이 실제 시간 차이인가, 같은 단계 비교인가`를 먼저 고르는 연습입니다.

## 직접 바꿔 보며 확인할 것

1. `stress-02`와 비슷한 churn 사례를 학습 파일에 두 건 더 추가했다고 가정하고 직접 넣어 봅니다.
   관찰할 점: 정규화보다 데이터 보강이 더 직접적으로 듣는가?

2. `usage_minutes_30d`를 `30일 평균 세션 수`처럼 다른 행동 특징으로 바꾼다고 가정해 봅니다.
   관찰할 점: `stress-03` 같은 애매한 retained 사례를 더 잘 분리할 수 있을까?

3. `scaled_1nn`에서 사용 시간 나누기 값을 `60` 대신 `30`, `120`으로 바꿔 봅니다.
   관찰할 점: 부분 스케일 조정은 얼마나 민감하고 왜 z-score보다 해석이 불안정할 수 있는가?

4. 길이가 다른 동작을 5초 단위와 25% 진행도 단위로 각각 묶는다고 가정해 봅니다.
   관찰할 점: 지금 비교하려는 질문은 실제 시간 차이를 보는 쪽에 가까운가, 같은 진행 단계의 패턴을 보는 쪽에 가까운가?

판단 기준은 가장 높은 점수가 아니라 실패가 줄어든 이유입니다. 전처리 뒤 사라진 실패는 입력 스케일 문제에 가깝고, 어떤 설정에서도 남는 실패는 데이터 경계나 질문 정의를 먼저 다시 봐야 합니다.

## 체크리스트

| 확인할 것 | 스스로 답할 질문 |
| --- | --- |
| 비교 실험 | 여러 비교 실험을 같은 평가 셋에서 나란히 실행했는가? |
| 실패 구분 | `전처리로 해결된 실패`와 `여전히 남는 실패`를 구분했는가? |
| 샘플 진단 | 점수뿐 아니라 샘플별 실패 진단을 기록했는가? |
| 다음 우선순위 | 다음 반복을 `전처리`와 `데이터 보강` 중 어디서 시작할지 적었는가? |
| 비교 축 | 길이가 다른 동작을 비교할 때 절대 시간축과 진행도축 중 어느 쪽이 현재 질문에 맞는지 적었는가? |

## 출처와 참고 자료

- 학습 데이터: [`p7-2-churn-dataset.csv`](../../../assets/part-07/chapter-02/p7-2-churn-dataset.csv)
- 스트레스 평가 데이터: [`p7-2-stress-test.csv`](../../../assets/part-07/chapter-02/p7-2-stress-test.csv)
- 동작 단위 합성 동작 요약: [`p7-action-unit-summary.csv`](../../../assets/part-07/chapter-01/p7-action-unit-summary.csv)
- 이 문서는 자체 실습 예시를 사용했습니다. 외부 자료를 직접 인용하지 않았습니다.

# 3.6 측정값과 샘플을 혼동하면 왜 문제가 생기는가

샘플 단위는 뒤에 나오는 거의 모든 개념의 기준점입니다. 따라서 측정값과 샘플을 혼동하면 단지 용어 하나를 잘못 쓰는 데서 끝나지 않습니다. feature의 뜻도 흔들리고, label의 뜻도 흔들리고, evaluation이 무엇을 평가하는지도 같이 흔들립니다.

먼저 가장 흔한 혼동부터 보겠습니다. 동작 중 1초 간격으로 측정된 시계열 표가 있다고 합시다. 초심자는 종종 이 표의 한 행을 그대로 `샘플 1건`으로 받아들입니다. 이렇게 되면 압력, 유량, 온도 같은 현재 값들을 곧바로 feature처럼 붙이기 시작합니다. 하지만 우리가 실제로 알고 싶은 것이 `이번 동작이 평소와 다른 구조였는가`라면, 시점별 한 줄은 그 질문에 답하는 샘플이 아닙니다.

왜 문제가 생기는지 항목별로 보겠습니다.

## 1. feature의 뜻이 흔들린다

동작 1회를 샘플로 본다면 총 동작 시간, 초반 평균, 후반 하강률, 변동성 같은 값이 feature가 될 수 있습니다. 반면 시점별 한 줄을 샘플로 본다면 같은 열들은 아직 계산할 수 없거나, 계산하더라도 그 줄 하나만으로는 의미가 불완전합니다.

## 2. label의 뜻이 흔들린다

어떤 운영 라벨이 `검토 필요`라면, 보통 그것은 개별 측정 한 점에 붙는 라벨이 아니라 동작 1회나 최근 구간에 붙는 라벨입니다. 그런데 시점별 한 줄을 샘플로 읽어 버리면, 그 라벨을 어느 줄에 붙여야 할지부터 애매해집니다.

## 3. 평가 단위가 흔들린다

동작 1회가 샘플이라면 학습과 평가도 동작 1회 단위로 해야 합니다. 그런데 시점별 한 줄을 샘플처럼 다루면, 같은 동작에서 나온 서로 가까운 행들이 훈련과 평가에 섞여 들어갈 수 있습니다.

## 4. 운영 해석이 흔들린다

운영자는 대개 `한 시점의 숫자`보다 `동작 전체가 어땠는가`를 알고 싶어 합니다. 그런데 측정값과 샘플을 혼동하면 운영 질문과 데이터 구조가 어긋납니다.

이 네 문제를 한 번에 보면 왜 샘플 단위가 단순한 용어 문제가 아닌지 더 분명해집니다.

| 흔들리는 것 | 왜 같이 흔들리는가 |
| --- | --- |
| feature | 무엇을 요약해야 하는지가 샘플 단위에 달려 있기 때문 |
| label | 어떤 결과가 한 건에 붙는지가 샘플 단위에 달려 있기 때문 |
| split/evaluation | 무엇을 훈련과 평가에 나눌지가 샘플 단위에 달려 있기 때문 |
| 운영 문장 | 사람이 무엇을 한 사례로 읽을지가 샘플 단위에 달려 있기 때문 |

즉 샘플 단위는 Part 3의 한 절에서만 필요한 결정이 아니라, 뒤에서 다룰 feature engineering, 기준선 비교, review queue, Part 4 handoff까지 모두 기대는 바닥 구조입니다.

아래 예시는 같은 원천데이터를 `시점별 표`로 볼 때와 `동작 단위 표`로 볼 때 해석이 어떻게 달라지는지 보여 줍니다.

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.5, "review_needed": 1},
        {"event_id": "A", "second": 1, "flow": 1.8, "review_needed": 1},
        {"event_id": "A", "second": 2, "flow": 1.1, "review_needed": 1},
        {"event_id": "B", "second": 0, "flow": 0.4, "review_needed": 0},
        {"event_id": "B", "second": 1, "flow": 1.1, "review_needed": 0},
        {"event_id": "B", "second": 2, "flow": 1.0, "review_needed": 0},
    ]
)

per_row = raw[["event_id", "second", "flow", "review_needed"]]
per_event = (
    raw.groupby("event_id")
    .agg(
        flow_mean=("flow", "mean"),
        flow_max=("flow", "max"),
        review_needed=("review_needed", "max"),
    )
    .reset_index()
)

print("row-level samples:", len(per_row))
print("event-level samples:", len(per_event))
print(per_event)
```

예상 출력:

```text
row-level samples: 6
event-level samples: 2
  event_id  flow_mean  flow_max  review_needed
0        A   1.133333       1.8              1
1        B   0.833333       1.1              0
```

이 출력에서 `review_needed`는 동작 1회에 붙는 라벨입니다. 그런데 원시 표를 그대로 샘플처럼 읽으면 라벨이 여섯 줄에 반복되어 붙습니다. 반면 동작 단위 표로 바꾸면 라벨이 두 건의 샘플에만 붙습니다. 이 차이가 바로 feature, label, evaluation 단위가 함께 흔들리는 이유입니다.

이 절에서 중요한 것은 `샘플 단위가 흔들리면 후속 개념이 함께 흔들린다`는 점입니다. feature, label, split, evaluation은 따로 떨어진 주제가 아니라, 무엇을 한 건으로 볼지에 기대고 있습니다. 따라서 이 절에서 기억할 핵심은 다음 문장입니다. `측정값과 샘플을 구분하지 못하면 데이터셋 전체의 뜻이 흔들린다.` 다음 장에서는 바로 이 구분을 전제로, 원시 로그를 어떤 표로 다시 묶어야 비교 가능한 샘플 구조가 생기는지 살펴보겠습니다.

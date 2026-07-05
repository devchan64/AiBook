# 3.16 어떤 운영 문제는 왜 비교 리포트로 남겨야 하는가

모든 운영 문제를 예측 문제로 밀어 넣는 것은 좋은 데이터 모델링이 아닙니다. 어떤 경우에는 비교 리포트가 더 정직하고 더 유용합니다. 특히 원인 라벨이 약하거나, 운영자가 실제로 보고 싶은 것이 `정답 분류`보다 `지금 먼저 볼 대상을 고르는 일`일 때 그렇습니다.

비교 리포트가 더 적합한 상황은 보통 다음과 같습니다.

- 평소 대비 최근 변화 방향을 먼저 보여 주는 것이 중요할 때
- 확정 라벨보다 검토 우선순위가 더 실용적일 때
- 변화 원인을 아직 자동으로 단정할 수 없을 때
- 사람의 후속 확인이 운영 절차에 포함될 때

예를 들어 최근 구간 평균, 변동성, 패턴 차이, 기준선 대비 차이값, 검토 필요 여부만 잘 정리해도 운영자에게 충분히 유용할 수 있습니다. 이 경우 중요한 것은 `무엇을 맞혔는가`보다 `무엇을 먼저 보여 주었는가`입니다. 즉 좋은 비교 리포트는 단순한 중간 산출물이 아니라, 실제 운영 의사결정의 한 형태가 됩니다.

반대로 예측 문제로 넘어가려면 적어도 다음 조건이 필요합니다.

- target이 비교적 안정적으로 정의되어 있다.
- 샘플 단위와 라벨 단위가 맞는다.
- split과 evaluation을 설계할 만큼 표본 구조가 정리되어 있다.

작은 장난감 표를 보면 비교 리포트와 예측 문제의 차이가 더 잘 보입니다.

| event_id | diff | repeatability | review_needed | cause_label |
| --- | --- | --- | --- | --- |
| A | -0.35 | high | 1 | 없음 |
| B | -0.08 | low | 0 | 없음 |
| C | -0.31 | high | 1 | 없음 |

```python
import pandas as pd

report_table = pd.DataFrame(
    [
        {"event_id": "A", "diff": -0.35, "repeatability": "high", "review_needed": 1, "cause_label": None},
        {"event_id": "B", "diff": -0.08, "repeatability": "low", "review_needed": 0, "cause_label": None},
        {"event_id": "C", "diff": -0.31, "repeatability": "high", "review_needed": 1, "cause_label": None},
    ]
)

print(report_table)
print("review label count:", report_table["review_needed"].notna().sum())
print("cause label count:", report_table["cause_label"].notna().sum())
```

예상 출력:

```text
  event_id  diff repeatability  review_needed cause_label
0        A -0.35          high              1        None
1        B -0.08           low              0        None
2        C -0.31          high              1        None
review label count: 3
cause label count: 0
```

이 출력에서는 `review_needed`는 모두 있지만 `cause_label`은 하나도 없습니다. 이런 상황에서는 검토 우선순위 리포트는 만들 수 있어도, 원인 예측 모델은 아직 바로 만들기 어렵습니다. 따라서 비교 리포트는 예측 모델의 실패 대안이 아니라, 데이터와 라벨 상태에 맞는 올바른 산출물일 수 있습니다.

따라서 이 절에서의 결론은 단순합니다. `비교 리포트는 임시 대안이 아니라, 그 자체로 올바른 문제 설정일 수 있다.`

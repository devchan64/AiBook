# 3.17 Part 4가 이어받을 feature와 target의 전제

Part 3의 마지막 단계는 이제 Part 4로 무엇을 넘길 수 있는지 정리하는 것입니다. 머신러닝은 데이터를 자동으로 이해하는 마법 단계가 아닙니다. 오히려 머신러닝 Part는 이미 정리된 샘플 단위, feature 후보, target 후보를 이어받아 학습 구조로 바꾸는 단계에 가깝습니다.

따라서 Part 4가 시작되기 전에 적어도 다음 질문에는 답할 수 있어야 합니다.

- 한 행은 무엇을 뜻하는가
- feature로 남길 열은 무엇인가
- target 후보는 실제로 무엇인가
- 비교 리포트로 남길 문제와 예측 문제를 구분했는가

예를 들어 동작 1회 요약 표가 있다면 총 시간, 구간 평균, 기울기, 변동성, 세그먼트 표현은 feature 후보가 될 수 있습니다. 반면 `검토 필요`, `정상/주의`, 특정 결과 상태 같은 값은 target 후보가 될 수 있습니다. 하지만 이 target 후보가 실제로 충분한 라벨인지, 운영상 일관되게 붙는 값인지는 다시 따져야 합니다.

이 절에서 중요한 것은 feature와 target을 이름만 붙이는 것이 아니라, 왜 그 구분이 가능한지 설명하는 것입니다. `이 열은 설명 변수로 쓸 수 있다`, `이 열은 나중에 맞히고 싶은 결과다`라는 구분이 서지 않으면 Part 4의 모델 설명도 공중에 뜹니다.

예를 들어 다음처럼 같은 표 안에서도 역할이 다릅니다.

| 열 이름 | 역할 후보 |
| --- | --- |
| `mid_flow_mean` | feature |
| `late_drop_rate` | feature |
| `flow_variability` | feature |
| `review_needed` | target 후보 |
| `window_start` | 식별 또는 운영 문맥 |

```python
import pandas as pd

dataset = pd.DataFrame(
    [
        {"event_id": "A", "mid_flow_mean": 2.3, "late_drop_rate": -0.8, "flow_variability": 0.22, "review_needed": 1},
        {"event_id": "B", "mid_flow_mean": 2.5, "late_drop_rate": -0.2, "flow_variability": 0.07, "review_needed": 0},
    ]
)

feature_cols = ["mid_flow_mean", "late_drop_rate", "flow_variability"]
target_col = "review_needed"

print("X shape:", dataset[feature_cols].shape)
print("y shape:", dataset[target_col].shape)
print(dataset[feature_cols])
print(dataset[target_col])
```

예상 출력:

```text
X shape: (2, 3)
y shape: (2,)
   mid_flow_mean  late_drop_rate  flow_variability
0            2.3            -0.8              0.22
1            2.5            -0.2              0.07
0    1
1    0
Name: review_needed, dtype: int64
```

이 출력은 Part 4가 이어받는 기본 형태를 그대로 보여 줍니다. 어떤 열은 입력 `X`로 가고, 어떤 열은 출력 `y`로 갑니다. 이 구분이 선명해야 뒤에서 split, 학습, 평가를 설명할 수 있습니다.

즉 Part 4가 이어받는 것은 단순한 CSV 파일이 아니라, `샘플 단위가 고정된 표`, `설명 가능한 feature`, `후보 target`, `비교 리포트로 남길 범위`까지 정리된 전제입니다.

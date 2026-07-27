<a id="off-policy"></a>

### 오프 정책(off-policy)

- 뜻: 실제로 행동을 만들어 낸 정책과는 다른 기준의 정책 가치를 배우는 강화학습 방식입니다. 예를 들어 다음 상태에서 가장 좋아 보이는 행동 가치를 기준으로 갱신하는 방식이 여기에 속합니다.
- 왜 중요한가: 탐험 때문에 실제 행동 흐름이 흔들려도, 학습은 목표 정책이나 최적 행동 쪽을 향할 수 있음을 설명해 줍니다. 이 개념이 있어야 off-policy 갱신이 on-policy 갱신보다 낙관적으로 보일 수 있는 이유를 이해할 수 있습니다.
- 함께 볼 개념: `on-policy`, `정책(policy)`, `탐험(exploration)`, `가치 기반 강화학습(value-based reinforcement learning)`
- 중심 Section: `P4-19.1`
- 등장 Section:

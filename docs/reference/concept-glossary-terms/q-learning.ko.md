<a id="q-learning"></a>

### Q-learning

- 뜻: 다음 상태에서 가장 좋아 보이는 행동의 Q-value를 기준으로 현재 상태-행동 값을 갱신하는 가치 기반 강화학습 알고리즘입니다. 실제로 다음에 어떤 행동을 했는지보다, 다음 상태에서 가능한 최선의 값을 기준으로 배웁니다.
- 왜 중요한가: Q-learning은 off-policy 관점을 보여 주는 대표 예입니다. 이 개념이 있어야 SARSA와 비교할 때 `가장 좋아 보이는 다음 행동`을 기준으로 하는 갱신과 `실제로 선택한 다음 행동`을 기준으로 하는 갱신을 구분할 수 있습니다.
- 함께 볼 개념: `Q-value`, `SARSA`, `off-policy`, `가치 기반 강화학습(value-based reinforcement learning)`
- 중심 Section: `P4-19.1`
- 등장 Section: `P4-19.5`

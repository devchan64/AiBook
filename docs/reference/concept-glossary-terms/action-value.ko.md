<a id="action-value"></a>

### 행동 가치(action value)

- 뜻: 어떤 상태에서 특정 행동을 선택했을 때 기대할 수 있는 장기 보상의 값입니다. 상태 자체의 좋음이 아니라 `이 상태에서 이 행동을 하는 것이 얼마나 좋은가`를 읽습니다.
- 왜 중요한가: 강화학습의 실제 선택은 상태 안에서 여러 행동 후보를 비교하는 문제이기 때문입니다. 행동 가치를 이해해야 Q-value, Q-learning, SARSA의 업데이트 기준을 같은 틀에서 읽을 수 있습니다.
- 함께 볼 개념: `상태 가치(state value)`, `Q-value`, `Q-learning`, `SARSA`
- 중심 Section: `P4-19.1`
- 등장 Section:

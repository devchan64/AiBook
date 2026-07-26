<a id="sarsa"></a>

### SARSA

- 뜻: 상태 표현(state), 에이전트 행동(action), 보상(reward), 다음 상태(next state), 다음 행동(next action)의 흐름을 기준으로 Q-value를 갱신하는 가치 기반 강화학습 알고리즘입니다. 다음 상태에서 실제로 선택한 다음 행동의 값을 업데이트 기준으로 씁니다.
- 왜 중요한가: SARSA는 on-policy 관점을 보여 주는 대표 예입니다. 탐험이 섞인 실제 행동 흐름까지 값 추정에 반영하므로, Q-learning과 비교할 때 실패 비용이나 탐험 비용을 어떻게 읽을지 판단하는 데 도움이 됩니다.
- 함께 볼 개념: `Q-value`, `Q-learning`, `on-policy`, `탐험(exploration)`
- 중심 Section: `P4-19.1`
- 등장 Section:

<a id="q-value"></a>

### Q-value

- 뜻: 상태 `s`에서 행동 `a`를 선택했을 때 기대되는 장기 보상을 나타내는 행동 가치입니다. 보통 `Q(s, a)`처럼 쓰며, `지금 이 상태에서 이 행동을 하면 앞으로 얼마나 괜찮은가`를 점수로 적습니다.
- 왜 중요한가: Q-learning과 SARSA는 모두 Q-value를 갱신하지만, 다음 값을 어디서 가져오느냐가 다릅니다. 그래서 Q-value는 가치 기반 강화학습에서 행동 비교와 업데이트 차이를 읽는 핵심 손잡이입니다.
- 함께 볼 개념: `행동 가치(action value)`, `Q-learning`, `SARSA`, `가치 기반 강화학습(value-based reinforcement learning)`
- 중심 Section: `P4-19.1`
- 등장 Section: `P4-19.5`

<a id="value-based-reinforcement-learning"></a>

### 가치 기반 강화학습(value-based reinforcement learning)

- 뜻: 상태나 상태-행동 쌍에 장기 보상의 예상값을 붙이고, 그 값을 기준으로 더 나은 행동을 고르는 강화학습 접근입니다. 정책을 바로 출력하기보다 `어떤 선택이 장기적으로 얼마나 좋은가`를 먼저 숫자로 배웁니다.
- 왜 중요한가: 상태 가치나 행동 가치 같은 가치 함수를 중심으로 읽는 강화학습 알고리즘의 공통 관점을 잡아 주기 때문입니다. 이 개념이 있어야 정책 기반 강화학습과 비교할 때 `값을 배운 뒤 행동을 고르는가`, `정책 자체를 직접 조정하는가`를 구분할 수 있습니다.
- 함께 볼 개념: `강화학습(reinforcement learning)`, `상태 가치(state value)`, `행동 가치(action value)`, `정책 기반 강화학습(policy-based reinforcement learning)`
- 중심 Section: `P4-19.1`
- 등장 Section: `P4-19.4`, `P4-19.5`

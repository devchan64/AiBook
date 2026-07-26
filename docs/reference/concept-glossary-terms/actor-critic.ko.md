<a id="actor-critic"></a>

### 액터-크리틱(actor-critic)

- 뜻: 행동을 만들어 내는 actor와 그 행동의 좋고 나쁨을 평가하는 critic을 함께 쓰는 강화학습 구조입니다. 정책을 직접 조정하되, 가치 추정에서 오는 평가 신호를 함께 사용합니다.
- 왜 중요한가: 정책 기반 접근과 가치 기반 접근을 단순한 경쟁 관계가 아니라 역할 분담으로 읽게 해 줍니다. actor-critic을 이해해야 정책 업데이트의 흔들림을 줄이기 위해 왜 critic이 함께 등장하는지 설명할 수 있습니다.
- 함께 볼 개념: `정책 기반 강화학습(policy-based reinforcement learning)`, `policy gradient`, `가치 기반 강화학습(value-based reinforcement learning)`
- 중심 Section: `P4-19.2`
- 등장 Section: `P4-19.4`, `P4-19.6`

<a id="policy-gradient"></a>

### 정책 기울기(policy gradient)

- 뜻: 정책 파라미터를 기대 보상이 커지는 방향으로 직접 조정하려는 강화학습 방법 계열입니다. 보상이 좋았던 행동은 더 자주 나오게 하고, 나빴던 행동은 덜 나오게 하는 방향을 찾습니다.
- 왜 중요한가: 정책 기반 강화학습이 단순히 행동을 고르는 규칙이 아니라 조정 가능한 함수라는 점을 보여 줍니다. 이 개념이 있어야 REINFORCE, actor-critic, 후속 정책 최적화 방법을 같은 흐름에서 읽을 수 있습니다.
- 함께 볼 개념: `정책 기반 강화학습(policy-based reinforcement learning)`, `REINFORCE`, `actor-critic`, `기대 보상(expected return)`
- 중심 Section: `P4-19.2`
- 등장 Section: `P4-19.6`

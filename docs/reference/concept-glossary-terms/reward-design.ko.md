<a id="reward-design"></a>

### 보상 설계(reward design)

- 뜻: 강화학습에서 강화학습 에이전트가 무엇을 잘했다고 볼지 보상 함수와 제약 조건으로 정하는 작업입니다. 단순히 숫자를 만드는 일이 아니라, 시스템이 어떤 행동을 더 하도록 유도할지 정하는 목표 정의입니다.
- 왜 중요한가: 보상이 실제 목표를 거칠게 대신하면 강화학습 에이전트는 숫자는 올리지만 사람의 의도는 놓칠 수 있습니다. 따라서 보상 설계는 reward hacking, 안전성, sim-to-real gap을 점검하는 출발점입니다.
- 함께 볼 개념: `보상(reward)`, `진짜 목표(true objective)`, `reward hacking`, `대리 목표(proxy target)`
- 중심 Section: `P4-19.3`
- 등장 Section:

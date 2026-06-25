# P3-2.3 근거 검토 메모

## 대상 섹션

- `docs/parts/part-03/chapter-02/section-03.md`
- 주제: 강화학습(reinforcement learning)

## 확인한 근거

### Sutton and Barto, Reinforcement Learning: An Introduction

- URL: https://mitpress.mit.edu/9780262039246/reinforcement-learning/
- 확인 날짜: 2026-06-25
- 활용 내용:
  - MIT Press 소개에서 강화학습을 복잡하고 불확실한 환경과 상호작용하면서 에이전트가 받는 보상의 총량을 최대화하려는 계산적 접근으로 설명하는 점을 확인했습니다.
  - 이 섹션에서는 해당 설명을 초심자용으로 `행동을 해 보고, 보상을 확인하며, 다음 행동 방식을 조정하는 학습`으로 일반화했습니다.
  - 책의 세부 알고리즘 목록은 본 섹션 범위를 넘기므로 소개하지 않았습니다.

### Buffet, Pietquin, Weng, Reinforcement Learning

- URL: https://arxiv.org/abs/2005.14419
- 확인 날짜: 2026-06-25
- 활용 내용:
  - 강화학습을 적응적 제어(adaptive control)와 순차적 의사결정(sequential decision-making) 문제로 설명하는 점을 확인했습니다.
  - 에이전트가 상태를 관찰하고, 행동을 수행하고, 보상을 받고, 새 상태로 이동하며, 시행착오를 통해 정책을 학습한다는 흐름을 본문 도식과 용어 설명에 반영했습니다.
  - 가치 기반(value-based), 정책 탐색(policy search), actor-critic 등 세부 접근은 현재 섹션의 범위를 넘기므로 다루지 않았습니다.

## 반영 판단

- Part 3 이후는 초심자를 기준으로 작성해야 하므로, 공식과 알고리즘 이름보다 게임 예시와 표를 먼저 배치했습니다.
- `agent`라는 용어가 LLM 서비스의 에이전트와 혼동될 수 있어, 강화학습 문맥의 에이전트와 서비스 아키텍처 문맥의 에이전트를 구분했습니다.
- RLHF와 LLM 정렬은 Part 5에서 다시 다룰 수 있으므로 이 섹션에서는 깊게 설명하지 않았습니다.
- Q-learning, SARSA, policy gradient, actor-critic은 본문에서 이름만 언급하되, 목차에 P3-19.1과 P3-19.2 후속 학습 위치를 추가했습니다.

## 주의할 표현

- 보상을 지도학습의 정답 라벨처럼 설명하지 않습니다.
- 강화학습을 단순히 `상벌로 훈련하는 방식`으로만 축소하지 않습니다.
- 게임 예시가 현실 적용의 쉬움을 보장한다고 말하지 않습니다.
- 강화학습의 에이전트와 LLM 에이전트를 같은 뜻으로 단정하지 않습니다.

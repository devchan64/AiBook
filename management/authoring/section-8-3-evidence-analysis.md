# 8.3 근거 검토 메모

이 문서는 `docs/parts/part-01/chapter-08/section-03.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- 8.1의 라벨(label), 8.2의 라벨 없는 구조(structure) 설명을 이어 받아 강화학습(reinforcement learning)의 차이를 설명합니다.
- 강화학습을 정답 라벨 문제로 오해하지 않도록 보상(reward)과 라벨(label)을 구분합니다.
- 에이전트(agent), 환경(environment), 상태(state), 행동(action), 보상(reward), 정책(policy)을 입문 수준에서 소개합니다.
- 게임 사례만으로 강화학습을 일반화하지 않도록 로봇, 추천, 재고, 대화형 시스템 예시를 함께 배치합니다.
- MDP, Bellman equation, Q-learning, policy gradient, deep RL은 Part 3 이후 주제로 남깁니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-8-3-evidence/google-ml-glossary.html`, `.tmp/section-8-3-evidence/google-ml-glossary.txt` | agent, environment, policy, reinforcement learning, reward, episode, epsilon greedy policy 설명 |
| OpenAI Spinning Up, `Part 1: Key Concepts in RL` | `.tmp/section-8-3-evidence/openai-spinningup-rl-intro.html`, `.tmp/section-8-3-evidence/openai-spinningup-rl-intro.txt` | agent-environment interaction loop, trial and error, state/observation, action space, policy, reward/return 설명 |
| Poole & Mackworth, `Artificial Intelligence: Foundations of Computational Agents`, Chapter 12 | `.tmp/section-8-3-evidence/poole-mackworth-ch12-planning-uncertainty.html`, `.tmp/section-8-3-evidence/poole-mackworth-ch12-planning-uncertainty.txt` | uncertainty 아래의 planning, reacting, observing, preferences, sequential decisions 배경 |
| `docs/parts/part-01/chapter-08/section-01.md` | 저장소 본문 | 라벨(label), 라벨링(labeling), 지도학습의 신호 경계 |
| `docs/parts/part-01/chapter-08/section-02.md` | 저장소 본문 | 라벨 없는 데이터와 구조 찾기의 경계 |
| `docs/parts/part-01/chapter-05/section-01.md` | 저장소 본문 | 학습 유형별 경험과 신호 구분 |

## 확인한 원문 위치

- `.tmp/section-8-3-evidence/google-ml-glossary.txt`
  - agent가 policy를 사용하고 states/environment를 관찰한다는 설명: 1116-1127행 부근
  - environment가 agent를 포함하고 state를 관찰하게 하며 action 이후 state가 전이된다는 설명: 4512-4522행 부근
  - episode 설명: 4531-4535행 부근
  - epsilon greedy policy에서 random policy와 greedy policy, exploration/exploitation 흐름: 4577-4589행 부근
  - reinforcement learning, reward, state, action, environment 요약: 11763-11777행 부근
  - return이 delayed rewards를 discount한다는 설명: 11904-11917행 부근
- `.tmp/section-8-3-evidence/openai-spinningup-rl-intro.txt`
  - 강화학습을 trial and error로 소개하는 설명: 174-180행 부근
  - agent-environment interaction loop와 state/observation/action/reward 설명: 197-207행 부근
  - action space 설명: 238-246행 부근
  - policy가 action을 결정하는 규칙이라는 설명: 251-256행 부근
  - reward function과 cumulative reward/return 설명: 448-479행 부근
  - stochastic transition/policy와 trajectory 확률 설명: 477-488행 부근
  - MDP가 표준 수학 형식이라는 설명: 585-602행 부근
- `.tmp/section-8-3-evidence/poole-mackworth-ch12-planning-uncertainty.txt`
  - 불확실성 아래에서 agent가 환경에 반응하도록 계획해야 한다는 설명: 39-74행 부근
  - agent ability, beliefs/observations, preferences가 의사결정 요소라는 설명: 75-111행 부근
  - Sequential Decisions 제목 확인: 122행 부근

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 강화학습은 행동의 결과에서 배운다 | OpenAI Spinning Up의 trial and error, agent-environment loop | 유지 |
| agent, environment, state, action, reward, policy가 기본 구성요소다 | Google Glossary와 OpenAI Spinning Up의 용어 설명 | 유지 |
| reward는 supervised learning의 label과 다르다 | 8.1의 label 정의와 RL 자료의 action 이후 reward 구조 비교 | 유지. 직접 동일 문구 근거보다 개념 경계 일반화 |
| policy는 상태에서 행동을 고르는 방식이다 | Google Glossary의 state-action mapping, OpenAI Spinning Up의 action decision rule | 유지 |
| delayed reward가 강화학습을 어렵게 만든다 | Google Glossary의 return/delayed rewards, Spinning Up의 cumulative reward/return | 유지 |
| exploration과 exploitation의 균형이 중요하다 | Google Glossary의 epsilon greedy policy 설명 | 유지 |
| 게임 예시는 유용하지만 강화학습 전체를 대표하지 않는다 | Spinning Up의 Atari/Go/robot action space 예시와 Poole & Mackworth의 planning under uncertainty | 유지. 게임 외 예시를 함께 배치 |
| deep RL과 RLHF는 강화학습 전체와 같은 말이 아니다 | 기존 5.1, 8.1, 8.2의 분류축 경계 | 유지 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 8.1 | 사람이 붙인 라벨과 지도학습의 구조 |
| 8.2 | 라벨 없는 데이터에서 구조, 군집, 표현을 찾는 비지도학습 |
| 8.3 | 행동, 보상, 정책을 중심으로 강화학습의 문제 설정 설명 |
| Part 3 | MDP, Bellman equation, Q-learning, policy gradient, 평가와 구현 |
| Part 5 | RLHF와 LLM 정렬(alignment) 맥락 |

## 보수화한 표현

- “보상은 정답이다”라고 쓰지 않았습니다. 보상은 행동 결과에 대한 피드백 신호로 제한했습니다.
- “강화학습은 사람처럼 시행착오로 생각한다”라고 쓰지 않았습니다. 시행착오는 agent-environment interaction을 이해하기 위한 입문 표현으로만 사용했습니다.
- “게임 AI가 강화학습의 본질이다”라고 쓰지 않았습니다. 게임은 설명하기 쉬운 예시일 뿐이며 로봇, 추천, 재고, 대화형 시스템 예시를 함께 배치했습니다.
- “보상을 높이면 언제나 좋은 AI가 된다”라고 쓰지 않았습니다. 보상 설계가 잘못되면 원하지 않는 행동이 생길 수 있다고 제한했습니다.
- “딥러닝과 강화학습은 같은 분류”라고 쓰지 않았습니다. 딥러닝은 강화학습과 결합될 수 있는 모델링 방식으로만 설명했습니다.
- RLHF는 현대 LLM 장에서 다룰 주제로 남기고, 8.3의 중심 설명으로 삼지 않았습니다.

## 남은 검토 사항

- Part 3에서 MDP, value function, Bellman equation, Q-learning, policy gradient를 수식과 예제로 다시 다룹니다.
- RLHF는 LLM 장에서 human feedback, preference data, alignment와 함께 별도 근거를 확보해야 합니다.
- 보상 설계와 안전 문제는 AI 윤리, 보안, 운영 장과 연결해야 합니다.

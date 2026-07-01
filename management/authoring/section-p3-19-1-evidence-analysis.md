# P3-19.1 가치 기반 강화학습 근거 메모

## Section 역할

- Part 3 Module 2 Chapter 19의 첫 번째 절입니다.
- P3-2.3에서 소개한 강화학습의 기본 구조를 이어 받아, 가치 기반 강화학습(value-based reinforcement learning)의 첫 입문 설명을 담당합니다.
- 초심자가 Q-learning과 SARSA를 처음 구분할 수 있도록, 정책(policy)보다 `가치(value)를 먼저 배운다`는 관점을 정리하는 절입니다.

## 핵심 주장

1. 가치 기반 강화학습은 상태나 상태-행동 쌍의 장기적 좋음을 값으로 추정하면서 행동 기준을 만들어 가는 접근으로 설명할 수 있다.
2. 행동을 실제로 고르려면 상태 가치(state value)보다 행동 가치(action value), 즉 Q-value 관점이 더 직접적이다.
3. Q-learning은 다음 상태에서 가장 큰 행동 가치 추정을 기준으로 현재 값을 업데이트하는 오프-정책(off-policy) TD control 알고리즘으로 설명할 수 있다.
4. SARSA는 다음 상태에서 실제로 선택한 행동의 가치를 기준으로 현재 값을 업데이트하는 온-정책(on-policy) TD control 알고리즘으로 설명할 수 있다.
5. 초심자 설명에서는 수렴 증명보다 `best-looking next action`과 `actual next action`의 차이를 먼저 보여 주는 편이 적절하다.

## 근거 출처

### 1) Sutton and Barto - Reinforcement Learning: An Introduction

- 문서: `Reinforcement Learning: An Introduction`, 2nd ed.
- 기관/출판: The MIT Press
- URL: https://mitpress.mit.edu/9780262039246/reinforcement-learning/
- 확인 날짜: 2026-06-27

### 2) Watkins and Dayan - Q-learning

- 문서: `Q-learning`
- 저자: Christopher J. C. H. Watkins, Peter Dayan
- 매체: Machine Learning, 1992
- URL: https://link.springer.com/article/10.1007/BF00992698
- 확인 날짜: 2026-06-27

### 3) Singh et al. - Single-Step On-Policy RL Algorithms

- 문서: `Convergence Results for Single-Step On-Policy Reinforcement-Learning Algorithms`
- 저자: Satinder Singh, Tommi Jaakkola, Michael L. Littman, Csaba Szepesvari
- 매체: Machine Learning, 2000
- URL: https://link.springer.com/article/10.1023/A:1022689125041
- 확인 날짜: 2026-06-27

## 제외한 내용

- Bellman optimality equation의 유도
- TD(0), Monte Carlo, eligibility trace 비교
- epsilon-greedy, softmax exploration 구현 세부
- DQN, replay buffer, target network
- continuous action space 문제

이 내용은 P3-19.2, P3-19.3 또는 후속 딥러닝 파트에서 확장할 수 있습니다.

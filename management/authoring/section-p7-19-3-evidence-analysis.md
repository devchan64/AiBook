# P3-19.3 강화학습 적용의 주의점 근거 메모

## Section 역할

- Part 3 Module 2 Chapter 19의 세 번째 절입니다.
- P3-19.1, P3-19.2에서 본 알고리즘 관점을 실제 적용 조건으로 다시 묶어 주는 정리 절입니다.
- 초심자가 강화학습을 `스스로 시도하며 배우는 강력한 방법`으로만 읽지 않도록, 보상 설계, 탐험 비용, sim-to-real gap을 입문 수준에서 정리합니다.

## 핵심 주장

1. 강화학습의 보상(reward)은 진짜 목표(true objective)의 대리 변수(proxy)일 수 있으며, 둘이 어긋나면 reward hacking 같은 문제가 생길 수 있다.
2. 강화학습의 탐험(exploration)은 현실 환경에서 비용, 안전, 법적 책임 문제를 만들 수 있어 별도의 안전한 탐험 문제가 된다.
3. 시뮬레이션에서 학습한 정책은 현실 환경의 잡음, 동역학 차이, 관측 차이 때문에 그대로 성능이 유지되지 않을 수 있다.
4. 실제 적용에서는 알고리즘 비교보다 먼저 목표 정의, 실험 가능성, 배포 환경 차이를 점검해야 한다.

## 근거 출처

### 1) Sutton and Barto - Reinforcement Learning: An Introduction

- 문서: `Reinforcement Learning: An Introduction`, 2nd ed.
- 기관/출판: The MIT Press
- URL: https://mitpress.mit.edu/9780262039246/reinforcement-learning/
- 확인 날짜: 2026-06-28

### 2) Amodei et al. - Concrete Problems in AI Safety

- 문서: `Concrete Problems in AI Safety`
- 저자: Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, Dan Mané
- 매체: arXiv, 2016
- URL: https://arxiv.org/abs/1606.06565
- 확인 날짜: 2026-06-28

### 3) Zhao et al. - Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey

- 문서: `Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey`
- 저자: Wenshuai Zhao, Jorge Peña Queralta, Tomi Westerlund
- 매체: arXiv, 2020
- URL: https://arxiv.org/abs/2009.13303
- 확인 날짜: 2026-06-28

## 제외한 내용

- inverse reinforcement learning
- constrained RL
- offline RL
- domain randomization 세부 기법
- 현실 배포용 감시 장치와 rollback 시스템의 구현

이 내용은 후속 심화 파트나 프로젝트 파트에서 다시 다룰 수 있습니다.

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
- 반영 포인트:
  - exploration/exploitation tradeoff의 기본 위치
  - 강화학습이 실제 환경과 상호작용하는 학습이라는 기본 전제

### 2) Amodei et al. - Concrete Problems in AI Safety

- 문서: `Concrete Problems in AI Safety`
- 저자: Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, Dan Mané
- 매체: arXiv, 2016
- URL: https://arxiv.org/abs/1606.06565
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - reward hacking
  - safe exploration
  - objective misspecification을 실제 AI 안전 문제로 다루는 기준

### 3) Zhao et al. - Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey

- 문서: `Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey`
- 저자: Wenshuai Zhao, Jorge Peña Queralta, Tomi Westerlund
- 매체: arXiv, 2020
- URL: https://arxiv.org/abs/2009.13303
- 확인 날짜: 2026-06-28
- 반영 포인트:
  - 실제 로봇 학습의 비용과 위험
  - simulation training의 필요성
  - sim-to-real gap을 별도 핵심 문제로 다루는 현대 강화학습 맥락

## 집필 판단

- 이 절은 수학이나 알고리즘보다 `현실 적용에서 왜 바로 막히는가`를 설명하는 절로 설계했습니다.
- reward hacking은 초심자가 즉시 이해할 수 있도록 클릭 수와 불만 비용의 간단한 대리 변수 예제로 풀었습니다.
- safe exploration은 별도 알고리즘 소개보다 `현실에서는 실패 자체가 비싸다`는 감각을 우선했습니다.
- sim-to-real gap은 로봇 분야 사례를 중심으로 설명하되, 더 일반적으로 `훈련 세계와 배포 세계가 다를 수 있다`는 문장으로 일반화했습니다.

## 제외한 내용

- inverse reinforcement learning
- constrained RL
- offline RL
- domain randomization 세부 기법
- 현실 배포용 감시 장치와 rollback 시스템의 구현

이 내용은 후속 심화 파트나 프로젝트 파트에서 다시 다룰 수 있습니다.

# P3-19.2 정책 기반 강화학습 근거 메모

## Section 역할

- Part 3 Module 2 Chapter 19의 두 번째 절입니다.
- P3-19.1의 가치 기반 강화학습 다음에, 정책(policy)을 직접 조정하는 강화학습 관점을 소개합니다.
- policy gradient, REINFORCE, actor-critic을 초심자가 처음 구분할 수 있도록 준비하는 절입니다.

## 핵심 주장

1. 정책 기반 강화학습은 상태-행동 가치 표를 먼저 완성하기보다 정책 파라미터를 직접 조정해 기대 보상을 높이는 접근으로 설명할 수 있다.
2. REINFORCE는 보상이 좋았던 행동의 확률을 높이는 방향으로 정책을 조정하는 대표적인 초기 policy gradient 알고리즘으로 소개할 수 있다.
3. actor-critic은 정책을 조정하는 actor와 평가 신호를 주는 critic을 분리해 정책 기반 접근의 변동을 줄이려는 구조로 설명할 수 있다.
4. 정책 기반 접근은 연속 행동이나 복잡한 확률적 정책을 다루는 문제에서 더 자연스럽게 읽히는 경우가 많다.
5. 초심자 설명에서는 정책 기반 접근을 `행동 분포를 직접 출력하거나 조정하는 관점`으로 풀어 쓰는 것이 유용하다.

## 근거 출처

### 1) Sutton and Barto - Reinforcement Learning: An Introduction

- 문서: `Reinforcement Learning: An Introduction`, 2nd ed.
- 기관/출판: The MIT Press
- URL: https://mitpress.mit.edu/9780262039246/reinforcement-learning/
- 확인 날짜: 2026-06-27

### 2) Williams 1992 - REINFORCE

- 문서: `Simple statistical gradient-following algorithms for connectionist reinforcement learning`
- 저자: Ronald J. Williams
- 매체: Machine Learning, 1992
- URL: https://link.springer.com/article/10.1007/BF00992696
- 확인 날짜: 2026-06-27

### 3) Sutton et al. 1999 - Policy Gradient with Function Approximation

- 문서: `Policy Gradient Methods for Reinforcement Learning with Function Approximation`
- 저자: Richard S. Sutton, David McAllester, Satinder Singh, Yishay Mansour
- 매체: NeurIPS 1999
- URL: https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html
- 확인 날짜: 2026-06-27

### 4) Konda and Tsitsiklis - On Actor-Critic Algorithms

- 문서: `On Actor-Critic Algorithms`
- 저자: Vijay R. Konda, John N. Tsitsiklis
- 매체: SIAM Journal on Control and Optimization, 2003
- URL: https://doi.org/10.1137/S0363012901385691
- 확인 날짜: 2026-06-27

## 제외한 내용

- policy gradient theorem 유도
- baseline subtraction의 엄밀한 설명
- advantage function의 수학적 정의
- PPO, TRPO, SAC, DDPG 같은 후속 알고리즘 비교
- 연속 제어의 실제 실험 코드

이 내용은 후속 Part 4, Part 5 또는 별도 심화 파트에서 확장할 수 있습니다.

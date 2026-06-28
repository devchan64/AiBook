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
- 반영 포인트:
  - policy gradient와 actor-critic을 강화학습의 표준 범주로 설명하는 교과서적 기준
  - 가치 함수와 정책 직접 최적화의 역할 구분

### 2) Williams 1992 - REINFORCE

- 문서: `Simple statistical gradient-following algorithms for connectionist reinforcement learning`
- 저자: Ronald J. Williams
- 매체: Machine Learning, 1992
- URL: https://link.springer.com/article/10.1007/BF00992696
- 확인 날짜: 2026-06-27
- 반영 포인트:
  - 대표적인 초기 policy gradient 계열 알고리즘의 역사적 기준
  - 보상이 좋았던 행동 경향을 강화하는 직관의 학술적 뿌리

### 3) Sutton et al. 1999 - Policy Gradient with Function Approximation

- 문서: `Policy Gradient Methods for Reinforcement Learning with Function Approximation`
- 저자: Richard S. Sutton, David McAllester, Satinder Singh, Yishay Mansour
- 매체: NeurIPS 1999
- URL: https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html
- 확인 날짜: 2026-06-27
- 반영 포인트:
  - policy gradient를 함수 근사와 연결하는 대표 논문
  - 현대 딥 강화학습으로 이어지는 연결 고리

### 4) Konda and Tsitsiklis - On Actor-Critic Algorithms

- 문서: `On Actor-Critic Algorithms`
- 저자: Vijay R. Konda, John N. Tsitsiklis
- 매체: SIAM Journal on Control and Optimization, 2003
- URL: https://doi.org/10.1137/S0363012901385691
- 확인 날짜: 2026-06-27
- 반영 포인트:
  - actor-critic을 정책과 평가의 역할 분리 구조로 다루는 학술 기준

## 집필 판단

- 이 절은 policy gradient 공식을 전면에 두지 않고, `정책을 직접 만진다`는 관점을 먼저 잡았습니다.
- REINFORCE는 세부 수식보다 `좋았던 행동 확률을 높인다`는 직관을 보여 주는 예로 사용했습니다.
- actor-critic은 A2C/A3C/PPO 같은 현대 변형보다 먼저, actor와 critic의 역할 차이를 설명하는 기본 구조로 제한했습니다.
- Python 예제는 엄밀한 gradient estimator가 아니라, 정책 점수와 확률이 보상 신호에 따라 어떻게 바뀌는지 보여 주는 장난감 예제로 제한했습니다.
- 사례 보강에서는 로봇 제어, 이동체 조향, 확률적 전술 선택처럼 `연속 행동`과 `행동 분포 직접 표현`의 장점이 드러나는 장면을 추가했습니다.

## 제외한 내용

- policy gradient theorem 유도
- baseline subtraction의 엄밀한 설명
- advantage function의 수학적 정의
- PPO, TRPO, SAC, DDPG 같은 후속 알고리즘 비교
- 연속 제어의 실제 실험 코드

이 내용은 후속 Part 4, Part 5 또는 별도 심화 파트에서 확장할 수 있습니다.

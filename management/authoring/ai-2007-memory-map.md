# 2007년 AI 학습 기억의 일반화

## 목적

이 문서는 사용자가 2007년 무렵 인공지능을 학습하며 기억한 흐름을 표준적인 AI 역사 설명과 연결하기 위한 관리 메모입니다.

이 내용은 현재 1.1절 `AI라는 말의 범위`에 길게 넣지 않습니다. 주로 다음 Section과 Chapter로 분리해 다룹니다.

- Chapter 2. AI의 역사와 패러다임 변화
- Chapter 7. 탐색과 휴리스틱
- Chapter 8. 지도학습, 비지도학습, 강화학습
- Chapter 9. 딥러닝 패러다임의 확산
- Chapter 11. LLM은 어디에서 왔는가

## 사용자의 기억

사용자는 2007년 무렵 AI를 학습할 때 다음과 같이 기억하고 있습니다.

- 휴리스틱(heuristic) 기반 접근이 중요한 기반에 있었다.
- 강화학습(reinforcement learning)이 유행하던 시기로 기억한다.
- 시냅스 기반의 인공지능, 즉 신경망(neural network) 계열 AI가 시작되던 시기로 기억한다.
- 이 구분은 비슷하지만 다른 AI 접근들을 설명하는 기준으로 남아 있다.

## 표준 설명으로 보정한 요약

이 기억은 다음처럼 보정할 수 있습니다.

> 2007년 전후의 AI 학습 환경에서는 여전히 탐색(search), 휴리스틱(heuristics), 지식 표현(knowledge representation), 확률적 추론(probabilistic reasoning), 머신러닝(machine learning), 강화학습(reinforcement learning)이 함께 다뤄졌다. 신경망(neural networks)은 새로 시작된 분야가 아니라 오래된 연구 전통이었지만, 2006년 전후 딥 빌리프 네트워크(deep belief networks)와 표현 학습(representation learning) 연구를 계기로 딥러닝(deep learning) 부흥의 초기 신호가 나타났다. 대중적·산업적 전환점은 2012년 이후 이미지 인식과 음성 인식 성과를 통해 더 뚜렷해졌다.

## 세 접근의 차이

| 접근 | 중심 질문 | 대표 표현 | 2007년 전후 위치 |
| --- | --- | --- | --- |
| 탐색과 휴리스틱 | 가능한 해가 너무 많을 때 어디부터 볼 것인가 | search, heuristic search, planning | 전통 AI 개론의 핵심 축 |
| 강화학습 | 행동의 결과가 나중에 보상으로 돌아올 때 어떻게 배울 것인가 | agent, state, action, reward, policy | 이미 확립된 연구 분야였고, 교재와 연구에서 중요하게 다뤄짐 |
| 신경망과 딥러닝 | 데이터에서 표현과 가중치를 어떻게 학습할 것인가 | neural network, weights, representation, deep learning | 신경망은 오래된 분야, 딥러닝은 2006년 전후 부흥 초기 |

## 휴리스틱은 무엇이었나

휴리스틱은 “불확실성을 확률로 직접 모델링한다”기보다, 탐색 공간(search space)이 너무 커서 모든 가능성을 계산할 수 없을 때 더 그럴듯한 후보를 먼저 보게 해주는 경험적 기준입니다.

예를 들어 게임, 퍼즐, 경로 찾기, 계획 문제에서 가능한 다음 상태를 모두 탐색하면 계산량이 폭발합니다. 휴리스틱은 이때 “정답을 보장하지는 않지만, 좋은 방향으로 탐색을 줄이는 규칙”으로 쓰입니다.

따라서 사용자의 “불확실성을 소프트웨어에 반영하려는 시도”라는 직관은 일부 맞습니다. 다만 표준적으로는 다음처럼 나누는 것이 안전합니다.

- 휴리스틱: 계산 한계 때문에 탐색을 줄이는 경험적 판단 기준
- 확률 모델: 불확실성을 수학적으로 표현하고 추론하는 모델
- 강화학습: 시행착오와 보상으로 행동 정책을 학습하는 틀
- 딥러닝: 많은 데이터에서 표현과 가중치를 학습하는 신경망 기반 방법

## 강화학습은 왜 기억에 남았나

강화학습은 1990년대에 이미 중요한 연구 분야로 정리되어 있었습니다. Sutton과 Barto의 `Reinforcement Learning: An Introduction` 초판은 1998년에 출간되었고, 2000년대 AI·머신러닝 학습에서 강화학습은 에이전트(agent), 상태(state), 행동(action), 보상(reward), 정책(policy)을 설명하는 대표 틀이었습니다.

다만 2007년의 강화학습은 지금 대중에게 알려진 “딥 강화학습(deep reinforcement learning)”의 전성기와는 다릅니다. 딥러닝과 결합해 Atari, AlphaGo 같은 사례로 널리 알려진 흐름은 2010년대에 더 뚜렷해졌습니다.

## 시냅스 기반 AI라는 기억의 보정

“시냅스 기반 AI”라는 표현은 신경망의 가중치(weights)를 생물학적 시냅스(synapse)에 비유한 기억으로 볼 수 있습니다.

하지만 신경망 연구는 2007년에 시작된 것이 아닙니다. 퍼셉트론(perceptron), 역전파(backpropagation), 연결주의(connectionism)는 그보다 훨씬 이전부터 존재했습니다. 2007년 전후에 새로웠던 것은 “깊은 층을 가진 신경망을 더 잘 학습할 수 있을 것 같다”는 딥러닝 부흥의 초기 흐름입니다.

2006년 Hinton, Osindero, Teh의 딥 빌리프 네트워크 연구는 여러 은닉층을 가진 모델을 층별로 학습하는 빠른 방법을 제시했고, 이후 표현 학습과 딥러닝 흐름의 중요한 전환점으로 자주 언급됩니다.

## 책에서 사용할 설명 방향

책에서는 이 기억을 다음 구조로 일반화합니다.

1. 전통 AI는 탐색, 규칙, 지식 표현, 휴리스틱을 통해 문제를 풀려고 했다.
2. 확률적 추론은 불확실한 정보를 수학적으로 다루는 별도 축으로 발전했다.
3. 머신러닝은 사람이 규칙을 모두 쓰기보다 데이터에서 관계를 학습하는 방향을 강화했다.
4. 강화학습은 환경과 상호작용하면서 보상을 최대화하는 행동 방식을 학습하는 틀을 제공했다.
5. 신경망과 딥러닝은 데이터에서 표현(representation)과 가중치(weights)를 학습하는 흐름을 크게 확장했다.
6. LLM은 이 중 딥러닝, 표현 학습, 대규모 데이터, 병렬 계산, 언어 모델링의 흐름 위에서 등장했다.

## 주의할 표현

| 피할 표현 | 이유 | 권장 표현 |
| --- | --- | --- |
| 2007년에 시냅스 기반 AI가 시작되었다 | 신경망 연구는 훨씬 이전부터 존재 | 2006년 전후 딥러닝 부흥의 초기 신호가 나타났다 |
| 휴리스틱은 확률이다 | 휴리스틱과 확률 모델은 다름 | 휴리스틱은 탐색을 줄이는 경험적 기준이고, 확률 모델은 불확실성을 수학적으로 표현한다 |
| 강화학습이 2007년에 처음 유행했다 | RL은 1990년대 이전부터 연구됨 | 2000년대 AI 학습에서 강화학습은 중요한 축으로 다뤄졌다 |
| 딥러닝은 LLM으로 바로 이어졌다 | 중간에 CNN, 음성 인식, seq2seq, attention, Transformer 등 여러 계보가 있음 | LLM은 딥러닝 확산과 NLP 계보가 만난 결과로 설명한다 |

## 출처와 참고 자료

- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed.](https://aima.cs.berkeley.edu/), 확인 날짜: 2026-06-22.
- Geoffrey E. Hinton, Simon Osindero, Yee-Whye Teh, [A fast learning algorithm for deep belief nets](https://www.cs.toronto.edu/~hinton/absps/fastnc.pdf), Neural Computation, 2006, 확인 날짜: 2026-06-22.
- Yann LeCun, Yoshua Bengio, Geoffrey Hinton, [Deep learning](https://www.nature.com/articles/nature14539), Nature, 2015-05-27, 확인 날짜: 2026-06-22.
- L. P. Kaelbling, M. L. Littman, A. W. Moore, [Reinforcement Learning: A Survey](https://arxiv.org/abs/cs/9605103), 1996, 확인 날짜: 2026-06-22.
- Richard S. Sutton, Andrew G. Barto, `Reinforcement Learning: An Introduction`, MIT Press, 1998.

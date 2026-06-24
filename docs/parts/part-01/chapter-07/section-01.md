# 7.1 탐색 공간(search space)과 계산 한계(computational limit)

6장에서는 불완전한 정보와 확률적 판단을 다뤘습니다. 이제 다른 종류의 어려움을 봅니다. 어떤 문제는 정보가 부족해서 어렵기도 하지만, 가능한 선택지가 너무 많아서 어렵기도 합니다.

이 절의 질문은 다음입니다.

```text
가능한 해가 너무 많을 때,
AI는 무엇을 모두 살펴볼 수 없게 되는가?
```

이 질문이 Chapter 7의 출발점입니다. 휴리스틱(heuristic)을 이해하려면 먼저 탐색(search)과 탐색 공간(search space)을 이해해야 합니다.

> 후보가 많아지는 순간, 문제는 정답을 아는 일이 아니라 정답을 찾아가는 일이 된다.

## 이 절의 범위

7.1은 탐색 알고리즘을 계산하지 않습니다. 너비 우선 탐색(breadth-first search), 깊이 우선 탐색(depth-first search), A* 탐색(A* search)은 여기서 구현하지 않습니다.

또한 휴리스틱 함수(heuristic function)를 본격적으로 설명하지 않습니다. 휴리스틱은 7.2에서 다룹니다.

여기서는 다음 관점만 잡습니다.

```text
문제를 풀 때 가능한 상태와 선택지가 너무 많아지면
모든 경우를 살펴보는 방식은 곧 한계에 부딪힌다.
```

## 목표

- 탐색(search)을 “가능한 후보를 살펴보며 해를 찾는 과정”으로 이해합니다.
- 상태(state), 행동(action), 목표(goal), 경로(path), 비용(cost)을 입문 수준에서 구분합니다.
- 탐색 공간(search space)이 커질 때 계산 한계(computational limit)가 왜 생기는지 이해합니다.
- 가능한 모든 경우를 살펴보는 완전 탐색(exhaustive search)이 왜 현실적으로 어려워지는지 설명할 수 있습니다.
- 7.2의 휴리스틱(heuristic)이 왜 필요한지 준비합니다.

## 탐색(search)은 후보를 살펴보는 문제 해결 방식이다

Poole과 Mackworth는 에이전트가 목표를 달성하는 방법을 찾는 문제를 그래프(graph)에서 시작 노드(start node)에서 목표 노드(goal node)까지의 경로(path)를 찾는 문제로 추상화할 수 있다고 설명합니다. AIMA도 문제 해결(problem solving)과 탐색(search)을 AI 개론의 초반 핵심 주제로 배치합니다.

Poole과 Mackworth는 이 흐름을 짧게 이렇게 표현합니다.

> “Search underlies much of AI.”  
> — David L. Poole, Alan K. Mackworth, *Artificial Intelligence: Foundations of Computational Agents*

입문 단계에서는 탐색을 이렇게 이해하면 됩니다.

```text
지금 상태에서 가능한 선택을 따라가며
목표에 도달하는 경로를 찾는 과정
```

예를 들어 길 찾기를 생각해 봅니다.

| 요소 | 길 찾기 예시 |
| --- | --- |
| 상태(state) | 현재 위치 |
| 행동(action) | 다음 길로 이동 |
| 목표(goal) | 목적지 도착 |
| 경로(path) | 거쳐 간 도로와 교차로의 순서 |
| 비용(cost) | 거리, 시간, 요금, 에너지 |

이 구조는 길 찾기에만 쓰이지 않습니다. 일정 짜기, 퍼즐 풀기, 게임 수 읽기, 코드 수정 순서 정하기, 문서 목차 후보 비교에도 비슷한 관점을 적용할 수 있습니다.

## 탐색 공간(search space)은 가능한 상태와 선택지의 전체다

탐색 공간(search space)은 문제를 풀 때 고려할 수 있는 상태(state)와 이동(action)의 전체 구조입니다.

간단한 예시를 봅니다.

```text
아침에 할 일을 정한다.
후보: 운동, 독서, 이메일 확인
그다음 후보: 출근, 회의 준비, 장보기
```

처음 선택지가 3개이고, 그다음 선택지도 3개라면 가능한 조합은 9개입니다. 선택 단계가 늘어나면 후보는 빠르게 커집니다.

| 단계 수 | 각 단계 선택지 3개일 때 가능한 조합 |
| ---: | ---: |
| 1 | 3 |
| 2 | 9 |
| 3 | 27 |
| 4 | 81 |
| 5 | 243 |
| 10 | 59,049 |

이 표는 수학을 깊게 하려는 것이 아닙니다. 중요한 감각은 이것입니다.

> 선택지가 조금씩만 늘어도 가능한 조합은 빠르게 커진다.

이런 증가 때문에 “전부 살펴보면 되지 않을까?”라는 생각은 곧 어려워집니다.

## 완전 탐색(exhaustive search)은 왜 어려워지는가

완전 탐색(exhaustive search)은 가능한 경우를 빠짐없이 살펴보는 방식입니다. 작은 문제에서는 좋은 기준이 될 수 있습니다. 하지만 후보가 많아지면 시간과 메모리가 빠르게 부족해집니다.

예를 들어 다음 문제들을 생각해 봅니다.

| 문제 | 가능한 후보가 커지는 이유 |
| --- | --- |
| 배송 경로 | 방문할 지점 순서가 많아짐 |
| 회의 일정 | 사람, 시간대, 회의실 조건이 얽힘 |
| 체스나 바둑 | 매 수마다 다음 가능한 수가 많음 |
| 문서 작성 | 목차, 문장, 예시, 근거 배치 후보가 많음 |
| 모델 튜닝 | 모델 종류, 특징, 하이퍼파라미터 조합이 많음 |

Poole과 Mackworth는 검색의 어려움이 문제 해결의 핵심이며, 효율적으로 해를 알아볼 수 있어도 효율적으로 찾는 방법이 없는 문제가 존재한다고 설명합니다. 여기서 중요한 점은 “정답을 확인하는 일”과 “정답을 찾는 일”이 다를 수 있다는 것입니다.

예를 들어 어떤 퍼즐의 완성 상태를 보면 정답인지 확인하기는 쉽습니다. 하지만 그 완성 상태에 도달하는 순서를 찾는 일은 어려울 수 있습니다.

> 해를 알아보는 것은 쉬울 수 있다. 해를 찾아가는 것은 어려울 수 있다.

## 계산 한계(computational limit)는 단순히 컴퓨터가 느리다는 뜻이 아니다

계산 한계(computational limit)는 컴퓨터 성능이 부족하다는 단순한 불평이 아닙니다. 문제 구조상 가능한 후보가 너무 빠르게 늘어나면, 아무리 빠른 컴퓨터라도 모든 경우를 현실적인 시간 안에 살펴보기 어렵습니다.

다음처럼 구분할 수 있습니다.

| 구분 | 의미 |
| --- | --- |
| 구현이 느림 | 코드를 고치면 빨라질 수 있음 |
| 데이터가 큼 | 저장, 전송, 병렬 처리로 완화할 수 있음 |
| 탐색 공간이 폭발함 | 가능한 후보 자체가 너무 빠르게 늘어남 |
| 목표 기준이 복잡함 | 무엇이 좋은 해인지 평가하기 어려움 |

물리적 성능 향상은 중요합니다. 더 빠른 CPU, GPU, 더 많은 메모리, 병렬 처리(parallel processing)는 더 큰 문제를 다룰 수 있게 합니다. 하지만 성능 향상이 모든 탐색 문제를 없애지는 않습니다.

문제가 커지는 속도가 계산 자원 증가보다 훨씬 빠를 수 있기 때문입니다.

> 더 빠른 컴퓨터는 더 멀리 보게 해 주지만, 모든 길을 다 보게 해 주지는 않는다.

## 현대 사례: AlphaDev와 FunSearch

탐색 공간(search space)과 계산 한계(computational limit)는 오래된 AI 교재에만 남은 표현이 아닙니다. 현대 AI 연구에서도 “무엇을 탐색할 것인가”와 “가능한 후보가 너무 많을 때 어떻게 줄일 것인가”는 계속 등장합니다.

Google DeepMind의 AlphaDev 사례는 탐색 공간이 너무 큰 현대 사례로 볼 수 있습니다. AlphaDev는 더 빠른 정렬 알고리즘을 찾기 위해 어셈블리 명령 조합을 탐색했습니다. DeepMind는 이 문제가 어려운 이유를 다음 구절로 설명합니다.

> “enormous number of possible combinations of instructions”  
> — Google DeepMind, *AlphaDev discovers faster sorting algorithms*

이 문구는 7.1의 탐색 공간 감각과 잘 맞습니다. 가능한 명령 조합이 너무 많으면 모든 조합을 살펴보는 방식은 현실적으로 어렵습니다.

FunSearch는 조금 다른 사례입니다. FunSearch는 정답 하나를 직접 찾기보다, 문제를 푸는 함수(function) 또는 프로그램(program)을 탐색 대상으로 삼습니다.

> “functions written in computer code”  
> — Google DeepMind, *FunSearch: Making new discoveries in mathematical sciences using Large Language Models*

이 사례는 탐색 대상 자체를 바꿀 수 있음을 보여 줍니다. 어떤 문제에서는 해답 후보를 직접 나열하는 대신, 해답을 만들어 내는 프로그램이나 함수를 탐색할 수 있습니다.

다만 이 두 사례는 경계를 분명히 해야 합니다.

| 사례 | 이 절에서 가져오는 의미 | 일반화하면 안 되는 것 |
| --- | --- | --- |
| AlphaDev | 탐색 공간이 매우 커질 수 있고, 가능한 후보를 모두 살펴보기 어렵다는 현대 사례 | 모든 AI 문제가 강화학습으로 알고리즘을 찾는 문제라는 뜻은 아님 |
| FunSearch | 탐색 대상을 해답 자체에서 함수나 프로그램으로 바꿀 수 있다는 현대 사례 | LLM이 학습 데이터에서 정답을 검색해 꺼낸다는 뜻은 아님 |

따라서 이 절에서 두 사례를 사용하는 목적은 제한적입니다.

```text
현대 AI에서도 탐색 공간은 여전히 중요하다.
하지만 탐색의 대상은 상태, 경로, 명령 조합, 함수, 프로그램처럼
문제에 따라 달라질 수 있다.
```

## 탐색은 확률과 다른 어려움을 다룬다

6장에서는 불확실성(uncertainty)과 확률(probability)을 다뤘습니다. 7.1의 탐색(search)은 다른 어려움에서 출발합니다.

| 어려움 | 중심 질문 | 대표 접근 |
| --- | --- | --- |
| 불확실성(uncertainty) | 무엇이 참인지 확실하지 않다 | 확률, 근거 갱신, 보정 |
| 탐색 공간(search space) | 가능한 후보가 너무 많다 | 탐색, 가지치기, 휴리스틱 |
| 학습(learning) | 판단 기준을 사람이 모두 쓰기 어렵다 | 데이터 기반 모델 |

물론 현실 문제에서는 이 셋이 함께 나타납니다. 길 찾기에서도 가능한 경로가 많고, 교통 상황은 불확실하며, 예상 시간은 데이터로 학습될 수 있습니다.

하지만 입문 단계에서는 먼저 구분하는 편이 좋습니다.

```text
모르는 것과,
후보가 너무 많은 것과,
판단 기준을 학습해야 하는 것은
서로 연결되지만 같은 문제가 아니다.
```

## 예시: 문서 목차를 탐색 문제처럼 보기

이 책을 만드는 과정도 탐색 문제처럼 볼 수 있습니다.

| 요소 | 이 책의 작성 예시 |
| --- | --- |
| 상태(state) | 현재까지 작성된 목차와 섹션 |
| 행동(action) | 섹션 추가, 순서 변경, 근거 보강, 표현 수정 |
| 목표(goal) | AI 재학습에 적합한 책 구조 |
| 비용(cost) | 독자 혼란, 근거 부족, 분량 증가, 작성 시간 |
| 제약(constraint) | 근거 중심 작성, 섹션 경계 유지, 한영 병기 |

가능한 목차 조합은 매우 많습니다. 모든 목차 후보를 만들어 비교할 수는 없습니다. 그래서 실제 작업에서는 다음처럼 진행합니다.

> 큰 구조를 먼저 잡고, 한 섹션의 중심 질문을 정한다.  
> 근거가 부족한 표현은 보류하고, 섹션 경계를 넘는 내용은 뒤 장으로 넘긴다.

이것은 엄밀한 탐색 알고리즘은 아닙니다. 하지만 “가능한 후보를 모두 볼 수 없으므로 기준을 두고 줄인다”는 점에서 탐색과 휴리스틱을 이해하는 좋은 비유가 됩니다.

## 왜 휴리스틱(heuristic)이 다음에 필요한가

탐색 공간이 너무 크면 모든 후보를 다 볼 수 없습니다. 그러면 다음 질문이 생깁니다.

```text
어떤 후보를 먼저 볼 것인가?
어떤 후보는 일찍 포기할 것인가?
충분히 좋은 해를 어디에서 멈출 것인가?
```

이 질문이 휴리스틱(heuristic)으로 이어집니다. Poole과 Mackworth는 탐색의 어려움과 사람이 일부 탐색 문제를 효율적으로 푸는 사실이, 컴퓨터 에이전트도 특수한 경우에 대한 지식을 활용해 해를 찾도록 해야 함을 시사한다고 설명합니다. 이런 추가 지식을 휴리스틱 지식(heuristic knowledge)이라고 부릅니다.

다음 절에서는 휴리스틱을 “정답을 보장하지는 않지만 탐색을 줄이는 경험적 기준”으로 다룹니다.

## 이 절에서 기억할 관점

탐색(search)은 가능한 후보를 살펴보며 목표에 도달하는 경로를 찾는 문제 해결 방식입니다. 탐색 공간(search space)이 커지면 모든 후보를 살펴보는 방식은 곧 계산 한계(computational limit)에 부딪힙니다.

그래서 AI는 다음 문제를 다룹니다.

> 가능한 모든 후보를 볼 수 없다면, 무엇을 먼저 보고, 무엇을 줄이고, 어디에서 충분하다고 판단할 것인가?

이 질문이 7.2의 휴리스틱(heuristic)으로 이어집니다.

## 체크리스트

- 탐색(search)을 가능한 후보를 살펴보며 해를 찾는 과정으로 설명할 수 있다.
- 상태(state), 행동(action), 목표(goal), 경로(path), 비용(cost)을 길 찾기 예시로 설명할 수 있다.
- 탐색 공간(search space)이 커질수록 가능한 조합이 빠르게 늘어난다는 점을 설명할 수 있다.
- 완전 탐색(exhaustive search)이 작은 문제에서는 가능하지만 큰 문제에서는 계산 한계에 부딪힌다는 점을 설명할 수 있다.
- 불확실성(uncertainty), 탐색 공간(search space), 학습(learning)의 어려움을 구분할 수 있다.
- 탐색 공간이 커질 때 휴리스틱(heuristic)이 왜 필요해지는지 설명할 수 있다.

## 출처와 참고 자료

- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed., Chapter 3 Searching for Solutions](https://artint.info/3e/html/ArtInt3e.Ch3.html), 확인 날짜: 2026-06-23.
- David L. Poole, Alan K. Mackworth, [3.1 Problem Solving as Search](https://artint.info/3e/html/ArtInt3e.Ch3.S1.html), 확인 날짜: 2026-06-23.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed., Full Table of Contents](https://aima.cs.berkeley.edu/contents.html), 확인 날짜: 2026-06-22.
- Google DeepMind, Daniel J. Mankowitz and Andrea Michi, [AlphaDev discovers faster sorting algorithms](https://deepmind.google/discover/blog/alphadev-discovers-faster-sorting-algorithms/), 2023-06-07, 확인 날짜: 2026-06-23.
- Google DeepMind, Alhussein Fawzi and Bernardino Romera-Paredes, [FunSearch: Making new discoveries in mathematical sciences using Large Language Models](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/), 2023-12-14, 확인 날짜: 2026-06-23.

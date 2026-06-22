# AI 개론 목차 조사

이 문서는 AI 개론 파트의 기준 목차를 만들기 위한 1차 조사 기록입니다. 유명 교재와 공개 강의의 목차를 그대로 복사하지 않고, 반복해서 등장하는 주제를 같은 범주로 묶어 통계화합니다.

## 조사 목적

- AI 개론에서 먼저 다룰 주제를 근거 기반으로 고릅니다.
- 깊은 수학과 구현은 뒤 파트로 미루고, 현재는 역사와 패러다임 변화의 지도를 만드는 데 집중합니다.
- 개인적인 작업 가설과 표준 커리큘럼에서 반복되는 설명을 구분합니다.

## 조사 방식

- 기준일: 2026-06-22
- 방식: 공개된 교재 목차와 대학 강의 주제 목록을 수집한 뒤, 주제의 등장 여부를 수동으로 분류했습니다.
- 단위: 한 자료 안에서 같은 주제가 여러 번 등장해도 1회로 계산했습니다.
- 한계: 표본이 작고, 각 강의의 깊이와 순서는 반영하지 않았습니다. 이 문서는 최종 통계가 아니라 목차 설계를 위한 1차 근거입니다.

서점 순위는 시점에 따라 크게 바뀌며, 검색 결과와 판매 순위의 기준도 공개적으로 일관되지 않을 수 있습니다. 따라서 이번 1차 조사에서는 공식 교재 페이지와 대학/교육기관 공개 강의만 사용합니다.

## 조사 표본

| 구분 | 자료 | 기관 또는 저자 | 확인한 내용 |
| --- | --- | --- | --- |
| 교재 | [Artificial Intelligence: A Modern Approach](https://aima.cs.berkeley.edu/) | Stuart Russell, Peter Norvig | AI, 문제 해결, 지식과 추론, 불확실성, 머신러닝, 지각과 행동, 윤리와 미래 |
| 공개 교재 | [Artificial Intelligence: Foundations of Computational Agents](https://artint.info/3e/html/ArtInt3e.html) | David L. Poole, Alan K. Mackworth | 에이전트, 탐색, 제약, 논리, 계획, 머신러닝, 딥러닝, 불확실성, 강화학습, 사회적 영향 |
| 공개 강의 | [CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/) | Harvard University | 탐색, 지식, 불확실성, 최적화, 학습, 신경망, 언어 |
| 공개 강의 | [CS188: Introduction to Artificial Intelligence](https://inst.eecs.berkeley.edu/~cs188/archive/fa24/) | UC Berkeley | 탐색, CSP, 게임, MDP, 강화학습, 확률, 베이즈 네트워크, HMM, 머신러닝 |
| 공개 강의 | [Artificial Intelligence, MIT 6.034](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/video_galleries/lecture-videos/) | MIT OpenCourseWare | 개론, 규칙 기반 전문가 시스템, 탐색, 게임, 제약, 학습, 신경망, 확률 추론, 표현 |

## 주제 정규화

서로 다른 자료가 같은 주제를 다른 이름으로 부르기 때문에 다음 범주로 묶었습니다.

| 정규화 주제 | 포함한 표현 |
| --- | --- |
| AI 개론, 역사, 에이전트 | AI 정의, intelligent agent, scope, AI의 분야와 역사 |
| 탐색과 문제 해결 | search, problem solving, A*, graph search |
| 지식 표현, 논리, 규칙 기반 AI | knowledge, reasoning, logic, rule-based expert systems |
| 제약과 최적화 | CSP, constraints, optimization |
| 게임과 적대적 탐색 | game tree, adversarial search |
| 불확실성과 확률 추론 | probability, Bayesian networks, HMM, uncertain reasoning |
| 계획과 의사결정 | planning, MDP, decision network |
| 머신러닝 | supervised learning, classification, learning |
| 신경망과 딥러닝 | neural networks, deep learning |
| 강화학습 | reinforcement learning |
| 언어, NLP, LLM | language, natural language, LLM |
| 지각, 비전, 로봇, 행동 | perception, vision, robotics, acting |
| 윤리, 사회적 영향, 미래 | social impact, ethics, safety, future |

## 1차 통계

| 순위권 | 정규화 주제 | 등장 수 | 해석 |
| --- | --- | ---: | --- |
| 1위권 | AI 개론, 역사, 에이전트 | 5/5 | AI 개론의 출발점입니다. 정의보다 먼저 "어떤 문제를 다루는 분야인가"를 보여줘야 합니다. |
| 1위권 | 탐색과 문제 해결 | 5/5 | 초기 AI와 현대 AI를 연결하는 핵심 역사 주제입니다. |
| 1위권 | 불확실성과 확률 추론 | 5/5 | 규칙과 논리만으로 설명하기 어려운 세계를 다루는 전환점입니다. |
| 1위권 | 머신러닝 | 5/5 | 현대 AI로 넘어가는 중심 축입니다. |
| 2위권 | 지식 표현, 논리, 규칙 기반 AI | 4/5 | 규칙 기반 AI와 상징주의를 이해하는 데 필요합니다. |
| 2위권 | 제약과 최적화 | 4/5 | 탐색, 문제 해결, 학습을 잇는 계산 관점입니다. |
| 2위권 | 게임과 적대적 탐색 | 4/5 | 초기 AI 성과와 탐색 알고리즘을 설명하는 좋은 역사 사례입니다. |
| 2위권 | 계획과 의사결정 | 4/5 | 에이전트가 행동을 고르는 문제로 AI를 이해하게 합니다. |
| 3위권 | 신경망과 딥러닝 | 3/5 | 개론에서는 역사와 위치만 잡고, 깊은 내용은 딥러닝 파트로 넘깁니다. |
| 3위권 | 강화학습 | 3/5 | 에이전트, 의사결정, 보상 개념을 연결합니다. |
| 3위권 | 언어, NLP, LLM | 2/5 | 최근 AI 경험과 연결되지만, 전통 개론 목차에서는 후반 주제로 다뤄지는 경향이 있습니다. |
| 3위권 | 지각, 비전, 로봇, 행동 | 2/5 | AI가 텍스트 모델만이 아니라 세계를 지각하고 행동하는 시스템이라는 점을 보여줍니다. |
| 3위권 | 윤리, 사회적 영향, 미래 | 2/5 | 개론 끝에서 다루되, 예측성 내용은 반드시 외부 근거를 붙입니다. |

## 목차 설계에 주는 의미

이번 조사만 보면 AI 개론의 첫 흐름은 최신 LLM 기능 소개가 아니라 다음 순서가 더 안정적입니다.

1. AI란 무엇인가: 정의보다 분야의 범위와 문제 유형을 먼저 정리합니다.
2. AI의 역사와 패러다임 변화: 상징주의, 탐색, 지식 표현, 확률적 추론, 머신러닝, 딥러닝, 생성형 AI의 연결선을 잡습니다.
3. 탐색과 문제 해결: 초기 AI의 대표 문제와 알고리즘적 사고를 봅니다.
4. 지식 표현과 규칙 기반 AI: 명시적 규칙과 논리적 추론의 강점과 한계를 봅니다.
5. 불확실성과 확률적 사고: 완전한 규칙으로 표현하기 어려운 세계를 다루는 방법을 봅니다.
6. 데이터와 학습: 머신러닝이 왜 중요한 전환점이 되었는지 설명합니다.
7. 신경망과 딥러닝의 위치: 가중치, 표현 학습, 병렬 처리의 의미를 개론 수준에서만 잡습니다.
8. 생성형 AI와 LLM의 위치: 지금 사용하는 도구가 긴 역사 위에서 어디에 있는지 연결합니다.
9. AI의 사회적 영향과 미래: 확인 가능한 자료에 근거한 쟁점만 정리합니다.

## 현재 책에 반영할 결정

- Part 1은 "최신 AI 기능 목록"이 아니라 "AI 역사와 패러다임 변화의 지도"로 시작합니다.
- 사용자의 작업 가설인 `CLI -> GUI -> LLM 에이전트` 흐름은 표준 커리큘럼 통계가 아니라 별도의 해석입니다. 따라서 `작업 가설`로 표시하고 Codex 소개 문서에서 다룹니다.
- `불확정성`, `가중치`, `병렬 처리`에 대한 해석은 흥미로운 축이지만, 개론에서는 먼저 표준 설명을 정리한 뒤 개인 해석을 검증합니다.
- LLM, RAG, Agent는 중요하지만, 개론 앞부분에서는 결론처럼 배치하고 세부 내용은 Part 5에서 다룹니다.

## 다음 조사 과제

- 서점과 대학 강의계획서의 추가 표본을 늘려 통계를 보강합니다.
- 각 주제의 등장 여부뿐 아니라 등장 순서도 기록합니다.
- 역사 파트에 사용할 연표 자료를 별도로 수집합니다.
- AI 윤리, 저작권, 보안은 법률과 정책 변화가 빠르므로 별도 출처 검토 문서로 분리합니다.

## 출처와 참고 자료

- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach](https://aima.cs.berkeley.edu/), 확인일: 2026-06-22.
- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents](https://artint.info/3e/html/ArtInt3e.html), 확인일: 2026-06-22.
- Harvard University, [CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/), 확인일: 2026-06-22.
- UC Berkeley, [CS188: Introduction to Artificial Intelligence](https://inst.eecs.berkeley.edu/~cs188/archive/fa24/), 확인일: 2026-06-22.
- MIT OpenCourseWare, [Artificial Intelligence, MIT 6.034](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/), 확인일: 2026-06-22.

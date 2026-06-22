# 2.2 Section 근거 분석

## 목적

이 문서는 `docs/chapters/chapter-02/section-02.md`의 핵심 주장과 참고 자료가 실제로 연결되는지 검토한 관리 메모입니다.

원문 확인 규칙에 따라 가능한 자료는 `.tmp/section-2-2-evidence/`, `.tmp/section-01-evidence/`, `.tmp/section-04-evidence/` 아래에 임시로 내려받아 확인했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 원문 확인 상태

| 자료 | 로컬 확인 상태 | 2.2에서의 역할 |
| --- | --- | --- |
| AIMA 4th US ed., Full Table of Contents | HTML 다운로드 확인 | 탐색, 휴리스틱 탐색, 지식·추론·계획, 불확실한 지식과 추론이 AI 개론의 큰 축으로 배치되는 근거 |
| Poole & Mackworth, `Artificial Intelligence: Foundations of Computational Agents`, 3rd ed. | HTML 다운로드 확인 | Searching for Solutions, Propositions and Inference, Deterministic Planning, Reasoning with Uncertainty, Planning with Uncertainty, Knowledge Graphs and Ontologies 배치 확인 |
| Poole & Mackworth, Chapter 3 세부 절 | HTML 다운로드 확인 | 경로 찾기, 배송 로봇, 격자 게임, state-space search, heuristic knowledge 예시 확인 |
| Poole & Mackworth, Chapter 9 세부 절 | HTML 다운로드 확인 | probability, prior/posterior probability, random variable, `Coughs`, `Distance_to_wall`, possible worlds 예시 확인 |
| Poole & Mackworth, Chapter 16 세부 절 | HTML 다운로드 확인 | triple representation, subject/verb/object, parcel/color, Wikidata 지식 그래프 예시 확인 |
| SEP, `Artificial Intelligence` | HTML 다운로드 확인 | 확률적 기법의 부활, probabilistic inference, Bayesian networks, 탐색과 표현 관련 설명의 보조 근거 |
| SEP, `Logic-Based Artificial Intelligence` | HTML 다운로드 확인 | knowledge representation, expert systems, planning as search, reasoning about uncertainty 관련 설명의 직접 근거 |

## 본문 주장별 검토

| 본문 위치 | 핵심 주장 | 근거 연결 | 판정 |
| --- | --- | --- | --- |
| `section-02.md:3-5` | 2.2는 탐색, 지식 표현, 확률 추론을 규칙 기반 접근 이후의 문제 해결 축으로 다룬다 | AIMA 목차는 search, knowledge/reasoning/planning, uncertain knowledge and reasoning을 큰 파트와 장으로 배치함. Poole & Mackworth도 reasoning/planning, uncertainty 관련 파트를 별도로 둠 | 유지 가능 |
| `section-02.md:14-36` | 규칙만으로 끝나지 않는 문제에서는 후보 탐색, 지식 표현, 불확실성 처리가 함께 필요하다 | AI 개론 교재 목차의 반복 주제를 학습용으로 일반화한 설명. Poole & Mackworth의 경로 찾기, 배송 로봇, 격자 게임 예시를 구조화해 사용함 | 유지 가능 |
| `section-02.md:38-78` | 탐색은 상태, 행동, 목표, 비용 또는 평가를 다루며 후보가 많을 때 휴리스틱이 중요하다 | AIMA는 solving problems by searching, search algorithms, informed heuristic search, A* search, learning heuristics from experience를 배치함. Poole & Mackworth는 path finding, delivery robot, grid video game을 state-space search 예시로 사용하고, heuristic knowledge를 목표 비용 추정으로 설명함 | 유지 가능 |
| `section-02.md:80-109` | 지식 표현은 사실, 관계, 제약, 행동의 결과, 예외 조건을 표현하는 문제이며 규칙 목록보다 넓다 | SEP logic-AI는 expert systems의 진화와 separate knowledge representation component의 필요성을 설명함. Poole & Mackworth는 `red(a)`, `color(a, red)`, triple representation, Wikidata knowledge graph 예시를 설명함 | 유지 가능 |
| `section-02.md:111-137` | 확률 추론은 불완전한 정보에서 가능한 결론의 그럴듯함을 계산하는 방식이다 | SEP AI는 probabilistic inference를 observed evidence에서 가설 확률을 계산하는 것으로 설명하고, Bayesian networks와 1990년대 확률적 기법의 부활을 설명함. Poole & Mackworth는 `Coughs`, `Distance_to_wall`, `Shape`, `Filled` 같은 random variable 예시를 제시함 | 유지 가능 |
| `section-02.md:139-164` | 탐색, 지식 표현, 확률 추론은 실제 시스템에서 함께 쓰일 수 있다 | 교재 목차와 SEP의 planning, representation, probabilistic reasoning 흐름을 바탕으로 한 학습용 일반화 | 유지 가능 |
| `section-02.md:166-174` | 탐색은 후보와 목표, 지식 표현은 사실과 관계, 확률 추론은 불확실성의 그럴듯함을 담당한다 | 본문 전체의 요약 문장. 각 개념의 세부 알고리즘은 후속 장으로 넘겼으므로 범위 적절 | 유지 가능 |

## 일반화 문구

사용자의 재학습 관점에서는 다음처럼 정리할 수 있습니다.

> 탐색은 가능한 후보 중에서 목표에 도달하는 길을 찾는 방식이고, 지식 표현은 문제를 풀기 위해 필요한 사실과 관계를 컴퓨터가 다룰 수 있게 정리하는 방식이며, 확률 추론은 불완전한 정보에서 가능한 결론의 그럴듯함을 계산하는 방식입니다.

## 범위 조정

- 탐색 알고리즘의 구체 절차, A*, 게임 탐색, 휴리스틱 함수는 Chapter 7에서 다룹니다.
- 확률, 조건부 확률, 베이즈 규칙, stochastic 구분은 Chapter 6에서 다룹니다.
- 머신러닝으로 넘어가는 흐름은 2.3과 Part 3에서 다룹니다.
- 지식 그래프와 RAG 같은 현대 서비스 구조는 LLM 및 서비스 아키텍처 장에서 다룹니다.

## 수정 반영

- 2.1의 규칙 기반 접근과 겹치지 않도록, 2.2는 후보 탐색, 지식 구조화, 불확실성 처리라는 세 질문으로 구성했습니다.
- `휴리스틱은 확률이다`로 읽히지 않도록, 휴리스틱은 탐색 후보를 줄이거나 순서를 정하는 경험적 기준으로 제한했습니다.
- 확률 추론은 무작위 응답이 아니라 관측 증거에서 결론의 그럴듯함을 계산하는 방식으로 설명했습니다.
- 세부 알고리즘과 수식은 후속 장으로 넘기고, 2.2는 역사와 패러다임 지형도 역할에 맞게 유지했습니다.
- Poole & Mackworth의 세부 절을 추가로 내려받아, 경로 찾기·배송 로봇·격자 게임·triple representation·random variable 예시를 본문에 일반화해 반영했습니다.

## 출처와 참고 자료

- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed., Full Table of Contents](https://aima.cs.berkeley.edu/contents.html), 확인 날짜: 2026-06-22.
- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed.](https://artint.info/3e/html/ArtInt3e.html), 확인 날짜: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/), 2018-07-12, 확인 날짜: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Richmond H. Thomason, [Logic-Based Artificial Intelligence](https://plato.stanford.edu/entries/logic-ai/), substantive revision 2024-02-27, 확인 날짜: 2026-06-22.

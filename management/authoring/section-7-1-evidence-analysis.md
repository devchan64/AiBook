# 7.1 근거 검토 메모

이 문서는 `docs/chapters/chapter-07/section-01.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- Chapter 6의 불확실성 설명에서 Chapter 7의 탐색과 휴리스틱으로 넘어가는 연결 절을 만듭니다.
- 사용자의 “휴리스틱은 불확실성과 계산 한계를 소프트웨어에 반영한 시도”라는 직관 중, 먼저 계산 한계와 탐색 공간을 분리해 설명합니다.
- 휴리스틱을 설명하기 전에 탐색(search), 탐색 공간(search space), 계산 한계(computational limit)를 입문 수준에서 정리합니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Poole & Mackworth, Chapter 3 `Searching for Solutions` | `.tmp/section-2-2-evidence/poole-mackworth-ch3-search.html` | 지능형 에이전트가 목표 달성 방법을 찾기 위해 그래프에서 경로를 탐색하는 문제로 추상화한다는 설명 |
| Poole & Mackworth, Section 3.1 `Problem Solving as Search` | `.tmp/section-2-2-evidence/poole-mackworth-ch3-s1-search-problem.html` | 시작 노드에서 목표 노드까지 경로를 찾는 추상화, 경로 찾기 예시, 검색의 어려움과 heuristic knowledge 설명 |
| AIMA 4th US ed. table of contents | `.tmp/section-2-2-evidence/aima-contents.html` | `Solving Problems by Searching`, `Informed (Heuristic) Search`, `Heuristic Functions`가 AI 개론의 주요 축으로 배치됨 |
| Google DeepMind, `AlphaDev discovers faster sorting algorithms` | `.tmp/section-7-1-evidence-modern/deepmind-alphadev.html`, `.tmp/section-7-1-evidence-modern/deepmind-alphadev.html.txt` | 명령 조합의 가능한 수가 매우 커지는 현대 탐색 공간 사례 |
| Google DeepMind, `FunSearch: Making new discoveries in mathematical sciences using Large Language Models` | `.tmp/section-7-1-evidence-modern/deepmind-funsearch.html`, `.tmp/section-7-1-evidence-modern/deepmind-funsearch.html.txt` | 해답 자체가 아니라 코드로 작성된 함수(function)를 탐색 대상으로 삼는 현대 사례 |
| `management/authoring/heuristics-and-ai-thinking.md` | 저장소 관리 문서 | 휴리스틱을 계산 한계 속에서 탐색을 줄이는 경험적 기준으로 설명하는 내부 기준 |
| `management/authoring/ai-2007-memory-map.md` | 저장소 관리 문서 | 2007년 AI 학습 기억 중 탐색, 휴리스틱, 확률 모델, 학습 모델의 경계를 정리한 내부 기준 |

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 탐색(search)은 가능한 후보를 살펴보며 목표에 도달하는 경로를 찾는 문제 해결 방식이다 | Poole & Mackworth는 문제를 시작 노드에서 목표 노드까지의 경로 찾기로 추상화할 수 있다고 설명함 | 유지 |
| `Search underlies much of AI.` 직접 인용 | Poole & Mackworth Section 3.1의 짧은 원문 문장 | 유지. 직접 인용은 5단어로 제한하고 본문에서 출처를 바로 표기 |
| 상태(state), 행동(action), 목표(goal), 경로(path), 비용(cost)으로 길 찾기 예시를 설명할 수 있다 | Poole & Mackworth의 computer maps 예시와 검색 문제 추상화에 기반 | 유지 |
| 탐색 공간(search space)이 커지면 가능한 조합이 빠르게 늘어난다 | AIMA와 Poole & Mackworth 모두 search algorithms, graph searching, heuristic search를 주요 주제로 배치함. 본문 표는 입문용 예시 | 유지 |
| 완전 탐색(exhaustive search)은 작은 문제에서는 가능하지만 큰 문제에서는 계산 한계에 부딪힌다 | Poole & Mackworth는 search의 어려움과 NP-complete 문제를 언급하며 해를 인식하는 것과 찾는 것의 차이를 설명함 | 유지. NP-complete 상세는 제외 |
| 계산 한계(computational limit)는 단순히 구현이 느리다는 뜻이 아니다 | 탐색 공간 증가와 계산 자원 한계를 구분하기 위한 본문 일반화 | 유지 |
| AlphaDev는 탐색 공간이 너무 큰 현대 사례다 | DeepMind는 AlphaDev가 가능한 명령 조합을 효율적으로 탐색해야 하며 그 수가 매우 크다고 설명함 | 유지. 모든 AI 문제가 강화학습 기반 알고리즘 탐색이라는 뜻으로 일반화하지 않음 |
| FunSearch는 탐색 대상을 함수/프로그램으로 바꾸는 현대 사례다 | DeepMind는 FunSearch를 코드로 작성된 함수를 탐색하는 방법으로 설명함 | 유지. LLM이 학습 데이터에서 정답을 검색한다는 뜻으로 일반화하지 않음 |
| 불확실성, 탐색 공간, 학습은 연결되지만 같은 문제가 아니다 | 6.2, 6.3의 용어 기준과 2007 기억 보정 메모에 기반 | 유지 |
| 휴리스틱은 7.2에서 다룬다 | 도메인 경계상 7.1은 탐색 공간과 계산 한계, 7.2는 휴리스틱 기준 | 유지 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 6.1 | 규칙만으로 닫히지 않는 문제 조건 |
| 6.2 | uncertainty, probability, stochastic 용어 구분 |
| 6.3 | 확률적 관점이 쓰이는 작업 위치 |
| 7.1 | 탐색 공간과 계산 한계 |
| 7.2 | 휴리스틱이 탐색에서 무엇을 줄이는지 |
| 7.3 | 휴리스틱과 확률 모델의 차이 |
| Part 2 | 조합, 지수적 증가, 확률 수학의 기초 |
| Part 3 | 모델 선택, 튜닝, 전처리 휴리스틱의 실무 적용 |

## 보수화한 표현

- “휴리스틱은 AI적 사고의 첫 시도”라는 표현은 7.1 본문에 넣지 않았습니다. 7.1은 휴리스틱 이전의 탐색 문제를 설명합니다.
- 지루함을 줄이기 위해 추가한 인용형 문구 대부분은 외부 인용이 아니라 본문 핵심을 뽑은 강조 문구입니다. 외부 직접 인용은 Poole & Mackworth의 짧은 문장 하나로 제한했습니다.
- 현대 기업 인용 후보로 OpenAI, Anthropic, Tesla 자료를 검토했지만, 7.1의 탐색 공간과 계산 한계를 설명하는 직접 근거로는 부적절하다고 판단해 본문에서 제외했습니다.
- 현대 사례는 DeepMind의 AlphaDev와 FunSearch만 채택했습니다. 두 사례 모두 탐색 공간 또는 탐색 대상의 변화와 직접 연결되기 때문입니다.
- AlphaDev는 `거대한 명령 조합 탐색`의 사례로 제한하고, 강화학습 일반론으로 확장하지 않았습니다.
- FunSearch는 `함수/프로그램 공간 탐색`의 사례로 제한하고, LLM이 정답을 검색해 꺼내는 방식으로 설명하지 않았습니다.
- `NP-complete`는 근거상 중요하지만 입문 절에서는 용어만 암시하고 상세 설명하지 않았습니다.
- 탐색을 웹 검색이나 파일 검색과 혼동하지 않도록, 목표 상태로 가는 후보 경로를 찾는 문제로 제한했습니다.
- 문서 목차 작성 예시는 엄밀한 알고리즘 사례가 아니라 탐색 관점을 이해하기 위한 비유로 명시했습니다.
- CPU/GPU 성능 향상이 중요하다는 점은 인정하되, 탐색 공간 증가 자체를 없애지는 못한다고 제한했습니다.

## 확인한 원문 위치

- `.tmp/section-2-2-evidence/poole-mackworth-ch3-s1-search-problem.html`
  - 시작 노드에서 목표 노드까지 경로를 찾는 추상화: 129-135행 부근
  - computer maps path finding 예시: 137-176행 부근
  - search가 AI 문제 해결의 기반이라는 설명: 191-201행 부근
  - satisficing, search difficulty, heuristic knowledge 설명: 203-225행 부근
- `.tmp/section-2-2-evidence/poole-mackworth-ch3-search.html`
  - 목표를 달성하기 위한 행동 결정을 그래프 경로 탐색으로 추상화한다는 장 도입: 111-122행 부근
- `.tmp/section-2-2-evidence/aima-contents.html`
  - `Solving Problems by Searching`: 80-106행 부근
  - `Informed (Heuristic) Search`, `Heuristic Functions`: 104-119행 부근
- `.tmp/section-7-1-evidence-modern/deepmind-alphadev.html.txt`
  - `enormous number of possible combinations of instructions` 문구 확인
  - AlphaDev가 가능한 명령 조합을 탐색한다는 설명 확인
- `.tmp/section-7-1-evidence-modern/deepmind-funsearch.html.txt`
  - `functions written in computer code` 문구 확인
  - brute-force 방식이 가능한 후보 수 때문에 작동하지 않는다는 설명 확인

## 채택하지 않은 현대 기업 인용 후보

| 후보 | 제외 이유 |
| --- | --- |
| OpenAI, `Learning to reason with LLMs` | reasoning model의 학습/추론 계산량 설명으로는 유용하지만, 7.1의 탐색 공간(search space)과 계산 한계(computational limit)를 설명하는 직접 인용으로는 부정확함 |
| Anthropic, `Tracing the thoughts of a large language model` | interpretability 사례로 흥미롭지만, 7.1의 탐색 공간 개념보다 LLM 내부 해석과 계획성 논의에 가까움 |
| Tesla, `AI & Robotics` | 자율주행/로봇 제품 방향 설명으로, 7.1의 학습용 개념 근거로 쓰기에는 범위가 넓고 기업 주장 성격이 강함 |

## 남은 검토 사항

- 7.2에서 휴리스틱 함수(heuristic function), 평가 함수(evaluation function), 가지치기(pruning), 만족해(satisficing)를 별도 근거로 다룹니다.
- 7.3에서 휴리스틱과 확률 모델(probabilistic model)을 혼동하지 않도록 다시 분리합니다.
- Part 2에서 조합 폭발(combinatorial explosion)이나 지수적 증가(exponential growth)를 수학 기초로 다룰지 결정합니다.

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

## 출처와 참고 자료

- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach](https://aima.cs.berkeley.edu/), 확인일: 2026-06-22.
- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents](https://artint.info/3e/html/ArtInt3e.html), 확인일: 2026-06-22.
- Harvard University, [CS50's Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/), 확인일: 2026-06-22.
- UC Berkeley, [CS188: Introduction to Artificial Intelligence](https://inst.eecs.berkeley.edu/~cs188/archive/fa24/), 확인일: 2026-06-22.
- MIT OpenCourseWare, [Artificial Intelligence, MIT 6.034](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/), 확인일: 2026-06-22.

---

# 데이터 모델링 커리큘럼 조사

이 아래 섹션은 `management/authoring/brewing-shot-ai-notes/01`부터 `10`, `management/authoring/data-modeling-part/01`부터 `15`에서 정리한 주제 축을 기준으로, 주요 대학과 학술 커리큘럼 문서에서 반복되는 항목을 다시 읽은 기록입니다.

## 조사 목적

- 책의 `데이터 모델링 Part`가 단지 개인 사례 정리가 아니라, 실제 데이터과학 교육에서 반복되는 축과 어떻게 맞물리는지 확인합니다.
- 다만 외부 커리큘럼의 이름을 그대로 베끼지 않고, 현재 책이 필요한 질문으로 다시 정규화합니다.
- 특히 다음 주제가 실제 커리큘럼에 어떤 형태로 나타나는지 봅니다.
  - 샘플 단위 정의
  - 원시 로그와 요약 표의 차이
  - 특징과 설명 가능한 중간 표현
  - 최근 구간과 기준선 비교
  - 표본 수, 반복성, 경고 해석의 보수성
  - 규칙, 통계, 머신러닝으로 이어지는 모델링 사다리

## 조사 방식

- 기준일: 2026-07-05
- 방식: 대학 공식 강의 페이지와 일정표, 학술 커리큘럼 합의 문서를 사용했습니다.
- 원칙: 대학 사례는 가능하면 공식 강의 페이지를 우선하고, 학술단체·합의 문서는 해당 문서 자체나 그 문서를 소개하는 1차 저자 문서를 사용했습니다.
- 표본 구성: `세부 주제 나열이 충분한 대학 공식 강의 페이지`와 `전공 설계 원칙을 제시하는 학술단체·합의 문서`를 함께 두고 읽었습니다. 두 부류는 역할이 다르므로 같은 층위의 목차로 취급하지 않았습니다.
- 한계:
  - 대학 공식 커리큘럼은 `데이터 모델링`이라는 이름보다 `data wrangling`, `EDA`, `feature engineering`, `model selection`, `inference`처럼 분산된 이름으로 나타나는 경우가 많았습니다.
  - `샘플 단위`, `원시 시계열을 동작 1회 요약 행으로 묶는 법`, `기준선 비교를 데이터 모델링 단계로 당겨오는 법`은 일반 커리큘럼에서 직접 제목으로 드러나기보다, 여러 주제에 흩어져 있었습니다.
  - 이번 1차 정리에서 대학 표본 가운데 현재 책의 주제 축과 직접 매핑할 수 있을 만큼 세부 주제 공개가 잘 되어 있던 자료는 Berkeley Data 100이 가장 강했습니다. 따라서 대학 사례의 질적 해석은 Berkeley 비중이 높고, 일반화는 학술단체 문서와 함께 보수적으로 잡았습니다.

## 현재 책 기준의 정규화 주제

| 정규화 주제 | 현재 노트/계획 문서에서의 위치 | 외부 커리큘럼에서 주로 보이는 이름 |
| --- | --- | --- |
| 샘플 단위 정의 | `data-modeling-part/03`, `06`, `12` | row meaning, sample, measurement, data representation |
| 원시 로그와 요약 표 | `brewing-shot-ai-notes/02`, `03`, `05`, `data-modeling-part/03`, `13` | data wrangling, cleaning, aggregation, summary statistics |
| 특징과 중간 표현 | `brewing-shot-ai-notes/04`, `07`, `data-modeling-part/03`, `06`, `14` | feature engineering, transformations, representation |
| 최근 구간과 기준선 비교 | `brewing-shot-ai-notes/05`, `06`, `data-modeling-part/03`, `05`, `06`, `14` | baseline, comparison, model selection, statistical inference |
| 표본 수와 해석 경계 | `brewing-shot-ai-notes/06`, `07`, `data-modeling-part/03`, `06`, `14`, `15` | sampling, bias and variance, inference, uncertainty |
| 모델링 사다리 | `brewing-shot-ai-notes/07`, `data-modeling-part/03`, `05` | regression, classification, clustering, machine learning |

## 조사 표본

| 구분 | 자료 | 기관 | 현재 책의 주제와 연결되는 포인트 |
| --- | --- | --- | --- |
| 대학 공식 강의 | [Data 100: Principles and Techniques of Data Science](https://ds100.org/) | UC Berkeley | 데이터 생애주기, 정제, EDA, 모델링, 특징 공학, 교차검증, 편향-분산 |
| 대학 커리큘럼 해설 | [Interleaving Computational and Inferential Thinking: Data Science for Undergraduates at Berkeley](https://arxiv.org/abs/2102.09391) | UC Berkeley faculty | 계산적 사고와 추론적 사고를 함께 가르치는 5개 코어 과목 구조 |
| 합의형 커리큘럼 문서 | [Curriculum Guidelines for Undergraduate Programs in Data Science](https://arxiv.org/abs/1801.06814) | PCMI 2016 Summer Undergraduate Faculty Program | 수학·통계·컴퓨터과학을 잇는 데이터과학 전공 설계 지침 |
| 학술단체 연계 통계 교육 지침 | [Updated guidelines, updated curriculum: The GAISE College Report and introductory statistics for the modern student](https://arxiv.org/abs/1705.09530) | ASA endorsement explained by report authors | 실데이터, 개념 중심, 기술 활용, 해석 중심의 통계 교육 지침 |

이 표본은 `대학 강의 세부 주제`, `대학 커리큘럼 해설`, `학술 합의형 전공 가이드`, `통계 교육 지침`을 분리해 본 것입니다. 즉, 현재 책의 데이터 모델링 Part는 한 강의의 목차만 따라가기보다, 강의 수준의 실무 주제와 학술 지침 수준의 설계 원칙을 겹쳐 읽는 방식으로 정리해야 합니다.

## 자료별 핵심 관찰

### 1. UC Berkeley Data 100

Berkeley의 공식 강의 설명은 데이터과학 생애주기를 `question formulation`, `data collection and cleaning`, `exploratory data analysis and visualization`, `statistical inference and prediction`, `decision-making`으로 잡고 있습니다. 또한 회귀, 분류, 군집 같은 머신러닝 방법과 측정 오차, 예측을 함께 다룹니다. 이는 현재 책의 `원시 로그/요약 표 -> 특징 -> 비교 기준 -> 학습` 흐름과 가장 직접적으로 맞닿아 있습니다. [turn25view1](https://ds100.org/)

같은 강의의 2026년 봄 일정표를 보면 `Data Wrangling and EDA`, `Sampling`, `Modeling and SLR`, `Constant Model, Loss, Transformations`, `Feature Engineering`, `Cross-Validation, Regularization`, `Estimators, Bias, and Variance`, `Parameter Inference & Bootstrap`가 순차적으로 배치됩니다. 즉 대학 커리큘럼 안에서도 데이터 정리와 표현, 특징 공학, 표본과 편향-분산, 검증이 한 흐름으로 이어진다는 점을 확인할 수 있습니다. [turn25view0](https://ds100.org/sp26/)

### 2. Berkeley 데이터과학 학부 커리큘럼 해설

Berkeley faculty가 쓴 커리큘럼 해설은 학부 데이터과학 커리큘럼이 `computational thinking`, `inferential thinking`, `working on real-world problems`를 함께 강조하는 5개 코어 과목에 anchored 되어 있다고 설명합니다. 이는 현재 책의 데이터 모델링 Part가 단순 전처리 절이 아니라, 계산과 추론 사이의 구조를 먼저 세우는 Part여야 한다는 판단을 지지합니다. [turn26view1](https://arxiv.org/abs/2102.09391)

### 3. PCMI 데이터과학 학부 커리큘럼 가이드

PCMI 2016 Summer Undergraduate Faculty Program이 만든 가이드는 수학, 통계, 컴퓨터과학 배경의 교수들이 데이터과학 전공 설계를 위해 만든 구조 문서입니다. 추상 수준은 높지만, 데이터과학 커리큘럼을 한 학과의 기술 목록이 아니라 `여러 기초를 묶는 전공 설계 문제`로 다룬다는 점이 중요합니다. 현재 책의 `데이터 모델링 Part를 독립 Part로 세운다`는 결정은 이런 합의형 문서의 취지와도 잘 맞습니다. [turn28view0](https://arxiv.org/abs/1801.06814)

### 4. ASA GAISE College Report 관련 업데이트 문서

이 문서는 2016년 갱신된 GAISE College Report가 ASA Board of Directors의 승인을 받았고, 통계 교육이 더 많은 실데이터 탐색과 해석 요구에 대응해야 한다는 점을 설명합니다. 현재 책의 `표본 수`, `반복성`, `경고와 원인 확정의 분리`, `실데이터와 기술을 이용한 해석` 축은 바로 이 통계 교육 방향과 맞닿아 있습니다. [turn28view1](https://arxiv.org/abs/1705.09530)

## 현재 책 주제와의 매핑

| 현재 책의 데이터 모델링 주제 | Berkeley Data 100 | Berkeley 커리큘럼 해설 | PCMI 가이드 | ASA GAISE 업데이트 |
| --- | --- | --- | --- | --- |
| 샘플 단위 정의 | 간접적으로 나타남. 강의 설명은 데이터 생애주기와 표 구조를 전제함 | 계산과 추론 사이의 구조를 먼저 세움 | 전공 설계 차원에서 구조화 필요성 지지 | 실데이터와 해석 중심이라는 점에서 간접 지지 |
| 원시 로그와 요약 표 | `data collection and cleaning`, `Data Wrangling and EDA`로 강하게 나타남 | 실제 문제 중심 데이터 구성 강조 | 데이터과학 전공의 공통 기초로 지지 | 실데이터 사용, 개념 중심 해석과 연결 |
| 특징과 중간 표현 | `Feature Engineering`, `Transformations`로 직접 나타남 | 계산적 사고와 추론적 사고의 접점 | 전공 설계 차원에서 필수 역량으로 읽힘 | 절차보다 개념과 해석을 우선하라는 방향과 연결 |
| 기준선 비교와 변화 해석 | `Constant Model`, `Cross-Validation`, `Bias and Variance`, `Inference`에 분산되어 나타남 | 모델링 이전의 구조화 필요성을 지지 | 데이터 표현과 추론의 연결축으로 읽힘 | 해석과 불확실성 강조와 직접 연결 |
| 표본 수, 반복성, 보수적 해석 | `Sampling`, `Bias and Variance`, `Bootstrap`으로 직접 나타남 | 추론적 사고 축으로 지지 | 통계 기초 축으로 간접 지지 | 매우 강하게 지지 |
| 모델링 사다리 | 회귀, 분류, 군집이 직접 나타남 | 5개 코어 과목 구조에서 계산/추론/응용 연결 | 전공 설계 전체 틀로 지지 | 통계적 사고를 우선하되 계산과 기술 사용을 허용 |

## 책 설계에 주는 의미

### 1. `샘플 단위`는 일반 커리큘럼보다 더 앞에 세워야 한다

외부 커리큘럼은 데이터 정리, EDA, feature engineering을 분명히 다루지만, `한 행이 무엇을 뜻하는가`, `측정 시점과 동작 1회가 왜 다른가`를 독립된 중심 질문으로 먼저 세우는 경우는 드뭅니다. 따라서 현재 책은 이 부분을 일반 커리큘럼보다 더 명시적으로 앞에 둬야 합니다.

### 2. `원시 로그 -> 요약 표 -> 특징` 흐름은 정당하다

Berkeley Data 100의 `wrangling -> modeling -> feature engineering` 흐름과, GAISE의 실데이터·기술 활용 지침을 함께 보면 현재 노트와 Part 설계가 잡은 `원시 시계열 -> 동작 1회 요약 행 -> 특징` 순서는 충분히 교육적으로 방어 가능합니다.

### 3. `기준선 비교`는 평가 절의 부록이 아니라 데이터 모델링 절의 핵심으로 승격할 가치가 있다

대학 커리큘럼은 보통 baseline, model selection, bias-variance, inference를 뒤쪽에 배치합니다. 하지만 현재 책은 자동 동작 1회 사례를 사용하므로, `최근 구간 vs 평소 기준선`을 더 앞에서 데이터 표현 문제로 다루는 편이 자연스럽습니다. 이는 외부 커리큘럼과 충돌하기보다, 그 요소를 더 실제 데이터 구조에 맞게 재배치하는 방식입니다.

### 4. `표본 수, 반복성, false alarm`은 통계 축과 더 직접 연결해야 한다

이 주제는 Berkeley의 `sampling`, `bias and variance`, `bootstrap`과 ASA GAISE의 실데이터·해석 중심 지침으로 정당화할 수 있습니다. 따라서 현재 책의 데이터 모델링 Part에서는 이 항목을 부록이 아니라 Chapter 6급 핵심 축으로 남기는 편이 맞습니다.

### 5. `모델링 사다리`는 뒤 Part의 예고가 아니라 현재 Part의 마무리 질문으로 쓰는 편이 좋다

외부 커리큘럼은 회귀, 분류, 군집, 추론을 뒤에서 본격적으로 다루지만, 현재 책은 `어떤 문제는 아직 분류기가 아니라 비교 리포트나 검토 큐가 더 낫다`는 판단을 먼저 세우려 합니다. 이 점은 단순 알고리즘 소개보다 데이터 모델링 Part의 교육적 차별점으로 활용할 수 있습니다.

## 현재 반영 결정

- `data-modeling-part/03-part-outline-draft.md`의 `정의 -> 샘플 -> 요약 -> 특징 -> 기준선 -> 해석 경계` 순서는 유지합니다.
- `data-modeling-part/06-chapter-section-map.md`에서 Chapter 2와 Chapter 3을 더 앞세우는 현재 배치는 유지합니다.
- `14-shared-assets-and-guards.md`의 공통 어휘와 과장 방지 문장은 유지합니다.
- 추가 보강이 필요한 것은 `대학 공식 커리큘럼이 직접 이름 붙이지 않는 샘플 단위 설명`과 `기준선 비교를 데이터 모델링 단계로 당기는 이유`를 더 분명히 쓰는 일입니다.

## 데이터 모델링 파트에 대한 잠정 결론

외부 커리큘럼을 그대로 따르면 데이터 정리, 특징 공학, 검증, 추론은 충분히 들어오지만, 현재 책이 중요하게 보는 `샘플 단위`, `원시 시계열과 동작 1회 요약 행의 구분`, `기준선 비교를 데이터 표현 문제로 먼저 다루는 방식`은 희미해질 수 있습니다.

따라서 현재 책은 표준 커리큘럼을 거스르기보다, 표준 커리큘럼에 흩어진 주제를 `자동으로 실행되는 동작 1회와 그 원천 시계열`이라는 사례 축으로 더 앞당겨 재구성하는 편이 맞습니다.

## 추가 출처와 참고 자료

- UC Berkeley, [Data 100: Principles and Techniques of Data Science](https://ds100.org/), 확인일: 2026-07-05.
- UC Berkeley, [Data 100 Spring 2026 Schedule](https://ds100.org/sp26/), 확인일: 2026-07-05.
- Ani Adhikari, John DeNero, Michael I. Jordan, [Interleaving Computational and Inferential Thinking: Data Science for Undergraduates at Berkeley](https://arxiv.org/abs/2102.09391), 확인일: 2026-07-05.
- Richard De Veaux et al., [Curriculum Guidelines for Undergraduate Programs in Data Science](https://arxiv.org/abs/1801.06814), 확인일: 2026-07-05.
- Beverly L. Wood et al., [Updated guidelines, updated curriculum: The GAISE College Report and introductory statistics for the modern student](https://arxiv.org/abs/1705.09530), 확인일: 2026-07-05.

# Sections 1.1-2.3 근거 재검토

## 목적

이 문서는 다음 본문 Section을 새 근거 검토 기준으로 다시 평가한 관리 메모입니다.

- `docs/chapters/chapter-01/section-01.md`
- `docs/chapters/chapter-01/section-02.md`
- `docs/chapters/chapter-01/section-03.md`
- `docs/chapters/chapter-02/section-01.md`
- `docs/chapters/chapter-02/section-02.md`
- `docs/chapters/chapter-02/section-03.md`

검토 기준은 다음 두 가지를 함께 본다.

- 학술적 일반화 가능성: 교과서, 학술 논문, 공식 문서, 반복 인용되는 연구처럼 넓은 설명으로 일반화할 수 있는가
- 중요도: 해당 Section의 중심 질문을 설명하는 핵심 근거인가, 보조적 비유나 주변 사례인가

## 전체 판단

| Section | 중심 질문 | 현재 판정 | 본문 수정 필요 | 관리 조치 |
| --- | --- | --- | --- | --- |
| 1.1 AI라는 말의 범위 | AI라는 말의 넓은 범위와 정의 | 유지 가능 | 즉시 수정 없음 | 사전·기관 정의는 핵심 근거, DSS/BI/DW/OLAP는 보조 근거로 분리 |
| 1.2 AI가 다루는 문제 | AI 문제를 입력·출력·목표 관점으로 보기 | 유지 가능 | 즉시 수정 없음 | 함수·워크플로우 관점은 학습용 일반화로 유지 |
| 1.3 AI, ML, DL, GenAI, LLM 관계 | 용어 층위(level) 구분 | 유지 가능 | 즉시 수정 없음 | 생성형 AI와 LLM 관계는 NIST와 LLM survey를 핵심 근거로 유지 |
| 2.1 기호 기반 AI와 규칙 기반 접근 | symbolic/rule-based 접근의 역사적 위치 | 유지 가능 | 즉시 수정 없음 | KCI 검색은 용어 선택 보조 근거로만 사용 |
| 2.2 탐색, 지식 표현, 확률 추론 | 규칙 이후의 문제 해결 축 | 유지 가능 | 즉시 수정 없음 | AIMA, Poole & Mackworth, SEP를 핵심 근거로 유지 |
| 2.3 머신러닝, 딥러닝, 생성형 AI 흐름 | 데이터 기반 학습으로 이동한 이유 | 대체로 유지 가능 | 일부 후속 보강 권장 | Software/workflow 관점은 보조 근거로 분리하고, 딥러닝 직관 문구는 후속 장에서 반영 |

## 1.1 AI라는 말의 범위

### 핵심 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| OECD AI system definition explanation | 높음. 국제기구의 공식 정의 해설 | 높음 | AI 시스템을 입력, 목표, 출력, 영향으로 설명하는 핵심 근거 |
| Merriam-Webster, Cambridge, Britannica | 중간. 사전 정의 | 높음 | AI가 능력, 시스템, 분야를 모두 가리킬 수 있다는 범위 설명에 사용 |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | 높음. 철학·AI 개론 자료 | 높음 | AI가 단일 기술이 아니라 여러 접근을 포함한다는 설명에 사용 |
| NIST GAI Profile, Zhao et al. LLM survey | 높음 | 중간 | 생성형 AI와 LLM 관계를 1.1에서 간단히 보강하는 근거 |

### 보조 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| ZDIC `人工智能` | 중간 이하. 동북아권 표현 확인용 | 낮음-중간 | 동북아권 표현의 보조 사례로만 사용 |
| Fayyad et al. KDD 논문 | 높음 | 중간 | 데이터마이닝과 데이터 기반 판단 배경 설명에 사용 |
| D. J. Power DSS history | 중간. 개인/전문 사이트 성격이나 DSS 흐름 정리에 유용 | 낮음-중간 | DSS/BI/DW/OLAP 배경 설명의 보조 근거로만 사용 |

### 검토 결과

1.1의 핵심 주장은 사전 정의, OECD, SEP로 충분히 뒷받침된다. 다만 DSS/BI/DW/OLAP는 AI 정의 자체의 핵심 근거가 아니라 데이터 기반 의사결정 환경을 설명하는 주변 근거다. 따라서 현재처럼 배경 설명으로 짧게 두는 것은 가능하지만, AI 정의의 핵심처럼 확장하지 않는다.

### 후속 보강

- 한국어권·일본어권 사전 정의는 아직 보강 필요다.
- DSS/BI/DW/OLAP는 이후 데이터 기반 의사결정 또는 실무 적용 장에서 별도 근거로 다시 다루는 편이 낫다.

## 1.2 AI가 다루는 문제

### 핵심 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| OECD AI system definition explanation | 높음 | 높음 | 입력, 목표, 출력, 영향 관점의 핵심 근거 |
| Poole & Mackworth, `Artificial Intelligence: Foundations of Computational Agents` | 높음. 공개 AI 교재 | 높음 | agent, black-box, transduction, controller 관점의 핵심 근거 |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | 높음 | 중간-높음 | 지능형 에이전트, 탐색, 계획, 학습의 보조 핵심 근거 |

### 보조 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| Cambridge Dictionary | 중간 | 낮음-중간 | 언어, 이미지, 문제 해결 예시를 보조 |
| Fayyad et al. KDD 논문 | 높음 | 중간 | 같은 데이터가 목표에 따라 분류, 회귀, 군집화, 예측 문제로 달라질 수 있다는 설명 보조 |

### 검토 결과

1.2는 현재 Section의 중심 질문과 근거가 잘 맞는다. `함수와 워크플로우로 읽기`는 사용자 관점을 살린 학습용 일반화이며, Poole & Mackworth의 agent function/transduction 관점과 연결 가능하다. 다만 업무 워크플로우 전체를 설명하는 직접 근거는 아니므로, 현재처럼 “학습용 일반화”로 제한해야 한다.

### 후속 보강

- 추천, 순위화, 제어는 1.2에서 예시 수준으로 충분하다. 후속 장에서 개별 주제로 다룰 때 별도 근거가 필요하다.
- 검색 서비스와 자율주행 예시는 자체 예시이므로, 심화 설명에서는 별도 자료가 필요하다.

## 1.3 AI, 머신러닝, 딥러닝, 생성형 AI의 관계

### 핵심 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| OECD AI system definition explanation | 높음 | 높음 | AI의 가장 넓은 시스템 범위 설명에 사용 |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | 높음 | 높음 | 머신러닝, 딥러닝, 표현 학습 관계 설명에 사용 |
| NIST GAI Profile | 높음. 공식 위험관리 문서 | 높음 | 생성형 AI의 출력 범주와 LLM이 대표 활동 중 하나임을 설명 |
| Zhao et al., `A Survey of Large Language Models` | 높음. survey 논문 | 높음 | LLM을 대규모 사전학습 언어 모델 계열로 설명 |

### 보조 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| AIMA 공식 사이트 | 높음이나 현재는 목차 중심 확인 | 중간 | AI 안에 ML, DL, NLP, vision, robotics가 배치된다는 보조 근거 |

### 검토 결과

1.3의 용어 층위(level) 구분은 근거와 잘 맞는다. 특히 생성형 AI를 딥러닝의 단순 하위 단계처럼 단정하지 않고, 출력 성격과 서비스 범주로 설명한 점은 안전하다. `AI > ML > DL > GenAI > LLM` 줄은 강한 단순화라고 본문에서 이미 제한하고 있으므로 유지 가능하다.

### 후속 보강

- Part 5에서 LLM 발전사를 다룰 때는 Zhao survey만으로 끝내지 말고 NLP 계보 자료를 추가해야 한다.
- `inference`와 `reasoning` 구분은 1.3에서는 예고 수준으로 두고, Chapter 5 또는 Part 5에서 본격화한다.

## 2.1 기호 기반 AI와 규칙 기반 접근

### 핵심 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| SEP, `Logic-Based Artificial Intelligence` | 높음 | 높음 | McCarthy, commonsense reasoning, logic-based AI, knowledge representation, expert systems 설명의 핵심 근거 |
| SEP, `Artificial Intelligence` | 높음 | 중간-높음 | symbolic/non-symbolic, logicist/non-logicist 구분 보조 |
| AIMA 공식 사이트 | 높음이나 현재는 목차 중심 확인 | 중간 | logical agents, inference, knowledge representation이 AI 개론의 주요 축임을 보조 |

### 보조 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| KCI 논문 검색 | 낮음-중간. 용어 사용례 확인용 | 중간 | 한국어 기본 표현 선택의 보조 근거로만 사용 |
| Google ML Glossary, Supervised Learning | 중간. 공식 교육 문서 | 낮음-중간 | 데이터 라벨링과 symbolic AI의 느슨한 접점 설명 보조 |

### 검토 결과

2.1의 핵심 설명은 SEP logic-AI에 잘 연결된다. KCI 검색은 `기호 기반 AI`라는 책 내부 표현을 선택하기 위한 보조 근거일 뿐, symbolic AI의 학술적 정의 근거로 쓰면 안 된다. 데이터 라벨링과 symbolic AI의 관계도 본문처럼 “느슨한 연결”으로 제한되어 있어 안전하다.

### 후속 보강

- Logic Theorist, GPS, MYCIN, DENDRAL 같은 대표 사례는 아직 본문에 깊게 들어가지 않았으므로, 추가 시 별도 근거가 필요하다.
- 현대 서비스에서 규칙 기반 접근이 쓰인다는 주장은 서비스 아키텍처 장에서 공식 문서나 구현 사례로 보강한다.

## 2.2 탐색, 지식 표현, 확률 추론

### 핵심 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| AIMA 4th US ed. 목차 | 높음. 대표 AI 교재 | 높음 | search, heuristic search, knowledge, planning, uncertainty가 AI 개론의 큰 축임을 보여줌 |
| Poole & Mackworth 공개 교재 | 높음 | 높음 | path finding, delivery robot, state-space search, random variables, knowledge graph 예시의 직접 근거 |
| SEP, `Artificial Intelligence` | 높음 | 중간-높음 | probabilistic inference, Bayesian networks, 확률적 기법의 부활 설명 |
| SEP, `Logic-Based Artificial Intelligence` | 높음 | 중간-높음 | knowledge representation, planning as search, uncertainty 관련 설명 |

### 검토 결과

2.2는 근거의 학술적 일반화 가능성과 Section 중요도가 모두 높다. 탐색, 지식 표현, 확률 추론은 대표 교재와 SEP에서 반복되는 축이다. 본문 예시는 Poole & Mackworth의 예시 구조를 학습용으로 재구성한 것으로 적절하다.

### 후속 보강

- 휴리스틱 함수, A* 탐색, 베이즈 규칙, 베이지안 네트워크 계산은 후속 장에서 별도 근거와 함께 다룬다.
- 2.2는 역사와 지형도 역할이므로 현재 수준을 유지한다.

## 2.3 머신러닝, 딥러닝, 생성형 AI로의 흐름

### 핵심 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| SEP, `Artificial Intelligence` | 높음 | 높음 | ML, supervised/unsupervised learning, feature representation, representation learning, deep learning 설명의 핵심 근거 |
| Fayyad et al. KDD 논문 | 높음 | 높음 | KDD와 data mining을 구분하고 데이터 기반 판단 배경을 설명 |
| NIST GAI Profile | 높음 | 높음 | 생성형 AI를 합성 콘텐츠 생성 모델 범주로 설명 |
| Zhao et al. LLM survey | 높음 | 중간-높음 | LLM을 언어 모델링과 대규모 사전학습 흐름으로 설명 |

### 보조 근거

| 자료 | 학술적 일반화 | 중요도 | 반영 판단 |
| --- | --- | --- | --- |
| AIMA 4th US ed. 목차 | 높음 | 중간 | ML, deep learning, NLP, vision, robotics가 AI 개론의 주요 영역임을 보조 |
| Poole & Mackworth 공개 교재 | 높음 | 중간 | uncertainty, learning, knowledge graph, probabilistic reasoning의 연결을 보조 |
| 사용자 관점 및 `user-claim-evidence-map.md` | 작업 가설 | 중간 | `SW 함수`, `workflow`, `직관적 패턴 판단`은 본문에서 학습용 일반화로만 사용 |

### 검토 결과

2.3의 중심 흐름은 근거와 잘 맞는다. 머신러닝과 딥러닝 정의는 SEP로, 데이터마이닝/KDD 배경은 Fayyad 논문으로, 생성형 AI는 NIST로, LLM의 큰 흐름은 Zhao survey로 뒷받침된다.

다만 `사용자의 관점을 일반화하기` 절은 핵심 학술 근거라기보다 사용자의 재학습 관점을 정리하는 부분이다. 현재 본문은 이 부분을 명시적으로 사용자의 관점이라고 분리하고 있어 유지 가능하다. 후속 보강 시에는 다음 자료를 보조 근거로 검토한다.

- Karpathy, `Software 2.0`: 소프트웨어 작성 방식 변화의 영향력 있는 비유. 표준 학술 정의로 쓰지 않는다.
- MLOps 논문: AI 서비스가 운영 워크플로우 안에서 구성된다는 보조 근거.
- Connectionism/Neurosymbolic 자료: 딥러닝과 직관적 패턴 판단, inference/reasoning 분리의 후속 근거.

### 후속 보강

- 2.3에 `직관적 패턴 판단` 문구를 넣기보다 Chapter 9 또는 딥러닝 장에서 다루는 편이 좋다.
- Software 2.0은 원문 로컬 확보가 실패했으므로 본문 핵심 근거로 사용하지 않는다.
- LLM의 직접 발전사는 Part 5에서 별도 근거로 분리한다.

## 반영 원칙

앞으로 위 Section을 수정할 때는 다음 기준을 적용한다.

1. 사전·공식 정의·교재·학술 리뷰는 핵심 개념 정의에 사용할 수 있다.
2. 개인 블로그, 에세이, 제품 문서, 검색 결과는 보조 관점이나 용어 사용례로만 사용한다.
3. 사용자의 해석은 `작업 가설` 또는 `학습용 일반화`로 보존하되, 표준 설명처럼 쓰지 않는다.
4. Section의 중심 질문과 직접 관련이 약한 근거는 본문에 길게 넣지 않고 관리 문서나 후속 Section 후보로 둔다.
5. 근거의 학술적 일반화 가능성이 높아도 본문 중요도가 낮으면 짧게만 언급한다.

## 이번 재검토 결론

이번 재검토에서 즉시 본문을 수정해야 할 정도의 오류는 발견하지 못했다. 다만 근거의 역할을 다음처럼 낮춰 보아야 할 항목이 있다.

- 1.1의 DSS/BI/DW/OLAP: AI 정의의 핵심이 아니라 데이터 기반 의사결정 배경
- 2.1의 KCI 검색 결과: symbolic AI 정의 근거가 아니라 한국어 표현 선택 보조 근거
- 2.3의 Software/workflow 관점: 학술 정의가 아니라 사용자 관점의 학습용 일반화
- `직관적 추론` 표현: 그대로 사용하지 않고 `직관적 패턴 판단`, `machine perception`, `inference`, `reasoning`으로 분해

따라서 1.1, 1.2, 1.3, 2.1, 2.2, 2.3은 현재 본문 구조를 유지하되, 이후 수정 시 위 반영 원칙을 적용한다.

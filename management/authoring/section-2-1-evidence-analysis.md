# 2.1 Section 근거 분석

## 목적

이 문서는 `docs/chapters/chapter-02/section-01.md`의 핵심 주장과 참고 자료가 실제로 연결되는지 검토한 관리 메모입니다.

원문 확인 규칙에 따라 가능한 자료는 `.tmp/section-01-evidence/`, `.tmp/section-04-evidence/`, `.tmp/section-2-1-korean-terms/`, `.tmp/section-2-1-labeling-evidence/` 아래에 임시로 내려받아 확인했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 원문 확인 상태

| 자료 | 로컬 확인 상태 | 2.1에서의 역할 |
| --- | --- | --- |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | HTML 다운로드 확인 | logicist AI, symbolic reasoning, non-logicist AI, machine learning과 neural network 흐름을 구분하는 보조 근거 |
| Stanford Encyclopedia of Philosophy, `Logic-Based Artificial Intelligence` | HTML 다운로드 확인 | McCarthy, commonsense reasoning, logic-based AI, knowledge representation, expert systems와 rules 설명의 직접 근거 |
| AIMA 공식 사이트 | HTML 다운로드 확인 | AI 교재 목차에서 logical agents, first-order logic, inference, knowledge representation, uncertain reasoning이 핵심 영역으로 배치되는 보조 근거 |
| 한국학술지인용색인(KCI) 논문 검색 | 검색 결과 HTML 다운로드 확인 | `symbolic AI`의 한국어 표현 후보가 학술 검색에서 어떻게 잡히는지 확인하는 보조 근거 |
| Google for Developers, `Machine Learning Glossary` | HTML 다운로드 확인 | label, labeled example, supervised machine learning 정의 확인 |
| Google for Developers, `Supervised Learning` | HTML 다운로드 확인 | 지도학습에서 labeled examples, features, labels의 관계 설명 확인 |

## 한국어 용어 후보 검토

KCI 논문 검색에서 다음 표현을 확인했습니다. KCI 검색은 형태소·분리 검색의 영향을 받을 수 있으므로, 단순 건수보다 제목에 실제 패러다임 용어가 직접 등장하는지를 함께 보았습니다.

| 검색어 | KCI 결과 | 검토 |
| --- | ---: | --- |
| `상징주의 AI` | 3건 | 결과 수가 적고, 제목 사례는 AI 패러다임 용어라기보다 예술·상징 해석 문맥이 섞임 |
| `기호주의 AI` | 7건 | 제목 사례는 기호학, 종교, 언어학, 인공신경망 논의 등이 섞여 있어 용어 정착 근거로 약함 |
| `상징적 AI` | 22건 | `신경-상징적 AI`처럼 직접 관련 사례가 있으나, 예술·상징 연구 문맥도 많이 섞임 |
| `심볼릭 인공지능` | 2건 | `심볼릭 인공지능을 위한 R 심볼릭 데이터분석`처럼 직접 제목 사례가 있음 |
| `symbolic AI` | 26건 | `뉴로-심볼릭`, `신경-상징적 AI`, `심볼릭 인공지능` 관련 제목이 함께 잡힘 |
| `기호 기반 인공지능` | 0건 | 설명어로는 명확하지만 KCI 제목 검색에서는 확인되지 않음 |
| `규칙 기반 인공지능` | 19건 | `규칙 기반`, `규칙기반 AI`의 실제 사용례가 확인됨. 다만 symbolic AI 전체가 아니라 구현 방식에 가까움 |

결론: `상징주의 AI`는 사용자의 독서 경험상 낯설고, KCI 검색에서도 강한 정착 표현으로 보기 어렵습니다. 본문 기본 표현은 의미가 투명한 `기호 기반 AI(symbolic AI)`로 두고, 국내 자료에서 확인되는 `심볼릭 인공지능`, `상징적 AI`는 보조 표현으로 설명합니다. `상징주의 AI`, `기호주의 AI`는 의미 전달은 가능하지만 이 책의 기본 표현으로 쓰지 않습니다.

## 본문 주장별 검토

| 본문 위치 | 핵심 주장 | 근거 연결 | 판정 |
| --- | --- | --- | --- |
| `section-01.md:3-5` | 2.1은 기호 기반 AI와 규칙 기반 접근을 다룬다 | 목차 기준과 1.1, 1.3의 용어 관계를 이어받는 구조. `symbolic AI`는 SEP에서 symbolic reasoning, symbolic paradigm 등으로 확인됨 | 유지 가능 |
| `section-01.md:14-22` | 기호 기반 AI와 규칙 기반 접근은 지식을 명시적으로 표현하고 추론하려는 초기 AI의 중요한 문제 해결 전략으로 등장했다 | SEP logic-AI는 McCarthy가 philosophical logic으로 commonsense reasoning을 formalize하려 했다고 설명하고, 초기 expert systems가 large systems of procedural rules에 기반했으며 이후 knowledge representation component가 강조되었다고 설명함 | 유지 가능 |
| `section-01.md:24-41` | `symbolic AI`의 symbol은 문학적 상징이 아니라 컴퓨터가 조작할 수 있는 명시적 표식으로 이해한다 | SEP AI는 symbolic, non-symbolic, logicist, non-logicist를 구분하고, SEP logic-AI는 symbolic representations와 knowledge representation을 설명함. KCI 검색 결과를 바탕으로 한국어 기본 표현은 `기호 기반 AI`로 조정함 | 유지 가능 |
| `section-01.md:45-59` | 기호 기반 AI는 기호, 규칙, 지식 표현, 추론, 탐색을 중심으로 한다 | SEP `Logic-Based Artificial Intelligence`는 논리, 추론, 지식 표현, expert systems, procedural rules를 설명함. AIMA 목차도 logical agents, inference, knowledge representation을 주요 영역으로 둠 | 유지 가능 |
| `section-01.md:61-103` | 규칙 기반 접근은 조건, 상황, 패턴에 따라 결론이나 행동을 정하는 명시적 규칙을 사용한다 | SEP logic-AI의 expert systems와 procedural rules 설명을 바탕으로 한 학습용 일반화. `IF-THEN`은 설명용 표기 예로만 제한하고, 생활 판단, 업무 처리, 분류, 접근 제어, 추천, 안전 정책 예시는 이해를 돕기 위한 일반화 예시로 둠 | 유지 가능 |
| `section-01.md:105-117` | McCarthy와 논리 기반 AI는 상식 추론을 형식화하려 했다 | SEP logic-AI는 McCarthy가 logical formalization과 commonsense reasoning을 AI에 적용하려 했다고 설명함 | 유지 가능 |
| `section-01.md:119-129` | 규칙 기반 접근은 설명 가능성과 통제 가능성이 강하다 | SEP logic-AI는 knowledge representation component, retrieval, maintenance, reasoning systems를 설명함. 설명 가능성은 규칙 기반 시스템의 일반적 장점을 바탕으로 한 학습용 정리 | 유지 가능 |
| `section-01.md:131-145` | 현실 세계의 모호함, 예외, 대규모 인식 문제는 규칙 기반 접근의 한계가 될 수 있다 | SEP AI는 symbolic paradigm에 대한 비판, non-logicist AI, neural networks, machine learning 흐름을 설명함 | 유지 가능 |
| `section-01.md:147-155` | 데이터 라벨은 학습 데이터 안의 명시적 이름표로서 기호처럼 볼 수 있지만, 데이터 라벨링과 기호 기반 AI를 같은 것으로 보지는 않는다 | Google ML Glossary는 label을 supervised machine learning에서 모델이 예측하는 부분으로 설명하고, labeled example은 feature와 label로 구성된다고 설명함. Google Supervised Learning은 모델이 features와 labels의 관계를 학습한다고 설명함. “기호처럼 볼 수 있다”는 표현은 SEP의 symbolic representations와 연결한 저자적 일반화이므로 약한 표현으로 제한 | 유지 가능 |
| `section-01.md:159-165` | 기호 기반 AI는 실패한 과거가 아니라 지식과 추론 문제를 이해하는 출발점이다 | SEP logic-AI는 논리 기반 AI가 여전히 knowledge representation과 관련 있음을 설명함. 현대 AI 서비스에서 규칙이 쓰인다는 문장은 일반적 설계 관점으로, 구체 사례는 후속 서비스 구조 장에서 보강 필요 | 유지 가능 |

## 일반화 문구

사용자의 재학습 관점에서는 다음처럼 정리할 수 있습니다.

> 기호 기반 AI는 지식을 사람이 읽을 수 있는 기호와 규칙으로 표현하고, 그 표현 위에서 추론과 탐색을 수행하려 한 접근입니다. 이 접근은 설명 가능성과 통제 가능성이 강하지만, 현실 세계의 모호함과 예외, 대규모 패턴 인식에는 한계를 보였습니다.

## 수정 반영

- “상징주의 AI”라는 표현이 낯설 수 있어, 상징을 컴퓨터가 조작할 수 있는 명시적 표식으로 설명하는 문단을 추가했습니다.
- `symbolic AI`, `logic-based AI`, `rule-based approach`, `classical AI`의 관계를 표로 분리했습니다.
- `classical AI`는 범위가 넓은 표현이므로 본문에서 문맥 확인이 필요하다고 제한했습니다.
- KCI 검색 결과를 반영해 본문 기본 표현을 `상징주의 AI`에서 `기호 기반 AI(symbolic AI)`로 조정했습니다.
- 국내 자료에서 보이는 `심볼릭 인공지능`, `상징적 AI`는 보조 표현으로 남기고, `상징주의 AI`, `기호주의 AI`는 기본 표현으로 쓰지 않도록 정리했습니다.
- 데이터 라벨링과의 관계는 “느슨한 연결”로만 추가했습니다. 라벨이 명시적 이름표라는 점은 설명하되, 데이터 라벨링을 기호 기반 AI와 동일시하지 않도록 제한했습니다.
- 기호 기반 AI와 규칙 기반 접근의 등장 배경을 추가했습니다. McCarthy의 commonsense reasoning 형식화, 초기 expert systems의 procedural rules, knowledge representation 흐름을 근거로 제한했습니다.
- `IF-THEN`은 규칙 기반 접근의 일반형이 아니라 설명용 표기 예로 낮추고, 본문 기본 설명은 조건, 상황, 패턴, 결론, 행동, 처리 절차로 일반화했습니다.
- 규칙 기반 접근의 예시를 생활 판단, 업무 처리, 분류, 접근 제어, 추천, 안전 정책으로 넓혀 `IF-THEN` 문법 자체보다 규칙 적용 구조를 이해하도록 보강했습니다.

## 범위 조정

- 전문가 시스템은 2.1에서 대표 사례로만 언급합니다. 구체적인 구조, 장점, 한계는 3.1에서 다룹니다.
- 휴리스틱은 탐색과 연결되는 중요한 개념이지만, 2.1에서는 기호 기반 AI의 주변 요소로만 언급합니다. 본격 설명은 3.1 또는 탐색·휴리스틱 Section에서 다룹니다.
- 확률적 추론과 머신러닝으로 넘어가는 흐름은 2.2, 2.3에서 다룹니다.

## 추가 보강 필요

- Logic Theorist, General Problem Solver, MYCIN, DENDRAL 같은 대표 사례는 Chapter 2 후속 Section 또는 3.1에서 별도 근거를 내려받아 검토합니다.
- 규칙 기반 시스템의 현대적 사용 예시는 실제 서비스 아키텍처 장에서 공식 문서나 구현 사례를 근거로 보강합니다.

## 출처와 참고 자료

- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/), 2018-07-12, 확인 날짜: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Richmond H. Thomason, [Logic-Based Artificial Intelligence](https://plato.stanford.edu/entries/logic-ai/), substantive revision 2024-02-27, 확인 날짜: 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed.](https://aima.cs.berkeley.edu/), 확인 날짜: 2026-06-22.
- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary), 확인 날짜: 2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised), 확인 날짜: 2026-06-22.
- 한국학술지인용색인(KCI), [논문 검색](https://www.kci.go.kr/kciportal/po/search/poArtiSear.kci), 검색어: `상징주의 AI`, `기호주의 AI`, `상징적 AI`, `심볼릭 인공지능`, `symbolic AI`, `기호 기반 인공지능`, `규칙 기반 인공지능`, 확인 날짜: 2026-06-22.

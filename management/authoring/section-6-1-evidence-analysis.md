# 6.1 근거 검토 메모

이 문서는 `docs/chapters/chapter-06/section-01.md`의 근거 연결과 범위 판단을 기록한 관리 메모입니다.

## 작성 목적

- Module 3 `불확실성과 문제 해결`의 도입으로, 규칙 기반 접근이 유효한 조건과 현실 문제가 규칙만으로 처리하기 어려운 이유를 구분합니다.
- 2.2의 탐색, 지식 표현, 확률 추론 설명을 반복하지 않고, Chapter 6-8로 이어지는 짧은 도입 역할로 제한합니다.
- 사용자의 “현상을 확률로 풀려는 시도”라는 직관을 표준 AI 개론의 불완전 정보, 부분 관측, 불확실성, 탐색 문제로 일반화합니다.
- 독자가 먼저 사례를 관찰한 뒤, 정보 부족, 부분 관측, 잡음, 예외, 후보 폭증이라는 조건을 스스로 연결할 수 있도록 예시 기반 도입으로 구성합니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| AIMA 4th US ed., Full Table of Contents | `.tmp/section-2-2-evidence/aima-contents.html` | 탐색, 휴리스틱 탐색, 부분 관측 환경, 불확실한 지식과 추론이 AI 개론의 주요 축으로 배치됨 |
| Poole & Mackworth, Chapter 3 `Searching for Solutions` | `.tmp/section-2-2-evidence/poole-mackworth-ch3-search.html` | 에이전트가 목표 달성 방법을 찾는 문제를 탐색으로 설명하는 근거 |
| Poole & Mackworth, Chapter 9 `Reasoning with Uncertainty` | `.tmp/section-2-2-evidence/poole-mackworth-ch9-uncertainty.html`, `.tmp/section-2-2-evidence/poole-mackworth-ch9-s1-probability.html` | 불확실한 상황에서 관측한 evidence를 바탕으로 믿음을 갱신하고 random variable, possible worlds 등을 사용한다는 배경 |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | `.tmp/section-01-evidence/sep-ai.html` | probabilistic inference, uncertainty, Bayesian networks, 확률적 기법의 역할에 대한 보조 근거 |

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 규칙은 조건과 행동이 명확한 문제에서 강하다 | 3.1의 규칙 기반 시스템 논의와 이어지는 일반화 | 유지. 단, 6.1에서는 규칙 기반 접근의 장단점 반복을 피함 |
| 현실 문제는 정보 부족, 잡음, 예외, 후보 폭증 때문에 규칙만으로 닫히기 어렵다 | AIMA의 partially observable environments, uncertain knowledge and reasoning, Poole & Mackworth의 uncertainty/evidence/search 논의 | 유지 |
| 고객 문의, 얼굴 인식, 자율주행 예시는 규칙이 필요한 동시에 규칙만으로 닫히기 어려운 문제를 보여 준다 | 3.1의 규칙 기반 사례 논의, AIMA/Poole & Mackworth의 부분 관측·불확실성·탐색 축 | 유지. 개별 사례의 기술사는 다루지 않고 생각을 여는 입문 예시로 제한 |
| 관측한 정보는 절대 사실이 아니라 evidence로 다뤄질 수 있다 | Poole & Mackworth Chapter 9의 evidence, observation, belief update 설명 | 유지. 수식과 조건부 확률 계산은 6.2 이후로 넘김 |
| 탐색은 규칙의 반대가 아니라 가능한 행동과 후보를 다루는 방법이다 | Poole & Mackworth Chapter 3, AIMA search 관련 목차 | 유지. 탐색 알고리즘 세부는 Chapter 7로 넘김 |
| 현대 AI 시스템은 규칙, 학습 모델, 확률적 판단, 검색, 사람 검토를 조합한다 | 3.1, 5장, 2.2의 흐름을 바탕으로 한 학습용 일반화 | 유지. 서비스 아키텍처 설계로 확장하지 않음 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 3.1 | 규칙 기반 시스템의 강점과 한계 |
| 5.1-5.3 | 학습(learning), 모델 실행(inference), 한국어 추론 표현의 혼동 |
| 6.1 | 규칙만으로 처리하기 어려운 불완전한 현실 문제의 조건을 도입 |
| 6.2 | 확률(probability), 불확실성(uncertainty), 확률적 과정(stochastic) 용어 구분 |
| 6.3 | 분류, 예측, 생성에서 확률적 판단이 쓰이는 위치 |
| Chapter 7 | 탐색 공간, 계산 한계, 휴리스틱 |
| Part 5 | RAG, Agent, 서비스 아키텍처의 구체 구조 |

## 보수화한 표현

- “규칙은 실패했다”라고 쓰지 않았습니다. 규칙은 여전히 정책, 안전, 권한, 절차에 필요하다고 명시했습니다.
- “현실은 철학적으로 열린 세계다”라고 단정하지 않았습니다. 본문 표현은 `규칙만으로 처리하기 어려운 문제`라는 입문용 작업 기준으로 일반화했습니다.
- 확률 계산, 베이즈 규칙, stochastic의 정의는 6.2 이후로 넘겼습니다.
- 휴리스틱을 확률과 같은 것으로 설명하지 않았습니다. 후보가 많아질 때 Chapter 7에서 다룰 문제로 연결만 했습니다.
- 서비스 아키텍처 그림은 실제 설계도가 아니라 여러 접근의 조합을 이해하기 위한 개념도라고 제한했습니다.

## 확인한 원문 위치

- `.tmp/section-2-2-evidence/aima-contents.html`
  - search와 heuristic search: 97-121행 부근
  - partially observable environments: 137-145행 부근
  - uncertainty 관련 장: 346행 이후
- `.tmp/section-2-2-evidence/poole-mackworth-ch3-search.html`
  - searching for a sequence of actions: 102행 부근
- `.tmp/section-2-2-evidence/poole-mackworth-ch9-s1-probability.html`
  - uncertainty/evidence/belief update: 123-153행, 376-418행, 602-612행 부근
- `.tmp/section-01-evidence/sep-ai.html`
  - probabilistic inference와 uncertainty: 2247-2256행 부근

## 남은 검토 사항

- 6.2에서 `uncertainty`, `probability`, `stochastic`, `randomness`, `nondeterminism`의 경계를 별도 근거로 정리해야 합니다.
- 7장에서 휴리스틱을 확률과 혼동하지 않도록 AIMA와 Newell/Simon, bounded rationality 근거를 다시 확인합니다.
- 현대 AI 서비스의 규칙/모델/사람 검토 조합은 Part 5 또는 프로젝트 장에서 실제 아키텍처 근거를 따로 확보합니다.

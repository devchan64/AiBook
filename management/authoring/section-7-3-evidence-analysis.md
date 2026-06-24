# 7.3 근거 검토 메모

이 문서는 `docs/parts/part-01/chapter-07/section-03.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- 사용자의 “휴리스틱은 불확실성을 소프트웨어에 반영한 시도”라는 직관을 표준적인 용어 경계 안에서 일반화합니다.
- 7.2의 휴리스틱 설명과 6.2/6.3의 확률 설명을 연결하되 반복하지 않습니다.
- 휴리스틱 점수, 확률 출력, 임계값, 운영 기준을 같은 것으로 섞지 않도록 분리합니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Poole & Mackworth, Section 3.1 `Problem Solving as Search` | `.tmp/section-2-2-evidence/poole-mackworth-ch3-s1-search-problem.html` | heuristic knowledge가 search space 바깥의 추가 지식이며 해를 찾는 방향을 안내한다는 설명 |
| Poole & Mackworth, Section 9.1 `Probability` | `.tmp/section-2-2-evidence/poole-mackworth-ch9-s1-probability.html` | probability를 믿음의 계산법으로 설명하고, 새 information/evidence에 따라 belief를 update한다는 설명 |
| AIMA 4th US ed. table of contents | `.tmp/section-2-2-evidence/aima-contents.html` | heuristic search와 probability/Bayes/Bayesian networks가 서로 다른 장으로 배치되는 개론 구조 |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-2-1-labeling-evidence/google-ml-glossary.html` | classification threshold가 사람이 선택하는 값이고 false positive/false negative에 영향을 준다는 설명 |
| scikit-learn, `Probability calibration` | `.tmp/section-6-2-evidence/scikit-learn-probability-calibration.html` | classification에서 class probability가 필요할 수 있지만, probability estimate는 calibration을 통해 신뢰성을 확인해야 한다는 설명 |
| `management/authoring/heuristics-and-ai-thinking.md` | 저장소 관리 문서 | 휴리스틱을 불확실성의 계산이 아니라 불확실성과 계산 한계 속 판단을 가능하게 하는 실용적 장치로 설명하는 내부 기준 |
| `management/authoring/section-6-3-evidence-analysis.md` | 저장소 관리 문서 | 확률 출력, calibration, threshold의 도메인 경계 |
| `management/authoring/section-7-2-evidence-analysis.md` | 저장소 관리 문서 | 휴리스틱, 현대적 휴리스틱 예시, 확률 모델과의 경계 |

## 확인한 원문 위치

- `.tmp/section-2-2-evidence/poole-mackworth-ch3-s1-search-problem.html`
  - heuristic knowledge 설명: 195-198행 부근
  - satisficing/good enough solution 설명: 184행 부근
- `.tmp/section-2-2-evidence/poole-mackworth-ch9-s1-probability.html`
  - probability가 belief calculus이며 새 information에 따라 belief를 update한다는 설명: 136-143행 부근
  - probability가 0과 1 사이 숫자로 믿음을 표현한다는 설명: 163-171행 부근
  - evidence에 따라 posterior probability로 갱신한다는 설명: 392-409행 부근
  - Bayes' rule이 새 evidence를 바탕으로 belief를 update한다고 설명: 599-612행 부근
- `.tmp/section-2-2-evidence/aima-contents.html`
  - heuristic search와 heuristic functions: 108-121행 부근
  - probability, Bayes' rule, Bayesian networks: 346-384행 부근
- `.tmp/section-2-1-labeling-evidence/google-ml-glossary.html`
  - classification threshold: 4083행 부근
  - threshold가 사람이 선택하는 값이라는 설명: 4093행 부근
  - threshold 선택이 false positive와 false negative 수에 영향을 준다는 설명: 4109행 부근
- `.tmp/section-6-2-evidence/scikit-learn-probability-calibration.html`
  - classification에서 class probability가 필요할 수 있다는 설명: 737-746행 부근
  - calibration curve가 predicted probability와 실제 fraction을 비교한다는 설명: 770-778행 부근

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 휴리스틱과 확률 모델은 모두 불확실하거나 복잡한 문제에서 쓰일 수 있지만 같은 말은 아니다 | Poole & Mackworth의 search/heuristic과 probability 장 구분, AIMA 목차 구조 | 유지 |
| 휴리스틱은 후보를 줄이고 우선순위를 정하는 기준이다 | Poole & Mackworth의 heuristic knowledge 설명, 7.2 근거 메모 | 유지 |
| 확률 모델은 불확실성을 숫자나 분포로 표현하고 근거에 따라 갱신할 수 있다 | Poole & Mackworth 9.1 probability, evidence, posterior probability 설명 | 유지 |
| 숫자가 있다고 해서 모두 확률은 아니다 | scikit-learn calibration, Google threshold, 내부 기준 | 유지 |
| classification threshold는 확률 모델 자체가 아니라 운영 기준일 수 있다 | Google ML Glossary는 threshold가 사람이 선택하는 값이라고 설명 | 유지 |
| 휴리스틱은 불확실성을 계산한다기보다 불확실성과 계산 한계 속에서 판단을 가능하게 한다 | 내부 휴리스틱 기준 문서와 7.2 근거 메모 | 유지 |
| 하나의 AI 시스템 안에서 휴리스틱, 확률 모델, 보정, 운영 기준이 함께 쓰일 수 있다 | 6.3의 확률 출력과 threshold 설명, 7.2의 현대적 휴리스틱 예시 | 유지 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 6.2 | uncertainty, probability, stochastic 용어 구분 |
| 6.3 | 확률 출력, calibration, threshold가 쓰이는 위치 소개 |
| 7.1 | 탐색 공간과 계산 한계 |
| 7.2 | 휴리스틱이 무엇을 줄이는지 |
| 7.3 | 휴리스틱과 확률 모델의 역할 차이 |
| Part 2 | 베이즈 규칙, 조건부 확률, 확률 분포의 수학 |
| Part 3 | 모델 평가, calibration, threshold tuning, hyperparameter tuning |
| Part 5 | LLM의 sampling, temperature, top-p와 생성 확률 |

## 보수화한 표현

- “휴리스틱은 불확실성을 계산한다”라는 표현은 본문 주장으로 쓰지 않았습니다.
- “휴리스틱은 불확실성과 계산 한계 속에서 판단과 탐색을 가능하게 하는 경험적 기준”으로 일반화했습니다.
- 확률 모델을 휴리스틱보다 우월한 방법으로 표현하지 않았습니다. 서로 역할이 다르다고 설명했습니다.
- `0.82` 같은 숫자를 확률로 단정하지 않고, score, model score, probability estimate, operation rule로 나뉠 수 있다고 설명했습니다.
- 임계값(threshold)은 6.3의 내용을 반복하지 않고, 확률 모델 위에 놓이는 운영 기준 또는 휴리스틱일 수 있다는 경계에 집중했습니다.
- RAG, LLM, 에이전트 예시는 개념 혼동 방지를 위한 짧은 현대적 주의점으로만 사용했습니다. 상세 구현은 Part 5와 Part 6으로 남겼습니다.

## 남은 검토 사항

- Part 3에서 calibration, threshold tuning, validation set, hyperparameter tuning을 실제 절차로 다룰 때 7.3의 구분을 다시 참조합니다.
- Part 5에서 LLM의 token probability와 프롬프트 휴리스틱을 분리해 설명합니다.
- Part 6의 AI 서비스 아키텍처에서 모델 출력, 정책 기준, 사람 검토 단계를 시스템 구성으로 다시 다룹니다.

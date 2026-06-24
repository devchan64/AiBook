# 4.4 근거 분석: 문제 정의가 모델을 결정하는 방식

이 문서는 `docs/parts/part-01/chapter-04/section-04.md`의 근거 연결을 검토한 관리 메모입니다.

원문 확인 규칙에 따라 이미 내려받은 `.tmp/` 자료를 우선 사용했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 확인한 자료

| 자료 | 로컬 확인 | 본문 반영 역할 |
| --- | --- | --- |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-4-1-evidence/google-ml-glossary.html` | task, classification model, regression model, evaluation, metric, loss, LLM evaluations 정의 확인 |
| Google for Developers, `Supervised Learning` | `.tmp/section-2-1-labeling-evidence/google-ml-terminology.html` | 지도학습에서 입력 특징과 라벨 관계를 학습한다는 설명 |
| scikit-learn, `Metrics and scoring: quantifying the quality of predictions` | `.tmp/chapter-04-reference-review/scikit-learn-model-evaluation.html` | 평가 함수 선택은 최종 목표와 적용 맥락에서 출발하고, 예측과 의사결정을 구분한다는 설명 |
| Stanford Encyclopedia of Philosophy, `Artificial Intelligence` | `.tmp/section-01-evidence/sep-ai.html` | AI 문제를 task, input, representation, performance 관점으로 설명하는 배경 근거 |

## 핵심 근거 연결

| 본문 주장 | 근거 | 반영 판단 |
| --- | --- | --- |
| 현실 목표는 모델링 과제로 좁혀야 한다 | Google ML Glossary는 task를 ML 기법으로 풀 수 있는 문제로 설명하고, classification, regression, clustering, anomaly detection을 예로 듦 | 유지 |
| 출력이 범주인지 숫자인지에 따라 과제 성격이 달라진다 | Google ML Glossary는 classification model을 class prediction, regression model을 numerical prediction으로 설명함 | 유지 |
| 평가와 지표는 모델 품질 판단에 필요하다 | Google ML Glossary는 evaluation을 모델 품질 측정/비교 과정으로, metric을 관심 있는 통계량으로 설명함 | 유지 |
| 평가 지표 선택은 적용 목표와 연결되어야 한다 | scikit-learn model evaluation 문서는 scoring function 선택이 ultimate goal과 prediction의 application에서 출발한다고 설명하고, prediction과 decision making을 구분함 | 유지. 본문에는 계산식 없이 평가 지표가 출력 사용 맥락과 연결된다는 수준으로 반영 |
| 학습 손실과 업무 평가를 구분해야 한다 | Google ML Glossary는 loss를 예측과 라벨 사이의 차이 측정으로 설명함 | 본문에서는 loss 세부 수식은 다루지 않고, 평가 기준이 출력 정의에 따라 달라진다는 수준으로만 반영 |
| LLM 평가는 성능 외 안전성과 윤리까지 포함할 수 있다 | Google ML Glossary는 LLM evaluations가 성능 비교와 안전하고 윤리적인 사용 확인에 도움이 된다고 설명함 | 생성형 AI 평가가 정확도 하나로 충분하지 않다는 보조 근거로 반영 |
| 표현 선택과 task 난이도는 연결된다 | SEP AI 항목은 feature representation이 task 난이도의 일부를 떠안을 수 있고, 올바른 representation 선택이 중요하다고 설명함 | 4.3과 연결하는 배경으로만 사용 |

## 섹션 구성 검토

| 검토 항목 | 판단 |
| --- | --- |
| 4.1과의 경계 | 모델의 의미와 모형 비유는 반복하지 않고, 문제 정의가 모델 선택의 기준이 된다는 쪽으로 확장 |
| 4.2와의 경계 | 입력/출력/데이터의 정의는 반복하지 않고, 출력 정의가 task, 데이터, 평가를 함께 바꾼다는 관계를 설명 |
| 4.3과의 경계 | 특징, 표현, 파라미터 설명은 반복하지 않고, 표현은 문제 정의와 연결된다는 수준으로만 언급 |
| Part 3와의 경계 | 분류, 회귀, 손실, 평가 지표의 수식과 알고리즘은 다루지 않고 입문적 위치만 제시 |
| LLM/생성형 AI 장과의 경계 | 생성 평가의 세부 방법은 다루지 않고, 생성형 출력은 평가 범위가 넓어진다는 관점만 제시 |
| AI 서비스 아키텍처와의 경계 | 라우팅, 권한 확인, 사람 검토, 도구 호출, 배포 후 모니터링은 설계하지 않고 후속 장으로 넘김 |

## 주의한 표현

- 문제 정의를 단순한 기획 문서가 아니라 모델링 선택의 기준으로 설명합니다.
- “좋은 모델”을 특정 알고리즘이나 큰 모델로 단정하지 않습니다.
- 분류, 회귀, 생성의 차이는 출력 형태 중심으로 설명하고 세부 알고리즘은 후속 장으로 넘깁니다.
- 정확도 하나로 업무 성과와 안전성을 모두 판단할 수 있다고 쓰지 않습니다.
- scikit-learn의 scoring function 논의는 적용 목표와 예측/의사결정 구분만 반영하고, 세부 지표 계산은 Part 3로 넘깁니다.
- 서비스 운영 흐름은 모델 출력의 사용 위치까지만 언급하고, 실제 아키텍처 설계로 확장하지 않습니다.
- 고객 문의 예시는 학습용 자체 예시입니다. 실제 서비스나 특정 조직의 라벨 체계가 아닙니다.

## 본문에 넣지 않은 내용

- accuracy, precision, recall, confusion matrix의 계산식은 Part 3에서 다룹니다.
- loss function과 optimization의 수학적 설명은 Part 3와 Part 4에서 다룹니다.
- LLM 평가 벤치마크, RAG 평가, human evaluation의 구체 절차는 LLM과 생성형 AI 장에서 다룹니다.
- 배포 후 모니터링과 A/B 테스트는 AI 서비스 아키텍처 또는 프로젝트 장에서 다룹니다.

## 검증 필요

- `모델링 과제(task)`를 본문 전체에서 `과제`, `작업`, `태스크` 중 어떤 한국어 표현으로 유지할지 용어표에서 재검토합니다.
- `업무 성과`와 `모델 성능`의 구분은 뒤의 서비스 아키텍처 장에서 다시 연결해야 합니다.

## 출처

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary/), 확인 날짜: 2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised), 확인 날짜: 2026-06-22.
- scikit-learn, [Metrics and scoring: quantifying the quality of predictions](https://scikit-learn.org/stable/modules/model_evaluation.html), 확인 날짜: 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/), 2018-07-12, 확인 날짜: 2026-06-22.

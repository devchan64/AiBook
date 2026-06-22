# Chapter 4 참고자료 후보 검토

이 문서는 4장 `문제를 모델로 바꾼다는 것`에 추가로 참고할 만한 자료를 보수적인 기준으로 검토한 관리 메모입니다.

원문 확인 규칙에 따라 후보 자료를 `.tmp/chapter-04-reference-review/`에 내려받아 검토했습니다. `.tmp/`의 원문 파일은 근거 검토용이며 저장소에 커밋하지 않습니다.

## 보수적 선정 기준

- 공식 문서, 표준기관 문서, 대학 강의 자료를 우선합니다.
- 개인 블로그, 뉴스, 마케팅 글은 4장 핵심 근거로 쓰지 않습니다.
- 본문에는 입문 수준의 일반화만 반영하고, 수식·알고리즘·평가 지표 계산은 후속 장으로 넘깁니다.
- 특정 라이브러리의 구현 관점은 일반 개념으로 바로 확장하지 않고, “참고 구현/용어 확인” 정도로 제한합니다.

## 다운로드한 후보

| 자료 | 로컬 파일 | 성격 | 4장 반영 판단 |
| --- | --- | --- | --- |
| scikit-learn User Guide, `Supervised learning` | `.tmp/chapter-04-reference-review/scikit-learn-supervised-learning.html` | 공식 라이브러리 문서 | 보조 참고. 분류/회귀 모델이 큰 범주로 나뉜다는 근거로 유용하나, 알고리즘 목록은 Part 3로 넘김 |
| scikit-learn User Guide, `Metrics and scoring: quantifying the quality of predictions` | `.tmp/chapter-04-reference-review/scikit-learn-model-evaluation.html` | 공식 라이브러리 문서 | 4.4에 가장 직접적으로 유용. 평가 함수 선택이 최종 목표와 적용 맥락에서 출발해야 한다는 근거로 적합 |
| NIST, `Artificial Intelligence Risk Management Framework (AI RMF 1.0)` | `.tmp/chapter-04-reference-review/nist-ai-rmf-1-0.pdf`, `.txt` | 표준기관 프레임워크 | 4.4의 “모델 성능과 업무/안전 평가는 다르다”는 보수적 관점에 보조 근거로 적합. 자세한 위험 관리는 윤리·보안/서비스 장으로 넘김 |
| Stanford CS229, `Machine Learning Notes` | `.tmp/chapter-04-reference-review/stanford-cs229-main-notes.pdf`, `.txt` | 대학 강의 노트 | 4장 본문에는 과도하게 수식 중심. Part 3에서 지도학습, 손실, 모델 선택 근거로 사용하는 것이 적합 |
| scikit-learn Metrics API redirect | `.tmp/chapter-04-reference-review/scikit-learn-metrics-api.html` | 리다이렉트 HTML | 근거로 사용하지 않음. `model_evaluation.html`로 대체 |

## 4장에 직접 도움이 되는 요점

| 요점 | 후보 근거 | 적용 위치 |
| --- | --- | --- |
| 현실 목표를 모델링 과제로 바꾸면 분류, 회귀 같은 과제 유형이 갈린다 | scikit-learn supervised learning, Google ML Glossary task/classification/regression | 4.4 |
| 출력 형태가 달라지면 평가 기준도 달라진다 | scikit-learn model evaluation | 4.4 |
| 어떤 scoring function을 쓸지는 최종 목표와 적용 맥락에서 출발해야 한다 | scikit-learn model evaluation | 4.4 보강 후보 |
| 예측과 의사결정은 구분할 수 있다 | scikit-learn model evaluation | 4.4 보강 후보 |
| AI 시스템의 위험과 평가는 실제 사용 맥락에 따라 달라진다 | NIST AI RMF | 4.4 보조, 후속 윤리/서비스 장 |
| 입력 특징과 목표 변수, 학습 세트라는 기본 구조는 지도학습의 표준적 설명이다 | Stanford CS229 | Part 3 우선, 4.2/4.3 보조 가능 |

## 본문 반영 권장

### 4.1

추가 반영은 권장하지 않습니다.

4.1은 모델이라는 말의 도입과 모형 비유가 핵심입니다. 이미 `Models in Science`, Google ML Glossary, Online Etymology Dictionary로 충분합니다. scikit-learn이나 CS229를 추가하면 알고리즘 도입으로 흐를 수 있습니다.

### 4.2

추가 반영은 최소화합니다.

4.2는 `입력/출력/데이터`의 기본 역할을 설명하는 절입니다. Stanford CS229의 입력 특징, 출력/타깃 변수, training set 설명은 개념적으로 잘 맞지만 수식 표기가 강하므로 본문에는 직접 끌어오지 않는 편이 안전합니다. 필요하면 관리 메모에만 보조 근거로 남깁니다.

### 4.3

추가 반영은 권장하지 않습니다.

4.3은 특징, 표현, 파라미터의 기본 위치를 잡는 절입니다. CS229의 파라미터와 feature 설명은 정확하지만 선형회귀 수식으로 빠질 위험이 큽니다. 현재 Google ML Glossary와 Bengio et al. 표현 학습 리뷰가 더 적합합니다.

### 4.4

scikit-learn `model_evaluation`의 관점은 반영 가치가 높습니다.

특히 다음 문맥은 4.4에 보수적으로 보강할 수 있습니다.

- 평가 지표는 임의로 고르는 것이 아니라 최종 목표와 적용 맥락에서 출발한다.
- 예측 결과와 그 결과를 사용한 의사결정은 구분할 수 있다.
- 지표 하나가 전체 업무 성과를 대표한다고 단정하면 안 된다.

NIST AI RMF는 다음 수준으로만 반영하는 것이 좋습니다.

- AI 시스템의 위험과 평가는 사용 맥락에 따라 달라진다.
- 운영 환경의 위험은 실험실 평가와 다를 수 있다.
- 신뢰성, 안전성, 책임성 같은 요소는 후속 장에서 별도로 다룬다.

## 반영하지 않는 편이 좋은 내용

| 내용 | 이유 |
| --- | --- |
| CS229의 손실 함수, 최적화, 모델 선택 수식 | 4장 입문 도메인을 넘어 Part 3에 해당 |
| scikit-learn 알고리즘 목록 전체 | 특정 라이브러리 구조를 커리큘럼 일반 구조로 오해할 수 있음 |
| NIST AI RMF의 조직 거버넌스 세부 항목 | 4장 문제 모델링 범위를 넘어 윤리/보안/운영 거버넌스에 해당 |
| 평가 지표 계산식 | 4.4에서는 지표 선택의 이유만 다루고 계산은 Part 3로 넘기는 것이 적절 |

## 다음 작업 후보

- 4.4에 scikit-learn `model_evaluation` 기반의 짧은 보강 문단 추가:
  - “평가 지표는 최종 목표와 적용 맥락에서 출발해야 한다.”
  - “예측과 의사결정은 구분해야 한다.”
- 4.4 근거 메모에 scikit-learn model evaluation 후보를 추가.
- Part 3 작성 전 Stanford CS229 노트를 별도 후보 문서로 재분류.

## 출처

- scikit-learn, [Supervised learning](https://scikit-learn.org/stable/supervised_learning.html), 확인 날짜: 2026-06-22.
- scikit-learn, [Metrics and scoring: quantifying the quality of predictions](https://scikit-learn.org/stable/modules/model_evaluation.html), 확인 날짜: 2026-06-22.
- NIST, [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf), 2023-01, 확인 날짜: 2026-06-22.
- Stanford University, Andrew Ng et al., [CS229 Machine Learning Notes](https://cs229.stanford.edu/main_notes.pdf), 확인 날짜: 2026-06-22.

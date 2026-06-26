# P3-6.1 근거 검토: 평가 지표(metric)의 역할

## 검토 대상

- Section: `docs/parts/part-03/chapter-06/section-01.md`
- 작성일: 2026-06-26
- 목적: 초심자 기준으로 평가 지표가 왜 여러 개 필요한지 설명한다.

## 사용한 근거

### scikit-learn, Metrics and scoring: quantifying the quality of predictions

- URL: https://scikit-learn.org/stable/modules/model_evaluation.html
- 확인 날짜: 2026-06-26
- 핵심 확인:
  - 평가 지표 선택은 결국 예측을 무엇에 사용할지와 연결된다고 설명한다.
  - 예측(prediction)과 의사결정(decision making)을 구분해 설명한다.
  - 분류와 회귀에서 서로 다른 scoring function과 metric이 쓰인다는 큰 구조를 제공한다.
- 본문 반영:
  - 지표를 단순 점수판이 아니라 목적과 결정 기준이 들어간 선택 기준으로 설명했다.
  - 다음 절에서 문제 유형별 평가 기준으로 나누어 보는 흐름의 배경 근거로 사용했다.

### C. J. van Rijsbergen, Information Retrieval, Chapter 7. Evaluation

- URL: https://www.dcs.gla.ac.uk/Keith/pdf/Chapter7.pdf
- 확인 날짜: 2026-06-26
- 핵심 확인:
  - 평가의 이유를 사회적(social) 질문과 경제적(economic) 질문으로 설명한다.
  - Cyril Cleverdon이 제시한 측정 항목들 가운데 recall과 precision을 검색 시스템 효과성(effectiveness)의 핵심 측정치로 다룬다.
  - precision-recall 그래프와 평가 절차를 정보 검색 평가의 표준적 접근으로 설명한다.
- 본문 반영:
  - 평가 지표의 역사적 배경을 정보 검색과 사용자 만족·비용 문제에서 시작된 흐름으로 설명했다.
  - 지표가 단순한 수식이 아니라 실제 도움이 되는가, 피해를 줄이는가의 질문과 연결된다는 문장에 사용했다.

### Google for Developers, Machine Learning Glossary

- URL: https://developers.google.com/machine-learning/glossary/
- 확인 날짜: 2026-06-26
- 핵심 확인:
  - accuracy를 전체 예측 중 맞춘 비율로 정의한다.
  - class-imbalanced dataset에서는 accuracy가 매우 misleading할 수 있다고 설명한다.
  - recall을 `실제 양성을 얼마나 제대로 잡았는가`의 질문으로 정의한다.
  - confusion matrix를 정답/오답 예측을 요약하는 표로 설명한다.
  - false positive, false negative의 기본 정의를 제공한다.
- 본문 반영:
  - 정확도, 재현율, 혼동 행렬, FP/FN의 초심자 정의에 사용했다.
  - 정확도 하나만으로는 부족할 수 있다는 설명의 근거로 사용했다.

## 일반화한 문장

- “평가 지표는 모델 결과를 숫자로 요약하면서, 어떤 오류를 더 중요하게 보는지도 함께 드러내는 기준이다.”
- “정확도는 출발점일 수 있지만, 불균형 데이터나 비용이 다른 오류 구조에서는 충분하지 않을 수 있다.”
- “정밀도와 재현율은 서로 다른 질문에 답하므로, 같은 정확도라도 모델 해석이 달라질 수 있다.”
- “지표 선택은 수학 공식만의 문제가 아니라 예측을 어떤 결정에 연결할지의 문제이기도 하다.”
- “평가 지표는 정보 검색에서 효과성과 사용자 만족을 따지던 문제의식이 머신러닝 평가로 이어진 결과로 볼 수 있다.”
- “사회현상에 모델을 적용할 때는 오류가 누구에게 어떤 비용으로 돌아가는지까지 포함해 지표를 읽어야 한다.”

## 검토한 경계

- 이 절은 지표의 역할을 설명하는 도입 절이다.
- ROC-AUC, PR-AUC, log loss, calibration 같은 세부 지표는 다루지 않는다.
- 회귀 지표와 군집화 지표의 구체 예시는 P3-6.2 이후로 넘긴다.
- threshold tuning과 비용 민감한 최적화는 뒤 절에서 더 다룰 수 있다.

## 검증 필요

- P3-6.2에서 분류, 회귀, 군집화별 지표를 나눌 때 현재 절의 `지표는 질문이다`라는 관점을 다시 연결할 필요가 있다.
- 이후 threshold와 confusion matrix를 더 자세히 다루는 절이 생기면 FP/FN 비용 차이를 확장할 수 있다.

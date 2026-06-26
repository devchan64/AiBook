# P3-5.2 근거 검토: 일반화(generalization)

## 검토 대상

- Section: `docs/parts/part-03/chapter-05/section-02.md`
- 작성일: 2026-06-26
- 목적: 초심자 기준으로 일반화의 의미를 설명한다.

## 사용한 근거

### Google for Developers, Machine Learning Glossary

- URL: https://developers.google.com/machine-learning/glossary
- 확인 날짜: 2026-06-26
- 핵심 확인:
  - generalization은 training set에 없는 example에서도 좋은 예측을 할 수 있는가의 질문으로 설명된다.
  - regularization은 training data의 peculiarities에 덜 정확히 맞추도록 도와 generalization을 장려한다고 설명한다.
- 본문 반영:
  - 일반화를 `보지 못한 데이터에서도 쓸 만하게 작동하는 성질`로 일반화했다.
  - 일반화가 학습 점수와 다른 목표라는 설명의 배경 근거로 사용했다.

### scikit-learn, Cross-validation: evaluating estimator performance

- URL: https://scikit-learn.org/stable/modules/cross_validation.html
- 확인 날짜: 2026-06-26
- 핵심 확인:
  - 같은 데이터로 학습과 테스트를 함께 하면 methodological mistake라고 설명한다.
  - overfitting은 방금 본 sample label을 반복하는 모델이 perfect score를 얻더라도 useful prediction에는 실패하는 상황으로 제시된다.
  - validation set과 test set 구분이 generalization performance 보고를 위해 필요하다고 설명한다.
- 본문 반영:
  - 검증과 테스트를 일반화 확인 장치로 설명했다.
  - 과적합이 일반화 약화로 이어질 수 있다는 문장을 뒷받침했다.

### An Introduction to Statistical Learning

- URL: https://www.statlearning.com/
- 확인 날짜: 2026-06-26
- 핵심 확인:
  - resampling methods, model selection, regularization 등으로 이어지는 통계학습의 핵심 흐름을 제공한다.
- 본문 반영:
  - 일반화가 평가, 재표본추출, 모델 선택으로 이어지는 큰 흐름의 일부라는 배경 참고 자료로 사용했다.

### Ulrike von Luxburg, Bernhard Schoelkopf, Statistical Learning Theory: Models, Concepts, and Results

- URL: https://is.mpg.de/publications/4179
- 확인 날짜: 2026-06-26
- 핵심 확인:
  - 통계학습이론(statistical learning theory)이 1960년대 러시아에서 시작되었다고 설명한다.
  - 1990년대 서포트 벡터 머신(SVM)의 발전과 함께 널리 알려졌다고 설명한다.
  - 핵심 질문을 경험적 데이터(empirical data)로부터 타당한 결론을 이끄는 문제로 제시한다.
- 본문 반영:
  - 일반화가 최근 생성형 AI에서 갑자기 생긴 말이 아니라, 통계학습이론의 오래된 핵심 질문이라는 역사적 배경 설명에 사용했다.

## 일반화한 문장

- “일반화는 모델이 아직 보지 못한 데이터에서도 쓸 만하게 작동하는 성질이다.”
- “머신러닝의 실제 목표는 학습 점수 자체가 아니라 일반화다.”
- “과적합과 과소적합은 모두 일반화를 약하게 만들 수 있다.”
- “검증과 테스트는 결국 일반화를 가늠하기 위한 장치다.”
- “일반화는 아무 데이터에나 통한다는 뜻이 아니라, 같은 문제의 보지 못한 예시에서 버티는 힘에 더 가깝다.”
- “일반화는 통계학습이론에서 오래 다루어진 질문이며, 현대 실무의 검증과 테스트 관행으로 이어진다.”

## 검토한 경계

- 이 절은 일반화의 의미에 집중한다.
- 일반화 오차의 수식, 이론 경계, 편향-분산(bias-variance) 세부는 다루지 않는다.
- 평가 지표(metric)의 구체 계산은 P3-6으로 넘긴다.
- 정규화, 조기 종료 등 일반화 개선 기법은 이후 장으로 넘긴다.

## 검증 필요

- P3-6에서 지표를 설명할 때 일반화와 지표 해석의 관계를 다시 연결할 필요가 있다.
- 이후 개별 모델 장에서 일반화가 모델별로 어떻게 다르게 보이는지 사례를 덧붙일 수 있다.

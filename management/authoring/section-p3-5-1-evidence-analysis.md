# P3-5.1 근거 검토: 과적합(overfitting)과 과소적합(underfitting)

## 검토 대상

- Section: `docs/parts/part-03/chapter-05/section-01.md`
- 작성일: 2026-06-26
- 목적: 초심자 기준으로 과적합과 과소적합의 차이를 설명한다.

## 사용한 근거

### scikit-learn, Underfitting vs. Overfitting

- URL: https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html
- 확인 날짜: 2026-06-26
- 핵심 확인:
  - 너무 단순한 함수는 학습 샘플을 충분히 설명하지 못해 underfitting이 된다.
  - 더 높은 복잡도는 학습 데이터를 잘 맞추지만, 지나치면 noise까지 배우며 overfitting이 된다.
  - 예시에서는 cross-validation으로 그 차이를 정량적으로 본다.
- 본문 반영:
  - 단순 모델 / 적절한 모델 / 너무 복잡한 모델의 대비 설명
  - 학습 데이터의 noise를 함께 배우는 과적합 설명

### Google for Developers, Machine Learning Glossary

- URL: https://developers.google.com/machine-learning/glossary
- 확인 날짜: 2026-06-26
- 핵심 확인:
  - overfitting: training data에 너무 밀착하여 new data에서 예측이 약해지는 상태
  - underfitting: training data의 complexity를 충분히 포착하지 못해 predictive ability가 낮은 상태
  - generalization: training set에 없는 example에서도 좋은 예측을 하는가의 질문
- 본문 반영:
  - 초심자 정의 문장
  - 학습 데이터와 새 데이터의 차이를 함께 읽는 설명

### An Introduction to Statistical Learning

- URL: https://www.statlearning.com/
- 확인 날짜: 2026-06-26
- 핵심 확인:
  - resampling methods, model selection, regularization 등으로 이어지는 통계학습 입문 구조를 제공한다.
- 본문 반영:
  - 이 절을 이후 일반화, 모델 선택, 정규화 논의와 연결하는 배경 참고 자료로 사용했다.

## 일반화한 문장

- “과소적합은 아직 중요한 패턴을 충분히 배우지 못한 상태다.”
- “과적합은 학습 데이터의 우연한 흔들림까지 너무 따라간 상태다.”
- “학습 점수가 높다고 곧바로 좋은 모델이라고 말할 수는 없다.”
- “학습 점수와 검증 점수를 함께 봐야 과적합과 과소적합을 더 잘 구분할 수 있다.”

## 검토한 경계

- 이 절은 상태 구분에 집중한다.
- 일반화의 더 넓은 의미는 P3-5.2로 넘긴다.
- 정규화, 조기 종료, 드롭아웃 같은 완화 기법은 다루지 않는다.
- 모델별 과적합 사례는 이후 개별 모델 장에서 다시 다룰 수 있다.

## 검증 필요

- P3-5.2에서 일반화와 연결할 때 “학습/검증 차이”와 “미보았던 데이터에서의 안정성”을 더 체계적으로 연결할 필요가 있다.
- 이후 회귀, 트리, 딥러닝 장에서 과적합 사례를 모델별로 다시 연결할 수 있다.

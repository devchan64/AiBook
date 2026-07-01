# P3-16.1 그래디언트 부스팅 근거 메모

## Section 역할

- Part 3 Module 5 Chapter 16의 첫 번째 절입니다.
- 랜덤포레스트 다음에, 트리 앙상블의 다른 축인 그래디언트 부스팅을 입문적으로 소개합니다.
- 초심자에게 `병렬 집계`와 `순차 보정`의 차이를 분명히 만드는 절입니다.

## 핵심 주장

1. 그래디언트 부스팅은 weak learner를 순차적으로 결합하는 앙상블 방식이다.
2. 각 단계는 이전 단계가 남긴 오차를 줄이는 방향으로 추가된다.
3. gradient boosting 모델은 additive model로 이해할 수 있다.
4. `learning_rate`는 각 weak learner의 기여를 축소(shrinkage)하는 값이다.
5. 작은 `learning_rate`는 보통 더 많은 weak learner, 즉 더 큰 `n_estimators`를 필요로 한다.
6. 랜덤포레스트와 그래디언트 부스팅은 모두 트리 앙상블이지만 학습 철학이 다르다.

## 근거 출처

### 1) scikit-learn User Guide - ensemble

- 문서: `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`
- URL: https://scikit-learn.org/stable/modules/ensemble.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-ensemble.html`

### 2) Friedman 2001

- 논문: Jerome H. Friedman, `Greedy Function Approximation: A Gradient Boosting Machine`

### 3) Friedman 2002

- 논문: Jerome H. Friedman, `Stochastic Gradient Boosting`

## 제외한 내용

- 손실 함수의 엄밀한 미분 전개
- multi-class 분류의 세부 수학
- early stopping, subsampling, regularization 세부 옵션
- XGBoost / LightGBM / CatBoost의 구조적 차이

이 내용은 P3-16.2 이후 성능과 위험, 또는 후속 심화 Part에서 다시 다룰 수 있습니다.

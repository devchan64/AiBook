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
- 반영 포인트:
  - gradient boosting이 boosting을 differentiable loss로 일반화한 방식이라는 설명
  - weak learner를 고정 크기의 regression tree로 설명한 부분
  - additive model 설명
  - `n_estimators`가 반복 횟수/weak learner 수라는 설명
  - learning rate가 shrinkage이며 작은 값일수록 더 많은 weak learner가 필요하다는 설명
  - HGBT와 ordinary gradient boosting 소개

### 2) Friedman 2001

- 논문: Jerome H. Friedman, `Greedy Function Approximation: A Gradient Boosting Machine`
- 반영 포인트:
  - gradient boosting의 대표 이론적 출발점
  - additive model과 greedy stage-wise fitting의 배경

### 3) Friedman 2002

- 논문: Jerome H. Friedman, `Stochastic Gradient Boosting`
- 반영 포인트:
  - shrinkage와 subsampling이 일반화 성능에 미치는 영향의 역사적 배경

## 집필 판단

- 16.1에서는 수식보다 `이전 오차를 다음 단계가 고친다`는 감각을 우선했습니다.
- scikit-learn이 분류와 회귀 모두를 다루지만, 초심자 설명은 residual이 직관적으로 보이는 회귀 예제로 먼저 열었습니다.
- 저장소 의존성에 `scikit-learn`이 아직 포함되어 있지 않으므로, 실행 가능한 작은 Python 리스트 예제를 우선 사용했습니다.
- 구현체 비교(XGBoost, LightGBM, CatBoost)는 16.1의 범위를 벗어나므로 넣지 않았습니다.

## 제외한 내용

- 손실 함수의 엄밀한 미분 전개
- multi-class 분류의 세부 수학
- early stopping, subsampling, regularization 세부 옵션
- XGBoost / LightGBM / CatBoost의 구조적 차이

이 내용은 P3-16.2 이후 성능과 위험, 또는 후속 심화 Part에서 다시 다룰 수 있습니다.

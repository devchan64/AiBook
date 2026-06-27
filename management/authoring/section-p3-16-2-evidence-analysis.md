# P3-16.2 부스팅의 성능과 위험 근거 메모

## Section 역할

- Part 3 Module 5 Chapter 16의 두 번째 절입니다.
- 16.1에서 부스팅의 순차 보정 구조를 설명한 뒤, 왜 성능이 강해 보이면서도 튜닝과 과적합 관리가 중요한지 설명합니다.
- 초심자에게 `좋은 성능 후보`와 `위험한 과적합 후보`를 동시에 읽는 태도를 주는 절입니다.

## 핵심 주장

1. 그래디언트 부스팅은 표 형식 데이터에서 강한 성능 후보가 될 수 있다.
2. 그러나 sequential correction 구조 때문에 과적합에 민감할 수 있다.
3. `learning_rate`는 shrinkage로서 각 weak learner의 기여를 축소한다.
4. 작은 `learning_rate`는 보통 더 많은 `n_estimators`를 필요로 한다.
5. `subsample`은 stochastic gradient boosting의 핵심 요소로 과적합과 분산 완화에 기여한다.
6. `staged_predict`, `train_score_`, early stopping은 적절한 단계 수를 찾는 데 중요하다.
7. HistGradientBoosting 계열은 실무에서 자주 언급되는 현대적 구현이다.

## 근거 출처

### 1) scikit-learn User Guide - ensemble

- 문서: `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`
- URL: https://scikit-learn.org/stable/modules/ensemble.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-ensemble.html`
- 반영 포인트:
  - learning rate가 shrinkage라는 설명
  - 작은 learning rate가 더 많은 weak learner를 필요로 한다는 설명
  - `train_score_`, `staged_predict`, early stopping 관련 설명
  - stochastic gradient boosting의 subsample 설명
  - HGBT와 ordinary gradient boosting 비교

### 2) Friedman 2001

- 논문: Jerome H. Friedman, `Greedy Function Approximation: A Gradient Boosting Machine`
- 반영 포인트:
  - gradient boosting의 기본 구조
  - shrinkage의 역사적 배경

### 3) Friedman 2002

- 논문: Jerome H. Friedman, `Stochastic Gradient Boosting`
- 반영 포인트:
  - subsampling과 일반화 성능 조절의 배경

## 집필 판단

- 16.2는 공식보다 운영 감각을 우선했습니다.
- 초심자에게는 “강한 모델”보다 “왜 잘못 쓰기 쉬운가”를 같이 설명하는 편이 더 중요하다고 판단했습니다.
- 저장소 의존성에 `scikit-learn`이 아직 없으므로, 과한 보정을 설명하는 장난감 숫자 예제를 사용했습니다.
- XGBoost, LightGBM, CatBoost는 이름만 연결하고 세부 비교는 하지 않았습니다.

## 제외한 내용

- 구현체별 최적화 구조
- GPU 학습 세부
- histogram binning 수학
- 자동 하이퍼파라미터 탐색
- calibration, ranking losses, custom objectives

이 내용은 후속 심화 절이나 프로젝트 파트에서 별도로 확장할 수 있습니다.

# P3-15.1 랜덤포레스트 근거 메모

## Section 역할

- Part 3 Module 5 Chapter 15의 도입 절입니다.
- 결정트리의 과적합 문제 다음에, 여러 randomized tree를 모아 안정성을 얻는 관점을 설명합니다.
- 특징 중요도(feature importance)와 OOB의 상세 해석은 다음 절로 넘깁니다.

## 핵심 주장

1. 랜덤포레스트는 여러 decision tree를 결합하는 averaging ensemble이다.
2. 각 트리는 bootstrap sample과 random feature subset을 통해 서로 다르게 학습된다.
3. 랜덤포레스트의 핵심 목적은 단일 결정트리의 높은 variance를 줄이는 것이다.
4. 트리들의 예측을 집계하면 일부 오류가 상쇄될 수 있다.
5. `n_estimators`, `max_features`, `bootstrap`, `oob_score`는 초심자가 먼저 읽어야 할 대표 설정값이다.

## 근거 출처

### 1) scikit-learn User Guide

- 문서: `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`
- URL: https://scikit-learn.org/stable/modules/ensemble.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-ensemble.html`
- 반영 포인트:
  - ensemble methods의 일반 정의
  - random forests가 randomized decision tree 기반 averaging algorithm이라는 설명
  - bootstrap sample과 feature subset 설명
  - variance reduction, bias-variance tradeoff 설명
  - bagging이 variance를 줄여 overfitting을 완화하는 계열이라는 설명
  - OOB(out-of-bag) 설명

### 2) scikit-learn API Reference

- 문서: `RandomForestClassifier`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-randomforestclassifier.html`
- 반영 포인트:
  - `n_estimators`, `max_features`, `bootstrap`, `oob_score`, `max_depth`, `min_samples_leaf` 정의
  - random forest classifier의 메타 추정기(meta estimator) 설명
  - `bootstrap=True`일 때 `max_samples` 동작
  - `predict`, `predict_proba` 집계 방식 설명

### 3) 원 논문

- 자료: Leo Breiman, `Random Forests`, Machine Learning, 45(1), 5-32, 2001
- 반영 포인트:
  - random forest 계열의 역사적 기준점
  - tree ensemble 관점의 고전 출처

## 집필 판단

- 초심자 기준이므로 배깅(bagging) 일반론 전체보다 `왜 여러 트리를 모으는가`에 먼저 집중했습니다.
- `variance reduction`을 핵심 메시지로 두고, 수식 대신 반복 실험 결과 흔들림으로 보여 주었습니다.
- 단일 트리 대 랜덤포레스트 비교에서 성능 수치 자체보다 `덜 흔들리는가`를 더 중요한 읽기 포인트로 제시했습니다.
- `majority vote`는 익숙한 표현이지만, scikit-learn 구현 기준으로는 확률 평균 집계가 더 정확하므로 그 점을 본문에 분리해 설명했습니다.

## 제외한 내용

- Extra Trees와의 상세 비교
- OOB 점수의 통계적 한계
- 특징 중요도 해석과 편향 문제
- 랜덤포레스트 회귀의 별도 실습

이 내용은 P3-15.2 또는 후속 장에서 다시 다룰 수 있습니다.

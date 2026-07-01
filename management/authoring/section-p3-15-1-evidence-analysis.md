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

### 2) scikit-learn API Reference

- 문서: `RandomForestClassifier`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-randomforestclassifier.html`

### 3) 원 논문

- 자료: Leo Breiman, `Random Forests`, Machine Learning, 45(1), 5-32, 2001

## 제외한 내용

- Extra Trees와의 상세 비교
- OOB 점수의 통계적 한계
- 특징 중요도 해석과 편향 문제
- 랜덤포레스트 회귀의 별도 실습

이 내용은 P3-15.2 또는 후속 장에서 다시 다룰 수 있습니다.

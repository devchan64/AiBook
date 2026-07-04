# P3-15.2 특징 중요도 근거 메모

## Section 역할

- Part 3 Module 5 Chapter 15의 두 번째 절입니다.
- 랜덤포레스트를 배운 직후, `feature_importances_`를 어떻게 읽고 어디서 오해가 생기는지 설명합니다.
- 초심자에게 중요도 숫자의 유용성과 한계를 동시에 주는 절입니다.

## 핵심 주장

1. 랜덤포레스트의 `feature_importances_`는 impurity-based importance(MDI)다.
2. MDI는 여러 randomized tree의 feature 사용 기여를 평균낸 내부 요약이다.
3. permutation importance는 feature를 섞었을 때 성능 저하를 보는 다른 방식이다.
4. impurity-based importance는 hold-out generalization importance를 직접 반영하지 않을 수 있다.
5. impurity-based importance는 high-cardinality feature를 선호할 수 있다.
6. correlated features가 있으면 중요도 해석이 왜곡되거나 분산될 수 있다.

## 근거 출처

### 1) scikit-learn User Guide - ensemble

- 문서: `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`
- URL: https://scikit-learn.org/stable/modules/ensemble.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-ensemble.html`

### 2) scikit-learn API Reference - RandomForestClassifier

- 문서: `RandomForestClassifier`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-randomforestclassifier.html`

### 3) Louppe 2014

- 자료: Gilles Louppe, *Understanding Random Forests: From Theory to Practice*, 2014

## 제외한 내용

- SHAP value
- partial dependence plot
- causal feature attribution
- 대규모 실제 데이터셋에서의 안정적 feature selection 절차

이 내용은 후속 심화 절이나 보충학습에서 다시 다룰 수 있습니다.

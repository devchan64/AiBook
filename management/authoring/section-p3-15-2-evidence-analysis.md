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
- 반영 포인트:
  - tree ensemble에서 importance를 평균하는 MDI 설명
  - 상위 분기가 더 많은 샘플에 기여한다는 설명
  - `feature_importances_` 정의
  - impurity-based importance의 두 가지 한계:
    - hold-out 성능 중요도를 직접 반영하지 않음
    - high-cardinality feature 편향
  - permutation importance를 대안으로 제시

### 2) scikit-learn API Reference - RandomForestClassifier

- 문서: `RandomForestClassifier`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-randomforestclassifier.html`
- 반영 포인트:
  - `feature_importances_`가 impurity-based feature importances라는 설명
  - inspection 모듈 및 permutation importance 관련 예제 링크

### 3) Louppe 2014

- 자료: Gilles Louppe, *Understanding Random Forests: From Theory to Practice*, 2014
- 반영 포인트:
  - Random Forest importance 해석의 이론적 배경 참고

## 집필 판단

- 15.1이 `왜 숲을 쓰는가`를 설명했다면, 15.2는 `숲이 말해 주는 중요도 숫자를 어떻게 조심해서 읽을 것인가`에 집중했습니다.
- 초심자 문맥에서는 SHAP, PDP보다 먼저 `MDI vs permutation`의 차이를 잡는 것이 더 중요하다고 판단했습니다.
- 중요도 숫자를 곧바로 원인 순위로 오해하는 것을 막기 위해 `좋은 사용법 / 위험한 사용법` 표를 넣었습니다.
- correlated feature와 high-cardinality feature는 실제 실무 오해를 자주 만드는 지점이므로 별도 소절로 분리했습니다.

## 제외한 내용

- SHAP value
- partial dependence plot
- causal feature attribution
- 대규모 실제 데이터셋에서의 안정적 feature selection 절차

이 내용은 후속 심화 절이나 보충학습에서 다시 다룰 수 있습니다.

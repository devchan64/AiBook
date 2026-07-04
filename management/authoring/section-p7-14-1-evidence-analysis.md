# P3-14.1 결정트리(decision tree) 근거 메모

## Section 역할

- Part 3 Module 5 Chapter 14의 도입 절입니다.
- 범위는 `결정트리의 직관`, `node / split / leaf`, `분류와 회귀에서의 공통 구조`, `좋은 첫 질문을 고르는 감각`까지입니다.
- 과적합(overfitting), pruning, ensemble은 이 절에서 깊게 다루지 않습니다.

## 핵심 주장

1. 결정트리는 분류와 회귀에 모두 쓰이는 지도학습 방법이다.
2. 결정트리는 feature에서 추론한 단순한 의사결정 규칙으로 target을 예측한다.
3. 결정트리는 질문을 반복해 데이터를 더 정리된 묶음으로 나누는 구조로 설명할 수 있다.
4. 분류 트리에서는 split 후보를 비교할 때 impurity 감소 관점으로 설명할 수 있다.
5. 결정트리는 비교적 읽기 쉬운 모델이지만, 깊어질수록 과적합 위험이 생긴다. 다만 과적합 상세는 다음 절로 넘긴다.

## 근거 출처

### 1) scikit-learn User Guide

- 문서: `1.10. Decision Trees`
- URL: https://scikit-learn.org/stable/modules/tree.html
- 확인 날짜: 2026-06-27

### 2) scikit-learn API Reference

- 문서: `DecisionTreeClassifier`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
- 확인 날짜: 2026-06-27

### 3) CART 고전 문헌

- 자료: Leo Breiman, Jerome Friedman, Richard Olshen, Charles Stone, *Classification and Regression Trees*, Routledge, 1984

## 제외한 내용

- entropy와 information gain 수식
- cost-complexity pruning 세부 절차
- `DecisionTreeRegressor` 세부 구현
- 범주형 분기 구현 차이와 라이브러리별 세부 동작

이 내용은 P3-14.2 이후나 Part 4 이후 심화 문맥에서 다시 검토할 수 있습니다.

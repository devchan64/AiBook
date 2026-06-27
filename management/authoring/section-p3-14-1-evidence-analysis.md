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
- 반영 포인트:
  - decision tree를 비모수적(non-parametric) 지도학습으로 소개
  - classification / regression 모두에 사용된다는 설명
  - feature로부터 단순한 decision rule을 학습해 target을 예측한다는 설명
  - tree를 piecewise constant approximation으로 볼 수 있다는 설명
  - white box model, boolean logic 설명
  - 장점과 한계의 큰 방향

### 2) scikit-learn API Reference

- 문서: `DecisionTreeClassifier`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
- 확인 날짜: 2026-06-27
- 반영 포인트:
  - 초심자에게 이후 다시 보이게 될 대표 하이퍼파라미터 이름 연결
  - `criterion`, `max_depth`, `splitter` 같은 설정명이 실제 API에 존재함을 확인
  - `predict_proba`가 leaf 내부 class 비율을 확률로 읽는다는 설명 확인
  - 기본 크기 제어값을 두지 않으면 fully grown and unpruned tree가 될 수 있다는 경고 확인

### 3) CART 고전 문헌

- 자료: Leo Breiman, Jerome Friedman, Richard Olshen, Charles Stone, *Classification and Regression Trees*, Routledge, 1984
- 반영 포인트:
  - decision tree 계열 설명의 역사적 기준점
  - 분류와 회귀 트리를 하나의 계열로 묶는 고전적 배경

## 집필 판단

- 초심자 기준이므로 수식 중심보다 `질문을 나누는 구조`를 먼저 보여 주는 편이 적절하다고 판단했습니다.
- impurity는 `섞임 정도`라는 직관 수준으로만 설명했습니다.
- 다만 `criterion`이라는 공식 용어는 이번 절에서 한 번 노출하고, 수식 전개는 뒤로 넘겼습니다.
- gini를 Python 예제로 직접 계산하게 하여, 트리가 `좋은 split을 비교해 고른다`는 점을 눈으로 확인하게 구성했습니다.
- `읽기 쉬움`을 장점으로 쓰되, 공식 문서의 `white box model` 설명과 연결했습니다.
- `항상 좋은 모델`이라는 오해를 만들지 않도록 fully grown tree 경고를 반영하고 다음 절의 과적합과 연결했습니다.

## 제외한 내용

- entropy와 information gain 수식
- cost-complexity pruning 세부 절차
- `DecisionTreeRegressor` 세부 구현
- 범주형 분기 구현 차이와 라이브러리별 세부 동작

이 내용은 P3-14.2 이후나 Part 4 이후 심화 문맥에서 다시 검토할 수 있습니다.

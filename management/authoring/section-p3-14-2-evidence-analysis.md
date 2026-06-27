# P3-14.2 트리의 과적합 근거 메모

## Section 역할

- Part 3 Module 5 Chapter 14의 두 번째 절입니다.
- 14.1의 `질문을 나누는 구조` 다음에, 그 구조가 왜 쉽게 과적합으로 이어질 수 있는지 설명합니다.
- 뒤의 랜덤포레스트, 그래디언트 부스팅으로 가기 전 `트리 복잡도 제어` 감각을 만드는 절입니다.

## 핵심 주장

1. 결정트리는 과하게 복잡한 트리를 만들 수 있으며, 이는 일반화 성능을 해칠 수 있다.
2. `max_depth`, `min_samples_leaf`, `min_samples_split` 같은 제어값은 과적합 방지와 연결된다.
3. `ccp_alpha`는 Minimal Cost-Complexity Pruning과 연결되는 pruning 제어값이다.
4. train 성능과 test 성능을 함께 봐야 트리의 과적합을 읽을 수 있다.
5. leaf가 너무 작아지면 패턴보다 예외를 설명할 위험이 커진다.

## 근거 출처

### 1) scikit-learn User Guide

- 문서: `1.10. Decision Trees`
- URL: https://scikit-learn.org/stable/modules/tree.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-14-1-evidence/scikit-tree.html`
- 반영 포인트:
  - over-complex trees와 overfitting 설명
  - pruning, `min_samples_leaf`, `max_depth` 필요성 설명
  - `max_depth`로 크기를 제어하라는 실무 팁
  - `min_samples_split`, `min_samples_leaf`로 여러 샘플이 분기에 기여하게 하라는 설명
  - Minimal Cost-Complexity Pruning 설명

### 2) scikit-learn API Reference

- 문서: `DecisionTreeClassifier`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-14-1-evidence/scikit-decisiontreeclassifier.html`
- 반영 포인트:
  - `max_depth` 정의
  - `min_samples_leaf` 정의와 smoothing 설명
  - `ccp_alpha`가 pruning 복잡도 파라미터라는 설명
  - 기본 크기 제어값이 fully grown, unpruned tree로 이어질 수 있다는 경고

### 3) CART 고전 문헌

- 자료: Leo Breiman, Jerome Friedman, Richard Olshen, Charles Stone, *Classification and Regression Trees*, Routledge, 1984
- 반영 포인트:
  - cost-complexity pruning의 역사적 배경
  - 분류/회귀 트리 복잡도 제어 논의의 고전적 출처

## 집필 판단

- 14.1에서 구조 설명을 끝냈으므로, 14.2에서는 성능 수치와 제어 손잡이를 바로 연결하도록 구성했습니다.
- 초심자 기준을 지키기 위해 pruning 공식을 전개하지 않고 `자란 뒤 줄이는 방법` 수준으로 설명했습니다.
- Python 예제는 `max_depth`와 `min_samples_leaf`를 각각 따로 보여 주어 손잡이 역할을 분리했습니다.
- `ccp_alpha`는 개념 소개까지만 하고, 자세한 탐색 실습은 뒤 튜닝 문맥이나 보충학습으로 넘겼습니다.

## 제외한 내용

- `min_impurity_decrease`의 세부 해석
- pruning path 계산 과정
- 교차검증으로 `ccp_alpha`를 고르는 전체 절차
- 랜덤포레스트의 평균화 효과와 부스팅의 잔차 보정 효과

이 내용은 P3-15, P3-16, 또는 별도 보충학습에서 다시 다룰 수 있습니다.

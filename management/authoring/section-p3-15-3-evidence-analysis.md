# P3-15.3 OOB와 랜덤포레스트 점검 근거 메모

## Section 역할

- Part 3 Module 5 Chapter 15의 세 번째 절입니다.
- 랜덤포레스트의 구조(15.1)와 특징 중요도 해석(15.2) 다음에, 모델 점검의 입문적 손잡이로 OOB(out-of-bag)를 설명합니다.
- 초심자가 `train score만 보고 멈추는 실수`를 줄이게 하는 절입니다.

## 핵심 주장

1. 랜덤포레스트의 OOB는 bootstrap에서 빠진 샘플을 이용한 내부 일반화 추정이다.
2. `oob_score=True`는 out-of-bag 샘플을 사용해 generalization score를 추정하겠다는 뜻이다.
3. OOB는 `bootstrap=True`일 때만 가능하다.
4. `oob_score_`는 train accuracy와 다른 내부 점검 점수다.
5. OOB는 편리한 빠른 점검 수단이지만, 별도 test/validation을 완전히 대체한다고 단정하면 안 된다.

## 근거 출처

### 1) scikit-learn User Guide - ensemble

- 문서: `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`
- URL: https://scikit-learn.org/stable/modules/ensemble.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-ensemble.html`
- 반영 포인트:
  - random forest가 bootstrap sample로 각 tree를 학습한다는 설명
  - bootstrap 사용 시 left out or out-of-bag samples로 generalization error를 추정할 수 있다는 설명
  - `oob_score=True`로 이 기능을 켤 수 있다는 설명

### 2) scikit-learn API Reference - RandomForestClassifier

- 문서: `RandomForestClassifier`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-randomforestclassifier.html`
- 반영 포인트:
  - `oob_score`는 out-of-bag samples를 사용해 generalization score를 추정하는 옵션
  - `bootstrap=True`일 때만 사용 가능
  - `oob_score_`는 out-of-bag estimate로 얻은 score
  - `oob_decision_function_` 관련 설명
  - OOB Errors for Random Forests 예제 링크

## 집필 판단

- 15.1은 구조, 15.2는 해석, 15.3은 점검으로 역할을 분리했습니다.
- OOB는 랜덤포레스트 안에서 자연스럽게 이어지는 주제이므로 Chapter 15 안에서 마무리하는 편이 흐름상 자연스럽다고 판단했습니다.
- 초심자 기준에서는 교차검증 전체 체계를 먼저 늘어놓기보다, `train / OOB / test를 함께 보는 태도`를 먼저 만드는 것이 더 중요하다고 판단했습니다.
- OOB를 `빠른 내부 점검판`으로 설명하고, 최종 검증과 동일시하지 않도록 보수적으로 서술했습니다.

## 제외한 내용

- 교차검증의 다양한 변형
- calibration, threshold moving
- OOB 기반 조기 종료(early stopping) 논의
- 그래디언트 부스팅에서의 OOB 추정 세부 차이

이 내용은 Chapter 16 이후 모델 비교와 평가 흐름에서 다시 확장할 수 있습니다.

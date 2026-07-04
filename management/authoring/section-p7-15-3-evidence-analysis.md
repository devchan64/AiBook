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

### 2) scikit-learn API Reference - RandomForestClassifier

- 문서: `RandomForestClassifier`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- 확인 날짜: 2026-06-27
- `.tmp` 저장본:
  - `.tmp/section-p3-15-1-evidence/scikit-randomforestclassifier.html`

## 제외한 내용

- 교차검증의 다양한 변형
- calibration, threshold moving
- OOB 기반 조기 종료(early stopping) 논의
- 그래디언트 부스팅에서의 OOB 추정 세부 차이

이 내용은 Chapter 16 이후 모델 비교와 평가 흐름에서 다시 확장할 수 있습니다.

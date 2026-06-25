# P3-4.1 근거 검토: 학습 데이터와 평가 데이터

## 검토 대상

- Section: `docs/parts/part-03/chapter-04/section-01.md`
- 작성일: 2026-06-25
- 목적: 학습 데이터와 평가 데이터를 나누는 이유를 초심자 기준으로 설명한다.

## 사용한 근거

### scikit-learn, Cross-validation: evaluating estimator performance

- URL: https://scikit-learn.org/stable/modules/cross_validation.html
- 로컬 확인 파일: `.tmp/section-p3-4-1-evidence/scikit-learn-cross-validation.html`
- 확인 날짜: 2026-06-25
- 핵심 확인:
  - 학습한 데이터와 같은 데이터로 테스트하는 것은 방법론적 오류가 될 수 있다고 설명한다.
  - 이미 본 샘플의 라벨을 반복하는 모델은 완벽한 점수를 얻을 수 있지만, 보지 못한 데이터에는 유용하게 예측하지 못할 수 있다고 설명한다.
  - 이를 피하기 위해 사용 가능한 데이터의 일부를 테스트 세트로 따로 두는 관행을 설명한다.
- 본문 반영:
  - “배운 문제지로만 시험을 보면 실력을 착각할 수 있다”는 초심자용 비유로 일반화했다.
  - 같은 데이터로 학습과 평가를 모두 하면 성능을 과대평가할 수 있다는 설명의 근거로 사용했다.

### scikit-learn, train_test_split

- URL: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
- 로컬 확인 파일: `.tmp/section-p3-4-1-evidence/scikit-learn-train-test-split.html`
- 확인 날짜: 2026-06-25
- 핵심 확인:
  - scikit-learn은 배열이나 행렬을 무작위 학습/테스트 부분집합으로 나누는 유틸리티를 제공한다.
- 본문 반영:
  - 데이터 분리가 실제 도구에서 기본 작업으로 다뤄진다는 배경 근거로만 사용했다.
  - 이 절에서는 코드 사용법을 설명하지 않았다.

### An Introduction to Statistical Learning

- URL: https://www.statlearning.com/
- 로컬 확인 파일: `.tmp/section-p3-4-1-evidence/statlearning-home.html`
- 확인 날짜: 2026-06-25
- 핵심 확인:
  - 통계학습 입문서로, 모델 평가와 재표본추출(resampling), 분류/회귀 모델 학습의 기본 주제를 다룬다.
- 본문 반영:
  - 데이터 분리와 모델 평가를 통계학습의 기본 흐름으로 설명하기 위한 참고 자료로 사용했다.
  - 본문에서 특정 문장을 직접 인용하지 않았다.

## 일반화한 문장

- “학습 데이터는 모델이 배우는 데 쓰는 데이터이고, 평가 데이터는 모델이 배운 결과를 확인하기 위해 남겨 두는 데이터다.”
- “같은 데이터로 학습하고 평가하면 모델이 일반적인 패턴을 배운 것인지, 학습 데이터의 흔적을 외운 것인지 구분하기 어렵다.”
- “평가 데이터는 미래 데이터를 완벽히 대체하지 않지만, 새 데이터에서의 동작을 추정하기 위한 최소 장치다.”

## 검토한 경계

- P3-4.1은 데이터 분리의 필요성에 집중한다.
- 검증 데이터와 테스트 데이터의 엄밀한 역할 구분은 P3-4.2로 넘겼다.
- 과적합과 과소적합의 자세한 설명은 P3-5로 넘겼다.
- 평가 지표의 계산과 선택은 P3-6으로 넘겼다.
- 교차검증의 세부 절차는 이 절에서 다루지 않고 후속 절로 넘겼다.

## 검증 필요

- P3-4.2 작성 시 `평가 데이터(evaluation data)`라는 넓은 표현을 `검증 데이터(validation data)`와 `테스트 데이터(test data)`로 세분화해야 한다.
- 후속 절에서 교차검증을 다룰 때, 이 절의 작은 데이터 관련 설명과 중복되지 않도록 조정해야 한다.

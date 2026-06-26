# P3-4.2 근거 검토: 검증(validation)과 테스트(test)

## 검토 대상

- Section: `docs/parts/part-03/chapter-04/section-02.md`
- 작성일: 2026-06-26
- 목적: 검증 데이터와 테스트 데이터의 역할 차이를 초심자 기준으로 설명한다.

## 사용한 근거

### scikit-learn, Cross-validation: evaluating estimator performance

- URL: https://scikit-learn.org/stable/modules/cross_validation.html
- 확인 날짜: 2026-06-26
- 기존 로컬 확인 파일: `.tmp/section-p3-4-1-evidence/scikit-learn-cross-validation.html`
- 핵심 확인:
  - 학습 데이터와 별개로 테스트 세트를 두는 이유를 설명한다.
  - 하이퍼파라미터 탐색과 모델 선택 과정에서 검증 구조가 필요함을 설명한다.
  - 교차검증은 모델 성능을 더 안정적으로 추정하려는 방법으로 제시된다.
- 본문 반영:
  - 검증은 선택 과정에, 테스트는 마지막 확인에 가깝다는 일반화 문장에 사용했다.
  - 테스트를 반복적으로 들여다보면 마지막 확인용 역할이 약해진다는 설명의 배경 근거로 사용했다.

### scikit-learn, train_test_split

- URL: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
- 확인 날짜: 2026-06-26
- 기존 로컬 확인 파일: `.tmp/section-p3-4-1-evidence/scikit-learn-train-test-split.html`
- 핵심 확인:
  - 데이터를 학습/테스트 부분집합으로 나누는 기본 유틸리티를 제공한다.
- 본문 반영:
  - 두 단계 `train -> temp -> validation/test` 분리 예제를 설명하는 실용적 배경 근거로 사용했다.

### An Introduction to Statistical Learning

- URL: https://www.statlearning.com/
- 확인 날짜: 2026-06-26
- 기존 로컬 확인 파일: `.tmp/section-p3-4-1-evidence/statlearning-home.html`
- 핵심 확인:
  - 통계학습 입문서로 재표본추출, 모델 평가, 검증 절차를 다룬다.
- 본문 반영:
  - 검증과 테스트 구분이 통계학습의 기본 평가 흐름이라는 배경 참고 자료로 사용했다.

## 일반화한 문장

- “검증 데이터는 여러 선택지를 비교하는 데 쓰고, 테스트 데이터는 최종 선택 뒤 마지막 확인에 쓴다.”
- “테스트 데이터를 중간에 반복해서 보면 테스트도 사실상 검증 데이터처럼 사용하게 된다.”
- “교차검증은 테스트를 자꾸 보는 대신, 주어진 데이터 안에서 검증을 더 안정적으로 하려는 방법이다.”
- “검증 점수는 후보 비교를 위한 숫자이고, 테스트 점수는 최종 선택 뒤 해석하는 숫자다.”
- “같은 점수 숫자라도 모델 선택 단계에서 본 것인지, 최종 확인 단계에서 본 것인지에 따라 의미가 달라진다.”

## 검토한 경계

- P3-4.2는 검증과 테스트의 역할 차이에 집중한다.
- 평가 지표의 수식과 해석은 P3-6으로 넘겼다.
- 모델 선택의 구체적 절차는 P3-8로 넘겼다.
- 과적합과 일반화의 자세한 설명은 P3-5로 넘겼다.
- 데이터 누수(data leakage)라는 용어는 직접 크게 확장하지 않고, “미래 정보가 섞임”, “테스트를 자주 봄” 같은 초심자 표현으로 제한했다.

## 검증 필요

- P3-5와 P3-8 작성 시, 검증 점수와 테스트 점수 차이를 실제 사례로 다시 연결할 필요가 있다.
- 추후 데이터 누수(data leakage)를 별도 절이나 예시로 확장할지 검토할 수 있다.
- 작은 데이터에서 교차검증과 홀드아웃 테스트의 설명 균형을 이후 절에서 다시 점검할 수 있다.

# P3-9.2 튜닝(tuning)과 검증 비용 근거 검토

## 핵심 주장

### 1. 튜닝은 하이퍼파라미터 후보를 교차검증 점수로 비교하는 절차다

- 근거:
  - scikit-learn, `3.2. Tuning the hyper-parameters of an estimator`
- 반영 방식:
  - `설정값을 validation 절차로 비교하는 일`로 초심자용 일반화
  - GridSearchCV 예제로 연결

### 2. test 데이터를 모델 선택에 섞으면 성능 추정이 낙관적으로 보일 수 있다

- 근거:
  - scikit-learn, `12. Common pitfalls and recommended practices`
- 반영 방식:
  - `test는 마지막 확인용`이라는 규칙으로 정리
  - leakage와 과대평가 위험을 9.2의 핵심으로 반영

### 3. grid search와 random search는 탐색 방식이 다르며, random search가 더 효율적일 수 있다

- 근거:
  - scikit-learn, `3.2. Tuning the hyper-parameters of an estimator`
  - James Bergstra, Yoshua Bengio, `Random Search for Hyper-Parameter Optimization`, JMLR, 2012
- 반영 방식:
  - 초심자용 비교 표로 일반화
  - `모든 조합`과 `일부를 전략적으로 샘플링`의 차이로 설명

### 4. 계산 비용과 검증 비용은 구분해서 봐야 한다

- 근거:
  - scikit-learn, `3.2. Tuning the hyper-parameters of an estimator`
  - scikit-learn, `12. Common pitfalls and recommended practices`
- 반영 방식:
  - 계산 비용은 시간/자원 문제
  - 검증 비용은 validation 과적합과 과대평가 문제로 구분

### 5. 실증 사례는 조합 수 증가, validation 반복 관찰, 작은 점수 개선의 해석 문제를 함께 보여 줘야 한다

- 근거:
  - scikit-learn, `3.2. Tuning the hyper-parameters of an estimator`
  - scikit-learn, `12. Common pitfalls and recommended practices`
  - James Bergstra, Yoshua Bengio, `Random Search for Hyper-Parameter Optimization`, JMLR, 2012
- 반영 방식:
  - 계산 비용은 조합 수와 교차검증 횟수의 곱으로 직관화
  - 검증 비용은 validation을 반복해서 들여다보는 과정의 신뢰도 저하로 설명
  - 작은 개선이 실제 가치가 있는지 다시 묻는 실무 해석 문단 추가

## 본문 반영 판단

- 9.2는 API 설명보다 `실험 절차와 비용` 중심으로 유지한다.
- nested CV, Bayesian optimization, 분산 탐색은 범위 밖으로 둔다.
- Python 예제는 `candidate combinations`, `best cv score`, `test score`를 함께 출력해 현재 절의 질문과 직접 연결한다.

## 도메인 경계 메모

- P3-9.1:
  - 하이퍼파라미터의 정의
  - 역사와 실증 사례
  - 작은 설정 변화 예시
- P3-9.2:
  - 튜닝 절차
  - grid/random search
  - 계산 비용
  - 검증 비용
  - test 분리 원칙

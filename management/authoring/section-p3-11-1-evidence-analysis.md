# P3-11.1 로지스틱 회귀(logistic regression)의 직관 근거 검토

## 핵심 주장

### 1. 로지스틱 회귀는 분류를 위한 선형 모델이다

- 근거:
  - scikit-learn, `1.1.11. Logistic regression`
  - scikit-learn, `LogisticRegression`
- 반영 방식:
  - `classification을 위한 linear model`이라는 공식을 초심자용 설명으로 일반화
  - 선형회귀와의 연속성으로 연결

### 2. 로지스틱 회귀는 선형 결합 결과를 sigmoid를 통해 0~1 범위 값으로 바꿔 읽는다

- 근거:
  - scikit-learn, `1.1.11. Logistic regression`
- 반영 방식:
  - 수식 유도는 생략
  - `선형 점수 -> sigmoid -> probability-like output` 흐름으로 단순화

### 3. `predict_proba`와 `predict`는 서로 다른 단계다

- 근거:
  - scikit-learn, `LogisticRegression`
- 반영 방식:
  - `점수 단계`와 `결정 단계`의 차이로 설명
  - threshold의 존재를 정책 관점으로 연결

### 4. threshold는 모델의 출력 위에 놓이는 서비스 판단 규칙이다

- 근거:
  - scikit-learn, `1.1.11. Logistic regression`
  - Part 3 앞 절의 metric, baseline, tuning 흐름
- 반영 방식:
  - 고객 이탈, 스팸 필터, 의료 위험 예시로 실증 설명

### 5. 계수 해석과 확률 해석에는 과잉 일반화 위험이 있다

- 근거:
  - scikit-learn, `1.1.11. Logistic regression`
  - 로지스틱 회귀 해석의 일반적 통계 입문 경고
- 반영 방식:
  - 계수를 곧 원인으로 읽지 말 것
  - 확률처럼 보이는 값을 자동으로 절대적 확률로 읽지 말 것을 주의 문구로 반영

### 6. 역사 설명은 `선형회귀 다음에 왜 로지스틱 회귀가 오는가`를 보여 주는 수준에서 정리한다

- 근거:
  - scikit-learn, `1.1.11. Logistic regression`
  - 통계 입문에서의 binary outcome modeling 일반 설명
- 반영 방식:
  - 연속값을 설명하던 선형회귀의 흐름
  - 이항 결과(binary outcome)를 다루려는 필요
  - 선형식을 버리지 않고 0~1 해석으로 확장한 흐름
  - 이 네 단계를 초심자용 역사 서술로 일반화

### 7. 주요 논의점은 `확률`, `계수`, `threshold`, `선형 한계`를 중심으로 정리한다

- 근거:
  - scikit-learn, `1.1.11. Logistic regression`
  - 로지스틱 회귀의 입문적 해석에서 반복되는 일반 경고
- 반영 방식:
  - 점수와 결정의 분리
  - probability-like output과 calibration의 긴장
  - coefficient 해석과 causation의 분리
  - linear model의 장점과 한계
  - threshold를 정책 선택으로 설명

## 본문 반영 판단

- 11.1은 binary classification의 직관에 집중한다.
- log-odds, likelihood, solver 차이는 범위 밖으로 둔다.
- Python 예제는 작은 1변수 이진 분류로 두어 coefficient, intercept, predict_proba, predict를 함께 출력하게 구성한다.
- threshold 설명은 표와 별도 Python 예제로 한 번 더 반복해, 점수와 결정의 분리를 눈으로 확인하게 한다.
- 역사 서술은 세부 연표보다 `왜 이런 모델이 필요해졌는가`를 설명하는 방향으로 유지한다.
- 주요 논의점은 수학 논쟁보다 초심자가 실제로 오해하기 쉬운 해석 문제를 우선한다.

## 도메인 경계 메모

- P3-11.1:
  - 로지스틱 회귀의 직관
  - 선형 결합과 sigmoid
  - predict_proba와 threshold
  - 분류 해석의 입문
- P3-11.2:
  - 결정 경계(decision boundary)
  - 입력 공간에서의 분리선 해석

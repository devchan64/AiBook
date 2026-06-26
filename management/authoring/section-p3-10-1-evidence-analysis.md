# P3-10.1 선형회귀(linear regression)의 직관 근거 검토

## 핵심 주장

### 1. 회귀(regression)는 연속값을 예측하는 문제다

- 근거:
  - scikit-learn, `1.1. Linear Models`
- 반영 방식:
  - 분류와 대비해 `연속값 예측`이라는 초심자용 정의로 일반화
  - 집값, 배송 시간, 점수 예시로 연결

### 2. 선형회귀는 입력과 출력의 관계를 직선 또는 선형 결합으로 표현하는 가장 기본적인 모델이다

- 근거:
  - scikit-learn, `1.1. Linear Models`
  - scikit-learn, `LinearRegression`
- 반영 방식:
  - `y = wx + b` 구조로 단순화
  - 다변수일 때는 입력의 선형 결합(linear combination)으로 넓혀 설명
  - 기울기와 절편의 의미를 계산보다 해석 중심으로 설명

### 3. 선형회귀는 예측 오차를 줄이는 방향으로 계수와 절편을 정한다

- 근거:
  - scikit-learn, `LinearRegression`
  - scikit-learn, `1.1. Linear Models`
- 반영 방식:
  - ordinary least squares의 엄밀한 유도는 생략
  - `오차를 줄이는 선을 찾는다`는 입문 설명으로 일반화

### 4. coefficient와 intercept는 방향성과 시작점을 읽는 핵심 값이다

- 근거:
  - scikit-learn, `LinearRegression`
- 반영 방식:
  - coefficient는 입력 증가당 출력 변화량
  - intercept는 수학적 출발점으로 정리
  - 절편의 현실적 해석 가능성은 도메인마다 다르다는 주의 문구 반영

### 5. 선형회귀는 baseline처럼 쓰기 좋은 첫 알고리즘이다

- 근거:
  - scikit-learn, `1.1. Linear Models`
  - Part 3 앞 절의 baseline, model selection 흐름
- 반영 방식:
  - `문제가 얼마나 선형적으로 읽히는가`를 먼저 보는 출발점으로 설명
  - 뒤 알고리즘과의 비교 기준 역할로 연결

### 6. 선형회귀는 관계를 선형적으로 단순화하고, 설명되지 않은 차이를 오차로 남긴다

- 근거:
  - scikit-learn, `1.1. Linear Models`
- 반영 방식:
  - 엄밀한 통계 가정 전체를 전개하지 않고
  - `선형 관계`, `더해지는 영향`, `남는 오차`라는 세 가지 입문 관점으로 정리

## 본문 반영 판단

- 10.1은 직관과 역할에 집중하고, 평가 지표와 잔차 해석은 10.2로 넘긴다.
- 수식은 `y = wx + b` 한 줄만 사용하고, 엄밀한 최소제곱 유도는 범위 밖으로 둔다.
- 다변수 선형회귀의 전체 행렬 표기는 범위를 넘기므로, `선형 결합` 수준에서만 소개한다.
- Python 예제는 작은 1변수 데이터와 다변수 데이터 두 가지로 두어 coefficient, intercept, prediction을 직접 출력하게 구성한다.

## 도메인 경계 메모

- P3-10.1:
  - 회귀 문제의 성격
  - 선형회귀의 직관
  - 선형 결합의 의미
  - 오차를 줄이는 모델이라는 관점
  - coefficient, intercept의 해석
  - baseline 관점
- P3-10.2:
  - 잔차(residual)
  - 오차(error)
  - 평가 지표
  - 선형 가정의 한계

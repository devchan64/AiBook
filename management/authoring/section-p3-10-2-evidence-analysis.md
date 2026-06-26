# P3-10.2 선형회귀의 평가와 한계 근거 검토

## 핵심 주장

### 1. 잔차(residual)는 실제값과 예측값의 차이로 읽을 수 있다

- 근거:
  - scikit-learn, `1.1. Linear Models`
  - scikit-learn, `3.4. Metrics and scoring: quantifying the quality of predictions`
- 반영 방식:
  - 잔차를 개별 데이터 수준의 차이로 설명
  - 부호와 절댓값 해석을 초심자용으로 정리

### 2. MAE, MSE, RMSE는 오차를 다른 방식으로 요약한다

- 근거:
  - scikit-learn, `mean_absolute_error`
  - scikit-learn, `mean_squared_error`
  - scikit-learn, `3.4. Metrics and scoring: quantifying the quality of predictions`
- 반영 방식:
  - MAE는 평균적인 빗나감
  - MSE는 큰 오차를 더 강하게 반영
  - RMSE는 큰 오차에 민감하면서 원 단위로 읽기 쉬운 지표로 일반화
  - 배송 시간, 병원 대기 시간, 매출 예측 같은 업무형 사례로 실증 해석 보강

### 3. R²는 평균 예측보다 얼마나 더 설명하는지를 보여 주는 요약값이다

- 근거:
  - scikit-learn, `r2_score`
  - scikit-learn, `3.4. Metrics and scoring: quantifying the quality of predictions`
- 반영 방식:
  - baseline 대비 설명력 관점으로 정리
  - R²만으로 충분하지 않다는 주의 문구 반영

### 4. 선형회귀의 한계는 직선 가정이 문제 구조를 충분히 담지 못할 때 드러난다

- 근거:
  - scikit-learn, `1.1. Linear Models`
- 반영 방식:
  - 비선형 관계, 구간별 변화, 중요한 특징 누락, 이상치 영향을 초심자용으로 정리
  - 배송 지연, 행사 매출, 초고가 주택 같은 실증 장면으로 보강

### 5. 좋은 지표 하나만으로 모델을 과신하면 안 된다

- 근거:
  - scikit-learn, `3.4. Metrics and scoring: quantifying the quality of predictions`
  - Part 3 앞 절의 baseline, evaluation 흐름
- 반영 방식:
  - baseline, 평균 오차, 큰 오차, 잔차 패턴을 함께 보도록 해석 순서로 정리

### 6. 선형회귀의 역사에는 least squares의 관측 오차 처리 전통과 regression의 통계 해석 전통이 함께 있다

- 근거:
  - 통계사에서 일반적으로 정리되는 least squares의 천문학·측지학 배경
  - regression 용어의 Galton 계보
- 반영 방식:
  - 세부 연표 대신 `오차를 줄이는 계산 방법`과 `관계를 해석하는 통계 용어`라는 두 흐름으로 일반화

### 7. 선형회귀의 주요 논란은 인과 과잉해석, 계수 과잉해석, 높은 R²의 과신, 역사적 사회 해석 문제로 정리할 수 있다

- 근거:
  - 회귀 해석에 대한 통계 입문서·교육 자료의 공통 경고
  - regression 용어의 역사적 배경
- 반영 방식:
  - 기술적 논란과 사회적 해석 논란을 분리
  - 초심자 수준에서 조심해야 할 해석 규칙으로 정리

## 본문 반영 판단

- 10.2는 지표의 엄밀한 통계 해석보다 `어떻게 읽을 것인가`에 초점을 둔다.
- 식 전개보다 residual과 metric의 역할 차이를 먼저 설명한다.
- Python 예제는 10.1의 작은 데이터셋을 재사용해 predictions, residuals, MAE, RMSE, R²를 한 번에 출력한다.
- 추가 예제로 outlier가 있을 때 MAE와 RMSE가 다르게 반응하는 비교를 넣어, 큰 오차 민감도를 실증적으로 보여 준다.
- 역사와 논란은 본 절의 중심을 밀지 않도록 짧은 배경 절로 넣고, 기술적 평가 절과 분리한다.

## 도메인 경계 메모

- P3-10.1:
  - 회귀 문제의 성격
  - 선형회귀의 직관
  - 기울기와 절편의 해석
- P3-10.2:
  - 잔차와 오차
  - 회귀 지표
  - 직선 가정의 한계
  - 지표 해석의 주의점

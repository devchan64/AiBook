# P3-7.2 전처리(preprocessing) - 근거 검토 메모

## 검토 목적

- 전처리를 `원시 입력을 더 적합한 표현으로 바꾸는 단계`로 초심자 기준에서 설명한다.
- 결측치 처리, 스케일 조정, 범주형 인코딩, 파이프라인과 누수 방지를 한 절로 연결한다.
- 알고리즘별 민감도를 과장하지 않고, 어느 계열이 왜 전처리에 더 민감한지 보수적으로 설명한다.

## 핵심 근거

1. scikit-learn, `8.3. Preprocessing data`
   - URL: https://scikit-learn.org/stable/modules/preprocessing.html
   - 확인 날짜: 2026-06-26
   - 반영 포인트:
     - 전처리는 raw feature vectors를 downstream estimator에 더 적합한 표현으로 바꾸는 단계다.
     - 많은 학습 알고리즘, 특히 선형 모델 등은 표준화의 이점을 본다.
     - 특징 분산이 크게 다르면 일부 특징이 목적 함수를 지배할 수 있다.
     - `StandardScaler`, `MinMaxScaler`, `MaxAbsScaler`, `RobustScaler` 같은 대표 도구 이름을 소개할 수 있다.

2. scikit-learn, `8.4. Imputation of missing values`
   - URL: https://scikit-learn.org/stable/modules/impute.html
   - 확인 날짜: 2026-06-26
   - 반영 포인트:
     - `SimpleImputer`는 평균, 최빈값, 상수 같은 전략을 제공한다.
     - 숫자형과 범주형의 결측치 전략을 구분해 설명할 수 있다.

3. scikit-learn, `8.1. Pipelines and composite estimators`
   - URL: https://scikit-learn.org/stable/modules/compose.html
   - 확인 날짜: 2026-06-26
   - 반영 포인트:
     - `Pipeline`은 fit/transform 단계를 연결하는 구조다.
     - `ColumnTransformer`는 서로 다른 칼럼 그룹에 서로 다른 변환을 적용할 수 있다.

4. scikit-learn, `12. Common pitfalls and recommended practices`
   - URL: https://scikit-learn.org/stable/common_pitfalls.html
   - 확인 날짜: 2026-06-26
   - 반영 포인트:
     - train/test split을 먼저 나누고, `fit`과 `fit_transform`은 train에만 적용해야 한다.
     - 전처리에서의 데이터 누수는 성능을 낙관적으로 왜곡한다.
     - pipeline은 누수 방지에 유용하다.

## 본문 일반화 원칙

- 전처리를 단순 청소가 아니라 `입력 표현 변환`으로 설명한다.
- 전처리를 `표현 변환`과 `모델 가정 맞춤`의 두 관점으로 설명한다.
- 결측치, 스케일, 인코딩을 별개 문제로 구분한다.
- `fit`과 `transform`의 역할 차이를 초심자도 설명할 수 있게 단순화한다.
- 거리 기반 모델과 선형 모델이 스케일에 더 민감하다는 점은 보수적으로 설명하고, 트리 계열은 상대적으로 덜 민감하다고만 적는다.
- 커리큘럼상 이 절이 특징 선택 뒤, 모델 선택 전, 알고리즘 입문 전의 연결 절이라는 점을 본문에서 드러낸다.
- 학술적으로는 전처리를 `원시 데이터를 학습 가능한 입력 표현으로 옮기는 독립 단계`로 설명하고, 커리큘럼적으로는 Module 2의 평가 관점에서 Module 3의 실험 설계 관점으로 넘어가는 전환점으로 정리한다.

## 도메인 경계

- 이 절은 전처리의 입문적 의미와 기본 판단을 다룬다.
- 고급 변환, PCA, whitening, sparse 최적화, 세부 파라미터는 뒤 절이나 보충 설명 대상으로 넘긴다.
- 알고리즘별 세부 민감도는 P3-10 이후 절에서 다시 구체화할 수 있다.

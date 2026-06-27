# P3-13.1 SVM의 직관 근거 검토

## 핵심 주장

### 1. SVM은 분류, 회귀, 이상치 탐지에 쓰이는 지도학습 방법군이다

- 근거:
  - scikit-learn, `Support Vector Machines`
- 반영 방식:
  - 본문에서는 초심자 기준으로 이진 분류를 중심에 둔다
  - 다른 용도는 범위 소개 수준으로만 언급

### 2. SVM의 교육적 핵심은 margin 최대화 직관이다

- 근거:
  - scikit-learn, `Support Vector Machines`
  - Cortes and Vapnik (1995)
- 반영 방식:
  - 수식 유도보다 `여러 경계 중 더 여유 있는 경계`라는 설명으로 일반화

### 3. support vector는 경계에 가장 가까운 핵심 점들이다

- 근거:
  - scikit-learn, `Support Vector Machines`
  - SVM 입문 일반 설명
- 반영 방식:
  - `경계를 떠받치는 점들`이라는 한국어 표현으로 설명
  - 전체 데이터가 아닌 근접 점들이 중요하다는 구조를 강조

### 4. 완벽한 분리가 어려운 현실 데이터에서는 soft margin 직관이 필요하다

- 근거:
  - scikit-learn, `Support Vector Machines`
  - Cortes and Vapnik (1995)
- 반영 방식:
  - `여유와 오류 허용의 균형`이라는 문장으로 입문 설명
  - `C`의 수식적 역할은 뒤 절이나 튜닝 절과 연결만 둔다

### 5. SVM은 통계학습이론과 일반화 논의에서 중요한 역사적 위치를 가진다

- 근거:
  - Cortes and Vapnik (1995)
  - 앞 절 P3-5.2의 statistical learning theory 흐름
- 반영 방식:
  - 세부 연표보다 `어떤 경계가 더 좋은가`라는 기준을 margin으로 제시한 점을 역사적 의미로 정리

## 본문 반영 판단

- 13.1은 커널을 다루지 않는다. 커널은 13.2로 명시적으로 넘긴다.
- Python 예제는 SVM 학습기 자체보다 `후보 경계의 margin 비교`를 직접 계산하게 한다.
- 예제 출력에는 각 경계 후보의 최소 거리와 support-like points를 함께 보여 준다.
- 두 번째 예제로 `완벽 분리`가 깨지는 순간을 보여 주고, soft margin의 필요를 입문 수준에서 연결한다.
- 로지스틱 회귀, k-NN, SVM 비교 표를 둬서 도메인 경계를 분명히 한다.
- `확률 출력`이나 `predict_proba` 중심 설명은 하지 않는다. SVM의 중심은 margin과 support vector에 둔다.
- 사례는 사기 탐지, 채용 분류, 이상 탐지처럼 `경계 안정성`을 떠올리기 쉬운 실무 장면으로 보강한다.
- 도식은 `small margin vs large margin`, `clean separation vs soft margin`처럼 서로 다른 질문을 분리해 보여 준다.

## 도메인 경계 메모

- P3-13.1:
  - margin
  - support vector
  - soft margin의 직관
  - 경계 품질의 개념
- P3-13.2:
  - kernel
  - 비선형 경계
  - 고차원 특징 공간의 입문적 의미

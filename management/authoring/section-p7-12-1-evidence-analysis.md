# P3-12.1 k-NN의 직관 근거 검토

## 핵심 주장

### 1. nearest neighbors는 분류와 회귀에 쓰이는 비모수적(non-parametric) 방법이다

- 근거:
  - scikit-learn, `Nearest Neighbors`
- 반영 방식:
  - 본문에서는 `식을 몇 개 학습하는 방식보다 데이터 비교를 더 직접 사용한다`는 초심자용 설명으로 일반화
  - 엄밀한 통계 정의는 생략

### 2. k-NN은 새 입력의 가까운 이웃을 보고 예측을 만든다

- 근거:
  - scikit-learn, `Nearest Neighbors`
  - scikit-learn, `KNeighborsClassifier`
- 반영 방식:
  - `query -> nearest neighbors -> labels -> vote` 흐름으로 단순화
  - 복잡한 내부 구현보다 판단 순서를 먼저 보여 줌

### 3. `k`는 몇 개의 이웃을 참조할지 정하며, 값에 따라 민감도와 안정성이 달라진다

- 근거:
  - scikit-learn, `KNeighborsClassifier`
  - nearest neighbors 일반 입문 설명
- 반영 방식:
  - 작은 k는 local/noisy, 큰 k는 smoother라는 교육용 설명으로 정리
  - 최적 k 선택의 수학적 절차는 P3-9와 뒤 절로 넘김

### 4. k-NN은 앞 절의 선형 경계 모델과 다른 관점을 제공한다

- 근거:
  - P3-11.2에서 정리한 decision boundary 관점
  - nearest neighbors의 instance-based prediction 구조
- 반영 방식:
  - `global boundary vs local neighbors` 대비로 설명
  - 로지스틱 회귀와의 비교를 커리큘럼 연결 용도로 사용

### 5. k-NN에서 거리와 스케일은 핵심 변수이며, 다음 절에서 분리 설명해야 한다

- 근거:
  - scikit-learn, `Nearest Neighbors`
  - 앞선 Part 3 전처리 절에서의 scale 민감도 설명
- 반영 방식:
  - 12.1에서는 문제 제기만 하고
  - 12.2에서 distance metric, scale sensitivity를 다루도록 경계 유지

### 6. 역사 설명은 `패턴 분류를 사례 비교로도 읽을 수 있게 만든 고전 방법` 수준에서 정리한다

- 근거:
  - Cover and Hart, *Nearest Neighbor Pattern Classification* (1967)
- 반영 방식:
  - 세부 연표보다 교육적 의미를 우선
  - `경계식만이 아니라 사례 비교`라는 관점 전환으로 일반화

## 본문 반영 판단

- 12.1은 구현 최적화보다 예측 직관에 집중한다.
- Python 예제는 외부 라이브러리 의존을 줄이기 위해 순수 Python으로 작성한다.
- 코드 출력에는 query, prediction, neighbor labels, distance를 함께 보여 준다.
- `lazy learning` 같은 용어는 본문 중심 용어로 밀지 않고, `예측 시점에 비교 작업이 들어간다`는 한국어 설명으로 대체한다.
- 분류 중심으로 설명하되, 회귀에도 쓸 수 있다는 정도만 언급한다.

## 도메인 경계 메모

- P3-12.1:
  - k-NN의 핵심 직관
  - `k`의 의미
  - 사례 기반 판단
  - 학습/예측 구조의 감각
- P3-12.2:
  - 거리(distance)
  - 스케일(scale)
  - 특징 단위 차이
  - 가까움 정의의 위험

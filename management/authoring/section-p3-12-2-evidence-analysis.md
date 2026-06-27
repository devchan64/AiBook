# P3-12.2 거리(distance)와 스케일(scale) 근거 검토

## 핵심 주장

### 1. nearest neighbors 계열에서 거리 계산은 핵심 판단 규칙이다

- 근거:
  - scikit-learn, `Nearest Neighbors`
  - scikit-learn, `KNeighborsClassifier`
- 반영 방식:
  - 본문에서 `누가 이웃으로 뽑히는가를 정하는 규칙`으로 일반화
  - 알고리즘 내부 구현보다 교육적 해석을 우선

### 2. 거리 함수(metric)가 달라지면 가까운 이웃의 순서가 달라질 수 있다

- 근거:
  - nearest neighbors 일반 설명
  - scikit-learn neighbors 문서의 metric 선택 구조
- 반영 방식:
  - 유클리드 거리와 맨해튼 거리의 입문 예시로 단순화
  - 모든 metric의 수학적 성질 비교는 범위 밖으로 둠

### 3. feature scaling은 many machine learning algorithms에서 중요한 preprocessing step이다

- 근거:
  - scikit-learn, `Importance of Feature Scaling`
- 반영 방식:
  - `거리 기반 모델에서 각 특징의 영향력 균형`이라는 한국어 설명으로 일반화
  - 표준화가 왜 필요한지 결과 변화 중심으로 설명

### 4. 스케일 조정은 자동 만능 개선이 아니다

- 근거:
  - scikit-learn, `Importance of Feature Scaling`
    - scaling 후 lower-scale noisy features가 더 기여해 overfitting이 증가할 수 있다는 설명
- 반영 방식:
  - `스케일 조정이 항상 성능을 올린다고 단정하지 않는다`는 경고로 반영
  - 초심자에게 과한 단정 문구를 피함

### 5. 거리와 스케일 문제는 k-NN에 한정되지 않고 뒤 장들과도 연결된다

- 근거:
  - Part 3 전처리 절에서 이미 정리한 scale sensitivity
  - scikit-learn feature scaling example
- 반영 방식:
  - SVM, 임베딩, 벡터 검색, 차원 축소로 이어지는 관점 메모를 본문에 둠

## 본문 반영 판단

- 12.2는 공식 유도보다 `거리 규칙`과 `표현 규칙`의 중요성을 먼저 보여 준다.
- Python 예제는 외부 라이브러리 의존 없이 순수 Python으로 작성한다.
- 예제는 동일 query가 scaling 전후에 다른 이웃을 갖는 사례를 직접 출력한다.
- `fit scaler on train only` 같은 데이터 누수(data leakage) 논의는 이 절의 중심에서 벗어나므로 길게 확장하지 않는다.
- k-NN 문맥에서 다루되, 뒤 장으로 이어지는 거리 기반 사고의 입문 역할을 분명히 둔다.

## 도메인 경계 메모

- P3-12.2:
  - distance metric
  - scale imbalance
  - preprocessing necessity
  - same data / different representation / different neighbors
- 뒤 절:
  - metric learning
  - 고차원 거리 문제
  - 벡터 검색의 similarity 선택

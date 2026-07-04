# P3-13.2 커널(kernel)의 입문적 의미 근거 검토

## 핵심 주장

### 1. SVM은 커널을 통해 비선형 분류 구조까지 다룰 수 있는 대표 방법이다

- 근거:
  - scikit-learn, `Support Vector Machines`
- 반영 방식:
  - `표현 공간을 바꾸면 선형 경계가 다시 의미를 가질 수 있다`는 교육용 설명으로 일반화

### 2. 커널의 핵심은 고차원 특징 공간을 직접 다 펼치지 않고도 그 공간의 유사도 계산 효과를 다루는 데 있다

- 근거:
  - scikit-learn, `Support Vector Machines`
  - kernel methods 일반 입문 설명
- 반영 방식:
  - 엄밀한 내적/힐베르트 공간 수식 대신 `유사도를 원래 공간 계산으로 대신 다룬다`는 문장으로 설명

### 3. XOR형 예시는 비선형 경계 필요를 보여 주는 입문 사례로 적합하다

- 근거:
  - 선형 분리 가능성(linear separability) 입문 교육의 대표 예시
- 반영 방식:
  - `x1 * x2`라는 새 특징을 추가하면 구조가 단순해진다는 소규모 Python 예제로 반영

### 4. polynomial과 RBF는 입문 단계에서 각각 `상호작용 특징`, `지역적 유사도`의 감각으로 설명할 수 있다

- 근거:
  - scikit-learn, `Support Vector Machines`
- 반영 방식:
  - 정식 수식보다 직관 설명과 후보 선택 감각을 우선

### 5. 커널 SVM은 항상 기본 선택지가 아니라, 선형 경계가 부족해 보일 때 떠올리는 후보여야 한다

- 근거:
  - scikit-learn SVM 문서의 모델 범위와 계산 특성
  - 앞 절 P3-8 모델 선택, P3-9 튜닝/비용 문맥
- 반영 방식:
  - 실무 후보 선택 표와 계산 비용 주의 문장으로 반영

### 6. 역사 설명은 `최적 마진 분류기의 비선형 확장 가능성`을 보여 주는 수준으로 유지한다

- 근거:
  - Boser, Guyon, Vapnik (1992)
- 반영 방식:
  - 세부 수학보다 `선형 경계 -> richer feature space -> kernel shortcut` 흐름으로 정리

## 본문 반영 판단

- 13.2는 커널 함수 목록을 외우게 하지 않는다.
- Python 예제는 scikit-learn 의존 없이 작은 XOR형 표현 변환만 보여 준다.
- 도식은 `original space에서 선형 실패`, `feature space 전환`, `explicit map vs kernel shortcut`으로 질문을 분리한다.
- `gamma`, `degree`, `coef0`는 언급만 하고 튜닝은 P3-9 맥락과 뒤 절로 넘긴다.
- 커널을 마법처럼 설명하지 않고, 표현 변환과 유사도 계산의 조합으로 설명한다.

## 도메인 경계 메모

- P3-13.2:
  - nonlinear-looking pattern
  - feature space
  - kernel intuition
  - polynomial / RBF 감각
- 뒤 절:
  - 하이퍼파라미터 세부 튜닝
  - 커널별 계산 비용 비교
  - 더 엄밀한 수학 배경

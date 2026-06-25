# P3-2.2 근거 검토 메모

## 대상 섹션

- `docs/parts/part-03/chapter-02/section-02.md`
- 주제: 비지도학습(unsupervised learning)

## 확인한 근거

### scikit-learn, Unsupervised learning

- URL: https://scikit-learn.org/stable/unsupervised_learning.html
- 확인 날짜: 2026-06-25
- 활용 내용:
  - 비지도학습 문서가 군집화(clustering), 다양체 학습(manifold learning), 행렬 분해(matrix factorization), 이상치 탐지(outlier detection), 밀도 추정(density estimation) 등을 포함해 넓은 범주로 다루는 점을 확인했습니다.
  - 입문 섹션에서는 전체 알고리즘 목록을 나열하기보다 군집화, 차원 축소, 이상치 탐지를 중심으로 좁혀 설명했습니다.

### Google for Developers, What is clustering?

- URL: https://developers.google.com/machine-learning/clustering/overview
- 확인 날짜: 2026-06-25
- 활용 내용:
  - 군집화가 라벨 없는 예시(unlabeled examples)를 유사도(similarity)에 따라 묶는 비지도학습 기법으로 설명되는 점을 확인했습니다.
  - 실제 적용에서는 유사도 기준을 명시해야 하며, 특징이 많을수록 비교가 복잡해진다는 설명을 군집화 해석 주의점에 반영했습니다.
  - 클러스터 ID가 큰 데이터셋을 단순화하는 표현으로 쓰일 수 있다는 관점은 지도학습 준비 단계로 이어지는 설명에 반영했습니다.

## 반영 판단

- Part 3 이후는 초심자를 기준으로 작성해야 하므로, 알고리즘 이름보다 라벨 없는 고객 데이터 예시를 먼저 배치했습니다.
- 비지도학습 결과를 `정답`으로 설명하지 않고 `구조 후보`로 표현했습니다.
- 군집 이름은 모델이 자동으로 제공하는 의미가 아니라 사람이 붙이는 해석임을 반복해 명시했습니다.
- Mermaid 도식은 본문 설명을 위해 새로 작성한 자체 도식입니다.

## 주의할 표현

- 군집화 결과를 실제 고객 유형이나 자연 범주로 단정하지 않습니다.
- 차원 축소 그림이 원래 데이터의 모든 정보를 보존한다고 말하지 않습니다.
- 이상치 후보를 실제 부정행위, 오류, 위험으로 바로 단정하지 않습니다.
- k-means, PCA, DBSCAN 등 알고리즘의 수식과 구현은 이 섹션의 범위를 넘기므로 후속 섹션에서 다룹니다.

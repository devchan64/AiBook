# P3-17.1 클러스터링의 직관 근거 메모

## Section 역할

- Part 3 Module 6 Chapter 17의 첫 번째 절입니다.
- 지도학습 중심 흐름에서 비지도학습으로 넘어가며, 클러스터링을 `라벨 없는 구조 탐색`으로 설명합니다.
- 초심자에게 군집(cluster)과 클래스(class)를 구분하는 감각을 주는 절입니다.

## 핵심 주장

1. 클러스터링은 unlabeled data에 대해 구조를 찾는 비지도학습 작업이다.
2. 클러스터링 알고리즘은 입력으로 보통 `(n_samples, n_features)` 형태의 데이터를 받는다.
3. k-means는 중심(centroid) 기반 직관을 가진 대표 알고리즘이다.
4. k-means는 군집 수를 미리 정해야 하며, convex / isotropic 가정에 잘 맞는 편이다.
5. DBSCAN은 밀도 기반 직관을 가지며, uneven cluster size와 outlier 처리에 유리할 수 있다.
6. 군집 결과는 사람이 미리 준 정답 클래스와 다르며, 해석이 추가로 필요하다.

## 근거 출처

### 1) scikit-learn User Guide - Clustering

- 문서: `2.3. Clustering`
- URL: https://scikit-learn.org/stable/modules/clustering.html
- 확인 날짜: 2026-06-27
- 반영 포인트:
  - clustering이 unlabeled data에 대해 수행된다는 설명
  - 표준 입력 행렬 `(n_samples, n_features)` 설명
  - clustering methods overview 표
  - KMeans가 equal variance, inertia 최소화, cluster count 지정이 필요한 알고리즘이라는 설명
  - DBSCAN이 non-flat geometry, uneven cluster size, outlier removal에 유용하다는 개요 설명

### 2) scikit-learn API Reference - KMeans

- 문서: `KMeans`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
- 확인 날짜: 2026-06-27
- 반영 포인트:
  - 대표적인 중심 기반 clustering estimator라는 점 확인용

### 3) scikit-learn API Reference - DBSCAN

- 문서: `DBSCAN`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html
- 확인 날짜: 2026-06-27
- 반영 포인트:
  - density-based clustering estimator라는 점 확인용

## 집필 판단

- 17.1에서는 구현보다 문제 정의를 먼저 잡았습니다.
- 초심자 오해를 줄이기 위해 군집을 곧바로 정답 범주로 읽지 않도록 클래스와 군집의 차이를 본문에서 분리했습니다.
- 저장소 의존성에 `scikit-learn`이 아직 없으므로, 실제 라이브러리 예제보다 점 집합 직관을 보여 주는 작은 Python 예제를 우선 사용했습니다.
- k-means와 DBSCAN은 17.1에서 직관 수준으로만 맛보기로 소개하고, 결과 해석의 위험은 17.2에서 이어서 정리하도록 역할을 분리했습니다.

## 제외한 내용

- 실루엣 점수(silhouette score)
- 계층적 군집화 세부 알고리즘
- 스펙트럴 클러스터링과 그래프 기반 방법
- HDBSCAN, OPTICS의 파라미터 차이

이 내용은 후속 절이나 심화 파트에서 다시 확장할 수 있습니다.

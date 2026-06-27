# P3-18.1 차원 축소 근거 메모

## Section 역할

- Part 3 Module 6 Chapter 18의 첫 번째 절입니다.
- 클러스터링 다음에, 많은 특징을 더 적은 축으로 줄여 보는 차원 축소의 입문적 목적을 설명합니다.
- 초심자에게 PCA를 처음 연결하는 준비 절입니다.

## 핵심 주장

1. 차원 축소는 많은 특징을 더 적은 수의 축/성분으로 바꾸는 비지도학습적 변환 관점으로 이해할 수 있다.
2. PCA는 다변량 데이터셋을 연속적인 직교 성분으로 분해하며, 가장 많은 분산을 설명하는 방향을 먼저 찾는다.
3. PCA는 `fit`에서 성분을 학습하고, 새 데이터에 `transform`처럼 적용할 수 있는 transformer 관점으로 이해할 수 있다.
4. PCA는 입력을 center하지만 기본적으로 feature별 scale 조정까지 자동으로 하지는 않는다.
5. 차원 축소는 계산과 시각화를 쉽게 하지만 정보 손실을 함께 가져온다.

## 근거 출처

### 1) scikit-learn User Guide - decomposition

- 문서: `2.5. Decomposing signals in components (matrix factorization problems)`
- URL: https://scikit-learn.org/stable/modules/decomposition.html
- 확인 날짜: 2026-06-27
- 반영 포인트:
  - PCA를 successive orthogonal components that explain maximum variance로 설명한 부분
  - PCA가 transformer object라는 설명
  - PCA가 center하지만 scale하지 않는다는 설명
  - PCA projection이 시각화와 downstream 모델에 유용할 수 있다는 설명

### 2) scikit-learn API Reference - PCA

- 문서: `PCA`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
- 확인 날짜: 2026-06-27
- 반영 포인트:
  - 대표 decomposition estimator로서 PCA 연결 확인

## 집필 판단

- 18.1은 수학보다 표현 변환의 직관을 우선했습니다.
- 초심자에게는 고유값/고유벡터보다 `축을 다시 잡는다`, `분산 큰 방향을 남긴다`, `더 적은 축으로 요약한다`는 감각이 먼저라고 판단했습니다.
- 저장소 의존성에 `scikit-learn`이 아직 없으므로, PCA 자체 실행 예제 대신 축을 줄이는 감각을 보여 주는 장난감 Python 예제를 넣었습니다.

## 제외한 내용

- PCA의 엄밀한 선형대수 유도
- kernel PCA, sparse PCA, incremental PCA 상세 비교
- explained_variance_ratio_ 실습
- 차원 축소 결과의 시각화 왜곡

이 내용은 P3-18.2나 후속 심화 파트에서 다시 확장할 수 있습니다.

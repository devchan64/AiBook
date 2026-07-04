# P3-18.2 시각화와 정보 손실 근거 메모

## Section 역할

- Part 3 Module 6 Chapter 18의 두 번째 절입니다.
- 18.1에서 차원 축소의 목적과 PCA 직관을 설명한 뒤, 차원 축소 그림을 어떻게 읽어야 하는지 해석 경계를 정리합니다.
- 초심자에게 `그림은 유용하지만 과신하면 안 된다`는 태도를 주는 절입니다.

## 핵심 주장

1. 차원 축소 결과는 더 읽기 쉬운 표현이지만 원래 고차원 구조의 완전한 복사본은 아니다.
2. 차원을 줄이면 일부 정보 손실과 왜곡이 생길 수 있다.
3. PCA는 큰 분산 방향을 우선 보존하려는 경향이 있으므로, 작은 세부 차이는 약해질 수 있다.
4. 2D/3D 시각화는 탐색적 분석과 설명에는 유용하지만, 최종 증거로 단정하면 위험하다.
5. 차원 축소 결과는 군집 가설이나 이상치 가설을 만들게 해 주지만, 원래 데이터와 후속 검토가 필요하다.

## 근거 출처

### 1) scikit-learn User Guide - decomposition

- 문서: `2.5. Decomposing signals in components (matrix factorization problems)`
- URL: https://scikit-learn.org/stable/modules/decomposition.html
- 확인 날짜: 2026-06-27

### 2) scikit-learn API Reference - PCA

- 문서: `PCA`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
- 확인 날짜: 2026-06-27

## 제외한 내용

- explained_variance_ratio_ 실습
- t-SNE / UMAP 세부 시각화 착시 비교
- trustworthiness / continuity 지표
- 재구성 오차의 공식 유도

이 내용은 후속 심화 절이나 프로젝트 파트에서 다시 확장할 수 있습니다.

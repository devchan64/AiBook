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
- 반영 포인트:
  - PCA가 분산을 많이 설명하는 성분을 우선 찾는다는 설명
  - PCA projection이 시각화와 downstream 사용에 유용하다는 설명
  - transform된 저차원 표현이 원래 데이터의 요약이라는 점

### 2) scikit-learn API Reference - PCA

- 문서: `PCA`
- URL: https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
- 확인 날짜: 2026-06-27
- 반영 포인트:
  - PCA가 feature projection / component representation으로 읽힐 수 있는 점 확인

## 집필 판단

- 18.2는 새로운 알고리즘 추가보다 해석 경계에 집중했습니다.
- 초심자가 가장 많이 하는 오해인 `2D에서 가까우면 원래도 가깝다`, `덩어리가 보이면 진짜 범주다`를 본문 중심에 놓았습니다.
- 저장소 의존성에 `scikit-learn`이 없으므로, 실제 PCA 시각화 코드보다 정보 압축 감각을 보여 주는 장난감 예제를 사용했습니다.
- 17장의 클러스터링과 연결해, 차원 축소 그림 위의 군집 해석 착시도 함께 짚었습니다.

## 제외한 내용

- explained_variance_ratio_ 실습
- t-SNE / UMAP 세부 시각화 착시 비교
- trustworthiness / continuity 지표
- 재구성 오차의 공식 유도

이 내용은 후속 심화 절이나 프로젝트 파트에서 다시 확장할 수 있습니다.

# 8.2 근거 검토 메모

이 문서는 `docs/chapters/chapter-08/section-02.md`의 근거 연결과 표현 판단을 기록한 관리 메모입니다.

## 작성 목적

- 8.1의 라벨(label) 설명을 이어 받아, 비지도학습(unsupervised learning)을 라벨 없는 데이터에서 구조(structure)를 찾는 방식으로 설명합니다.
- `라벨 없음`을 `목표 없음`이나 `아무 기준 없음`으로 오해하지 않도록 정리합니다.
- 군집화(clustering), 차원 축소(dimensionality reduction), 표현(representation)을 입문 수준에서 구분합니다.
- 클러스터 라벨(cluster label)과 사람이 붙인 지도학습 라벨(label)을 혼동하지 않도록 경계를 둡니다.
- 군집화가 추상적으로 보이지 않도록 입력 데이터, 비교 특징, 가능한 군집, 해석 주의를 예시로 나눠 설명합니다.
- 사람이 직접 데이터를 묶는 수동 분류와 알고리즘 기반 군집화(clustering)를 구분합니다.

## 사용 근거

| 자료 | 로컬 확인 | 반영 내용 |
| --- | --- | --- |
| Google for Developers, `Machine Learning Glossary` | `.tmp/section-8-2-evidence/google-ml-glossary.html`, `.tmp/section-8-2-evidence/google-ml-glossary.txt` | unsupervised learning, unlabeled examples, clustering, cluster 설명 |
| scikit-learn, `2. Unsupervised learning` | `.tmp/section-8-2-evidence/scikit-learn-unsupervised-learning.html`, `.tmp/section-8-2-evidence/scikit-learn-unsupervised-learning.txt` | 비지도학습 아래의 clustering, manifold learning, PCA 등 항목 구조 |
| scikit-learn, `2.3. Clustering` | `.tmp/section-8-2-evidence/scikit-learn-clustering.html`, `.tmp/section-8-2-evidence/scikit-learn-clustering.txt` | unlabeled data clustering, `labels_`가 training data의 cluster labels라는 점, k-means와 clustering 평가 주의 |
| scikit-learn, `2.5. Decomposing signals in components` | `.tmp/section-8-2-evidence/scikit-learn-decomposition.html`, `.tmp/section-8-2-evidence/scikit-learn-decomposition.txt` | PCA, dimensionality reduction, explained variance 설명 |
| Stanford CS229, `Machine Learning Notes` | `.tmp/chapter-04-reference-review/stanford-cs229-main-notes.pdf`, `.tmp/chapter-04-reference-review/stanford-cs229-main-notes.txt` | k-means가 라벨 없는 데이터에서 cohesive clusters를 만들고, 가까운 centroid에 배정하는 절차라는 설명 |
| `docs/chapters/chapter-08/section-01.md` | 저장소 본문 | 라벨(label), 라벨링(labeling), 구분 표식 설명과 도메인 경계 |
| `docs/chapters/chapter-05/section-01.md` | 저장소 본문 | 학습 유형별 경험과 신호 구분 |

## 확인한 원문 위치

- `.tmp/section-8-2-evidence/google-ml-glossary.txt`
  - clustering 항목과 examples are grouped 후 사람이 cluster 의미를 붙일 수 있다는 설명: 2425-2445행 부근
  - labeled example과 unlabeled example 구분: 4737-4747행 부근
  - hierarchical clustering 설명: 6483-6509행 부근
- `.tmp/section-8-2-evidence/scikit-learn-unsupervised-learning.txt`
  - `2. Unsupervised learning` 제목과 clustering, manifold learning, PCA 등 항목 구조: 130-165행 부근
- `.tmp/section-8-2-evidence/scikit-learn-clustering.txt`
  - unlabeled data의 clustering을 `sklearn.cluster`로 수행한다는 설명: 132-139행 부근
  - clustering algorithm의 class/function 구조와 training data의 `labels_` 설명: 141-149행 부근
  - clustering methods overview와 다양한 알고리즘의 조건 차이: 180-315행 부근
  - K-means가 샘플을 n개 그룹으로 나누려 한다는 설명: 342-347행 부근
  - inertia와 cluster 가정의 한계, high-dimensional space 문제와 PCA 언급: 373-387행 부근
  - K-means의 centroids, nearest centroid assignment, centroid update 절차: 398-411행 부근
- `.tmp/section-8-2-evidence/scikit-learn-decomposition.txt`
  - PCA가 다변량 데이터셋을 분산을 많이 설명하는 직교 성분들로 분해한다는 설명: 137-145행 부근
  - 낮은 차원 공간으로 투영하면서 설명된 분산을 많이 보존한다는 설명: 233-245행 부근
- `.tmp/chapter-04-reference-review/stanford-cs229-main-notes.txt`
  - clustering은 `{x(1), ..., x(n)}` training set을 cohesive clusters로 묶고, label `y(i)`가 없다는 설명: 6599-6602행 부근
  - k-means는 cluster centroids를 초기화하고 각 training example을 가장 가까운 centroid에 배정한다는 설명: 6603-6624행 부근
  - 각 training example과 배정된 centroid 사이의 squared distances 합을 측정한다는 설명: 6647-6650행 부근

## 핵심 주장별 검토

| 본문 주장 | 근거 연결 | 판단 |
| --- | --- | --- |
| 비지도학습은 라벨 없는 데이터에서 구조를 찾는다 | Google Glossary의 unlabeled examples, scikit-learn unsupervised learning 구조 | 유지 |
| 라벨 없음은 목표 없음이 아니다 | 비지도학습이 clustering, decomposition, manifold learning 등 구체적 목적을 가진다는 scikit-learn 구조 | 유지. 입문용 일반화 |
| 군집화는 비슷한 것끼리 묶는 비지도학습 예시다 | Google clustering 설명, scikit-learn clustering 문서 | 유지 |
| 사람의 수동 묶기와 알고리즘 기반 군집화는 다르다 | scikit-learn clustering 문서의 feature, labels_, algorithm 구조, Stanford CS229의 centroid/거리 기반 k-means 설명, 8.1의 사람이 붙인 label 경계 | 유지. 사람의 업무 해석과 계산 절차를 분리 |
| 군집화 결과는 사용한 특징과 기준에 따라 달라질 수 있다 | scikit-learn clustering methods overview와 알고리즘별 조건 차이 | 유지. 수식 대신 예시로만 설명 |
| 클러스터 라벨은 사람이 붙인 지도학습 라벨과 다르다 | scikit-learn `labels_` 설명과 8.1의 label 정의 | 유지. 중요한 오해 방지 지점 |
| 차원 축소는 복잡한 데이터를 더 적은 축으로 다시 보는 방식이다 | scikit-learn PCA/dimensionality reduction 설명 | 유지 |
| 비지도학습 결과는 해석이 필요하다 | Google Glossary의 사람이 cluster 의미를 붙일 수 있다는 설명, clustering 알고리즘 조건 차이 | 유지. 과도한 업무 의미 부여 경계 |
| 딥러닝은 비지도학습과 같은 분류축이 아니다 | 5.1과 8.1의 기존 도메인 경계 | 유지 |

## 도메인 경계

| 섹션 | 맡는 역할 |
| --- | --- |
| 8.1 | 사람이 붙인 라벨과 지도학습의 구조 |
| 8.2 | 라벨 없는 데이터에서 구조, 군집, 표현을 찾는 비지도학습 |
| 8.3 | 행동과 보상을 다루는 강화학습 |
| Part 3 | clustering, PCA, distance, evaluation, high-dimensional data의 실제 알고리즘과 수식 |

## 보수화한 표현

- “라벨이 없으므로 자유롭게 배운다”라고 쓰지 않았습니다. 라벨은 없지만 구조를 찾는 목표는 있다고 설명했습니다.
- “비지도학습이 진짜 의미를 발견한다”라고 쓰지 않았습니다. 결과는 후보 구조이며 사람의 해석과 검토가 필요하다고 제한했습니다.
- “군집화가 사람처럼 알아서 분류한다”라고 쓰지 않았습니다. 사람이 정한 특징과 알고리즘의 계산 기준에 따라 묶음을 찾는 절차로 설명했습니다.
- 클러스터 번호를 사람이 붙인 라벨과 같은 것으로 쓰지 않았습니다.
- 쇼핑몰 고객, 고객 문의, 뉴스 기사, 상품 이미지, 서버 로그 예시는 개념 설명용입니다. 특정 알고리즘의 성능이나 실제 업무 분류 정확도를 주장하지 않습니다.
- PCA와 차원 축소는 수식 없이 “중요한 구조를 가능한 한 유지하며 낮은 차원으로 본다”는 입문 표현으로 제한했습니다.
- 표현(representation)은 깊게 다루지 않고, 비지도학습과 연결될 수 있는 관점으로만 소개했습니다.

## 남은 검토 사항

- Part 3에서 clustering과 PCA를 실제 알고리즘, 거리 기준, 평가 기준과 함께 다시 다룹니다.
- 8.3에서는 `라벨 없음`과 `보상 신호`의 차이를 명확히 해야 합니다.
- 8.2의 `표현` 설명은 Chapter 9의 표현 학습과 겹치지 않도록 이후 장에서 확장합니다.

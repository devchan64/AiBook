<a id="eigenvector"></a>

### 고유벡터(eigenvector)

- 뜻: 어떤 행렬을 적용해도 방향은 유지되고 크기만 바뀌는 특별한 방향 벡터입니다. PCA에서는 공분산 행렬의 고유벡터를 데이터가 크게 퍼지는 새 축의 방향으로 읽습니다.
- 왜 중요한가: PCA의 `축을 다시 잡는다`는 비유를 실제 계산과 연결해 주기 때문입니다. 고유벡터를 이해하면 주성분이 원래 특징 하나가 아니라 데이터 변동을 잘 설명하는 새 방향이라는 점을 읽을 수 있습니다.
- 함께 볼 개념: `고유값(eigenvalue)`, `공분산 행렬(covariance matrix)`, `PCA(principal component analysis)`
- 중심 Section: `P4-18.1`
- 등장 Section:

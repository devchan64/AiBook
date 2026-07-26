<a id="eigenvalue"></a>

### 고유값(eigenvalue)

- 뜻: 어떤 행렬이 특정 방향 벡터를 같은 방향으로 늘리거나 줄일 때, 그 크기 변화가 얼마나 되는지를 나타내는 값입니다. PCA에서는 공분산 행렬의 고유값을 각 새 축이 설명하는 변동 크기로 읽을 수 있습니다.
- 왜 중요한가: PCA가 새 축을 고르는 기준을 `방향`과 `설명되는 변동 크기`로 나누어 이해하게 해 주기 때문입니다. 고유값이 크면 그 축을 따라 데이터가 더 크게 퍼져 있다고 해석할 수 있습니다.
- 함께 볼 개념: `고유벡터(eigenvector)`, `공분산 행렬(covariance matrix)`, `PCA(principal component analysis)`
- 중심 Section: `P4-18.1`
- 등장 Section:

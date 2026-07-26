<a id="truncated-svd"></a>

### Truncated SVD

- 뜻: 특이값 분해(SVD)에서 가장 중요한 일부 성분만 계산해 큰 행렬을 낮은 차원 표현으로 압축하는 방법입니다.
- 왜 중요한가: PCA와 비슷하게 성분을 줄여 표현하지만, scikit-learn 문맥에서는 입력 행렬을 꼭 중심화하지 않아도 되므로 희소 행렬이나 텍스트-단어 행렬 같은 큰 행렬에서 자주 등장합니다.
- 함께 볼 개념: `PCA(principal component analysis)`, `차원 축소(dimensionality reduction)`, `희소 행렬(sparse matrix)`
- 중심 Section: `P4-18.1`
- 등장 Section:

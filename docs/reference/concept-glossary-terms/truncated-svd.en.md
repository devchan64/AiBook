<a id="truncated-svd"></a>

## Truncated SVD

- Meaning: Truncated SVD computes only a selected number of important components from singular value decomposition to compress a large matrix into a lower-dimensional representation.
- Why it matters: It is close to PCA in spirit, but in the scikit-learn context it does not require centering the input matrix, so it often appears with sparse matrices and text-term matrices.
- Related concepts: `PCA`, `dimensionality reduction`, `sparse matrix`
- Core Section: `P4-18.1`
- Appears in:

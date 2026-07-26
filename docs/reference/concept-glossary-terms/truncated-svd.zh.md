<a id="truncated-svd"></a>

## Truncated SVD

- 含义: Truncated SVD 是只计算奇异值分解中一部分重要成分的方法，用来把大矩阵压缩成较低维的表达。
- 为什么重要: 它和 PCA 的直觉相近，但在 scikit-learn 语境里不要求先把输入矩阵中心化，所以常出现在稀疏矩阵和文本-词矩阵场景中。
- 相关概念: `PCA`, `降维`, `稀疏矩阵`
- 核心 Section: `P4-18.1`
- 出现 Section:

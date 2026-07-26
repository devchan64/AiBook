<a id="rbf-kernel"></a>

## RBF 核(radial basis function kernel)

- 含义: 一种强烈反映点之间距离和局部相似度的常见 kernel。靠近的点会被读成更相似，距离一拉开，相似度就会快速下降。
- 为什么重要: 当数据呈现圆形、局部团块或弯曲 boundary 这类结构时，RBF kernel 可以成为读取线性 boundary 难以处理模式的候选。
- 相关概念: `核函数(kernel)`, `特征空间(feature space)`, `距离(distance)`, `SVM`
- 中心 Section: `P4-13.2`
- 出现 Section: `P4-13.2`

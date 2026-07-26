<a id="kernel"></a>

## 核函数(kernel)

- 含义: 给定两个输入，计算它们在更丰富表示空间里有多相似或多接近的核心函数。在 SVM 语境里，它可以读成：不显式构造所有新特征，也能用原始空间里的计算取得新表示空间里的比较效果。
- 为什么重要: 当原始坐标空间里的 linear boundary 很别扭时，问题可能不只在 boundary 本身，也可能在 representation space。kernel 能帮助读者把非线性结构解释成 `改变读取数据的空间`，而不只是 `画出更复杂的线`。
- 相关概念: `特征空间(feature space)`, `SVM`, `多项式核(polynomial kernel)`, `RBF 核(RBF kernel)`
- 中心 Section: `P4-13.2`
- 出现 Section: `P4-13.2`

<a id="impurity"></a>

## 不纯度(impurity)

- 含义: 在 decision tree 的一个 node 中，表示不同 class 混杂程度的量。分类树可以用 gini、entropy、log loss 等 criterion 来比较 split 前后的混杂程度。
- 为什么重要: 好的 split 通常会把一个混杂的 node 变成几个更少混杂的 node。理解 impurity 后，读者就能把决策树训练读成比较每个问题能否整理 label，而不是单纯凭直觉挑规则。
- 相关概念: `决策树(decision tree)`, `分裂(split)`, `叶(leaf)`, `gini`
- 中心 Section: `P4-14.1`
- 出现 Section: `P4-14.1`

<a id="split"></a>

## 分裂(split)

- 含义: 在 decision tree 中，按照某个问题或标准把数据分成两个或多个分支的动作。对于数值 feature，它常写成 `x <= threshold` 这样的条件。
- 为什么重要: 决策树通过不断选择有用的 split 来建立预测结构。理解 split 后，读者就能看到树不是人手写的规则列表，而是在选择能让当前 node 变得更少混杂的问题。
- 相关概念: `决策树(decision tree)`, `节点(node)`, `叶(leaf)`, `不纯度(impurity)`, `阈值(threshold)`
- 中心 Section: `P4-14.1`
- 出现 Section: `P4-14.1`

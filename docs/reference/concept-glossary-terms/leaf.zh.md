<a id="leaf"></a>

## 叶(leaf)

- 含义: decision tree 中不再继续提问、直接输出最终预测的终点。分类时可以输出 class 或 class proportion，回归时可以输出平均值等代表数值。
- 为什么重要: leaf 能显示经过多次 split 后哪些案例聚到了一起，以及它们会得到什么预测。即使分数相近，如果某个 leaf 里仍然混入很多其他 class，解释和泛化都需要谨慎。
- 相关概念: `决策树(decision tree)`, `分裂(split)`, `节点(node)`, `不纯度(impurity)`
- 中心 Section: `P4-14.1`
- 出现 Section: `P4-14.1`

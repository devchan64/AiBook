<a id="feature-importance"></a>

## 特征重要度

- 含义: 特征重要度是一个总结值，用来表示训练好的模型在预测时相对更多地使用了哪些特征。在树模型里，它可以来自 split 降低了多少 impurity，也可以来自打乱某个特征后性能下降多少。
- 为什么重要: 它是检查模型主要依赖什么的起点。但 importance 是模型使用痕迹，不是现实世界原因排序，也不是因果效果本身。
- 相关概念: `随机森林(random forest)`, `相关特征(correlated features)`
- 中心 Section: `P4-15.2`
- 出现 Section: `P4-15.2`

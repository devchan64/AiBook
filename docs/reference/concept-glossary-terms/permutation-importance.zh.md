<a id="permutation-importance"></a>

## 置换重要度

- 含义: 置换重要度会把某个特征的值随机打乱，再测量模型性能下降多少，以此估计该特征的重要度。
- 为什么重要: MDI 总结模型内部 split 的使用量，而置换重要度检查的是这个特征被破坏后，预测性能会依赖它到什么程度。
- 相关概念: `特征重要度(feature importance)`, `平均不纯度减少(MDI)`, `相关特征(correlated features)`
- 中心 Section: `P4-15.2`
- 出现 Section: `P4-15.2`

<a id="n-estimators"></a>

## n_estimators

- 含义：`n_estimators` 是在集成模型中决定要建立多少个 estimator 的超参数。 在随机森林里，它通常读成森林中的树数；在梯度提升里，它更接近顺序修正阶段或 weak learner 的数量。
- 为什么重要：在随机森林里，树越多，平均判断可能越稳定，但计算成本也会上升。 在梯度提升里，阶段越多，模型越有机会继续减少残余误差，但阶段过多也会增加过拟合风险。 因此 `n_estimators` 同时关系到模型大小、修正机会和运行成本。
- 相关概念：`随机森林(random forest)`，`梯度提升(gradient boosting)`，`学习率(learning rate)`，`集成(ensemble)`
- 中心 Section：`P4-15.1`
- 出现 Section：`P4-15.1`, `P4-16.1`

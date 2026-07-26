<a id="additive-model"></a>

## 加性模型

- 含义：加性模型把最终预测写成多个组成部分的和。 在梯度提升里，最终预测是从基础预测开始，再把各阶段的小修正顺序加上去。
- 为什么重要：从 additive model 角度读，梯度提升就不是 `很多树投票`，而是 `很多修正累加`。 这个区分能帮助读者把 boosting 和随机森林这类最后聚合独立预测的方法分开。
- 相关概念：`梯度提升(gradient boosting)`，`残差(residual)`，`集成(ensemble)`
- 中心 Section：`P4-16.1`
- 出现 Section：`P4-16.1`

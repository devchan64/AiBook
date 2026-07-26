<a id="shrinkage"></a>

## 收缩

- 含义：在梯度提升里，收缩是用 learning rate 缩小每个 weak learner 修正量的策略。 新阶段给出的 correction 不会全部加上去，而是只按较小比例反映，让模型走得更慢。
- 为什么重要：Boosting 会不断减少剩余误差，所以如果单阶段修正太强，就可能很快追上训练数据里的噪声。 shrinkage 会放慢修正速度，帮助降低过度贴合和过拟合风险。 但 learning rate 变小时通常需要更多阶段，因此要和 `n_estimators` 一起读。
- 相关概念：`梯度提升(gradient boosting)`，`学习率(learning rate)`，`过拟合(overfitting)`
- 中心 Section：`P4-16.2`
- 出现 Section：`P4-16.2`

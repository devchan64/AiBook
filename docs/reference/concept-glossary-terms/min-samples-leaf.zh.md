<a id="min-samples-leaf"></a>

## 最小 leaf 样本数(min_samples_leaf)

- 含义：`min_samples_leaf` 是规定决策树每个 leaf 至少要留下多少训练样本的超参数。值越大，leaf 越不容易只代表一两个例外案例。
- 为什么重要：如果 leaf 太小，树可能会把训练数据里的例外说成稳定规则。`min_samples_leaf` 通过要求每个最终判断有更多样本支撑，降低这种过拟合风险。
- 相关概念：`leaf`，`决策树(decision tree)`，`过拟合(overfitting)`，`超参数(hyperparameter)`
- 中心 Section：`P4-14.2`
- 出现 Section：`P4-14.2`

<a id="ccp-alpha"></a>

## ccp_alpha

- 含义：`ccp_alpha` 是 scikit-learn 决策树中用于 Minimal Cost-Complexity Pruning 的复杂度参数。值越大，保留复杂分支的代价越高，因此更多分支可能被剪掉。
- 为什么重要：`ccp_alpha` 控制已经长出来的树要被简化到什么程度。太小可能留下过多残枝并导致过拟合，太大则可能剪掉重要模式并导致欠拟合。
- 相关概念：`剪枝(pruning)`，`决策树(decision tree)`，`过拟合(overfitting)`，`超参数(hyperparameter)`
- 中心 Section：`P4-14.2`
- 出现 Section：`P4-14.2`

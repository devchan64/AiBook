<a id="max-depth"></a>

## 最大深度(max_depth)

- 含义：`max_depth` 是限制决策树(decision tree)从根到 leaf 最多能长到多少层的超参数。值较小时，树更偏向大的模式；值较大或不限制时，树可以提出更细的问题。
- 为什么重要：树越深，越容易贴合训练数据，但也可能记住小例外并产生过拟合。`max_depth` 是在树变得过复杂之前限制它的直观手柄。
- 相关概念：`决策树(decision tree)`，`leaf`，`过拟合(overfitting)`，`超参数(hyperparameter)`
- 中心 Section：`P4-14.2`
- 出现 Section：`P4-14.2`

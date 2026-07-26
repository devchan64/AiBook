<a id="mean-decrease-in-impurity-mdi"></a>

## 平均不纯度减少(MDI)

- 含义: MDI 会把每个 split 降低的 impurity 记到使用该特征的分支上，再在整片森林里取平均，形成特征重要度。
- 为什么重要: 它让随机森林的 `feature_importances_` 可以快速查看，但也可能高估那些在训练数据里容易制造很多 split 的高基数特征。
- 相关概念: `特征重要度(feature importance)`, `不纯度(impurity)`, `随机森林(random forest)`, `高基数特征(high-cardinality feature)`
- 中心 Section: `P4-15.2`
- 出现 Section: `P4-15.2`

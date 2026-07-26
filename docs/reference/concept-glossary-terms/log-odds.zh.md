<a id="log-odds"></a>

### log-odds

- 含义：log-odds 是先把 probability \(p\) 改写成 odds \(p/(1-p)\)，再取 logarithm 得到的值。在 logistic regression 中，log-odds 会和 linear score \(z\) 连在一起。
- 为什么重要：probability 被限制在 0 到 1 之间，而 log-odds 可以跨过负数和正数，因此更容易和 linear formula 相连。它也解释了为什么 `probability 0.5`、`odds 1`、`log-odds 0`、`linear score z = 0` 指向同一个决策中点。
- 相关概念：`logistic regression`, `log loss`, `decision boundary`
- 中心 Section：`P4-11.3`
- 出现 Section：`P4-11.4`

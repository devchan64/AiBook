<a id="softmax"></a>

### softmax

- 含义：softmax 会把多个 score 变成归一化后的值，让它们总和为 1，从而可以像候选项或 class 之间的 probability distribution 那样读取。
- 为什么重要：softmax 连接 class score、类似 probability 的输出和最终候选选择。它说明为什么必须把所有候选 score 放在一起比较，以及为什么某个 class probability 总是相对于其他 class score 来决定。
- 相关概念：`指数函数(exponential function)`, `对数(logarithm)`, `分类(classification)`, `逻辑回归(logistic regression)`
- 中心 Section：`P2-2.4`
- 出现 Section：`P4-11.4`, `P5-3.6`, `P6-4.1`

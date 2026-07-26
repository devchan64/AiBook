<a id="solver"></a>

## solver

- 含义：solver 是在学习目标已经确定以后，真正去寻找 model parameters 的计算过程。在 logistic regression 中，它是把 log loss 和 regularization 组成的目标函数通过反复计算降下来的实现选择。
- 为什么重要：即使模型名一样，换 solver 也可能改变收敛方式、支持的 penalty，以及处理大数据或 sparse input 的能力。所以比较实验时，不能只写 `logistic regression`，还要记录使用了哪个 solver。
- 相关概念：`logistic regression`, `regularization`, `optimization`
- 核心 Section：`P4-11.5`
- 出现 Section：`P4-11.5`

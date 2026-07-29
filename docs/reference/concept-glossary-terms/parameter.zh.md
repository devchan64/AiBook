<a id="parameter"></a>

### 参数(parameter)

- 含义: 在学习过程中被调整的模型内部值。它像权重(weight)和偏置(bias)一样保存在模型内部，决定同一个输入进入模型时会沿着怎样的计算路径产生怎样的输出。这里的 parameter 不是普通函数调用里的 `参数(argument)`，而是机器学习模型通过训练得到并保留下来的内部调整值。
- 为什么重要: 只有区分模型内部学到的 parameter 和外部预先设定的 hyperparameter，才能正确理解训练、调优和验证流程。例如 temperature 是使用者从外部调整的设置值，而权重(weight)和偏置(bias)是训练后保存在模型里的 parameter。这个区分能帮助读者把 `模型学到了什么` 和 `人在外部设定了什么` 分开阅读。
- 相关概念: `模型(model)`, `训练(training)`, `表示(representation)`, `超参数(hyperparameter)`
- 核心 Section: `P1-4.3`
- 出现 Section: `P4-9.1`


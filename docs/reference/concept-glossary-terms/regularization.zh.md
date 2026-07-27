<a id="regularization"></a>

## 正则化(regularization)

- 含义：正则化是在学习过程中加入约束或额外成本，让 model 不只贴紧 training data，而是更偏好简单、稳定、可泛化的解。它不是单纯让训练误差最低，而是让过度复杂或不稳定的解变得不那么有吸引力。训练时临时让部分节点输出或连接失效，是一种代表性的正则化策略。
- 为什么重要：model 可能在 training data 上分数很高，却在新数据上失败。正则化让学习同时包含两个问题：一方面要拟合数据，另一方面要避免没有必要的复杂解。比如不鼓励过大的 weight 或过度敏感的模式，训练分数可能稍微低一些，但 generalization 反而更好。
- 相关概念：`过拟合(overfitting)`, `泛化(generalization)`, `validation`
- 核心 Section：`P5-8.1`
- 出现 Section：`P4-5.1`, `P4-11.5`, `P5-8.2`

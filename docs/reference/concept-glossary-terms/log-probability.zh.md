<a id="log-probability"></a>

## 对数概率(log-probability)

- 含义: log-probability 是某个事件或被选择 action 的 probability 取 logarithm 之后的值。
- 为什么重要: 在策略型强化学习中，`log pi(a|s)` 这样的形式常被用来把所选 action 的 probability 连接到 update 计算。
- 相关概念: `policy gradient`, `REINFORCE`, `log-odds`
- 核心 Section: `P4-19.6`
- 出现 Section:

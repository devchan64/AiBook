<a id="q-value"></a>

## Q-value

- 含义: Q-value 是状态 `s` 下采取行动 `a` 时的行动价值，通常写成 `Q(s, a)`。它用分数表示：现在在这个状态做这个行动，之后整体预期会有多好。
- 为什么重要: Q-learning 这类价值型方法会更新 Q-value，而下一个值从哪里读取会改变更新的性质。因此 Q-value 是比较价值型强化学习更新方式的核心把手。
- 相关概念: `action value`, `Q-learning`, `on-policy`, `value-based reinforcement learning`
- 核心 Section: `P4-19.1`
- 出现 Section: `P4-19.5`

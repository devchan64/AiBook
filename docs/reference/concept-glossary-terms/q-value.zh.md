<a id="q-value"></a>

## Q-value

- 含义: Q-value 是状态 `s` 下采取行动 `a` 时的行动价值，通常写成 `Q(s, a)`。它用分数表示：现在在这个状态做这个行动，之后整体预期会有多好。
- 为什么重要: Q-learning 和 SARSA 都会更新 Q-value，但它们读取下一个值的位置不同。因此 Q-value 是比较价值型强化学习更新方式的核心把手。
- 相关概念: `action value`, `Q-learning`, `SARSA`, `value-based reinforcement learning`
- 核心 Section: `P4-19.1`
- 出现 Section: `P4-19.5`

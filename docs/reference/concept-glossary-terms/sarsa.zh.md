<a id="sarsa"></a>

## SARSA

- 含义: SARSA 是一种价值型强化学习算法，它按 state、action、reward、next state、next action 这一串经验来更新 Q-value。它使用的是下一个状态里实际选择的行动价值。
- 为什么重要: SARSA 是理解 on-policy 的代表例子。它会把实际正在执行的行为策略也反映进值估计，因此适合和 Q-learning 对照，阅读 exploration 成本与失败成本。
- 相关概念: `Q-value`, `Q-learning`, `on-policy`, `exploration`
- 核心 Section: `P4-19.1`
- 出现 Section:

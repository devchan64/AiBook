<a id="q-learning"></a>

## Q-learning

- 含义: Q-learning 是一种价值型强化学习算法，它用下一个状态里看起来最好的 Q-value 来更新当前状态-行动值。它看的不是实际接下来做了什么，而是下一个状态里可用的最好行动价值。
- 为什么重要: Q-learning 是理解 off-policy 的代表例子。它和 SARSA 的差别在于：Q-learning 用看起来最好的下一个行动更新，SARSA 用实际选择的下一个行动更新。
- 相关概念: `Q-value`, `SARSA`, `off-policy`, `value-based reinforcement learning`
- 核心 Section: `P4-19.1`
- 出现 Section: `P4-19.5`

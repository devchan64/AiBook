<a id="off-policy"></a>

## 离策略(off-policy)

- 含义: off-policy 指学习的目标策略，不一定和当前实际产生行动的策略相同。例如，它可以按下一个状态里看起来最好的行动价值来更新，而不只看实际选择的下一个行动。
- 为什么重要: 它说明即使实际行为里混有 exploration，学习仍然可以朝目标策略或最优策略方向推进。这个概念是和 on-policy 对照阅读价值型更新的关键。
- 相关概念: `on-policy`, `policy`, `exploration`, `value-based reinforcement learning`
- 核心 Section: `P4-19.1`
- 出现 Section:

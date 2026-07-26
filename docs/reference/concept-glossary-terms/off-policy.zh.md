<a id="off-policy"></a>

## 离策略(off-policy)

- 含义: off-policy 指学习的目标策略，不一定和当前实际产生行动的策略相同。Q-learning 是常见例子，因为它按下一个状态里看起来最好的行动来更新。
- 为什么重要: 它说明即使实际行为里混有 exploration，学习仍然可以朝目标策略或最优策略方向推进。这个概念是和 on-policy 对照阅读 Q-learning 的关键。
- 相关概念: `Q-learning`, `on-policy`, `policy`, `exploration`
- 核心 Section: `P4-19.1`
- 出现 Section:

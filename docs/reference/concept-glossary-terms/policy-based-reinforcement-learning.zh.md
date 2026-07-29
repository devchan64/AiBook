<a id="policy-based-reinforcement-learning"></a>

## 策略型强化学习(policy-based reinforcement learning)

- 含义: 策略型强化学习不是先给状态或行动建立价值记分板，而是直接调整选择行动的 policy。它更接近`直接改变行动方式`，而不是`先算分数再选择`。把 policy parameters 朝平均 reward 更高的方向更新，是这种方法的代表性下位方式。
- 为什么重要: 这个概念帮助读者区分 value-based 方法和 policy-based 方法在强化学习中的学习对象。它也说明为什么在连续行动、随机行动选择、以及结合 value estimate 更新 policy 的方法里，直接调整 policy 会更自然。
- 相关概念: `强化学习(reinforcement learning)`, `强化学习策略(reinforcement learning policy)`, `奖励(reward)`
- 核心 Section: `P4-19.2`
- 出现 Section: `P4-2.3`, `P4-19.3`, `P4-19.4`

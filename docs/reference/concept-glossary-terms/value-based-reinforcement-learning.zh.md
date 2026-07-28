<a id="value-based-reinforcement-learning"></a>

## 价值型强化学习(value-based reinforcement learning)

- 含义: 价值型强化学习会为状态或状态-行动组合学习长期回报的预期值，再用这些值来选择更好的行动。它不是先直接写出 policy，而是先学习`这个选择从长期看有多好`。
- 为什么重要: 这类算法可以先从状态或状态-行动组合的长期回报价值估计连起来读。这个概念也帮助读者区分 value-based reinforcement learning 与 policy-based reinforcement learning：前者先看值，后者更直接地调整 policy。
- 相关概念: `reinforcement learning`, `reinforcement learning policy`, `reward`, `policy-based reinforcement learning`
- 核心 Section: `P4-19.1`
- 出现 Section: `P4-19.4`, `P4-19.5`

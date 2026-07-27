<a id="safe-reinforcement-learning"></a>

## 安全强化学习(safe reinforcement learning)

- 含义: safe reinforcement learning 是一种强化学习分支，在改进 policy 的同时把安全约束一起纳入考虑，以减少危险动作、损坏或责任问题。它也包括限制 exploration 范围，避免新行动造成不可接受的失败。
- 为什么重要: 在现实应用中，exploration 本身可能制造成本和风险，所以不能只看性能，还要同时看失败容忍度和约束条件。
- 相关概念: `exploration`, `offline reinforcement learning`, `error cost`
- 核心 Section: `P4-19.4`
- 出现 Section:

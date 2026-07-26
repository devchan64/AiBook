<a id="actor-critic"></a>

## actor-critic

- 含义: actor-critic 是同时使用 actor 和 critic 的强化学习结构。actor 负责产生行动或 policy，critic 负责评价这些行动有多好，并把评价信号反馈给更新过程。
- 为什么重要: 它让读者把 policy-based 和 value-based 思路读成角色分工，而不是只能二选一的路线。critic 提供评价信号，可以帮助 policy update 更稳定。
- 相关概念: `policy-based reinforcement learning`, `policy gradient`, `value-based reinforcement learning`
- 核心 Section: `P4-19.2`
- 出现 Section: `P4-19.4`, `P4-19.6`

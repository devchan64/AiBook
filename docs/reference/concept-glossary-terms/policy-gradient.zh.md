<a id="policy-gradient"></a>

## 策略梯度(policy gradient)

- 含义: policy gradient 是一类直接调整 policy parameter、让 expected return 上升的强化学习方法。基本想法是让带来更好 reward 的行动更常出现，让带来较差 reward 的行动更少出现。
- 为什么重要: 它说明 policy 不是固定规则，而是可以被优化的函数。理解 policy gradient，才能把早期 policy gradient 算法、actor-critic 以及后续 policy optimization 方法连成同一条线。
- 相关概念: `policy-based reinforcement learning`, `actor-critic`, `expected return`, `policy`
- 核心 Section: `P4-19.2`
- 出现 Section: `P4-19.6`

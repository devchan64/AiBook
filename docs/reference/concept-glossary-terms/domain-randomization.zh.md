<a id="domain-randomization"></a>

## 域随机化(domain randomization)

- 含义: domain randomization 是一种 sim-to-real 强化策略，故意改变 simulator 条件，让 policy 对现实差异没那么脆弱。
- 为什么重要: 因为 simulator 很难完美复制 reality，所以不能让 policy 只过度适应一种过于干净的模拟条件。
- 相关概念: `sim-to-real gap`, `simulation`, `policy`
- 核心 Section: `P4-19.4`
- 出现 Section:


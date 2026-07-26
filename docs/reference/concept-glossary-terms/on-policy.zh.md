<a id="on-policy"></a>

## 在策略(on-policy)

- 含义: on-policy 指学习当前实际正在执行的 policy 的价值。SARSA 是常见例子，因为它用实际选择的下一个行动来更新。
- 为什么重要: 如果当前行为里包含 exploration 或失误路径，on-policy 学习会把这些成本也反映进值估计。这个概念帮助读者理解为什么 SARSA 在有风险的场景里可能比 Q-learning 更保守。
- 相关概念: `SARSA`, `off-policy`, `policy`, `exploration`
- 核心 Section: `P4-19.1`
- 出现 Section:

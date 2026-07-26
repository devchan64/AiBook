<a id="reinforce"></a>

## REINFORCE

- 含义: REINFORCE 是早期代表性的 policy gradient 算法。它根据一个 episode 中的行动与 reward，提高那些最终带来较好结果的选择概率。
- 为什么重要: 它直接展示了 policy-based reinforcement learning 的基本直觉。理解 REINFORCE，可以先抓住`根据 reward 结果调整行动概率`这一 policy gradient 起点。
- 相关概念: `policy gradient`, `policy-based reinforcement learning`, `episode`
- 核心 Section: `P4-19.2`
- 出现 Section: `P4-19.6`

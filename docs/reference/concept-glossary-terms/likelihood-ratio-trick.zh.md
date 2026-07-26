<a id="likelihood-ratio-trick"></a>

## 似然比技巧(likelihood ratio trick)

- 含义: likelihood ratio trick 在直接微分 probability distribution 很别扭时，把它改写成 log-probability gradient 的形式，使期望值内部的计算更容易处理。
- 为什么重要: 它解释为什么在 REINFORCE 和 policy-gradient 公式里会反复出现 `log pi(a|s)` 这样的形式。
- 相关概念: `log-probability`, `policy gradient theorem`, `REINFORCE`
- 核心 Section: `P4-19.6`
- 出现 Section:


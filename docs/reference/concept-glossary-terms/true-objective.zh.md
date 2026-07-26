<a id="true-objective"></a>

## 真实目标(true objective)

- 含义: true objective 是 reward、metric 或 proxy 想要代替表达的真实目标。在强化学习应用里，它可能是 clicks、speed 这类容易数字化指标背后的长期满意、安全或稳定性。
- 为什么重要: 如果 reward 数字和 true objective 不同，系统可能提高容易测量的数字，却伤害真正目标。这个概念是检查 reward design 和 reward hacking 的基准。
- 相关概念: `reward design`, `proxy target`, `reward hacking`, `objective function`
- 核心 Section: `P4-19.3`
- 出现 Section:

<a id="candidate-distribution"></a>

## 候选分布

- 含义：候选分布是在当前上下文或条件下，可能作为下一步出现的多个候选及其相对自然程度。有些候选更强，有些候选更弱，并不是所有候选都以同样可能性摆在一起。
- 为什么重要：LLM 生成不是一次性取出完整句子，而是在当前上下文中制造候选分布，选择一个实际片段，再在更新后的上下文中制造新的候选分布。这个概念能帮助读者把 sampling、temperature、next-token prediction 看成阅读生成流程的工具，而不是孤立的设置项。
- 相关概念：`采样`，`next-token prediction`，`上下文`，`temperature`
- 中心 Section：`P6-1.3`
- 出现 Section：`P6-4.1`

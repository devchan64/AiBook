# P2-6.1 最优化到底在寻找什么

> Section ID: `P2-6.1`
> Version: `v2026.07.09`

在总结数据和用样本估计之后，问题又变了：当有多个候选值时，我们怎样找到更好的那个？

## 本节范围

本节把最优化介绍成“在目标与约束下比较候选”的问题，不深入展开具体凸优化算法。

## 中心问题

为什么最优化不是单纯计算，而是带有结构的候选搜索？

## 先固定的术语

| 术语 | 很短的意思 | 本节中的作用 |
| --- | --- | --- |
| optimization | 寻找更好值的问题 | 本章入口 |
| candidate | 尚未固定的可能选择 | 被比较的对象 |
| criterion | 判断好坏的标准 | 评价规则 |
| constraint | 必须遵守的条件 | 现实边界 |
| minimization / maximization | 减小或增大的方向 | 基本目标 |

![在目标与约束下比较候选的最优化流程](../../../assets/part-02/chapter-06/optimization-search-loop-en.svg)

## 记住的视角

- 最优化是候选之间的搜索问题。
- “最好”必须放在明确目标和明确约束下才有意义。
- 模型学习也可以读成“寻找更好的参数”。

## 简短检查

- 能把最优化解释成候选之间的搜索。
- 能区分 candidate、objective、constraint。
- 能说明为什么 optimal 不等于“在所有意义上都完美”。

## 来源与参考资料

- Google for Developers, [ML Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.

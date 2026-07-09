# Part 2 总结：基础恢复

> Section ID: `P2-summary`
> Version: `v2026.07.09`

Part 2 是在重新进入机器学习与深度学习之前，恢复阅读语言的一段。目标不是把每个证明做完、把每条语法都背熟，而是把公式、代码、数组、表、图、运行环境与变更记录重新连成一条学习流程。

## 先抓住的基准

| 现在应该能直接说出的事 | 为什么在 Part 3 前重要 |
| --- | --- |
| 在小表里区分 feature 与 label | 为了读懂监督学习的输入与目标 |
| 解释 row、column、`shape`、`axis` | 为了把 `X`、`y`、sample、feature 读成数组结构 |
| 区分 mean、error、loss | 为了不把统计摘要与训练标准混在一起 |
| 解释执行环境与变更原因 | 为了让实验与说明保持可复现 |

## Part 3 快速回返表

| 在 Part 3 卡住的地方 | 先回到 Part 2 的哪里 |
| --- | --- |
| `X`、`y`、feature、label 变得模糊 | `P2-12.3`, `P2-15.2` |
| `shape`、`axis`、row、column 混在一起 | `P2-11.2`, `P2-15.2` |
| mean、error、loss 开始混用 | Chapter 5, Chapter 6, `P2-15.2` |
| 执行位置又混起来了 | `P2-3.5`, Chapter 7, Chapter 10 |
| 图表或记录看起来像额外内容 | Chapter 13, Chapter 14 |

## 记住的视角

- Part 2 不是“永远彻底学完基础”的考试，而是一张回返地图。
- 数学在这里被当成计算语言来读。
- Python、NumPy、Pandas、Matplotlib、Git 被当成互相连接的阅读工具。
- 回到代表 Section 复习，是这条学习路线的一部分，不是失败。

## 最后简短检查

- 能用一个小场景解释 feature、label、`X`、`y`、`shape`。
- 能说明为什么学习结果既需要数值读取，也需要变更记录。
- 能说明当 Part 3 术语变得陌生时，自己会先回到哪里。

## 来源与参考资料

- scikit-learn, [Getting Started](https://scikit-learn.org/stable/getting_started.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.

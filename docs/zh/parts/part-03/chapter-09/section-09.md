# P3-9.9 实际目标与代理 target 应该如何区分

> Section ID: `P3-9.9`
> Version: `v2026.07.10`

在现实数据里，真正想预测的结果往往无法被直接看见。所以就会很想拿一个运营中间判断，或者一个替代列，先当成临时 target 来用。这里需要区分的是`实际目标（actual target）`和`代理 target（proxy target）`。必须先写清楚：当前使用的 target，到底就是你真正想知道的结果，还是用来替代它的一列。

| target 类型 | 含义 |
| --- | --- |
| 实际目标 | 你真正想知道、最终也真正想减少的结果 |
| 代理 target | 因为实际目标看不到，或出现得太晚，所以临时拿来替代的一列 |

例如，如果无法直接看到`故障最终确认`，那就可能先把`需要复核`拿来做 target 候选。但两者不是同一个意思。代理 target 可以成为起点，但它不会自动等同于实际目标。

| 先写下的备注 | 为什么需要 |
| --- | --- |
| 真正想知道的结果是什么？ | 为了不把问题原本的目的藏起来 |
| 当前这一列为什么是代理 target？ | 为了留下它与实际目标之间的距离和限制 |
| 之后要怎样重新连回实际目标？ | 为了把代理 target 的局限以及与实际目标的距离保留下来 |

因此，proxy target 不是一个为了方便而起的临时名字，而是一种明确声明：当前测量的是一个不同于原始目标的替代对象。这里的核心，是把`真正想知道的结果`、`现在能观测到的代理列`、以及`两者之间距离的记录`一起留下来，让代理目标的限制被保存在结构里。

## 来源与参考资料

- Google, *Machine Learning Glossary*, `label`, `proxy labels`, 确认日 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }


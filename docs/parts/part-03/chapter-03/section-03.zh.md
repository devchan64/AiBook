# P3-3.3 要把问题搬到第一张表草案里，应该先草拟哪些列

> Section ID: `P3-3.3`
> Version: `v2026.07.25`

拿到问题之后，真正立刻需要的，不是一次把完成表写出来，而是先在第一张表草案里分清：哪些[列(column)](/AiBook/zh/reference/concept-glossary-pinyin/c/#glossary-column)负责识别[样本(sample)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-sample)，哪些列负责状态、比较和结果。问题句一变，表草案的列结构也会跟着变，所以如果要把已存记录搬到[问题表示结构](/AiBook/zh/reference/concept-glossary-pinyin/w/#glossary-problem-representation-structure)里，这第一张草图就必须清楚。第一张表草案真正重要的，不是完整列名清单，而是这种角色划分。

画第一张表草案时，最好不要一开始就试图把所有列都写出来，而是先写下下面四组。

1. 用来识别样本的列
2. 描述样本的候选[特征(feature)](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)列
3. 为比较而需要的[基准线(baseline)](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-baseline)列或差值列
4. 人要读、或以后可能要拿来预测的结果列

把这四组压成表，就是下面这样。

| 列分组 | 为什么要先写它 |
| --- | --- |
| 样本识别列 | 因为表里必须先显露什么算一条案例 |
| 候选特征列 | 因为需要有值来描述样本状态 |
| 比较列 | 因为只有有了差值结构，和平常状态的变化才看得见 |
| 结果列 | 因为必须先看出方向是复核候选，还是目标标签候选(target candidate) |

也就是说，第一张表草案并不是 `把所有原始列都抄过来`，而是 `先摆好这个问题所需要的按角色分组的列`。

## 从问题到表草案的最小变换

例如，如果问题是 `最近一次动作是不是比平时更摇晃？`，那么表草案马上就可以这样画出来。

| 列角色 | 草案示例 |
| --- | --- |
| 样本识别列 | `event_id` |
| 候选特征列 | `flow_mean`, `flow_std`, `late_drop_rate` |
| 比较列 | `baseline_diff`, `repeatability_score` |
| 结果列 | `review_needed` 或 `report_sentence` |

问题一变，草案也会跟着变。

| 问题句 | 草案里最先变化的地方 |
| --- | --- |
| 最近一次动作是不是比平时更摇晃？ | 样本会被固定成 `一次动作` |
| 最近 20 次和此前 200 次相比是不是变了？ | 会先把 `区段聚合` 和比较列推到前面，而不是先盯着样本 |
| 人应该先看哪一次动作？ | 结果列会转向 `priority_score`、`review_needed` |
| 能不能做出以后要预测的结果候选？ | 结果列会更明确地变成 `target` 候选 |

换句话说，问题并不会停留在一句话上，而会立刻推动表的列结构。

## 一开始不需要完美的列名

这里最常停住的原因，是会冒出一个想法：`准确列名我还不知道，那怎么画表？` 但在 Part 3 这个阶段，列名不需要一开始就完全定死。先把角色写下来就可以。

例如，下面这样写就已经足够了。

- 1 个样本识别列
- 1 到 2 个表示水平的特征
- 1 到 2 个表示变化或摇晃的特征
- 1 个相对基准线的差值列
- 1 个给人工复核看的结果列

哪怕只写到这个程度，也已经能勾勒出这个问题到底要求什么样的表结构。

## 用一个小图来看

问题情境：确认问题一变，第一张表草案里的列分组也会跟着改变。

输入(input)：三个不同的问题

期望输出(output)：针对每个问题，`识别`、`特征`、`比较`、`结果` 这几类草案列会被画成不同样子

要确认的概念：第一张表草案不是一份完成的列名清单，而是先把问题要求的按角色分组的列显露出来的阶段

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-3-mermaid-01-zh.mmd"
```

这个例子的关键，不在于列名清单本身，而在于看到 `问题一变，最先变化的是哪一组列`。在比较一次动作时，先显露出来的是 `event_id` 和 `review_needed`；在比较最近 20 次时，更自然的是 `window_id` 和 `report_sentence`；反过来，一旦开始考虑以后的学习候选，结果列就会变成 `target_candidate`。所以，第一张表草案并不是一次把正确表完整做出来的过程，而是一张先把问题要求的样本单位和结果方向显露出来的草图。

只要先把问题搬成按角色分组的列，后面再去读样本单位和摘要表时，也能在 `什么算一条案例`、`哪些值在承担比较与结果角色` 已经可见的状态下继续往下读。也就是说，这一节的核心，是把问题句直接改写成表结构的角色单位，让第一张表草案不再只是抽象备忘，而成为实际工作表的设计起点。如果把这一节重新读成如何用角色单位书写 `first-table specification` 的问题，就会更清楚：第一张表草案不是一份完成的列字典，而是先把问题要求的按角色分组的列写出来的阶段。

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。因为一个 example 预设了 feature 和 label 结构，所以它为这点提供依据：即使在第一张表草案里，也应该先把识别、说明和结果的角色分开。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary` 中的 `label leakage`。它说明 feature 会变成 label proxy 的设计缺陷，因此强化了这一点：结果列和说明列的角色，应该从草案阶段起就先分开。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 它说明基准时段是拿来和其他时段比较的 reference，因此为“草案里应单独放 baseline diff 这类比较角色列”提供了一般依据。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

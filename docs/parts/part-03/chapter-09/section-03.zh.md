# P3-9.3 比较报告、复核候选队列和目标标签候选表有什么不同

> Section ID: `P3-9.3`
> Version: `v2026.07.20`

同一个事件列表，也会因为目的不同而变成[比较报告（comparison report）](/AiBook/en/reference/concept-glossary/#glossary-comparison-report)、[复核候选队列（review queue）](/AiBook/en/reference/concept-glossary/#glossary-review-queue)、或者[目标标签候选（target candidate）](/AiBook/en/reference/concept-glossary/#glossary-target-candidate)表。有的表把比较句子和差值放在前面，有的表把复核优先级放在前面，还有的表把输入列和结果候选列的区分放在前面。这里的目标标签候选，即使还没有凝固成确认答案，也应该被读成：在把输入列和结果列分开的问题结构里，先被立起来的一列结果候选。

核心差别不在于`计算了什么`，而在于`同一个事件列表，会按照什么问题被重新组织`。

| 产物 | 当前最直接的目的 | 表里最先看到的内容 |
| --- | --- | --- |
| 比较报告 | 立刻展示什么与平时不同 | 差值、比较句子、相对基线的变化 |
| 复核候选队列 | 按顺序挑出人应当先看的对象 | 优先级、是否需要复核、重复性 |
| 目标标签候选表 | 在问题结构里整理要作为结果列的候选 | 特征列、目标候选、暂时保留的列 |

即使面对同一批事件，只要问题变了，表的中心列也会改变。如果问的是`相对平时，哪里变了、变了多少`，那比较报告是自然的；如果问的是`现在人应该先看什么`，那复核候选队列是自然的；如果问的是`什么可以作为结果列`，那就需要目标标签候选表。

假设现在已经有一张单个事件摘要表，里面同时有相对基线的差异、重复性和判断备注。那么同一份数据，也可以像下面这样被读成三张不同的表。

## 1. 比较报告是读变化的表

在比较报告里，最先出来的必须是`哪里变了`。因为此时的目的还不是自动判定，而是先把变化的形状展示出来。

| event_id | baseline_mean | current_mean | diff | repeatability | report_sentence |
| --- | --- | --- | --- | --- | --- |
| A | 2.6 | 2.2 | -0.4 | high | 后段区间均值明显低于基线 |
| B | 2.5 | 2.4 | -0.1 | low | 与基线没有明显差异 |
| C | 2.7 | 2.1 | -0.6 | high | 均值下降与波动性增加同时出现 |

这张表的中心是`差异说明`。人在这里可以立刻读出，哪些地方与平时不同。但仅凭这张表，`先看什么`可能还不会自动确定下来，而像`正常/异常`这类目标标签也还未必明确。

## 2. 复核候选队列是优先级表

一旦变成复核候选队列，表的中心就变了。现在重要的不只是有没有变化，而是`它值不值得由人先看`。

| event_id | diff | repeatability | review_needed | priority_score | queue_rank |
| --- | --- | --- | --- | --- | --- |
| C | -0.6 | high | 1 | 0.92 | 1 |
| A | -0.4 | high | 1 | 0.81 | 2 |
| B | -0.1 | low | 0 | 0.18 | 3 |

在这张表里，`priority_score`、`queue_rank`、`review_needed` 会排在 `report_sentence` 前面。也就是说，如果比较报告是在说`看到了什么变化`，那复核候选队列就是在说`这些变化里，人该先看哪一个`。

重要的是，复核候选队列并不会自动变成目标标签表。`review_needed` 可以用于后续判断，但它本身不一定立刻就能变成稳定的原因标签或最终状态标签。

## 3. 目标标签候选表是结果列整理表

当表变成目标标签候选表时，中心又会再次改变。此时最重要的不再是`展示什么`，而是`把什么作为输入，什么作为结果`。

| event_id | feature_1_mean | feature_2_delta | feature_3_variability | review_needed | status_label |
| --- | --- | --- | --- | --- | --- |
| A | 2.2 | -0.4 | 0.21 | 1 | 无 |
| B | 2.4 | -0.1 | 0.08 | 0 | 无 |
| C | 2.1 | -0.6 | 0.27 | 1 | 无 |

在这里，`feature_1_mean`、`feature_2_delta`、`feature_3_variability` 这些特征列，会和 `review_needed` 这样的目标候选一起出现。它既不是像比较报告那样为了立刻读句子，也不是像复核队列那样为了给优先级排序。它更像是一张把输入列和结果列分开的表，用来整理问题结构。

但即使在这个例子里，`status_label` 依然是空的。因此，并不是说只要有了这种表，所有预测问题就都能立刻开始。像 `review_needed` 这样的判断列候选，可能是一些预测问题的起点，但还不足以立刻跳到更细的状态分类。

## 同一份数据分成三张表的最小步骤

如果按下面这个顺序来读，上面的差别会更简单。

1. 先比较基线和当前区间，生成比较报告。
2. 在这个差异上加上重复性和判断标准，生成复核候选队列。
3. 再把其中可以作为结果候选的列单独收集出来，生成目标标签候选表。

这个顺序重要，是因为三张表不是彼此替代的。没有比较报告就直接做复核候选队列，那么为什么某个案例会被提上来，解释就会变弱。没有复核候选队列，只做目标标签候选表，那么这个问题当前为什么重要，也可能会消失。反过来，如果只有复核队列，没有目标标签候选表，那么输入列和结果列该从哪里切开，也会很难整理。

下面这张图展示了同一个事件列表如何分叉成三种产物。

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-3-mermaid-01-zh.mmd"
```

这张图里首先要看的，不是`一张表被复制了三次`，而是`一个事件列表，会为了三个问题被重新切开`。比较报告留下的是变化说明，复核候选队列留下的是复核优先级，目标标签候选表留下的是输入列与结果列的分界。所以，这三张表不该被读成同一份数据的重复拷贝，而应被读成：同一份事件列表，针对不同目的被重新组织后的结果。

如果只把代表列的作用再压缩着看一次，可以读成下面这样。

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-3-mermaid-02-zh.mmd"
```

这第二张图，只是把第一张图分叉之后`每种产物里什么会先被看见`再次压缩出来。比较报告更先看到差值和比较句子，复核候选队列更先看到是否需要复核和优先级分数，目标标签候选表更先看到特征列与结果候选列的分界。所以，第一张图更适合读成`会分成什么`，第二张图更适合读成`分开之后什么会被放在前面`。

## 什么时候该停在什么产物上

最后，如果像下面这样判断，混乱会更少。

| 当前最需要的是什么 | 先做的产物 | 还暂缓的东西 |
| --- | --- | --- |
| 读取变化本身 | 比较报告 | 复核优先级、目标标签表 |
| 决定人应该先看什么 | 复核候选队列 | 稳定的预测标签 |
| 整理学习输入和结果 | 目标标签候选表 | 取代比较报告里的解释 |

关键在于，这三种产物并不是`把同一份数据浪费性地做三遍`，而是在回答三个不同问题。比较报告负责变化解释，复核候选队列负责复核优先级，目标标签候选表负责输入列和结果列的区分。

## 来源与参考资料

- U.S. Bureau of Labor Statistics (BLS), *BLS Handbook of Methods: Glossary*, base period。用于确认基准时期或时间点可以作为比较参照这一用法。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- National Cancer Institute (NCI), *NCI Dictionary of Cancer Terms: baseline*, baseline。用于确认初始测量值可以作为后续变化的比较基准这一说明。 [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Google, *Machine Learning Glossary*, `label`, `labeled example`。用于确认在监督学习里，标签和已标注样本如何把输入特征与结果列分开。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, entity/activity provenance overview。用于确认 provenance 视角：同一事件列表生成不同产物时，应保留各自产生语境与处理步骤。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20

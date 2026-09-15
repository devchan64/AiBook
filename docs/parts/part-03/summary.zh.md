# Part 3 总结

> Section ID: `P3-summary`
> Version: `v2026.09.15`

本 Part 将[数据建模](/AiBook/zh/reference/concept-glossary-pinyin/d/#data-modeling)理解为问题表示结构的设计，而不只是存储结构的说明。关键是：[源数据](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-source-data)也是[数据集](/AiBook/zh/reference/concept-glossary-pinyin/d/#glossary-dataset)，但要把它用作特定分析的输入，就需要确认样本和列的含义。Part 2 与 Part 3 共同构成基础恢复阶段，其中 Part 3 负责`重建数据科学问题结构`。先明确数据建模的目标和范围，把存储记录重新看作候选数据集，确定样本与表结构，设计[特征](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)和[基准线](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-baseline)，再划定解释边界，后面的机器学习说明才能建立在明确基础上。

最后要把四个问题放在一起确认：`什么算一条样本`、`保留了哪些特征和基准线`、`哪些内容仍是比较报告`、`哪些被设为候选学习问题`。明确这四个问题，Part 4 的学习与评估说明才能建立在已定义的数据结构上。

代表案例是这样一种结构：有一次自动执行的动作，这个动作里留下了控制参数时间序列和传感器时间序列，之后又把多次动作重新聚成近期区段，与基准线做比较。Part 3 解释的，就是如何把这个结构改写成人能读、模型也能接得住的表结构。

Part 3 的流程，比起按 Chapter 编号记住，更重要的是按下面三个模块来记。

| 流程模块 | 这一 Part 回收的问题 | 留下的结果 |
| --- | --- | --- |
| 固定职责与顺序 | 数据建模负责什么，又按什么顺序判断？ | 问题结构设计的位置、工作顺序地图 |
| 重建比较结构 | 存储好的记录应重新读成什么样本、表、特征和基准线结构？ | 数据集候选、摘要表、特征、基准线比较表 |
| 整理解释与问题 | 可以说到哪里，什么还应该保留为[比较报告(comparison report)](/AiBook/zh/reference/concept-glossary-pinyin/s/#output-structure)？ | 保守表述、运营输出、输入/结果边界、时间边界 |

只要这三行还在，Part 3 就仍然可以被重新读成 `把问题改写成可表达结构的一连串判断`。

## 这一 Part 的核心流程

- 区分存储结构和问题表达结构。
- 重新构造带有样本、特征和基准线的可比较表。
- 先建立解释边界，再区分比较报告和预测问题。
- 整理输入/结果边界与时间边界，为后面的学习说明建立干净的起点。

## 必须留下来的核心概念

- 样本单位
- 存储结构与问题表达结构的差异
- 摘要表与特征(feature)
- 基准线与比较结构
- 比较报告与预测问题的差异
- 目标标签候选与产出物之间的追踪规则
- 防泄漏与运行时再现性
- 表向量输入与时间序列输入表达之间的分叉

Part 3 结束后留下来的，不应该只是 `某张表`。而应该是一种已经固定了样本单位、区分了输入特征和之后想预测的结果候选、并且也整理出了哪些范围暂时还应该保留为比较报告的结构。压成一句话，就是 `源数据 -> 可比较的表 -> 保守解释 -> 问题结构整理` 这一条链条必须留下来。所以在 Part 3 结束时，至少要确认三条前提。

- 特征和结果候选有没有混在一起？
- 学习时构造特征的规则，能不能在运行时用同样规则再现？
- 时间轴有没有确认，也就是到底看到了多少信息、又在预测什么时候的结果？

只要这些前提确认了，后面的学习说明就能自然地接到 `在已经整理好的问题结构上，到底在学什么` 这个问题上。换句话说，Part 3 的职责不是提前把下一 Part 讲完，而是先把当前数据和问题整理成一个不会轻易晃动的结构。

## 用一页设计备忘录收尾

围绕`从近期动作中选出优先复核的 10 次`这个问题，写出下面的备忘录。

1. 写明动作标识与开始、结束标准，决定如何标记记录缺失的动作。
2. 写出两个保留特征的计算方法和单位，确定基准线的期间及运行条件。
3. 画出包含候选排名和依据的一行输出。把分数与实际复核结果放在不同列中。
4. 如果问题改为`预测未来 7 天内是否发生故障`，写出还需要的预测时点、结果观察期间和已确认标签。

第一个问题可以依据比较规则构造复核队列，而不需要已确认的故障标签。第二个问题则需要能够确认实际结果的期间和标签。如果能解释这个差别，并且没有把观察未完成的记录填成 0，就说明已经区分了比较输出与预测问题的边界。

## 来源与参考资料

- National Academies of Sciences, Engineering, and Medicine, *Data Science for Undergraduates: Opportunities and Options*, 2018. 它把数据收集、清洗、表达、建模和解释视为一条连贯流程，因此支持本页把 Part 3 的结尾绑成 `数据科学问题结构恢复` 这一总结。 [https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options](https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- Google for Developers, `Machine Learning Glossary`. 它提供 feature、label、label leakage、example 等术语区分，因此支持 Part 3 的最小前提：不能把特征与结果候选混在一起，也必须确认输入/结果边界。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- W3C, `PROV-Overview`. 它同时处理 derivation 和 reproducibility，因此支持本页的总结判断：Part 3 结尾留下的比较结构和特征定义，之后也必须能用同样规则被重新构造出来。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08

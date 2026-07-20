# Part 3. 数据建模

> Section ID: `P3-index`
> Version: `v2026.07.20`

在 Part 2 里，我们重新恢复了阅读数学、Python、数组、表格和图形的基础。但能够重新读懂计算工具，并不等于立刻就能把 AI 问题建好。真正面对源数据时，首先撞上的问题，往往不是 `该用什么模型`，而是 `什么才算一条数据样本`。在这本书的整体结构里，Part 2 和 Part 3 一起构成基础能力恢复区段，而 Part 3 负责的是 `数据科学问题结构的恢复`。

Part 3 的代表案例不是围绕某个具体设备名，而是围绕一个更一般的结构来说明。这里有一次自动执行的动作，这次动作会留下动作中使用的控制参数时间序列，以及动作过程中观测到的传感器时间序列。之后又会把多次动作重新聚成近期区段，与基准线做比较。在这种结构里，一个时刻的一次测量可以被看成一个样本，一次完整动作也可以被看成一个样本，甚至多个动作组成的近期区段也可以被看成一个样本。怎么选，会直接改变后面形成的数据集、比较方式、还能解释的问题，以及实际行动流程会分成几条支路。即使是同一份源数据，只要重组方式、保留内容、比较对象和要接入的行动流程结构不同，AI 问题就会完全不同。

这个代表案例在 Part 内如何演化，可以先用下面这张基准表抓住。

| 阶段 | 一行表示什么 | 这一阶段主要保留什么 |
| --- | --- | --- |
| 原始日志 | 动作过程中的一条记录 | 传感器值、控制值、时间顺序 |
| 动作摘要表 | 一次动作 | 平均值、斜率、波动性、区段差异 |
| 近期/基准线比较表 | 由多次动作构成的状态比较 | 近期均值、基准线均值、差值 |
| 运营输出 | 供人阅读或交给下一阶段的结果 | 警告、复核候选、目标标签候选 |

这里说的数据建模，并不只是整理存储结构。数据建模更接近把现实中的源数据重新表达成样本、特征、基准线和输出结构，让人可以比较、AI 可以使用。更准确地说，它不是单纯地 `读给定的表`，而更像是在设计 `什么算一条样本`、`原始日志该如何重组为摘要表`、`哪些特征和比较结构要保留`、`应该保守到什么程度`，以及 `哪些结果暂时只保留为比较报告，哪些才提升成预测问题`。

Part 3 把在数据科学课程里常常分开讲的 data wrangling、feature engineering、sample design、inference、problem framing，重新绑成一个再学习流程。这里不会把它们列成独立的命名步骤，而是沿着同一个案例，依次确认 `什么会变成样本`、`什么会被重组进表`、`什么会被比较`、`我们能说到什么程度`。因此，Part 3 的重点是先建立 `问题表达结构`，而不是算法。

下面这张表还能更短地说明，Part 3 的 spine 不是随意拼出来的顺序，而是把数据科学和机器学习里常见的标准概念包，用 `问题结构恢复` 的视角重新排列。

| 这一 Part 的模块 | 对应的标准概念 | 代表性依据轴 |
| --- | --- | --- |
| 重新组织源数据的区段 | data wrangling, sample design | W3C PROV, Fayyad/KDD |
| 建立特征与基准线的区段 | feature engineering, labeled example, base period | Google ML Glossary, BLS |
| 收束解释强度与输出边界的区段 | problem framing, conservative interpretation, output structure | Google ML Glossary, NASEM |

在 Part 3 里，`数据建模` 这个大定义本身先在 3.1 固定，工作顺序先在 3.2 固定。后面的 Section 不再重复同一个词的长定义，而只保留当前问题需要的最小连接。[样本(sample)](/AiBook/en/reference/concept-glossary/#glossary-sample)、[特征(feature)](/AiBook/en/reference/concept-glossary/#glossary-feature)、[基准线(baseline)](/AiBook/en/reference/concept-glossary/#glossary-baseline)、[比较报告(comparison report)](/AiBook/en/reference/concept-glossary/#glossary-comparison-report)、[目标(target)](/AiBook/en/reference/concept-glossary/#glossary-target) 需要时可以回到概念词汇表再确认。

Part 3 会先固定数据建模想要达成什么，以及它按什么顺序推进。接着再确认，为什么存储好的记录不能直接读成数据集，为什么要先决定一行和一样本分别代表什么，再把原始日志重组为可比较的表。然后才会设计特征和中间表示，区分哪些列用于标识、比较还是目标候选。接下来再建立近期区段与基准线的比较结构，并在小样本和重复性不稳定面前，给解释划出边界。最后才把应当保留为比较报告的问题，与应当提升为预测问题的问题分开，并把输入/结果边界和时间边界一起收口。

## 数据建模承担的作用

- 防止把数据建模误解成只有数据库设计。
- 熟悉把源数据重新表达成样本、摘要表、特征和基准线的流程。
- 理解数据整理、特征工程、保守解释和问题设定其实是一条连续流程。
- 学会在不混淆比较报告与预测问题的前提下，先收束应该先闭合的问题结构。

## 为什么需要这一 Part

- 因为必须先学会：原始日志并不直接等于数据集。
- 因为如果样本单位和比较基准没有固定，feature 和 label 的解释就会摇晃。
- 因为警告候选和诊断确认、基准线比较和绝对值判断，经常会被混在一起。
- 因为即使平均值一样，区段模式和波动性也可能不同，而人很容易只凭一个代表值就下得太快。
- 因为如果样本结构和输入边界是模糊的，后面的学习解释也容易只剩名字，没有问题结构。

## 主要问题

- 数据建模在整个数据科学流程里承担什么角色？
- 为什么存储好的记录不能直接算作数据集？
- 一行和一样本有什么不同，需要怎样的表结构？
- 特征和中间表示是为了保留什么而设计的？
- 为什么基准线和比较结构必须先于模型被固定？
- 在样本量和重复性面前，解释可以推进到什么程度？
- 什么应该保留为比较报告，什么应该交给学习问题？

## 建立问题结构的流程

Part 3 虽然沿着 9 个 Chapter 前进，但整体流程可以概括成三个模块。

1. 固定数据建模的职责与顺序。
2. 把存储结构重新建成带有样本、表结构、特征和基准线的比较结构。
3. 先建立解释边界，再区分比较报告和预测问题，并收口输入/结果边界。

之所以坚持这个顺序，是因为如果在把存储结构改写成问题结构之前就先谈 feature 和 label，这些词会漂在半空；而如果在解释边界建立之前就先提预测问题，模型名字就会比数据结构先出现。下面这张表更短地说明了，这三个模块分别在固定什么。

| 流程模块 | 这里抓住的问题 | 留下的结构 |
| --- | --- | --- |
| 固定职责与顺序 | 数据建模负责什么，又按什么顺序判断？ | 问题结构设计的位置、工作顺序地图 |
| 重建比较结构 | 存储好的记录应重新读成什么样本、表、特征和基准线结构？ | 数据集候选、摘要表、特征列、基准线比较表 |
| 收口解释与问题 | 可以说到哪里，什么还应该留在报告里？ | 保守表述、运营输出、输入/结果边界、时间边界 |

Part 3 反复处理的问题，也可以这样再聚一下：什么算一个样本，原始日志该重组为什么表，哪些特征和基准线要保留，什么应该继续当比较报告，什么应该提升成目标候选，以及输入结构和观测边界是否已经闭合。每个 Chapter 都是在把这些问题包中的某一组变得更清楚。

## 数据建模要闭合的边界与留下的问题

Part 3 处理的是样本单位、原始日志与摘要表、特征与中间表示、基准线比较、样本量与重复性，以及警告候选与标签预测之间的边界。

相对地，具体机器学习算法的学习方式、train/validation/test 切分的细致流程，以及复杂时间序列深度学习结构本身，都不是这里的中心。

这个范围限制的原因很简单。Part 3 的责任，是先把 `什么数据应该被做成什么结构` 说清楚。

## 读完 Part 3 之后应该留下的理解

应该留下这样的感觉：数据集不是一张现成表，而是一个被设计出来的比较结构；机器学习也只有放在这种结构之上，才会被真正读懂。样本结构、特征、目标候选和时间边界必须先被整理好，这样后面的学习解释才能一直保持 `到底在预测什么`、`又在用什么输入` 的清晰状态。

## 来源与参考资料

- National Academies of Sciences, Engineering, and Medicine, *Data Science for Undergraduates: Opportunities and Options*, 2018. 它把数据收集、清洗、表达、建模和解释视为一条完整数据科学流程，因此支持本页把 Part 3 放在 `问题结构恢复` 位置上的课程视角。 [https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options](https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary`. 它提供 sample、feature、label、label leakage 等核心术语的角色区分，因此支持 Part 3 必须先固定样本结构和输入/结果边界，而不是先讨论模型名字。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. 它把 provenance 和 derivation 一起处理，因此支持 Part 3 的共同前提：当源数据被重做成问题表达结构时，派生表是按什么规则生成的也必须可追踪。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Usama Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, `Knowledge Discovery and Data Mining: Towards a Unifying Framework`, Microsoft Research publication page, 1996. 这一 KDD 经典参考支持把源数据重组视为数据准备与发现流程中的独立轴。 [https://www.microsoft.com/en-us/research/publication/knowledge-discovery-and-data-mining-towards-a-unifying-framework/](https://www.microsoft.com/en-us/research/publication/knowledge-discovery-and-data-mining-towards-a-unifying-framework/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- U.S. Bureau of Labor Statistics, `Consumer Price Index: Concepts`, Handbook of Methods. 其中对 CPI index values 和 base periods 的说明，用来参考“先固定基准期间，再比较当前值”的观念。 [https://www.bls.gov/opub/hom/cpi/concepts.htm](https://www.bls.gov/opub/hom/cpi/concepts.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

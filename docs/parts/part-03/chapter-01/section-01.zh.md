# P3-1.1 数据建模想要达成什么

> Section ID: `P3-1.1`
> Version: `v2026.09.15`

一进入 Part 3，读者很快就会遇到 [sample](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-sample)、[feature](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)、[baseline](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-baseline)、[output structure](/AiBook/zh/reference/concept-glossary-pinyin/s/#output-structure)、[target](/AiBook/zh/reference/concept-glossary-pinyin/m/#target) 这些词。它们并不是彼此分开的。真正把 `什么算一条记录`、`哪些值要保留`、`拿什么去比较`、`最终要用什么结果格式收口` 一起决定下来的外层判断，就是 [data modeling](/AiBook/zh/reference/concept-glossary-pinyin/d/#data-modeling)。

如果只把数据建模理解为整理存储结构，就容易认为它只是把已有表格整理得更美观。本书 Part 3 在更宽的意义上使用这个词，指按照问题设计样本和表示。这是本书选定的讨论范围，并不是取代数据库领域数据建模定义的标准定义。这里要决定的是：让现有的[源数据](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-source-data)能够回答哪些问题。

最常见的早期混淆，是把 `数据库该怎么存` 和 `AI 该怎么读这个问题结构` 当成同一件事。它们确实有关，但目标不同。

| 比较点 | 先看存储结构的视角 | Part 3 的数据建模视角 |
| --- | --- | --- |
| 最先问的问题 | 如何无遗漏地存下记录，并且之后还能找回？ | 应该怎样构造样本和比较结构，才能回答一个问题？ |
| 代表单位 | 一条日志、一条事件、一条传感器测量 | 一次动作、一个近期区段、一个实体作为分析样本 |
| 主要关心点 | 是否无遗漏、关联正确、可以追踪 | 能比较什么，还要保留哪些特征 |
| 直接产出 | 原始日志表、事件表、可 join 的存储结构 | 摘要表、特征表、基准线比较表、复核输出结构 |
| 这一 Part 里的问题 | 也许仍然是起点，但不是终点 | Part 3 全程都在处理的中心问题 |

如果说存储结构是 `为了不丢记录的框架`，那么数据建模更接近 `为了回答问题而构造比较结构的框架`。即使面对同一份源数据，只有存储结构也还不够。只有连 `应该把它按什么样本单位、用什么比较基准重新读` 都一起定下来，学习和分析所需的表才真正建立起来。

假设这里有一份自动执行动作的记录。源数据里可能有逐时刻的传感器值、控制参数、动作开始与结束时间。这个结构也许已经足够用于存储和追踪。但仅凭这种状态，还是很难立刻回答 `这次动作和以往相比是否不同`、`近期区段的重复性是否在晃动`、`人应该先看什么` 之类的问题。

这里数据建模真正想达成的目标其实很简单：不是原样接受源数据，而是把它改造成能被人比较、也能被模型使用的结构。通常要做出来的结果可以拆成四层。

1. 决定什么算一条样本。
2. 构造描述这条样本的特征。
3. 建立近期状态要拿来对比的基准线。
4. 决定输出结构，比如结果是给人复核，还是作为预测目标候选。

因此，数据建模更接近 `设计让问题可解的比较结构`，而不只是 `整理表格`。

在这里，也需要一起固定数据建模与[数据科学](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-data-science)的关系。数据科学是一个更大的流程，里面包含数据收集、清洗、探索、汇总、比较、解释、预测，以及和决策的连接。Part 3 聚焦的数据建模，则更接近其中 `把源数据改造成适合 AI 学习和分析的问题结构` 这一前段判断。换句话说，Part 3 不是在教授整个数据科学，而是在处理 AI 学习必须经过的数据科学核心设计区间。

把数据建模实际上要产出的东西并排摆出来，会更清楚。

| 想要达成的结果 | 为什么需要它 | 后面会连到的问题 |
| --- | --- | --- |
| 样本单位 | 因为必须先决定什么算一条记录 | 一行到底表示什么？ |
| 特征表 | 因为必须构造可用于比较和学习的描述值 | 哪些值应该留下？ |
| 基准线比较结构 | 因为近期状态必须放在平常状态旁边读 | 应该拿什么来比较？ |
| 输出结构 | 因为不能把人工复核和预测目标混在一起 | 最终结果该用什么形式输出？ |

这张表里最重要的一点是：数据建模还不是 `模型选择` 阶段。在这一阶段，比起分类器名字或深度学习结构，更早要决定的是要构造什么表、让什么比较成为可能。只有这样，后面机器学习部分里的 `X`、`y`、评估、基准模型才不会悬在半空。

把数据建模的判断顺序再压成一句话，可以这样读：

```mermaid
--8<-- "assets/part-03/chapter-01/p3-1-1-mermaid-01-zh.mmd"
```

如果这样看仍然太抽象，把源数据表和建模后的表放在同一个场景里并排看，会更容易抓住。

假设源数据是这样的逐时刻日志。

| action_id | t_sec | flow_rate | pressure | valve_open |
| --- | ---: | ---: | ---: | ---: |
| A-101 | 0.0 | 24.8 | 101.2 | 1 |
| A-101 | 1.0 | 25.1 | 101.0 | 1 |
| A-101 | 2.0 | 23.9 | 102.4 | 1 |
| A-102 | 0.0 | 24.7 | 100.9 | 1 |
| A-102 | 1.0 | 24.8 | 101.1 | 1 |
| A-102 | 2.0 | 24.8 | 101.0 | 1 |

这张表对于存储和追踪来说已经足够，但要直接比较 `哪一次动作比平常更不稳定`，就很困难。数据建模会把这种日志重新做成动作级摘要表。

| action_id | flow_mean | flow_std | pressure_mean | late_drop_rate | baseline_gap | review_flag |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| A-101 | 24.60 | 0.62 | 101.53 | -1.2 | -1.2 | review |
| A-102 | 24.77 | 0.06 | 101.00 | 0.0 | 0.0 | no_flag |

这张表由用于说明的虚构记录计算得到。假设流量单位为 L/min，压力单位为 kPa。`flow_std` 是三个流量值的样本标准差，分母为 3−1；`late_drop_rate` 是最后两个流量值之差除以 1 秒。A-101 的计算为 `(23.9−25.1)/1 = −1.2 L/min/s`。负值越小，下降越陡。另行假定平时下降率为 0，按 `baseline_gap = late_drop_rate−0` 计算，仅在差值小于 −0.5 时标记 `review`。`no_flag` 只表示没有触发这条规则，并不表示已确认正常。基准线和阈值不是仅由上面六行日志估计出来的。

这两张表之间的差别，正好说明了数据建模的目的。

- 源数据表保留的是逐时刻记录。
- 建模后的表显露的是比较与判断所需的样本单位和特征。
- `review_flag` 这样的输出结构，是为了先筛出人要优先检查的对象。
- `baseline_gap` 这样的比较列，则把近期状态直接连到平常状态上。

把人原来怎么读、以及数据建模改变了什么，再压成一个场景，会更清楚。

| 判断阶段 | 人直接读日志时 | 经过数据建模之后 |
| --- | --- | --- |
| 一条样本怎么数 | 一次看一行时间记录 | 把一次完整动作聚成一样本 |
| 比较怎么做 | 靠眼睛来回扫多行 | 直接通过均值、波动和基准线差值比较 |
| 优先级怎么定 | 人重读后再选 | 先用 `review_flag` 一类列筛选 |
| 下一步行动 | 记录在，但判断会慢 | 可以直接交给复核候选表或预测输入表 |

```mermaid
--8<-- "assets/part-03/chapter-01/p3-1-1-mermaid-02-zh.mmd"
```

数据建模做得好不好，并不是看有没有用上华丽的模型。更关键的是，看下面这些问题能不能回答。

- 现在这张表里的一行到底表示什么？
- 为什么要保留这个值？
- 它应该拿什么来比较？
- 这个结果是自动结论，还是只是给人复核的候选？

如果能回答这四个问题，数据建模就已经完成了很重要的一部分。反过来，如果无法回答，无论源数据有多少，后面的模型说明都容易失去基础。每一列都应能追溯到原始记录或计算规则，其他人才可以重新生成同一张表。

因此，Part 3 首先确定的是`什么算样本`、`保留哪些值`、`拿什么比较`以及`输出成什么结果结构`。数据清洗与探索、统计检验和学习算法，都是在这套设计之上继续理解的后续工作。只有明确这个边界，才能把数据问题理解为`在已设计好的结构上继续求解的问题`。

从更宽的角度看，这一节其实是在一起决定：`什么该算一条对象`、`应该留下什么表达`、`拿什么去比较`、`最后用什么结果格式收口`。

因此，把数据建模理解成 `先设计能够回答问题的表达和比较结构`，比理解成单纯的 `整理表` 要准确得多。

## 检查清单

- 你是否重新计算了 A 的流量标准差和基准线差值，并与表中的值核对？
- 你能否区分数据库存储结构的说明与本例的分析输入设计？

## 来源与参考资料

- W3C, `PROV-Overview`. provenance framework 说明它应当支持 object identification 和 derivation representation，因此它为这种一般判断提供依据：`什么算一条对象`、`摘要表和比较结构是通过什么过程做出来的`，都应该保留可解释性。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary`, `example`, `labeled example`. example 可以没有标签；labeled example 同时包含特征与标签。 用于区分样本、输入与结果的作用。 [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-09-15
- U.S. Bureau of Labor Statistics, `Base period`. 它提供“拿某个时点或区段作为参考”的一般概念，因此支持这种说明：数据建模必须先建立一个基准线，用来比较近期状态。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Usama M. Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, `From Data Mining to Knowledge Discovery in Databases`. 它说明了包含数据收集、选择、预处理、转换与解释在内的更大知识发现流程，因此为这个边界提供背景：Part 3 并不是覆盖全部数据科学，而是聚焦在其中的问题结构设计和表达转换。 [https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

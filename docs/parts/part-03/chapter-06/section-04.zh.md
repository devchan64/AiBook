# P3-6.4 为什么汇总表里的所有列都不一定是特征

> Section ID: `P3-6.4`
> Version: `v2026.09.19`

汇总表可以同时包含比较值、输入候选、结果以及标识和上下文信息。列名或数字格式不能决定是否作为模型输入。**先确定预测什么、何时预测，再检查当时是否真正能获得该值。** 同一列可以既用于比较，又作为输入候选。

## 在动作结束时预测之后七天

在这个虚构案例中，动作结束后立即预测之后七天内是否会出现故障记录。假设当前传感器汇总在结束时已完成，基准值也已提前用更早的动作计算好。如果当前汇总之后才重新计算，就需要重新检查可用性假设。

结果列 `failure_within_7d` 表示结束之后七天以内是否存在故障记录，不包含结束瞬间，包含七天的截止点。有记录为 1；只有追踪完成且没有故障记录才为 0。下面 A、B 是追踪结束后补上结果的训练表，实际预测时尚不知道结果。

| event_id | mid_flow_mean | baseline_mid_flow_mean | delta_from_baseline | failure_within_7d |
| --- | ---: | ---: | ---: | ---: |
| A | 2.40 | 3.05 | −0.65 | 1 |
| B | 2.55 | 2.60 | −0.05 | 0 |

流量单位为 L/min。A 的差值为 `2.40−3.05=−0.65 L/min`，表示比历史基准低 0.65。B 为 `2.55−2.60=−0.05 L/min`。负数本身不是故障判定，仅凭两行也不能确定预测规则或性能。

## 分别标记比较用途与输入候选

下表针对上述预测问题。“候选”表示可以考虑，并不保证采用或有用。比较用途是指在报告中检查数值和条件，与模型训练是不同用途。

| 列或表达 | 用于比较 | 输入候选 | 结束时是否可用 |
| --- | --- | --- | --- |
| mid_flow_mean | 查看当前水平 | 是 | 假设汇总完成时为是 |
| baseline_mid_flow_mean | 查看历史基准 | 是 | 已提前用过去资料算好时为是 |
| delta_from_baseline | 查看相对基准的差值 | 是 | 两个源值当时都可用时为是 |
| event_id | 连接源记录、检查重复 | 本例排除 | 是 |
| 从结束时刻提取的时段 | 按时段比较条件 | 依目标而定 | 时刻立即记录时为是 |
| failure_within_7d | 追踪结束后比较结果 | 从此预测的输入中排除 | 否 |

本例排除 event_id，是因为它只承担标识作用，并非所有问题都永久禁止标识符。设备 ID 等重复对象的信息可能有意义，但是否应用到新设备、模型是否记住 ID，需要另行检查。记录时刻也可以直接使用或提取时段，因此不能说上下文列永远不能成为输入。

## 同名差值也会因基准时点不同而改变

现在假设 A 的基准 3.05 混入了动作结束后一周的测量。即使差值仍为 −0.65，结束时也无法构造这个基准。它可用于事后比较，但若用于结束时的预测输入，就引入了未来信息。

即使基准只使用过去资料，如果计算工作到第二天才完成，结束后立即预测时仍然不可用。**源数据发生时点与计算结果可用时点都要检查。** 训练行也应连接当时可用的基准版本，不能把用全部资料重新计算的平均值统一贴到历史各行。

若把预测时点移到动作开始之前，当前动作的中段均值也尚不存在。表名和数值不变，输入候选列表却会改变。历史基准可能仍可用，当前中段均值及其相对基准差值则不能使用。

## 同时记录列角色与计算来源 {#_5}

```mermaid
--8<-- "assets/part-03/chapter-06/p3-6-4-mermaid-01-zh.mmd"
```

请为 `delta_from_baseline` 标记“用于比较/输入候选/当时可用”。第一种情况的基准仅使用过去资料且立即可用，三项都为是。混入未来资料或计算延迟的情况，只能事后比较，应从指定预测时点的输入中排除。不能因它是比较列就排除，也不能因它是数字就纳入。

之后把结果补入训练表本身没有问题，但必须分开使用输入列和目标列。B 尚未完成追踪时，能因为没有故障记录就标记 0 吗？不能。应另行记录追踪完成状态，未完成结果暂缓确定。

保留源事件 ID、基准包含的时间范围、基准版本与汇总完成时刻，就能复查每个差值的来源。角色是关于用途与时点的记录，不是只能选择一个的互斥标签。

## 检查清单

- 能否带单位计算 A、B 的基准差值？
- 能否解释比较值与输入候选的角色可以重叠？
- 能否同时检查未来资料混入与计算完成时点？
- 能否选出预测移到动作开始前时应排除的列？

相关概念：[汇总表(summary table)](/AiBook/zh/reference/concept-glossary-pinyin/d/#data-modeling), [特征(feature)](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature).

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。它把 labeled example 解释为特征与标签的组合，因此提供了一个基础框架：输入说明列与候选结果列应当被区分开来。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary` 中的 `label leakage`。它解释了“特征变成标签代理”这种设计缺陷，因此为“不应把 `failure_within_7d`、`failure_within_7d` 这样的候选结果列随手混进 feature”提供了依据。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. 它提供了一个关于 provenance information 应该被单独记录和追踪的标准语境，因此也可以作为一般依据：像 `event_id`、`captured_at` 这样的识别/上下文列，应保留为一种和“描述样本本身的 feature”不同角色的信息。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

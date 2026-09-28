# P3-3.3 要把问题搬到第一张表草案里，应该先草拟哪些列

> Section ID: `P3-3.3`
> Version: `v2026.09.19`

第一张草表要选出能回答问题的列，并说明每个值来自哪里。与其背诵列名，不如区分[样本](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-sample)标识、原始观测值、计算得到的[特征](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)、比较基准和结果语句。并不是每个数据集都必须包含这些列；只保留当前问题所需的内容。

## 先确定问题与计算区间

问题是“已完成动作的后段平均流量，是否低于相同运行条件下的历史基准？”下面是本节编制的虚构记录，与前一节 CSV 无关。一个样本是一次动作，本练习把动作内第 8、9、10 秒的观测点定义为“后段”，均值是三个测量值的算术平均。

| event_id | operating_mode | 8秒 flow | 9秒 flow | 10秒 flow |
| --- | --- | ---: | ---: | ---: |
| A | standard | 2.2 | 2.4 | 2.6 |
| B | fast | 2.0 | 2.2 | 2.4 |

所有流量单位为 L/min。假定已提供 `standard` 条件的历史基准 2.8 L/min，它汇总了历史动作中同样第 8、9、10 秒的均值。本练习的基准标识为 `standard_8_10_v1`，没有提供 `fast` 条件的基准。实际使用时，应确认该标识对应的原始资料、选取条件和计算方法。

## 从空白模板填写 A 的一行

请先填写下面的空格。`mean` 表示平均值，`delta` 表示当前值减去基准值的差。

| event_id | operating_mode | late_flow_mean | baseline_id | baseline_late_flow_mean | delta_from_baseline | report_sentence |
| --- | --- | --- | --- | --- | --- | --- |
| A | ___ | ___ | ___ | ___ | ___ | ___ |

各单元格的角色与依据可分为以下几类。

| 角色 | 使用的记录或列 | A 的填写方法 |
| --- | --- | --- |
| 标识 | `event_id`, `operating_mode` | 从原始记录取动作 A 及其运行条件 |
| 观测 | 第 8、9、10 秒的 `flow` | 关联 2.2、2.4、2.6 作为计算依据 |
| 派生特征 | `late_flow_mean` | `(2.2+2.4+2.6)/3 = 2.4` |
| 比较 | `baseline_id`、基准值、`delta_from_baseline` | 找到条件与区间匹配的 2.8，计算 `2.4−2.8 = −0.4` |
| 结果 | `report_sentence` | 只把比较确认的差异写成语句 |

三个观测值与其均值不同。均值 2.4 是原始测量值的计算结果，即使恰好等于第 9 秒的值，也不能把它当作原始测量值。草表可以只保留均值，但必须能找回 A 的 8~10 秒原始记录和计算规则。

| event_id | operating_mode | late_flow_mean | baseline_id | baseline_late_flow_mean | delta_from_baseline | report_sentence |
| --- | --- | ---: | --- | ---: | ---: | --- |
| A | standard | 2.4 | standard_8_10_v1 | 2.8 | -0.4 | 后段均值比相同条件的基准低 0.4 L/min |

均值、基准值与差值的单位都是 L/min。这是流量较低的比较语句，不是故障标签。多个动作的重复性分数或复核优先级并非当前问题所需，因此不加入第一张草表。

## B 没有基准时保留什么

请自己填写 B 的一行。决定应复制 A 的基准 2.8、填 0，还是保留未确认，并说明理由。

B 的均值可以计算：`(2.0+2.2+2.4)/3 = 2.2`。但其运行条件是 `fast`，没有依据直接套用 `standard` 的基准，因此基准与差值都保留为未确认。

| event_id | operating_mode | late_flow_mean | baseline_id | baseline_late_flow_mean | delta_from_baseline | report_sentence |
| --- | --- | ---: | --- | --- | --- | --- |
| B | fast | 2.2 | 未确认 | 未确认 | 未确认 | 需要取得 fast 条件下 8~10 秒的基准 |

`未确认`不是 0。在实际文件中，可以把缺失标记与原因列分开保存。随意把基准填为 0，就会产生没有依据的差值 `2.2−0 = +2.2`。如果后来确认适用基准确实是 2.2，差值才是 **0**，这与“无法计算差值”不同。

## 把问题转成标识、说明与结果列 {#_3}

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-3-mermaid-01-zh.mmd"
```

如果新问题是“哪次动作的后段均值最高？”，不需要基准，比较 A 的 2.4 与 B 的 2.2 就能回答 A。但条件不同，无法据此知道为何更高。这个问题的草表只需标识、条件与均值；“是否低于平时？”则还需要条件匹配的基准。相比增加列数，更重要的是不遗漏问题所需的依据。

## 检查清单

- 是否用 A 的三个观测值计算了均值 2.4 和基准差 −0.4？
- 能否区分原始标识、观测值与派生均值、比较值及报告语句？
- 能否解释为什么不能给 B 套用 A 的基准或随意填 0？
- 能否区分计算得到的差值 0 与无法计算而未确认的状态？
- 问题变成比较均值大小时，能否选出不再需要的列？

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary`：`label`、`labeled example`、`unlabeled example`。用于确认监督学习的输入与结果角色，以及无标签案例的区别。 [原文](https://developers.google.com/machine-learning/glossary#labeled-example){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-09-19
- W3C, `PROV-Overview` (2013)。用于支持追踪数据生成涉及的对象、活动、人员及处理步骤与版本。 [原文](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-09-19

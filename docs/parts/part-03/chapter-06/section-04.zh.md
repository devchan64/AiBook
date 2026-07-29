# P3-6.4 为什么汇总表里的所有列都不一定是特征

> Section ID: `P3-6.4`
> Version: `v2026.07.25`

“[汇总表(summary table)](/AiBook/zh/reference/concept-glossary-pinyin/s/#data-modeling)里有一列”这件事，和“它就是[特征(feature)](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)”这个判断，并不是同一句话。汇总表里当然会有用来描述样本结构的特征，但也可能同时包含用于比较的列、结果候选列，以及用于识别和保留上下文的列。所以，这一节最先要抓住的区分是：`汇总表中的列` 和 `应该被当成模型输入来读取的特征`，并不会自动重合。

## 为什么需要这个区分

当我们做出一张“一次动作汇总表”时，很多不同类型的列，可能会像下面这样一起出现在同一张表里。

| 列名示例 | 它会直接是 feature 吗 | 更自然的角色 |
| --- | --- | --- |
| `mid_flow_mean` | 通常是 | 描述样本结构的特征 |
| `late_minus_early` | 通常是 | 展示变化结构的特征 |
| `baseline_mid_flow_mean` | 视情况而定 | 比较基准列 |
| `review_needed` | 不是 | 结果或目标标签候选 |
| `event_id` | 不是 | 识别列 |
| `captured_at` | 不是 | 时间上下文列 |

这张表之所以重要，是因为它会减缓那种 `只要是数字列，就是 feature` 的习惯。有些列是在描述样本结构，有些列是为了比较才贴上去的，还有一些列则可能记录了我们后面想去预测的结果。

## 为什么同一张表里会混入多种角色

汇总表，是把 `一次动作样本` 改写成一行一行更容易读的形式。但人在读这张表时需要的信息，和直接送给模型作为输入的信息，并不总是完全一样。

例如，我们可以想象下面这样一张表。

| event_id | mid_flow_mean | late_minus_early | baseline_mid_flow_mean | review_needed |
| --- | ---: | ---: | ---: | ---: |
| A | 2.40 | -0.80 | 3.05 | 1 |
| B | 2.55 | -0.10 | 2.60 | 0 |

看这张表时，所有东西都像数字，但角色并不一样。

- `mid_flow_mean`、`late_minus_early` 在描述样本结构。
- `baseline_mid_flow_mean` 是为了拿来和以往状态比较而贴上的基准列。
- `review_needed` 可能是我们后面想预测的结果候选。
- `event_id` 则是指向这条样本的名字。

也就是说，一张表里可能会暂时同时放着 `给人阅读的比较信息`、`后面要送进学习阶段的输入`、以及 `候选结果`。

## 先分成四类，会更不容易混淆

第一次读的时候，不妨先不要想得太复杂，而是先把列分成四类。

| 列类型 | 先问的问题 | 示例 |
| --- | --- | --- |
| 特征列 | 这个值是不是在描述样本结构？ | 平均值、斜率、波动性 |
| 比较列 | 这个值是不是在帮助读取平时和近期之间的差异？ | 基准线平均值、差值 |
| 候选结果列 | 这个值是不是后面想预测的结果？ | `review_needed`、`final_status` |
| 识别/上下文列 | 这个值是不是在区分样本或解释它的时间点？ | `event_id`、`captured_at` |

只要先按这四个盒子分开来看，就会更清楚：即使这些列同处一张工作表，它们依然承担着不同角色。比较列负责让我们读出平时与近期的差异，候选结果列负责把以后要预测的值单独立起来，而识别/上下文列则保证我们不会失去“这个判断是从哪条样本、哪个时点来的”。所以，这里的区分并不是一张单纯的分类表，而是在说明：为什么同一张表里的列，不能都用同一种方式去读。

## 即使同样是数值列，也不一定就是 feature

最容易混淆的，往往是像 `baseline_mid_flow_mean` 或 `delta_from_baseline` 这样的列。因为它是数值，看起来像 feature，但应该先看：它为什么会被加上来。

| 数值列 | 第一眼容易冒出的误解 | 应该先确认什么 |
| --- | --- | --- |
| `baseline_mid_flow_mean` | 它是数字，所以一定是 feature | 它是在存放基准线本身，还是一个真的要送作输入的特征？ |
| `delta_from_baseline` | 它是差值，所以一定是 feature | 它是在解释比较结构，还是之后真的要作为输入？ |
| `review_score` | 它是数字，所以一定是 feature | 它是结果分数，还是输入描述值？ |

所以，比起 `是不是数值列`，更优先的问题是 `为什么会做出这一列。`

## 小型检查表

这一节的例子，比起计算实验，更重视列角色分离。我们可以不按 `值的格式`，而按 `为什么做出这一列`，重新读取工作表中的列。

| 列名 | 示例值 | 先读作什么角色 | 是否直接作为模型输入 | 判断理由 |
| --- | ---: | --- | --- | --- |
| `event_id` | A | context | 否 | 它识别样本。 |
| `mid_flow_mean` | 2.40 | feature | 是 | 它描述样本自身的中段平均值。 |
| `late_minus_early` | -0.80 | feature | 是 | 它描述样本内部从前段到后段的变化结构。 |
| `baseline_mid_flow_mean` | 3.05 | comparison | 视情况而定 | 它保存基准线本身。 |
| `delta_from_baseline` | -0.65 | comparison | 视情况而定 | 它表达相对于基准线的差距。 |
| `review_score` | 87 | target candidate | 否 | 它可能是后面想预测的结果分数。 |
| `review_needed` | 1 | target candidate | 否 | 它是“是否需要复查”这一结果候选。 |
| `captured_at` | 2026-07-08 09:10 | context | 否 | 它记录样本被捕捉的时间。 |

这张表展示的，并不是什么惊人的分类规则。核心在于：同一张工作表里可以暂时并排放着多种角色的列，而我们又必须按角色和理由重新去读这些列。尤其是，`baseline_mid_flow_mean` 和 `delta_from_baseline` 虽然是数值列，但首先应读作比较列；`review_score` 和 `review_needed` 虽然也是数值列，但首先应读作候选结果。这里 `depends` 的原因也会一起显露出来。因为基准线本身或相对基准线的差值，本来就是为了解释比较结构而做出的列，所以它是否应被直接送去当作输入特征，还要根据后面要建立什么预测问题来再次判断。

如果在特征设计之后，先把这个区分碰一遍，`反正不都是 feature 吗？` 这种错觉就会弱很多。汇总表并不是一个只存放 feature 的表，而是一张工作表：feature 候选、比较列、结果候选、识别/上下文列，都可能暂时一起放在里面。这样读过之后，后面再次碰到基准线比较列和 target 候选列时，它们的角色也不会显得那么突兀地“突然变了”。

这一节与其说只是在问 `哪一个数值列算 feature`，不如说更接近于在讨论：[工作表里的列角色应该怎样分离(column-role separation in a working table)](/AiBook/zh/reference/concept-glossary-pinyin/l/#glossary-column-role-separation)。


因此，取代 `只要是数字列就是 feature` 这种误解，更应该先问：每一列是在描述样本、保存比较基准、记录结果，还是只是保留上下文。

## 用一个小图来看

这一节的核心，是不要把工作表里的所有列都读成同一种东西。即使在同一张表里，列也会分成特征列、比较列、结果候选列和上下文列，而这种角色区分必须先建立起来。

--8<-- "assets/part-03/chapter-06/p3-6-4-mermaid-01-zh.mmd"

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。它把 labeled example 解释为特征与标签的组合，因此提供了一个基础框架：输入说明列与候选结果列应当被区分开来。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary` 中的 `label leakage`。它解释了“特征变成标签代理”这种设计缺陷，因此为“不应把 `review_needed`、`review_score` 这样的候选结果列随手混进 feature”提供了依据。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. 它提供了一个关于 provenance information 应该被单独记录和追踪的标准语境，因此也可以作为一般依据：像 `event_id`、`captured_at` 这样的识别/上下文列，应保留为一种和“描述样本本身的 feature”不同角色的信息。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

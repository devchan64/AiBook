# P3-9.9 实际目标与代理 target 应该如何区分

> Section ID: `P3-9.9`
> Version: `v2026.07.31`

如果决定使用代理 target，就要在表中一起留下 `business_goal`、`proxy_target`、`proxy_reason`、`proxy_gap`、`review_owner` 等 备注。这些字段可以防止 target 名称凝固成实际目标，并在以后把问题 类型 提升为预测时，重新分清直接预测的是什么、替代预测的是什么。

在现实数据里，真正想预测的结果往往无法被直接看见。所以就会很想拿一个运营中间判断，或者一个替代列，先当成临时[目标(target)](/AiBook/zh/reference/concept-glossary-pinyin/m/#target)来用。这里需要区分的是[实际目标(actual target)](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-actual-target)和[代理目标(proxy target)](/AiBook/zh/reference/concept-glossary-pinyin/d/#glossary-proxy-target)。必须先写清楚：当前使用的 target，到底就是你真正想知道的结果，还是用来替代它的一列。

| target 类型 | 含义 |
| --- | --- |
| [实际目标(actual target)](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-actual-target) | 你真正想知道、最终也真正想减少的结果 |
| [代理目标(proxy target)](/AiBook/zh/reference/concept-glossary-pinyin/d/#glossary-proxy-target) | 因为实际目标看不到，或出现得太晚，所以临时拿来替代的一列 |

例如，如果无法直接看到`实际状态确认`，那就可能先把`需要复核`拿来做目标标签候选(target candidate)。但两者不是同一个意思。代理目标可以成为起点，但它不会自动等同于实际目标。

| 先写下的备注 | 为什么需要 |
| --- | --- |
| 真正想知道的结果是什么？ | 为了不把问题原本的目的藏起来 |
| 当前这一列为什么是代理 target？ | 为了留下它与实际目标之间的距离和限制 |
| 它与实际目标是以怎样的距离连接的？ | 为了把代理 target 的局限以及它与实际目标之间的距离保留下来 |

## 为什么这个区分会改变问题类型本身

actual target 和 proxy target 的差别，并不只是名称不同。只要你真正要预测的对象变了，当前这个问题应该被放成[比较报告(comparison report)](/AiBook/zh/reference/concept-glossary-pinyin/s/#output-structure)、[复核候选(review candidate)](/AiBook/zh/reference/concept-glossary-pinyin/s/#output-structure)筛选问题，还是要提升成[预测(prediction)](/AiBook/zh/reference/concept-glossary-pinyin/y/#prediction)问题，也会一起改变。

| 当前真正能看到的东西 | 更自然的问题类型 | 原因 |
| --- | --- | --- |
| 实际目标可以直接看到 | 预测实际目标 | 因为输入与结果可以直接绑定到同一个问题上 |
| 实际目标出现得晚，只能先看到代理列 | 预测代理 target，或把它当成复核候选问题 | 因为现在预测的值与真正想知道的值并不相同 |
| 实际目标很弱，代理列也不稳定 | 保持为比较报告或[复核候选队列(review queue)](/AiBook/zh/reference/concept-glossary-pinyin/s/#output-structure) | 因为连“哪一列该当结果列”本身都还没有足够关上 |

换句话说，一旦使用 proxy target，就必须区分`这个问题可以先做`和`这个问题正在直接解决原始目标`。表面上看像是同一个预测问题，实际上可能预测的是`代理判断`，而不是`实际目标`。如果这层差别没有写出来，后面再去解释分数时，就会混淆到底是把什么预测对了。

## 先看一个场景

假设你真正想知道的是`最终状态确认`，但当前立刻能观测到的只有 `review_needed`。

| event_id | recent_diff | repeatability | review_needed | final_status |
| --- | --- | --- | --- | --- |
| A | -0.31 | high | 1 | 尚未出现 |
| B | -0.05 | low | 0 | 尚未出现 |
| C | -0.28 | high | 1 | 尚未出现 |

在这张表里，现在立刻能构造出的预测问题可能是 `review_needed`。但那并不等于直接预测 `最终状态确认`。也就是说，此刻建立的问题是`是否需要复核`，而不是`最终状态会是什么`。只有保留 proxy target 这个标记，当前问题类型到底是`实际目标预测`还是`代理列预测`才会清楚。

## 用一个小图来看

一旦使用 proxy target，就更适合按下面顺序重读：`现在能看到什么`，以及它和`真正想知道什么`到底在哪里分开。

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-9-mermaid-01-zh.mmd"
```

因此，proxy target 不是一个为了方便而起的临时名字，而是一种明确声明：当前测量的是一个不同于原始目标的替代对象。这里的核心，是把`真正想知道的结果`、`现在能观测到的代理列`、以及`两者之间距离的记录`一起留下来，让代理目标的限制被保存在结构里。

## 来源与参考资料

- Google, *Machine Learning Glossary*, `label`, `derived label`, `proxy labels`。用于确认术语依据：在监督学习中，标签是一个样本的答案或结果部分；当实际标签不存在时，应谨慎选择代理标签。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20

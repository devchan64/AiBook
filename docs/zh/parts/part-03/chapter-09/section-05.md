# P3-9.5 同一个事件在多个产物之间靠什么持续追踪

> Section ID: `P3-9.5`
> Version: `v2026.07.11`

即使比较报告、复核候选队列和目标标签候选表承担的是不同角色，最好也要让同一个样本始终沿用同一套识别标准来持续追踪。像 `event_id` 这样的列之所以会在多张表里反复出现，就是因为这个原因。如果这条连接变得模糊，那么即使能理解三种产物是三张不同的表，也会很难再解释：为什么这个事件会被提上来、某个复核结果后来又是如何变成某个目标标签候选的。[比较报告（comparison report）](../../../reference/concept-glossary.md#glossary-comparison-report)、[复核候选队列（review queue）](../../../reference/concept-glossary.md#glossary-review-queue)、[目标标签候选（target candidate）](../../../reference/concept-glossary.md#glossary-target-candidate)表可以承担不同角色，但同一样本的身份和最小依据连接最好不要被切断。

## 为什么要持续追踪同一个事件

之所以要持续追踪同一个事件，主要有三个原因。

| 需要追踪的原因 | 为什么重要 |
| --- | --- |
| 需要回查比较依据 | 因为要回到原始比较报告里看，这个复核候选为什么会被提上来 |
| 需要接续人工复核结果 | 因为复核队列里的判断以后可能会积累成目标标签候选 |
| 需要重新确认目标候选的来源 | 因为要能回头看当前标签候选是从哪个样本、通过什么路径生成的 |

也就是说，产物可以分成三种，但样本的身份不能跟着分裂。

## 什么会成为追踪标准

最简单的情况下，`event_id` 或 `sample_id` 这样的标识列就能成为追踪键。但在实际里，往往还需要下面这种两三项一起留下来。

| 追踪标准 | 为什么会用到 |
| --- | --- |
| 样本标识符 | 用来指向基本单位，例如一次运行或一个最近区间 |
| 时间点或生成时刻 | 用来区分同一个样本是在什么时候生成的 |
| 版本或基线语境 | 用来回看这个产物是在什么比较条件下生成的 |

例如，即使 `event_id` 相同，基线定义和复核时点也可能不同。因此，追踪同一个事件时，最好不仅留下`它是谁`，还要一起留下`它是在什么时候、在什么比较条件下被读取的`。

## 三种产物里，什么会留下、什么会缩减

即使面对同一个事件，只要产物目的不同，列结构也会缩减。但识别标准和核心依据列，不应该太早消失。

| 产物 | 通常应该保留的东西 | 容易被缩掉的东西 |
| --- | --- | --- |
| 比较报告 | `event_id`、基线值、差值、比较句子 | 只为学习输入准备的精细化列 |
| 复核候选队列 | `event_id`、优先级依据、`review_needed`、`priority_score` | 一部分较长的解释句子 |
| 目标标签候选表 | `event_id`、特征列、目标标签候选、依据备注引用 | 用于比较说明的长句子 |

关键是：像 `event_id` 这样的追踪键和最小依据要保留下来，但不适合当前产物目的的说明可以缩减。

## 一个事件在三张表之间流动的例子

假设存在同一个事件 `A`。

### 1. 比较报告

| event_id | baseline_mean | current_mean | diff | report_sentence |
| --- | ---: | ---: | ---: | --- |
| A | 2.6 | 2.2 | -0.4 | 后段区间均值低于基线 |

### 2. 复核候选队列

| event_id | diff | repeatability | review_needed | priority_score |
| --- | ---: | --- | ---: | ---: |
| A | -0.4 | high | 1 | 0.81 |

### 3. 目标标签候选表

| event_id | mid_flow_mean | late_drop_rate | review_needed | note_source |
| --- | ---: | ---: | ---: | --- |
| A | 2.2 | -0.4 | 1 | 后段区间均值低于基线 |

三张表的列不同，但都指向同一个 `event_id = A`。只有有了这条连接，才能在后面重新解释`为什么 A 会变成 review_needed = 1`。

## 为什么需要像 `note_source` 这样的依据列

在制作目标标签候选表时，最容易漏掉的就是`依据`。如果只留下 `review_needed = 1`，却把它为什么会被附上全部删掉，那么以后就很难再回查标签一致性。

| 值得保留的依据 | 作用 |
| --- | --- |
| 原始比较句子的引用 | 回看为什么它会变成复核候选 |
| 复核备注摘要 | 回看人工到底看到了什么、怎么判断 |
| 基线语境备注 | 回看这个判断是在什么比较条件下附上的 |

所以，目标标签候选表在变成完全`干净的学习表`之前，最好还能暂时保留一套能追溯最小依据的结构。

## 用一个小图来看

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-5-mermaid-01-zh.mmd"
```

这张图更直接展示的，不只是同一个 `event_id` 会在多张表里重复出现，而是为什么这种重复是必要的。即使比较报告、复核候选队列和目标标签候选表承担不同目的，最后也仍然应该能够重新回答：`为什么 A 会被提上来？` 所以，比起合并代码，更重要的是`同一样本身份 + 被保留下来的依据`共同构成了这套追踪结构。

因此，同一个标识列之所以会反复出现，不是为了`机械地 join 表`，而是为了以后还能解释结果的来源和判断的依据。比较报告、复核候选队列和目标标签候选表，即使角色不同，也最好保留同一套样本识别标准，这样之后才能把依据和标签候选重新接回去。如果这个识别标准变得模糊，那么同一个事件的比较依据、复核结果和目标候选就会更难重新串起来。

## 来源与参考资料

- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, provenance and entity linkage overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
- Google, *Machine Learning Glossary*, `labeled example`, `label`, 确认日 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }

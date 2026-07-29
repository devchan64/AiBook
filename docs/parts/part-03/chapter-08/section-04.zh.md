# P3-8.4 保守解读与运营列

> Section ID: `P3-8.4`
> Version: `v2026.07.25`

_副标题: 解读句子如何变成 warning 列和 review queue 标准？_

读完[比较表](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-output-structure)之后，往往会留下类似`最近区间相对基线后段下降更大，因此提高复核优先级`这样的保守解读句子。接下来需要做的判断，是如何把这句话转成 `warning_level`、`review_needed`、`priority_score` 这样的结构化运营列。保守解读句子不是终点，而是在转成[复核候选队列（review queue）](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-output-structure)这类[输出结构](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-output-structure)之前，最后一层人工解读。如果把比较表直接改写成结构化运营输出，中间的判断理由可能会丢失；但如果只留下句子，又很难按同一标准去排运营优先级、检索、或重新排序。

| 层级 | 主要形式 | 作用 |
| --- | --- | --- |
| [比较结果](/AiBook/zh/reference/concept-glossary-pinyin/c/#glossary-comparison-result) | 差值、[基线（baseline）](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-baseline)、重复性 | 显示哪里发生了变化 |
| 保守解读句子 | `需要继续观察`、`提高复核优先级` | 整理给人阅读的判断强度 |
| 结构化运营输出 | `warning_level`、`review_needed`、`priority_score` | 让运营中可再次排序、搜索和后续处理 |

把这三个层级分开，就会形成`数字 -> 句子 -> 运营列`的流程。

## 为什么要先经过句子阶段

在直接生成运营列之前，先经过句子阶段，原因很简单。

- 哪些差异只保留在`记录`级别
- 哪些差异要升成`复核候选`
- 哪些差异要升成`强告警`

这些判断通常不是单靠一个数字，而是要把样本量、重复性和比较条件形成的[证据强度（evidence strength）](/AiBook/zh/reference/concept-glossary-pinyin/j/#interpretation-boundary)一起读完之后才能定下来。因此，句子不是装饰，而是把数字翻译成运营判断的中间阶段。

## 把一个场景重新看成三个阶段

例如，假设最近区间被读成下面这样。

1. 最近 20 条里，后段下降比基线更大。
2. 同时还存在重复性，因此它更接近状态变化候选，而不是一次性事件。
3. 暂缓原因确认，并提高复核优先级。

把这三句话转成运营列之后，可以变成下面这样。

| 句子阶段所说的内容 | 结构化列示例 |
| --- | --- |
| 差异很明确，但暂缓原因确认 | `warning_level = caution` |
| 值得由人工重新看一遍 | `review_needed = 1` |
| 比其他案例更值得先看 | `priority_score = 0.82` |

也就是说，句子不会只停留在自由叙述，它可以被压缩成后面会反复使用的列名。

## 为什么保守解读和运营列不是同一件事

这里要注意的一点是，不能误以为句子和列之间存在自动的一一对应关系。

| 保守句子 | 它并不立刻等于 | 原因 |
| --- | --- | --- |
| `需要继续观察` | 立刻等于 `review_needed = 1` | 因为继续观察也可能仍停留在记录级别 |
| `提高复核优先级` | 立刻等于`原因确认` | 因为复核和诊断是不同层级 |
| `强变化信号` | 立刻等于`自动处置` | 因为还需要运营策略和安全标准 |

所以，句子负责整理强度，但在变成真正的运营列和策略之前，还需要再做一次结构化。

## 先看比较表

| event_id | diff | repeatability | conservative_sentence |
| --- | ---: | --- | --- |
| A | -0.35 | high | 提高复核优先级，并暂缓原因确认 |
| B | -0.35 | low | 虽然看到了差异，但样本较少，因此需要继续观察 |

把这些句子转成结构化运营列之后，可以变成下面这样。

| event_id | warning_level | review_needed | priority_score |
| --- | --- | ---: | ---: |
| A | caution | 1 | 0.82 |
| B | watch | 0 | 0.41 |

之所以这两张表都需要，是因为第一张表留下了`为什么做出这个判断`，而第二张表留下了`运营里可以再次使用的格式`。

## 用一个小图来看

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-4-mermaid-01-zh.mmd"
```

这张图显示的是，即使差值相同，也不会直接进入同样的运营列。要先读取比较结果，再通过人工句子调节解读强度，之后才压缩成 `warning_level`、`review_needed`、`priority_score` 这样的运营列。也就是说，像 `warning_level` 这样的列，并不是突然冒出来的实现物，而是把观测结果经过人工解读之后，再压缩成更容易在运营里复用的格式。这里首先要固定的顺序，同样是先读`哪里变了`，再用句子调节`可以说得多强`，最后再压缩成运营列。

## 来源与参考资料

- Google for Developers, `Thresholds and the confusion matrix`。它说明模型的 raw score 会经过 threshold 才连接到最终分类，因此为本节提供了一般性依据：人工解读句子应当与 `warning_level`、`review_needed`、`priority_score` 这类结构化运营列分开来看。 [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- W3C, `PROV-Overview`。它提供了一种追踪观测结果如何经过中间判断而派生出来的 provenance 视角，因此可用于解释本节在比较结果、保守句子和结构化运营列之间所做的层级区分。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20

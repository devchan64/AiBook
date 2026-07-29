# P3-9.12 target 名称与错误成本

> Section ID: `P3-9.12`
> Version: `v2026.07.25`

_副标题: 即使 target 相同，为什么也要先写清漏掉与误报哪一种更痛？_

即使 [目标(target)](/AiBook/zh/reference/concept-glossary-pinyin/m/#glossary-target) 名称相同，不同问题里更痛的错误也可能不一样。哪怕都是在预测 `review_needed`，漏掉风险案例更危险，还是把本来不需要的人也送去复核更有负担，都会随着运营语境不同而改变。也就是说，即使 target 相同，漏判和误报的成本也可能不同，所以必须先把这种 [错误成本(error cost)](/AiBook/zh/reference/concept-glossary-pinyin/c/#glossary-error-cost) 差别写下来，才能明确当前更想减少的是哪一种判断错误。

| 错误类型 | 在运营里可能发生的事情 |
| --- | --- |
| [假阴性(false negative)](/AiBook/zh/reference/concept-glossary-pinyin/j/#glossary-false-negative) | 漏掉风险案例，可能扩散成更大的异常 |
| [假阳性(false positive)](/AiBook/zh/reference/concept-glossary-pinyin/j/#glossary-false-positive) | 人会白白花时间，增加复核负担 |

| 先写下的备注 | 为什么需要 |
| --- | --- |
| 哪种错误更痛？ | 为了固定当前要优先减少哪类判断 |
| 这种成本在真实运营中以什么形式出现？ | 为了把它解释成行动负担，而不只是数字 |
| 当前更想减少什么？ | 为了即使 target 相同，也能固定解释方向 |

## 为什么错误成本会改变 target 的解释方式

即使是同一个 `review_needed` target，也不是所有预测分数都要用同一种方式去读。在有些问题里，漏判（false negative）更痛，所以即使要让更多项目进入[复核候选队列(review queue)](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-review-queue)，也宁可少漏掉风险案例；而在另一些问题里，过检（false positive）更痛，所以反而更适合把复核队列压得更窄。这里改变的，不只是某个 [阈值(threshold)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-threshold) 数字，而是`应该用什么判断结构去解释这个 target`。

例如，假设模型分数如下。

| event_id | score | 解读 1：漏判成本高 | 解读 2：过检成本高 |
| --- | --- | --- | --- |
| A | 0.82 | 直接放到复核队列顶部 | 放到复核队列顶部 |
| B | 0.64 | 纳入复核队列 | 先保留 |
| C | 0.41 | 作为辅助复核候选保留 | 排除 |

如果漏判成本高，那么把 `B` 也放进复核队列会更自然。相反，如果过检成本高，那么更自然的做法可能是先保留 `B`，只看 `A`。也就是说，即使[分数(score)](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-score)相同、target 名称相同，只要错误成本结构不同，复核队列优先级和 threshold 解读也会一起改变。

下面的例子把多个 threshold 应用到同一组分数上，并分别计算 false negative 和 false positive 的成本。这里把漏判成本设为 10，把误报成本设为 2。

问题场景：想确认同一组 `review_needed` 分数在 threshold 和错误成本设置改变时，总成本会怎样变化。

输入(input)：每个 event 的 `score`、实际结果 `actual`、threshold 候选和错误成本。

期望输出(output)：每个 threshold 下的复核队列大小、false negative 数、false positive 数和总成本。

要确认的概念：threshold 选择不能只看准确率，而要和“哪种错误成本更大”一起读。

```python
# 这个例子用来确认同一组 score 在 threshold 和错误成本设置下会产生不同判断成本。
import pandas as pd
from sklearn.metrics import confusion_matrix

scores = pd.DataFrame(
    [
        {"event_id": "A", "score": 0.82, "actual": 1},
        {"event_id": "B", "score": 0.64, "actual": 1},
        {"event_id": "C", "score": 0.41, "actual": 0},
        {"event_id": "D", "score": 0.36, "actual": 1},
        {"event_id": "E", "score": 0.22, "actual": 0},
    ]
)

thresholds = [0.3, 0.5, 0.7]
miss_cost = 10
false_alarm_cost = 2

for threshold in thresholds:
    predicted = scores["score"].ge(threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(scores["actual"], predicted, labels=[0, 1]).ravel()
    total_cost = fn * miss_cost + fp * false_alarm_cost
    print(
        {
            "threshold": threshold,
            "queued": int(predicted.sum()),
            "false_negative": int(fn),
            "false_positive": int(fp),
            "total_cost": int(total_cost),
        }
    )
```

期望输出：

```text
{'threshold': 0.3, 'queued': 4, 'false_negative': 0, 'false_positive': 1, 'total_cost': 2}
{'threshold': 0.5, 'queued': 2, 'false_negative': 1, 'false_positive': 0, 'total_cost': 10}
{'threshold': 0.7, 'queued': 1, 'false_negative': 2, 'false_positive': 0, 'total_cost': 20}
```

threshold 较低时，复核队列会变大，但不会漏掉风险案例。threshold 较高时，复核队列会变小，但漏判增加，总成本也会上升。这个例子里可以改的值是 `miss_cost`、`false_alarm_cost` 和 `thresholds`。如果把误报成本设得更高，另一个 threshold 可能会更自然。因此，即使 target 名称相同，也必须先写清错误成本，才能沿着同一个方向解释 score 和 threshold。

## 用一个小图来看

即使分数相同，只要当前更想减少的错误不同，复核队列的流向也会跟着改变。

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-12-mermaid-01-zh.mmd"
```

因此，这一节并不只是定义 `false negative` 和 `false positive`。它更是在迫使我们把当前问题重新读成：`到底更想减少哪一种错误`。如果 target 名称已经固定，那么下一步就必须写清楚，在这个 target 之下，哪种错误更痛，这样分数、threshold、复核队列优先级才能沿着同一个方向来解释。

所以，不要只靠准确率就把问题关上，而是先要看：为什么`想优先减少哪一类错误`这件事必须先写出来。这一节把`漏判成本`、`过检成本`和`判定规则调整`捆在一起，先固定错误成本结构，再看它如何改变目标的解释方式。

## 来源与参考资料

- Google, *Machine Learning Glossary*, `false negative`, `false positive`, `ROC curve`。用于确认 false negative 与 false positive 的术语依据，以及真实阈值选择可能受到不同错误成本影响这一说明。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Google, *Thresholds and the confusion matrix*。用于确认：不同阈值会改变 true/false positive 与 true/false negative 的数量；当错误成本不对称时，简单默认阈值可能并不合适。 [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20

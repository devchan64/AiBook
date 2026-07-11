# P3-4.4 哪些信号说明样本单位抓错了

> Section ID: `P3-4.4`
> Version: `v2026.07.10`

如果样本单位抓错了，这个问题通常不会当场消失，而会在后面的阶段以奇怪的形状重新冒出来。`我现在到底该怎么察觉自己抓错了样本单位？` 这个问题之所以重要，也正因为如此。很多情况下，人会在错误的样本单位上继续做特征、标签、比较表，直到很后面才发现整个结构已经开始摇晃。所以这一节把应该怀疑“样本单位判断错了”的代表性警告信号集中放在一起。

当样本单位错了时，问题通常会在后面的步骤里以奇怪形状再次出现。如果同一个标签反复贴在多行上，如果某个特征无法在单行上自然解释，或者虽然已经做出了比较表，却仍然说不清 `这一条到底算什么案例`，那就该重新怀疑样本单位。

## 最常见的警告信号

| 现在看到的异常现象 | 首先该怀疑什么 |
| --- | --- |
| 同一个 `event_id` 的多行上重复贴着同样的标签 | 标签实际上可能属于整次动作，而我们却把时点行读成了样本 |
| 像均值、斜率、波动性这样的特征，很难直接在一行上解释 | 我们可能把时点记录当成样本来读了 |
| 想描述比较结果，却说不清 `这一次` 到底指什么 | 样本单位和比较单位可能被混在一起了 |
| 做训练/评估分割时，同一动作里相邻的行同时进了两边 | 分割单位可能和样本单位没对齐 |
| 做出了近期区段比较表，但个别动作和聚合区段在一张表里看起来混在一起 | 我们可能把样本层级和区段层级当成了同一个单位 |

这张表的重点，并不是说 `所有问题都来自样本单位`。它的意思是：如果在 Part 3 这个阶段看到了这些现象，那么在继续加特征或换模型之前，通常更高效的做法是先回头重新检查样本单位。

## 如果特征总是解释不清，就回头看样本单位

一个很常见的场景是：已经做出了 `late_drop_rate`、`flow_std`、`duration_seconds` 这些特征，但看着某一行时，还是很难自然解释 `这个值到底代表什么`。这时，特征定义本身当然可能有问题，但更常见的原因，是样本单位还不对。

| 特征名 | 自然匹配的样本单位 |
| --- | --- |
| `duration_seconds` | 一次完整动作 |
| `late_drop_rate` | 一次完整动作，或区段摘要 |
| `flow_std` | 一次完整动作，或近期区段 |
| `current_flow` | 一条时点记录 |

也就是说，单看特征名，就已经能大致看出它更适合哪个样本单位。这也正是为什么，一旦我们试图把 `duration_seconds` 放到单个时点行上解释，就会显得很别扭。

## 如果标签在重复，就回头看单位

如果某个运营标签如 `review_needed` 是贴在一次完整动作上的值，那么同样的标签在多条时点日志行里反复出现，就是最典型的“应该重新怀疑样本单位”的信号之一。

| 看到的现象 | 更自然的解释 |
| --- | --- |
| `A` 的三行全都是 `review_needed=1` | 标签可能实际上属于完整动作 `A` |
| `B` 的所有时点行都带着同样的状态值 | 这未必是每行都有新标签，而可能只是把动作级结果重复存了下来 |

这里重要的，并不是说 `标签重复就一定错`。更重要的是重新追问：`这个标签到底附着在哪个单位上？`

## 如果比较句子总觉得别扭，就回头看单位

当样本单位没对齐时，报告句子也会开始变得奇怪。比如说，如果只看一条时点行就试图写出 `这次动作的后段下降比平时更大`，这句话其实站不住，因为“后段下降”必须要在看过完整动作或区段结构之后才能说。

| 想写的句子 | 先需要的样本单位 |
| --- | --- |
| 这次动作比平时更不稳定 | 一次完整动作 |
| 最近状态比平时更低 | 近期区段聚合 |
| 这个时点的传感器值很高 | 一条时点记录 |

换句话说，如果我们总想写的句子，谈论的是比 `一行` 更大的对象，那就应该重新怀疑样本单位。

## 小型代码示例

问题情境：当时点表里同一个标签在重复，而动作级特征又只会在重新归组后出现时，检查该如何把这些读成“样本单位抓错了”的警告信号。

输入(input)：按 `event_id` 存放的原始日志表，其中保存了时点流量值以及实际上属于动作级的 `review_needed`

期望输出(output)：展示重复标签、重复行数，以及只在重组后才出现的事件摘要特征

要确认的概念：重复标签和解释不清的事件级特征，是“单条时点行未必是真正样本单位”的警告信号

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.5, "review_needed": 1},
        {"event_id": "A", "second": 1, "flow": 1.8, "review_needed": 1},
        {"event_id": "A", "second": 2, "flow": 1.1, "review_needed": 1},
        {"event_id": "B", "second": 0, "flow": 0.4, "review_needed": 0},
        {"event_id": "B", "second": 1, "flow": 1.1, "review_needed": 0},
        {"event_id": "B", "second": 2, "flow": 1.0, "review_needed": 0},
    ]
)

label_repetition = raw.groupby("event_id", as_index=False).agg(
    row_count=("second", "count"),
    review_needed_sum=("review_needed", "sum"),
)

event_summary = raw.groupby("event_id", as_index=False).agg(
    duration_seconds=("second", "max"),
    flow_mean=("flow", "mean"),
    review_needed=("review_needed", "max"),
)

warning_check = pd.DataFrame(
    [
        {
            "warning_sign": "same event repeated across many rows",
            "seen_in_output": "yes" if label_repetition["row_count"].max() > 1 else "no",
        },
        {
            "warning_sign": "same label repeated within one event",
            "seen_in_output": "yes" if label_repetition["review_needed_sum"].max() > 1 else "no",
        },
        {
            "warning_sign": "event-level features appear only after regrouping",
            "seen_in_output": "yes" if "duration_seconds" in event_summary.columns else "no",
        },
    ]
)

print("1) row-level table where labels repeat inside one event")
print(raw)
print()
print("2) repeated rows and repeated labels per event")
print(label_repetition)
print()
print("3) event-level summary that appears only after regrouping")
print(event_summary)
print()
print("4) warning signs that sample unit may be wrong")
print(warning_check)
```

期望输出：

```text
1) row-level table where labels repeat inside one event
  event_id  second  flow  review_needed
0        A       0   0.5              1
1        A       1   1.8              1
2        A       2   1.1              1
3        B       0   0.4              0
4        B       1   1.1              0
5        B       2   1.0              0

2) repeated rows and repeated labels per event
  event_id  row_count  review_needed_sum
0        A          3                  3
1        B          3                  0

3) event-level summary that appears only after regrouping
  event_id  duration_seconds  flow_mean  review_needed
0        A                 2   1.133333              1
1        B                 2   0.833333              0

4) warning signs that sample unit may be wrong
                                  warning_sign seen_in_output
0           same event repeated across many rows            yes
1              same label repeated within one event            yes
2  event-level features appear only after regrouping            yes
```

这个例子的关键，不在于计算值本身，而在于 `警告信号究竟是从哪里冒出来的`。在第 2 步里，我们看到同一个 `event_id` 在多行中重复出现，也看到 `review_needed` 在同一次完整动作里被原样复制。第 3 步里，我们看到像 `duration_seconds`、`flow_mean` 这样的动作级特征在原始行里并不存在，只有重新归组后才出现。所以第 4 步的警告表，并不是在制造新的判断，而是在把前面输出里已经看见的信号重新聚起来。

## 说明应该重新看样本单位的问题

在实际里，只要重新写下下面四个问题，方向通常就会清楚很多。

1. 这个标签是贴在一行上，还是贴在一次完整动作上？
2. 这个特征是一行里就能直接读出来，还是必须把多行归起来后才会出现？
3. 我想写的句子是在谈一行，还是在谈一整次动作？
4. 训练/评估分割分的是当前表的行，还是样本单位本身？

这四个问题里，只要有两三个已经对不齐，通常就应该在继续加特征之前，先回头重新检查样本单位。

只要先把这些诊断信号收集起来，我们就能更早区分：哪些情况必须重新归组样本单位，哪些情况可以继续保持原样。也就是说，这里真正重要的不是预告下一阶段，而是通过当前表里已经可见的重复标签、解释不清的特征、别扭的比较句子，尽早识别出“样本单位判断错了”。

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`、`label leakage`。它们一方面解释标签附着在哪个 example 单位上，另一方面说明混淆 feature 和 label 角色的风险，因此支持本节的核心判断：一旦看见重复标签和解释不清的特征，就应该重新检查样本单位。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- W3C, `PROV-Overview`. 它说明应该一起保留 identifying an object 和 derivation，因此强化了这个上位框架：要尽早发现样本单位判断错误，就必须能追踪当前这一行到底是时点记录，还是一次动作摘要。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. 它区分变量、观测值和表结构，因此提供了一般原理，解释为什么把动作级特征硬贴到时点行上时，解释会变得别扭。 [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08

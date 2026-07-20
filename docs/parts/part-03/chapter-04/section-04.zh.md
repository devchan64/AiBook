# P3-4.4 哪些信号说明样本单位抓错了

> Section ID: `P3-4.4`
> Version: `v2026.07.20`

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

输入(input)：保存在 [p3_4_4_sample_unit_warning_log.csv](/AiBook/assets/part-03/chapter-04/p3_4_4_sample_unit_warning_log.csv) 里的原始日志表，以及重复警告标准 `repeat_warning_threshold`。这张表里按 `event_id` 存放了时点流量值，并把属于动作级的 `review_needed` 重复保存到了多行中。

期望输出(output)：同时展示重复标签、重复行数，以及只在重组后才出现的事件摘要特征。只要改变 `repeat_warning_threshold`，哪些重复会被视为警告也会跟着改变。

要确认的概念：重复标签和解释不清的事件级特征，是“单条时点行未必是真正样本单位”的警告信号。只有明示警告标准，代码才不是单纯输出表格，而是在检查样本单位是否被误判。

```python
# 这个例子检查样本单位选错时出现的行数、标签和特征信号。
import csv
from collections import defaultdict
from pathlib import Path

repeat_warning_threshold = 1
preview_row_count = 8

input_path = Path("docs/assets/part-03/chapter-04/p3_4_4_sample_unit_warning_log.csv")

with input_path.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

for row in rows:
    row["second"] = int(row["second"])
    row["flow"] = float(row["flow"])
    row["review_needed"] = int(row["review_needed"])

events = defaultdict(list)
for row in rows:
    events[row["event_id"]].append(row)

label_repetition = []
event_summary = []

for event_id, event_rows in sorted(events.items()):
    review_needed_values = [row["review_needed"] for row in event_rows]
    label_repetition.append(
        {
            "event_id": event_id,
            "row_count": len(event_rows),
            "review_needed_sum": sum(review_needed_values),
        }
    )
    event_summary.append(
        {
            "event_id": event_id,
            "duration_seconds": max(row["second"] for row in event_rows),
            "flow_mean": sum(row["flow"] for row in event_rows) / len(event_rows),
            "review_needed": max(review_needed_values),
        }
    )

max_row_count = max(item["row_count"] for item in label_repetition)
max_label_sum = max(item["review_needed_sum"] for item in label_repetition)

warning_check = [
    (
        "same event repeated across many rows",
        max_row_count > repeat_warning_threshold,
    ),
    (
        "same label repeated within one event",
        max_label_sum > repeat_warning_threshold,
    ),
    (
        "event-level features appear only after regrouping",
        bool(event_summary),
    ),
]

print("1) row-level table where labels repeat inside one event")
for row in rows[:preview_row_count]:
    print(
        f"{row['event_id']} at {row['second']}s: "
        f"flow={row['flow']:.1f}, review_needed={row['review_needed']}"
    )
print(f"... {len(rows) - preview_row_count} more time-point rows")
print()
print("2) repeated rows and repeated labels per event")
for item in label_repetition:
    print(
        f"{item['event_id']}: row_count={item['row_count']}, "
        f"review_needed_sum={item['review_needed_sum']}"
    )
print()
print("3) event-level summary that appears only after regrouping")
for item in event_summary:
    print(
        f"{item['event_id']}: duration={item['duration_seconds']}s, "
        f"flow_mean={item['flow_mean']:.2f}, "
        f"review_needed={item['review_needed']}"
    )
print()
print("4) warning signs that sample unit may be wrong")
for warning_sign, seen in warning_check:
    print(f"{warning_sign}: {'yes' if seen else 'no'}")
```

期望输出：

```text
1) row-level table where labels repeat inside one event
A at 0s: flow=0.5, review_needed=1
A at 1s: flow=0.9, review_needed=1
A at 2s: flow=1.2, review_needed=1
A at 3s: flow=1.5, review_needed=1
A at 4s: flow=1.8, review_needed=1
A at 5s: flow=1.6, review_needed=1
A at 6s: flow=1.4, review_needed=1
A at 7s: flow=1.2, review_needed=1
... 28 more time-point rows

2) repeated rows and repeated labels per event
A: row_count=18, review_needed_sum=18
B: row_count=9, review_needed_sum=0
C: row_count=6, review_needed_sum=6
D: row_count=3, review_needed_sum=0

3) event-level summary that appears only after regrouping
A: duration=17s, flow_mean=0.94, review_needed=1
B: duration=8s, flow_mean=0.88, review_needed=0
C: duration=5s, flow_mean=1.07, review_needed=1
D: duration=2s, flow_mean=0.67, review_needed=0

4) warning signs that sample unit may be wrong
same event repeated across many rows: yes
same label repeated within one event: yes
event-level features appear only after regrouping: yes
```

这个例子的关键，不在于计算值本身，而在于 `警告信号究竟是从哪里冒出来的`。在第 2 步里，我们看到同一个 `event_id` 在多行中重复出现，也看到 `review_needed` 在同一次完整动作里被原样复制。这里可以调节的值是 `repeat_warning_threshold`。如果设为 `1`，重复两次以上的事件和标签就会被视为警告；如果把它提高到 `3`，即便输出相同，警告也可能减少。第 3 步里，我们看到像 `duration_seconds`、`flow_mean` 这样的动作级特征在原始行里并不存在，只有重新归组后才出现。所以第 4 步的警告表，并不是在制造新的判断，而是根据明示标准把前面输出里已经看见的信号重新聚起来。

## 说明应该重新看样本单位的问题

在实际里，只要重新写下下面四个问题，方向通常就会清楚很多。

1. 这个标签是贴在一行上，还是贴在一次完整动作上？
2. 这个特征是一行里就能直接读出来，还是必须把多行归起来后才会出现？
3. 我想写的句子是在谈一行，还是在谈一整次动作？
4. 训练/评估分割分的是当前表的行，还是样本单位本身？

这四个问题里，只要有两三个已经对不齐，通常就应该在继续加特征之前，先回头重新检查样本单位。

## 用一个小图来看

这一节列出的警告信号，并不是彼此独立的检查项。重复标签、单行解释不清的特征、别扭的比较句子、错误的分割，最后都会收敛到同一个方向：重新检查样本单位。

--8<-- "assets/part-03/chapter-04/p3-4-4-mermaid-01-zh.mmd"

只要先把这些诊断信号收集起来，我们就能更早区分：哪些情况必须重新归组样本单位，哪些情况可以继续保持原样。也就是说，这里真正重要的不是预告下一阶段，而是通过当前表里已经可见的重复标签、解释不清的特征、别扭的比较句子，尽早识别出“样本单位判断错了”。

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`、`label leakage`。它们一方面解释标签附着在哪个 example 单位上，另一方面说明混淆 feature 和 label 角色的风险，因此支持本节的核心判断：一旦看见重复标签和解释不清的特征，就应该重新检查样本单位。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- scikit-learn developers, `Cross-validation: evaluating estimator performance`。它说明在 grouped data 中，验证 fold 的样本应来自配对训练 fold 中完全没有出现过的组，因此直接强化了这个警告：如果同一动作里的相邻行同时出现在训练和评估两边，就应该重新检查样本单位和分割单位。 [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. 它说明应该一起保留 identifying an object 和 derivation，因此强化了这个上位框架：要尽早发现样本单位判断错误，就必须能追踪当前这一行到底是时点记录，还是一次动作摘要。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. 它区分变量、观测值和表结构，因此提供了一般原理，解释为什么把动作级特征硬贴到时点行上时，解释会变得别扭。 [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

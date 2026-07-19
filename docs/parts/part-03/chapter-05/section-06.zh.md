# P3-5.6 当重叠的输入窗口很多时，为什么样本数会看起来比实际更大

> Section ID: `P3-5.6`
> Version: `v2026.07.20`

一旦输入窗口(window)定下来，就可以从同一条源时间序列里切出多个窗口。这时很容易忽略一个问题：`窗口变多了，所以样本也变多了。` 但当窗口之间大量重叠时，这往往意味着 `同一个事件被切着看了很多次`，并不等于独立事件数也按同样倍数增加。

输入窗口数和源事件数，不一定是同一个数字。

| 区分 | 含义 |
| --- | --- |
| 源事件数 | 实际发生过的完整动作或真实事件数 |
| 输入窗口数 | 从这些事件里切出来的学习输入片段数 |

例如，如果对一次动作用长度 30、stride 10 来切窗口，那么一个事件就可能扩展成多个输入。

| event_id | 源长度 | 窗口长度 | stride | 生成的窗口数 |
| --- | ---: | ---: | ---: | ---: |
| A | 100 | 30 | 10 | 8 |
| B | 100 | 30 | 10 | 8 |

如果只看这张表就说 `有 16 条样本`，那只对了一半。真实事件数是 2，输入窗口数是 16。所以，在比较报告或代表性判断里，仍然应该把 `只有 2 个真实事件` 这件事一起写出来。

重叠窗口越多，下面这些问题就越容易出现。

| 会出现的问题 | 为什么要注意 |
| --- | --- |
| 样本数看起来变大 | 证据看起来会比实际事件数更夸张 |
| 很相似的窗口反复出现 | 同一个事件的模式会多次重复，独立性变弱 |
| 最近事件被切得更多 | 某些特定事件在表里的影响可能被放大 |

在这个阶段，还不需要把复杂的评估设计全部展开。但最好先留下下面这些备注。

| 先写下来的备注 | 为什么需要 |
| --- | --- |
| 源事件数 | 避免真实证据单位被隐藏掉 |
| 输入窗口数 | 便于把模型输入规模单独看清 |
| 窗口长度与 stride | 便于再次说明窗口是按什么规则扩展开来的 |

看一个小例子，会更清楚。

问题情境：确认当重叠输入窗口很多时，如果把窗口数和源事件数当成同一个数字去读，会产生什么错觉。

输入(input)：源事件表 [p3_5_6_source_events.csv](/AiBook/assets/part-03/chapter-05/p3_5_6_source_events.csv)，以及要实验的移动间隔 `stride_to_try`。这张表中的一行就是一个源事件，并包含事件长度(`length`)和窗口长度(`window`)。

期望输出(output)：显示每个事件会扩展成多少个窗口，以及 `window` 数相对 `source_event` 数放大了多少。改变 `stride_to_try` 时，窗口数和扩展比例也会改变。

要确认的概念：输入窗口数只是派生出来的片段数，不能和源事件数当成同一种单位来读

```python
import csv
from collections import defaultdict
from pathlib import Path

stride_to_try = 10
preview_event_count = 8
source_events_path = Path("docs/assets/part-03/chapter-05/p3_5_6_source_events.csv")

with source_events_path.open(newline="", encoding="utf-8") as file:
    events = []
    for row in csv.DictReader(file):
        length = int(row["length"])
        window = int(row["window"])
        window_count = ((length - window) // stride_to_try) + 1
        events.append(
            {
                "event_id": row["event_id"],
                "line_id": row["line_id"],
                "mode": row["mode"],
                "length": length,
                "window": window,
                "stride": stride_to_try,
                "window_count": window_count,
                "source_event_weight": 1,
            }
        )


def print_event_preview(rows):
    print("event_id line_id     mode  length  window  stride  window_count")
    for row in rows:
        print(
            f"{row['event_id']:>8} {row['line_id']:>7} {row['mode']:>8} "
            f"{row['length']:>7} {row['window']:>7} {row['stride']:>7} "
            f"{row['window_count']:>13}"
        )


def print_expansion_preview(rows):
    print("event_id  window_count")
    for row in rows:
        print(f"{row['event_id']:>8} {row['window_count']:>13}")

print("1) how many windows each source event creates")
print_event_preview(events[:preview_event_count])
print(f"... {len(events) - preview_event_count} more source events")
print()
print("2) source-event count vs window count")
print("          unit  count")
print(f"0  {'source_event':<12} {sum(row['source_event_weight'] for row in events):>5}")
print(f"1  {'window':>12} {sum(row['window_count'] for row in events):>5}")
print()
print("3) expansion per source event")
print_expansion_preview(events[:preview_event_count])
print(f"... {len(events) - preview_event_count} more source events")
print()
print("4) expansion summary by line and mode")
groups = defaultdict(lambda: {"source_event_count": 0, "window_count": 0})
for row in events:
    group = groups[(row["line_id"], row["mode"])]
    group["source_event_count"] += row["source_event_weight"]
    group["window_count"] += row["window_count"]

print("line_id     mode  source_event_count  window_count  mean_windows_per_event")
for line_id, mode in sorted(groups):
    group = groups[(line_id, mode)]
    mean_windows = group["window_count"] / group["source_event_count"]
    print(
        f"{line_id:>7} {mode:>8} {group['source_event_count']:>19} "
        f"{group['window_count']:>13} {mean_windows:>23.2f}"
    )
print()
print("5) expansion ratio")
print(round(sum(row["window_count"] for row in events) / len(events), 2))
```

期望输出：

```text
1) how many windows each source event creates
event_id line_id     mode  length  window  stride  window_count
     E01      L1 baseline     100      30      10             8
     E02      L1 baseline      96      30      10             7
     E03      L1 baseline      92      30      10             7
     E04      L1 baseline      88      30      10             6
     E05      L1 baseline      84      30      10             6
     E06      L1 baseline      80      30      10             6
     E07      L1   recent     110      30      10             9
     E08      L1   recent     104      30      10             8
... 28 more source events

2) source-event count vs window count
          unit  count
0  source_event    36
1        window   237

3) expansion per source event
event_id  window_count
     E01             8
     E02             7
     E03             7
     E04             6
     E05             6
     E06             6
     E07             9
     E08             8
... 28 more source events

4) expansion summary by line and mode
line_id     mode  source_event_count  window_count  mean_windows_per_event
     L1 baseline                   6            40                    6.67
     L1   recent                   6            42                    7.00
     L2 baseline                   6            40                    6.67
     L2   recent                   6            43                    7.17
     L3 baseline                   6            34                    5.67
     L3   recent                   6            38                    6.33

5) expansion ratio
6.58
```

这个例子的目的，并不主要是计算窗口数，而是确认 `窗口数会把真实事件数膨胀成什么样子`。这里可以操作的值是 `stride_to_try`。如果把 `10` 改成 `20`，窗口数和扩展比例会下降；如果改成更小的值，同一批源事件会产生更多输入片段。但 `source_event` 数仍然是 36 个。因此，重叠输入窗口可能只是同一个事件被切着看了很多次，不能把窗口数直接当作事件数来读。像第 4 步那样按线路和运行模式重新分组后也可以看到：每个条件下的源事件数都是 6 个，但派生出的 window 数会随着长度和窗口设置而不同程度地膨胀。

## 用一个小图来看

这一节的核心，是把 `窗口数变大了` 和 `源事件数增加了` 分开来看。即使从同样 2 个事件里切出很多重叠窗口，输入片段数会变大，但事件数本身并不会跟着变。

--8<-- "assets/part-03/chapter-05/p3-5-6-mermaid-01-zh.mmd"

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。因为 example 预设的是特征和标签附着的单位，所以它支持这一节的判断：即使生成了很多输入窗口，也不意味着源事件数本身自动增加了。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- W3C, `PROV-Overview`. provenance framework 说明应能追踪某个实体是通过什么派生过程生成的，因此它提供了一个更高层的框架：每个输入窗口都应与它来自哪个源事件分开保留，才能避免把窗口数和事件数混淆。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Datasets: Dividing the original dataset`. 它提供了一般视角：训练样本应与源数据及其生成规则区分开来。因此，它也有助于推广这一节的说明：即使窗口大量重叠，也应把源事件单位和输入片段单位分开写明。 [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- scikit-learn developers, `Cross-validation: evaluating estimator performance`. 该文档说明，同一源过程产生的依赖样本可能破坏独立同分布假设；在 grouped data 中，也应避免同一组的样本同时出现在训练 fold 和验证 fold 中。因此，它强化了这一节的提醒：重叠输入窗口可能只是来自同一事件的依赖片段，而不是新的真实事件。 [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

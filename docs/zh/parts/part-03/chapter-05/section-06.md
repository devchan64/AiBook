# P3-5.6 当重叠的输入窗口很多时，为什么样本数会看起来比实际更大

> Section ID: `P3-5.6`
> Version: `v2026.07.10`

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

输入(input)：给定事件长度以及 `window`、`stride` 的源事件表

期望输出(output)：显示每个事件会扩展成多少个窗口，以及 `window` 数相对 `source_event` 数放大了多少

要确认的概念：输入窗口数只是派生出来的片段数，不能和源事件数当成同一种单位来读

```python
import pandas as pd

events = pd.DataFrame(
    [
        {"event_id": "A", "length": 100, "window": 30, "stride": 10},
        {"event_id": "B", "length": 100, "window": 30, "stride": 10},
    ]
)

events["window_count"] = ((events["length"] - events["window"]) // events["stride"]) + 1
events["source_event_weight"] = 1

print("1) how many windows each source event creates")
print(events[["event_id", "length", "window", "stride", "window_count"]])
print()
print("2) source-event count vs window count")
print(
    pd.DataFrame(
        [
            {"unit": "source_event", "count": events["source_event_weight"].sum()},
            {"unit": "window", "count": events["window_count"].sum()},
        ]
    )
)
print()
print("3) expansion per source event")
print(events[["event_id", "window_count"]])
```

期望输出：

```text
1) how many windows each source event creates
  event_id  length  window  stride  window_count
0        A     100      30      10             8
1        B     100      30      10             8

2) source-event count vs window count
          unit  count
0  source_event      2
1        window     16

3) expansion per source event
  event_id  window_count
0        A             8
1        B             8
```

这个例子的目的，并不主要是计算窗口数，而是确认 `窗口数会把真实事件数膨胀成什么样子`。所以第 1 步里，我们先看每个事件会扩展成多少个窗口；第 2 步里，把 `source_event` 和 `window` 分开计数；第 3 步里，再看每个事件分别扩展了多少。这里真正重要的是：`重叠输入窗口，往往只是把同一个事件切着看了很多次，因此不能把窗口数直接当作事件数来读。`

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。因为 example 预设的是特征和标签附着的单位，所以它支持这一节的判断：即使生成了很多输入窗口，也不意味着源事件数本身自动增加了。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- W3C, `PROV-Overview`. provenance framework 说明应能追踪某个实体是通过什么派生过程生成的，因此它提供了一个更高层的框架：每个输入窗口都应与它来自哪个源事件分开保留，才能避免把窗口数和事件数混淆。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- Google for Developers, `Datasets: Dividing the original dataset`. 它提供了一般视角：训练样本应与源数据及其生成规则区分开来。因此，它也有助于推广这一节的说明：即使窗口大量重叠，也应把源事件单位和输入片段单位分开写明。 [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08

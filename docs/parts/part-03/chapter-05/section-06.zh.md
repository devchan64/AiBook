# P3-5.6 重叠输入窗口与样本数

> Section ID: `P3-5.6`
> Version: `v2026.09.19`

_副标题: 把同一事件切成多个窗口时，为什么样本数会看起来比实际更大？_

一旦[输入窗口(input window)](/AiBook/zh/reference/concept-glossary-pinyin/m/#model-input)定下来，就可以从同一条[源时间序列(source time series)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-source-data)里切出多个窗口。这时很容易忽略一个问题：`窗口变多了，所以样本也变多了。` 但当窗口之间大量重叠时，这往往意味着 `同一个事件被切着看了很多次`，并不等于独立事件数也按同样倍数增加。

输入窗口数和[源事件(source event)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-source-data)数，不一定是同一个数字。

| 区分 | 含义 |
| --- | --- |
| 源事件数 | 实际发生过的完整动作或真实事件数 |
| 输入窗口数 | 从这些事件里切出来的学习输入片段数 |

例如，如果对一次动作用长度 30、stride 10 来切窗口，那么一个事件就可能扩展成多个输入。

`stride` 表示窗口起点每次移动多少个测量点。源长度为 100、窗口长度为 30、步长为 10 时，起点为 0、10、…、70，共八个窗口。如果规则是丢弃末尾不完整的窗口，则 `窗口数 = floor((源长度−窗口长度)/步长)+1`；源长度短于窗口时，窗口数为 0。这里 `floor` 表示向下取整。

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
| 较长或切分更密集的事件产生更多窗口 | 某些特定事件在表里的影响可能被放大 |

在这个阶段，还不需要把复杂的评估设计全部展开。但最好先留下下面这些备注。

| 先写下来的备注 | 为什么需要 |
| --- | --- |
| 源事件数 | 避免真实证据单位被隐藏掉 |
| 输入窗口数 | 便于把模型输入规模单独看清 |
| 窗口长度与 stride | 便于再次说明窗口是按什么规则扩展开来的 |

## 同一个观测进入两个窗口

假设一个小型虚构事件 A 按观测顺序包含 `[10, 11, 12, 13, 14, 15]`。这些数字是测量值，位置编号从 0 到 5。窗口长度为 4，步长为 2，丢弃不完整窗口。`[起点, 终点)` 表示包含起点位置，但不包含终点位置。

| source_event_id | window_id | 位置范围 | 窗口内的值 |
| --- | --- | --- | --- |
| A | A-01 | [0, 4) | [10, 11, **12, 13**] |
| A | A-02 | [2, 6) | [**12, 13**, 14, 15] |

两个窗口中的 12、13 是**位置 2、3 的同一批观测**，不是数值偶然相同。两个窗口共有 8 个值的位置，但不同的原始观测只有 6 个，源事件只有 1 个。把步长改为 1 后，起点 0、1、2 生成 3 个窗口，并没有采集新事件或新测量。

同样，源长度 100、窗口长度 30、步长 10 的前两个窗口是 [0, 30) 和 [10, 40)，共享位置 10～29 的 20 个观测。这里长度和步长的单位是测量点数；换算成秒需要知道测量间隔。

派生窗口应保留 `source_event_id`、`window_id`、`window_start`、`window_end`，并记录窗口长度、步长与不完整窗口的处理规则。源表先确认每个事件只有一行，再统计行数；窗口表则统计去重后的 `source_event_id` 数量。下面的例子直接统计事件数，不需要单独的事件权重列。

问题情境：确认当重叠输入窗口很多时，如果把窗口数和源事件数当成同一个数字去读，会产生什么错觉。

输入(input)：源事件表 [p3_5_6_source_events.csv](/AiBook/assets/part-03/chapter-05/p3_5_6_source_events.csv){ .csv-preview }，以及要实验的移动间隔 `stride_to_try`。这张表中的一行就是一个源事件，并包含事件长度(`length`)和窗口长度(`window`)。

期望输出(output)：显示每个事件会扩展成多少个窗口，以及 `window` 数相对 `source_event` 数放大了多少。改变 `stride_to_try` 时，窗口数和扩展比例也会改变。

要确认的概念：输入窗口数只是派生出来的片段数，不能和源事件数当成同一种单位来读

```python
# 这个例子检查重叠输入窗口是否因重复计算同一事件而放大样本数。
import csv
from collections import defaultdict
from pathlib import Path

stride_to_try = 10
if not isinstance(stride_to_try, int) or isinstance(stride_to_try, bool) or stride_to_try <= 0:
    raise ValueError("stride_to_try must be a positive integer")
preview_event_count = 8
source_events_path = Path("docs/assets/part-03/chapter-05/p3_5_6_source_events.csv")

with source_events_path.open(newline="", encoding="utf-8") as file:
    events = []
    for row in csv.DictReader(file):
        length = int(row["length"])
        window = int(row["window"])
        if length < 0 or window <= 0:
            raise ValueError("length must be nonnegative and window positive")
        window_count = max(0, ((length - window) // stride_to_try) + 1)
        events.append(
            {
                "event_id": row["event_id"],
                "line_id": row["line_id"],
                "mode": row["mode"],
                "length": length,
                "window": window,
                "stride": stride_to_try,
                "window_count": window_count,
            }
        )

if not events:
    raise ValueError("source-event table must not be empty")
if len({row["event_id"] for row in events}) != len(events):
    raise ValueError("event_id must be unique in the source-event table")

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
print(f"... {max(0, len(events) - preview_event_count)} more source events")
print()
print("2) source-event count vs window count")
print("          unit  count")
print(f"0  {'source_event':<12} {len(events):>5}")
print(f"1  {'window':>12} {sum(row['window_count'] for row in events):>5}")
print()
print("3) expansion per source event")
print_expansion_preview(events[:preview_event_count])
print(f"... {max(0, len(events) - preview_event_count)} more source events")
print()
print("4) expansion summary by line and mode")
groups = defaultdict(lambda: {"source_event_count": 0, "window_count": 0})
for row in events:
    group = groups[(row["line_id"], row["mode"])]
    group["source_event_count"] += 1
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

## 6.58 的分母是 36 个源事件

默认输出的 **237 个窗口 ÷ 36 个事件 ≈ 6.58 个窗口/事件**，表示每个事件的平均窗口数。它不表示新信息增加到 6.58 倍，也不表示存在 237 个独立事件。即使某个短事件没有生成窗口，这里的分母仍统计输入源表中的全部事件；应与至少生成一个窗口的事件数区分。

| 步长：测量点数 | 输入源事件数 | 窗口数 | 平均窗口数：个/事件 |
| ---: | ---: | ---: | ---: |
| 5 | 36 | 453 | 12.58 |
| 10 | 36 | 237 | 6.58 |
| 20 | 36 | 129 | 3.58 |

运行前先预测把步长改为 20 会改变什么，再把输出与表格比较。答案是 129 个窗口，每个事件约 3.58 个窗口，事件数仍为 36。仅计算 E01，起点 0、20、40、60 就会生成 4 个窗口。这一规则不会额外补上从 70 开始的窗口。

分组输出中，L2 recent 和 L3 baseline 各有 6 个事件，却分别贡献 43 和 34 个窗口。如果每个窗口的比重相同，两组的贡献为 43:34；如果按事件等比重比较，则为 6:6。应根据问题选择赋予相同比重的单位。recent 这个名称本身不会增加窗口；这份数据中的长度与窗口设置造成了数量差异。

## 事件 ID 不同也需要检查独立性

36 个不同的事件 ID 不保证是 36 次独立实验。同一设备、同一天或同一工作批次连续产生的事件，可能受到共同条件影响。这也不意味着重叠窗口没有用途：它们能把同一事件的不同位置作为输入，但这与采集新事件不同。

评估新事件上的性能时，若把 A-01 用于训练、A-02 用于评估，同一原始观测就会进入两边。按源事件划分是防止这种重叠的一种方法；若评估新设备或未来时段，还需要检查更大的分组或时间顺序。因此，派生窗口不能丢掉源事件 ID。


## 区分输入窗口数与源事件数 {#_1}

这一节的核心，是把 `窗口数变大了` 和 `源事件数增加了` 分开来看。即使从同样 2 个事件里切出很多重叠窗口，输入片段数会变大，但事件数本身并不会跟着变。

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-6-mermaid-01-zh.mmd"
```

## 检查清单

- 能否用不同单位解释 237 个窗口、36 个事件和 6.58 个窗口/事件？
- 能否指出两个窗口共享的观测位置，并验证步长 20 时有 129 个窗口？
- 能否解释源事件数为什么不能保证统计独立性？

- 你是否根据输入长度和步长计算了窗口数量？
- 你能否解释重叠窗口数为什么不等于独立事件数？

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary`, `example`, `labeled example`. example 可以没有标签；labeled example 同时包含特征与标签。 将重叠窗口数与源事件数分开统计，是本节案例展示的区别。 [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-09-15
- W3C, `PROV-Overview`. provenance framework 说明应能追踪某个实体是通过什么派生过程生成的，因此它提供了一个更高层的框架：每个输入窗口都应与它来自哪个源事件分开保留，才能避免把窗口数和事件数混淆。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Datasets: Dividing the original dataset`. 它提供了一般视角：训练样本应与源数据及其生成规则区分开来。因此，它也有助于推广这一节的说明：即使窗口大量重叠，也应把源事件单位和输入片段单位分开写明。 [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- scikit-learn developers, `Cross-validation: evaluating estimator performance`. 该文档说明，同一源过程产生的依赖样本可能破坏独立同分布假设；在 grouped data 中，也应避免同一组的样本同时出现在训练 fold 和验证 fold 中。因此，它强化了这一节的提醒：重叠输入窗口可能只是来自同一事件的依赖片段，而不是新的真实事件。 [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-09-19

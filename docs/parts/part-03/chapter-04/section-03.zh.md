# P3-4.3 一行、一个样本、一个近期区段有什么不同

> Section ID: `P3-4.3`
> Version: `v2026.07.25`

[一行(row)](/AiBook/zh/reference/concept-glossary-pinyin/h/#glossary-row)、一个[样本(sample)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-sample)、`一个近期区段` 都会在看数据表时浮现出来，但它们并不属于同一个层级。在[源数据(source data)](/AiBook/zh/reference/concept-glossary-pinyin/y/#glossary-source-data)表里，先看见的是行；在比较一次完整动作时，中心会变成样本；到了[基准线(baseline)](/AiBook/zh/reference/concept-glossary-pinyin/b/#glossary-baseline)比较时，近期区段又会作为另一个比较单位出现。

必须一次把这三个单位区分开的原因，是[特征(feature)](/AiBook/zh/reference/concept-glossary-pinyin/f/#glossary-feature)、基准线比较和复核语句分别贴在不同层级上。一旦把一行误当成样本，或者把区段读成一条样本，后面搭出来的表结构和比较结构也会一起开始摇摆。

把这三个层级重新分开，可以写成下面这样。

- `一行` 是当前表里看得见的一条线。
- `一个样本` 是用来比较或学习的基本单位。
- `一个近期区段` 是把多个样本重新聚起来后的比较单位。

这三者可以彼此包含，但并不是同一件事。

| 现在看到的对象 | 最自然的问题 | 这一节里的层级 |
| --- | --- | --- |
| 一条时点日志 | 这个时点测到了什么？ | 行 |
| 一次完整动作 | 这次动作的结构是不是和平常不同？ | 样本 |
| 最近 20 次这组样本 | 最近状态是不是和平常区段不一样？ | 区段 |

这张表说明：`有一条线`、`有一条样本`、`有一个可比较的近期区段` 其实各自在回答不同问题。Part 3 容易一直混淆，不是因为它们本来就在同一层，而是因为这三个问题都从看数据表开始。

## 把同一个场景重新读成三个层级

再来看一次自动执行动作的数据。

| event_id | second | flow |
| --- | ---: | ---: |
| A | 0 | 0.8 |
| A | 1 | 1.5 |
| A | 2 | 1.1 |
| B | 0 | 0.7 |
| B | 1 | 1.2 |
| B | 2 | 1.0 |

第一次看到这张表时，会看见六行。但这六行未必就是六条样本。如果这里把 `A` 这一次完整动作看成一条样本，那么上面的三行其实只是组成这条样本的时点记录。

再往下，如果把多个动作重新聚起来做成 `最近 20 次的均值`，那么像 `A`、`B` 这样的单条样本就会再往下掉一级。因为近期区段是把多个样本重新聚起来后的聚合单位。

把同一个场景放到三个层级里，就可以这样读。

| 层级 | 什么算一条 | 例子 |
| --- | --- | --- |
| 行 | 一条时点记录 | `A, second=1, flow=1.5` |
| 样本 | 一次完整动作 | `event_id=A` 的整体 |
| 区段 | 多个样本的集合 | 最近 20 次的均值和波动性 |

换句话说，`A, second=1` 可能不是一条样本，而只是构成样本的一小块；而 `最近 20 次` 则可能是把 20 条样本再次聚起来后得到的更大比较单位。

如果把同样的场景再写成句子，就会更清楚。

- 如果运营人员问的是 `第 1 秒时点的流量是多少？`，那他们想看的就是行。
- 如果运营人员问的是 `A 这次动作是不是比平常更不稳定？`，那他们想看的就是样本。
- 如果运营人员问的是 `最近 20 次是不是比上周的基准线更差？`，那他们想看的就是区段。

关键就在于：只要问题变了，同一份源数据就会被重新读成不同层级。混淆通常不是因为数据太复杂，而是因为我们还没先写下自己当前到底贴的是哪个问题，就开始看表了。

## 为什么必须做这个区分

之所以必须区分，是因为后面的概念会贴在不同层级上。

| 概念 | 主要贴在哪个层级 | 原因 |
| --- | --- | --- |
| 原始测量值 | 行 | 因为它是某个时点的真实观测值 |
| 特征 | 样本 | 因为它是在描述一次完整动作的结构 |
| 基准线比较 | 区段，或样本对区段 | 因为必须拿近期状态和平常状态作比较 |
| 复核语句 | 区段或样本 | 因为它是给人读取的判断单位 |

例如，像 `late_drop_rate` 这样的特征，并不会直接贴在单个时点行上。它只能在先把一次完整动作构造成样本之后才能算出来。反过来，像 `recent_count=20` 这样的值就不是单条样本特征，而更像近期区段聚合。所以，只要把这些层级混着读，特征、基准线和[输出结构(output structure)](/AiBook/zh/reference/concept-glossary-pinyin/s/#glossary-output-structure)就都会变得抽象。

## 一眼看懂的代码小例子

问题情境：通过行数和输出结构确认 `一行`、`一个样本`、`一个近期区段` 在同一份原始日志里属于不同层级。

输入(input)：按 `event_id` 存放的时点流量记录，以及标记近期/基准线区段的列

期望输出(output)：`row count`、`sample count`、`window count` 各不相同，而且每个层级里“一条”的含义也不同

要确认的概念：行、样本、区段是同一份数据的不同表达层级，不能当作同一个单位来读

```python
# 这个例子把一行、一个样本和一个近期区段作为不同分析单位进行比较。
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.8},
        {"event_id": "A", "second": 1, "flow": 1.5},
        {"event_id": "A", "second": 2, "flow": 1.1},
        {"event_id": "B", "second": 0, "flow": 0.7},
        {"event_id": "B", "second": 1, "flow": 1.2},
        {"event_id": "B", "second": 2, "flow": 1.0},
        {"event_id": "C", "second": 0, "flow": 0.9},
        {"event_id": "C", "second": 1, "flow": 1.6},
        {"event_id": "C", "second": 2, "flow": 1.2},
    ]
)

per_event = (
    raw.groupby("event_id", as_index=False)
    .agg(
        flow_mean=("flow", "mean"),
        flow_max=("flow", "max"),
    )
    .assign(window=lambda df: df["event_id"].map({"A": "recent", "B": "baseline", "C": "recent"}))
)

per_window = (
    per_event.groupby("window", as_index=False)
    .agg(
        event_count=("event_id", "count"),
        flow_mean=("flow_mean", "mean"),
    )
)

print("1) counts change by level")
print("row count:", len(raw))
print("sample count:", len(per_event))
print("window count:", len(per_window))
print()
print("2) one row still means one time-step record")
print(raw.loc[[1], ["event_id", "second", "flow"]])
print()
print("3) one sample means one whole event")
print(per_event.loc[per_event["event_id"] == "A", ["event_id", "flow_mean", "flow_max"]])
print()
print("4) one window means multiple samples regrouped")
print(per_window)
```

期望输出：

```text
1) counts change by level
row count: 9
sample count: 3
window count: 2

2) one row still means one time-step record
  event_id  second  flow
1        A       1   1.5

3) one sample means one whole event
  event_id  flow_mean  flow_max
0        A   1.133333       1.5

4) one window means multiple samples regrouped
     window  event_count  flow_mean
0  baseline            1   0.966667
1    recent            2   1.183333
```

这里真正要看的，不是数字本身，而是 `到底在数什么`。

- `row count: 9` 表示 9 条时点记录。
- `sample count: 3` 表示 3 次动作。
- `window count: 2` 表示 `recent` 和 `baseline` 两个区段。

而下面那三段输出，则把每个层级的代表形态直接展示出来。

- `one row example` 是像 `A, second=1, flow=1.5` 这样的一条时点线。
- `one sample example` 是一条样本，比如动作 `A` 的均值和最大值。
- `window summary` 则是把样本表进一步聚成 `recent` 和 `baseline` 之后得到的区段汇总。

行数减少，并不是因为简单压缩，而是因为 `什么算一条案例` 已经发生了变化。

如果把这个例子压成一句话，就是：`A, second=1` 展示的是当时发生了什么，`event_id=A` 展示的是一次动作整体怎么样，而 `recent` 展示的是把若干条样本重新聚起来后的状态比较。即便是同一份数据，只要问题变了，我们就会在这三个层级之间来回切换。

## 第一次拿到表时可以快速追问的问题

在实际里，只要先写下下面三个问题，混淆就会少很多。

1. 当前表里的一条线表示的是时点记录、一次完整动作，还是近期区段聚合？
2. 我现在想读的是一条线、一整次动作，还是整个近期状态？
3. 我现在要贴上的值，是特征、比较列，还是复核语句候选？

这三个问题分别在重新拆开 `行`、`样本`、`区段`。

这一节并不是一个术语对照表，而可以重新读成：它在处理的是如何同时阅读 `表达层级(levels of representation)` 的问题。

## 用一个小图来看

把前面的说明压到最短，就是 `一行 -> 一个样本 -> 一个区段` 代表同一份数据被一步步读成更大的比较单位。每个层级回答的问题不同，所以不能把它们混成同一个单位来读。

--8<-- "assets/part-03/chapter-04/p3-4-3-mermaid-01-zh.mmd"

所以，`一行`、`一个样本`、`一个近期区段` 不应该被读成三个名字相近的对象，而应该被读成：为了回答不同问题，同一份源数据在不同层级上被重新表达之后得到的结果。

## 来源与参考资料

- W3C, `PROV-Overview`. provenance framework 说明它应支持 identifying an object 和 representing derivation，因此为把行级记录、事件级样本、窗口级聚合作为不同表达层级分别记录下来提供了一般依据。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 它说明基准时期是拿来和其他时期比较的 reference，因此强化了这一点：像近期区段和基准区段这类聚合层级表达，属于和样本层级不同的比较层级。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。因为 example 预设的是样本层级结构，所以它支持这样一点：不应该把行级记录和窗口级聚合读成样本层级 example。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

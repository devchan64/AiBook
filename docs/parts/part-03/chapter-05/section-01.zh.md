# P3-5.1 如何把原始日志转换成可比较的表

> Section ID: `P3-5.1`
> Version: `v2026.07.20`

第一次看到原始日志时，数据往往显得非常丰富。因为按时间顺序积累了很多数值，可能还有多个传感器，也可能同时包含控制参数。但这种丰富，并不自动意味着我们已经拥有了可比较的数据集。在样本 [sample](/AiBook/en/reference/concept-glossary/#glossary-sample) 单位定下来之后，仍然需要一个把原始日志转换成汇总表和聚合表的过程。原始日志、汇总表、聚合表各自承担不同角色，而且每一行所代表的对象也不同。

`原始日志 -> 汇总表 -> 聚合表`，是把同一条时间序列重新表达成适合不同问题的表结构的顺序。只要这个顺序能被看见，后面的 [baseline](/AiBook/en/reference/concept-glossary/#glossary-baseline) 比较和 [intermediate representation](/AiBook/en/reference/concept-glossary/#glossary-intermediate-representation) 设计究竟接在什么层级上，也会更清楚。

以自动执行的一次动作作为例子。原始日志里，在动作进行中的每一个时点，都会留下包含传感器值和控制值的一行记录。到了汇总表，一次完整的自动动作才会变成一行。到了聚合表，一行又可能表示把多个动作重新汇总后的结果，比如最近 20 次的平均值，或者平时某个区间的平均值。

| 表的类型 | 一行代表什么 | 主要回答的问题 |
| --- | --- | --- |
| 原始日志 | 动作过程中的一个时点记录 | 现在测到了什么？ |
| 汇总表 | 对一次完整动作做出的样本汇总 | 这次动作是什么结构？ |
| 聚合表 | 由多个动作构成的近期或基准线汇总 | 最近的变化和以往状态不同吗？ |

这不只是表名不同而已。原始日志擅长保留细节流程，但很难直接比较完整动作。汇总表让动作之间的比较更容易，但大多数瞬时波动会被压缩掉。聚合表让人更快读出近期状态，但单个动作的特殊形状可能会被抹平。

所以，这一节里的表转换，与其说是 `做出一张表`，不如说更接近 `把数值型信息和类别型状态一起整理成可探索的结构`。数值探索要到汇总表能够比较水平、变化和波动性时才真正开始；类别探索也要把状态标签、缺失标记、重叠情况、不可比较原因等一起整理出来，才算真正开始。

| 探索视角 | 在表里先要留下什么 | 后面小节会继续读什么 |
| --- | --- | --- |
| 数值探索 | 区间平均值、变化率、波动性 | 超出平均值的模式、近期对基准线的差异 |
| 类别探索 | 状态标签、缺失标记、重叠/不可比较标记 | 样本坍塌的区分、可比较性判断 |

因此，把 `汇总` 理解成简单压缩是不够的。一条动作汇总行，是把原始时间序列中的多行记录，改写成人和模型都更容易处理的一行。关键不在于再次重定义样本单位，而在于在已经定好的样本单位之上，做出可比较的表。它能让比较更容易，但并不会替代原始时间序列里的所有上下文。

所以，读表时最先该问的，不是 `列是什么`，而是 `这一行是什么`。原始日志中的一行，通常还不是一条完整样本。只有变成汇总表里的一行时，完整动作才算真正能被读作可比较的样本。聚合表则更进一步，把多个样本重新组合成一个比较结构。

从原始日志走到汇总表，不只是把行数减少而已。在这一阶段，我们还要一起决定 `要怎么切区间`、`要计算哪些变化率`、`哪些传感器值应当留下来作为代表值`。例如，一次动作的汇总表中，可能会包含总动作时长、前段平均压力、中段平均流量、后段下降率、控制跟随误差等列。这些值并不是原始日志里本来就以单行形式存在的值，而是把多个时点的值重新表达成更适合人类比较的结果。

下面的图，把这个转换压缩成了最短的形式。

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-1-mermaid-01-zh.mmd"
```

在这条流程里，`Segment by progress` 这一步尤其重要。我们并不是直接对原始日志整体求平均，而是先把动作切成前段、中段、后段这样的可比较区间，然后才会得到汇总值。`Aggregate across events` 则是下一步。对一次动作做汇总，和对近期区间再做聚合，不是同一件事，后者是再往上做一次组合。

所以，看到这些表时，最好先确认 `现在我手里的这张表，在这三种表里属于哪一种起点`，这样才不容易把不同表混在一起读。

| 现在手里的表 | 首先要做什么 | 仅靠这张表仍然困难的事 |
| --- | --- | --- |
| 原始日志 | 确定动作边界和区间标准 | 直接比较不同动作 |
| 汇总表 | 比较动作与动作之间的差异 | 读取近期反复变化的趋势 |
| 聚合表 | 看近期状态与基准线的差异 | 查看单个动作的细节形状 |

聚合表的角色还会再变一次。这里的重点不再是单个动作的形状，而是 `最近 20 次的平均值`、`最近 20 次的波动性`、`相对基准线的差异`、`同方向变化重复了多少次` 这样的组合走势。也就是说，如果汇总表更接近 `读案例`，那么聚合表就更接近 `读状态`。

下面的例子展示原始日志如何先变成动作级汇总表，再进一步变成近期/基准线聚合表。这里假设我们把动作按三个进度区间切开，计算区间平均值，并比较 3 个 `baseline` 动作和 3 个 `recent` 动作。

问题情境：一次性查看原始日志如何先变成 `动作级汇总表`，再变成 `近期/基准线聚合表`。

输入(input)：[`p3_5_1_raw_log_segments.csv`](/AiBook/assets/part-03/chapter-05/p3_5_1_raw_log_segments.csv){: target="_blank" rel="noopener noreferrer" } 文件。一行表示一次动作中一个进度区间里的 `flow` 测量记录，`window` 表示该动作属于基准线区间还是近期区间。

期望输出(output)：`raw`、`summary`、`aggregate` 三张表分别具有不同的行含义与比较角色

要确认的概念：把原始日志变成可比较的表，意味着把同一份记录逐步改写成汇总表与聚合表

```python
import csv
from collections import defaultdict
from pathlib import Path

data_path = Path("docs/assets/part-03/chapter-05/p3_5_1_raw_log_segments.csv")

with data_path.open(newline="", encoding="utf-8") as file:
    raw = [
        {**row, "flow": float(row["flow"])}
        for row in csv.DictReader(file)
    ]

event_segments = defaultdict(lambda: {"window": None, "segments": defaultdict(list)})
for row in raw:
    event = event_segments[row["event_id"]]
    event["window"] = row["window"]
    event["segments"][row["progress_bin"]].append(row["flow"])

summary = []
for event_id in sorted(event_segments):
    event = event_segments[event_id]
    summary.append(
        {
            "event_id": event_id,
            "window": event["window"],
            "early_flow_mean": sum(event["segments"]["early"]) / len(event["segments"]["early"]),
            "mid_flow_mean": sum(event["segments"]["mid"]) / len(event["segments"]["mid"]),
            "late_flow_mean": sum(event["segments"]["late"]) / len(event["segments"]["late"]),
        }
    )

window_groups = defaultdict(list)
for row in summary:
    window_groups[row["window"]].append(row)

aggregate = []
for window in sorted(window_groups):
    rows = window_groups[window]
    aggregate.append(
        {
            "window": window,
            "event_count": len(rows),
            "early_flow_mean": sum(row["early_flow_mean"] for row in rows) / len(rows),
            "mid_flow_mean": sum(row["mid_flow_mean"] for row in rows) / len(rows),
            "late_flow_mean": sum(row["late_flow_mean"] for row in rows) / len(rows),
        }
    )

print("1) raw log rows before comparison")
for row in raw[:6]:
    print(
        f'{row["event_id"]} {row["window"]:<8} '
        f'{row["progress_bin"]:<5} flow={row["flow"]:.2f}'
    )
print(f"... {len(raw) - 6} more raw log rows")
print()
print("2) per-event summary table for direct comparison")
for row in summary:
    print(
        f'{row["event_id"]} {row["window"]:<8} '
        f'early={row["early_flow_mean"]:.2f} '
        f'mid={row["mid_flow_mean"]:.2f} '
        f'late={row["late_flow_mean"]:.2f}'
    )
print()
print("3) recent-vs-baseline aggregate table built from event summaries")
for row in aggregate:
    print(
        f'{row["window"]:<8} events={row["event_count"]} '
        f'early={row["early_flow_mean"]:.2f} '
        f'mid={row["mid_flow_mean"]:.2f} '
        f'late={row["late_flow_mean"]:.2f}'
    )
```

期望输出：

```text
1) raw log rows before comparison
A baseline early flow=0.70
A baseline early flow=0.90
A baseline mid   flow=2.00
A baseline mid   flow=2.10
A baseline late  flow=1.70
A baseline late  flow=1.80
... 30 more raw log rows

2) per-event summary table for direct comparison
A baseline early=0.80 mid=2.05 late=1.75
B baseline early=0.80 mid=2.15 late=1.65
C baseline early=0.80 mid=2.00 late=1.85
D recent   early=0.95 mid=2.45 late=1.85
E recent   early=1.05 mid=2.65 late=1.95
F recent   early=1.00 mid=2.55 late=1.75

3) recent-vs-baseline aggregate table built from event summaries
baseline events=3 early=0.80 mid=2.07 late=1.75
recent   events=3 early=1.00 mid=2.55 late=1.85
```

从这个输出可以看到，原始日志包含 36 条时点记录；到了第 2 步，6 次完整动作才分别变成一行；第 3 步则把这些样本再次汇总成 `baseline` 和 `recent` 聚合结果。这里重要的，不只是行数减少了，而是 `前段`、`中段`、`后段` 这样的比较单位进入了汇总表的列结构，并且这张汇总表又成了后续近期状态比较表的原料。如果改动 CSV 里的数值，动作级汇总值和近期/基准线聚合值都会一起变化，因此读者可以直接确认判断究竟在哪个表示层发生变化。

看完这个例子之后，可以用下面几个问题来检查，刚才发生的到底只是压缩，还是表示层的转换。

1. 现在减少的只是行数，还是连样本级表示都重新定义了？
2. `early`、`mid`、`late` 是原始日志里本来就有的列，还是为了比较新造出来的区间？
3. 如果下一步想做最近 20 次的平均值，现在更直接的起点是这张表，还是原始日志？

只要能回答这些问题，`原始日志 -> 汇总表 -> 聚合表` 就更容易被读成不是简单的压缩顺序，而是为了不同判断问题而发生的一连串表示转换。

同样的流程，也可以更短地这样判断。

| 现在需要的判断 | 更直接的起点 |
| --- | --- |
| 比较单个动作的结构 | 汇总表 |
| 比较近期状态与平时状态 | 聚合表 |
| 检查异常变化发生的具体时点 | 原始日志 |

这张表的重要性，不是说 `只要做出一张好表就结束了`，而是说：不同的问题，需要向上或向下切换到不同的表去读。

另一个重要点是，这三种表并不是互相竞争的。做出了汇总表，并不意味着原始日志就不需要了。做出了聚合表，也不意味着动作级表失去价值。恰恰相反，如果在聚合表里看到了异常变化，就应该重新回到汇总表和原始日志去检查。为了比较而增加的表示层越多，重新回看原始时间序列的过程也越重要。

因此，`原始日志 -> 汇总表 -> 聚合表` 不是简单的压缩顺序，而是把同一条时间序列依次改写到记录层、样本层、状态层的一套连续设计。关键不在于表一张张增加，而在于：有些问题以原始记录为更直接的依据，有些问题以样本汇总为更直接的依据，还有些问题以状态聚合为更直接的依据。

## 来源与参考资料

- W3C, `PROV-Overview`. provenance framework 说明处理步骤、可复现性、版本和派生关系都应可表示，因此它为“原始日志是如何经过处理变成汇总表和聚合表”的分层记录提供了一般依据。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary` 中的 `example` 和 `labeled example`。因为 example 预设的是特征和标签附着在样本层结构上，所以它强化了区分原始行与动作汇总行，并构建样本层表结构的必要性。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 它把基准时段说明为比较其他时段的参考，因此为“比较近期状态和基准线状态时，需要像聚合表这样的独立表示层”提供了一般依据。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

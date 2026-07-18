# P3-4.1 怎样决定一条可比较的样本

> Section ID: `P3-4.1`
> Version: `v2026.07.17`

读数据时最先要确认的，不是数值大小，而是 `一行到底表示什么`。如果这个问题没有先定下来，那么后面做特征、贴标签、读评估结果时，标准都会一起晃动。归根到底，这个问题会继续追到 `什么应该算一条可比较样本`。

假设在一次自动执行动作里，同时留下了控制参数时间序列和传感器时间序列。在某张表里，一行可能表示 `第 1 秒时刻的压力和流量测量值`。在另一张表里，一行可能表示 `一次完整动作的摘要`。再换一张表，一行又可能表示 `最近 30 分钟内若干次动作的聚合结果`。这三种都来自同一份源数据，但一行所代表的对象完全不同。

| 区分 | 一行表示什么 | 主要回答的问题 |
| --- | --- | --- |
| 测量值表 | 动作中的某个时点的一项传感器值或控制值 | 当前这个时点的值是多少？ |
| 动作单位表 | 一次完整的自动执行动作 | 这次动作整体结构怎么样？ |
| 近期区段表 | 由若干动作聚成的近期聚合 | 最近的变化是否在重复？ |
| 基准线表 | 代表平常状态的比较聚合 | 和平常相比，现在差了多少？ |

这张表说明，即使面对同一份数据，`一行的含义` 也会随着要回答的问题不同而变化。测量值表擅长读取当前状态，但不能立刻展示完整动作的结构。反过来，动作单位表更适合比较一次动作，却不会原样保留逐时点的瞬时变化。近期区段表和基准线表还会再往前一步，它们表示的已经不是 `一条案例`，而是 `把若干案例重新聚起来后的比较结构`。因此，眼前看见了行，并不意味着那一行就能直接当作一条样本。如果模型要学的是 `完整动作的模式`，那么多个时点测量行就必须重新归成一个新的样本，也就是 `一次动作`。

在这里，要把某个单位称为 `可比较样本`，至少要同时满足三件事。

1. 一条案例的边界要清楚。
2. 同类特征必须能用同一种方式贴到所有案例上。
3. 后面要贴上的标签或比较基准，必须能自然地接到这个单位上。

用这三条来看，按时点记录的一行通常只比较容易满足第一条，第二条和第三条都偏弱。反过来，动作 1 次的摘要表往往更容易同时满足这三条。近期区段表在第三条的比较基准上很强，但它更像是把若干样本重新聚起来后的解释结构，而不是一条单独样本比较。因此，这一节真正要定的是：在 `一个时点`、`一次完整动作`、`一个近期区段` 这三者之间，哪一个该被看作一条可比较样本。

当一张表第一次摆到眼前时，按下面顺序去读，角色区分会更清楚。

1. 先看当前表里的一行表示的是 `一个时点`、`一次完整动作`，还是 `多个动作的聚合`。
2. 再看这一行是为了回答什么问题而做出来的。
3. 最后确认那个问题是否和我们现在要解的问题一致。

走完这个顺序之后，就能稍微延后那种自动化假设：`既然看见了行，那样本应该也已经有了吧。` 也正因为这样，我们才不会把原始日志、摘要表、近期区段表混成同一类表去读。

下面这个小表会让这种差别更清楚。

| event_id | elapsed_seconds | pressure | flow |
| --- | --- | --- | --- |
| A | 0 | 1.0 | 0.0 |
| A | 1 | 2.0 | 1.4 |
| A | 2 | 2.4 | 1.6 |
| B | 0 | 1.1 | 0.0 |
| B | 1 | 1.7 | 1.1 |
| B | 2 | 2.0 | 1.2 |

在这张表里，一行并不是 `一次完整动作`，而是 `动作中的某个时点`。所以，如果我们想把一条样本看成一次完整动作，那么同一个 `event_id` 下的多行就必须重新归到一起。而且再往下看一步，就会发现：即使面对同一份源数据，选择把 `一个时点`、`一次完整动作` 还是 `一个近期区段` 读成一条案例，不仅会让样本数变化，也会连带改变哪些列只在那个单位上才真正有意义。

现在把这个例子再按前面三条标准重读一遍，就更清楚为什么说 `一次完整动作` 更接近可比较样本。

| 候选单位 | 边界清楚吗？ | 容易贴上同类特征吗？ | 容易贴上标签 / 比较基准吗？ |
| --- | --- | --- | --- |
| 一条测量行 | 是 | 弱 | 弱 |
| 一次完整动作 | 是 | 是 | 是 |
| 一组近期区段 | 是 | 只在部分情况下 | 对比较基准很强，但对单条样本标签较弱 |

换句话说，如果把 `一次完整动作` 作为一条样本，那么 `pressure_mean`、`pressure_rise`、`flow_mean` 这类特征就能用同样方式贴到所有案例上，而像 `需要复核`、`正常`、`异常` 这样的结果，也会自然地连接在这个单位上。反过来，一条测量行很适合保存瞬时观测值，却很难稳定地承载“比较完整动作结构”所需的特征和标签。近期区段一组，则更像不是“单条动作比较样本”，而是“把若干动作重新聚成一组后的解释单位”。

所以在实际里，`到底应该先拿哪个单位当样本？` 可以按下面这样来决定。

| 现在要回答的问题 | 先抓的样本单位 | 原因 |
| --- | --- | --- |
| 这次动作是不是比其他动作更异常？ | 一次完整动作 | 因为比较对象是 `动作 对 动作` |
| 压力是在哪个时点突然升高的？ | 测量时点 | 因为问题本身就在问瞬时变化发生的时点 |
| 最近的运行状态是不是变得不同了？ | 一个近期区段包 | 因为比较对象不是单次动作，而是近期区段和基准区段 |
| 能不能做出以后用来预测 `needs review` 的输入表？ | 一次完整动作 | 因为结果通常贴在动作级别上，特征也会在这里更稳定地算出来 |

所以，什么该算一条样本，并不是只看表长什么样就能定，而必须先按当前问题到底是 `时点比较`、`动作比较` 还是 `区段比较` 来决定。在这一节的例子里，问题是 `比较完整动作的模式`，所以一次完整动作就成了最自然的样本单位。

## 用一个小图来看

把前面的判断压成一行，就是先选定 `现在要回答的问题`，再把和这个问题相匹配的单位当作样本。在这一节里，问题是 `这次动作异常吗`，所以最自然会落到 `一次完整动作` 这条可比较样本上。

--8<-- "assets/part-03/chapter-04/p3-4-1-mermaid-01-zh.mmd"

问题情境：确认即使面对同一份原始日志，只要把 `一个时点`、`一次完整动作`、`一个近期区段` 读成一条样本，后面得到的可比较表就会不一样。

输入(input)：按 `event_id` 保存时点记录的原始日志表，以及一个标记每条记录是否属于近期区段的标志列

期望输出(output)：`measurement_row`、`event`、`window` 这三种单位会产生不同的样本数和不同的特征可能性

要确认的概念：一条可比较样本不是由眼前看见的行数决定的，而是由和问题匹配的分析单位决定的

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "elapsed_seconds": 0, "pressure": 1.0, "flow": 0.0, "is_recent": 1, "review_needed": 1},
        {"event_id": "A", "elapsed_seconds": 1, "pressure": 2.0, "flow": 1.4, "is_recent": 1, "review_needed": 1},
        {"event_id": "A", "elapsed_seconds": 2, "pressure": 2.4, "flow": 1.6, "is_recent": 1, "review_needed": 1},
        {"event_id": "B", "elapsed_seconds": 0, "pressure": 1.1, "flow": 0.0, "is_recent": 0, "review_needed": 0},
        {"event_id": "B", "elapsed_seconds": 1, "pressure": 1.7, "flow": 1.1, "is_recent": 0, "review_needed": 0},
        {"event_id": "B", "elapsed_seconds": 2, "pressure": 2.0, "flow": 1.2, "is_recent": 0, "review_needed": 0},
        {"event_id": "C", "elapsed_seconds": 0, "pressure": 1.2, "flow": 0.1, "is_recent": 1, "review_needed": 1},
        {"event_id": "C", "elapsed_seconds": 1, "pressure": 2.3, "flow": 1.5, "is_recent": 1, "review_needed": 1},
        {"event_id": "C", "elapsed_seconds": 2, "pressure": 2.7, "flow": 1.8, "is_recent": 1, "review_needed": 1},
    ]
)

event_summary = (
    raw.groupby("event_id", as_index=False)
    .agg(
        total_duration_seconds=("elapsed_seconds", "max"),
        pressure_mean=("pressure", "mean"),
        pressure_rise=("pressure", lambda s: s.iloc[-1] - s.iloc[0]),
        flow_mean=("flow", "mean"),
        is_recent=("is_recent", "max"),
        review_needed=("review_needed", "max"),
    )
)

window_summary = (
    event_summary.groupby("is_recent", as_index=False)
    .agg(
        event_count=("event_id", "count"),
        pressure_mean=("pressure_mean", "mean"),
        flow_mean=("flow_mean", "mean"),
    )
    .assign(window_name=lambda df: df["is_recent"].map({0: "baseline", 1: "recent"}))
    [["window_name", "event_count", "pressure_mean", "flow_mean"]]
)

unit_check = pd.DataFrame(
    [
        {
            "unit_name": "measurement_row",
            "sample_count": len(raw),
            "can_use_pressure_rise": "no",
            "label_attaches_naturally": "weak",
        },
        {
            "unit_name": "event",
            "sample_count": len(event_summary),
            "can_use_pressure_rise": "yes",
            "label_attaches_naturally": "yes",
        },
        {
            "unit_name": "window",
            "sample_count": len(window_summary),
            "can_use_pressure_rise": "partial",
            "label_attaches_naturally": "weak",
        },
    ]
)

print("1) count rows under each candidate unit")
print("measurement rows:", len(raw))
print("event samples:", len(event_summary))
print("window aggregates:", len(window_summary))
print()
print("2) raw rows still mean per-time-step records")
print(raw.groupby("event_id").size().reset_index(name="measurement_rows"))
print()
print("3) event-level summaries can hold comparison features and labels")
print(
    event_summary[
        [
            "event_id",
            "total_duration_seconds",
            "pressure_mean",
            "pressure_rise",
            "flow_mean",
            "review_needed",
        ]
    ]
)
print()
print("4) window-level aggregates are for broader comparison, not single-sample judgment")
print(window_summary)
print()
print("5) unit check for comparable-sample suitability")
print(unit_check)
```

期望输出：

```text
1) count rows under each candidate unit
measurement rows: 9
event samples: 3
window aggregates: 2

2) raw rows still mean per-time-step records
  event_id  measurement_rows
0        A                 3
1        B                 3
2        C                 3

3) event-level summaries can hold comparison features and labels
  event_id  total_duration_seconds  pressure_mean  pressure_rise  flow_mean  review_needed
0        A                       2       1.800000            1.4   1.000000              1
1        B                       2       1.600000            0.9   0.766667              0
2        C                       2       2.066667            1.5   1.133333              1

4) window-level aggregates are for broader comparison, not single-sample judgment
  window_name  event_count  pressure_mean  flow_mean
0    baseline            1       1.600000   0.766667
1      recent            2       1.933333   1.066667

5) unit check for comparable-sample suitability
         unit_name  sample_count can_use_pressure_rise label_attaches_naturally
0  measurement_row             9                    no                      weak
1            event             3                   yes                       yes
2           window             2               partial                      weak
```

这段输出里首先应该看到的是 `到底在数什么`。在原始表里，是 9 条测量时点；按 `event_id` 归组之后，是 3 条动作级样本；再往上按近期与基准区段重新分组之后，就变成了 2 组用于比较的聚合。接着要看的，是 `哪些值只有在某个单位上才真正有意义`。像 `pressure_rise` 这种看起点和终点差值的列，不可能从单独一条时点行里直接做出来，只有在数据先被归成一次完整动作后，它才真正有意义。反过来，`window_summary` 不是用来比较单次动作的表，而是把多个动作重新聚在一起之后才得到的比较解释表。所以，即便面对同一份源数据，只要把 `一个时点`、`一次完整动作`、`一个近期区段` 读成一条样本，行数、表的含义，以及能放上去的列的角色都会跟着一起变。

这里 `unit check` 的输出还会更直接地展示本节的判断。`measurement_row` 虽然样本数最多，但它没法直接承载 `pressure_rise`，也很难让 `review_needed` 这类结果自然地贴上去。`window` 可以用来解释近期状态，却不太适合作为单条动作比较样本。反过来，`event` 把样本数、摘要特征和结果列都放在同一个单位上，所以它最符合本节的问题，也就是 `一条可比较样本`。

这个例子并不只是展示如何计数样本单位。

| 这里看见的值 | 它自然属于哪个单位 | 原因 |
| --- | --- | --- |
| 单个时点值，如 `pressure`、`flow` | 测量时点 | 因为它们是那个瞬间的观测值 |
| `pressure_mean`、`pressure_rise` | 一次完整动作 | 因为它们只有在多个时点被归到一起后才成为摘要值 |
| `event_count`、近期均值 | 近期区段或基准区段 | 因为它们是把多个动作重新聚起来后的比较聚合 |

这样看下来，`决定一条样本` 并不只是减少行数，而是在决定：哪些列会在当前单位上读起来更自然。

第一次拿到表时，也可以很快做一个判断。这种快速判断同时也暴露了它在数据生命周期里处在什么阶段。测量值表更接近观测和记录，动作单位表更接近可比较样本的表达，而近期区段表和基准线表则更接近解释与决策准备。

| 如果当前表长这样 | 首先该怀疑的行含义 |
| --- | --- |
| 有时间列，而且同一个 `event_id` 重复出现很多次 | 很可能是一条时点记录 |
| 每个 `event_id` 只有一行，并且有均值、最大值、斜率这类摘要列 | 很可能是一条完整动作样本 |
| 出现最近 20 次均值、此前 200 次均值这类比较列 | 很可能是把多个动作聚起来后的区段聚合 |

这张判别表的目的，不是背表名，而是快速分出：眼前的行到底是 `可以立刻比较的样本`，还是 `仍然需要重新归组成样本的记录`。

只有先有动作级摘要表，均值、斜率、波动性这类特征才能稳定地建立起来，之后近期区段和基准线的比较也才能在同一个单位上阅读。所以，`一行到底表示什么` 这个问题，并不会在决定样本单位时就结束，它会成为支撑 Part 3 后续结构的底层规则。

可比较样本，并不是先由数据自己决定的。它是由问题所要求的比较单位，以及之后要放上去的特征和标签结构一起决定的。所以当我们说 `决定一条样本` 时，意思不是重新数行，而是在观测单位和聚合单位之间，决定哪个对象应该被当作可比较的分析单位。

## 来源与参考资料

- W3C, `PROV-Overview`. provenance framework 说明它应支持 identifying an object 和 representing derivation，因此提供了一般依据：在时点记录、一次完整动作、近期区段这些不同单位之间，必须能够说明到底把哪个对象选成了分析单位。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- Google for Developers, `Machine Learning Glossary` 中的 `labeled example`。因为一个 example 应该是 feature 和 label 能自然附着的单位，所以它强化了这点：样本更应该选成“一次完整动作”这样的单位，而不是一条时点记录。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- U.S. Bureau of Labor Statistics, `Base period`. 它说明基准时段是用来和其他时期比较的 reference，因此为这一点提供了一般依据：要和基准区段比较，必须先定下“比较单位本身”是什么。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08

# P3-6.1 应该用什么特征把可比较的结构留下来

> Section ID: `P3-6.1`
> Version: `v2026.07.17`

第一次学习特征时，人们常常会把它理解成 `列越多越好吗？` 但特征(feature)并不是简单地往里塞更多数值。特征是把样本所具有的结构，重新表达成可以用于比较和预测的值。所以，好的特征与其说是“更多”，不如说应该先让 `它到底想展示什么` 变得清楚。如果前一节已经把原始日志变成了汇总表，那么现在就要决定：这张汇总表里到底该留下什么结构。

所谓“设计特征”，不是把汇总表里的数字原样照用，而是重新选择：要用什么数字表达，来保留我们想比较的结构。所以，只有先决定想保留什么结构，平均值、斜率、波动性这样的特征候选才会真正有意义。这里还会再分出一个判断。把同一个结构转换成平均值、差值、斜率、token、比率这样的不同表达，是变量变换(variable transformation)；而从这些已经变换出来的表达里，再决定究竟保留哪些项目，则是特征选择(feature selection)。

| 视角 | 现在问的问题 | 代表例子 |
| --- | --- | --- |
| 变量变换 | 同一个结构要转换成什么表达？ | 平均值、区间差值、斜率、比率、token |
| 特征选择 | 转换出来的表达里，哪些真正要留下来？ | 整体水平特征、后段崩塌检测特征、波动性特征 |

假设我们把一次自动执行的动作看成一个样本。此时，不能把时点级传感器值整串原样塞进同一行里。我们需要做的是，生成能显露动作关键面向的汇总值。例如，下面这些值经常是不错的起点。

- 平均值(mean)
- 斜率(slope)
- 波动性(variability)
- 最大值或最小值
- 特定区间的变化率

为什么这些值会经常出现？第一，它们能在不过度粗暴丢弃原始曲线的前提下，比较容易转成可比较的数字。第二，即使是人来读，也更容易说明成 `这次动作平均值差不多，但后段下降更陡` 这样的句子。第三，即使平均值相同，只要波动性或斜率不同，也可能显露出真实的结构差异。

也就是说，好的特征更接近 `合适的问题`，而不是 `很多数值`。平均值展示整体水平，斜率展示方向和变化速度，波动性展示摆动幅度。之所以需要不同特征，也是因为每个值能显露出的结构不同。对于同一张汇总表，先做什么变换、再从中保留什么，正是变量变换和特征选择的核心。

| 动作 | 平均值 | 斜率 | 波动性 | 可以读出的结构 |
| --- | --- | --- | --- | --- |
| A | 相近 | 平缓 | 低 | 相对稳定 |
| B | 相近 | 陡 | 高 | 不稳定或变化较大 |

问题情境：当两次动作的整体水平相近，但上升幅度和波动程度不同时，确认应该留下哪些特征。

输入(input)：只保留了分段平均值的动作汇总表

期望输出(output)：从同一张汇总表中分别计算出水平、区间差值、斜率、波动性的特征表

要确认的概念：特征不是把已有列直接罗列出来，而是把想比较的结构计算后再附着上去的表达

```python
import pandas as pd

segment_summary = pd.DataFrame(
    [
        {"event_id": "A", "early_flow_mean": 1.8, "mid_flow_mean": 2.2, "late_flow_mean": 2.6},
        {"event_id": "B", "early_flow_mean": 2.1, "mid_flow_mean": 2.2, "late_flow_mean": 2.3},
    ]
)

feature_table = segment_summary.copy()
feature_table["overall_mean"] = feature_table[
    ["early_flow_mean", "mid_flow_mean", "late_flow_mean"]
].mean(axis=1)
feature_table["late_minus_early"] = (
    feature_table["late_flow_mean"] - feature_table["early_flow_mean"]
)
feature_table["early_to_late_slope"] = feature_table["late_minus_early"] / 2
feature_table["segment_variability"] = feature_table[
    ["early_flow_mean", "mid_flow_mean", "late_flow_mean"]
].std(axis=1)

print("1) segment means before feature design")
print(segment_summary)
print()
print("2) designed features for comparison")
print(
    feature_table[
        [
            "event_id",
            "overall_mean",
            "late_minus_early",
            "early_to_late_slope",
            "segment_variability",
        ]
    ].round(2)
)
```

期望输出：

```text
1) segment means before feature design
  event_id  early_flow_mean  mid_flow_mean  late_flow_mean
0        A              1.8            2.2             2.6
1        B              2.1            2.2             2.3

2) designed features for comparison
  event_id  overall_mean  late_minus_early  early_to_late_slope  segment_variability
0        A           2.2               0.8                  0.4                  0.40
1        B           2.2               0.2                  0.1                  0.10
```

输出的第 1 步，还只是带有区间平均值的汇总表。到了第 2 步，`overall_mean`、`late_minus_early`、`early_to_late_slope`、`segment_variability` 才被新加上去。`overall_mean` 展示整体水平，`late_minus_early` 展示前后段差异，`early_to_late_slope` 把这种差异除以区间距离后，变成一个简单斜率表达，`segment_variability` 则展示各区间之间的波动程度。也就是说，特征不是把原本写着的值再展示一遍，而是从同一张汇总表中，计算并附着上想比较的结构。

如果把这些特征按更小的层次来读，每个值承担的角色会更清楚。

| 特征类型 | 代表例子 | 主要展示什么 |
| --- | --- | --- |
| 水平特征 | 平均值、最大值 | 整体规模 |
| 变化特征 | 区间差值、斜率 | 方向与速度 |
| 稳定性特征 | 标准差、波动性 | 摆动程度 |

这张表会再次提醒前面说过的两条分岔。把结构转成平均值、差值、斜率、波动性这一阶段，是变量变换；从里面决定当前问题真正要留下哪些值，这一阶段是特征选择。数值特征是概括结构的第一步，而 token 化表达，则是把这种结构进一步转换成人更容易读的中间表示的下一步。

设计特征时，应该持续检查下面这些问题。

- 这个值展示了动作的哪一个方面？
- 它是否补足了平均值单独看不到的结构？
- 人在阅读时也能解释它吗？
- 它和样本单位匹配得好吗？

如果把这些问题稍微压缩成更实务的形式，那么“想先看什么结构”和“应当先想到什么特征”之间，可以像下面这样去选。

| 想先看的结构 | 优先想到的特征 |
| --- | --- |
| 整体水平是否相近 | 平均值、最大值 |
| 前段和后段差了多少 | 区间差值、斜率 |
| 波动有多大 | 标准差、波动性 |
| 是否在某个时点剧烈变化 | 最大值时点、变化率 |

这张表的重点不是 `多背几个特征名`，而是先决定想看什么结构，再附上最能直接显露该结构的特征。

人们还会再卡住一个地方：即使说“先看结构，再选特征”，这句话本身仍然可能显得抽象。所以，如果再更短地写一次“如何把真实问题转成特征设计”，可以得到下面这样的对应。

| 现场最先冒出来的问题 | 优先做出的特征 | 为什么这个特征要先出现 |
| --- | --- | --- |
| 这次动作的整体水平是否比平时更低 | 平均值、中位数 | 因为可以先确认整体规模差异 |
| 前段还好，但后段是不是崩掉了 | `late_minus_early`、分段斜率 | 因为可以直接显露是哪一段结构变了 |
| 结果看起来差不多，但过程是不是更抖了 | 标准差、分段波动性 | 因为能单独看到被平均值掩盖的不稳定 |
| 峰值是不是来得太晚，或者消失得太早 | 最大值时点、下降开始时点 | 因为时序差异可能会极大改变运行意义 |

所以，特征不是从 `列候选清单` 里挑，而是在做“现在到底在问什么”到数字表达之间的翻译。如果问题在 `整体水平`，那水平特征就应该先出来；如果问题在 `形状变化`，那区间差值和斜率这样的变化特征就应该先出来。只有这层连接定住了，后面的基准线比较里，才能再次解释 `为什么偏偏保留了这个特征。`

这一节与其说是特征列表介绍，不如说更接近于：应该用什么问题来引导 `结构的数值表示(numeric representation of structure)`。

## 用一个小图来看

这一节的顺序是：先定 `要比较的结构`，再把它转换成平均值、差值、斜率、波动性这样的表达，最后才决定哪些特征真正留下来。特征不是简单加列，而是把结构重新翻译成数值形式。

--8<-- "assets/part-03/chapter-06/p3-6-1-mermaid-01-zh.mmd"


因此，特征并不是 `再多加几列`，而是把想比较的结构重新翻译成水平、变化、稳定性这样的数值表达。

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `feature`。它把 feature 解释为用于预测的输入变量，因此支持这样一点：应该先决定想展示什么结构，再把这个结构转成输入变量。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- Google for Developers, `Machine Learning Glossary` 中的 `feature engineering`。它把 feature engineering 解释为决定哪些变换有助于模型训练的过程，因此强化了这一点：特征设计不是保留原始值不动，而是把结构转换成可比较的数字表达。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- U.S. Bureau of Labor Statistics, `Base period`. 它把基准时段解释为比较其他时段的参考，因此提供了一般依据：水平/变化/稳定性特征也应被选成便于在基准线比较中读取的结构。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08

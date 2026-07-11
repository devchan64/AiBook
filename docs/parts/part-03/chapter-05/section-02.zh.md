# P3-5.2 汇总表如何保留平均值之外的模式

> Section ID: `P3-5.2`
> Version: `v2026.07.10`

两个平均值相同的动作，并不一定意味着它们具有相同结构。平均值对于一眼总结整体水平很有用，但它并不能把随时间如何变化的过程全都展示出来。所以，把原始日志转换成汇总表时，不能只因为 `平均值一样` 就放心，还要一起思考：平均值之外的模式差异，要怎样保留下来。

这一节不会重复解释汇总表转换本身的过程。这里更关注前一节做出来的汇总表，不应该只是“留下平均值的表”，而应该继续保留那些会通向后续特征设计和基准线比较的模式差异。

例如，假设两次自动动作的平均流量都记录为 2.4。一次可能是前段快速上升，中段稳定保持，后段缓慢下降。另一次可能是前段几乎不动，后段突然升高后立刻回落。只看一个平均值，二者似乎差不多，但在实际运行上的含义可能完全不同。

为了把这种差异显露出来，就必须在平均值之外，一起留下能表现结构的值。例如：

- 前段平均值
- 中段平均值
- 后段平均值
- 分段斜率
- 最大值出现的时点
- 下降开始的时点

| 动作 | 平均流量 | 前段斜率 | 后段斜率 | 解释 |
| --- | --- | --- | --- | --- |
| A | 2.4 | 大 | 缓慢下降 | 相对稳定 |
| B | 2.4 | 几乎没有 | 急剧下降 | 后段可能不稳定 |

读这张表时也有顺序。先看 `平均值是否相同`，再看 `各区间平均值有什么不同`，最后看 `斜率或时点信息能带来什么解释`。按这个顺序读，`平均值相同，但结构不同` 这句话就会更清楚。

| 读取层级 | 先看的值 | 能知道什么 |
| --- | --- | --- |
| 整体水平 | 整体平均值 | 大致规模是否相近 |
| 区间结构 | 前/中/后段平均值 | 是哪个区间发生了变化 |
| 形状变化 | 斜率、最大值时点、下降开始时点 | 发生了什么样的形状差异 |

也就是说，平均值只是起点。平均值相同，并不能说明结构也相同；平均值不同，也不自动说明究竟是哪个区间不同。汇总表应该是一张能把这些层级区分开来并展示出来的表。

这里，把 `只看平均值会错过什么` 单独写下来，会更容易看清汇总表还需要多展示什么。

| 只看平均值会错过什么 | 应该一起留下的值 |
| --- | --- |
| 变化发生在前段还是后段 | 区间平均值 |
| 上升速度与下降速度是否不同 | 分段斜率 |
| 峰值什么时候出现 | 最大值出现时点 |
| 是稳定维持，还是剧烈波动 | 波动性、下降开始时点 |

这里还要再补上一点。平均值也很容易掩盖离群值(outlier)和分布偏斜(skewness)的影响。例如，大多数动作都在相似范围里，但只有少数案例突然跳到很大值时，平均值会上升，可是 `大多数动作实际上处在什么水平` 反而会变得模糊。反过来，如果大部分值集中在一边，只有少数案例向另一边拉出很长的尾部，那么平均值也很难表现这种不对称结构。

| 仅靠平均值不容易看见什么 | 为什么容易漏掉 | 应该一起留下的值 |
| --- | --- | --- |
| 少数极端值的影响 | 少量案例也可能大幅拉动平均值 | 最小值、最大值、分位数 |
| 单边长尾 | 平均值会把分布不对称压成一个数字 | 中位数、分位数、区间频次 |
| 大多数稳定但少数波动很大的结构 | 平均值无法区分典型案例和稀有案例 | 样本数、离群值备注、波动性 |

下面这个小例子，用数字确认“平均值相同，但模式不同”的情况。

问题情境：确认即使整体平均值看起来相同，只要分段流动不同，就应该读作不同的运行结构。

输入(input)：只保留 `early_flow_mean`、`mid_flow_mean`、`late_flow_mean` 的动作汇总表

期望输出(output)：即使 `overall_mean` 相同，区间差异和 `pattern_note` 仍然不同的输出

要确认的概念：单个平均值无法解释所有模式差异，因此应一起保留分段差异和解释备注

```python
import pandas as pd

summary = pd.DataFrame(
    [
        {
            "event_id": "A",
            "early_flow_mean": 1.8,
            "mid_flow_mean": 2.8,
            "late_flow_mean": 2.6,
        },
        {
            "event_id": "B",
            "early_flow_mean": 2.4,
            "mid_flow_mean": 2.4,
            "late_flow_mean": 2.4,
        },
    ]
)

summary["overall_mean"] = summary[
    ["early_flow_mean", "mid_flow_mean", "late_flow_mean"]
].mean(axis=1)
summary["mid_minus_early"] = summary["mid_flow_mean"] - summary["early_flow_mean"]
summary["late_minus_mid"] = summary["late_flow_mean"] - summary["mid_flow_mean"]
summary["pattern_note"] = summary.apply(
    lambda row: "mid peak then slight drop"
    if row["mid_minus_early"] > 0 and row["late_minus_mid"] < 0
    else "flat across segments",
    axis=1,
)

print("1) the same overall mean is not enough")
print(summary[["event_id", "overall_mean"]])
print()
print("2) segment-level differences remain")
print(
    summary[
        [
            "event_id",
            "early_flow_mean",
            "mid_flow_mean",
            "late_flow_mean",
            "mid_minus_early",
            "late_minus_mid",
        ]
    ]
)
print()
print("3) one-line pattern interpretation")
print(summary[["event_id", "pattern_note"]])
```

期望输出：

```text
1) the same overall mean is not enough
  event_id  overall_mean
0        A           2.4
1        B           2.4

2) segment-level differences remain
  event_id  early_flow_mean  mid_flow_mean  late_flow_mean  mid_minus_early  late_minus_mid
0        A              1.8            2.8             2.6              1.0            -0.2
1        B              2.4            2.4             2.4              0.0             0.0

3) one-line pattern interpretation
  event_id               pattern_note
0        A  mid peak then slight drop
1        B       flat across segments
```

两个动作的 `overall_mean` 都是 2.4。但看第 2 步时，A 的 `mid_minus_early=1.0`、`late_minus_mid=-0.2`，说明它在中段上升、后段回落；而 B 这两个值都是 0.0，表示区间结构没有变化。第 3 步中的 `pattern_note`，就是把这种差异重新折叠成一句说明。所以，只看平均值，它们像是同一种案例；把区间平均值和区间差异一起看，就能看出它们是不同的动作结构。

这个例子也可以按同样顺序来读。

1. 先看 `overall_mean` 是否相同。
2. 再看三个区间平均值是不是都一样，还是只有某一个区间不同。
3. 最后用一句话写下：为什么“平均值相同但结构不同”的案例在运行解释上很重要。

例如，A 可以概括成 `中段较高、后段略有下降的动作`，B 则可以概括成 `从头到尾几乎保持同一水平的动作`。只有这种一句话的总结能够成立，数字表才真正延伸到结构解释。这里要再次确认的是，并不是说要放弃平均值，而是说如果只留下平均值，结构解释就会停住。因此，即使平均值相同，也应该一起留下区间平均值、分段斜率、峰值时点、下降开始时点等信息。

这种差异，在后面的基准线比较里也同样重要。即使近期区间平均值看起来和平时差不多，只要后段下降模式更强，状态变化就可能已经开始了。因此，读懂 `相同平均值，不同模式`，并不只是多看一个特征的小技巧，而是为后面读取 `近期结构是否和以往不同` 做准备。

如果因为平均值相同，就把两个动作直接归为同一类，就可能漏掉那些实际上后段下降更快的案例。所以，汇总表里应该能看见 `即使平均值相同，结构也可能不同`。这个想法会自然延伸到后面的特征设计、区段表示和基准线比较。

## 来源与参考资料

- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. 它提供了在时间流程里读取信号和模式的视角，因此为“单个平均值无法解释全部结构变化，必须保留区间变化和形状差异”提供了一般依据。 [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- Google for Developers, `Machine Learning Glossary` 中的 `feature engineering`。它把 feature engineering 解释为把原始数据变成更有用的输入表示，因此强化了汇总表不仅要保留平均值，也要保留区间平均值、斜率、时点等结构信息这一点。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- W3C, `PROV-Overview`. provenance framework 说明派生关系和处理步骤应当可解释，因此它强化了一个更高层的框架：除了整体平均值之外，保留下来的区间汇总和派生值也应该是可追溯、可重构的。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08

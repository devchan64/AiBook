# P3-6.5 当特征的单位和尺度不同的时候，应该怎样一起读取和保留

> Section ID: `P3-6.5`
> Version: `v2026.07.24`

做出几个特征之后，很容易又重新陷入一种混乱。`值大的那一列是不是更重要？` `秒和压力单位，可以放在同一张表里吗？` `平均值 200 的列和 0.2 的列，能不能就这样并排比较？` 这里首先需要的，不是去看数字大小，而是先建立一种感觉：要区分单位(unit)、范围(range)、变化幅度、以及相对基准线的变化。

“它们出现在同一张表里”这件事，和“它们应该用同一种大小标准去读”这个判断，并不是同一句话。特征可以有不同的单位、范围和变动宽度；如果不知道这一点，只看数值大小，就很容易把结构读错。

例如，假设在一次自动动作的汇总表里，同时出现了下面这些列。

| 列名 | 示例值 | 含义 |
| --- | ---: | --- |
| `duration_seconds` | 48 | 动作持续时间 |
| `pressure_mean` | 101.2 | 平均压力 |
| `flow_std` | 0.18 | 流量波动性 |
| `late_drop_rate` | -0.42 | 后段下降率 |

这四个值虽然都是数字，但它们并不在描述同一种大小。

- `duration_seconds` 是时间长度。
- `pressure_mean` 是压力水平。
- `flow_std` 是波动幅度。
- `late_drop_rate` 是变化方向和速度。

所以，不能只因为它们都叫“数字”，就读成 `101.2 比 48 更重要` 这样的比较。

## 为什么需要这个区分

在特征设计阶段，这种感觉至少因为下面三点而必要。

| 先要知道的事 | 为什么需要 |
| --- | --- |
| 单位不同 | 因为同样大小的数值，也可能表示完全不同的东西 |
| 范围不同 | 因为有些列本来就在 0 附近波动，而有些列本来就在 100 附近波动 |
| 变化幅度不同 | 因为如果把变化小的列和变化大的列放在同一眼尺上看，容易错过重要差异 |

这并不是说现在就要进入模型计算用的归一化公式。Part 3 在这里的目的，是先建立这样一种感觉：`重要的不是这个数大不大，而是它到底在测什么。`

## 放在同一张表里，不等于用同一种方式去读

在同一张样本表里，当然可以放多个特征。但每一列的阅读方式，仍然可以不同。

| 特征列 | 先怎么读 |
| --- | --- |
| `duration_seconds` | 看它是否比平时更长 |
| `pressure_mean` | 看它和基准线之间的水平差异 |
| `flow_std` | 看波动是不是变大了 |
| `late_drop_rate` | 看后段结构是不是更陡地崩掉了 |

也就是说，比较不是在 `数字和数字之间`，而是在 `承担同样角色的同一列之间`。不是直接拿 `duration_seconds` 和 `pressure_mean` 互相比大小，而是应该拿 `这次的 duration_seconds` 去和“平时的 duration_seconds”比，再拿 `这次的 pressure_mean` 去和“平时的 pressure_mean”比。

## 常见误解

| 误解 | 其实应该重新看什么 |
| --- | --- |
| 值更大的列更重要 | 我是不是在用大小去比较单位和角色都不同的数字？ |
| 0.2 这样的值看起来很小，所以影响也小 | 这列原本是不是就只会在很小范围内变化？ |
| 所有特征都可以用同一种方式去读 | 我有没有把水平、变化、波动性和持续时间区分开？ |

例如，`flow_std = 0.18` 只看数字时可能显得很小，但如果平时值是 `0.03`，那它实际上可能代表了很大的波动增加。相反，`pressure_mean = 101.2` 只看数字似乎很大，但如果平时值是 `101.0`，它的相对变化就可能很小。

## 所以应该先写下什么

在 Part 3 阶段，如果能在每一列特征旁边简短写下下面三样东西，就会安全很多。

| 要写下来的东西 | 示例 |
| --- | --- |
| 这一列的单位或含义 | 秒、压力、变化率、波动性 |
| 这一列展示的结构 | 水平、方向、波动、持续时间 |
| 比较基准 | 是看绝对值本身，还是看相对基准线的差值 |

例如，可以这样写。

| 列名 | 单位/含义 | 结构角色 | 比较方式 |
| --- | --- | --- | --- |
| `duration_seconds` | 秒 | 持续时间 | 是否比平时更长 |
| `pressure_mean` | 压力水平 | 平均水平 | 和基准线相比差异大吗 |
| `flow_std` | 波动性 | 摆动程度 | 是否比平时更抖 |
| `late_drop_rate` | 变化率 | 后段崩塌速度 | 后段斜率是否变得更陡 |

有了这张表，`这是什么数字` 和 `该怎样读它` 就能同时被固定下来。

## 小型检查表

这一节与其用 Python 输出固定的两行，不如先用表固定“应该沿着什么轴读取数值列”。例如，先看下面这张工作表。

| event_id | `duration_seconds` | `pressure_mean` | `flow_std` | `late_drop_rate` |
| --- | ---: | ---: | ---: | ---: |
| A | 48 | 101.2 | 0.18 | -0.42 |
| B | 44 | 100.9 | 0.05 | -0.10 |
| 基准线 | 45 | 101.0 | 0.03 | -0.12 |

只看绝对值时，`pressure_mean` 会显得最大。但如果按相对基准线的变化来读，就会出现另一幅图。

| event_id | `duration_delta` | `pressure_delta` | `flow_std_delta` | `late_drop_delta` |
| --- | ---: | ---: | ---: | ---: |
| A | 3 | 0.2 | 0.15 | -0.30 |
| B | -1 | -0.1 | 0.02 | 0.02 |

这张表里重要的，不是数字绝对值大小，而是每一列承担的角色，以及同一列内部相对基准线的变化。只看第一张表时，`101.2` 可能显得很大，而 `0.18` 可能显得很小；但一旦按相对基准线的变化来读，`flow_std_delta=0.15` 反而可能表示波动大幅增加，而 `pressure_delta=0.2` 可能只是一个很小的水平差异。

| 列名 | 角色 | 先比较的方式 |
| --- | --- | --- |
| `duration_seconds` | 持续时间(duration) | 相对基准线的差异 |
| `pressure_mean` | 水平(level) | 相对基准线的差异 |
| `flow_std` | 波动性(variability) | 相对基准线的差异 |
| `late_drop_rate` | 变化(change) | 相对基准线的差异 |

所以，真正应该先读的不是 `谁的数字更大`，而是 `怎样比较承担同一角色的同一列。`

所以 Part 3 的责任，至少要做到下面这三点。

1. 知道同一张表里可以并排放着含义不同的数字。
2. 能写出每个特征到底是在表示水平、变化、波动性，还是持续时间。
3. 知道比起数字大小本身，`同一列相对基准线的变化` 可能更重要。

因为特征表里的数字并不都在表达同一种大小，所以应先写清单位和角色，再通过同一列相对基准线的变化去读取。这一节与其说是在介绍缩放公式，不如说更接近于：在一张工作表里，应该如何进行 `跨异质尺度的角色感知阅读(role-aware reading across heterogeneous scales)`。


同样的问题也会出现在模型输入里。下面的例子使用同一个 k-NN 模型，但比较两种读法：不做尺度调整直接读取，以及用 `StandardScaler` 把各列调整到可比较尺度后再读取。

问题场景：想确认当单位和范围不同的特征被直接放进 k-NN 时，数值范围大的列可能会更强地牵动邻居判断。

输入(input)：包含持续时间、压力变化、流量波动变化的小型特征表，以及一个要确认的新样本。

期望输出(output)：尺度调整前后的最近 `event_id` 和预测值。

要确认的概念：即使特征在同一张表里，当模型用距离来比较它们时，是否做尺度调整也可能改变邻居和预测。

```python
# 这个例子用来确认距离模型会怎样读取单位和范围不同的特征。
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

features = pd.DataFrame(
    [
        {"event_id": "A", "duration_seconds": 44, "pressure_delta": 0.10, "flow_std_delta": 0.02, "review_needed": 0},
        {"event_id": "B", "duration_seconds": 48, "pressure_delta": 0.20, "flow_std_delta": 0.15, "review_needed": 1},
        {"event_id": "C", "duration_seconds": 43, "pressure_delta": -0.10, "flow_std_delta": 0.01, "review_needed": 0},
        {"event_id": "D", "duration_seconds": 49, "pressure_delta": 0.00, "flow_std_delta": 0.16, "review_needed": 1},
    ]
)
query = pd.DataFrame(
    [{"duration_seconds": 44, "pressure_delta": 0.15, "flow_std_delta": 0.14}]
)
columns = ["duration_seconds", "pressure_delta", "flow_std_delta"]

plain = KNeighborsClassifier(n_neighbors=1).fit(features[columns], features["review_needed"])
scaled = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=1))
scaled.fit(features[columns], features["review_needed"])

plain_neighbor = plain.kneighbors(query, return_distance=False)[0][0]
scaled_query = scaled.named_steps["standardscaler"].transform(query)
scaled_neighbor = scaled.named_steps["kneighborsclassifier"].kneighbors(
    scaled_query, return_distance=False
)[0][0]

print("without scaling nearest_event:", features.iloc[plain_neighbor]["event_id"])
print("without scaling prediction:", int(plain.predict(query)[0]))
print("with scaling nearest_event:", features.iloc[scaled_neighbor]["event_id"])
print("with scaling prediction:", int(scaled.predict(query)[0]))
```

期望输出：

```text
without scaling nearest_event: A
without scaling prediction: 0
with scaling nearest_event: B
with scaling prediction: 1
```

尺度调整前，因为 A 的 `duration_seconds=44` 与查询样本相同，所以它会被选成最近案例。但把压力变化和流量波动变化也调整到可比较尺度后，B 会变成更近的案例。这个输出不是在说 `数值更大的列更重要`，而是在说明：在距离模型里，范围更大的列可能支配计算。所以即使还没有细学模型公式，Part 3 也应该先写下每个特征的单位、范围和比较方式。

因此，特征表不该被理解成“数值大小竞赛表”，而应理解成一种结构：不同测量轴被并排放在一起，并按照各自角色来读取。

## 用一个小图来看

这一节抓住的是：即使不同单位、不同尺度的值放在同一张表里，也应该按列角色去读，并和该列自己的基准线比较。比起数值大小，首先要问的是 `这列到底在测什么。`

--8<-- "assets/part-03/chapter-06/p3-6-5-mermaid-01-zh.mmd"

## 来源与参考资料

- Google for Developers, `Machine Learning Glossary` 中的 `feature`。它把 feature 解释为用于预测的输入变量，因此支持这样一点：比起数字本身大不大，更重要的是它作为输入变量到底在测什么。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- Google for Developers, `Machine Learning Glossary` 中的 `feature engineering`。它解释了把原始数据改造成更适合学习的形式，因此强化了这一节的说明：持续时间、水平、波动性、变化率这样承担不同角色的特征，应当分开读取。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. 它提供了一个一般概念：比较之所以成立，是因为把同一个项目与参考点并排放在一起。因此，它可以支持这里的说明：与其直接把不同特征互相比大小，不如把每一列读成相对基准线的变化。 [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-20

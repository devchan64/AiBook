# P3-6.6 即使列名相同，只要测量方式或单位变了，为什么也可能不是同一个特征

> Section ID: `P3-6.6`
> Version: `v2026.07.11`

在设计特征(feature)时，还有一个很容易被忽略的陷阱。那就是一想到 `列名一样，那应该就是同一个特征吧`。但在真实数据里，即使都叫 `flow_mean`，也可能是传感器版本变了、单位变了，或者计算规则变了。只要发生这种变化，数字虽然还在那里，也很难再说它还是同一个特征。

一个特征是不是“同一个特征”，不能只看列名，而应该连同 `它到底测了什么量、按什么规则、用什么单位做出来` 一起判断。

## 什么情况下，同样的列名并不代表同一个特征

如果只因为列名相同就直接当作同一个特征继续用，那么即使特征的意义已经变了，也很容易被直接放上同一张比较表和同一条基准线。

| 表面上看到的状态 | Part 3 应该先问的问题 |
| --- | --- |
| 列名没变 | 计算规则和单位也没变吗？ |
| 数值分布突然变了 | 是真实变化，还是测量方式变了？ |
| 维护之后数值变了 | 是工艺状态变化，还是传感器定义变化？ |

所以，仅仅因为特征名相同，并不能说明相同的比较结构依然成立。

## 只要什么变了，就可能不再是同一个特征

即使列名相同，只要下面这些内容里有一个发生变化，Part 3 就应该先重新问：`它还是同一个特征吗？`

| 发生变化的东西 | 为什么重要 |
| --- | --- |
| 测量单位 | 因为数值之间的比较本身就变了 |
| 传感器位置或传感器版本 | 因为同一个名字也可能开始更接近另一种物理量 |
| 区间计算规则 | 因为即使同样写成平均值，也可能是在不同区间上求出来的 |
| 运行定义 | 因为即使叫同一个 `正常范围`，背后的标准也可能已经变了 |

这四种变化，都不是首先属于模型技巧问题，而是属于 `现在保留下来的这个特征，到底是什么意思` 的问题。

## 用一个小图来看

| event_id | flow_mean | flow_unit | sensor_version | segment_rule | ops_definition |
| --- | ---: | --- | --- | --- | --- |
| A | 2.4 | L/min | v1 | early-mid-late | normal-band-v1 |
| B | 2.5 | L/min | v1 | early-mid-late | normal-band-v1 |
| C | 41.0 | mL/s | v2 | early-mid-late | normal-band-v1 |
| D | 39.5 | mL/s | v2 | quartile-4bin | normal-band-v2 |

如果看这张表，所有行都叫 `flow_mean`，但实际上已经同时发生了不止一种变化。

1. `A`、`B` 和 `C`、`D` 的单位不同。
2. `C`、`D` 的传感器版本也不同。
3. `D` 的区间计算规则也不同。
4. `D` 的运行定义也不同，因此很难立刻挂到同一条基准线说明里。

所以，如果把这四行当作同一列“没变的特征”来读，那么在谈数字是否相近之前，特征含义本身就已经晃了。也正因为如此，这里最先应该抓住的结论很简单：`相同列名` 并不保证 `相同特征定义`。

```mermaid
--8<-- "assets/part-03/chapter-06/p3-6-6-mermaid-01-zh.mmd"
```

## 所以，这个阶段最先要写下什么

在 Part 3 里，比起立刻进入复杂的校正技术，更重要的是先留下特征定义备注。

| 先要写下来的备注 | 为什么需要 |
| --- | --- |
| 单位(unit) | 因为要先判断绝对数值比较是否成立 |
| 生成规则(rule) | 因为要先确认是不是在同一区间、用同一种计算方式做出来的 |
| 采集版本(version) | 因为要区分传感器或管道版本的变化 |
| 是否可以直接比较 | 因为要判断它能不能立刻被放上同一条基准线 |

这些备注不是为了让说明变长，而是为了挡住 `列名相同` 这种错觉所需要的最低限度结构信息。

## 为什么连基准线比较也会一起被动摇

一旦它不再是同一个特征，Chapter 7 的基准线比较也会立刻被动摇。

| 当前看到的现象 | 实际可能被动摇的是什么 |
| --- | --- |
| 最近值变得比平时更高 | 可能不是工艺变化，而是单位或传感器变化 |
| 维护之后差值一直很大 | 基准线群体和测量定义可能都已经变了 |
| 从某个时点开始波动性变大 | 可能是区间计算规则变了 |

所以，所谓基准线，不只是同一群体之间的比较，还应该是 `同一特征定义` 之间的比较。把这些备注先留下来，才能在说 `模型有问题` 之前，先检查 `是不是混进了不同的特征定义`。

## 小型代码示例

问题情境：确认即使都使用 `flow_mean` 这个列名，只要单位、传感器版本、区间规则、运行定义不同，它们也可能不是同一个特征。

输入(input)：一张特征目录表，其中同时写有 `feature_name`、`unit`、`sensor_version`、`segment_rule`、`ops_definition`

期望输出(output)：即使在同一个列名下，`same_definition_group` 也会分裂开的输出

要确认的概念：特征的同一性，不应只在列名层面判断，而应在包含测量单位和生成规则的定义层面判断

```python
import pandas as pd

feature_catalog = pd.DataFrame(
    [
        {
            "event_id": "A",
            "feature_name": "flow_mean",
            "unit": "L/min",
            "sensor_version": "v1",
            "segment_rule": "early-mid-late",
            "ops_definition": "normal-band-v1",
        },
        {
            "event_id": "B",
            "feature_name": "flow_mean",
            "unit": "L/min",
            "sensor_version": "v1",
            "segment_rule": "early-mid-late",
            "ops_definition": "normal-band-v1",
        },
        {
            "event_id": "C",
            "feature_name": "flow_mean",
            "unit": "mL/s",
            "sensor_version": "v2",
            "segment_rule": "early-mid-late",
            "ops_definition": "normal-band-v1",
        },
        {
            "event_id": "D",
            "feature_name": "flow_mean",
            "unit": "mL/s",
            "sensor_version": "v2",
            "segment_rule": "quartile-4bin",
            "ops_definition": "normal-band-v2",
        },
    ]
)

feature_catalog["same_definition_group"] = (
    feature_catalog["feature_name"]
    + "|"
    + feature_catalog["unit"]
    + "|"
    + feature_catalog["sensor_version"]
    + "|"
    + feature_catalog["segment_rule"]
    + "|"
    + feature_catalog["ops_definition"]
)

definition_groups = (
    feature_catalog.groupby("same_definition_group", as_index=False)
    .agg(
        event_count=("event_id", "count"),
        event_ids=("event_id", lambda values: ",".join(values)),
    )
)

print("1) same column name, different definition notes")
print(
    feature_catalog[
        [
            "event_id",
            "feature_name",
            "unit",
            "sensor_version",
            "segment_rule",
            "ops_definition",
        ]
    ]
)
print()
print("2) rows that can be treated as the same definition group")
print(definition_groups)
```

期望输出：

```text
1) same column name, different definition notes
  event_id feature_name   unit sensor_version    segment_rule ops_definition
0        A    flow_mean  L/min             v1  early-mid-late  normal-band-v1
1        B    flow_mean  L/min             v1  early-mid-late  normal-band-v1
2        C    flow_mean   mL/s             v2  early-mid-late  normal-band-v1
3        D    flow_mean   mL/s             v2   quartile-4bin  normal-band-v2

2) rows that can be treated as the same definition group
                                same_definition_group  event_count event_ids
0  flow_mean|L/min|v1|early-mid-late|normal-band-v1            2       A,B
1   flow_mean|mL/s|v2|early-mid-late|normal-band-v1            1         C
2    flow_mean|mL/s|v2|quartile-4bin|normal-band-v2            1         D
```

这个例子的目的，不是再去计算一个新特征，而是先确认：`即使列名一样，究竟哪些行还能被归到同一个定义组里？` 第 1 步里，我们看到四行都叫 `flow_mean`，但定义备注已经不同；第 2 步里，我们看到真正还能被归为同一定义的，只有 `A,B`，而 `C`、`D` 都必须各自单独留下。也就是说，这一节重要的并不是内部拼出来的 key 字符串本身，而是先把哪些行还能放进同一条基准线、同一张比较表里分开。

这里最后要检查的三件事是：单位和计算规则有没有被写下来；版本变化或传感器变化有没有被区分出来；那些不能混进同一条基准线和同一分组里的定义差异，有没有被标记出来。只有这三点一起成立，特征表才不再只是数字集合，而会变成一张带着“可比较定义”的结构。检查当前特征表是不是只在比较“真正意义相同的列”，正是这一节的中心。

如果测量单位、传感器版本、计算规则发生了变化，那么同一个列名也可能已经不是同一个特征，所以在 Part 3 里，应该先检查特征定义是否一致，再去看数字。这一节与其说是在讲列名管理技巧，不如说更接近于：应该怎样识别 `特征定义身份(feature-definition identity)`。


因此，特征同一性不该被读成“只有一行列名”，而应被读成一个定义包：它包含了“按什么规则、什么版本做出了什么”。

## 来源与参考资料

- W3C, `PROV-Overview`. 它提供了一个一般框架：通过 provenance information 追踪数据是经过什么过程、什么版本生成的，因此强化了这一点：为了保持可比性，特征除了名称，还应保留生成规则和版本。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08
- Google for Developers, `Machine Learning Glossary` 中的 `feature engineering`。它说明特征不是未经处理的原始值，而是经过选择性变换的结果，因此支持这一节的核心：只要单位或计算规则变了，即使列名一样，也很难再说它还是同一个特征定义。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-08

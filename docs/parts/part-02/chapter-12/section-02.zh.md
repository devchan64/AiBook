# P2-12.2 选择、过滤与聚合

> Section ID: `P2-12.2`
> Version: `v2026.07.26`

在 P2-12.1 中，我们把 Pandas `DataFrame` 看作带有行(row)、列(column)与索引(index)的表格型数据结构。接下来会自然出现另一个问题。

拿到一张表，并不意味着需要的信息已经直接摆在眼前。实际工作中，人们会不断做下面这些事。

- 只挑出某些列。
- 只看某些行。
- 只保留满足条件的行。
- 查看数值列的平均值或数量。
- 按类别拆开后再做总结。

在 Pandas 中，选择(selection)、过滤(filtering)、聚合(aggregation)处理的就是这条流程。

本节说明 `Series`、过滤(filtering)、聚合(aggregation)、`groupby`、`loc`、`iloc` 的基本区分。`DataFrame` 本身的代表性说明放在 P2-12.1 与[DataFrame 词条](/AiBook/zh/reference/concept-glossary-pinyin/d.zh/#dataframe)中，这里关注的是：从那张表里读什么、留下什么、概括什么。

## 核心判断标准：选择、过滤与聚合

- 你可以说明选择一列与选择多列时，结果会有什么不同。
- 你可以说明 `loc` 按标签(label)读取，`iloc` 按位置(position)读取。
- 你可以说明布尔(Boolean)条件是如何用来筛选行的。
- 你可以说明聚合是把原来的整张表变成更小的总结值的过程。
- 你可以把 `groupby` 说明成先把同一类别归在一起，再对每组做总结的方法。

## 三个判断标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 列选择与行过滤的区别 | 它能避免把“要读什么”和“要留下什么”混在一起。 | 理解前者是在选要读的内容，后者是在选要留下的内容。 |
| 为什么要区分 `loc` 与 `iloc` | 它能避免把按标签读取和按位置读取混淆。 | 理解 `loc` 用标签，`iloc` 用位置。 |
| `groupby` 在做什么 | 它能把“整张表如何变成按类别总结”的流程说明白。 | 理解为先把同一类别归在一起，再计算总结值。 |

| 术语 | 本节先固定的含义 |
| --- | --- |
| Series | 带有索引的一维值列。 |
| filtering | 只保留满足条件的行的一种选择方式。 |
| aggregation | 把很多值变成平均值、总和、数量等更小总结的过程。 |
| `groupby` | 先把同一类别归在一起，再对每组计算总结的方法。 |
| `loc` / `iloc` | 分别按标签、按位置选择行与列的工具。 |

本节之后的衔接也很简单。

- 在 `P2-12.3` 中，我们会看到这里做过选择和总结的表，如何接到真实的数据集准备与防止泄漏的语境里。
- 在后面的 Pandas 实践与模型输入准备部分，同一个问题会反复出现为：`哪些列该留下，哪些总结该做出来？`

## 先固定一个示例表

本节会一直使用下面这个小表。

问题场景：为了把选择、过滤、聚合的例子放在同一张表里连续观察，我们需要先准备一个作为基准的小型 `DataFrame`。
输入(input)：包含姓名、分数、是否通过、地区的四列。
预期输出(output)：输出一张包含四位学生的示例表。
要确认的概念：后面所有选择与过滤，都会在同一张表上只改变问题而不改变基准。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Kim", "Park", "Lee", "Choi"],
        "score": [82, 45, 90, 73],
        "passed": ["yes", "no", "yes", "yes"],
        "region": ["Seoul", "Busan", "Seoul", "Busan"],
    }
)

print(df)
```

输出可以这样读。

```text
   name  score passed region
0   Kim     82    yes  Seoul
1  Park     45     no  Busan
2   Lee     90    yes  Seoul
3  Choi     73    yes  Busan
```

我们先从“看整张表”开始，但很快就会转向“哪一列？”“哪一行？”“什么条件？”这些问题。

如果用图示来看，本节流程如下。

```mermaid
--8<-- "assets/part-02/chapter-12/table-reading-flow-zh.mmd"
```

## 选一列时会得到 Series

在 Pandas 中，可以只挑出一列。

问题场景：你想确认，当只取出分数列时，结果会从整张表变成什么形态。
输入(input)：`df["score"]`。
预期输出(output)：只包含分数的一维 `Series`。
要确认的概念：选择一列时，通常返回的是 `Series`，而不是 `DataFrame`。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df["score"])
```

输出大致如下。

```text
0    82
1    45
2    90
3    73
Name: score, dtype: int64
```

这里最重要的是：结果不是 `DataFrame`，而是 `Series`。`Series` 不是一行表，更适合读成“带索引的一维值列”。

这里先记住下面这组差别就够了。

- `df["score"]`：取出一列。结果通常是 `Series`。
- `df[["name", "score"]]`：选择多列。结果是 `DataFrame`。

例如：

问题场景：你想比较一下，把姓名与分数一起保留时，结果形态会和单列选择有什么不同。
输入(input)：`df[["name", "score"]]`。
预期输出(output)：保留两列的小型 `DataFrame`。
要确认的概念：选择多列时，会保留下原表结构的一部分。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df[["name", "score"]])
```

输出仍然是表格形状。

```text
   name  score
0   Kim     82
1  Park     45
2   Lee     90
3  Choi     73
```

也就是说，选一列时更像是在读一个值列；选多列时则仍然保留着“从原表切下一部分来观察”的感觉。

同样的差别放到表里会更清楚。

| 代码 | 结果形态 | 在问什么 |
| --- | --- | --- |
| `df["score"]` | `Series` | 我是不是只想看分数这一列的值？ |
| `df[["name", "score"]]` | `DataFrame` | 我是不是想把姓名与分数放在一起比较？ |

再做一个小检查也很有用。

问题场景：你想直接确认，选一列与选多列返回的是不同类型的对象。
输入(input)：`df["score"]` 与 `df[["name", "score"]]`。
预期输出(output)：两行类型名 `Series` 与 `DataFrame`。
要确认的概念：看起来相似的选择，返回对象也可能不同。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(type(df["score"]).__name__)
print(type(df[["name", "score"]]).__name__)
```

输出大致会这样读。

```text
Series
DataFrame
```

## `loc` 按标签读取，`iloc` 按位置读取

Pandas 官方文档把 `.loc` 说明为基于标签(label-based)的选择，把 `.iloc` 说明为基于整数位置(integer position-based)的选择。

这里先这样区分。

- `loc`：看标签来选。
- `iloc`：看它是第几个位置来选。

例如，当当前默认索引是 `0, 1, 2, 3` 时：

问题场景：在默认数字索引下，`loc` 与 `iloc` 很容易看起来差不多，从而忽略差别。
输入(input)：`df.loc[1]`、`df.iloc[1]`。
预期输出(output)：两者都像是在指向第二位学生的那一行。
要确认的概念：即使当前结果看起来一样，依据仍然分别是标签与位置。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df.loc[1])
print(df.iloc[1])
```

两者都可能看起来在指向第二行。这只是因为当前索引标签是数字，而位置也正好用数字计数。

但如果把索引改成名字，差别就会更明显。

问题场景：你想更清楚地看到按标签选择与按位置选择之间的差异。
输入(input)：把 `name` 设为索引后的 `named`，以及对应的 `loc` / `iloc` 调用。
预期输出(output)：分别选出标签为 `Lee` 的行，以及第三个位置的行。
要确认的概念：`loc` 看名字标签，`iloc` 看顺序位置。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
named = df.set_index("name")

print(named.loc["Lee"])
print(named.iloc[2])
```

这时：

- `named.loc["Lee"]` 会查找标签 `Lee`。
- `named.iloc[2]` 会查找第三个位置的行。

这个区分非常重要，因为按名字选择与按顺序选择，本来就是两种不同的读表动作。

用一个小表整理如下。

| 代码 | 依据 | 含义 |
| --- | --- | --- |
| `df.loc[1]` | 标签 | 索引标签为 1 的那一行 |
| `df.iloc[1]` | 位置 | 第二个位置上的那一行 |
| `named.loc["Lee"]` | 标签 | 名字为 `Lee` 的那一行 |
| `named.iloc[2]` | 位置 | 第三个位置上的那一行 |

## 条件过滤是在保留或丢弃行

读表时最常见的事情之一，就是只留下满足条件的行。

问题场景：你想只保留分数在 80 分以上的学生。
输入(input)：应用条件 `df["score"] >= 80` 后的表。
预期输出(output)：只剩下 Kim 与 Lee 的局部表。
要确认的概念：条件过滤并不是修改行里的值，而是在选择哪些行可以留下。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df[df["score"] >= 80])
```

输出大致如下。

```text
  name  score passed region
0  Kim     82    yes  Seoul
2  Lee     90    yes  Seoul
```

这段代码可以分两步来读。

1. `df["score"] >= 80` 为每一行产生 `True` 或 `False`。
2. 只保留结果为 `True` 的行。

如果直接看中间结果，会更清楚。

问题场景：你想先看到过滤在内部生成了怎样的 `True` / `False` 列表。
输入(input)：由 `df["score"] >= 80` 生成的 `mask`。
预期输出(output)：显示每一行是否满足条件的布尔 `Series`。
要确认的概念：过滤会先形成逐行判断结果，然后再只保留 `True` 的行。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
mask = df["score"] >= 80
print(mask)
```

```text
0     True
1    False
2     True
3    False
Name: score, dtype: bool
```

这种布尔结果常被称作 `mask`。把过滤读成“向每一行提问，只保留回答是(True)的行”，会更容易理解。

条件也可以多个一起使用。

问题场景：你想只保留同时满足分数条件与地区条件的行。
输入(input)：分数至少 70 且 `region == "Busan"` 的复合条件。
预期输出(output)：只剩下同时满足两个条件的 Choi 行。
要确认的概念：布尔条件可以通过 `&` 等运算符组合起来。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df[(df["score"] >= 70) & (df["region"] == "Busan")])
```

这段代码会只保留分数在 70 以上并且地区是 Busan 的行。

把过滤前后放到表里，可以这样读。

| 步骤 | 留下的行 |
| --- | --- |
| 原始表 | Kim, Park, Lee, Choi |
| `df["score"] >= 80` | Kim, Lee |
| `(df["score"] >= 70) & (df["region"] == "Busan")` | Choi |

所以，过滤比起“改变值”，更接近于“决定留下哪些行”。

## 选择与过滤问的是不同的问题

刚开始学习时，选择与过滤看起来可能很像。但它们提出的问题并不一样。

| 动作 | 问题 |
| --- | --- |
| 列选择 | 我想看哪些变量？ |
| 行选择 | 我想看哪个位置、哪个标签对应的案例？ |
| 条件过滤 | 我想留下哪些满足条件的案例？ |

例如：

问题场景：你想一次比较列选择、单行选择、条件过滤这三种动作，如何以不同方式缩小同一张表。
输入(input)：`df[["name", "score"]]`、`df.loc[2]`、`df[df["passed"] == "yes"]`。
预期输出(output)：分别得到列数减少的表、单独一行、满足条件的多行。
要确认的概念：即使都是“把表缩小”，结果形态也会随着问题不同而变化。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df[["name", "score"]])
print(df.loc[2])
print(df[df["passed"] == "yes"])
```

这三段代码都在缩小表，但缩小的依据并不相同。

- 第一段是在减少列。
- 第二段是在点出一行。
- 第三段是在保留满足条件的多行。

必须把这些差别区分清楚，这样以后代码变长时，才不会失去对它在做什么的判断。

如果把同一个问题换成三种方式读取，会更明显。

问题场景：你想看同一份数据中，列选择、行选择、过滤后再选列是如何衔接的。
输入(input)：三种不同的 Pandas 选择代码。
预期输出(output)：根据目的不同，被缩到不同范围的结果。
要确认的概念：Pandas 代码经常把一个问题拆成更小的步骤，再逐步缩小表的范围。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df[["name", "score"]])
print(df.loc[2])
print(df[df["passed"] == "yes"][["name", "score"]])
```

这三行分别展示的是：

- 通过减少列来看的表
- 作为单一案例抽出来看的一行
- 先留下满足条件的案例，再只看需要的列的表

## 聚合会把表变成更小的总结

聚合(aggregation)是把原来的表转成总结值的过程。

例如：

问题场景：你想把整个分数列总结成几个数字来观察。
输入(input)：对 `score` 列做平均值、最大值、数量聚合。
预期输出(output)：三个用于总结分数分布的数字。
要确认的概念：聚合会把很多行压缩成更小的总结结果。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df["score"].mean())
print(df["score"].max())
print(df["score"].count())
```

每个输出分别回答下面的问题。

- 平均值(mean)：分数的中心大概在哪里？
- 最大值(max)：最大的值是什么？
- 数量(count)：一共有多少个值？

聚合的核心在于：不是继续原样看整张表，而是用几个数字把它概括起来。

在本节里，我们对聚合的理解比“计算统计量”更宽一点。只要把它理解成`把很多行压缩成更少结果`就够了。

再看一个很小的例子会更容易明白。

问题场景：如果只单独输出一个平均值，就更容易看清聚合是如何让整张表变简单的。
输入(input)：`df["score"].mean()`。
预期输出(output)：一个分数平均值。
要确认的概念：聚合结果不能替代整张表，但能快速显示中心。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df["score"].mean())
```

```text
72.5
```

这一个数字无法替代整张表，但在快速查看中心值时很有用。

如果把多个聚合放在一起，也可以这样来读。

问题场景：你想一次性检查平均值、最大值、数量。
输入(input)：`df["score"].agg(["mean", "max", "count"])`。
预期输出(output)：把多个聚合结果打包在一起的小型总结输出。
要确认的概念：同一列也可以同时按多个聚合标准来读取。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df["score"].agg(["mean", "max", "count"]))
```

输出大致可能如下。

```text
mean     72.5
max      90.0
count     4.0
dtype: float64
```

这个结果可以理解成：它像一张小表，用多种方式总结同一个 `score` 列。

## `groupby` 是先把同类归在一起再做总结

Pandas 官方文档把 `groupby` 说明为：按某种标准把数据拆开，对每组应用函数，再把结果组合起来。这里先把 `groupby` 理解成：先把值相同的行归为一组，再对每组做聚合，就足够了。

例如，如果你想看按地区划分的平均分：

问题场景：你想把问题单位从“每个学生的分数”改成“每个地区的平均分”。
输入(input)：按 `region` 分组并计算 `score` 平均值的 `groupby` 代码。
预期输出(output)：Busan 与 Seoul 的平均分分别出现的总结结果。
要确认的概念：`groupby` 会先把单独的行变成按类别组织的分组，然后再对每组做聚合。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
print(df.groupby("region")["score"].mean())
```

输出大致可能如下。

```text
region
Busan    59.0
Seoul    86.0
Name: score, dtype: float64
```

这段代码可以这样读。

1. 先把 `region` 值相同的行放在一起。
2. 在每一组里只看 `score` 这一列。
3. 计算每一组的平均值。

所以 `groupby` 不只是单纯地给出一个平均值，而是在说明：`这个平均值是按什么标准分开来看得到的？`

如果把原表与 `groupby` 结果并排看，变化会更明显。

| 原表中的问题 | `groupby` 之后的问题 |
| --- | --- |
| 每个学生的分数是多少？ | 每个地区的平均分是多少？ |
| 一共有多少行？ | 一共有多少个类别？ |
| 看单个案例 | 看类别总结 |

这一点很重要。`groupby` 主要不是排序功能，而更接近于一种改变`读取单位`的功能：把单位从单独的行变成按类别组织的组。

读表时，一行并不一定天然就是一个完整案例。比如在动作进行过程中记录下来的原始日志里，可能需要多行合在一起才构成一次动作记录。这时，更自然的做法往往是先按动作标识列分组，再在组内总结时长、区间平均值、最后一个值，从而重新做出一个动作级别的表。

| event_id | elapsed_seconds | progress_fraction | signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 0.0 | 0.00 | 0.8 |
| A-01 | 1.0 | 0.20 | 1.4 |
| A-01 | 2.0 | 0.40 | 1.9 |
| B-02 | 0.0 | 0.00 | 0.7 |
| B-02 | 1.0 | 0.25 | 1.3 |
| B-02 | 2.0 | 0.50 | 1.5 |

| event_id | total_duration_seconds | signal_a_mean | end_signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 2.0 | 1.37 | 1.9 |
| B-02 | 2.0 | 1.17 | 1.5 |

问题场景：你想把跨多行记录的原始日志重新变成按动作单位总结的表。
输入(input)：按 `event_id` 分组，再计算时间长度与传感器值总结的代码。
预期输出(output)：每个 `event_id` 只剩一行的总结 `DataFrame`。
要确认的概念：`groupby` 不只是把同类归在一起，也是在让多行重新被读成一个案例。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
log_df = pd.DataFrame(
    {
        "event_id": ["A-01", "A-01", "A-01", "B-02", "B-02", "B-02"],
        "elapsed_seconds": [0.0, 1.0, 2.0, 0.0, 1.0, 2.0],
        "progress_fraction": [0.00, 0.20, 0.40, 0.00, 0.25, 0.50],
        "signal_a": [0.8, 1.4, 1.9, 0.7, 1.3, 1.5],
    }
)

summary = (
    log_df.groupby("event_id")
    .agg(
        total_duration_seconds=("elapsed_seconds", "max"),
        signal_a_mean=("signal_a", "mean"),
        end_signal_a=("signal_a", "last"),
    )
    .reset_index()
)

print(summary)
```

输出可以这样读。

```text
  event_id  total_duration_seconds  signal_a_mean  end_signal_a
0     A-01                     2.0       1.366667           1.9
1     B-02                     2.0       1.166667           1.5
```

## 改变阈值时，过滤和聚合会一起移动

前面的小表是为了阅读 Pandas 语法而准备的说明型例子。但在真实表中，需要确认条件值改变时，留下的行和聚合结果是否会一起变化。

输入文件是 [`student-progress-samples.csv`](/AiBook/assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview }。一行表示一名学生的学习记录，核心列是 `region`、`study_hours`、`absences`、`practice_quizzes`、`score`、`passed`。这里通过改变 `pass_threshold` 和 `focus_region`，观察哪些行会留下，以及按地区汇总的结果怎样变化。

问题场景：想确认分数阈值和地区条件改变时，过滤结果与地区摘要是否会一起改变。
输入(input)：36 行学生学习进度 CSV、`pass_threshold`、`focus_region`。
期望输出(output)：满足条件的行列表、按地区的平均分、超过阈值的学生数量。
要确认的概念：条件过滤和 `groupby` 聚合不是为了确认固定答案，而是观察基准值改变时留下的行和摘要如何移动。

```python
# 这个例子在 DataFrame 中选择列、行和条件，并聚合分数数据。
from pathlib import Path
import pandas as pd

csv_path = Path("docs/assets/part-02/chapter-12/student-progress-samples.csv")
df = pd.read_csv(csv_path)

pass_threshold = 75
focus_region = "Busan"

selected = df.loc[
    (df["score"] >= pass_threshold) & (df["region"] == focus_region),
    ["student_id", "region", "score", "passed"],
]

summary = (
    df.assign(over_threshold=df["score"] >= pass_threshold)
    .groupby("region")
    .agg(
        sample_count=("student_id", "count"),
        mean_score=("score", "mean"),
        over_threshold_count=("over_threshold", "sum"),
        mean_absences=("absences", "mean"),
    )
    .round(2)
)

print(selected)
print(summary)
```

同样的代码也可以通过 [`p2_12_2_filter_aggregate_threshold.py`](/AiBook/assets/part-02/chapter-12/p2_12_2_filter_aggregate_threshold.py) 执行。把 `pass_threshold` 改成 `70`、`75`、`80` 时，超过阈值的学生数量会改变；把 `focus_region` 改成其他地区时，被选中的行列表也会改变。

## 如果把读表流程画成图

选择、过滤、聚合大多会连成下面这样的流程。

```mermaid
--8<-- "assets/part-02/chapter-12/table-processing-flow-zh.mmd"
```

在真实工作里，这个顺序不一定总是固定的。即便如此，`不要原封不动地抱着整张表，而是根据问题不断缩小并总结`这条流程仍然重要。

## 用案例来看

### 案例 1. 想重新查看不及格学生的成绩表

假设一位老师在看成绩表，想确认`谁不及格了`、`是否要重新只看不及格学生的分数与地区`、`各地区平均分如何`。人可以在脑中快速浏览整张表，再回头只看需要的部分；但在数据工作里，这个过程必须明确写成选择、过滤与聚合。

先通过 `passed` 列只保留不及格学生，就等于决定了要看哪些行。接着再只选 `name` 与 `score`，就等于决定了要读什么。最后调用 `groupby("region")["score"].mean()`，就把单个学生表压缩成按地区组织的总结。

这个案例一次性展示出三种动作的差别。列选择决定的是`看哪些变量`，行选择与过滤决定的是`留下哪些案例`，聚合决定的是`整张表该用什么总结值来表示`。处理表格并不只是背代码，而更接近于把问题拆成更小的步骤。

所以即使 Pandas 代码很短，也必须连同问题结构一起读。同样一张成绩表，`看一个学生`、`看满足条件的多个学生`、`看按类别划分的平均值`是不同的读法。只有把这个差别区分开，后面做数据集准备与模型输入构造时才不会混乱。

## 检查清单

- 你能说明选择一列与选择多列的差别吗？
- 你能说出 `loc` 与 `iloc` 分别按什么标准选择吗？
- 你能说明布尔条件是如何用来保留或丢弃行的吗？
- 你能说明为什么需要平均值、数量、最大值这样的聚合吗？
- 你能把 `groupby` 解释成“先分组，再总结”的流程吗？
- 你能说明单列选择常读成 `Series`，多列选择常读成 `DataFrame` 吗？

## 来源与参考资料

- pandas Developers, [Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation，确认日期：2026-07-20。用于确认 column selection、`loc`/`iloc`、boolean indexing 和 row filtering。
- pandas Developers, [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation，确认日期：2026-07-20。作为用 split-apply-combine flow 说明 `groupby` 的依据。
- pandas Developers, [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation，确认日期：2026-07-20。用于确认 DataFrame creation、selection、summary statistics 和基本 table manipulation 示例。

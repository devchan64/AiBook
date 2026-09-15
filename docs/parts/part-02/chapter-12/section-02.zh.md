# P2-12.2 选择、筛选与聚合

> Section ID: `P2-12.2`
> Version: `v2026.09.15`

## 学生成绩表

建立一张包含四名学生的姓名、分数、通过状态和地区的表。每名学生占一行，可以根据分数和地区选择行或计算平均值。

```python
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

输出如下：

```text
   name  score passed region
0   Kim     82    yes  Seoul
1  Park     45     no  Busan
2   Lee     90    yes  Seoul
3  Choi     73    yes  Busan
```

```mermaid
--8<-- "assets/part-02/chapter-12/table-reading-flow-zh.mmd"
```

## Series 与 DataFrame

`df["score"]` 将分数列返回为 `Series`，即带有索引的一维值集合。

```python
print(df["score"])
```

输出形式如下：

```text
0    82
1    45
2    90
3    73
Name: score, dtype: int64
```

结果是 `Series`，而不是 `DataFrame`。Series 是带有索引的一维值列，不应理解为只有一行的表。

```python
print(df[["name", "score"]])
```

结果是包含姓名和分数的四行两列 DataFrame。像 `df[["score"]]` 一样传入只含一个列名的列表，会保留四行一列的 DataFrame。

```text
   name  score
0   Kim     82
1  Park     45
2   Lee     90
3  Choi     73
```

```python
print(type(df["score"]).__name__)
print(type(df[["name", "score"]]).__name__)
```

输出如下：

```text
Series
DataFrame
```

## 标签选择与位置选择

Pandas 官方文档将 `.loc` 说明为基于标签的选择，将 `.iloc` 说明为基于整数位置的选择。

```python
print(df.loc[1])
print(df.iloc[1])
```

两条语句都输出 Park 所在的行，因为当前标签 1 与第二个位置指向同一行。

把索引改为姓名后，区别会更加明显。

```python
named = df.set_index("name")

print(named.loc["Lee"])
print(named.iloc[2])
```

此时：

- `named.loc["Lee"]` 查找标签 `Lee`。
- `named.iloc[2]` 按位置选择第三行。

## 切片终点与行顺序

`.loc` 的标签切片包含终点标签，`.iloc` 的位置切片不包含终点位置。在当前默认索引上比较两种选择，就能看到区别。

```python
print(df.loc[1:2, "name"].tolist())
print(df.iloc[1:2]["name"].tolist())

ranked = df.sort_values("score", ascending=False)
print(ranked.index.tolist())
print(ranked.loc[0, "name"])
print(ranked.iloc[0]["name"])
```

```text
['Park', 'Lee']
['Park']
[2, 0, 3, 1]
Kim
Lee
```

排序改变行的位置，但保留原有标签。因此第一个位置是 Lee，标签 0 仍指向 Kim。`reset_index(drop=True)` 会用新的位置编号作为标签；如果还需要学生标识，应将其保存在单独的列中。

## 按条件选择行

选择分数不低于 80 的学生，会留下 Kim 和 Lee 的行。原始分数不会改变。

```python
print(df[df["score"] >= 80])
```

输出形式如下：

```text
  name  score passed region
0  Kim     82    yes  Seoul
2  Lee     90    yes  Seoul
```

这个表达式可以分两步理解：

1. `df["score"] >= 80` 为每行生成 `True` 或 `False`。
2. 只保留标记为 `True` 的行。

可以直接查看中间结果：

```python
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

这样的布尔结果通常称为掩码。筛选可以理解为向每一行提出一个问题，只留下回答为 True 的行。

用 `&` 结合分数不低于 70 和地区为 Busan 的条件，只会留下 Choi。每个条件都需要用括号包围。

```python
print(df[(df["score"] >= 70) & (df["region"] == "Busan")])
```

这段代码选择分数不低于 70 且地区为 Busan 的行。 逐行组合条件时，使用 `&`（且）或 `|`（或）。Python 的 `and`、`or` 会尝试把整个 Series 判断为单一布尔值，因此不能用于此处。

## 按条件修改值

筛选用于选择行，赋值用于修改所选位置的值。若要保留原表，同时给低于 60 分的学生加 5 分，应先复制表，再通过 `.loc[行条件, 列]` 赋值。

```python
adjusted = df.copy()
low = adjusted["score"] < 60
adjusted.loc[low, "score"] = adjusted.loc[low, "score"] + 5
print(df["score"].tolist())
print(adjusted["score"].tolist())
```

```text
[82, 45, 90, 73]
[82, 50, 90, 73]
```

不要用 `df[条件]["score"] = ...` 这样的连锁赋值修改原表。尤其在 pandas 3 的写时复制机制下，这种写法不会改变原表。应在一次 `.loc` 赋值中明确要修改的表和位置。需要把赋值与前面只读取数据的 `df.iloc[1:2]["name"]` 区分开。

## 平均值、最大值与数量

聚合把多个值归纳为摘要值。分数 `[82, 45, 90, 73]` 的平均值为 72.5，最大值为 90，值的数量为 4。

```python
print(df["score"].mean())
print(df["score"].max())
print(df["score"].count())
```

向 `agg` 传入聚合名称列表，可以一次汇总三个结果。`count` 只统计非缺失值。

```python
print(df["score"].agg(["mean", "max", "count"]))
```

输出形式如下：

```text
mean     72.5
max      90.0
count     4.0
Name: score, dtype: float64
```

这个结果可以看作对 `score` 一列进行多种汇总后形成的小表。

## 按地区计算平均分

Pandas 官方文档将 `groupby` 解释为按标准拆分数据、对各组应用函数、再合并结果。计算地区平均分时，需要把 `region` 值相同的行归为一组。

Busan 的平均分为 Park 的 45 分与 Choi 的 73 分的平均值 59；Seoul 的平均分为 Kim 的 82 分与 Lee 的 90 分的平均值 86。

```python
print(df.groupby("region")["score"].mean())
```

输出形式如下：

```text
region
Busan    59.0
Seoul    86.0
Name: score, dtype: float64
```

计算过程如下：

1. 将 `region` 值相同的行分组。
2. 在每组中选择 `score` 列。
3. 计算各组平均值。

## 缺失值与聚合的分母

如果 Park 的分数尚未录入，Busan 仍有两名学生，但只有 Choi 的 73 分这一个已观测分数。`size` 统计行数，`count` 统计非缺失值数量。平均值默认也排除缺失值。 `Float64` 是可以保存缺失值 `pd.NA` 的 Pandas 浮点类型。转换为此类型，是为了在同一列中区分数值与尚未录入的值。

```python
missing = df.copy()
missing["score"] = missing["score"].astype("Float64")
missing.loc[1, "score"] = pd.NA
print(missing.groupby("region")["score"].agg(["size", "count", "mean"]))
```

```text
        size  count  mean
region
Busan      2      1  73.0
Seoul      2      2  86.0
```

Busan 的平均值 73 并不是观测到两名学生分数后的平均值。用 0 填充缺失值，会使平均值变为 `(0 + 73) / 2 = 36.5`，相当于把尚未录入解释成 0 分。在聚合值旁同时列出总行数和已观测值数量，有助于确认汇总依据。

## 按动作汇总传感器记录

动作 A-01 和 B-02 分别在三个时刻接受测量。按动作分组后，可以把最后记录时刻、平均信号和最后观测信号放在每个动作对应的一行中。

| action_id | elapsed_seconds | progress_fraction | signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 0.0 | 0.00 | 0.8 |
| A-01 | 1.0 | 0.20 | 1.4 |
| A-01 | 2.0 | 0.40 | 1.9 |
| B-02 | 0.0 | 0.00 | 0.7 |
| B-02 | 1.0 | 0.25 | 1.3 |
| B-02 | 2.0 | 0.50 | 1.5 |

| action_id | last_recorded_seconds | signal_a_mean | last_recorded_signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 2.0 | 1.37 | 1.9 |
| B-02 | 2.0 | 1.17 | 1.5 |

```python
log_df = pd.DataFrame(
    {
        "action_id": ["A-01", "A-01", "A-01", "B-02", "B-02", "B-02"],
        "elapsed_seconds": [0.0, 1.0, 2.0, 0.0, 1.0, 2.0],
        "progress_fraction": [0.00, 0.20, 0.40, 0.00, 0.25, 0.50],
        "signal_a": [0.8, 1.4, 1.9, 0.7, 1.3, 1.5],
    }
)

summary = (
    log_df.sort_values(["action_id", "elapsed_seconds"]).groupby("action_id")
    .agg(
        last_recorded_seconds=("elapsed_seconds", "max"),
        signal_a_mean=("signal_a", "mean"),
        last_recorded_signal_a=("signal_a", "last"),
    )
    .reset_index()
)

print(summary.round(2).to_string(index=False))
```

输出如下：

```text
action_id  last_recorded_seconds  signal_a_mean  last_recorded_signal_a
    A-01                    2.0           1.37                     1.9
    B-02                    2.0           1.17                     1.5
```

按经过时间排序后，`last` 在此例中返回最晚记录的信号。默认情况下，`last` 跳过缺失值，因此最后时刻的信号若缺失，可能返回更早的值。不排序时，它选择的是当前行顺序中最后一个非缺失值，而不一定是时间上最晚的值。两个动作的最后记录均在 2 秒，但进度分别为 0.40 和 0.50。因此，这代表最后观测时刻，而不是整个动作的完成时间。

## 案例：改变阈值与地区

输入文件为 [`student-progress-samples.csv`](/AiBook/assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview }。一行代表一名学生的学习记录，核心列为 `region`、`study_hours`、`absences`、`practice_quizzes`、`score` 和 `passed`。应用 75 分阈值与 Busan 地区条件后，会选出 S010、S013、S016、S018 四名学生。

```python
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

也可以用文件运行相同的计算。

[p2_12_2_filter_aggregate_threshold.py](/AiBook/assets/part-02/chapter-12/p2_12_2_filter_aggregate_threshold.py)

```bash
python docs/assets/part-02/chapter-12/p2_12_2_filter_aggregate_threshold.py
```

将 `pass_threshold` 改为 `70`、`75` 或 `80`，达到阈值的人数会变化；将 `focus_region` 改为其他地区，所选行的列表会变化。

```mermaid
--8<-- "assets/part-02/chapter-12/table-processing-flow-zh.mmd"
```

把分数阈值提高到 80 后，Busan 选择结果中的 S016 因为只有 77 分而被排除，剩下三名学生。地区聚合使用完整的 `df`，而不是 `selected`，因此平均分和学生人数保持不变，只有达标人数改变。只把 `focus_region` 改为 Seoul，会改变所选学生列表，但地区聚合完全不变。

CSV 中的 `passed` 是已保存的通过状态。改变 `pass_threshold` 并不会重新计算该列，因此不能把它等同于是否达到当前阈值。

## 检查清单

- 能否解释选择一列与选择多列的区别？
- 能否说明 `loc` 和 `iloc` 分别依据什么选择？
- 能否解释布尔条件如何保留或舍弃行？
- 能否解释为什么需要平均值、数量、最大值等聚合？
- 能否把 `groupby` 解释为先分组再汇总？
- 能否说明阈值和地区改变时，选择结果与完整地区聚合中哪些内容会改变？
- 能否解释两种切片的终点差异以及 size 与 count 的区别？

## 来源与参考资料

- pandas Developers, [Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-09-15. 列选择、loc/iloc、包含终点的标签切片和布尔筛选。
- pandas Developers, [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-09-15. 拆分、应用与合并，以及组行数、非缺失值数量和平均值。
- pandas Developers, [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-07-20. DataFrame 创建、选择、摘要统计与表操作。
- pandas Developers, [Copy-on-Write (CoW)](https://pandas.pydata.org/docs/user_guide/copy_on_write.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-09-15. 连锁赋值与单次 loc 赋值的区别.
- pandas Developers, [DataFrameGroupBy.last](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.typing.DataFrameGroupBy.last.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-09-15. last 默认跳过缺失值的行为.

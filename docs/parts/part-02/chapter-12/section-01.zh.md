# P2-12.1 Pandas DataFrame 表示什么

> Section ID: `P2-12.1`
> Version: `v2026.09.15`

## 带有行和列的表

Pandas 的 DataFrame 是行和列都带有标签的二维表结构。在学生成绩表中，一行记录一名学生的姓名、分数和通过状态，列名区分各个值的含义。同一张表中，分数列保存数值，姓名列保存字符串。

把字典的键作为列名、值列表作为对应列的数据，就能建立三名学生的表。

```python
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Kim", "Park", "Lee"],
        "score": [82, 45, 90],
        "passed": ["yes", "no", "yes"],
    }
)

print(df)
```

```text
   name  score passed
0   Kim     82    yes
1  Park     45     no
2   Lee     90    yes
```

左侧的 `0, 1, 2` 是行标签，称为索引。`name`、`score` 和 `passed` 是列标签。不计索引，数据区域为三行三列；标签为 1 的行记录 Park 的 45 分和通过状态 `no`。

```mermaid
--8<-- "assets/part-02/chapter-12/dataframe-structure-flow-zh.mmd"
```

## 按列组织与按行组织

也可以把每名学生的信息放进一个字典，再将字典列表转成 DataFrame。下面的代码会输出与前面相同的表。

```python
rows = [
    {"name": "Kim", "score": 82, "passed": "yes"},
    {"name": "Park", "score": 45, "passed": "no"},
    {"name": "Lee", "score": 90, "passed": "yes"},
]

df = pd.DataFrame(rows)
print(df)
```

第一种方式把 `[82, 45, 90]` 放入 `score` 列；第二种方式把 `score: 82` 放入 Kim 的记录。输入的组织方向不同，最终表的行和列却相同。

## 指定行标签

不指定索引时，默认生成 `0, 1, 2, ...` 的 `RangeIndex`。把姓名指定为索引后，行标签就从数字变为 Kim、Park 和 Lee。

```python
named = pd.DataFrame(
    {
        "score": [82, 45, 90],
        "passed": ["yes", "no", "yes"],
    },
    index=["Kim", "Park", "Lee"],
)

print(named)
```

```text
      score passed
Kim      82    yes
Park     45     no
Lee      90    yes
```

这张表只有 `score` 和 `passed` 两个数据列。姓名位于索引中，因此 `named.shape` 为 `(3, 2)`。之前的 `df` 把姓名也放在数据列中，形状为 `(3, 3)`。数字索引不一定等于当前行位置，标签也可能重复。

## 按标签对齐值

将 Series 赋给一列时，Pandas 按索引标签匹配，而不是仅按值的排列顺序匹配。假设要向以姓名为索引的成绩表添加学生加分。加分数据的顺序是 Lee、Kim、Park，而成绩表的顺序是 Kim、Park、Lee。

```python
bonus = pd.Series([5, 10, 0], index=["Lee", "Kim", "Park"])
adjusted = named.copy()
adjusted["bonus"] = bonus
adjusted["adjusted_score"] = adjusted["score"] + adjusted["bonus"]
print(adjusted[["score", "bonus", "adjusted_score"]])
```

```text
      score  bonus  adjusted_score
Kim      82     10              92
Park     45      0              45
Lee      90      5              95
```

第一个值 5 对应 Lee，而不是 Kim，因为标签决定数据如何连接。把 `bonus` 中的 Lee 标签改为 Choi 后，成绩表中的 Lee 找不到对应值，便会出现缺失值。长度相同并不意味着匹配的是同一名学生。实际资料中姓名可能重复，应先确定学生 ID 等记录标识。

## 列类型与表结构

输出前面 `df` 的大小、列名、索引、各列类型和前两行。确认 `score` 是否为数值类型，有助于判断能否直接计算平均分等结果。

```python
print(df.shape)
print(df.columns)
print(df.index)
print(df.dtypes)
print(df.head(2))
```

`shape` 为 `(3, 3)`，`columns` 包含 `name`、`score` 和 `passed`。`index` 为 `RangeIndex(start=0, stop=3, step=1)`，`head(2)` 只显示 Kim 和 Park 两行。

| 检查项 | 在此表中确认的内容 |
| --- | --- |
| `shape` | 三名学生、三个数据列 |
| `columns` | 姓名、分数、通过状态的列名 |
| `index` | 各行的标签 |
| `dtypes` | 分数列的数值类型和其他列的字符串类型 |
| `head(2)` | 前两名学生的实际值 |

根据 Pandas 版本和设置，字符串列的类型可能显示为 `str` 或 `object` 等。这里 `passed` 中的 `yes`、`no` 是字符串，不会自动变为布尔值。

NumPy 数组整体使用一个 `dtype`，DataFrame 则按列拥有各自的 `dtype`。可以用 DataFrame 选择和整理有名称的列，再将数值列转为数组，进行向量和矩阵计算。

## 一行与分析单位

一行并不总是代表一个最终分析对象。下面的传感器记录分别在三个时刻测量动作 A-01 和 B-02。一行代表一次测量，一个动作则包含多行。

```python
import pandas as pd

raw = pd.DataFrame(
    [
        ["A-01", 0.0, 0.00, 0.8],
        ["A-01", 1.0, 0.20, 1.4],
        ["A-01", 2.0, 0.40, 1.9],
        ["B-02", 0.0, 0.00, 0.7],
        ["B-02", 1.0, 0.25, 1.3],
        ["B-02", 2.0, 0.50, 1.5],
    ],
    columns=["action_id", "elapsed_seconds", "progress_fraction", "signal_a"],
)

print("rows =", len(raw))
print("actions =", raw["action_id"].nunique())
print(raw.groupby("action_id").size())
```

```text
rows = 6
actions = 2
action_id
A-01    3
B-02    3
dtype: int64
```

`len(raw)` 统计六条测量记录。`nunique()` 统计两个不同的动作 ID，`groupby("action_id").size()` 显示每个动作各有三条记录。`elapsed_seconds` 是动作开始后的经过时间，`progress_fraction` 是进度比例，`signal_a` 是测量值。

给 A-01 增加一条测量记录后，总记录数变为七条，A-01 的记录数变为四条，但动作数仍为两个。即使使用同一段代码，所计数的对象也会影响结果。要比较各动作的平均信号，就需要按 `action_id` 对测量行分组。

在客户表中，一行可能代表一名客户；在订单表中，同一客户的订单可能占多行。因此，能否用行数代表客户数，取决于表的记录单位。

## 案例：检查学生 CSV 的行和列

[`student-progress-samples.csv`](/AiBook/assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview } 保存了 36 名学生的学习记录。第一名学生 S001 来自 Seoul，学习时间为 8.0 小时，缺勤一次，练习测验九次，分数为 86，通过状态为 `yes`。

从仓库根目录运行以下代码，可以确认 `(36, 7)`、七个列名、索引、各列类型以及前三行。

```python
from pathlib import Path
import pandas as pd

csv_path = Path("docs/assets/part-02/chapter-12/student-progress-samples.csv")
df = pd.read_csv(csv_path)

print("shape:", df.shape)
print("columns:", list(df.columns))
print("index:", df.index)
print(df.dtypes)
print(df.head(3))
```

`student_id` 是数据列，左侧索引则是独立的 `0` 到 `35` 编号。`study_hours` 包含小数，`region` 和 `passed` 是字符串。并非所有列都是数值，因此不能把整张表直接用于数值计算。

例如预测分数时，`score` 是目标候选列，学习时间、缺勤次数和测验次数是输入候选列。`student_id` 用于区分学生。需要结合列名和实际值，才能确定各列的角色。

只把 CSV 中 S001 的分数从 86 改为 96，`shape` 和列名不变，`head(3)` 中的分数却会改变。添加一名学生的记录后，行数变为 37。结构检查与值检查能够发现不同的变化。

要以文件形式执行相同的 CSV 检查，请在仓库根目录运行以下命令。

[p2_12_1_dataframe_first_check.py](/AiBook/assets/part-02/chapter-12/p2_12_1_dataframe_first_check.py)

```bash
python docs/assets/part-02/chapter-12/p2_12_1_dataframe_first_check.py
```

## 类型与值的含义

分数为数值类型，只能说明可以计算，不能保证分数记录正确。满分 100 的考试被录入 900 分，数值类型本身仍然正常。仅凭 `dtype` 也无法判断学习时间列中的 8 是小时还是分钟。读懂表结构后，还应确认各列的单位、允许范围和记录时点。

## 检查清单

- 能否分别说明行、列和索引的作用？
- 能否解释 DataFrame 如何同时保存数值列和字符串列？
- 能否解释姓名作为数据列与作为索引时形状的区别？
- 能否解释测量行数与动作数为何不同？
- 能否说明 `shape`、`columns`、`index`、`dtypes`、`head()` 分别能揭示哪些变化？
- 能否解释 Series 值的顺序改变后为何仍按相同学生标签匹配？

## 来源与参考资料

- pandas Developers, [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-09-08. 带有行列标签的 DataFrame 结构。
- pandas Developers, [Package overview](https://pandas.pydata.org/docs/getting_started/overview.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-07-20. 表格、时间序列和矩阵数据的背景。
- pandas Developers, [Migration guide for the new string data type](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-09-08. 不同版本与设置下的字符串类型显示。
- pandas Developers, [Intro to data structures](https://pandas.pydata.org/docs/user_guide/dsintro.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, 查阅日期：2026-09-15. Series 赋值时的标签对齐和缺失标签处理.

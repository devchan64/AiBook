# P2-12.1 Pandas DataFrame 表达什么

> Section ID: `P2-12.1`
> Version: `v2026.07.23`

在 Part 2 Chapter 11 里，我们用 NumPy array 处理了 vector、matrix、axis 与 broadcasting。那条路径很适合数值计算，但当我们开始读取长得像表格的数据集时，问题会发生变化。

现实数据经常长成下面这样。

| name | score | passed |
| --- | ---: | --- |
| Kim | 82 | yes |
| Park | 45 | no |
| Lee | 90 | yes |

看到这张表时，我们通常先读的是 `谁`、`哪一列`、`哪个值`，而不是位置。Pandas 的 DataFrame 正是这种表格式数据的核心结构。

本节说明 `DataFrame`、`row`、`column`、`index` 的基本区分。前一章的 NumPy 更强调这些值怎样以 vector 与 matrix 的形状进入计算；这里则转向它们该怎样被读成“案例与变量组成的表”。下一章会再从这张表走向图表，去看表里不容易直接看到的变化与关系。后续继续进入选择、聚合与数据集准备时，也可以配合 [概念词汇表](/AiBook/en/reference/concept-glossary/) 一起作为回返点。

## 核心判断标准：Pandas DataFrame 表达什么

- 你可以把 DataFrame 解释为带标签的二维表格式数据结构。
- 你可以解释 row、column、index 各自识别什么。
- 你可以解释 DataFrame 能在同一张表里同时容纳数字、字符串等不同类型。
- 你可以解释为什么在机器学习数据集中，一行常被读成一个 case 或 sample，而一列常被读成一个 variable 或 feature。
- 你可以解释为什么 `shape`、`columns`、`index`、`dtypes`、`head()` 值得先检查。

## 三个标准

| 标准 | 为什么重要 | 本节需要的理解程度 |
| --- | --- | --- |
| DataFrame 是什么 | 它能帮助我们把 Pandas 读成“揭示表格含义的结构”，而不是单纯存值工具。 | 把它理解成带标签的二维表。 |
| 它与数组有什么不同 | 它能避免 NumPy array 与 DataFrame 的角色混在一起。 | 抓住行列名字，以及可同时容纳不同列类型这一点。 |
| 应该怎样开始读 | 它为后续的选择、聚合、数据集准备建立起点。 | 先从“一行是一个案例，一列是一个变量”出发。 |

| 术语 | 本节中的工作含义 |
| --- | --- |
| DataFrame | 带有行列标签的二维表结构。 |
| row | 表中的横向一行，常表示一个案例或一次观测。 |
| column | 表中的纵向一列，常表示一个变量或属性。 |
| index | 用来识别每一行的标签。 |
| label | 附着在行或列上的名字，而不只是位置编号。 |

## DataFrame 是带标签的二维表

Pandas 官方文档把 `DataFrame` 描述为二维、可改变大小、可能包含异质类型的表格式数据。文档也说明，行与列都带有标签，而且很多运算会按照这些标签进行对齐。

这里我们把 DataFrame 理解成：`一张有行名和列名的表，并且每一列都可能带着不同的含义与数据类型`。

如果说 NumPy array 强在基于位置的计算，那么 DataFrame 强在把 `表格的含义` 显示出来。

| 结构 | 最先看的东西 | 最自然回答的问题 |
| --- | --- | --- |
| NumPy array | position、shape、axis | 第几个值？计算沿哪个方向走？ |
| Pandas DataFrame | row label、column label、column 含义 | 这是谁的案例？这是哪个变量？该比较哪些列？ |

如果 NumPy 负责“可计算的数值形状”，那这一节就在重新把同一组值读成表：一行到底表示什么，一列又表示什么变量。这个视角会直接连到下一节的选择与聚合、后面章节的可视化，以及更后面的记录整理。这里最先需要建立的是表格直觉：一行作为一个案例，一列作为一个变量。

最简单的创建方式，是用“按列组织的 `dict`”。

问题场景：你想先做出一张最小的带标签表，看看它的基础形状。
输入(input)：包含 `name`、`score`、`passed` 三列的 `dict`。
预期输出(output)：一张装着 3 个学生信息的 3 行 3 列表。
要确认的概念：DataFrame 是带有列名的二维表结构。

```python
# 这个例子用 Pandas DataFrame 构造有行和列的表格数据，并检查其结构。
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

但现实中的原始数据也经常以“按行组织”的形式到来。比如 JSON 响应或日志记录，常常是一个由若干 `dict` 组成的列表。

问题场景：同一张表不一定是按列给你的，也可能是按行给你的。
输入(input)：一个列表，其中每个学生都被存成一个 `dict`。
预期输出(output)：和前一个例子结构相同的 DataFrame。
要确认的概念：DataFrame 能把按列输入与按行输入都转成同一种表结构。

```python
# 这个例子用 Pandas DataFrame 构造有行和列的表格数据，并检查其结构。
rows = [
    {"name": "Kim", "score": 82, "passed": "yes"},
    {"name": "Park", "score": 45, "passed": "no"},
    {"name": "Lee", "score": 90, "passed": "yes"},
]

df = pd.DataFrame(rows)
print(df)
```

这两种方式都能生成同一张表。这里可以这样区分。

- 按列输入：先想每一列里装的是什么值组。
- 按行输入：先想每一个案例由哪些属性组成。

无论输入是按列还是按行，这件事本身都不会自动决定“什么算一个样本”。

这里还要再小心一点。在 DataFrame 里，不能总是直接把 `一行 = 一个完整案例` 当成绝对规则。比如原始时间序列表里，一行可能只是 `某次动作中的一个记录时刻`，而不是整个动作本身。

原始时间序列里，一行可能只是一个测量时刻，而真正要比较的对象，可能是由许多行共同构成的一个完整动作。

| action_id | elapsed_seconds | progress_fraction | signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 0.0 | 0.00 | 0.8 |
| A-01 | 1.0 | 0.20 | 1.4 |
| A-01 | 2.0 | 0.40 | 1.9 |
| B-02 | 0.0 | 0.00 | 0.7 |
| B-02 | 1.0 | 0.25 | 1.3 |
| B-02 | 2.0 | 0.50 | 1.5 |

在这样的表里，一行表示一个时间点，而像 `action_id` 这样的标识列，会成为把多行绑定成一个动作的规则。也就是说，读 DataFrame 时，要先把 `一行是不是已经是一个最终案例` 和 `是不是多行合在一起才构成一个案例` 这两个问题分开。

下面这个表会让区别更清楚。

| 读取单位 | 在这张表里表示什么 |
| --- | --- |
| 一行 | 传感器记录下来的一个时刻 |
| 一个 `action_id` | 一次动作实例 |
| 多个 `action_id` 组 | 由多次动作组成的数据集 |

这个区分之所以重要，是因为即使 DataFrame 没变，读取单位也会随问题而改变。读原始时间序列时，一行很重要；比较完整动作时，我们可能要把多行汇总成“每个动作一行”的摘要表。

所以，DataFrame 提供的是表结构，但不会替我们决定分析单位。先看行和列长什么样，再单独判断真正要比较的样本 1 件到底是什么。

例如，只是数一数每个 `action_id` 有几行，就已经把读取单位从“一行”切换到了“一次动作”。

问题场景：你想用最短的代码，看清多个原始日志行背后到底有几次动作。
输入(input)：一个包含 `action_id`、`elapsed_seconds`、`progress_fraction`、`signal_a` 的小型原始时间序列表。
预期输出(output)：总行数、不同 `action_id` 的数量、每个 `action_id` 的行数。
要确认的概念：在 DataFrame 中，一行可能只是一个时间点，而 `groupby` 可以帮助你把多行重新读成一个动作单位。

```python
# 这个例子用 Pandas DataFrame 构造有行和列的表格数据，并检查其结构。
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

输出大致可以这样读。

```text
rows = 6
actions = 2
action_id
A-01    3
B-02    3
dtype: int64
```

这里真正关键的是视角，而不是算式本身。

- 整个 DataFrame 有 6 行。
- 但真实动作只有 2 个。
- 也就是说，DataFrame 很自然地能表达“多行共同构成一个案例”的情形。

这张表目前只展示了源数据结构，还没有告诉我们任何质量判断或因果解释。

这个视角不仅会在下一节的 filtering 与 aggregation 里回来，后面做 feature 或 summary table 时也会再次用到。

## 分开读取行、列与索引

很多人第一次看到 DataFrame 时，只盯着整张表。实际上，我们需要同时读取三个层次。

1. row：case、sample、observation
2. column：variable、feature、attribute
3. index：识别 row 的标签

再看一次那个小例子。

问题场景：在讲 row、column、index 之前，需要先重新看一眼最简单的表。
输入(input)：包含姓名、分数、是否通过的小 `DataFrame`。
预期输出(output)：左侧带默认数字索引的表。
要确认的概念：一行是一个案例，而列标签与索引一起构成表结构。

```python
# 这个例子用 Pandas DataFrame 构造有行和列的表格数据，并检查其结构。
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

输出可以这样读。

```text
   name  score passed
0   Kim     82    yes
1  Park     45     no
2   Lee     90    yes
```

这里：

- 左边的 `0, 1, 2` 是 index，
- `name`、`score`、`passed` 是 column label，
- 每一条横向记录则是一行关于一个人的 row。

这个关系用图看会更清楚。

```mermaid
--8<-- "assets/part-02/chapter-12/dataframe-structure-flow-zh.mmd"
```

这里最关键的一点是：index 本身不是数据值，而是指向行的规则。

## 索引可以是简单编号，也可以是有意义的标签

Pandas 官方文档说明，如果不单独提供 index，就会默认使用 `RangeIndex`。所以我们在刚创建 DataFrame 时，经常会看到 `0, 1, 2, ...`。

但 index 不一定非得是数字。

问题场景：你想确认表左侧不只可以放编号，也可以放有意义的标签。
输入(input)：带有 `score`、`passed` 两列，并把姓名列表作为 index 的 `DataFrame`。
预期输出(output)：左边显示 `Kim`、`Park`、`Lee` 作为行标签的表。
要确认的概念：index 是一套独立的行识别结构，而不只是默认编号装饰。

```python
# 这个例子用 Pandas DataFrame 构造有行和列的表格数据，并检查其结构。
df = pd.DataFrame(
    {
        "score": [82, 45, 90],
        "passed": ["yes", "no", "yes"],
    },
    index=["Kim", "Park", "Lee"],
)

print(df)
```

输出会变成这样。

```text
      score passed
Kim      82    yes
Park     45     no
Lee      90    yes
```

此时 `Kim`、`Park`、`Lee` 就成了行标签。这里可以这样记。

- 数字 index：指向默认顺序。
- 标签 index：指向行身份或行名字。

这个差异在下一节学习选择与 filtering 时会变得很重要。

再做一个小实验，会更清楚。

问题场景：你想直接把当前 index 结构当成 Python 对象看出来。
输入(input)：刚才的 `df`。
预期输出(output)：形如 `RangeIndex(...)` 或 `Index([...])` 的索引信息。
要确认的概念：index 不是视觉装饰，而是 Pandas 用来管理行的结构。

```python
# 这个例子用 Pandas DataFrame 构造有行和列的表格数据，并检查其结构。
print(df.index)
```

如果使用默认数字索引，输出会像这样。

```text
RangeIndex(start=0, stop=3, step=1)
```

如果使用标识标签，则会像这样。

```text
Index(['Kim', 'Park', 'Lee'], dtype='object')
```

所以，index 不是表左边的边角内容，而是另一层“识别行”的结构。

## DataFrame 能把不同类型的列放在一起

NumPy array 通常最擅长的是许多值共享同一种数值 `dtype` 的情况。但真实表格数据里，经常一列是数字，一列是文本，一列是类别值。

哪怕在最简单的例子里：

- `name` 是偏字符串的文本，
- `score` 是数值，
- `passed` 则可以被读成用文本表示的类别值。

因此，DataFrame 对真实数据更自然，因为它允许 `每一列带着不同的含义`。

这件事在准备机器学习数据集时很重要。真实数据经常同时混着数字、日期、文本、类别字段，以及缺失值。

我们可以这样看类型。

问题场景：在后面做选择与预处理判断前，先知道每一列到底是数值还是文本。
输入(input)：包含姓名、分数与通过情况的 `df`。
预期输出(output)：每一列对应的 `object`、`int64` 等类型信息。
要确认的概念：在 DataFrame 中，类型是按列分开的，而不是整张表只有一种统一类型。

```python
# 这个例子用 Pandas DataFrame 构造有行和列的表格数据，并检查其结构。
print(df.dtypes)
```

输出大致像这样。

```text
name      object
score      int64
passed    object
dtype: object
```

关键点不是“整张 DataFrame 只有一个类型”，而是“每一列都有自己的类型”。

- `score` 是可以直接用于数值工作的列。
- `name` 与 `passed` 更接近标识与分类，而不是直接做数值计算。

后面要决定哪些列变成模型输入、哪些列需要先转换时，这个直觉就会派上用场。

## 先把一行读成一个案例，一列读成一个变量

读学习用表格时，最重要的第一个习惯，是先用 `一行是一个案例，一列是一个变量` 的方式来试读。

比如我们有一张客户数据表。

| customer_id | age | region | purchased |
| --- | ---: | --- | --- |
| C001 | 29 | Seoul | yes |
| C002 | 41 | Busan | no |
| C003 | 35 | Seoul | yes |

我们可以这样读。

- 每一行：一个客户
- `age`、`region`：候选输入变量或 feature
- `purchased`：候选预测目标

即便还没有训练模型，这种读取习惯也很重要。否则以后再看到 `feature`、`label`、`target`、`split` 这些词时，就会显得脱节。

不过，这句话并不是绝对真理，更像是 `最先应该拿来试的默认读取方式`。

| 表类型 | 一行是否马上就是一个完整 sample？ |
| --- | --- |
| 客户列表、订单列表、学生名单这类案例表 | 往往是 |
| 按时间堆起来的原始时间序列表 | 不一定 |
| 已经聚合好的摘要表 | 聚合单位本身就可能是 sample |

当然，并不是每一张表都完全遵守这个模式。有的表是按时间记录的日志，有的表本身已经是总结结果。即便如此，从 `row = case, column = variable` 开始，通常依然最有帮助。

## DataFrame 与数组不是竞争关系，而是角色不同

没有必要把 DataFrame 与 NumPy array 看成只能二选一的竞争关系。

它们经常一起出现。

| 工作 | 更自然的结构 |
| --- | --- |
| 读取表格数据、查看列名、整理数据集 | DataFrame |
| 数值数组计算、vectorization、线性代数计算 | NumPy array |
| 模型输入前的数值化转换 | 从 DataFrame 走向 array |

在实践中，常见流程像这样。

1. 先把 CSV 读成 DataFrame 并检查。
2. 选出需要的列。
3. 处理缺失值和数据类型。
4. 当真正需要数值计算时，再转到 NumPy array 或模型输入形状。

所以，DataFrame 强在把数据保持为 `可解释的表`，而 NumPy 强在把数据变成 `可计算的数组`。

## 第一次拿到 DataFrame 时先看什么

第一次拿到一个新的 DataFrame 时，不必立刻做复杂操作。应先检查结构。

问题场景：在操作新表前，你想快速确认它的大小、列名、索引、类型，以及前几行长什么样。
输入(input)：`df`。
预期输出(output)：`shape`、`columns`、`index`、`dtypes`、`head()` 的结果。
要确认的概念：DataFrame 的第一次检查，本质上是一次快速结构扫视。

```python
# 这个例子用 Pandas DataFrame 构造有行和列的表格数据，并检查其结构。
print(df.shape)
print(df.columns)
print(df.index)
print(df.dtypes)
print(df.head())
```

每一项都在回答不同问题。

| 检查项 | 在问什么 |
| --- | --- |
| `shape` | 一共有多少行、多少列？ |
| `columns` | 存在什么列？ |
| `index` | 行是怎样被识别的？ |
| `dtypes` | 每一列正被读成什么类型？ |
| `head()` | 前几行实际长什么样？ |

这五项可以看作 DataFrame 的 `第一印象检查表`。

其中 `dtypes` 特别重要。有些列看起来像数字，但实际上可能被读成文本。这件事在下一节做 filtering 与 aggregation 时就会立刻产生影响。

把这几项一次性看完，会更直观。

问题场景：你想看“五个结构检查”一起执行时的输出到底长什么样。
输入(input)：`df`。
预期输出(output)：依次打印表大小、列列表、索引结构、列类型，以及前两行。
要确认的概念：很短的一组输出就足以总结整张表的大致轮廓。

```python
# 这个例子用 Pandas DataFrame 构造有行和列的表格数据，并检查其结构。
print(df.shape)
print(df.columns)
print(df.index)
print(df.dtypes)
print(df.head(2))
```

输出大致可以这样读。

```text
(3, 3)
Index(['name', 'score', 'passed'], dtype='object')
RangeIndex(start=0, stop=3, step=1)
name      object
score      int64
passed    object
dtype: object
   name  score passed
0   Kim     82    yes
1  Park     45     no
```

这五行已经能快速提供一个结构总览。

- `shape`：表大小
- `columns`：列名列表
- `index`：行标签结构
- `dtypes`：列类型
- `head(2)`：前几行真实长相

即使还没开始操作表，只靠这些检查，也已经能更快知道这张表到底是什么类型的数据。

行数稍多的 CSV 文件也可以用同样方式检查。输入文件是 [`student-progress-samples.csv`](/AiBook/assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview }。一行表示一名学生的学习记录，核心列是 `student_id`、`region`、`study_hours`、`absences`、`practice_quizzes`、`score`、`passed`。

问题场景：在读取表之前，先确认表的形状、列名、索引和数据类型。
输入(input)：36 行学生学习进度 CSV。
期望输出(output)：`shape`、`columns`、`index`、`dtypes` 和前三行。
要确认的概念：在用 DataFrame 计算之前，要先确认它有多少行列，以及每一列是什么意思。

```python
# 这个例子用 Pandas DataFrame 构造有行和列的表格数据，并检查其结构。
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

同样的代码也可以通过 [`p2_12_1_dataframe_first_check.py`](/AiBook/assets/part-02/chapter-12/p2_12_1_dataframe_first_check.py) 执行。进入下一节的 filtering 与 aggregation 之前，这个文件会先帮助你确认表有几行几列，以及各列被读成了什么类型。

## 案例来看

### 案例 1. 第一次拿到成绩表时，应该从哪里开始读？

假设一个学习者拿到了一张班级成绩表。表里同时有姓名、地区、缺勤次数、分数、是否通过。人当然可以马上看出“谁拿了多少分”，但从模型读取的角度，必须重新整理成：一行表示什么案例，每一列又表示什么含义。

这时，DataFrame 就不只是数字容器，而是一张带有 `name`、`score`、`passed` 等标签的表。一行变成一个学生案例，一列则变成一个有不同含义的变量位置，比如分数或缺勤次数。index 也不再只是左边的编号，而是“指向行”的规则。

这个案例之所以重要，是因为后面的 selection、filtering 与学习数据集准备，全都建立在这种读取习惯上。也正因为如此，第一次拿到表时，通常更应该先看 `shape`、`columns`、`dtypes`、`head()`，而不是先急着写公式或模型代码。

所以，DataFrame 的入门更接近“视角切换”，而不只是语法记忆。我们需要开始把 `看起来像电子表格的表` 读成 `其中每一行和每一列已经带着角色的数据结构`。这样后面的 Pandas 操作与机器学习准备才会自然得多。

## 检查清单

- 能否把 DataFrame 解释成“有行名和列名的表”？
- 能否分别说明 row、column、index 的角色？
- 能否说明 DataFrame 可以同时容纳数值列与文本列？
- 能否说明在机器学习数据集中，一行与一列通常怎样读取？
- 能否说明为什么 `shape`、`columns`、`index`、`dtypes`、`head()` 应先检查？
- 能否把 DataFrame 解释成带标签的二维表格型数据结构？

## 来源与参考资料

- pandas Developers, [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation，确认日期：2026-07-20。作为把 DataFrame 说明为具有 labeled axes 的 two-dimensional tabular data structure 的依据。
- pandas Developers, [Package overview](https://pandas.pydata.org/docs/getting_started/overview.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation，确认日期：2026-07-20。作为说明 pandas 用于 tabular、time series、matrix data 的入门背景。

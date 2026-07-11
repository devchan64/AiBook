# P2-12.3 准备学习数据集(dataset)的直觉

> Section ID: `P2-12.3`
> Version: `v2026.07.11`

在 P2-12.1 中，我们把 `DataFrame` 读成表格型数据结构。在 P2-12.2 中，我们从这张表里挑出需要的列，用条件筛掉行，并查看了总结值。现在问题再往前走一步：`如果要把这张表变成模型能读取的学习数据集，需要准备什么？`

这里重要的一点是，`会熟练使用 Pandas` 与 `会准备学习数据集` 并不是同一件事。前者是操作表格的技术，后者是决定模型接收什么输入、学习什么答案的工作。

本节说明 `数据集(dataset)`、`特征(feature)`、`目标(target)`、`验证(validation)`、`数据泄漏(data leakage)` 的基本区分。`DataFrame` 与表选择的代表性说明放在 P2-12.1、P2-12.2 与[概念词汇表](../../../reference/concept-glossary.md)中，这里关注的是：如何把那张表重新组织成学习输入与答案。

如果说 Chapter 11 让我们得到可计算的数组形状，那么现在的 Chapter 12 就是在表中决定哪些列要留下、哪些列要去掉。这里整理出的输入与答案候选，会接到下一章 Chapter 13 的可视化，以及 Chapter 14 的记录整理。

## 本节范围

本节不覆盖所有预处理(preprocessing)技术。缺失值(missing value)处理、缩放(scaling)、编码(encoding)的入门流程会在 P3-7.2 再处理，交叉验证(cross-validation)的详细步骤会在 P3-4.2 与 P3-9.2 再接上。pipeline 的实现与更广泛的自动化结构，先放在当前正文范围之外。

本节回答以下问题。

- 在表格数据里，什么是输入 `X`，什么是答案 `y`？
- 为什么有些列要留下，有些列要去掉？
- 为什么要把数据分成 train、validation、test？
- 为什么预处理顺序一旦弄错，就会产生数据泄漏(data leakage)？
- Pandas 在这个准备过程中扮演什么角色？

## 本节目标

- 你可以把学习数据集准备说明成`把原始表重新组织成模型输入与答案`的过程。
- 你可以把一行(row)读成一个样本(sample)，把一列(column)读成一个特征(feature)或目标(target)候选。
- 你可以说明为什么要分开输入 `X` 与答案 `y`。
- 你可以说明为什么要分开 train、validation、test。
- 你可以说明为什么数据泄漏(data leakage)会扭曲评估。
- 你可以说明 Pandas 用于读数据、选择、过滤、生成列、做基础检查，而训练划分常常会与其他工具一起处理。

## 先抓住的一个画面

本节最先要抓住的画面是：一行(row)通常是一个样本(sample)，一列(column)是特征(feature)或目标(target)候选，`X` 是输入列的集合，`y` 是要预测的答案列。

再看一次一个小型学生表：

| 在表里看到的东西 | 换成学习数据集语言后如何读取 |
| --- | --- |
| 一行 | 一个学生样本 |
| `region`、`absences`、`score` 列 | 输入特征候选 |
| `passed` 列 | 答案目标候选 |
| `X.shape = (4, 3)` | 4 个样本，3 个特征 |
| `y.shape = (4,)` | 4 个样本对应的一组答案 |

如果先把这张图景抓住，后面的 `train_test_split`、`fit`、`predict` 读起来就不会那么抽象。

## 三个判断标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 为什么不能把整张表原样拿去训练 | 它能让你区分表结构与模型输入结构。 | 理解到和问题无关的列、答案列、标识列可能会混在一起。 |
| 为什么要分开 `X` 与 `y` | 它能把输入与答案之间的边界说清楚。 | 理解到必须把输入与要预测的对象分开，学习结构才会清晰。 |
| 为什么要先划分数据 | 它是防止泄漏与防止评估被抬高的判断标准。 | 理解到这是为了避免把后续评估要用的信息提前漏进训练里。 |

| 术语 | 本节先固定的含义 |
| --- | --- |
| 数据集(dataset) | 为了学习或评估而整理好的样本与变量集合。 |
| 特征(feature) | 用作模型输入的列或值。 |
| 目标(target) | 模型要预测的答案列。 |
| 验证(validation) | 用来比较设置与选择的中间评估数据。 |
| 数据泄漏(data leakage) | 在预测时本来不该知道的信息，提前混进学习过程的问题。 |

## 不是把表原样喂给模型，而是按问题重新组织

原始表往往更适合人来阅读，但未必已经是模型可以直接学习的形状。

例如，看下面这张表。

| student_id | name | region | absences | score | passed |
| --- | --- | --- | ---: | ---: | --- |
| S001 | Kim | Seoul | 1 | 82 | yes |
| S002 | Park | Busan | 5 | 45 | no |
| S003 | Lee | Seoul | 0 | 90 | yes |
| S004 | Choi | Busan | 2 | 73 | yes |

人从这张表里可以提出很多问题。

- 是不是想预测分数(score)？
- 是不是想分类通过/不通过(passed)？
- 是不是想观察按地区(region)划分的倾向？

即使是同一张表，只要问题变了，学习数据集的组织方式也会跟着变。

| 问题 | `y` 候选 | `X` 候选 |
| --- | --- | --- |
| 是不是要预测是否通过 | `passed` | `region`、`absences`、`score` 等 |
| 是不是要预测分数 | `score` | 需要重新考虑是否排除 `passed`，以及 `region`、`absences` |
| 是不是要识别学生身份 | 需要单独的问题定义 | `student_id`、`name` 通常更像标识列 |

所以，数据集准备与其说是`整理表格`，不如更准确地理解成：`根据问题重新划定输入与答案的边界`。

## 分开 `X` 与 `y`

scikit-learn 文档通常把 `X` 用作输入特征矩阵(feature matrix)，把 `y` 用作目标(target)。在 glossary 中，feature 被说明成用数值或类别值来表示样本(sample)的量，在数据矩阵里通常以列(columns)表示。sample 通常被说明成一个 feature vector，而 target 则是在监督学习(supervised learning)中的因变量(dependent variable)。

这里先记住下面这组差别就够了。

- `X`：模型会拿来观察并用于判断的输入列集合
- `y`：模型要预测的答案列

看一个小例子。

问题场景：要把学生表改成预测是否通过的分类问题时，必须先把输入 `X` 与答案 `y` 分开。
输入(input)：一个小型 `DataFrame`，里面包含每位学生的地区、缺勤数、分数、是否通过。
预期输出(output)：输入列集合 `X` 与答案列 `y` 被分离出来。
要确认的概念：准备学习数据集不是原样使用整张表，而是按照问题定义拆出输入与目标。

```python
import pandas as pd

df = pd.DataFrame(
    {
        "student_id": ["S001", "S002", "S003", "S004"],
        "region": ["Seoul", "Busan", "Seoul", "Busan"],
        "absences": [1, 5, 0, 2],
        "score": [82, 45, 90, 73],
        "passed": ["yes", "no", "yes", "yes"],
    }
)

X = df[["region", "absences", "score"]]
y = df["passed"]
```

这段代码可以读成一个预测 `passed` 的分类(classification)问题。

- 每一行都是一个学生样本(sample)。
- `region`、`absences`、`score` 是输入特征(feature)。
- `passed` 是答案目标(target)。

画成图后如下。

```mermaid
--8<-- "assets/part-02/chapter-12/x-y-split-flow/zh.mmd"
```

核心点在于：`X` 与 `y` 不是一开始就固定好的。先有问题定义，再去拆列。

这里也保留一层会直接接到 P2-11.2 的视角。

| 表达 | 在本节里的读取方式 |
| --- | --- |
| `X.shape[0]` | 样本(sample)数 |
| `X.shape[1]` | 特征(feature)数 |
| `y.shape[0]` | 答案个数，通常和样本数相同 |

所以，说要分开 `X` 与 `y`，并不只是拆列名，也是在决定模型要读取的数组形状(shape)。

## 不能把所有列原样放进去

表里的列并不都适合作为模型输入。通常要区分下面三类。

1. 可以直接用于预测的列
2. 需要先做变换的列
3. 应该从输入里剔除的列

例如：

| 列 | 能否直接使用 | 原因 |
| --- | --- | --- |
| `absences` | 相对可以直接使用 | 因为它是数值列 |
| `region` | 需要变换 | 因为它是字符串类别 |
| `student_id` | 通常排除 | 因为它是标识列，本身未必代表一般模式 |
| `passed` | 如果它是目标，就要从输入中排除 | 因为把答案列放进输入，会显著增加泄漏风险 |

这里像 `region` 这样的类别型(categorical)列，可能需要根据模型先转换成数值形式。pandas 的 `get_dummies()` 被介绍为把类别变量转换成 dummy/indicator variables 的函数。

例如：

问题场景：像 `region` 这样的字符串类别，许多模型不能直接读取，因此需要改变其表示方式。
输入(input)：由 `region`、`absences`、`score` 组成的输入 `X`。
预期输出(output)：`region` 被展开成多个 0/1 列之后的 `X_encoded`。
要确认的概念：类别列在学习之前，可能需要先重新表示成数值形式。

```python
X = df[["region", "absences", "score"]]
X_encoded = pd.get_dummies(X, columns=["region"])

print(X_encoded)
```

这个阶段的关键并不是`背下编码方法`。更重要的问题是：`这列能不能像数字一样直接读？还是应该先改变表示方式？`

## 如果不区分标识列与答案列，就很容易读错

一个常见混淆是：`会感觉眼前出现的所有列都像是 feature`。但标识列(identifier)与目标(target)的角色和特征并不一样。

例如：

- `student_id` 是区分每一行的标记。
- `name` 是方便人阅读的名字。
- `passed` 可能就是要预测的答案。

如果把它们原样放进输入，会出现两个问题。

1. 模型可能被偶然的标识信息吸引，而不是学习一般模式。
2. 太接近答案的信息可能流入输入，从而把评估抬高。

这种感觉在后面还会继续重要。好的数据集不是因为列很多才好，而更接近于：`只保留了符合问题定义的列的数据集`。

## 分成 train、validation、test

数据集准备中的下一个关键步骤是划分(split)。scikit-learn 的 `train_test_split` 文档把它说明成：把数组或矩阵随机拆成 train 与 test 子集的工具。

这里可以先这样理解。

- train：模型真正拿来学习的数据
- validation：用来检查设置、比较选择的数据
- test：最后当成第一次见到的数据来确认的数据

画成图就是：

```mermaid
--8<-- "assets/part-02/chapter-12/train-val-test-flow/zh.mmd"
```

为什么一定要分开？因为模型在已经见过的数据上表现好，并不够。我们真正想知道的是：`它在第一次见到的数据上，能不能也差不多地工作？`

这个视角会直接连到 Part 3 的过拟合(overfitting)、泛化(generalization)、评估指标(metric)。

## 先划分，再只从 train 学到训练中要用的变换规则

scikit-learn 的 common pitfalls 文档强烈警告两类错误。

- inconsistent preprocessing：对训练数据与测试数据应用了不同预处理的错误
- data leakage：把预测时本不该知道的信息混进学习过程的错误

其中，文档特别说明 test data should never be used to make choices about the model，并把`不要对测试数据调用 fit 或 fit_transform`作为一般规则来提醒。

这里可以把下面这条顺序当作标准。

1. 先从整张表里挑出输入候选与答案候选。
2. 先把它们分成 train / validation / test。
3. 像平均值、标准化、编码、特征选择这类`需要学出来的变换`，只在 train 上建立规则。
4. 对 validation、test 只应用同一套变换，不从它们身上再学习。

如果打乱这个顺序，就会变得像是模型提前偷看了答案。

把错误流程与更安全的流程并排看：

| 流程 | 问题 |
| --- | --- |
| 先用整份数据建立规则，再去划分 | test 信息可能提前混进来 |
| 先划分，再只用 train 建立规则 | 评估会更公平 |

本节先抓住的是这个判断标准，而不是实现细节。

再用下面的图看会更清楚。

```mermaid
--8<-- "assets/part-02/chapter-12/no-leakage-preprocessing-flow/zh.mmd"
```

如果把错误顺序与更安全顺序重新写成问题，可以得到下面的表。

| 问题 | 更安全的回答 |
| --- | --- |
| 可以把整张表都整理完之后再划分吗？ | 不可以，因为后续评估要用的信息可能会提前混进来，所以要先划分。 |
| 平均值、标准化、编码规则该从哪里学？ | 只从 train 学。 |
| validation、test 的作用是什么？ | 只接收 train 学到的同一套规则。 |

## 用案例来看

### 案例 1. 想预测是否通过，却把答案列一起塞进输入

假设学习者想用学生表做一个预测 `是否通过(passed)` 的模型。表里同时有 `student_id`、`region`、`absences`、`score`、`passed`。这时很容易想把所有看得见的列都放进 `X`。

但这样会出问题。`passed` 本来就是要预测的答案，却也被一起放进了输入；而 `student_id` 也可能只是区分学生的标记，并不直接对应一般模式。模型会更像是在偷看答案，或者被偶然的标识信息牵着走，而不是真的学到规则。

所以，在数据集准备里，先要决定`到底想预测什么`，然后把 `y` 分出来，再重新选择哪些特征该留下、哪些列该排除。接着先分 train、validation、test，再把像编码、缩放这样需要在训练中学规则的变换，只放在 train 一侧建立。

这个案例说明，数据集准备并不只是简单整理表格。即使是同一张表，`X` 与 `y` 的边界也会随问题变化；而如果划分顺序选错，评估就可能被抬高。Pandas 是这个过程前半段里用来挑列、检查结构的工具，而公平的学习评估，则必须连后面的划分与变换顺序也一起对齐。

读者在这里尤其要抓住下面这句话。

- `先分开 X 与 y，先分开 train / validation / test，再只从 train 建立要学习的变换规则。`

## Pandas 负责准备过程的前半段

Pandas 通常强在数据集准备的前半段。

- 读取 CSV、Excel、JSON 等原始来源。
- 只选出需要的列。
- 检查错误值或奇怪格式。
- 区分类别列与数值列。
- 进行基础的列生成与变换。

例如：

问题场景：在模型训练之前，你想先用眼睛检查一下输入列与答案列实际长什么样。
输入(input)：已经分开的 `X`、`y`。
预期输出(output)：输出 `X` 的前几行与 `y` 的前几个值。
要确认的概念：Pandas 很擅长在学习之前检查表结构与列角色。

```python
X = df[["region", "absences", "score"]]
y = df["passed"]

print(X.head())
print(y.head())
```

或者：

问题场景：你需要检查是否存在缺失值，以及每一列被读成了什么类型。
输入(input)：原始 `DataFrame` `df`。
预期输出(output)：每列缺失值数量与每列数据类型列表。
要确认的概念：学习前检查不只是看值本身，也是在看缺失值与类型结构。

```python
print(df.isna().sum())
print(df.dtypes)
```

这样的代码，与其说是`训练模型`，不如更接近于`在训练前检查表格`。

相对地，真正的划分与学习 pipeline，通常会接到 scikit-learn 之类的工具上去处理。

例如：

问题场景：检查结束后，为了把学习与评估分开，你需要把数据分成 train/test。
输入(input)：输入 `X`、答案 `y`、划分比例与随机种子。
预期输出(output)：分成学习用与测试用的 `X_train`、`X_test`、`y_train`、`y_test`。
要确认的概念：表操作阶段与学习数据划分阶段是连着的，但角色不同。

```python
from sklearn.model_selection import train_test_split

X = df[["region", "absences", "score"]]
y = df["passed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
```

这里重要的不是把函数用法全部背下来，而是理解`表操作`与`学习划分`是彼此衔接但不同的阶段。

## 如果用一句话概括学习数据集准备

如果把本节核心压缩成一句话，那么学习数据集准备就是：`在原始表里重新分配 sample、feature、target 的角色，并守住划分顺序，避免评估被扭曲。`

没有这个视角时，Pandas 代码越长，就越容易丢失“为什么要改列、为什么要分开”的判断。反过来，只要这个视角抓住了，即使还不懂所有预处理技术，你也可以继续追问：`现在这段代码是在挑输入、挑答案，还是在防止泄漏？`

## 本节要记住的视角

- 数据集准备不是原样使用表格，而是按照问题定义拆成 `X` 与 `y`。
- 一行通常是一个样本(sample)，一列是特征(feature)或目标(target)候选。
- 标识列、说明性列、答案列的角色可能都不同于输入特征。
- 类别列可能需要先改变表示方式，而不是直接使用。
- train / validation / test 的划分，是为了更公平地看泛化性能。
- 如果先用整份数据建立变换规则，数据泄漏(data leakage)风险就会提高。

## 简短检查

- 你能用一句话说出当前表里到底想预测什么吗？
- 你能区分哪一列是 `y`，哪些列是 `X` 候选吗？
- 你能说明为什么把标识列与答案列直接放进输入会有风险吗？
- 你能说明为什么要分开 train / validation / test 吗？
- 你能说明为什么预处理规则只能从 train 学吗？
- 当你看到 `X.shape = (4, 3)` 与 `y.shape = (4,)` 时，能说出哪个是样本数、哪个是特征数吗？

## 什么时候要先想起这个视角

- 当你不想把表直接塞进模型，而是要先决定预测什么、哪些列可以作为输入时，就先想起学习数据集准备这个视角。
- 当你需要解释为什么要分开 `X` 与 `y`、为什么要过滤标识列与泄漏风险列、为什么要分开 train/validation/test 时，就回到本节。
- 当你需要再次确认预处理规则应该只从 train 学，而不是从整份数据学时，本节就是判断标准。

## 来源与参考资料

- pandas Developers, `pandas.get_dummies`, pandas API reference, 确认日期: 2026-06-25. [https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn Developers, `Glossary`, scikit-learn documentation, 确认日期: 2026-06-25. [https://scikit-learn.org/stable/glossary.html](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn Developers, `train_test_split`, scikit-learn API reference, 确认日期: 2026-06-25. [https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn Developers, `Common pitfalls and recommended practices`, scikit-learn user guide, 确认日期: 2026-06-25. [https://scikit-learn.org/stable/common_pitfalls.html](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }

# P2-10.1 为什么笔记本(notebook)对学习有用

> Section ID: `P2-10.1`
> Version: `v2026.07.19`

在 Part 2 Chapter 7 中，我们已经区分了 Python 是在哪里执行的，包括 terminal、shell、interpreter、script、virtual environment。在 Part 2 Chapter 8 和 Chapter 9 中，我们通过小例子重新恢复了 Python 语法和数据结构。

现在我们单独来看 Jupyter Notebook 或 Google Colab 这类 notebook 环境。这里说的 notebook 不是纸质笔记本，而是一种把 code、output、explanation 一起保存在一个文档里的计算文档。

Notebook 在 AI 学习里尤其常见。因为你可以把公式改写成代码后立刻检查，可以打印数据表，可以画图，也可以把解释写在旁边。

这里说明 `notebook`、`code cell`、`markdown cell`、`output` 的基本区分。如果说 Chapter 7 讨论的是“在哪里执行”，Chapter 8 到 9 讨论的是“用什么句子写什么内容”，那么这里讨论的就是：如何把这些执行和计算结果一起留在一个文档里，并且以后还能重新阅读。Notebook 与其说是一种新的执行环境名称，不如说是一种把已经执行过的代码和输出打包成学习记录的格式。后面这些概念再次出现时，也可以把[概念词汇表](/AiBook/en/reference/concept-glossary/)当作基准点。

在 Part 2 的流程里阅读这一章时，先抓住下面的最小线索。

| 现在这里先抓住的最小线索 | 可以留给下一节的内容 |
| --- | --- |
| notebook 是一种把代码、输出和解释留在同一个文档里的记录格式 | Colab 和 Jupyter 的详细差异 |
| code cell、markdown cell 和 output 各有不同角色 | runtime 与文件访问的更细区分 |
| notebook 很适合学习和探索，但并不会完全替代 script | 如何把记录整理成可重新执行的具体习惯 |

| 术语 | 本节先要抓住的含义 |
| --- | --- |
| notebook | 一种同时包含代码、解释和输出的计算文档 |
| code cell | 执行实际 Python 代码的区块 |
| markdown cell | 以文字保留问题、解释和解读的区块 |
| output | 代码执行后可见的结果，例如值、表、图和错误信息 |
| computational notebook | 一种把计算与解释一起保留在同一文档里的格式 |

把 notebook 理解成 `不是新语法，而是把计算和解读放在一起的地方` 就足够了。执行位置和可复现性会在 P2-10.2 与 P2-10.3 里更具体地讨论。

## 本节的范围

本节不是详细说明如何安装 notebook 或如何使用 Colab。Colab 与本地 PC 环境的差异已经在 P2-3.5 和 Part 2 Chapter 7 里看过，Jupyter 与 Colab 的差异则会在 P2-10.2 单独处理。

本节回答以下问题。

- 什么是 notebook？
- code cell、markdown cell 和 output 如何一起使用？
- 为什么 notebook 对学习记录有用？
- 为什么 notebook 并不总是比 script 更好？
- 在 AI 再学习过程中，用 notebook 的合适态度是什么？

本节先收束 notebook 为什么适合学习这个问题：代码、输出和说明可以一起留在同一份记录里。`.ipynb` 文件和正在运行的 runtime 的区别，会在接下来的 P2-10.2 与 P2-10.3 中马上重新连接。Server 与 kernel 的内部结构本身放在当前正文范围之外。

## 本节的目标

- 能把 notebook 解释成同时包含代码、解释和输出的计算文档。
- 能区分 code cell 与 markdown cell 的角色。
- 能说明为什么 notebook 对实验和学习记录有用。
- 能说明 cell 的执行顺序和隐藏状态是 notebook 的重要注意点。
- 能说明 notebook 可以作为学习草稿使用，但反复复用的代码可能需要拆分到 script 或 module 中。

## 三个标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| notebook 是什么 | 它帮助你把 notebook 读成“把计算和解读放在一起的文档”，而不是新语法 | 理解成一种把代码、解释和执行结果一起保留下来的文档型练习空间 |
| 为什么它对学习有用 | 它把“小步练习”和“立即确认”的优势连接到当前问题上 | 抓住一点：代码可以按 cell 执行，并且结果能立刻检查 |
| 最需要小心的是什么 | 它让你把便利性和可复现风险一起看到 | 理解一点：一旦 cell 执行顺序混乱，结果解读也会出错 |

## Notebook 是代码和解释一起留下来的文档

Project Jupyter 的官方文档把 notebook 解释成：一种可共享文档，能够组合 code、plain-text explanation、data、visualization 和 interactive elements。Jupyter 架构文档也把 notebook 解释成：一种同时保存 code、output 和 markdown notes 的可编辑文档。

这里把 notebook 理解成：既是 `执行代码的文档`，也是 `把执行结果和解释一起保留下来的学习记录`。

一般的 Python script 文件通常更偏向 code。

问题场景：你想简单看看，当 script 文件里只有计算代码时，到底发生了什么执行。
输入(input)：一个学生分数列表和一个平均值计算式。
期望输出(output)：平均分会通过 `print` 打印出来。
要确认的概念：看到在 script 中，往往是 code 的执行本身先于 explanation。

```python
scores = [82, 75, 45]
average = sum(scores) / len(scores)
print(average)
```

而在 notebook 里，你可以把 explanation 和 result 一起放在同一个计算前后。例如，在一个 markdown cell 里写上 `在这个 cell 中，我们计算三位学生的平均分。`

问题场景：你想确认，在 notebook 里计算结果可以作为 cell output 直接看到，而不只是通过 `print` 保存。
输入(input)：一个学生分数列表和一个平均值计算式。
期望输出(output)：cell 最后一行的 `average` 值会被直接显示出来。
要确认的概念：确认在 notebook 中，explanation 和 output 会一起在一个文档里被阅读。

```python
scores = [82, 75, 45]
average = sum(scores) / len(scores)
average
```

从 output 可以立刻确认：平均值大约是 `67.3`。

这个差别看起来很小，但在学习里非常重要。因为 `计算了什么`、`为什么这样计算`、`如何解释这个结果` 都会一起留在同一个文档里。

## Cell 是 notebook 的基本单位

Notebook 通常由 cell 组成。Cell 是文档里的小区块。

| Cell 类型 | 英文 | 角色 |
| --- | --- | --- |
| 代码单元 | code cell | 执行 Python 代码等内容 |
| Markdown 单元 | markdown cell | 写解释、标题、列表、公式和链接 |
| 输出 | output | 展示执行结果、表、图和错误信息 |

流程可以看成下面这样。

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-cell-learning-flow-zh.mmd"
```

Notebook 学习的核心，就是短循环地重复四步：`写下问题`、`运行代码`、`看结果`、`留下解释`。

这种方式在重新学习 AI 数学和 Python 时很有用。例如在学习 sigma、mean、variance、gradient 时，只读公式会显得抽象。而在 notebook 里，可以在下面一个 cell 中立刻用数字确认。

## Notebook 很适合留下学习痕迹

Notebook 对学习有用的第一个原因，是它很容易留下思考痕迹。

例如学习平均值时，如果只留下最终代码，后来就很容易忘记为什么要做这个计算。

问题场景：你想看看，当只留下平均值计算代码而没有问题和解释时，会是什么样子。
输入(input)：一行用学生分数列表计算平均值的代码。
期望输出(output)：平均值会被算出来，但代码里不会留下为什么要这样算的解释。
要确认的概念：看到只有结果的代码，与同时保留问题和解释的 notebook 记录，学习效果是不同的。

```python
scores = [82, 75, 45]
sum(scores) / len(scores)
```

在 notebook 里，你可以在计算前留下一个问题，例如：`如果把三位学生的分数总结成一个代表值，会看到什么？`

而在计算后，可以附上这样的解释：`平均值有助于看到整组分数的中心，但像 45 这样的低分混在其中，仅靠平均值并不能充分显露出来。`

这种记录在之后重新看 P3-5 的 generalization、P3-6 的 evaluation metric，以及 P3-10.2 的 residual 和 error 时都会有帮助。

## Notebook 很适合把实验切成小步骤

第二个原因，是代码可以按 cell 分开执行。

例如可以想象下面这样的流程。

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-experiment-flow-zh.mmd"
```

同样的事在 script 中也能做，但相比一次性运行整个文件，按一个 cell 一个 cell 检查往往压力更小。

小练习可以这样切分。

第一个 cell 先准备数据。

问题场景：你想在把 notebook 练习拆成小步骤时，先放一个独立的数据准备 cell。
输入(input)：一个包含五个分数的列表。
期望输出(output)：虽然没有输出，但为后续 cell 准备好了数据。
要确认的概念：看到在 notebook 中，把数据准备拆成独立 cell，会让后面的依赖关系更容易看清。

```python
scores = [82, 75, 45, 90, 61]
```

第二个 cell 计算摘要值。

问题场景：你想从准备好的数据里只计算平均值，并确认这个中间结果。
输入(input)：上一格创建的 `scores` 列表。
期望输出(output)：平均分 `mean_score` 作为 cell output 显示。
要确认的概念：看到如果一个 cell 只做一个计算，就更容易读出在哪一步值发生了变化。

```python
mean_score = sum(scores) / len(scores)
mean_score
```

第三个 cell 再改变条件。

问题场景：你想在同一份数据里改变条件后，立刻比较会留下哪些值。
输入(input)：`scores` 列表和 `60分及以上` 这个条件。
期望输出(output)：只包含及格分数的列表被显示出来。
要确认的概念：看到 notebook 很适合一次只改变一个条件，快速比较结果差异。

```python
passed = [score for score in scores if score >= 60]
passed
```

像这样切开之后，就更容易看清：`哪一步发生了什么变化？`

## 能立刻看到 output 是它的重要优点

Notebook 会把 output 直接显示在代码下面。数字、表、图和错误信息都会留在靠近代码的位置。

这在 AI 学习里很重要。

| 学习场景 | 在 notebook 里特别容易确认的东西 |
| --- | --- |
| 公式恢复 | 小型数值计算结果 |
| 统计恢复 | 平均值、方差、样本计算结果 |
| 数据检查 | 表、行数、缺失值 |
| 可视化 | 折线图、散点图、直方图 |
| 模型实验 | loss 值、评估指标、预测结果 |

能立刻看到 output，并不意味着 `结果总是正确的`。更重要的是，你可以立刻追问：`这个值是不是比预期大？`、`表的行数对吗？`、`图是不是我想的形状？`、`错误信息是在哪个 cell 里产生的？`

Notebook 正是适合不断重复这些问题的环境。

## Notebook 的注意点：cell 执行顺序

Notebook 虽然方便，但也有必须小心的地方。最重要的是执行顺序。

看下面这个例子。

问题场景：你假定后一个 cell 要用到的变量，已经先在前一个 cell 中创建好了。
输入(input)：把 `10` 存进变量 `x` 的代码。
期望输出(output)：虽然没有输出，但会在 runtime 中生成后续 cell 依赖的状态。
要确认的概念：看到 notebook cell 不只是文档里可见的代码，还会创建 runtime 状态。

```python
x = 10
```

另一个 cell 运行下面这段代码。

问题场景：你在后一个 cell 里直接使用前一个 cell 创建的变量来做计算。
输入(input)：假定已经定义好的变量 `x`。
期望输出(output)：计算出 `15`。
要确认的概念：确认如果前一个 cell 没有执行，或顺序乱掉，后一个结果也会改变。

```python
x + 5
```

这段代码只有在前面已经创建了 `x` 时才能运行。但如果你跳过中间 cell，或者残留了以前运行过的值，那么文档里看起来的顺序和实际执行状态就可能不同。

这里需要养成下面这些习惯。

| 要检查的点 | 原因 |
| --- | --- |
| 从上到下重新执行一遍 | 减少隐藏状态 |
| 把必要的 import 放在前面 | 让所需包一眼可见 |
| 保留清晰的数据准备 cell | 让后续 cell 依赖的对象更容易看清 |
| 把解释写在结果正下方 | 为以后再次阅读保留上下文 |

正因为 notebook 可以自由执行，执行顺序反而更容易混乱。这一点比 script 更需要小心。

## 通过案例来看

### 案例 1. 一份重新确认平均值和方差的学习笔记

假设有一个重新学习统计的人，想一次理解 `mean` 和 `variance`。如果把代码都写在一个很长的 script 文件里，计算虽然能完成，但为什么要这样算，以及这个结果该如何阅读，很快就会模糊。

在 notebook 里，你可以先写一个问题，例如 `如果把五个分数压缩成一个代表值，会看到什么？`，然后在下一个 cell 里计算平均值，再在正下方附上解释，例如 `仅靠平均值，并不能充分显露其中混入了一次低分。` 如果接着再放一个 variance 计算 cell，就能在同一组数据里继续比较离散程度。

这个流程说明：notebook 不只是执行器。人可以把问题、计算、输出和解释绑在同一份文档里，等以后再次打开时，能够马上恢复当时到底检查了什么。

同时，这个案例也暴露了 notebook 的一个注意点。如果只重新执行修改平均值的 cell，而没有修正解释 cell，那么文档中可见的说明和真实计算结果就会发生偏离。所以 notebook 既要被当成 `带着执行结果的文档`，也要被当成 `必须重新执行和验证的记录`。

## Notebook 不会取代 script

Notebook 很适合学习和探索，但并不适合所有场景。

那些需要反复执行、要在其他项目中复用、或者必须自动化的代码，通常更适合拆分成 `.py` script 或 module。

| 场景 | notebook 更好吗？ | script 更好吗？ |
| --- | --- | --- |
| 第一次实验一个概念 | 是 | 也可以，但解释要另外保留 |
| 一边看数据和图一边做解读 | 是 | 也可以，但检查中间结果会更不方便 |
| 每天自动运行同样工作 | 可能不利 | 是 |
| 在多个项目里复用函数 | 可能不利 | 是 |
| 连同实验记录一起共享文档 | 是 | 需要另备文档 |

因此，这里把 notebook 看成学习记录和小实验工具。等代码变长、需要重复执行时，就需要判断是否迁移到 script 和 package 结构里。

## 在 AI 再学习里如何使用 notebook

对这份文档的读者来说，notebook 更接近 `恢复理解的工作台`，而不是 `提交正确答案的文件`。

比较好的使用顺序如下。

1. 先在 markdown cell 里写下问题。
2. 在 code cell 里写一个小数据或小数字例子。
3. 输出结果。
4. 简短解释结果是否符合预期。
5. 从上到下重新执行所有 cell。

例如在学习概率和统计时，可以先从一个问题开始：`如果数据改变，样本平均值会变化多少？`

问题场景：你想在一个 notebook cell 中比较两个不同样本的平均值。
输入(input)：两个由不同数值组成的样本列表 `sample_a` 和 `sample_b`。
期望输出(output)：两个样本的平均值一起显示出来。
要确认的概念：看到 notebook 很适合把问题、计算和解释一起保留成一个小型样本比较实验。

```python
sample_a = [10, 12, 13, 11, 14]
sample_b = [8, 16, 9, 15, 12]

mean_a = sum(sample_a) / len(sample_a)
mean_b = sum(sample_b) / len(sample_b)

mean_a, mean_b
```

如果接着再写上这样的解释：`两个样本的取值构成不同，但平均值仍可能相近。仅靠平均值不能揭示分布中的全部差异。` 那么计算结果就会留下来，成为一条记录。

这种方式在之后的机器学习实践里也会持续出现。不要试图一次把数据准备、模型训练、评估和解释全部完成，而是按 cell 去确认一个个小问题。

## 检查清单

- 能把 notebook 解释成同时包含代码、解释和输出的计算文档。
- 能区分 code cell 和 markdown cell。
- 能说明为什么 notebook 对 AI 数学与 Python 练习记录有用。
- 能说明 cell 执行顺序会影响结果。
- 能说明 notebook 不会完全取代 script。
- 能在学习 notebook 中同时留下问题、代码、输出和解释。
- 能把 notebook 说明成执行工具和学习记录文档两种角色。

## 来源与参考资料

- Project Jupyter, [Project Jupyter Documentation](https://docs.jupyter.org/en/latest/){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation 4.1.1 alpha，确认日期：2026-07-19。用于确认 notebook 是把代码、说明、数据、可视化和交互放在一起的文档。
- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation 4.1.1 alpha，确认日期：2026-07-19。作为区分 notebook document、user interface、kernel 等组成部分的背景依据。
- Google, [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }, Google Colab，确认日期：2026-07-19。用于确认在浏览器 notebook 环境中一起执行和记录代码与说明的示例。

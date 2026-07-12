# Part 2. 基础恢复

> Section ID: `P2-index`
> Version: `v2026.07.12`

Part 2 是在重新学习机器学习与深度学习之前，恢复数学、Python、数据工具与文档管理感的一段。这里不会深入证明数学，也不会要求把所有 Python 语法都背下来。它要建立的是：让你在 Part 3 中阅读模型训练、数据切分、评估、过拟合和泛化时，能够跟上说明，并用小段代码亲自确认的基础。

在同一个 Part 内，Part 2 也尽量把主要概念的详细说明先放在一个代表 Section 中。后面的章节只保留当前语境需要的最小连接。像公式阅读、向量与矩阵、导数、概率、优化、数组与表格数据这些会反复再遇到的概念，应先读代表 Section，再在重新出现时结合 [概念词汇表](/AiBook/en/reference/concept-glossary/) 回头确认。

这里最核心的目的，是 `让 AI 文档与示例代码里反复出现的计算语言重新变得可读`。公式、数组、表、图、运行环境、Git 历史不是彼此分离的话题。它们是在读取模型计算、检查数据集、可视化结果、留下学习记录时一起被使用的工具。

读这一 Part 时，要不断确认诸如 `这个公式在计算什么`、`这段代码输入了什么值，又在检查什么结果`、`这个工具为什么现在需要` 这样的问题。数学、Python、NumPy、Pandas、Git 会连成一组共同准备，服务于 Part 3 的机器学习正文阅读。

所以 Part 2 做的是重新连接基础。

1. 重新阅读公式记号。
2. 恢复线性代数、导数、概率、统计、优化的直觉。
3. 复习 Python 运行环境与语法。
4. 用 NumPy、Pandas、Matplotlib 检查小计算。
5. 用 Git 管理文档与代码变更历史。
6. 在进入 Part 3 机器学习之前建立检查标准。

## 先抓住的基准

在完整阅读 Part 2 之前，先抓住下面四行就够了。

| 现在先抓住的基准 | 为什么重要 | 卡住时先回去的位置 |
| --- | --- | --- |
| 公式在计算什么 | 为了把平均值、误差、损失、梯度重新读成句子 | `P2-1`, `P2-2`, `P2-4`, `P2-5`, `P2-6` |
| 数组和表是什么形状 | 为了读懂 `X`、`y`、sample、feature | `P2-11`, `P2-12` |
| 代码在哪里运行 | 为了不把 Colab、本地 PC、终端、notebook 混在一起 | `P2-3.5`, Chapter 7, Chapter 10 |
| 能不能留下“改了什么、为什么改” | 为了把实验与文档可复现性一起带走 | Chapter 13, Chapter 14, `P2-15.2` |

也就是说，Part 2 不是一个把数学、Python、工具各自单独学完的 Part，而是一个恢复 `在 Part 3 中读取数据与学习流程所需最小共同语言` 的 Part。

## 这一 Part 的目的

Part 2 是把你很久以前学过，或者只零散接触过的数学与软件工具，重新整理成 AI 再学习语言的一段。

人们在重新学习 AI 时会卡住，不一定只是因为数学本身难，而是因为 \(x\)、\(\sum\)、\(\frac{1}{n}\)、向量、矩阵、导数、梯度、概率、平均值、损失这些表达会同时出现在代码、数据和模型说明里。

这一 Part 的关键主轴如下。

| 代表轴 | 先读的代表位置 | 为什么需要先看 |
| --- | --- | --- |
| 数学在 AI 计算中的角色 | `P2-1.1` | 为了把数学读成计算语言，而不是考试科目 |
| 公式、代码、数据之间的连接 | `P2-1.2` | 为了在后面的例子里把文档、代码、结果一起读 |
| sigma、log、指数记号 | `P2-2.1`, `P2-2.2`, `P2-2.4` | 为了读懂压缩记号和概率分数语言 |
| 向量、矩阵、内积、距离 | `P2-3.1`, `P2-3.4`, `P2-11.1` | 为了读懂数据形状和向量比较标准 |
| 导数、chain rule、概率、优化 | `P2-4.1`, `P2-4.6`, `P2-5.1`, `P2-6.1` | 为了读懂损失、梯度、反向传播、不确定性与学习方向 |

如果分别学习 Python、NumPy、Pandas、Matplotlib、Git，它们会散开。但在机器学习语境里，它们会连成一条流程：用 Python 执行小计算，用 NumPy 处理向量和矩阵，用 Pandas 读取表格数据，用 Matplotlib 画出数据和学习流程，再用 Git 留下文档、代码和实验记录的变更历史。

Part 2 恢复的正是这种连接。目标不是专家级数学证明，也不是软件熟练度，而是让你在阅读 Part 3 机器学习说明时，能够跟上 `这个计算到底在做什么`。

### 当前阅读原则

Part 2 应按下面这些原则来读。

| 原则 | 含义 |
| --- | --- |
| 先看角色，再看工具 | 先抓住 NumPy 负责数组计算，Pandas 负责表数据，Matplotlib 负责可视化，Git 负责变更历史管理。 |
| 如果卡住，就短暂绕回补充学习 | 像不同操作系统安装、终端、class、传统数据结构这类超出当前范围的内容，只在补充学习里按需要回收。 |
| 持续想象它在 Part 3 会回到什么场景 | 持续确认这其实是在为读懂 `X`、`y`、sample、feature、loss、metric` 这些表达做准备。 |

把完整阅读 Part 2 时更实务化的问题压缩起来，可以写成下面这样。

| 阅读中要一直追问的问题 | 为什么需要这个问题 |
| --- | --- |
| 现在看到的内容会连到 Part 3 的哪个场景？ | 让说明不会只在当前 Section 里自我封闭 |
| 如果在这里卡住，应该短暂回到哪里？ | 让你不必从头把 Part 2 全部重读一遍 |
| 在这里必须留下的最小句子是什么？ | 让你能从长篇说明里挑出真正该带走的标准 |

## 这一 Part 的目标

读完 Part 2 后，目标是达到大致下面这种理解程度。

- 能把 variable、function、expression、sigma、limit 重新读成 AI 文档阅读语言。
- 能说明为什么 log、exp、log loss 这类表达会反复出现。
- 能从数据与模型计算视角说明 scalar、vector、matrix、vector space、matrix multiplication。
- 能把 dot product、norm、distance、similarity 说明成向量比较标准。
- 能把 derivative、gradient、loss function、gradient descent 理解成 `为了把值调得更好而需要的方向与标准`。
- 能把 composite function 与 chain rule 说明成 backpropagation 之前的最小背景。
- 能把 probability、distribution、mean、variance、sample、estimation、error 用成数据判断的基本语言。
- 能区分 Python 运行环境、终端、虚拟环境、依赖与 notebook 执行流程。
- 能说明 Python 的 value、variable、list、dictionary、loop、function、class 的入门角色。
- 能把 NumPy array、shape、axis、indexing、slicing、broadcasting、vectorization 与模型计算连接起来。
- 能通过 row、column、index 阅读 Pandas DataFrame，并形成数据集准备的直觉。
- 能用 Matplotlib 视觉化地检查公式、分布、关系与损失曲线。
- 能把 Git commit 与 branch 理解成学习文档可复现性管理工具。

## 这一 Part 解释的范围与不解释的范围

Part 2 是面向 AI 学习的基础恢复 Part，因此正文范围内会解释以下内容。

- 重新阅读公式与计算语言的最小标准
- 线性代数、导数、概率、统计、优化的入门直觉
- Python 运行环境与基本语法
- NumPy、Pandas、Matplotlib、Git 的学习型角色

相对地，下面这些内容不会在这一 Part 中全部深入展开。

- 数学定理与证明的严密推导
- Python 高级语法与大规模软件设计
- 数据工程与协作自动化工具的完整体系
- 像组合数学单元那样长篇展开搜索空间增长

这并不是回避解释，而是范围控制。Part 2 的责任是 `让计算语言重新变得可读`，而高级工具用法与更严格的数学证明留给后续学习或单独参考资料。对于搜索空间中情况数迅速增长的直觉，先通过 P1-7.1 的表格与例子抓住，这里不再另开一个组合论 Section 重新展开。

## 面向入门读者的阅读标准

Part 2 会同时出现数学、Python、数据工具与 Git，所以一开始可能看起来像几个不同科目。最初不要试图把所有语法与公式一次性全部学完，而是先按下面三个问题来读。

| 先抓住的问题 | 为什么需要这个问题 | 在这一 Part 中抓到什么程度就够 |
| --- | --- | --- |
| 这个公式在 `计算什么`？ | 即使符号陌生，只要先抓住计算目的，就还能继续进入下一节。 | 读懂像平均、和、梯度、误差这样 `是在减少什么或比较什么`。 |
| 这段代码输入 `什么值`，又展示 `什么结果`？ | 必须先看到输入、计算、输出的流程，才能跟上练习，而不是先困在 Python 语法里。 | 能读懂一个小 list、array、table 会产出什么输出。 |
| 这个工具 `为什么现在` 需要？ | 如果只记工具名，很快就会散掉。 | 先抓住角色：NumPy 用于数组计算，Pandas 用于表数据，Matplotlib 用于可视化，Git 用于变更历史。 |

1. 数学是把计算简洁写下来的语言。
2. Python 是实际执行这种计算的工具。
3. NumPy、Pandas、Matplotlib 帮你读取和检查数据。
4. Git 负责把你改了什么留下来。

即使工具名很多，也只需要先抓住下面五条主流。

| 先抓住的主流 | 为什么现在需要 | 后面立刻会再次使用的位置 |
| --- | --- | --- |
| 公式、平均、误差、梯度 | 因为要读懂 Part 3 中损失与评估的说明 | Part 3 |
| Python 的输入、计算、输出流程 | 因为要跟上示例代码到底在检查什么 | Part 3, Part 4, Part 5 |
| NumPy 的数组、`shape`、`axis` | 因为要读懂数据方向和模型输入形状 | Part 3, Part 4, Part 5, Part 6 |
| Pandas 的 row、column、`DataFrame` | 因为要在表里区分 feature 与 label | Part 3 |
| Git 的 commit 与变更理由记录 | 因为要把实验比较和文档历史一起留下 | Part 3, Part 4, Part 7 |

## 它解释什么

Part 2 由 15 个 Chapter 组成。

首先，它把数学重新读成计算语言。它恢复 variable、function、expression、sigma、limit，并把 log 与 exponential 重新连到后面 Parts 里再次出现的概率分数语言。它建立的是：在代码与数据中再次确认公式的视角。

接着，它处理读取模型计算所需的核心数学。在线性代数中，它看 scalar、vector、matrix、vector space、matrix multiplication，然后还要抓住 `应该怎样比较向量`，通过 dot product、norm、distance、similarity 来完成。对导数，它看 rate of change、slope、gradient，以及为什么学习需要导数，再通过 composite function 与 chain rule 加强 backpropagation 之前的最小连接。对概率与统计，它整理怎样把不确定性写成数字，怎样通过 mean、variance、distribution、sample、estimation、error 去读数据集合。这里不是完整对比频率主义与贝叶斯主义，而只是恢复 `long-run frequency` 与 `degree of belief` 这条最小区分，并把 Bayes' rule 留在“用新证据更新信念”的直觉层级。对优化，它从“不是直接写出最好答案，而是寻找更好的值”进入。

中段会处理运行环境与 Python 基础。它区分 Colab 与本地 PC、terminal 与 shell、Python interpreter 与 script、virtual environment 与 package、dependency 与 reproducibility。然后恢复 Python 的 value、variable、type、list、dictionary、loop、function、class 的基本直觉。

后半部分处理数据结构与数据工具。它建立 array、table、tree、graph 的直觉，再看如何通过 Jupyter 与 Colab notebook 同时留下代码与说明。它用 NumPy 计算向量与矩阵，用 Pandas 处理表格数据，用 Matplotlib 检查数字的形状。

最后，它处理 Git 与文档管理。在文档、示例代码、图片、实验记录会一起变化的项目里，变更历史与可复现性很重要。Part 2 的结尾会整理把公式搬进代码的小流程，并检查进入 Part 3 前所需的直觉。

## 为什么需要

学习机器学习时，很多说明会以如下形式出现。

1. 有输入数据 \(X\) 和标签 \(y\)。
2. 模型产生预测值 \(\hat{y}\)。
3. 损失函数把预测与真实值之间的差变成一个数字。
4. 学习沿着减少这个损失的方向调整参数。
5. 评估在没见过的数据上检查结果。

要读懂这种说明，需要几个基础同时到位。你需要能够把 \(X\) 和 \(y\) 读成数组与表，把损失读成平均与求和，能通过图去检查学习流程，还要能追踪：示例代码在什么环境里运行，结果图和原稿在哪个 commit 里一起发生了变化。

Part 2 不会把这些基础都挖得太深。相反，它只准备最小语言与实践直觉，让你在 Part 3 阅读模型与数据流时不会直接被卡住。

## 进入 Part 3 前的快速回返表

| 在 Part 3 卡住的表达 | 先回到 Part 2 的哪里 |
| --- | --- |
| `X`, `y`, feature, label | `P2-12.3`, `P2-15.2` |
| `shape`, `axis`, row, column | `P2-11.2`, `P2-15.2` |
| mean, error, loss | Chapter 5, Chapter 6, `P2-15.2` |
| `fit`, `predict`, train/test | `P2-12.3`, `P2-15.2` |
| Colab, terminal, notebook, runtime environment | `P2-3.5`, Chapter 7, Chapter 10 |

## 这一 Part 不完成的问题

因为 Part 2 专注于基础恢复，所以它有意把下面这些问题留给 Part 3 及之后。

- 损失与优化在真实模型训练中怎样连接起来？
- 为什么需要 train、validation、test 的切分？
- 为什么神经网络和深度学习结构需要更大的计算资源？

这些问题会在 Part 3、Part 4、Part 5 的正文说明里被回收。

## 读完这一 Part 后会形成的理解

读完这一 Part 后，你不再需要把数学与软件工具分别记忆，而可以把它们看成一条共同的学习流程。

1. 公式写下计算意图。
2. Python 执行小计算。
3. NumPy 复用向量与矩阵计算。
4. Pandas 让数据集被读成表。
5. Matplotlib 让数字的形状被检查。
6. Git 留下原稿、代码与结果的变更历史。

一旦形成这种理解，在 Part 3 的机器学习正文里，你就不会再把 `X`、`y`、`fit`、`predict`、loss、metric、train、validation、test 这些表达看成完全陌生的语言。Part 2 不是所有基础都学完的阶段，而是为进入机器学习建立最小共同底层的阶段。

## 完成标准

- 能说明公式里的变量、函数、sigma、平均值、误差怎样连到实际计算步骤。
- 能说出向量与矩阵在数据和模型计算中出现在哪里。
- 能用入门水平解释导数、梯度、损失函数、梯度下降。
- 能把 probability、distribution、mean、variance、sample、estimation 区分成数据判断语言。
- 能说明 Python 代码在哪里运行，以及 Colab 与本地 PC 的差别。
- 能说明 Python list、dictionary、loop、function、class 的基本角色。
- 能用小例子确认 NumPy array 的 shape、axis、indexing、slicing、broadcasting。
- 能围绕行列读取 Pandas DataFrame，并说明学习型数据集准备为什么重要。
- 能用 Matplotlib 检查函数形状、散点图、直方图与损失曲线。
- 能从文档、代码、图片和实验记录的变更历史管理角度说明 Git commit 与 branch。
- 在进入 Part 3 前，能说出 `X`、`y`、sample、feature、fit、predict` 的基本含义。

## 检查清单

- 能说明公式、数组、表、图与 Git 会在 Part 3 里连成同一条学习流程吗？
- 看到一个卡住的表达时，能选出应该回到哪个 Chapter 吗？
- 能把 `X`、`y`、shape、mean、error、runtime environment` 分别用一句话解释吗？

## 来源与参考

本文是整理 Part 2 目的与学习路径的原创概览，不直接引用外部资料。

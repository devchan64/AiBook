# P2-10.3 把笔记本整理成可重新执行的记录

> Section ID: `P2-10.3`
> Version: `v2026.07.11`

在 P2-10.1 中，我们把 notebook 看成同时包含 code、explanation 和 output 的计算文档。在 P2-10.2 中，我们又从执行位置和文件访问的角度区分了 Jupyter、Colab 和本地执行。

现在再往前走一步。Notebook 作为学习记录很有用，但当 cell 被多次执行后，文档里看到的顺序和实际执行状态可能会分离。所以 notebook 必须同时被整理成 `可读的文档` 和 `可复现的记录`。

这里说明 `reproducible record`、`execution order`、`hidden state`、`runtime state` 的基本区分。关于 `notebook` 与 cell 结构的代表性说明放在 P2-10.1，执行位置差异放在 P2-10.2，而 `reproducibility` 的代表性说明放在 P2-7.5 和[概念词汇表](../../../reference/concept-glossary.md)。这里关注的是：如何整理这些记录，让它们以后仍然值得信任。

放回 Part 2 的流程里看，Chapter 7 处理的是 `在哪里执行`，Chapter 8 到 9 处理的是 `写什么、用什么句子写`，而 Chapter 10 处理的是 `怎样把这些执行和输出保留下来，并且以后还能再读`。只有这个标准立起来，紧接着的 Chapter 11 到 14 才不会读成一串新工具名称，而会读成一种准备流程：在 notebook 里计算数组、读取表格、检查图，再用 Git 留下记录。

本节关注的不是 notebook 美化技巧，而是怎样把执行结果整理成以后还能继续相信的记录。如果前两节讨论的是 notebook 是什么，以及它在哪里运行，那么这里看的就是：要让 notebook 以后还能重新执行、重新解释，到底必须留下什么。这样一来，Chapter 11 到 14 里的工具也更容易被读成“重新确认计算和解释的记录流程”，而不是新的功能清单。

| 本节现在要抓住的内容 | 紧接着会延伸到的问题 | 之后再次出现的位置 |
| --- | --- | --- |
| 好的 notebook 必须同时是可读文档和可重跑记录 | 会延伸到在 Chapter 11 到 14 里，计算、表格、可视化和 Git 记录应该按什么顺序保留 | 之后会在所有练习 notebook、Colab 共享和项目记录中反复出现 |
| cell 顺序和 hidden state 会改变结果 | 会延伸到为什么需要“重启后从上到下运行”的习惯 | 之后在调试、可复现性检查和协作共享中都持续重要 |
| 在 notebook 中验证过的代码，最终会到达应拆成函数和 `.py` 文件的时点 | 会延伸到如何判断记录和可复用代码的边界 | 之后会在工具脚本、项目结构和 Git 记录整理中再次使用 |

| 术语 | 本节先要抓住的含义 |
| --- | --- |
| reproducible record | 一种 notebook，即使以后重新打开，也能用同样流程重新得到执行和解释 |
| execution order | cell 实际被执行的顺序 |
| hidden state | 文档里看不到，但 runtime 中还残留的变量、import 和临时结果 |
| runtime state | 只存在于当前 session 中的变量、包和内存状态 |
| setup cell | 放在前部、集中处理 package import、选项和数据准备的 cell |

## 本节的范围

本节不讨论如何把 notebook 做得更漂亮。不讨论 Jupyter 扩展、Colab 高级设置、自动部署或大规模实验跟踪工具。这里的范围只到“把 notebook 整理成可重跑记录的习惯”为止，而更大的实验跟踪体系，会在之后的补充学习 P3-9.3 和 Part 6 项目记录中再次连接。

本节回答以下问题。

- 为什么 notebook 要从上到下重新跑一遍？
- code cell、markdown cell 和 output 应该按什么顺序组织？
- package、data file 和 randomness 应该写在哪里？
- 在 Colab 和本地执行中，应分别怎样小心 reproducibility？
- 从 notebook 开始的代码，什么时候适合拆分成 `.py` 文件？

本节把 Part 2 Chapter 7 Section 5 的 dependency 和 reproducibility、P2-10.1 的 notebook 优缺点，以及 P2-10.2 的执行环境差异，重新连接成练习记录的习惯。

## 本节的目标

- 能说明为什么 notebook 要整理成可重新执行的学习记录。
- 能说明 execution order 和 hidden state 为什么会让 notebook 结果变得混乱。
- 能说明为什么环境、package 和数据准备 cell 应该放在 notebook 前部。
- 能说明在 Colab 共享中，notebook 内容和 runtime 状态是不同的东西。
- 能说明在什么时点，notebook 中验证过的代码应该拆分成函数和 script。

## 先要抓住的标准

本节最先要抓住的标准是：`好的 notebook 既是可读文档，也是可重跑记录。`

| 现在看 notebook 时要看什么 | 先问的问题 |
| --- | --- |
| cell 顺序 | 它能从上到下重新运行吗？ |
| import 和 setup | 所需 package 和 setting 是否都集中在前部？ |
| 数据准备 | 用了哪些文件或例子，是否清楚？ |
| output 与解释 | 数字和图的下方有没有意义说明？ |
| runtime 状态 | 有没有依赖隐藏变量，也能重新运行？ |

也就是说，notebook 应该按 `即使重新跑，也能留下同样流程吗？` 来读，而不只是按 `里面有代码吗？` 来读。

## 三个标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 好的 notebook 到底哪里不同 | 它让你把文档质量和可重跑性一起看 | 阅读流程和执行流程必须一起被整理 |
| 为什么必须关心 cell 顺序 | 它把 notebook 的 hidden state 问题和文档结构本身连接起来 | 理解 notebook 虽然看起来像文档，但实际上也是真正的执行记录 |
| 它之后会通向什么 | 它让你提前看见“记录型 notebook”和“可复用代码”之间的边界 | 整理好的 notebook 会成为 script 和项目代码的起点 |

## Notebook 既是文档，也是执行记录

Jupyter Notebook 文件是带有 `.ipynb` 扩展名的 JSON 文档。nbformat 文档解释说，notebook 包含 cell 列表和 metadata，而每个 cell 可以带有 input 和 output。Jupyter 架构文档也把 notebook 解释成同时存储 code、output 和 markdown notes 的文档。

这里把这种结构理解成下面这样。

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-structure-flow-en.mmd"
```

这里重要的是：保存在文件里的内容，和执行中的状态，并不是同一回事。

Notebook 文件里可以留下 code 和一部分 output。但变量、import 过的 package、临时文件和内存状态都活在 runtime 里。一旦 runtime 被重启，这些状态就可能消失。

所以，仅仅保存 notebook 还不够。还必须检查这个 notebook 以后是否真的还能重新执行。

## 做出一个能从上到下运行的流程

好的学习型 notebook，应该能从上到下被阅读，也能从上到下被执行。

下面这个流程可以作为默认标准。

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-rerun-flow-en.mmd"
```

这种结构不是形式主义，而是思考顺序。

先写你想确认什么。然后加载需要的 package、准备数据、运行计算。看到结果后，再写解释。

如果这个顺序崩掉了，那么以后再打开 notebook 时，就很容易失去：`为什么要做这个计算？`、`用了什么数据？`、`这个结果是什么意思？`

## 第一格先写目的

在 notebook 前部，应先把目的写在 code 之前。

例如可以这样开始：`This notebook calculates the mean and variance of a small score dataset and checks how the center and spread of data differ.`

这一句话到后来会变得非常重要。因为 notebook 一旦不断增加 cell，就会很快变长。没有目的时，实验会散掉，结果也会变得不清楚，不知道到底在说明什么。

在目的 cell 里，简短写下下面这些内容。

| 项目 | 为什么要写 |
| --- | --- |
| 要检查的问题 | 防止实验散掉 |
| 使用的数据 | 明确结果的范围 |
| 预期输出 | 定义到底该看什么 |
| 不处理什么 | 防止 notebook 过度膨胀 |

Notebook 其实和 Section 很像。一个 notebook 最好也尽量只围绕一个中心问题。

## 把 package 和 setting 集中放在前面

如果 import 散落在 notebook 中间，之后重新运行时，就很难找到到底需要哪些 package。

一个好的习惯，是在前面放一个 setup cell。

问题场景：你想在 notebook 前部一眼看出到底用了哪些 package。
输入(input)：`numpy`、`pandas`、`matplotlib` 的 import 代码。
期望输出(output)：虽然没有输出，但后面 cell 需要的 package 名字已经准备好。
要确认的概念：看到把 import 集中在前部，会让 notebook 重跑和 dependency 检查都更容易。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

这个 cell 告诉你：`这个 notebook 到底用什么工具？`

在 Colab 中，安装 package 的 cell 也要放在前面。

问题场景：你想让收到共享 Colab notebook 的人先安装需要的 package。
输入(input)：一个 `%pip` 命令，用于安装 `numpy`、`pandas`、`matplotlib`。
期望输出(output)：这些 package 会被安装到当前 kernel 里。
要确认的概念：看到把 package 安装 cell 放在前面，会让别人更容易准备出类似 runtime。

```python
%pip install numpy pandas matplotlib
```

在 Colab 或 Jupyter 里，你也常会看到 `!pip install ...`。`!` 表示在 notebook cell 中执行 shell 命令。但对 Python package 安装来说，像 `%pip` 这样的 IPython magic command 往往和当前正在运行的 kernel 更匹配，因此这里优先介绍 `%pip`。

此处重要的不是安装方法本身，而是 package 安装与 import 必须集中在前面，这样别人才能明白 notebook 重跑需要做哪些准备。

## 保留清晰的数据准备 cell

Notebook 练习失败的常见原因之一，是文件路径。

在本地 PC 上，下面这个路径可能存在。

问题场景：你想通过最简单的字符串例子，看懂为什么同一个 notebook 在不同执行环境里会有不同文件路径。
输入(input)：一个基于本地项目的 CSV 文件路径字符串。
期望输出(output)：虽然没有输出，但代码预期的文件位置变得明确。
要确认的概念：看到可重跑 notebook 必须在代码里明确留下文件路径和数据位置。

```python
data_path = "data/scores.csv"
```

但在 Colab 里，同样的文件可能不存在。路径会因为你是上传文件、连接 Google Drive，还是从 GitHub 下载，而发生变化。

所以在数据准备 cell 中，下面几种情况至少有一种应当明确。

| 情况 | notebook 里要留下什么 |
| --- | --- |
| 小型示例数据 | 直接在代码里创建 |
| 本地文件 | 写出文件位置和文件夹结构 |
| Colab 上传 | 写明需要上传 |
| Drive 文件 | 写明 Drive 连接与权限条件 |
| 从网络下载的文件 | 写明下载来源和确认日期 |

在这里，如果可能，更推荐直接把小型示例数据写进代码。

问题场景：为了不被文件路径问题打断、只专注于概念本身，你把一个小型示例数据直接写进代码里。
输入(input)：一个包含五个分数的列表。
期望输出(output)：虽然没有输出，但后续 cell 立即拥有要用的数据。
要确认的概念：看到在学习初期，比起文件型设置，代码里的小数据更有利于重跑和理解。

```python
scores = [82, 75, 45, 90, 61]
```

这对真实项目可能还不够，但对概念学习很好。它能让你把注意力放在平均值、方差、样本、误差这些概念上，而不是文件问题上。

## 不只留下 output，也要留下解释

Notebook 可以保存 output。但如果只留下 output，学习记录仍然不够。

例如，假设 notebook 里只留下了下面这个 output。

问题场景：你想看看，为什么只保存一个数字的 output，后来会很难解释。
输入(input)：一个作为 cell output 留下来的单个数字 `67.3`。
期望输出(output)：只剩下一个脱离上下文的数字，不知道它是平均值还是损失值。
要确认的概念：看到 output 不能只留下数值，而要在下面配上解释。

```python
67.3
```

以后再看时，很难知道这个数字到底是 mean、accuracy 还是 loss。

所以应该在 output 正下方附上一句短解释，例如：`The mean is 67.3. But because a low value like 45 is included, the whole distribution is hard to explain through the mean alone.`

这一句话会改变学习记录的质量。Notebook 不应该只是堆放代码的文件，而应该是解释计算结果的记录。

## cell 执行顺序会改变结果

Notebook 可以自由执行 cell。这个优点同时也是风险。

想象下面这种情况。

问题场景：你先在一个 cell 里定义一个超参数值。
输入(input)：代码 `learning_rate = 0.1`。
期望输出(output)：虽然没有输出，但当前学习率值会存进 runtime。
要确认的概念：看到 notebook 中变量状态会随着 cell 执行顺序改变。

```python
learning_rate = 0.1
```

然后在另一个 cell 中又重新修改这个值。

问题场景：在同一个 notebook 里，你又在另一个 cell 覆写了这个变量。
输入(input)：代码 `learning_rate = 0.01`。
期望输出(output)：虽然没有输出，但 runtime 里的当前值会被新值覆盖。
要确认的概念：确认文档里看到的顺序，和实际最后的执行状态，可能不是一回事。

```python
learning_rate = 0.01
```

文档里从上到下能看到两个值，但在实际 runtime 中，会留下最近执行的那个值。如果你先执行下面那个 cell，再执行上面的 cell，结果又会再次变化。

所以，一个重要 notebook 应按下面方式检查。

1. 重启 runtime。
2. 从第一个 cell 到最后一个 cell 按顺序执行。
3. 检查是否有报错的 cell。
4. 检查 output 是否和 explanation 对得上。
5. 清理不必要的临时 cell。

经历这个过程后，notebook 才更接近 `可以重新执行的记录`，而不只是 `在我的电脑上偶然跑通一次的记录`。

如果把这个检查顺序再写短一点：

| 检查步骤 | 为什么需要 |
| --- | --- |
| 重启 runtime | 为了清掉 hidden state |
| 从上到下执行 | 为了让文档顺序和执行顺序一致 |
| 检查错误 | 为了确认没有漏掉必要的 cell |
| 检查 output 和 explanation | 为了确认结果和解释一致 |
| 清理不必要的 cell | 为了不让可重跑记录变得模糊 |

## 固定 randomness，或至少解释它

在 AI 与统计练习里，random 元素经常出现。抽样、打乱数据、设定模型初值时，结果都可能发生变化。

在这里，仅仅说明“这里存在 randomness”，就已经是一个好的开始。

问题场景：你想看一个例子，通过固定 seed 来让同样的随机抽样可以再次确认。
输入(input)：一个 seed 为 `42` 的随机生成器，以及从五个值里抽三个值的代码。
期望输出(output)：一个以可复现方式输出的样本列表。
要确认的概念：看到在带有随机性的练习中，留下 seed 会让同样结果流更容易再次检查。

```python
rng = np.random.default_rng(seed=42)
sample = rng.choice([10, 20, 30, 40, 50], size=3, replace=False)
sample
```

这里的 `seed` 可以看成重新制造同样随机流的起点值。不是每一个 notebook 都必须固定 seed，但如果你想再次看到同样结果，留下 seed 是好的做法。

一个要注意的点是：seed 并不能解决所有 reproducibility 问题。结果仍然可能因为 package 版本、执行环境、硬件或并行处理方式而不同。本节不深入展开这些细节。

## 在 Colab 共享中，notebook 共享和 runtime 共享不是一回事

Colab FAQ 说明，共享 notebook 时，text、code、output、comments 等 notebook 内容可以共享，但 virtual machine、runtime 文件和已安装的库状态不会一起共享。

因此，共享 Colab notebook 时，应检查下面这些点。

| 要检查什么 | 原因 |
| --- | --- |
| 是否有安装所需 package 的 cell | 对方的 runtime 中可能没装这些 package |
| 是否有准备数据文件的方法 | 我 runtime 中的文件不一定会被共享 |
| 是否需要 Drive 文件权限 | 对方可能访问不到我的私人 Drive 文件 |
| 是否能从上到下运行 | 这是在确认它不依赖 hidden state |
| output 是否已经过时 | 已保存 output 可能和当前代码的结果不同 |

这一点对本书里的示例 notebook 也很重要。读者打开链接时，不应该只看到代码，还应该知道什么必须先运行。

## 什么时候该从 notebook 迁移到 script

从 notebook 开始的代码，随着时间推移会变长。到某个时点，把它迁移到 `.py` script 会更合适。

当下面这些信号出现时，就应该考虑分离。

| 信号 | 含义 |
| --- | --- |
| 同样的代码在多个 cell 里重复出现 | 它可以被打包成函数 |
| cell 顺序经常打乱 | script 的执行顺序可能更安全 |
| 每次都要做同样的预处理 | 它可以搬进单独的函数或 module |
| 其他 notebook 里也会用到同样的代码 | 可能需要一个公共 `.py` 文件 |
| 需要自动执行 | script 比 notebook 更自然 |

流程可以这样看。

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-to-module-flow-en.mmd"
```

这里并不要求你一开始就建立 package 结构。先在 notebook 中理解，等重复代码出现后再打包成函数，等复用真正变重要时再拆分成文件。

## 学习型 notebook 的最小模板

制作学习型 notebook 时，可以把下面这个流程当成默认模板。

| 顺序 | cell 角色 | 例子 |
| --- | --- | --- |
| 1 | purpose | 这个 notebook 要确认的问题 |
| 2 | environment | package 安装、import、版本检查 |
| 3 | data | 小型示例数据或文件路径 |
| 4 | calculation | 一次只运行一个概念 |
| 5 | output | 数字、表、图、错误信息 |
| 6 | interpretation | 结果意味着什么 |
| 7 | summary | 学到了什么、下一个问题是什么 |

这个模板不是形式主义，而是一个检查表。随着 notebook 变长，你要不断检查 `purpose、environment、data、calculation、output、interpretation` 是否都还在。

在进入 Part 2 下一章之前，只需要检查三件事。Notebook 能不能从上到下重新运行？Package、data 和 output explanation 是否都留在前部附近？重复代码是否已经准备好将来迁移到函数和 `.py` 文件？只要这个标准成立，后面的 Chapter 11 到 14 就会继续读成：在整理好的 notebook 中计算数组、读表、检查图、用 Git 留下记录，而不是在继续背新工具名称。

换句话说，P2-10 的目标并不是把 notebook 完全学透，而是建立一个标准，让 Part 3 之前的计算记录能以可重跑的形式留下来。

## 通过案例来看

### 案例 1. 今天能跑，明天却不能跑的 notebook

假设一个学习者在 Colab 中做数据预处理练习，cell 跑得很随意。中间执行了文件上传 cell，又在另一个 cell 里改了变量名，最后图也画出来了。那一天，文档看起来像是完成了。

但第二天重新打开 runtime，再从上到下执行时，文件可能不存在，后面的 cell 可能引用了前面并不存在的变量，而保存的 output 也可能已经和当前代码不一致。人会觉得：`昨天还能跑，为什么现在不行？` 但实际上，notebook 只是被留下成了 `可读文档`，却没有被整理成 `可重跑记录`。

为了减少这个问题，应把 purpose、package 安装、import 和 data preparation 集中放在前面，把 calculation 和 interpretation 按顺序排好，最后再重启 runtime，从头到尾重新执行。只有当同样结果再次出现时，这个 notebook 才会更接近一个可复现记录，而不只是一个偶然跑通的实验。

这个案例展示了整理 notebook 的核心。可复现性不是为了做出 `漂亮文档`，而是为了减少 hidden state，并且让另一天的人仍然能沿着同样流程再次确认。

## 本节要记住的视角

- Notebook 既是文档，也是执行记录。
- 如果 cell 顺序和 runtime 状态错位，结果就会变得难以信任。
- 只要把 setup、data、calculation、output、interpretation 按顺序整理好，可重跑性就更高。
- 无论是 Colab 还是本地环境，重要的都不是 `同一个文件`，而是 `同样的准备流程`。
- 当以后需要复用的代码越来越长时，就要考虑是否该拆成函数或 `.py` 文件。

Notebook 是由保存下来的文档和执行中的 runtime 一起组成的工作环境。

有 notebook 文件，并不意味着执行状态也被保留。

可重跑的 notebook 应该能从上到下运行。

Package、data file 和 randomness 应该留在 notebook 前部或紧邻的 explanation 中。

Colab 中共享的主要是 notebook 内容，而不是 runtime 的临时状态原样共享。

Notebook 中重复的代码可以拆分成函数和 script。

## 简短检查

- 能不能把好的 notebook 解释成 `可重跑的记录`？
- 能不能说明 hidden state 为什么会成为问题？
- 能不能说明为什么 setup cell 和 data-preparation cell 应该放在 notebook 前部？
- 能不能说明为什么需要重启 runtime 后再从上到下执行？
- notebook 前部有没有 purpose 和 scope？
- 所需的 import 和 package 安装 cell 是否都在前面？
- 是否解释了 data file 从哪里来？
- 从上到下重跑时会不会报错？
- output 下方有没有留下解释？
- 如果存在 randomness，是否说明了 seed 或波动可能性？
- 在 Colab 共享时，是否检查了 file、package 和 permission 问题？
- 是否有必要把重复代码拆成函数或 `.py` 文件？

## 什么时候应先想起这个视角？

- 当你想做的不是“一次跑通的 notebook”，而是“另一天再打开也能沿着同样流程走”的记录时，应先想起本节。
- 当你不只是想保留实验结果，还要把 purpose、input data、installation condition 和 interpretation 一起整理下来时，应重新检查可重跑性的标准。
- 当你要检查共享 notebook 为什么可能在别的环境里坏掉，或判断重复代码是否到了该拆分的时候时，就用这份检查表。

## 来源与参考资料

- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.
- Project Jupyter, [The Jupyter Notebook Format](https://nbformat.readthedocs.io/en/latest/format_description.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.
- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.

# P2-3.5 Python 运行环境：Colab 与本地 PC

> Section ID: `P2-3.5`
> Version: `v2026.07.19`

从 P2-3.1 到 P2-3.4，我们主要是用公式和比较标准来阅读线性代数(linear algebra)。下一节会开始用 NumPy 直接检查向量(vector)、矩阵(matrix)、矩阵乘法(matrix multiplication)。在这之前，必须先分清 Python 代码到底是在哪里运行的。

这一部分前半段的实践，按两个运行环境来说明。

1. Google Colab 直接在浏览器里运行。
2. 本地 PC 则在自己的终端和 Python 安装环境里运行。

因此，这里不会深入学习 Colab 本身，也不会细讲本地安装步骤，而是集中区分 `写在代码单元(code cell)里运行的命令`、`写在自己电脑终端里的命令`、以及 `写在 Python 代码内部的语句`，好让后面的 Python/NumPy 实践能够顺利跟上。

这里重新整理 `Colab`、`本地 PC`、`代码单元(code cell)`、`终端(terminal)`，以及 `import` 和安装命令之间的差别。如果 3.1 到 3.4 是在读公式和线性代数结构，那么这里就是先整理“把那些结构真正带入代码时，应该在哪个位置运行”。

如何在个人电脑上安装 Python、如何管理虚拟环境，会在 `P2-7.1`、`P2-7.6`、`P2-7.7`、`P2-7.8` 里再次出现。这里先固定 Colab 与本地 PC 的执行位置差异。需要快速回看术语时，也可以一起查看[概念词汇表](/AiBook/en/reference/concept-glossary/)。

本文依据 2026 年 7 月 19 日确认的 Google Colab 官方说明和 FAQ、IPython `%pip` 文档、pip 用户指南编写。Colab 是外部服务，因此未来它的 UI、使用条件、免费范围、运行策略、甚至服务是否持续，都可能发生变化。如果你阅读这一节时，Colab 已无法提供、或看起来和这里不同，那么应另外查看 Google Colab 官方文档和当前服务状态。

## 本节目标

- 能把 Google Colab 理解成一个不需要安装、基于浏览器的运行环境。
- 能把本地 PC 运行理解成在自己电脑的终端和 Python 安装环境中运行。
- 能打开 `Welcome to Colab` 指南，并尝试运行一个代码单元(code cell)。
- 能说明 Colab/Jupyter 里的 `%pip` 不是普通 Python 语法，而是一个 magic command。
- 能区分 Colab 代码单元命令与个人电脑终端命令。
- 能为下一节在 Colab 中运行 NumPy 示例做好准备。

## 先抓住的一个场景

这一节最先要抓住的，是 `如果想用 NumPy，到底该在什么地方输入什么内容`。

| 想做的事 | Colab 代码单元 | 本地 PC 终端 | Python 代码 |
| --- | --- | --- | --- |
| 安装 NumPy | `%pip install numpy` | `python -m pip install numpy` | 不用写 |
| 导入 NumPy | `import numpy as np` | 不用写 | `import numpy as np` |
| 运行简单计算 | `print(np.array([1, 2]))` | 可以通过 `python example.py` 来运行 | `print(np.array([1, 2]))` |

因此，读者第一步要区分的，不是 `这到底是什么命令`，而是 `这是写在什么地方的什么句子`。

## 三个基准

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| Colab 是基于浏览器的练习空间 | 因为在本地还没安装 Python 之前，也能直接运行示例。 | 理解它是一个在代码单元里运行 Python 和笔记本式安装命令的地方。 |
| 本地 PC 会用到终端和安装环境 | 因为即使是同一个 NumPy 准备动作，只要执行位置变了，命令写法也会变。 | 理解 `python -m pip` 用在终端，而 `import` 用在 Python 代码里。 |
| 安装命令和 Python 代码不是一个位置的内容 | 因为一旦把执行位置混在一起，语法错误和环境错误就会反复出现。 | 理解 Colab 单元、本地终端、Python 代码这三个位置。 |

## 先把运行环境分开

“运行 Python 代码”这句话并不只有一种意思。即使是同一个示例，只要运行位置不同，命令的形式也会改变。

| 执行位置 | 英文 | 它表示什么 | 示例命令 |
| --- | --- | --- | --- |
| Colab 代码单元 | Colab code cell | 在浏览器笔记本中的代码单元里运行 | `%pip install numpy` |
| 本地 PC 终端 | local terminal | 在自己电脑的终端程序中运行 | `python -m pip install numpy` |
| Python 代码 | Python code | 在 `.py` 文件或代码单元里的 Python 语句中运行 | `import numpy as np` |

只要漏掉这个区分，就很容易把 `%pip`、`python -m pip`、`import` 当成同一种东西。它们都可能和 NumPy 有关，但执行位置和作用并不相同。

1. 包是在 Colab 代码单元或本地 PC 终端里安装的。
2. 已安装的包要在 Python 代码内部通过 `import` 导入。

把最常见的混淆再写得更短一点，会是下面这样。

| 混淆场景 | 为什么会卡住 | 应先修正的问题 |
| --- | --- | --- |
| 把 `%pip install numpy` 写进 `.py` 文件 | 因为把安装命令和 Python 代码混在一起了 | 我现在写的是代码单元，还是 Python 文件？ |
| 想把 `import numpy as np` 当成终端命令直接运行 | 因为把 Python 语句当成了 shell 命令 | 我现在写的是终端，还是 Python 解释器？ |
| 把 Colab 示例原样复制到本地环境 | 因为执行位置变了，但语法没跟着变 | 我现在是在浏览器笔记本里，还是在自己的电脑上？ |

## Colab 是在浏览器里打开的笔记本环境

Google Colab 是一种托管服务，它让你在浏览器里以 Jupyter Notebook 的形式运行 Python 代码。即使个人电脑上没有安装 Python，也可以创建并运行代码单元。

- [Google Colab](https://colab.research.google.com/){: target="_blank" rel="noopener noreferrer" }
- [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }

先打开 `Welcome to Colab` 指南，确认代码单元是怎样运行的。本节里的示例都非常小，因此不需要 GPU 或 TPU。不过 Colab 可能会有 Google 账号要求、运行时限制和资源限制。

## 本地 PC 意味着在自己的电脑上运行

所谓在本地 PC(local PC) 上运行，意思是使用自己电脑中安装好的 Python 和终端。命令会在 macOS 的 Terminal、Windows Terminal、PowerShell、Linux shell 等程序中运行。

例如，在本地 PC 终端里，可以这样安装 NumPy。

```bash
python -m pip install numpy
```

而在 Python 文件里，则这样导入 NumPy。

```python
import numpy as np
```

这里不详细解释本地安装过程。安装本身会在 P2-7.7 的补充学习里再次出现，而终端和环境变量语法会在 P2-7.6 和 P2-7.8 里再次出现。现在真正重要的是先分清：`Colab 代码单元命令` 和 `本地 PC 终端命令` 不是一回事。

## 把 Python 代码放进代码单元

Colab 笔记本里有写文字的单元，也有执行代码的单元。Python 代码要放进代码单元(code cell)里运行。

例如，下面这段代码可以放进代码单元并直接运行。

```python
print("hello, colab")
```

运行结果会像这样出现。

```text
hello, colab
```

这里的 `print(...)` 是 Python 代码。相对地，安装包的命令在性质上和普通 Python 代码略有不同。

## 在 Colab 里可以使用 `%pip`

在很多情况下，Colab 环境里已经准备好了 NumPy。但由于环境可能变化，如果需要，也可以在代码单元里运行下面这个命令。

```python
%pip install numpy
```

这里的 `%pip` 不是普通 Python 语法，而是 Jupyter Notebook 系环境里使用的 magic command。它的意思是“把这个包安装到当前笔记本内核(kernel)里”。

在 Colab 或 Jupyter 文档里，你也可能看到用感叹号(`!`)运行 shell 命令的示例，比如：

```python
!pip install numpy
```

这里我们优先使用 `%pip install numpy`，因为它更明确地表达了“安装目标是当前笔记本环境”。

如果把这个差别再写成一条流程，会变成这样：

```mermaid
--8<-- "assets/part-02/chapter-03/execution-location-flow-zh.mmd"
```

## 不要和个人电脑终端命令混用

在个人电脑的终端里，不使用 `%pip` 或 `!pip`。这些写法属于 Colab/Jupyter 的代码单元环境。

在个人电脑终端里，通常会这样写：

```bash
python -m pip install numpy
```

所以，必须先把执行位置分开。

1. 在 Colab 代码单元里，用 `%pip install numpy`。
2. 在个人电脑终端里，用 `python -m pip install numpy`。
3. 在 Python 代码内部，用 `import numpy as np`。

下一节就是建立在这个区分之上，再去检查 NumPy 代码。

读者在这里至少应该留下这一句话：

- `安装写在代码单元或终端里，import 和计算写在 Python 代码里。`

## 检查清单

- 能用一句话说明 Colab 运行和本地 PC 运行的区别吗？
- 能说明为什么 `%pip install numpy` 和 `python -m pip install numpy` 不能写在同一个地方吗？
- 能说明 `import numpy as np` 不是安装命令，而是 Python 代码吗？
- 能区分眼前这句话究竟是写给代码单元、终端，还是 Python 代码的吗？
- 能说明为什么在背语法之前，要先区分执行位置吗？

## 来源与参考资料

- Google, `Google Colab`. 可以直接确认 Colab 是基于浏览器的笔记本环境，并看到基本使用流程。 [https://colab.research.google.com/](https://colab.research.google.com/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-19
- Google, `Welcome to Colab`. 可以直接确认代码单元如何运行，以及笔记本的基础流程。 [https://colab.research.google.com/notebooks/intro.ipynb](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-19
- Google, `Google Colab FAQ`. 可以确认 Colab 是无需安装的托管 Jupyter Notebook 服务，并了解运行时和使用限制可能变化。 [https://research.google.com/colaboratory/faq.html](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-19
- IPython Development Team, `Built-in magic commands - %pip`. 可以确认 `%pip install` 会在当前内核中运行 pip 包管理器。 [https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-19
- Python Packaging Authority, `pip User Guide`. 可以确认在本地终端中使用 `python -m pip install ...` 安装包的官方示例。 [https://pip.pypa.io/en/stable/user_guide/](https://pip.pypa.io/en/stable/user_guide/){: target="_blank" rel="noopener noreferrer" } / 确认日期: 2026-07-19

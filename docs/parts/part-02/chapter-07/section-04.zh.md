# P2-7.4 虚拟环境（virtual environment）与包（package）

> Section ID: `P2-7.4`
> Version: `v2026.07.19`

在 P2-7.3 中，我们看过了运行 Python 代码的方式。现在再看一个更接近实际的问题。

例如，下面这些情况经常会遇到。

- Python 能运行，但提示没有 NumPy。
- 昨天还能运行，今天包版本变了，结果也跟着变了。
- 在我的电脑上可以，在别人的电脑上却不行。

这类问题不能只靠 Python 语法来解决。你还需要一起看代码运行的空间，以及那个空间里安装了哪些包。

这里会说明 `virtual environment`、`package`、`pip`、`import` 之间的关系。即使后面的章节还会重新讨论依赖列表或环境检查顺序，你也应该以这里的说明为基准去理解安装和使用到底要连接到哪个 Python 空间。

这里不是要学习整个 Python 分发与打包体系，而是把重点放在理解为什么按项目分开执行环境之后，实践结果会不同。如果你在这里先抓住虚拟环境、包、安装和 `import` 的区别，那么后面再看依赖列表、可复现性以及团队协作环境时，就能自然理解哪些内容要记录、哪些内容需要重新安装。

| 本节要先抓住什么 | 紧接着会出现什么问题 | 之后会在什么地方再次使用 |
| --- | --- | --- |
| 虚拟环境是按项目划分的执行空间 | 在 P2-7.5 中会接到依赖列表和可复现性。 | 之后在所有本地 Python 实践里解释环境冲突时都会再次用到。 |
| `pip install` 和 `import` 是不同阶段 | P2-7.9 会进一步检查安装环境和运行环境错开的错误。 | 会在包安装错误、Colab 与本地差异、库准备等语境里反复出现。 |
| Colab runtime 和本地 `.venv` 是不同空间 | P2-7.6、P2-7.7 会补充不同操作系统下的安装与激活步骤。 | 会成为 Part 3 之后复现实践环境和说明团队协作时的基础。 |

| 术语 | 本节先要抓住的意思 |
| --- | --- |
| 虚拟环境（virtual environment） | 按项目分开的 Python 执行空间。 |
| 包（package） | 可以拿到 Python 里使用的一组代码。 |
| `pip` | 安装包的工具。 |
| `import` | 在 Python 代码里载入已经准备好的包的语句。 |
| `.venv` | 放在项目文件夹中的典型本地虚拟环境目录名。 |

## 本节范围

这里回答下面这些问题。

- 为什么需要虚拟环境？
- 什么是包？
- `pip` 做什么？
- 为什么安装和 `import` 不一样？

如何保存依赖列表，以及如何在另一台电脑上恢复相同环境，会在 P2-7.5 中讨论。

| 如果你现在的症状是这样 | 先去哪里看 | 否则在本节先抓住什么 |
| --- | --- | --- |
| 连本地 PC 现在是否该先安装 Python 都判断不清 | P2-7.7 补充学习 | 先理解虚拟环境是在安装之后用来区分项目执行空间的装置 |
| 明明执行了 `pip install`，但 `import` 还是失败 | P2-7.9 补充学习 | 现在先留下一个标准：安装和执行可能正在看不同环境 |
| 你只是想知道为什么像 NumPy 这样的包会在不同项目里分别需要 | 继续读本节 | 先确认虚拟环境为什么能减少包冲突 |

## 本节目标

- 能把虚拟环境解释为按项目划分的 Python 执行空间。
- 能把包解释为可以拿到 Python 里使用的一组代码。
- 能把 `pip` 解释为安装包的工具。
- 能说明 `pip install` 和 `import` 做的是不同的事。
- 能说明即使在同一台电脑里，不同项目所需的包版本也可能不同。

## 三个标准

| 标准 | 为什么重要 | 本节所需的理解程度 |
| --- | --- | --- |
| 虚拟环境是按项目划分的 Python 执行空间 | 因为不同项目可能需要不同版本的工具 | 把虚拟环境理解为减少冲突的隔离装置 |
| 安装和 `import` 是不同阶段 | 安装是准备，`import` 是在代码里真正载入使用 | 能说明终端命令和 Python 代码在角色上的区别 |
| 最常见的失误是安装的环境和运行的环境不同 | 同一台电脑里也可能存在多个 Python 空间 | 能区分“环境不一致”这种问题类型 |

## 虚拟环境为什么会变得必要

对刚学 Python 的人来说，虚拟环境看起来可能像一种有点麻烦的装置。但它并不是单纯的习惯，而是 Python 生态扩大之后，为解决实际问题而稳定下来的做法。

PEP 405 是把 `venv` 加入 Python 标准库的提案。这份文档创建于 2011 年，目标版本是 Python 3.3。PEP 405 的动机（motivation）说明，当时像 `virtualenv` 这样的第三方虚拟环境工具，已经被广泛用于依赖管理（dependency management）、隔离（isolation）、在没有系统管理员权限的情况下安装和使用包，以及在多个 Python 版本上做自动化测试等工作。

如果从入门者的视角把这段背景压缩一下，大致就是下面这些原因。

- Python 包变多了：不同项目所需的外部代码开始不同。
- 不能随便改系统 Python：那样可能会破坏操作系统或其他程序使用的 Python 环境。
- 很多场景需要在没有管理员权限时安装：个人项目或服务器账号里，往往不能随意更改整个系统。
- 需要测试多个项目和多个 Python 版本：只靠一个全局安装空间，很难避开冲突。

所以，虚拟环境并不是为了让学习流程更复杂，而是出于按项目分离 Python 和包、从而减少冲突的历史需求而出现的工具。

## 为什么需要虚拟环境

看起来好像只有一个 Python 就够了。人很容易直接想到“安装 Python”“安装需要的包”“运行代码”就结束了。

但是项目一多，问题就会出现。

例如，项目需求可能像下面这样不同。

- 项目 A 是按 `numpy 1.x` 编写的。
- 项目 B 是按 `numpy 2.x` 编写的。
- 如果把它们混在同一个空间里，可能会有一边坏掉。

虚拟环境（virtual environment）就是为了减少这种冲突，按项目划分 Python 执行空间的方法。Python 官方文档说明，`venv` 会创建轻量级虚拟环境，而且每个虚拟环境都可以拥有彼此独立的一组 Python 包。

这里把虚拟环境理解为“按项目划分的 Python 执行空间”。
- 项目 A 的虚拟环境：安装项目 A 所需的包。
- 项目 B 的虚拟环境：另外安装项目 B 所需的包。

## 虚拟环境不是项目代码本身

虚拟环境是运行项目所需的外围环境。它和项目的正文或代码本身并不是一回事。

例如，在某个项目文件夹里，你可能会看到一个名为 `.venv` 的文件夹。这个文件夹是一个本地执行环境，里面装着运行 Python 或构建文档所需的包。它不是项目正文文件，也不是代码本身。

所以，通常不会把虚拟环境文件夹提交到 Git。Python 官方文档也说明，虚拟环境通常可以在项目目录里以 `.venv` 这样的名称创建，而且一般不会放进源码管理系统中。

因此通常会像下面这样划分。

- 要提交的内容：原稿、代码、配置文件、示例文件
- 不提交的内容：我在自己电脑上创建的虚拟环境文件夹

与其共享虚拟环境本身，更安全的做法是记录需要哪些包，并让别人可以重新安装。这一问题会在 P2-7.5 的依赖（dependency）和可复现性（reproducibility）里继续展开。

## 包是可以拿来使用的一组代码

包（package）是为了让你能在 Python 中拿来使用而分发的一组代码。NumPy、Pandas、Matplotlib 这类工具都属于这里。

这里同样先区分三个层次。

- Python：语言本身和执行程序
- 包：可以拿到 Python 里使用的一组代码
- 包仓库：可以下载包的地方

Python Packaging User Guide 介绍了使用 `pip` 和 `venv` 在虚拟环境中安装包的流程。这里最重要的是，安装包和在代码里载入包是不同的事。

## `pip install` 是安装，`import` 是使用

下面这条命令是在终端里安装包的命令。

```bash
python -m pip install numpy
```

这条命令不是写在 Python 代码文件里的语句，而是在终端执行的命令。就像 P2-7.3 里看到的那样，`python -m` 是要求 Python 运行某个特定模块的方式。这里运行的是 `pip`，目的是安装 NumPy。

相反，下面的是 Python 代码。

问题场景：与安装相对照，确认包在 Python 代码里到底是怎样被载入的。
输入（input）：`import numpy as np` 这一句。
期望输出（output）：不会打印输出，但 NumPy 会在当前 Python 代码里处于可用状态。
要确认的概念：`pip install` 是安装，而 `import` 是在代码里使用已经安装好的包这一阶段。

```python
import numpy as np
```

这段代码表示把已经安装好的 NumPy 载入当前 Python 代码中，以便使用。

这两种语句不能混在一起看。

| 目的 | 示例 | 输入位置 |
| --- | --- | --- |
| 安装包 | `python -m pip install numpy` | 终端 |
| 使用包 | `import numpy as np` | Python 代码 |

这里像下面这样区分。

- `install`：在我的执行环境里准备好这个包
- `import`：在当前 Python 代码里使用那个包

## 安装的地方和运行的地方必须一致

有一种错误很常见。

入门者经常遇到的错误，就是“明明安装过了，但 Python 说它不存在”。

这时就要把“装到了哪里”和“从哪里运行”分开来看。

例如，安装的地方和运行的地方可能会像下面这样错开。

- 你安装到了系统 Python，但却用虚拟环境中的 Python 来运行。
- 你安装到了虚拟环境 A，但却在虚拟环境 B 中运行。
- 你安装在了 Colab 里，但却在本地 PC 上运行。

包并不是抽象地“安装在电脑某个地方”。它们是安装到某个特定的 Python 执行环境中的。所以，使用虚拟环境时，不管是安装包还是运行代码，都应该以同一个虚拟环境为基准。

## 像看图一样理解虚拟环境的流程

实际命令会因操作系统和项目情况而不同，但整体流程大致如下。

实际流程通常可以按下面这个顺序来理解。

1. 移动到项目文件夹。
2. 创建虚拟环境。
3. 把虚拟环境切换到使用状态。
4. 安装所需的包。
5. 运行 Python 代码。

如果用终端命令来表示，常见的流程大致像下面这样。

问题场景：把从创建虚拟环境到安装包、再到运行脚本的流程一次看完。
输入（input）：三行命令，分别用于创建 `venv`、用 `pip` 安装、以及用 `python` 运行。
期望输出（output）：可以看见“创建项目专用环境、准备包、运行代码”的顺序。
要确认的概念：虚拟环境和包的使用要理解成一个连续的工作流程。

```bash
python -m venv .venv
python -m pip install numpy
python example.py
```

这里有一个重要的省略。实际使用时，可能还需要“激活（activate）虚拟环境”这一步。不同操作系统中的激活命令在 Windows、macOS、Linux 下看起来不同，所以这里先不要求记忆。详细的使用过程会在 P2-7.6 补充学习中处理，而为什么激活状态和安装环境经常错开，则会在 P2-7.9 补充学习中再次说明。

这里先只留下下面这个视角。

- 你创建了虚拟环境：这表示你创建了一个项目专用的 Python 空间。
- 你安装了包：这表示你在那个空间里准备好了工具。
- 你执行了 `import`：这表示你在 Python 代码里载入了那些工具。

## 在 Colab 里也一定要懂虚拟环境吗

Colab 是在浏览器中运行的笔记本环境。在前期学习中，即使不了解 Python 安装和虚拟环境，也可以运行代码。所以这本书在前面的实践里允许使用 Colab。

但即使在 Colab 里，包安装和执行环境的问题也不会消失。

问题场景：确认即使在 Colab 中，也可能需要把包直接安装到当前 runtime 里。
输入（input）：代码单元中的 `%pip install numpy` 命令。
期望输出（output）：NumPy 会安装到当前 Colab runtime 中。
要确认的概念：Colab 很方便，但它是一个与本地虚拟环境不同的独立执行空间。

```python
%pip install numpy
```

这条命令会把包安装到当前笔记本 runtime 中。如果 runtime 被重置，可能就需要重新安装这些包。另外，本地 PC 里的 `.venv` 和 Colab runtime 也不是同一个空间。

总结一下，这两个空间是不同的。

- Colab runtime：浏览器之外的外部执行环境
- 本地虚拟环境：围绕我电脑上的项目文件夹而存在的执行环境

一开始 Colab 可能就够用了。但如果你想长期维护一个项目，或者想和别人复现同一份代码，就需要理解虚拟环境和依赖管理。

## 用案例来看

### 案例 1. 明明装了 NumPy，为什么 `import` 还是失败

假设有一位学习者先在终端执行了 `python -m pip install numpy`，然后立刻去运行示例文件。但 `import numpy as np` 这里仍然报错。人通常会先想到“是不是没装上”“是不是 `pip` 命令骗了我”。

但在这种情况下，问题往往不在安装本身，而是在安装包的环境和运行代码的环境不一致。也可能是装到了系统 Python 中，却用虚拟环境里的 Python 来运行；也可能是在另一个项目的虚拟环境开启状态下运行了代码。

本节的核心，是把 `virtual environment`、`package`、`pip install`、`import` 当作不同阶段来读。安装是准备，而 `import` 是在当前正在运行的 Python 环境里真正把东西载入进来。

只要在同一个终端里检查当前到底在使用哪个 Python 环境，这个结果就是可以验证的。如果安装命令成功了，但只有当前虚拟环境里 `import numpy` 失败，那就可以说明问题不在包名，而在环境分离上。

## 检查清单

- 能把虚拟环境解释为按项目划分的 Python 执行空间。
- 能说明虚拟环境文件夹不是项目原稿或代码本身，而是执行环境。
- 能把包解释为 Python 中可拿来使用的一组代码。
- 能说明 `pip` 是安装包的工具。
- 能区分 `python -m pip install numpy` 是终端命令，而 `import numpy as np` 是 Python 代码。
- 能说明包是安装到特定 Python 执行环境中的。
- 能说明 Colab runtime 和本地虚拟环境不是同一个空间。
- 能检查 `我现在在用哪个 Python 环境`、`需要的包是否安装在那个环境里`、`安装命令和代码执行看到的是不是同一个环境` 这三件事。

## 来源与参考资料

- Carl Meyer, [PEP 405 – Python Virtual Environments](https://peps.python.org/pep-0405/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals，确认日期：2026-07-19。作为虚拟环境拥有自己的包集合和 Python 可执行文件，并可与系统 site-packages 隔离这一设计说明的依据。
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-19。用于确认用 `venv` 创建和激活虚拟环境，以及环境内部 Python 与包状态相互分离的说明。
- Python Packaging Authority, [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide，确认日期：2026-07-19。用于确认按项目创建虚拟环境，并通过 `python -m pip install` 安装包的流程。
- Python Software Foundation, [Installing Python Modules](https://docs.python.org/3/installing/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-19。用于确认 `pip`、`venv`、PyPI、`python -m pip install` 的基本角色，以及优先考虑虚拟环境而不是系统级安装的语境。

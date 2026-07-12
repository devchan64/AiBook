# P2-10.2 Jupyter、Colab 与本地执行的区别

> Section ID: `P2-10.2`
> Version: `v2026.07.12`

在 P2-10.1 中，我们把 notebook 看成一种同时包含 code、explanation 和 output 的计算文档。现在要区分三种在实践里最常遇到的执行方式。

Jupyter、Colab、本地执行。

这三个名字看起来互相重叠。Colab 也使用 Jupyter Notebook 格式，Jupyter 也可以运行在你自己的电脑上，本地执行也不仅能通过 notebook，还能通过 `.py` script 来完成。所以要把 `在哪里执行`、`保存在哪里`、`共享的是什么` 分开看。

这里说明 `Jupyter`、`Colab`、`local execution`、`runtime`、`.ipynb` 文件之间的关系。如果前一节解释的是 notebook 文档格式，那么这里建立的标准就是：这个文档实际上在哪里执行，以及它和什么一起被共享。
这个区分要先抓住。
只要执行地点变了，同一个 notebook 的含义也会跟着变化。

## 本节的范围

本节不是详细说明 Jupyter 和 Colab 用法的手册。不讨论安装步骤、菜单位置、快捷键、GPU 设置或 Google Drive 集成细节。比起背这些功能名称，本节更先抓住 `执行位置`、`runtime` 和 `文件访问` 的差异，而像实验跟踪这样更扩展的话题，会在后面的补充学习 P3-9.3 和 Part 6 的项目记录语境里再连接。

| 术语 | 本节先要抓住的含义 |
| --- | --- |
| Jupyter | 一个开源 notebook 工具与生态 |
| Colab | Google 提供的、基于 Jupyter 格式的托管 notebook 服务 |
| local execution | 直接在自己电脑的 Python、文件和包环境里执行的方式 |
| runtime | 实际运行代码的当前 Python 环境与状态 |
| `.ipynb` 文件 | 保存 notebook 内容的文档文件，它可能和当前正在运行的状态不同 |

本节回答以下问题。

这里先要解决的问题是：`即使看起来像同一个 notebook 文件，为什么一旦执行位置不同，结果和文件访问就会不同？`

所以本节回答以下问题。

- Jupyter 和 Colab 到底是什么关系？
- 本地执行到底有什么不同？
- 为什么 notebook 文件和 runtime 状态不是一回事？
- 在 Colab 中，什么会被共享，什么不会被共享？
- 学习者什么时候适合用 Colab，什么时候应考虑本地执行？

本节重点在于区分执行位置和 runtime 条件。如果前一节讨论的是 notebook 如何把 code 与 output 一起留在同一文档中，那么这里讨论的就是：这个文档实际上在哪里执行，以及它依赖哪些文件和 runtime 条件。下一节会再把这个问题重新整理成可复现记录的习惯。

本节之后的流程也很简单。

- 在 `P2-10.3` 中，这里看到的执行差异会被重新整理成可复现记录的习惯。
- 如果把这里和 Chapter 7 的环境部分连起来看，那么 runtime、文件访问和 package 安装问题，都可以用同一个 `执行位置` 问题来阅读。
- 在 Part 6 的项目部分里，这个差异会在实验记录与可复现性语境下再次变得重要。

## 本节的目标

- 能把 Jupyter 解释成开源 notebook 生态，把 Colab 解释成基于 Jupyter 的托管服务。
- 能把本地执行解释成在自己电脑的 Python、文件、terminal 和 package 环境中运行的方式。
- 能区分 notebook 文件(`.ipynb`)和正在运行的 runtime。
- 能说明在 Colab 中 notebook 内容也许可以共享，但 runtime 里的文件与安装状态不一定会原样共享。
- 能根据学习场景判断 Colab、Jupyter 和本地 script 中哪一种应先使用。

## 三个标准

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| Jupyter 和 Colab 的关系 | 它能防止把它们的名字误解为同一层级的对立项 | 把 Colab 理解成提供 Jupyter 风格 notebook 的一种服务 |
| 选择环境的标准 | 它帮助你把执行位置和可复现条件一起考虑 | 从启动门槛、可复现性、文件访问和重复执行便利性来判断 |
| 共享时该注意什么 | 它能防止混淆 notebook 文件和 runtime | 单独确认到底共享的是文件，还是同样的执行环境 |

即使是同一个 `.ipynb` 文件，只要执行位置变了，runtime 和文件访问也会变。Colab 是托管服务，而本地 Jupyter 和本地 script 则是你更直接管理的环境。同时，notebook 文件和当前正在运行的 runtime 也是不同的。只要这个区分建立起来，Chapter 10 就不再只是 `notebook 服务比较`，而更像 `理解执行记录放在哪里、在什么条件下存在` 的一章。

换句话说，这一章的核心是：问题已经从 `我们要把什么留在一个文档里？` 移向 `这个文档实际上是在什么地方、什么条件下执行的？`。在 P2-10.3 中，这种执行差异会再被整理成留下可复现记录的习惯。

## Jupyter 和 Colab 不是同一层级的词

Google Colab FAQ 把 Jupyter 解释成 Colab 所依赖的开源项目。同时也把 Colab 解释成一种 hosted 服务，让你不必自己下载、安装和运行，就能使用和共享 Jupyter notebook。

这里这样区分它们。

| 名称 | 先要理解成什么 | 执行位置 |
| --- | --- | --- |
| Jupyter | 一个开源 notebook 工具和生态 | 通常是你自己的 PC、server 或 cloud |
| Colab | Google 提供的 hosted Jupyter Notebook 服务 | Google 提供的远程 runtime |
| local execution | 用自己电脑的 Python 直接执行 | 你自己的 PC |

所以 `Jupyter 还是 Colab？` 这个问题，并不是完全对立的选择。Colab 是基于 Jupyter Notebook 格式和工作流的服务。不同点在于：用户不需要直接管理安装和 server 执行。

## 把 notebook 文件和执行位置分开看

最常见的混淆点，是把文件和执行状态看成一回事。

Notebook 文件通常是 `.ipynb` 格式。Jupyter 架构文档解释说，Jupyter Notebook 是一种结构化数据，用来表示 code、metadata、content 和 output；而在磁盘上保存时，它使用 `.ipynb` 扩展名和 JSON 结构。

但 `有这个文件` 和 `这段代码正在运行` 并不是一回事。

| 区分 | 它是什么 | 例子 |
| --- | --- | --- |
| notebook 文件 | 保存了 code、explanation 和部分 output 的文档 | `practice.ipynb` |
| runtime | 真正执行代码的 Python 环境 | Colab VM、Jupyter kernel |
| file system | 代码读写文件的位置 | 你 PC 上的文件夹、Colab VM、Google Drive |

这个区分重要的原因很简单。Notebook 文件可以留下来，但 runtime 可能会消失；即使 code cell 还在，那些在 runtime 中安装的 package 或临时生成的文件，也可能会消失。

Colab FAQ 也说明，Colab 代码运行在分配给账号的 virtual machine 中，而这个 virtual machine 会在空闲一段时间后被删除，并且有最大寿命限制。

## 一次性看懂三种环境的差别

下面这张表只整理学习者一开始最需要知道的差别。

| 标准 | Colab | 本地 Jupyter | 本地 script |
| --- | --- | --- | --- |
| 执行位置 | Google 远程 runtime | 你自己的 PC 或你自己启动的 server | 你自己的 PC |
| 安装负担 | 低 | 中 | 中 |
| 文件访问 | Colab VM、上传、Drive 集成 | 自然访问你 PC 上的文件 | 自然访问你 PC 上的文件 |
| 结果记录 | 很适合保留在 notebook 里 | 很适合保留在 notebook 里 | 需要另外保存输出或日志 |
| 重复自动化 | 有限制 | 可以，但要注意 notebook 特性 | 最自然 |
| 共享 | 链接共享很方便 | 需要文件共享或 server 访问 | 需要代码文件和环境说明 |
| 注意点 | runtime 限制、资源限制、Drive 权限 | 安装和 package 管理 | explanation 与结果记录容易分离 |

这张表里重要的不是 `哪一个永远最好？`。当学习目的和执行目的变化时，合适的环境也会变化。

## Colab 会降低启动门槛

Colab 的大优点是启动门槛低。在你还没有在自己的 PC 上安装 Python、Jupyter、NumPy、pandas 之前，就可以直接在浏览器里运行代码。

对于这个 Part 前半段那种练习，例如小型数学计算、列表和字典例子、简单的 NumPy 检查，Colab 往往已经够用了。

Colab 适合以下情况。

- 还没有安装 Python。
- 想在另一台电脑上也打开同一份 notebook。
- 想通过链接共享 code、explanation 和 result。
- 想用小数据快速确认一个概念。
- 想短暂测试 GPU 或 TPU 这样的加速环境。

但 Colab 是外部服务。免费资源并不保证永远存在，也不是无限的；使用限制和 runtime 结束条件都可能变化。Colab FAQ 也说明，使用限制、空闲终止、最大 runtime 和 GPU 类型都可能随着时间变化。

因此，更安全的理解方式是：不要把 Colab 看成 `一直在那里等我的电脑`，而要把它看成一个能快速开始学习与实验的远程工作空间。

## 本地 Jupyter 会在你自己的环境中运行 notebook

本地 Jupyter 是在你自己的电脑，或者你自己管理的 server 上运行 Jupyter Notebook 或 JupyterLab 的方式。

它的优势是：你可以直接控制文件和环境。

- 可以直接读写你 PC 文件夹里的文件。
- 可以直接选择 virtual environment。
- 可以管理 package 版本，使其和项目匹配。
- 可以较少依赖网络连接或外部服务政策。

但需要准备的东西也会更多。

- 必须已经安装 Python。
- 可能还要安装和 Jupyter 相关的 package。
- 要按项目管理 virtual environment。
- 如果要在另一台电脑上复现，就必须记录 dependency。

所以在这里，更自然的路线是：先用 Colab 降低执行门槛，再把本地安装和 virtual environment 变得必要的时机，交给 Part 2 Chapter 7 Section 7 去单独处理。

## 本地 script 更适合重复执行和复用

Notebook 对学习记录很好，但如果所有代码都只留在 notebook 中，之后复用会变得困难。

例如，如果你必须每天读取一个数据文件并重复同样处理，或者同一个函数要在多个项目里复用，那么 `.py` 文件通常更自然。

问题场景：你想把最初在 notebook 中验证的计算，迁移成一个以后可以反复复用的函数。
输入(input)：一个函数定义，它接收数字列表并返回平均值。
期望输出(output)：虽然没有输出，但会形成一个可复用的函数形式。
要确认的概念：看到一旦需要重复执行和复用，notebook 代码就可以迁移成 `.py` 函数。

```python
def mean(values):
    return sum(values) / len(values)
```

这个函数可以先在 notebook 里实验。但一旦需要反复复用，它就可能更适合被移动到像 `stats_utils.py` 这样的文件里。

这里自然的顺序如下。

1. 先在 notebook 中通过小例子理解。
2. 当代码变长时，把它打包成函数。
3. 当它开始被重复使用时，把它拆分成 `.py` 文件。
4. 如果它必须在另一台电脑上运行，就记录 dependency 和执行方式。

Notebook 和 script 不是竞争关系。Notebook 强在探索和解释，script 强在重复执行和复用。

## 共享时要确认到底共享了什么

Colab FAQ 说明，共享 notebook 时，notebook 里的 text、code、output、comments 等完整内容都可能被共享。相反，你正在使用的 virtual machine、执行过程中准备的文件，以及安装好的库状态，并不会原样一起共享。

这个差别非常重要。

| 会被共享的东西 | 可能不会被共享的东西 |
| --- | --- |
| notebook 里的 explanation cells | runtime 里的临时文件 |
| code cells | 你手动安装过的 package 状态 |
| 已保存的 output | 当前内存里的变量 |
| comments 或文档内容 | 个人账号的 Google Drive 文件权限 |

所以，一个准备共享的 notebook，应该把必要的准备过程一起留在文档内部。

例如，把下面这些内容放在前面的 cell 中。

问题场景：你想让别人重跑 Colab notebook 时，先安装所需 package。
输入(input)：一个用于安装 `numpy` 的 `%pip` 命令。
期望输出(output)：`numpy` 会被安装到当前 kernel 中。
要确认的概念：看到共享 notebook 应该把必要准备过程留在前面的 cell 中，才能让重跑更容易。

```python
%pip install numpy
```

然后在代码里，把必要的 import 明确写出来。

问题场景：你想清楚展示实际代码在安装之后用到了哪个 package。
输入(input)：把 `numpy` 以 `np` 名称导入的代码。
期望输出(output)：虽然没有输出，但后面的 cell 已准备好可以使用 `np`。
要确认的概念：看到把安装 cell 和 import cell 分开，会让执行环境依赖更明显。

```python
import numpy as np
```

如果还需要文件，就必须把这个文件该从哪里获得也写出来。因为文件即使在你的 runtime 里存在，在别人的 runtime 里也未必存在。

## 文件访问会随着环境而变化

即使是同一段代码，文件路径也会随着执行环境而变化。

例如，在本地 PC 上，当前项目文件夹里可能有 `data/scores.csv`。

问题场景：你想通过最简单的路径例子，看懂为什么读文件代码会随着环境而改变。
输入(input)：一个基于本地项目的文件路径字符串。
期望输出(output)：虽然没有输出，但代码想找的文件变得可见。
要确认的概念：看到文件问题不一定来自代码语法，也可能来自执行环境和路径差异。

```python
path = "data/scores.csv"
```

在 Colab 里，同样的文件可能并不存在于 runtime 中。路径会因为你是上传了文件、挂载了 Google Drive，还是从 GitHub 下载而不同。

这里先检查下面这些问题。

| 问题 | 原因 |
| --- | --- |
| 这段代码是在哪里执行的？ | 因为本地 PC 和 Colab 的文件位置不同 |
| 这个文件在哪里？ | 你 PC 上的文件夹、Colab VM、Google Drive 是不同地方 |
| 重新运行后这个文件还会存在吗？ | 临时 runtime 文件可能会消失 |
| 其他人也能访问这个文件吗？ | 个人 Drive 权限可能不会被共享 |

文件问题看起来像代码错误，但很多时候，真正的问题是执行环境。

## 应该先选择哪种环境？

在跟着这个 Part 做练习时，可以用下面这个标准开始。

| 情况 | 先选的环境 |
| --- | --- |
| 安装 Python 仍然有负担 | Colab |
| 检查小型数学计算和表格输出 | Colab 或本地 Jupyter |
| 要大量读写自己 PC 上的文件 | 本地 Jupyter 或本地 script |
| 要重复执行或自动化同一段代码 | 本地 script |
| 要把 explanation 和 result 一起展示给别人 | Colab 或 Jupyter notebook |
| 必须严格固定 package 版本 | 本地 virtual environment |

没有必要一开始就选一个完美环境。重要的是，当练习卡住时，先把问题分成：`这是代码问题、package 问题、文件位置问题，还是 runtime 问题？`

## 通过案例来看

### 案例 1. 为什么同一个 CSV 文件在 Colab 里打不开？

假设某个学习者昨天在本地 Jupyter 里成功读取了 `data/scores.csv`，但第二天把同样代码放到 Colab 里运行时，却出现了 `找不到文件` 的错误。从人的角度看，很容易觉得是 `昨天还对的代码` 自己坏掉了。

但真实问题更可能是执行位置，而不是代码本身。在本地 Jupyter 中，你自己电脑的文件夹直接可见；而在 Colab 中，远程 runtime 会重新打开，里面未必有同样的文件。结果会因为是否连接了 Drive、是否上传了文件、是否存在下载 cell 而不同。

这个案例帮助你把 `Jupyter`、`Colab` 和 `local execution` 读成执行环境的差异，而不是功能名称。即使是同一个 `.ipynb` 文档，文件路径、安装状态、保留下来的 runtime 都会随着执行地点不同而改变。

所以，在阅读练习文档时，先检查 `这段代码是在哪里执行的？`、`这个文件在哪里？`、`如果别人重新运行，能不能看到同一个文件？`。只有先分清环境，错误原因才能更快缩小。

## 检查清单

- 能说明 Jupyter 和 Colab 并不是完全同一层级的词。
- 能区分 notebook 文件(`.ipynb`)和 runtime。
- 能说明 Colab 中的 code 可以在远程 virtual machine 上运行。
- 能说明共享的 notebook 不一定会连同 runtime 文件和安装状态一起共享。
- 能区分本地 Jupyter 和本地 script 的优缺点。
- 能说明文件路径问题其实可能是执行环境问题。
- 能说明即使是同一个 `.ipynb` 文件，只要执行位置和 runtime 不同，文件、package 和共享条件也会不同。

## 来源与参考资料

- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.
- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.
- Jupyter Notebook Team, [The Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-25.

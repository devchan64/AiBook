# P2-7.5 依赖（dependency）与可复现性（reproducibility）

> Section ID: `P2-7.5`
> Version: `v2026.07.12`

在 P2-7.4 中，我们看过了虚拟环境和包。现在还剩下一个问题。

把包装上就结束了吗？

看起来似乎如此。但学习代码只要稍微变长一点，下面这些问题就会出现。

- 在我的电脑上能运行。
- 在别人的电脑上不能运行。
- 昨天还能运行。
- 今天包版本变了，结果也跟着变了。
- 在 Colab 里可以。
- 在本地 PC 上不行。

这个问题与其说和代码本身有关，不如说和“能不能把执行环境重新做出来”有关。所以要把依赖和可复现性分开来看。

这里会说明 `dependency`、`reproducibility`、`requirements.txt`、`version pinning` 的基本区别。即使后面还会重新看示例项目或协作环境，你也应该以这里的说明为基准，再去理解除了代码之外还要一起记录什么。

这里不是要深入学习 Python 包分发体系，而是把重点放在：如果将来还想再次运行同一份代码，到底还要一起记录哪些东西。如果你在这里先抓住依赖、requirements 文件、版本记录的作用，那么后面在团队协作或长期实践中，就能更准确地判断“只有代码够不够”。

| 本节要先抓住什么 | 紧接着会出现什么问题 | 之后会在什么地方再次使用 |
| --- | --- | --- |
| 依赖和可复现性是代码之外也要单独管理的对象 | 这会接到 P2-7.9 中本地环境实际检查顺序。 | 之后会在所有实践和团队共享环境里再次使用。 |
| `requirements.txt` 和版本记录的作用 | 会接到按操作系统安装和检查 Python 版本的问题。 | 会在 Part 3 之后的示例重跑、项目交接、协作环境说明中反复出现。 |
| 即使在 Colab 中，可复现性问题也不会消失 | 这会成为比较本地环境和云环境差异的标准。 | 会成为长期实验、报告重跑、Part 6 项目验证的基础。 |

| 术语 | 本节先要抓住的意思 |
| --- | --- |
| 依赖（dependency） | 我的代码所依靠的外部包和执行条件。 |
| 可复现性（reproducibility） | 把条件留下来，使同一份代码以后还能再次运行的性质。 |
| `requirements.txt` | 记录所需包列表和版本的代表性文件。 |
| 版本固定（version pinning） | 通过明确写出特定包版本来减少环境差异的方法。 |
| 环境记录（environment record） | 重新执行所需的备注，例如 Python 版本、包列表、运行位置等。 |

## 本节范围

本节处理依赖和可复现性的入门概念。不会深入讨论包分发、lock 文件、dependency resolver、容器（container）或 CI 环境。在本地环境里到底实际在看哪个 Python、哪些包，这个检查顺序会在 P2-7.9 补充学习中重新整理。安装流程本身会在 P2-7.4 再次出现，不同操作系统下的 Python 准备则会在 P2-7.7 再次处理。

这里回答下面这些问题。

- 什么是依赖？
- 为什么需要可复现性？
- requirements 文件记录什么？
- 所谓固定版本是什么意思？

按操作系统使用终端的方法在 P2-7.6 中补充，Python 安装在 P2-7.7 中补充，而本地环境里最常卡住人的检查顺序在 P2-7.9 中作为补充学习处理。特别是，如果 `requirements.txt` 明明能看到，但本地 PC 上 `import` 还是不断失败，那么先把这一节读完，再暂时移动到 P2-7.9，先检查“我现在看到的是哪个 Python 环境”，然后再回来。

| 如果你现在的症状是这样 | 先去哪里看 | 否则在本节先抓住什么 |
| --- | --- | --- |
| 能看到 `requirements.txt`，但不知道该安装到哪个 Python 环境里 | P2-7.9 补充学习 | 现在先抓住：即使记录了依赖，只要执行环境不同，就无法复现 |
| 本地安装本身以及确认 `python --version` 更紧急 | P2-7.7 补充学习 | 现在先留下为什么需要版本固定和包列表 |
| 你只是想知道为什么“在我的电脑上能跑”并不够 | 继续读本节 | 先确认可复现性是重新做出同样代码、同样条件的问题 |

## 本节目标

- 能把依赖（dependency）解释为我的代码运行所需的外部包。
- 能把可复现性（reproducibility）解释为以后还能再次运行同一份代码的条件。
- 能说明 `requirements.txt` 是装载待安装包列表的文件。
- 能在入门层面说明版本固定（version pinning）的必要性和局限。
- 能理解“在我的电脑上能跑”并不是充分说明。

## 三个标准

| 标准 | 为什么重要 | 本节所需的理解程度 |
| --- | --- | --- |
| 依赖是代码所依靠的外部包和执行条件 | 它能解释为什么只看代码也无法运行 | 看到 `import` 时，能联想到需要哪个外部包 |
| 可复现性是把条件留下来，使同一份代码以后还能再次运行 | 学习和协作不是只运行一次就结束 | 理解除了代码，还要把环境条件一起留下 |
| requirements 文件记录所需包列表和版本范围 | 它会成为别人重新搭环境的起点 | 能用一句话说明 `requirements.txt` 的作用 |

## 依赖是我的代码所依靠的外部条件

依赖（dependency）是我的代码为了运行而需要的外部条件。在 Python 实践里，最先遇到的通常是包依赖。

例如，下面这段代码需要 NumPy。

问题场景：用最简单的例子确认一段代码依赖哪个外部包。
输入（input）：创建 NumPy 数组并输出平均值的代码。
期望输出（output）：如果安装了 NumPy，就会输出平均值 `2.0`。
要确认的概念：只要看到 `import numpy as np`，就说明这段代码依赖 NumPy 包。

```python
import numpy as np

values = np.array([1, 2, 3])
print(values.mean())
```

这段代码并不是只有 Python 就够了。还必须安装 NumPy。

- 我的代码：使用 `import numpy as np`。
- 所需外部包：NumPy。
- 因此，NumPy 就是这段代码的依赖。

依赖还可以分成直接依赖和间接依赖。

- 直接依赖：我在代码里直接使用的包。
- 间接依赖：我安装的包在内部又需要的其他包。

不需要把这个结构全部背下来。但你需要有一种感觉：我安装的一个包背后，可能还会一起跟来好几个包。

## 示例：同一段代码，在有些地方会失败

想一想下面这个情况。你下载了书里的示例，并运行一个用来计算平均值的 Python 文件。

问题场景：确认同一段平均值计算代码在 Colab 中能运行，但在本地 PC 上可能因为缺少包而失败。
输入（input）：用 NumPy 数组计算平均值的短代码。
期望输出（output）：在准备好 NumPy 的环境里会输出平均值，而在没有准备好的环境里可能会在 import 阶段失败。
要确认的概念：需要把代码问题和执行环境问题分开来看。

```python
import numpy as np

scores = np.array([82, 91, 77, 88])
print(scores.mean())
```

它在 Colab 中可以运行。但在本地 PC 的终端里，可能会出现下面这样的错误。

```text
ModuleNotFoundError: No module named 'numpy'
```

这个错误并不表示平均值计算代码写错了。它表示当前 Python 环境里没有准备好 NumPy。

这时如果把问题拆成下面这样，就更容易找到原因。

- 代码需要什么：NumPy
- 当前环境里缺少什么：NumPy 包
- 解决方向：在当前使用中的 Python 环境里安装 NumPy，或者查看所需包列表并重新搭建环境

所以，只记得“我装过包”是不够的。还要留下装在了哪个环境、哪个包、哪个版本。

## 可复现性是以后还能再次运行的条件

可复现性（reproducibility）是指：在同样代码、同样条件下再次运行时，仍然可以期待同样行为的性质。

在 AI 和数据实践中，可复现性很重要。阅读数学说明时，这个问题看起来可能不大，但一旦开始运行代码，环境差异就可能改变结果。

- Python 版本可能不同。
- 包版本可能不同。
- 操作系统可能不同。
- 数据文件位置可能不同。
- Colab runtime 可能已经被重置。

因此，如果想共享实践内容，只给代码可能不够。你还需要把“我是在哪个环境里运行的”一起留下。

## 示例：一个月后再次打开学习笔记本

在 AI 学习中，“今天运行过的笔记本”一个月后再打开，是很常见的事。

在运行当天，下面这些条件是成立的。

- Colab runtime 处于开启状态。
- `numpy`、`pandas`、`matplotlib` 已经安装好了。
- 数据文件上传到了 `/content/data/` 文件夹。
- 代码单元从上到下按顺序执行过。

一个月后，情况可能已经不同。

- Colab runtime 被重置了，手动安装过的包消失了。
- 数据文件没有重新上传。
- 从中间单元开始执行，所以前面创建的变量不存在。
- 默认包版本改变了。

这时如果立刻判断“代码错了”，就可能错过真正原因。首先要检查执行条件有没有重新搭起来。可复现性就是一种让这种检查更容易的记录习惯。

## requirements 文件是留下安装列表的方法

pip 文档把 requirements files 说明为：交给 `pip install` 的安装项目列表文件。常见文件名就是 `requirements.txt`。

例如，可以创建下面这样的文件。

```text
numpy
pandas
matplotlib
```

然后可以像下面这样安装。

```bash
python -m pip install -r requirements.txt
```

这里这样理解。

- `requirements.txt` 不是 Python 代码。
- 它也不是终端命令。
- 它是写下“需要安装哪些包”的文件。

如果有这个文件，别人就能更容易知道“这个项目需要哪些包”。

## 示例：把一个小实践文件夹交给别人

假设一个小实践文件夹是下面这样组成的。

```text
score-summary/
  summary.py
  scores.csv
  requirements.txt
```

`summary.py` 会读取 CSV 文件并计算平均值。

问题场景：确认交给别人的小实践代码需要哪些包。
输入（input）：用 `pandas` 读取 CSV 并计算平均值的脚本。
期望输出（output）：如果准备好所需环境，就会输出平均分。
要确认的概念：只交代码时，很难知道需要哪些包，所以 requirements 文件需要一起提供。

```python
import pandas as pd

scores = pd.read_csv("scores.csv")
print(scores["score"].mean())
```

如果只交这个文件，接收的人很难立刻知道是否需要 `pandas`。所以要把需要的包写进 `requirements.txt`。

```text
pandas
```

接收的人进入该文件夹后，可以用下面的命令准备好所需包。

```bash
python -m pip install -r requirements.txt
```

这个例子里重要的一点是，`requirements.txt` 不是执行代码的文件。它是留下代码所依赖的外部包列表的文件。

## 固定版本意味着缩小范围

包会随着时间变化。今天安装的 NumPy，并不能保证一年后安装到的还是同样版本。

所以可以把版本写下来。

```text
numpy==2.0.0
pandas==2.2.2
matplotlib==3.9.0
```

`==` 表示指定某个特定版本。这种方式可以称为版本固定（version pinning）。

pip 用户指南说明，可以把 `pip freeze` 的结果写入 requirements 文件，用于可重复安装（repeatable installs）。这时，文件里会记录执行 `pip freeze` 当时环境中已安装的包和版本。

例如，你可能会遇到下面这条命令。

```bash
python -m pip freeze > requirements.txt
```

然后在另一个环境里，可以像下面这样安装。

```bash
python -m pip install -r requirements.txt
```

但是，固定版本并不能让所有问题都消失。操作系统、Python 版本、硬件、包分发状态都可能产生影响。这里把它理解为“提高可复现性的出发点”。

例如，在制作学习资料时，可以考虑下面两种方式的差别。

- `pandas`：可能会安装最新版本，因此随着时间推移环境可能改变。
- `pandas==2.2.2`：因为要求特定版本，所以能更接近当时的环境。

刚开始学习时，不一定要把所有包都严格固定。但如果是书中示例、课程材料、团队项目这类需要让别人再次运行的代码，版本记录的重要性就会提高。

## requirements 文件和项目配置文件的角色不同

Python Packaging User Guide 区分了 requirements 文件与包安装要求。这里值得记住下面这个差别。

- requirements 文件：为了构成某个特定环境而要安装的列表
- 项目配置文件：用于分发包，或说明项目元数据的文件

本 Part 的实践不会处理复杂的包分发结构。因此，把 `requirements.txt` 理解为“重新搭建实践环境所需的安装列表”即可。

## 即使在 Colab 中，可复现性也不会消失

Colab 很容易开始使用。但可复现性问题并不会消失。

Colab runtime 可能被重置。那时之前安装过的包也可能消失。并且，Colab 提供的默认包版本也可能随着时间发生变化。

所以，最好在笔记本顶部留下所需安装命令，或者养成记录“我是在哪个环境里运行的”的习惯。

问题场景：当再次打开 Colab 笔记本时，能够先重新准备好所需包。
输入（input）：用于安装 NumPy、pandas、matplotlib 的 `%pip` 命令。
期望输出（output）：这三个包会被安装到当前 Colab runtime 中。
要确认的概念：即使在 Colab 中，如果想提高可复现性，也要把所需安装命令和环境备注一起留下。

```python
%pip install numpy pandas matplotlib
```

这个命令很方便，但从长期看，把包版本和执行日期一起留下会更安全。

例如，可以在笔记本最上方留下下面这样的简短备注。

- 编写日期：2026-06-24
- 执行环境：Google Colab
- 主要包：numpy, pandas, matplotlib
- 再次运行时要检查的内容：runtime 是否被重置，数据文件是否已上传

即使只是这个程度的备注，也能减少以后反复追踪同一错误所花的时间。

## 在实践项目里至少要留下的信息

不需要一下子就做出完美的可复现环境。但养成留下下面这些信息的习惯是好的。

- 使用的是哪个 Python 版本
- 需要哪些包
- 重要包的版本是什么
- 代码是以哪个文件夹为基准运行的
- 数据文件应该放在哪里
- 是 Colab 还是本地 PC

有了这些信息，将来出现错误时，就更容易缩小原因范围。

## 用案例来看

### 案例 1. 一个月后重新打开的笔记本为什么突然不能用了

假设有一位学习者重新打开了上个月还能顺利运行的数据分析笔记本。当时图表能正常显示，CSV 也能正确读取，但这一次却同时出现了包错误和文件路径错误。

人很容易想到“是不是笔记本文件坏了”。但实际上，更大的可能是 Colab runtime 被重置了，包版本变了，或者数据文件位置变了。也就是说，问题更主要在于执行条件没有被重新复现出来，而不是代码本身。

本节所说的 `dependency`、`reproducibility`、`requirements.txt`、`version pinning`，就是为了减少这种失败而设置的装置。要想把代码再次运行起来，就必须把它当时依赖的是哪些包、哪些版本也一起留下。

可以通过是否存在安装列表和版本记录来判断这个结果。如果没有 `requirements.txt`，只是靠记忆去记包，那可复现性就是薄弱的。相反，如果所需包和版本都有记录，就已经有了重新搭出同样环境的起点。

## 检查清单

- 能把依赖（dependency）解释为我的代码运行所需的外部包。
- 能把可复现性（reproducibility）解释为以后还能再次运行同一份代码的条件。
- 能说明 `requirements.txt` 是装载待安装包列表的文件。
- 能说明 `python -m pip install -r requirements.txt` 是根据 requirements 文件来安装包的命令。
- 能说明 `pip freeze` 可以用来记录当前环境里安装的包和版本。
- 能说明版本固定可以提高可复现性，但并不能解决所有问题。
- 能检查这段代码依赖哪些外部包、它们装在哪个 Python 环境里、以及是否留下了以后重建同样环境的记录吗？

## 来源与参考资料

- Python Packaging Authority, [User Guide](https://pip.pypa.io/en/stable/user_guide/){: target="_blank" rel="noopener noreferrer" }, pip documentation，确认日期：2026-06-24。
- Python Packaging Authority, [pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/){: target="_blank" rel="noopener noreferrer" }, pip documentation，确认日期：2026-06-24。
- Python Packaging Authority, [install_requires vs requirements files](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide，确认日期：2026-06-24。

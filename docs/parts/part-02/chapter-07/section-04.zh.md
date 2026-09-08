# P2-7.4 虚拟环境（virtual environment）与包（package）

> Section ID: `P2-7.4`
> Version: `v2026.09.08`

虚拟环境(virtual environment)让每个项目拥有独立的 Python 包集合。如果安装包的 Python 与执行代码的 Python 不同，即使安装成功，`import` 也可能失败。

| 术语 | 本节先要抓住的意思 |
| --- | --- |
| 虚拟环境（virtual environment） | 按项目分开的 Python 执行空间。 |
| 包（package） | 可以拿到 Python 里使用的一组代码。 |
| `pip` | 安装包的工具。 |
| `import` | 在 Python 代码里载入已经准备好的包的语句。 |
| `.venv` | 放在项目文件夹中的典型本地虚拟环境目录名。 |

## 项目隔离与安装位置

| 标准 | 为什么重要 |
| --- | --- |
| 虚拟环境是按项目划分的 Python 执行空间 | 因为不同项目可能需要不同版本的工具 |
| 安装和 `import` 是不同阶段 | 安装是准备，`import` 是在代码里真正载入使用 |
| 最常见的失误是安装的环境和运行的环境不同 | 同一台电脑里也可能存在多个 Python 空间 |

## venv 的引入背景

PEP 405 是把 `venv` 加入 Python 标准库的提案。这份文档创建于 2011 年，目标版本是 Python 3.3。PEP 405 的动机（motivation）说明，当时像 `virtualenv` 这样的第三方虚拟环境工具，已经被广泛用于依赖管理（dependency management）、隔离（isolation）、在没有系统管理员权限的情况下安装和使用包，以及在多个 Python 版本上做自动化测试等工作。

如果从入门者的视角把这段背景压缩一下，大致就是下面这些原因。

- Python 包变多了：不同项目所需的外部代码开始不同。
- 不能随便改系统 Python：那样可能会破坏操作系统或其他程序使用的 Python 环境。
- 很多场景需要在没有管理员权限时安装：个人项目或服务器账号里，往往不能随意更改整个系统。
- 需要测试多个项目和多个 Python 版本：只靠一个全局安装空间，很难避开冲突。

## 各项目的包版本

例如，项目需求可能像下面这样不同。

- 项目 A 是按 `numpy 1.x` 编写的。
- 项目 B 是按 `numpy 2.x` 编写的。
- 如果把它们混在同一个空间里，可能会有一边坏掉。

虚拟环境（virtual environment）就是为了减少这种冲突，按项目划分 Python 执行空间的方法。Python 官方文档说明，`venv` 会创建轻量级虚拟环境，而且每个虚拟环境都可以拥有彼此独立的一组 Python 包。

- 项目 A 的虚拟环境：安装项目 A 所需的包。
- 项目 B 的虚拟环境：另外安装项目 B 所需的包。

## 虚拟环境与共享文件

虚拟环境是运行项目所需的外围环境。它和项目的正文或代码本身并不是一回事。

例如，在某个项目文件夹里，你可能会看到一个名为 `.venv` 的文件夹。这个文件夹是一个本地执行环境，里面装着运行 Python 或构建文档所需的包。它不是项目正文文件，也不是代码本身。

所以，通常不会把虚拟环境文件夹提交到 Git。Python 官方文档也说明，虚拟环境通常可以在项目目录里以 `.venv` 这样的名称创建，而且一般不会放进源码管理系统中。

因此通常会像下面这样划分。

- 要提交的内容：原稿、代码、配置文件、示例文件
- 不提交的内容：我在自己电脑上创建的虚拟环境文件夹

相比共享虚拟环境本身，更稳妥的是记录所需的包，使其可以重新安装。

## Python 包

包（package）是为了让你能在 Python 中拿来使用而分发的一组代码。NumPy、Pandas、Matplotlib 这类工具都属于这里。

这里同样先区分三个层次。

- Python：语言本身和执行程序
- 包：可以拿到 Python 里使用的一组代码
- 包仓库：可以下载包的地方

Python Packaging User Guide 介绍了使用 `pip` 和 `venv` 在虚拟环境中安装包的流程。这里最重要的是，安装包和在代码里载入包是不同的事。

## pip 安装与 import

下面这条命令是在终端里安装包的命令。

```bash
python -m pip install numpy
```

这是一条终端命令，不是写在 Python 代码文件中的语句。`python -m` 用指定的 Python 执行模块，此处运行 pip 来安装 NumPy。

相反，下面的是 Python 代码。

在已安装 NumPy 的 Python 中运行 `import numpy as np`，即可使用名称 `np`，不会产生单独输出。

```python
# 这里在 Python 代码中导入当前环境已安装的 NumPy 包。
import numpy as np
```

这段代码表示把已经安装好的 NumPy 载入当前 Python 代码中，以便使用。

这两种语句不能混在一起看。

| 目的 | 示例 | 输入位置 |
| --- | --- | --- |
| 安装包 | `python -m pip install numpy` | 终端 |
| 使用包 | `import numpy as np` | Python 代码 |

- `install`：在我的执行环境里准备好这个包
- `import`：在当前 Python 代码里使用那个包

## 安装环境与执行环境

入门者经常遇到的错误，就是“明明安装过了，但 Python 说它不存在”。

这时就要把“装到了哪里”和“从哪里运行”分开来看。

例如，安装的地方和运行的地方可能会像下面这样错开。

- 你安装到了系统 Python，但却用虚拟环境中的 Python 来运行。
- 你安装到了虚拟环境 A，但却在虚拟环境 B 中运行。
- 你安装在了 Colab 里，但却在本地 PC 上运行。

包并不是抽象地“安装在电脑某个地方”。它们是安装到某个特定的 Python 执行环境中的。所以，使用虚拟环境时，不管是安装包还是运行代码，都应该以同一个虚拟环境为基准。

## 用虚拟环境的 Python 安装与执行

在项目文件夹创建虚拟环境后，可直接指定其中的 Python 路径来安装和导入包。这种方式不依赖激活状态。

在 macOS/Linux 终端依次运行以下命令，需要已安装 `python3`。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install numpy
.venv/bin/python -c "import numpy; print(numpy.__version__)"
```

在 Windows PowerShell 中，如果可用 `python` 命令运行 Python，则使用以下命令。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy
.\.venv\Scripts\python.exe -c "import numpy; print(numpy.__version__)"
```

第一条命令创建 `.venv`，第二条在其中安装 NumPy。最后一条中的 `-c` 将后面的字符串作为 Python 代码执行，打印已安装的 NumPy 版本。

只创建 `.venv`，然后运行普通的 `python -m pip install numpy`，可能会安装到另一个 Python 中。也可以使用激活(activate)方式，但像上面这样直接指定可执行文件路径，能从命令看出使用哪个环境。

## Colab 运行时中的包

Colab 是在浏览器中编辑代码、在运行时执行代码的笔记本环境。使用托管运行时，无需在本地安装 Python。

但即使在 Colab 里，包安装和执行环境的问题也不会消失。

Colab 代码单元中的 `%pip` 将包安装到当前笔记本内核。运行下面的单元，即可在该环境中准备 NumPy。

```python
# 这条命令是在 Colab/Jupyter 代码单元中把 NumPy 安装到当前运行时。
%pip install numpy
```

这条命令会把包安装到当前笔记本 runtime 中。如果 runtime 被重置，可能就需要重新安装这些包。另外，本地 PC 里的 `.venv` 和 Colab runtime 也不是同一个空间。

总结一下，这两个空间是不同的。

- Colab runtime：浏览器之外的外部执行环境
- 本地虚拟环境：围绕我电脑上的项目文件夹而存在的执行环境

## 文件夹同名，环境不同

假设两个项目各自都有 `.venv`。

```text
project-a/.venv/
project-b/.venv/
```

把 NumPy 安装到 `project-a/.venv` 的 Python，并不会自动安装到 `project-b/.venv`。如果两个环境均按默认设置创建，且 B 没有 NumPy，在 B 的 Python 中执行 `import numpy` 会产生 `ModuleNotFoundError`。

即使文件夹都叫 `.venv`，完整路径不同就是独立的环境。比较 `sys.executable` 打印的 Python 路径与安装命令所用的路径，即可确认安装到了哪个项目环境。

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

- Carl Meyer, [PEP 405 – Python Virtual Environments](https://peps.python.org/pep-0405/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals，确认日期：2026-07-20。作为虚拟环境拥有自己的包集合和 Python 可执行文件，并可与系统 site-packages 隔离这一设计说明的依据。
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-09-08。用于确认用 `venv` 创建和激活虚拟环境，以及环境内部 Python 与包状态相互分离的说明。
- Python Packaging Authority, [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide，确认日期：2026-07-20。用于确认按项目创建虚拟环境，并通过 `python -m pip install` 安装包的流程。
- Python Software Foundation, [Installing Python Modules](https://docs.python.org/3/installing/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认 `pip`、`venv`、PyPI、`python -m pip install` 的基本角色，以及优先考虑虚拟环境而不是系统级安装的语境。

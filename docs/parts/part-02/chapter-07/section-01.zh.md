# P2-7.1 本地环境(local environment)与运行时(runtime)

> Section ID: `P2-7.1`
> Version: `v2026.09.08`

Python 代码由解释器(interpreter)读取并执行。本地环境(local environment)包括电脑上的 Python、包、文件与设置；运行时(runtime)指实际运行代码的程序与资源。即使在浏览器中输入代码，也可能由另一台电脑执行。

## AI 实验与 Python

学 AI 时，Python 会反复出现。这时很自然会问，`为什么偏偏是 Python？`

Python 在 1980 年代末由 Guido van Rossum 开始设计，并在 1991 年公开。Python 官方 FAQ 说明，Python 受到了 ABC 语言经验的影响，也是在一个背景下诞生的：仅靠 C 程序或 shell 脚本，很难处理系统管理工作，因此需要一种更可扩展的脚本语言。

这段历史里真正重要的是：Python 从一开始就是一种既适合人阅读和书写的高级语言，同时又能连到真实系统工作的执行工具。

所以 Python 很适合学习、自动化、数据处理与实验代码。Python 官方 FAQ 也说明，Python 语法清晰、标准库大、又有交互式解释器，因此也适合作为第一门语言。

AI 领域里为什么经常看到 Python，也和这条脉络连在一起。

- 把公式翻成代码比较容易。
- 可以快速跑小实验。
- NumPy、Pandas、Matplotlib 这类工具很多。
- 机器学习和深度学习库大多聚集在 Python 生态里。

Python 并非唯一的语言。实际服务也使用 C++、Java、JavaScript、Go、Rust 等语言，但在 AI 学习与实验中，经常会遇到 Python。

## 终端命令与 Python 代码

终端(terminal)是交换命令与结果的窗口，shell 是解释输入命令的程序。可以在 macOS Terminal 或 Windows Terminal 中使用 shell，Bash 与 PowerShell 都是 shell 的例子。

在终端的 shell 提示符下输入以下命令，会打印 Python 版本。

```bash
python --version
```

`print("hello")` 是 Python 代码。在笔记本代码单元或 Python 解释器中输入，会打印 `hello`。

```python
# 打印字符串的 Python 语句。
print("hello")
```

只是把这句话写在记事本里，并不会执行。需要由程序读取并执行 Python 代码。在终端输入 `python --version` 与在 Python 中输入 `print("hello")` 是不同的操作。

| 语句 | 输入位置 | 结果 |
| --- | --- | --- |
| `python --version` | 终端的 shell 提示符 | 打印 Python 版本 |
| `python example.py` | 终端的 shell 提示符 | 执行 example.py |
| `print("hello")` | Python 代码或笔记本代码单元 | 打印 hello |
| `%pip install numpy` | 基于 IPython 的笔记本代码单元 | 在该内核中安装 NumPy |

## 解释器的执行方式

Python 解释器(Python interpreter)是读取并执行 Python 代码的程序。执行方式不同，提供代码的位置也不同。

| 方式 | 使用方法 |
| --- | --- |
| 交互式执行 | 在终端运行 `python`，再于 `>>>` 输入 Python 代码 |
| 脚本执行 | 把代码保存为 example.py，在终端运行 `python example.py` |
| 笔记本执行 | 运行连接到 Python 内核的代码单元 |

要结束交互式执行并返回 shell，在 `>>>` 输入 `exit()`。提示符 `>>>` 本身不是要输入的代码。

## 本地环境的组成

`本地环境(local environment)` 指的是代码在我电脑内部运行所依赖的条件。其中可能包括操作系统、Python 安装位置、包安装状态、当前工作文件夹、环境变量等。

即使是同一份代码，不同电脑上的结果也可能不同。

例如，不同电脑的条件可能这样不同。

- 我的电脑上已经安装了 NumPy，但别人的电脑上可能没有。
- 我的电脑使用 Python 3.12，别人的电脑可能是 Python 3.10。
- 在我的电脑上文件路径是对的，但在另一台电脑上文件位置可能不同。

所以，在练习文档里，和“代码”同样重要的，是 `到底在哪里执行。`

## 本地执行与 Colab 运行时

运行时(runtime)是代码实际执行的位置。本地执行时，由自己的电脑运行；使用 Colab 托管运行时，则由 Google 提供的环境处理代码。

| 执行方式 | 运行时 |
| --- | --- |
| 执行 Colab 代码单元 | Colab runtime |
| 在自己电脑终端里运行 | 本地 Python 环境 |
| 开启虚拟环境后运行 | 那个虚拟环境里的 Python 和包 |

Colab 很方便。它不需要安装 Python，就能在浏览器里运行。但 runtime 可能会断开、文件可能会消失、服务策略也可能变化。

本地 PC 一开始设置起来比较麻烦。但项目文件、包版本、运行方式都可以由自己直接管理。

总结起来就是下面这样。

- Colab：容易开始，运行时由外部服务管理。
- 本地 PC：需要先设置，但运行时由我自己管理。

## 项目专用虚拟环境

`虚拟环境(virtual environment)` 是一种装置，能为每个 Python 项目创建各自独立的执行空间。Python 官方文档说明，`venv` 能创建轻量级虚拟环境，而每个虚拟环境都可以拥有独立的 Python 包集合。

为什么需要它？项目 A 可能需要 `numpy 1.x`，而项目 B 可能需要 `numpy 2.x`。如果把两者全都混装到同一台电脑里，就可能冲突，所以要把空间按项目分开。

虚拟环境本身并不是项目代码。Python 官方文档也说明，虚拟环境通常建在 `.venv` 或 `venv` 这样的目录里，而且不会被放进源码管理系统。对任何项目来说，`.venv` 都是为了执行而准备的本地环境，不是正文文件，也不是代码本体。

在项目文件夹的终端中运行以下命令，会在 `.venv` 目录创建虚拟环境。

```bash
python -m venv .venv
```

选择所创建虚拟环境的 Python 来运行代码，才能使用其中安装的包。创建与激活命令参见[虚拟环境与包安装](section-04.zh.md)。

## 包安装与 import

包(package)是将相关代码组织起来以便复用的单位。NumPy、Pandas、Matplotlib 都属于此类工具。

各部分的作用如下。

- Python：语言本身和执行程序
- 包：在 Python 里拿来借用的代码集合
- `pip`：安装包的工具

例如，安装 NumPy 的命令和把它导入代码中，是不同的事。

```bash
python -m pip install numpy
```

在安装了 NumPy 的 Python 中运行以下代码，会以 `np` 为名导入 NumPy。成功时没有单独输出，而是继续执行下一条语句。

```python
# 这里确认当前运行环境能否导入 NumPy。
import numpy as np
```

前者是在安装。后者是在 Python 代码里把它加载进来准备使用。

## Colab 中成功的 import 在本地失败

假设 `import numpy as np` 在 Colab 中能执行，在本地却出现以下错误。

```text
ModuleNotFoundError: No module named 'numpy'
```

这表示正在运行的 Python 找不到 NumPy。它可能安装在另一个 Python 或虚拟环境中，因此应先确认实际使用的解释器。在出现错误的同一个笔记本内核或相同 Python 执行方式下运行以下代码，会打印解释器文件路径。

```python
import sys

# 当前执行此代码的 Python 的位置。
print(sys.executable)
```

确认该路径是否为项目原本打算使用的 Python。在终端选定该 Python 后，可用 `python -m pip show numpy` 检查安装状态。未安装时，用 `python -m pip install numpy` 安装到这个 Python 中。

如果安装命令成功后仍有相同错误，应比较安装与执行代码所用的 Python 路径是否相同。只检查包名，无法区分安装在不同运行环境中的情况。

## 执行问题的检查位置

| 问题 | 检查内容 |
| --- | --- |
| 找不到文件 | [终端与工作文件夹](section-02.zh.md) |
| 不知道怎样运行 Python 代码 | [解释器与脚本执行](section-03.zh.md) |
| 安装后无法导入包 | [虚拟环境与包安装](section-04.zh.md) |
| 换电脑后结果不同 | [依赖与可复现性](section-05.zh.md) |

## 检查清单

- 能把 `本地环境(local environment)` 解释成代码在我电脑上运行的条件。
- 能把 `运行时(runtime)` 解释成代码真正执行的地方。
- 能区分终端命令和 Python 代码。
- 能把 Python 解释器解释成读取并执行 Python 代码的程序。
- 能把虚拟环境解释到“按项目划分的执行空间”这个程度。
- 能用入门层次说明包安装和 `import` 是两件不同的事。
- 能说明 Colab 和本地 PC 都是运行时，但管理方式不同。
- 能先检查 `在哪里运行`、`由什么执行`、`需要什么包`、`那个包安装在哪里`。

## 来源与参考资料

- Python Software Foundation, [Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-07-20。用于支撑如何调用 Python 解释器，以及如何区分交互式输入与脚本执行。
- Python Software Foundation, [General Python FAQ](https://docs.python.org/3/faq/general.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-07-20。用于确认 Python 是解释型、交互式编程语言，并可在多种操作系统上使用的基础说明。
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-07-20。用于确认虚拟环境会在隔离目录中拥有自己的 Python 安装与包状态。
- Python Packaging Authority, [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide, 确认日期: 2026-07-20。用于确认按项目创建虚拟环境、激活虚拟环境并安装包的流程。

- Python Software Foundation, [sys.executable](https://docs.python.org/3/library/sys.html#sys.executable){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-09-08。用于确认当前 Python 解释器的可执行文件路径。

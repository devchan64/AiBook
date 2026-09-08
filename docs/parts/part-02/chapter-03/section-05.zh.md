# P2-3.5 Python 运行环境：Colab 与本地 PC

> Section ID: `P2-3.5`
> Version: `v2026.09.08`

Python 代码可以在 Colab 笔记本的代码单元中运行，也可以在本地 PC 的 Python 解释器中运行。安装命令应符合运行环境，已安装的包则在 Python 代码中通过 `import` 导入。

本文依据 2026 年 7 月 19 日确认的 Google Colab 官方说明和 FAQ、IPython `%pip` 文档、pip 用户指南编写。Colab 是外部服务，因此未来它的 UI、使用条件、免费范围、运行策略、甚至服务是否持续，都可能发生变化。如果你阅读这一节时，Colab 已无法提供、或看起来和这里不同，那么应另外查看 Google Colab 官方文档和当前服务状态。

## 安装、导入与运行

| 想做的事 | Colab 代码单元 | 本地 PC 终端 | Python 代码 |
| --- | --- | --- | --- |
| 安装 NumPy | `%pip install numpy` | `python -m pip install numpy` | 不用写 |
| 导入 NumPy | `import numpy as np` | 不用写 | `import numpy as np` |
| 运行简单计算 | `print(np.array([1, 2]))` | 可以通过 `python example.py` 来运行 | `print(np.array([1, 2]))` |

## 命令的执行位置 {#_2}

“运行 Python 代码”这句话并不只有一种意思。即使是同一个示例，只要运行位置不同，命令的形式也会改变。

| 执行位置 | 英文 | 它表示什么 | 示例命令 |
| --- | --- | --- | --- |
| Colab 代码单元 | Colab code cell | 在浏览器笔记本中的代码单元里运行 | `%pip install numpy` |
| 本地 PC 终端 | local terminal | 在自己电脑的终端程序中运行 | `python -m pip install numpy` |
| Python 代码 | Python code | 在 `.py` 文件或代码单元里的 Python 语句中运行 | `import numpy as np` |

只要漏掉这个区分，就很容易把 `%pip`、`python -m pip`、`import` 当成同一种东西。它们都可能和 NumPy 有关，但执行位置和作用并不相同。

1. 包是在 Colab 代码单元或本地 PC 终端里安装的。
2. 已安装的包要在 Python 代码内部通过 `import` 导入。

执行位置错误时，可能出现以下问题。

| 混淆场景 | 为什么会卡住 | 修正方法 |
| --- | --- | --- |
| 把 `%pip install numpy` 写进 `.py` 文件 | 因为把安装命令和 Python 代码混在一起了 | 在代码单元中运行，或改用终端的 `python -m pip` 命令。 |
| 想把 `import numpy as np` 当成终端命令直接运行 | 因为把 Python 语句当成了 shell 命令 | 在 Python 解释器或 `.py` 文件中运行。 |
| 把 Colab 示例原样复制到本地环境 | 因为执行位置变了，但语法没跟着变 | 区分笔记本专用安装命令与本地终端命令。 |

## Colab 笔记本

Google Colab 是一种托管服务，它让你在浏览器里以 Jupyter Notebook 的形式运行 Python 代码。即使个人电脑上没有安装 Python，也可以创建并运行代码单元。

- [Google Colab](https://colab.research.google.com/){: target="_blank" rel="noopener noreferrer" }
- [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }

先打开 `Welcome to Colab` 指南，确认代码单元是怎样运行的。本节里的示例都非常小，因此不需要 GPU 或 TPU。不过 Colab 可能会有 Google 账号要求、运行时限制和资源限制。

## 本地 PC 运行

所谓在本地 PC(local PC) 上运行，意思是使用自己电脑中安装好的 Python 和终端。命令会在 macOS 的 Terminal、Windows Terminal、PowerShell、Linux shell 等程序中运行。

例如，在本地 PC 终端里，可以这样安装 NumPy。

```bash
python -m pip install numpy
```

而在 Python 文件里，则这样导入 NumPy。

```python
# 这一行是在 Python 代码里导入 NumPy。
import numpy as np
```

## 代码单元中的 Python 语句

Colab 笔记本里有写文字的单元，也有执行代码的单元。Python 代码要放进代码单元(code cell)里运行。

例如，下面这段代码可以放进代码单元并直接运行。

```python
# 这是确认 Colab 代码单元正在运行的最小输出例子。
print("hello, colab")
```

运行结果会像这样出现。

```text
hello, colab
```

这里的 `print(...)` 是 Python 代码。相对地，安装包的命令在性质上和普通 Python 代码略有不同。

## 笔记本安装命令 `%pip`

在很多情况下，Colab 环境里已经准备好了 NumPy。但由于环境可能变化，如果需要，也可以在代码单元里运行下面这个命令。

```python
# %pip 是在 Colab/Jupyter 代码单元中使用的安装命令。
%pip install numpy
```

这里的 `%pip` 不是普通 Python 语法，而是 Jupyter Notebook 系环境里使用的 magic command。它的意思是“把这个包安装到当前笔记本内核(kernel)里”。

在 Colab 或 Jupyter 文档里，你也可能看到用感叹号(`!`)运行 shell 命令的示例，比如：

```python
# 感叹号形式是在代码单元中调用终端命令的方式。
!pip install numpy
```

这里我们优先使用 `%pip install numpy`，因为它更明确地表达了“安装目标是当前笔记本环境”。

安装与导入的执行位置如下。

```mermaid
--8<-- "assets/part-02/chapter-03/execution-location-flow-zh.mmd"
```

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

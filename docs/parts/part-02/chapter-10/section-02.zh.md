# P2-10.2 Jupyter、Colab 与本地执行的区别

> Section ID: `P2-10.2`
> Version: `v2026.09.15`

## 工具与执行位置

Colab FAQ 将 Jupyter 描述为 Colab 所基于的开源项目。Colab 是托管服务，用户无需自行下载、安装和运行本地服务，即可使用和分享 Jupyter 笔记本。

Jupyter 指工具和生态，Colab 指服务，本地执行指执行位置。下面对 Colab 的说明以 Google 管理的远程运行时为准。Colab 界面也可以连接本地运行时。

| 名称 | 含义 | 执行位置 |
| --- | --- | --- |
| Jupyter | 开源笔记本工具与生态 | 本地电脑、服务器、云等多种环境 |
| Colab | Google 提供的托管 Jupyter Notebook 服务 | Google 提供的远程运行时 |
| 本地执行 | 用自己电脑上的 Python 执行 | 本地电脑 |

因此，“Jupyter 还是 Colab”并非两个完全对立的选择。Colab 基于 Jupyter Notebook 的格式与工作方式，区别在于用户不必直接管理安装和服务器运行。

## 文档、运行时与文件

常见的混淆是把文件与执行状态当成同一件事。

笔记本文件通常使用 `.ipynb` 格式。Jupyter 架构文档说明，这种结构化数据包含代码、元数据、内容与输出，保存到磁盘时使用 JSON 结构和 `.ipynb` 扩展名。

拥有文件不等于其中的代码正在运行。

| 区分 | 含义 | 示例 |
| --- | --- | --- |
| 笔记本文件 | 保存代码、说明与部分输出的文档 | `practice.ipynb` |
| 内核（kernel） | 执行代码并保留变量的进程 | 与笔记本连接的 Python 内核 |
| 运行环境（runtime） | 内核使用的 Python、包和计算资源 | Colab VM 内的环境、本地虚拟环境 |
| 文件系统 | 代码读写文件的位置 | 本地文件夹、Colab VM、Google Drive |

运行时消失后，笔记本文件仍可能保留。代码单元仍在，其中安装的包或创建的临时文件却可能已经消失。

Colab FAQ 说明，代码在分配给账户的虚拟机中运行；虚拟机会在闲置一段时间后被删除，也有最长存续时间。

## 执行方式比较

即使使用相同的笔记本格式，实际执行代码的计算机和可访问文件范围也可能不同。

| 标准 | Colab | 本地 Jupyter | 本地脚本 |
| --- | --- | --- | --- |
| 执行位置 | Google 远程运行时 | 本地电脑 | 本地电脑 |
| 安装负担 | 低 | 中等 | 中等 |
| 文件访问 | Colab VM、上传、Drive 集成 | 便于直接访问本地文件 | 便于直接访问本地文件 |
| 结果记录 | 便于保留在笔记本中 | 便于保留在笔记本中 | 需要单独输出或日志 |
| 重复自动化 | 有限制 | 可以，但要注意笔记本状态 | 更自然 |
| 分享 | 便于通过链接分享 | 需要文件或服务器访问权 | 需要代码和环境说明 |
| 注意事项 | 运行时与资源限制、Drive 权限 | 安装与包管理 | 说明与结果容易分离 |

没有一种环境始终最好。学习目标与执行需求不同，适合的环境也会不同。

## Colab 的准备与资源

Colab 的启动门槛较低。在本地安装 Python、Jupyter、NumPy 或 pandas 之前，就可以在浏览器中执行代码。

对于本部分前面的小型数学计算、列表与字典示例、基础 NumPy 计算，Colab 可以满足需求。

Colab 适用于以下情况：

- 尚未安装 Python。
- 希望在其他电脑上打开同一笔记本。
- 希望通过链接分享代码、说明与结果。
- 希望用小数据验证概念。
- 希望短时间试用 GPU 或 TPU 加速环境。

Colab 是外部服务，免费资源既不保证可用，也不是无限的；用量限制与运行时终止条件可能变化。FAQ 说明，用量限制、闲置超时、最长运行时间和 GPU 类型等因素会随时间变化。

应把 Colab 理解为快速开始学习和实验的远程工作空间，而非始终保留的个人电脑。

## 本地 Jupyter 的环境管理

本地 Jupyter 在自己的电脑上运行 Jupyter Notebook 或 JupyterLab 及其内核。如果连接的是服务器上的 Jupyter，文件访问也以该服务器为准。

优点是可以直接控制文件与环境。

- 直接读写电脑文件夹中的文件。
- 自行选择虚拟环境。
- 按项目管理包版本。
- 减少对网络连接和外部服务政策的依赖。

相应地，需要做更多准备：

- 安装 Python。
- 必要时安装 Jupyter 相关包。
- 管理项目专用虚拟环境。
- 记录依赖，以便在其他电脑上复现。

在浏览器中查看笔记本，并不能说明 Python 在哪里运行。可用文件和包取决于内核运行在本地电脑还是服务器上。

## 找不到已安装的包时

即使终端成功安装 NumPy，笔记本中的 `import numpy` 仍可能失败。如果终端和笔记本内核使用不同的 Python 环境，已安装的包也不同。下面的单元显示当前内核使用的执行文件和 Python 版本。

```python
import sys

print("Python executable:", sys.executable)
print("Python version:", sys.version.split()[0])
```

执行文件路径因电脑而异。如果本地内核没有使用预期的项目虚拟环境，应检查笔记本的内核选择。要把 NumPy 安装到当前内核环境，在笔记本代码单元中执行下面的命令。

```text title="IPython · 笔记本代码单元"
%pip install numpy
```

安装完成后，仍要单独执行 `import numpy as np`。升级已导入的包后，可能需要重启内核并从准备单元重新执行。安装问题应检查执行环境；找不到文件时应检查工作目录与路径。

## 把函数分离到模块

笔记本适合记录学习，但把所有代码都留在笔记本中，会让后续复用变得困难。

例如，每天读取文件并执行相同处理，或在多个项目中复用函数时，`.py` 文件更自然。

把下面的函数保存为 `stats_utils.py`。它返回非空分数列表的平均值。仅保存文件不会执行函数。

```python
def mean(values):
    return sum(values) / len(values)
```

如果文件位于 Python 可以找到的当前工作目录中，就能在笔记本或其他脚本中导入。下面的输出为 `67.33333333333333`。

```python
from stats_utils import mean

print(mean([82, 75, 45]))
```

笔记本保留输入与解释，模块让同一计算能在多份文档中复用。导入的模块会留在内存中，因此只修改 `.py` 文件并重复同一条 import，可能不会立即加载修改。这个示例中，可以重启内核并从导入单元重新运行，检查修改后的函数。

## 共享文档与环境准备

Colab FAQ 说明，分享内容包括笔记本的文本、代码、输出和评论，但不会同时分享正在使用的虚拟机、执行时准备的文件和库的安装状态。

| 会共享的内容 | 可能不会共享的内容 |
| --- | --- |
| 说明单元 | 运行时中的临时文件 |
| 代码单元 | 手动安装的包状态 |
| 已保存的输出 | 当前内存变量 |
| 评论或文档内容 | 个人 Drive 文件权限 |

因此，共享笔记本需要记录必要的准备步骤。

在前面说明的安装单元之后，导入包并记录版本。

下面的单元输出 NumPy 版本与平均值 `67.33333333333333`。版本取决于执行环境。

```python
import numpy as np

print(np.__version__)
print(np.mean([82, 75, 45]))
```

如果需要文件，也要说明从哪里获取。自己的运行时中有文件，不代表别人的运行时中也有。

## 按任务选择环境

可以根据文件位置、结果记录方式和重复执行需求选择环境。

| 情况 | 优先选择 |
| --- | --- |
| 安装 Python 仍有困难 | Colab |
| 查看小型计算与表格输出 | Colab 或本地 Jupyter |
| 大量读写本地文件 | 本地 Jupyter 或脚本 |
| 重复执行或自动化相同代码 | 本地脚本 |
| 同时展示说明与结果 | Colab 或 Jupyter 笔记本 |
| 严格固定包版本 | 本地虚拟环境 |

缺少包和路径错误需要不同的解决方法。应结合错误检查环境的准备状态。

## 案例：只存在于本地的 CSV

假设笔记本原本在电脑的 `project` 目录中读取 `project/data/scores.csv`，后来在全新的 Colab 远程运行时中打开。文档中的 `data/scores.csv` 字符串被带过去了，本地文件却没有一起传输。

下面的代码输出当前工作目录、文件的完整路径以及文件是否存在。`Path.cwd()` 指代码执行环境的工作目录。

```python
from pathlib import Path

path = Path("data/scores.csv")
print("working directory:", Path.cwd())
print("resolved path:", path.resolve())
print("file exists:", path.is_file())
```

本地工作目录下存在该文件时，最后输出为 `True`。新环境的相同相对路径下没有文件时，输出为 `False`。此时打开文件会产生 `FileNotFoundError`。

在新环境准备好文件后，要让保存位置与代码路径对应。如果直接上传到工作目录下并命名为 `scores.csv`，就应使用 `Path("scores.csv")`。要保留 `data/scores.csv`，则需把文件放在 `data` 文件夹内。

把笔记本交给别人时，也要记录输入文件位置、访问权限与包安装方法，才能重新执行相同计算。

## 检查清单

- 能解释 Jupyter 与 Colab 并非同一层面的概念。
- 能区分笔记本文件（`.ipynb`）与运行时。
- 能解释 Colab 代码可能在远程虚拟机上执行。
- 能解释分享笔记本为何不会同时分享运行时文件与包安装状态。
- 能比较本地 Jupyter 与本地脚本。
- 能解释文件路径问题如何源于执行环境。
- 能解释同一个 `.ipynb` 为何会因执行位置和运行时不同而具有不同的文件、包和共享条件。

## 来源与参考资料

- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, Google Colab，确认日期：2026-09-15。作为区分 notebook 中会共享的内容，以及不会一起共享的 runtime、VM、文件和已安装库状态的依据。
- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation，确认日期：2026-09-15。作为区分 Jupyter document、interface、kernel、执行位置和 runtime 的背景依据。
- Jupyter Notebook Team, [The Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Notebook documentation，确认日期：2026-07-20。作为说明本地 notebook server 和浏览器 notebook 使用流程的依据。
- Python Software Foundation, [sys.executable](https://docs.python.org/3/library/sys.html#sys.executable){: target="_blank" rel="noopener noreferrer" }, 核对日期：2026-09-15。确认内核 Python 执行文件的依据。
- Python Software Foundation, [Modules](https://docs.python.org/3/tutorial/modules.html){: target="_blank" rel="noopener noreferrer" }, 核对日期：2026-09-15。模块导入及会话内复用行为的依据。
- IPython, [%pip](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip){: target="_blank" rel="noopener noreferrer" }, 核对日期：2026-09-15。向当前内核环境安装包的命令依据。

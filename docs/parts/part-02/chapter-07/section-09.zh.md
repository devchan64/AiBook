# P2-7.9 补充学习：检查本地 Python 环境问题

> Section ID: `P2-7.9`
> Version: `v2026.09.08`

找不到 `python` 命令与 `import numpy` 失败，发生在不同位置。前者应检查 shell 的命令连接，后者应检查正在运行的 Python 的包状态。即使 Python 版本相同，也可能属于不同虚拟环境，因此还要比较可执行文件路径。

## 错误消息与检查对象

| 消息或情况 | 检查对象 |
| --- | --- |
| `python: command not found` | 执行命令名称、安装状态、PATH |
| `ModuleNotFoundError: No module named 'numpy'` | 当前 Python 中 NumPy 的安装状态 |
| `FileNotFoundError` | 当前工作文件夹与数据路径 |
| `Permission denied` | 写入位置与访问权限 |
| `SyntaxError` | Python 语法、是否将 shell 命令输入到 Python |

## 实际运行的 Python 命令

在终端检查所用 Python 命令的版本。

```bash
python --version
```

macOS/Linux 中可能使用 `python3 --version`，Windows 中根据安装方式可能使用 `py --version`。一个命令失败，不代表完全没有解释器。

PATH 是 shell 查找可执行文件所用的目录列表。即使已安装 Python，也可能因命令名称、PATH 或执行别名而无法调用。各操作系统的安装与命令连接检查，请参见 [Python 安装](section-07.zh.md)中的官方文档链接。

## 实际解释器与工作文件夹

在发生错误的笔记本内核或脚本执行环境中运行以下代码，会打印当前 Python 的可执行文件、环境路径与工作文件夹。

```python
import os
import sys

print("Python:", sys.executable)
print("环境:", sys.prefix)
print("虚拟环境:", sys.prefix != sys.base_prefix)
print("工作文件夹:", os.getcwd())
```

标准 `venv` 环境中，`sys.prefix` 与 `sys.base_prefix` 不同。这是在直接确认运行中的 Python 属于哪个环境，而非凭记忆判断是否激活。编辑器或笔记本选定的解释器可能与终端的 Python 不同。

## 版本相同的不同虚拟环境

以下示例展示两个不同项目的 Python 输出。

| 项目 | 安装时使用的环境 | 运行示例时使用的环境 |
| --- | --- | --- |
| Python 版本 | 3.12.3 | 3.12.3 |
| 可执行文件 | `/home/user/project-a/.venv/bin/python` | `/home/user/project-b/.venv/bin/python` |
| NumPy | 已安装 | 未安装 |

版本相同，但路径不同，因此是不同环境。A 中安装成功，B 中的 `import numpy` 仍可能失败。要运行项目 B，就向 B 的 Python 安装所需包。路径不同本身不一定是错误，判断标准是该环境是否满足要运行的项目要求。

## pip 与包的位置

在选定所需 Python 的终端运行以下命令。

```bash
python -m pip --version
python -m pip show numpy
```

第一条显示 pip 的版本与安装位置。第二条在 NumPy 已安装时显示版本与 `Location`；否则显示找不到包的消息。

`python -m pip` 使用命令开头的 Python 运行 pip。实际代码也需要用同一个 Python 执行，才能使用该安装。直接指定虚拟环境路径的方法，请参见[用虚拟环境的 Python 安装与执行](section-04.zh.md)。

如果缺少所需的 NumPy，就使用同一个 Python 安装。

```bash
python -m pip install numpy
```

在该环境执行以下代码，会打印 NumPy 版本与导入文件的位置。

```python
import numpy as np

print("NumPy:", np.__version__)
print("文件:", np.__file__)
```

如果有安装列表，可以用 `python -m pip install -r requirements.txt` 准备项目要求，而非逐个安装。

## 权限错误与包缺失

向系统区域安装包时，可能因没有写入权限而失败。在项目文件夹创建虚拟环境，再用该环境的 Python 安装，就能在不改变系统包的情况下准备所需包。

`Permission denied` 是访问权限问题，`ModuleNotFoundError` 表示运行中的 Python 找不到模块。后者应检查是否装到其他环境、安装未完成，或导入名称错误等情况。

## 根据检查结果采取措施

| 检查结果 | 下一步措施 |
| --- | --- |
| 没有可用的 Python 命令 | 检查安装状态与操作系统对应的执行命令 |
| 编辑器使用另一个项目的 Python | 选择目标项目的解释器 |
| 选定环境缺少所需包 | 用同一个 Python 的 pip 安装 |
| 有包，但缺少数据文件 | 检查文件位置、工作文件夹与输入数据准备 |
| 环境和输入正确，但仍报错 | 检查完整错误消息与代码要求的版本 |

将环境检查结果与[依赖与可复现性](section-05.zh.md)中所述的安装列表、数据和执行位置一同记录，便于重新运行时比较。

## 检查清单

- 能区分找不到命令与找不到包的错误。
- 能说明 Python 版本相同，可执行文件路径也可能不同。
- 能用 `sys.executable` 与 `sys.prefix` 检查当前环境。
- 能比较安装所用的 Python 与执行代码所用的 Python。
- 能通过 `pip show` 与导入结果确认包的安装和使用位置。
- 能根据错误消息分别检查命令、环境、权限与文件问题。

## 来源与参考资料

- Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认按平台设置 Python 与调用解释器的文档结构，作为本地环境检查顺序的背景依据。
- Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认 Windows 中 Python 执行命令和安装方式有单独的官方说明。
- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认 Unix/Linux 中 Python 执行命令和安装路径可能因环境而异。
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于支撑需要把虚拟环境是否激活与包安装位置一起检查这一说明。

- Python Software Foundation, [sys — System-specific parameters and functions](https://docs.python.org/3/library/sys.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-09-08。用于确认解释器与虚拟环境路径的 sys.executable、sys.prefix、sys.base_prefix 依据。

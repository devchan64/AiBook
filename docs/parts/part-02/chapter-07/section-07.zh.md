# P2-7.7 补充学习：什么时候需要安装 Python

> Section ID: `P2-7.7`
> Version: `v2026.09.08`

使用 Colab 托管运行时，不需要在自己的电脑上安装 Python。在本机执行 `.py` 文件或处理本地文件，则需要本地解释器。Python 可能已经安装，因此先检查执行命令与版本。

## 官方安装手册链接

链接收集日期：2026-07-20

安装画面和推荐方式会随着时间变化。真正进行安装时，不要只看本节说明，也要一起查看下面的官方文档。

- 整体安装与使用指南：Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }.
- 下载页面：Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }.
- Windows 中的安装与运行：Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }.
- macOS 中的安装与运行：Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }.
- Linux/Unix 平台中的使用：Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }.
- 虚拟环境：Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }.

## 执行位置与安装需求

| 标准 | 为什么重要 |
| --- | --- |
| 一开始并不一定非要本地安装 | 因为小型实践可以只靠 Colab 开始 |
| 本地安装是在自己的电脑上建立运行 Python 解释器的基础 | 如果把安装、虚拟环境、包准备看成一整团，判断就会变模糊 |
| 安装之后第一步要确认的是版本和执行命令 | 安装成功与命令连接成功不是同一回事 |

## Colab 托管运行时

在前期学习里，很多时候 Colab 就够了。

- 运行简单的 Python 代码
- 确认 NumPy 数组计算
- 处理小型表格数据
- 快速画图
- 按单元格跟着书里的示例代码做

浏览器负责代码输入与结果显示，托管运行时执行 Python 代码。无需本地安装 Python，即可完成上述任务。

但 Colab 不是自己的电脑。运行时由外部服务提供，会话可能重置，文件与包状态也不保证一直保留。

## 需要本地解释器的任务

要在自己的电脑执行以下任务，需要本地 Python。

- 从终端或编辑器运行 `.py` 文件。
- 读取本地数据文件，并将结果保存在同一台电脑。
- 创建项目虚拟环境并管理包。
- 在无网络连接时运行 Python 计算。

项目包含多个文件或属于 Git 仓库，并不意味着必须本地执行。远程运行时也可以管理项目与包。决定是否安装的条件是实际执行代码的位置，而非文件数量。

## Python 安装与命令连接

Python 安装，是在我的电脑上准备 Python 解释器（Python interpreter）的过程。Python 官方文档分别介绍了不同平台上的 Python 环境设置、解释器运行方式，以及便于工作的相关信息。

完成安装、命令连接与所需组件准备后，可以进行以下任务。

- 能在终端中运行 Python 命令。
- 能用 Python 运行 `.py` 文件。
- 能通过 `pip` 安装包。
- 能创建虚拟环境。

但仅仅安装，还没有结束一切。

即使安装了 Python，下面这些问题仍然可能存在。

- 终端里 `python` 命令可能不能工作。
- 在 macOS/Linux 中，可能需要使用 `python3` 命令。
- 在 Windows 中，可能会遇到 `py` 命令。
- 可能装了多个 Python 版本。
- 如果不用虚拟环境，不同项目的包可能会混在一起。

所以安装之后，不能只停在“安装好了”，而是要确认“哪个命令指向哪个 Python”。

## 检查各命令的 Python 版本

在终端里确认下面这条命令。

```bash
python --version
```

在 macOS 或 Linux 中，下面这条命令可能更自然。

```bash
python3 --version
```

在 Windows 中，根据 Python 的安装方式，可能会看到下面这条命令。

```powershell
py --version
```

其中一个能运行，并不表示另外几个一定都能运行。重要的是确认在我的环境里，哪个命令会真正运行 Python 解释器。

若未打印版本，应先检查安装状态与命令连接。不同命令也可能打印不同版本，因此需要确定项目使用的 Python。

## Windows 安装途径

Python 官方 Windows 文档说明，与大多数 Unix 系统一样自带系统支持的 Python 安装不同，Windows 并不一定包含这种默认安装。Python 可以从多个分发渠道获得，而如果要使用 CPython 团队提供的发行版，可以使用 Python Install Manager。

安装与执行时检查以下事项。

- Windows 里可能并没有一个可以默认信赖的系统 Python。
- Python 可以通过 python.org 下载页或 Microsoft Store 安装。
- 安装后要确认 `python`、`py` 命令是否能工作。
- 官方文档建议为每个项目创建虚拟环境。

若已安装却找不到命令，应检查安装路径、执行别名与 PATH 设置。上述官方 Windows 文档的 Troubleshooting 列出了不同安装方式的检查项目。

## macOS 安装途径

Python 官方 macOS 文档说明，在 macOS 中获取和安装 Python 有多种方式，除了 python.org 提供的安装包，还可能存在其他发行版。当前受支持的 Python 版本，会在 python.org 上提供 macOS 安装包。

安装与执行时检查以下事项。

- macOS 中可能存在被系统工具使用的 Python 相关组件，因此不要随意修改系统区域。
- 学习用 Python 应使用 python.org 安装包或其他广为人知的发行方式。
- 在终端中，通常会先确认 `python3 --version`。
- 即使安装之后，项目实践也最好通过虚拟环境隔离。

macOS 文档说明，从终端里运行脚本和从 Finder 中运行脚本，方式可能不同。在终端中一边确认当前文件夹一边运行，会更透明。

## Linux 发行版中的 Python

Python 官方 Unix 平台文档说明，Python 在大多数 Linux 发行版中已经预装；即使没有，也通常会作为软件包提供。

安装与执行时检查以下事项。

- 在 Linux 中，`python3 --version` 可能已经能工作。
- Python 往往通过发行版的软件包管理器来管理。
- 系统 Python 可能被操作系统工具使用，因此不要随意删除或改动。
- 项目实践最好创建虚拟环境并加以隔离。

在 Linux 资料里，你可能会看到 `sudo apt install python3` 这类命令。但不同发行版的软件包管理器和包名可能不同。因此，Linux 安装命令要以自己发行版的官方文档为准来确认。

## 解释器、虚拟环境与包

Python 安装与创建虚拟环境并不是同一件事。

| 区分 | 做的是什么 | 示例 |
| --- | --- | --- |
| Python 安装 | 在电脑上准备 Python 解释器 | python.org 安装、操作系统包安装 |
| 创建虚拟环境 | 为某个特定项目创建 Python 执行空间 | `python -m venv .venv` |
| 安装包 | 在那个环境里准备外部包 | `python -m pip install numpy` |

Python 官方 `venv` 文档说明，激活虚拟环境后，会通过把对应路径放到前面来让该环境里的 Python 解释器运行。文档还提醒：虚拟环境应该能够在需要时重新创建，并且应该能借助 `requirements.txt` 这类记录重新安装包。

按以下顺序准备项目环境。

1. 安装 Python。
2. 移动到项目文件夹。
3. 创建虚拟环境。
4. 激活虚拟环境，或直接指定该环境的 Python 路径。
5. 安装所需包。
6. 运行 Python 代码。

## 安装与执行环境检查

当 Python 安装过程出问题时，不要马上就重装。先确认下面这些内容。

- 现在打开的是哪个终端？
- 当前工作文件夹在哪里？
- `python --version` 能运行吗？
- `python3 --version` 能运行吗？
- 如果是 Windows，`py --version` 能运行吗？
- 是否安装了多个 Python 版本？
- 当前是否打开了虚拟环境？
- 安装包所用的 Python 和运行代码所用的 Python 是不是同一个？

下面这些情况尤其常见。

- 你把包装到了系统 Python 中，却用虚拟环境里的 Python 在运行。
- 你把包装到了虚拟环境里，却在关掉虚拟环境后运行。
- 你误以为在 Colab 里装过的包，在本地 PC 上也已经装好了。
- 在 Windows 中 `python` 不工作，但 `py` 能工作。
- 在 macOS/Linux 中，`python` 不存在或指向 Python 2，而 `python3` 才真正指向 Python 3。

在看错误信息时，需要养成把“Python 代码错误”和“执行环境错误”分开看的习惯。

## 少一个命令就要重新安装吗

假设 Linux 终端显示以下结果。版本号仅用于说明输出形式。

```text
$ python --version
bash: python: command not found
$ python3 --version
Python 3.12.3
```

此环境没有名为 `python` 的命令，但有通过 `python3` 运行的解释器。重新安装前，可以先用 `python3 example.py` 执行脚本，或用 `python3 -m venv .venv` 创建项目环境。

反过来，如果相关 Python 命令都不可用，又需要本地执行，则按操作系统的安装流程进行。区分一个命令失败与解释器本身缺失，可以减少不必要的重装。

## 检查清单

- 能说明 Colab 与本地 Python 安装的角色差异。
- 能判断什么时候需要本地安装。
- 能说明 `python --version`、`python3 --version`、`py --version` 的目的。
- 能说明 Windows、macOS、Linux 中的 Python 安装方式可能看起来不同。
- 能区分 Python 安装、创建虚拟环境、安装包。
- 能说明安装出错时，应该先检查执行环境而不是代码。
- 能检查 `我的终端里 Python 由哪个命令运行`、`那个命令指向哪个版本的 Python`、`是否已经准备好创建项目专用虚拟环境`、`安装包的环境和运行代码的环境是否相同`。

## 来源与参考资料

- Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认按平台设置 Python 环境、调用解释器与安装相关文档结构。
- Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }, Python.org，确认日期：2026-07-20。用于确认最新 Python 下载入口与按操作系统区分的下载入口。
- Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认 Windows 中 Python 安装与运行有单独的官方说明。
- Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认 macOS 中 python.org 发行版和安装后包使用说明。
- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认 Linux/Unix 系统中安装路径会因操作系统而异，例如发行版包或源码构建。
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认项目专用虚拟环境可能是不同于安装 Python 本身的单独步骤。

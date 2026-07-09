# P2-7.7 补充学习：什么时候需要安装 Python

> Section ID: `P2-7.7`
> Version: `v2026.07.07`

在 P2-7.6 中，我们看过了如何在 Windows、macOS、Linux 中打开终端并确认当前位置。现在还剩下这个问题。

我的电脑里一定要安装 Python 吗？

这里会说明 `什么时候需要安装 Python`、`安装后首先要确认的命令`、以及 `安装与虚拟环境的区别`。

这个问题是在看过执行环境的大图景之后自然接上的。这里整理的是：安装现在是否需要、还是以后再需要的判断标准。

并不是一开始就一定要安装。这个 Part 前面的实践，也可以通过 Colab 这样的浏览器执行环境来跟进。但从某个时点开始，就会出现需要在本地 PC（local PC）上安装 Python、创建虚拟环境（virtual environment）、并直接管理包（package）的理由。

这里不重点放在逐个点击安装按钮，而是集中在判断“什么时候需要安装”“安装之后要确认什么”“安装与虚拟环境该怎样区分”。不同操作系统下的画面会不断变化，Python 的分发方式也会随着时间变化。

| 术语 | 本节先要抓住的意思 |
| --- | --- |
| 本地安装（local installation） | 让 Python 解释器能够在我的电脑里直接运行的准备工作。 |
| Colab 起步阶段 | 不安装也能先在浏览器中建立实践感觉的阶段。 |
| `python --version` / `python3 --version` / `py --version` | 安装后第一批要确认的命令，用来检查我的环境里究竟哪个 Python 命令真的连上了。 |
| 安装与虚拟环境的差异 | 安装是准备 Python 本身，而虚拟环境是在已安装的 Python 之上按项目划分空间。 |
| 官方安装文档 | 用来确认不同操作系统下最新安装方式和注意事项的基准资料。 |

## 官方安装手册链接

链接收集日期：2026-06-24

安装画面和推荐方式会随着时间变化。真正进行安装时，不要只看本节说明，也要一起查看下面的官方文档。

- 整体安装与使用指南：Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }.
- 下载页面：Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }.
- Windows 中的安装与运行：Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }.
- macOS 中的安装与运行：Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }.
- Linux/Unix 平台中的使用：Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }.
- 虚拟环境：Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }.

## 本补充学习的范围

这里处理的是 Python 安装的必要性与确认标准。不处理逐个跟着点击的操作系统详细安装步骤，安装后的环境不一致检查会在 P2-7.9 中再次回收。

这里回答下面这些问题。

- 什么时候只用 Colab 就够了？
- 什么时候需要在本地 PC 上安装 Python？
- 为什么 Windows、macOS、Linux 中的安装方式看起来不同？
- 安装后应该用哪些命令来确认？
- Python 安装与创建虚拟环境有什么不同？
- 当安装过程出问题时，首先要确认什么？

这里不会长篇跟随不同操作系统的安装画面。也不会深入处理特定版本安装、PATH 问题修复、Windows Store 与 python.org 安装方式比较、Homebrew、pyenv、conda、Docker、WSL 设置。PATH 以及安装后常见卡点的检查顺序，会在 P2-7.9 补充学习中重新整理；详细的安装方式比较，则会在真正搭建项目环境时再次处理。

## 本补充学习的目标

- 能说明 Colab 与本地 Python 安装的角色差异。
- 能判断什么时候需要本地安装。
- 能说明安装后应该通过 `python --version`、`python3 --version`、`py --version` 来确认。
- 能说明 Python 安装与创建虚拟环境不是同一件事。
- 能说明不同操作系统下的安装指引，需要在写作时点重新确认官方文档。

## 三个标准

| 标准 | 为什么重要 | 本节所需的理解程度 |
| --- | --- | --- |
| 一开始并不一定非要本地安装 | 因为小型实践可以只靠 Colab 开始 | 区分 Colab 与本地安装的角色差异 |
| 本地安装是在自己的电脑上建立运行 Python 解释器的基础 | 如果把安装、虚拟环境、包准备看成一整团，判断就会变模糊 | 能说明安装到底是在准备什么 |
| 安装之后第一步要确认的是版本和执行命令 | 安装成功与命令连接成功不是同一回事 | 能说明 `python --version` 这类检查的目的 |

## 可以从 Colab 开始的阶段

在前期学习里，很多时候 Colab 就够了。

- 运行简单的 Python 代码
- 确认 NumPy 数组计算
- 处理小型表格数据
- 快速画图
- 按单元格跟着书里的示例代码做

由于 Colab 在浏览器中运行，它可以把 Python 安装问题往后推。这是一个很大的优点，因为在遇到安装、PATH、操作系统权限、终端差异之前，你可以先建立“代码能跑起来”的感觉。

但 Colab 不是你的电脑。runtime 是由外部服务提供的，会话可能被初始化，也很难保证文件和包状态会一直保持。因此，当学习进入下一阶段时，对本地安装的需求就会变大。

## 本地安装变得必要的时点

需要在本地 PC 上安装 Python 的时点，不是“开始学 Python 的第一天”，而是当你必须自己管理执行环境的时候。

例如，下面这些情况里，本地安装就可能变得必要。

- 需要在自己的电脑里直接运行 `.py` 文件。
- 需要在项目文件夹中一起管理多个文件。
- 需要在本地文件夹里读写数据文件。
- 需要运行通过 Git 得到的示例项目。
- 需要创建虚拟环境，并按项目隔离包。
- 想减少对网络连接或 Colab runtime 状态的依赖。
- 需要把编辑器、终端、测试工具、文档构建工具一起使用。

相反，在下面这些阶段，Colab 可能仍然足够。

- 只是确认一两行计算。
- 运行小型代码单元。
- 重点是理解概念，而不是安装。
- 不需要保存结果或管理项目结构。

所以，这里先通过 Colab 建立运行感觉，之后在本地 PC 上进入项目级实践时，再正式考虑 Python 安装。

## 安装是在准备 Python 解释器

Python 安装，是在我的电脑上准备 Python 解释器（Python interpreter）的过程。Python 官方文档分别介绍了不同平台上的 Python 环境设置、解释器运行方式，以及便于工作的相关信息。

通常说“已经安装了”，意味着下面这些事变得可行。

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

## 安装后先确认版本

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

先留下下面这些问题。

- `python` 能运行吗？
- `python3` 能运行吗？
- 如果是 Windows，`py` 能运行吗？
- 输出的版本和书里的示例差别是否过大？
- 打开虚拟环境之后，同一个命令是否仍然指向同一个 Python？

如果这里卡住了，在修改 Python 代码之前，应该先怀疑安装或命令连接的问题。

## 在 Windows 中，可能会遇到 Python Install Manager

Python 官方 Windows 文档说明，与大多数 Unix 系统一样自带系统支持的 Python 安装不同，Windows 并不一定包含这种默认安装。Python 可以从多个分发渠道获得，而如果要使用 CPython 团队提供的发行版，可以使用 Python Install Manager。

这里记住下面这些标准。

- Windows 里可能并没有一个可以默认信赖的系统 Python。
- Python 可以通过 python.org 下载页或 Microsoft Store 安装。
- 安装后要确认 `python`、`py` 命令是否能工作。
- 官方文档建议为每个项目创建虚拟环境。

在 Windows 里经常出现的问题是：“明明安装了，但终端里找不到命令。” 这时候问题可能不是 Python 代码，而是安装路径或 PATH 设置。这里不展开到手动修改 PATH 的步骤。如何理解 PATH 和环境变量（environment variable），会在 P2-7.8 补充学习中再次处理；安装后的检查顺序，则会在 P2-7.9 补充学习中重新整理。这里先只抓到：去看官方文档里的 Troubleshooting，或者重新检查安装方式。

## 在 macOS 中，要区分 python.org 安装与其他发行版

Python 官方 macOS 文档说明，在 macOS 中获取和安装 Python 有多种方式，除了 python.org 提供的安装包，还可能存在其他发行版。当前受支持的 Python 版本，会在 python.org 上提供 macOS 安装包。

这里记住下面这些标准。

- macOS 中可能存在被系统工具使用的 Python 相关组件，因此不要随意修改系统区域。
- 学习用 Python 应使用 python.org 安装包或其他广为人知的发行方式。
- 在终端中，通常会先确认 `python3 --version`。
- 即使安装之后，项目实践也最好通过虚拟环境隔离。

macOS 文档说明，从终端里运行脚本和从 Finder 中运行脚本，方式可能不同。在终端中一边确认当前文件夹一边运行，会更透明。

## 在 Linux 中，可能已经安装好了

Python 官方 Unix 平台文档说明，Python 在大多数 Linux 发行版中已经预装；即使没有，也通常会作为软件包提供。

这里记住下面这些标准。

- 在 Linux 中，`python3 --version` 可能已经能工作。
- Python 往往通过发行版的软件包管理器来管理。
- 系统 Python 可能被操作系统工具使用，因此不要随意删除或改动。
- 项目实践最好创建虚拟环境并加以隔离。

在 Linux 资料里，你可能会看到 `sudo apt install python3` 这类命令。但不同发行版的软件包管理器和包名可能不同。因此，Linux 安装命令要以自己发行版的官方文档为准来确认。

## Python 安装与创建虚拟环境是不同的事

Python 安装与创建虚拟环境并不是同一件事。

| 区分 | 做的是什么 | 示例 |
| --- | --- | --- |
| Python 安装 | 在电脑上准备 Python 解释器 | python.org 安装、操作系统包安装 |
| 创建虚拟环境 | 为某个特定项目创建 Python 执行空间 | `python -m venv .venv` |
| 安装包 | 在那个环境里准备外部包 | `python -m pip install numpy` |

Python 官方 `venv` 文档说明，激活虚拟环境后，会通过把对应路径放到前面来让该环境里的 Python 解释器运行。文档还提醒：虚拟环境应该能够在需要时重新创建，并且应该能借助 `requirements.txt` 这类记录重新安装包。

这里把流程区分成下面这样。

1. 安装 Python。
2. 移动到项目文件夹。
3. 创建虚拟环境。
4. 激活虚拟环境。
5. 安装所需包。
6. 运行 Python 代码。

这里不要求你记住第 4 步在不同操作系统中的激活命令。激活命令会因 Windows、macOS、Linux 以及 shell 类型不同而看起来不同。现在只先记住这个方向：不要让“安装好的一个 Python 被所有项目直接共用”，而是为每个项目建立独立环境。

## 当安装过程出问题时，先确认什么

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

## 本节要记住的视角

Python 安装不是学习的起点，而是为了直接管理执行环境所做的准备。

你可以从 Colab 开始。但当你需要直接管理项目文件夹、数据文件、虚拟环境、包版本和可复现性时，本地安装就会变得必要。

安装后，先确认下面这些问题。

1. 在我的终端里，Python 是通过哪个命令运行的？
2. 那个命令指向的是哪个版本的 Python？
3. 我是否已经准备好为每个项目创建虚拟环境？
4. 安装包的环境和运行代码的环境是不是同一个？

读完这个补充学习之后，比起“是否已经完成所有安装步骤”，更重要的是“我该回到正文里的哪个问题”。

| 这里解决的问题 | 回去后要接续的正文问题 | 接下来继续读哪里 |
| --- | --- | --- |
| 现在是否需要本地安装 Python，安装后应该先确认什么？ | 为什么执行环境、解释器、虚拟环境、包管理必须分开理解？ | 执行环境的大图景在 P2-7.1，解释器与脚本在 P2-7.3，虚拟环境与包在 P2-7.4 |

这里整理的是 `现在 Colab 是否已经足够？`、`现在是否到了需要本地安装的时候？`、`安装后该用哪个命令确认？` 这些问题。不同操作系统下的安装细节和 PATH 问题，会在真正处理项目环境时再重新连接。

## 用案例来看

### 案例 1. 到什么时候 Colab 还够用，从什么时候开始需要本地安装

假设一位学习者到现在为止都只是在 Colab 里跟着示例做。但现在出现了一个情况：他需要下载一个包含多个 `.py` 文件的项目，并在本地文件夹中运行它。这时人通常会先问：“现在就一定要安装吗？”“不能直接上传到 Colab 吗？”

在前期，Colab 可能确实已经足够。但如果必须保留项目文件夹结构、在本地读取数据文件、分开虚拟环境、并直接管理包版本，那么本地安装 Python 就变得必要了。

本节的作用不是罗列安装按钮，而是让人能够判断 `什么时候需要安装`。也就是说，它给出的是区分 `浏览器 runtime 是否仍然足够` 与 `是否必须在自己的电脑里直接管理执行环境` 的标准。

可确认的结果可以直接通过安装后的命令看到。如果 `python --version`、`python3 --version`、`py --version` 其中之一能够真正运行本地解释器，之后又能继续创建虚拟环境并安装包，那就说明已经准备好从 Colab 转向本地环境了。

## 简短检查

- 能区分 Colab 足够的学习阶段与需要本地安装的阶段。
- 能说明 Python 安装是在电脑中准备 Python 解释器的过程。
- 能说明 `python --version`、`python3 --version`、`py --version` 的目的。
- 能说明 Windows、macOS、Linux 中的 Python 安装方式可能看起来不同。
- 能区分 Python 安装、创建虚拟环境、安装包。
- 能说明当出现安装错误时，应该先检查执行环境，而不是先改代码。

## 什么时候应该先想起这个视角

- 当你无法判断一开始是否一定需要本地安装，因此需要重新区分 Colab 与本地安装的角色时，就想起这个视角。
- 当你不知道安装后应该先确认什么，因此需要重新抓住 `python --version`、`python3 --version`、`py --version` 这类命令的检查顺序时，就想起这个视角。
- 当你把 Python 安装和创建虚拟环境当成一回事，因此需要重新区分准备阶段与项目隔离阶段时，就想起这个视角。

## 来源与参考资料

- Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-06-24。
- Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }, Python.org，确认日期：2026-06-24。
- Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-06-24。
- Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-06-24。
- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-06-24。
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-06-24。

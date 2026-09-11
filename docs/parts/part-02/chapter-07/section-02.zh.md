# P2-7.2 终端(terminal)、shell、工作目录(working directory)

> Section ID: `P2-7.2`
> Version: `v2026.09.08`

运行 `python example.py` 时，shell 负责解释命令，并按基准文件夹查找文件。即使文件存在，从其他文件夹执行相同命令也可能找不到它。

| 术语 | 含义 |
| --- | --- |
| 终端(terminal) | 输入命令并查看结果的窗口或应用。 |
| shell | 在终端里读取、解释并执行命令的程序。 |
| 工作文件夹(working directory) | 当前命令拿来作为基准的文件夹。 |
| 路径(path) | 指向文件或文件夹位置的字符串。 |
| 命令(command) | 向 shell 发出的“现在请执行这件事”的语句。 |

## 命令解释与基准位置

| 标准 | 为什么重要 |
| --- | --- |
| 终端是画面，而 shell 是在里面解释命令的程序 | 只有把输入位置和解释主体分开，混乱才会减少。 |
| 工作文件夹决定命令的基准位置 | 同一个命令会因为当前位置不同而指向不同文件。 |
| 最先要检查的是当前位置和文件列表 | 很多失败不是语法问题，而是位置问题。 |

## 终端与 shell 的由来

terminal 和 shell 并不是最近才出现的 app 名称。它们都保留着一个时代的痕迹：当时很多人通过纯文本来使用计算机。

早期的 `terminal` 并不是像今天这样装在笔记本里的 app，而是连接到中央计算机的输入/输出装置。Text-Terminal-HOWTO 说明，真正的文本终端看起来像显示器和键盘，但显示的不是图形，而是基于文本的 `command-line interface`，并且在 1970 年代后期和 1980 年代广泛用于连接大型主机。后来真正的硬件终端减少了，而今天的终端 app 更接近一种 `terminal emulator`，也就是用软件去模拟当年的工作方式。

`shell` 也是很老的概念。GNU Bash 手册说明，Bash 是 GNU 操作系统的 shell，也就是 `command language interpreter`。它也说明，Unix shell 既是命令解释器，也是编程语言。

过去的终端设备与现代应用之间的联系如下。

- 过去：人们通过单独的终端设备向中央计算机输入命令。
- 现在：终端 app 用软件提供这种基于文本的工作方式。
- shell：解释并执行用户输入命令的程序。

这也就是为什么即使到了今天的开发环境里，`打开终端`、`在 shell 里运行`、`在命令行输入` 这些说法还会保留下来。它们都连着同一条流向：`不是点图形按钮，而是用文本输入命令并执行。`

## 终端应用与 shell

`终端(terminal)` 是输入命令并查看结果的画面。macOS 的 Terminal、Windows Terminal、VS Code 的 Terminal 面板，都属于这里。

`shell` 是读取、解释并执行用户输入命令的程序。用户通过 shell，可以运行和组合操作系统提供的各种工具。

这里按下面这种方式区分。

- terminal：输入命令和查看结果的窗口
- shell：在 terminal 内部读取并执行命令的程序
- command：我们让 shell 去做的事

所以，即使都叫“打开了终端”，里面也有很多不同情况。

| 环境 | 终端 app | shell 例子 |
| --- | --- | --- |
| macOS | Terminal, iTerm2, VS Code Terminal | zsh, bash |
| Windows | Windows Terminal, PowerShell, VS Code Terminal | PowerShell, Command Prompt, WSL shell |
| Linux | GNOME Terminal, Konsole, VS Code Terminal | bash, zsh |

## 当前位置、目录切换与文件列表

输入到终端里的句子，并不是自然语言句子。它是 shell 按固定规则读取的执行请求。

例如，下面是检查当前位置的命令。

```bash
pwd
```

下面这个命令会移动到某个文件夹。

```bash
cd docs
```

下面这个命令会查看当前文件夹的文件列表。

```bash
ls
```

在 Windows PowerShell 中，可用 `Get-Location` 检查当前位置，用 `Set-Location` 切换位置，也常见 `pwd`、`cd` 等别名(alias)。Microsoft 文档说明，这两个命令分别显示和设置当前工作位置。

同一个命令，只要当前文件夹不同，执行目标就可能完全不同。

## 工作文件夹与文件执行

`工作文件夹(working directory)` 是当前命令拿来作为基准的文件夹。它也常被叫作 `current working directory`（CWD）。

例如，假设我们在终端中执行下面这个命令。

```bash
python example.py
```

这个命令通常可以读成：`在当前工作文件夹里找到叫 example.py 的文件，然后用 Python 去运行它。` 但如果当前工作文件夹里根本没有 `example.py`，命令就会失败。

它一定是因为文件不存在吗？未必。

很常见的一种情况是：文件并不是真的没有，而是我自己站错了文件夹。

很多常见错误，并不是从代码语法开始，而是从位置问题开始。文件可能在 `downloads/` 里，但终端当前却在 `home/`；项目文件夹可能在 `project-name/` 里，但终端却停在它的上一级。

所以，在开始练习前，我们要先检查当前位置。

```bash
pwd
```

然后再移动到需要的文件夹。

```bash
cd /Users/someone/ws/project-name
```

在 Windows PowerShell 里，可以这样检查。

```powershell
Get-Location
```

也可以这样移动。

```powershell
Set-Location C:\Users\someone\ws\project-name
```

即使命令名字不同，核心其实一样。

所以要先问下面两个问题。

- 我现在到底在哪个文件夹里？
- 这个命令是以哪个文件夹为基准来执行的？

## 相对路径与绝对路径

`路径(path)` 是表示文件或文件夹位置的字符串。这里区分 `相对路径(relative path)` 与 `绝对路径(absolute path)`。

这两个词可以这样区分。

- 相对路径：以当前工作文件夹为基准去寻找的位置。
- 绝对路径：从文件系统起点一路完整写出来的位置。

当前工作文件夹为 `/Users/someone/ws/project-name` 时，相对路径 `docs/parts` 指向它下面的 `docs/parts` 文件夹。

相反，绝对路径会把起点到终点都完整写出来。

```text
/Users/someone/ws/project-name/docs/parts
```

相对路径短而方便。但只要当前工作文件夹一变，它的意义就会跟着变。

`docs/parts` 在 `project-name` 文件夹里执行时有意义；但如果换到别的项目文件夹去执行，它就会指向完全不同的位置，甚至变成不存在的路径。

## 检查文件列表

当命令失败时，不要一上来就改代码，而是先检查当前文件夹和文件列表。

在 Unix 系 shell 中，通常会用下面这些命令。

```bash
pwd
ls
```

在 Windows PowerShell 中，则可以使用下面这些命令。

```powershell
Get-Location
Get-ChildItem
```

在 PowerShell 里，`ls` 往往会作为 `Get-ChildItem` 的别名工作。但即使如此，还是值得至少看一眼本来的命令名。以后查官方文档时，你可以用正式名字来检索。

## Colab 运行时的 shell 命令

Colab 也能执行命令。但如果把它理解成和本地 PC 终端完全一样，就会产生误解。

如果在 Colab 代码单元里像下面这样加上 `!`，就能执行 shell 命令。

在连接到托管运行时的 Colab 代码单元执行 `!pwd`，会打印该运行时的当前文件夹路径。

```python
# 这条 shell 命令是在 Colab 代码单元中确认当前工作文件夹。
!pwd
```

这时，命令不是在我的笔记本电脑上执行，而是在 Colab runtime 中执行。所以文件位置、安装好的包、保存下来的文件，都可能和本地 PC 不一样。

整理起来就是下面这样。

- 我自己 PC 的终端：基于我电脑里的文件和环境执行。
- Colab 代码单元里的 `!` 命令：基于 Colab runtime 的文件和环境执行。

`!` 是在基于 IPython 的笔记本中执行 shell 命令的标记，不是普通 Python 文件的语法。

## 常见终端错误

终端错误看起来很复杂，但通常可以先分成几类。

| 情况 | 先检查的问题 |
| --- | --- |
| 提示找不到文件 | 当前工作文件夹对吗？ |
| 提示找不到命令 | 这个程序装了吗，而且 PATH 能找到它吗？ |
| Python 文件执行不了 | 有没有把终端命令和 Python 代码混着用？ |
| 在 Colab 能运行，本地不行 | 本地环境里装了同样的包吗？ |
| 在本地能运行，Colab 不行 | 文件有没有上传到 Colab runtime 里？ |

## 文件存在却无法执行

假设 `workspace` 文件夹中有 `project` 文件夹，里面有 `example.py`。

```text
workspace/
└── project/
    └── example.py
```

当前工作文件夹为 `workspace` 时，`python example.py` 会查找 `workspace/example.py`。该位置没有文件，因此无法执行。用 `ls project` 确认文件后，可采用以下两种方式之一。

```bash
# 切换到 project 文件夹后执行。
cd project
python example.py
```

也可以停留在 `workspace`，指定文件的相对路径。

```bash
python project/example.py
```

两者执行的是同一个脚本，但当前工作文件夹不同。如果脚本以 `data.csv` 这样的相对路径读取数据，第一种方式查找 `project/data.csv`，第二种方式查找 `workspace/data.csv`。需要区分寻找脚本文件与脚本内部寻找数据的问题。

## 检查清单

- 能把终端(terminal)解释成输入命令和查看结果的画面。
- 能把 shell 解释成解释并执行命令的程序。
- 能说明终端 app 是用软件继承了过去基于文本的终端装置角色。
- 能把工作文件夹(working directory)解释成当前命令的基准位置。
- 能用入门层次说明相对路径(relative path)和绝对路径(absolute path)的区别。
- 能说明为什么需要 `pwd`、`cd`、`ls`。
- 知道在 PowerShell 中还存在 `Get-Location`、`Set-Location`、`Get-ChildItem` 这些正式命令名。
- 能说明 Colab 代码单元里的 `!` 命令是在 Colab runtime 中执行，而不是在本地 PC 上执行。
- 能先检查 `我在用什么 shell`、`我现在在哪个文件夹`、`这个命令正在找什么文件或程序`。

## 来源与参考资料

- David S. Lawyer, [Text-Terminal-HOWTO](https://tldp.org/HOWTO/Text-Terminal-HOWTO.html){: target="_blank" rel="noopener noreferrer" }, The Linux Documentation Project, 确认日期: 2026-07-20。作为说明早期文本终端与现代命令行界面之间关系的历史辅助依据。
- Free Software Foundation, [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html){: target="_blank" rel="noopener noreferrer" }, GNU Bash 5.3 manual, 确认日期: 2026-07-20。用于确认 shell 既是命令解释器也是编程语言，并支撑 Bash 命令处理语境。
- Microsoft, [Get-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 确认日期: 2026-07-20。用于确认 PowerShell 中查看当前工作位置的正式命令及其 `pwd` 别名语境。
- Microsoft, [Set-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 确认日期: 2026-07-20。用于确认 PowerShell 中改变当前工作位置的正式命令及其 `cd` 别名语境。
- Python Software Foundation, [os.getcwd](https://docs.python.org/3/library/os.html#os.getcwd){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-07-20。用于支撑 Python 代码可以把当前工作目录读取为字符串这一说明。

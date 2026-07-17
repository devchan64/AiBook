# P2-7.2 终端(terminal)、shell 与工作文件夹(working directory)

> Section ID: `P2-7.2`
> Version: `v2026.07.17`

在 P2-7.1 中，我们先看了代码运行的位置。现在来看：在本地 PC 上输入命令时，最先遇到的那个画面到底是什么。

刚开始学编程时，下面这些句子会反复出现。

例如，入门文档里经常会写出这样的句子。

- 打开终端并执行。
- 移动到项目文件夹。
- 输入下面的命令。

这些句子虽然很短，但里面一次塞进了很多概念。如果分不清 `终端(terminal)`、`shell`、`命令(command)`、`工作文件夹(working directory)`，就会不断遇到这样的场景：`我明明输入得一模一样，为什么还是不行？`

这里解释的是 `终端(terminal)`、`shell`、`工作文件夹(working directory)` 之间的基本区分。即使后面几节继续接着讲 Python 执行、虚拟环境激活、包安装命令，命令到底输入到哪里、以及它是以什么位置为基准被解释的，都要回连到这里的说明上。

这里并不是要把各操作系统里的终端使用法全部学完，而是把重点放在：建立在本地 PC 上阅读和执行命令的最小语言。如果先把终端、shell、工作文件夹这几个角色区分开，后面再看到 Python 文件执行、虚拟环境、包安装时，就能先把问题分成“代码错误”还是“位置错误”。

| 现在这一节先抓什么 | 紧接着下一步会问什么 | 以后会再次用在哪里 |
| --- | --- | --- |
| 终端、shell、工作文件夹的角色区分 | 在 P2-7.3 中会继续看 Python 文件到底怎样被执行。 | 以后在所有本地练习里，区分位置问题和代码问题时都会再次使用。 |
| 为什么 `pwd`、`cd`、`ls` 要先出现 | 在 P2-7.4 中会继续接到虚拟环境和包安装命令。 | 会在读取数据文件、运行脚本、移动到项目根目录的语境里反复出现。 |
| Colab shell 和本地终端并不是同一件事 | 会把操作系统差异和高级 shell 语法延后到 P2-7.6 与 P2-7.8 补充学习。 | 会成为 Part 3 以后阅读练习环境说明时的基础。 |

| 术语 | 这一节先抓住的意思 |
| --- | --- |
| 终端(terminal) | 输入命令并查看结果的窗口或应用。 |
| shell | 在终端里读取、解释并执行命令的程序。 |
| 工作文件夹(working directory) | 当前命令拿来作为基准的文件夹。 |
| 路径(path) | 指向文件或文件夹位置的字符串。 |
| 命令(command) | 向 shell 发出的“现在请执行这件事”的语句。 |

## 本节范围

这里回答下面这些问题。

- 什么是终端？
- 什么是 shell？
- 为什么这些老词到现在还在用？
- 命令到底是在什么地方被解释？
- 为什么工作文件夹很重要？

Python 文件执行会在 P2-7.3 再讲，虚拟环境和包安装会在 P2-7.4 再讲。这里先建立那之前需要的最小语言。

至于在 Windows、macOS、Linux 上到底怎样打开终端、第一步该输入什么命令，会作为补充学习放在 P2-7.6。这里先抓住共通概念，再处理按操作系统区分的步骤。

| 如果现在的症状是这样 | 先去哪里 | 否则就在这一节先抓住什么 |
| --- | --- | --- |
| 我一开始就卡在 Windows、macOS、Linux 上到底从哪里打开终端 | 补充学习 P2-7.6 | 先抓住共通概念：终端是输入命令的位置，而 shell 负责解释命令 |
| 我的注意力先被 `|`、`>`、环境变量这样的符号吸走 | 补充学习 P2-7.8 | 现在先只留下：为什么工作文件夹和命令输入位置重要 |
| 我只是有点不明白为什么要学 `pwd`、`cd`、`ls` | 继续读这一节 | 先确认当前的位置和文件基准会影响命令的解释 |

## 本节目标

- 能把 `终端(terminal)` 解释成输入命令和查看结果的画面。
- 能把 `shell` 解释成解释并执行命令的程序。
- 能说明 terminal 与 shell 这些词保留了较早时期的计算机使用方式。
- 能把 `工作文件夹(working directory)` 解释成当前命令拿来作为基准的文件夹。
- 能说明为什么 `pwd`、`cd`、`ls` 或 `dir` 这样的基础命令会先出现。
- 当命令失败时，能先把问题分成代码问题还是位置问题。

## 三个判断标准

| 标准 | 为什么重要 | 这里需要的理解层次 |
| --- | --- | --- |
| 终端是画面，而 shell 是在里面解释命令的程序 | 只有把输入位置和解释主体分开，混乱才会减少。 | 只要能把 terminal 和 shell 说成两个不同角色就足够。 |
| 工作文件夹决定命令的基准位置 | 同一个命令会因为当前位置不同而指向不同文件。 | 抓住把位置错误和代码错误分开的感觉。 |
| 最先要检查的是当前位置和文件列表 | 很多失败不是语法问题，而是位置问题。 | 能说明 `pwd`、`cd`、`ls` 或对应命令的目的。 |

## 为什么 terminal 和 shell 这些词还在用

terminal 和 shell 并不是最近才出现的 app 名称。它们都保留着一个时代的痕迹：当时很多人通过纯文本来使用计算机。

早期的 `terminal` 并不是像今天这样装在笔记本里的 app，而是连接到中央计算机的输入/输出装置。Text-Terminal-HOWTO 说明，真正的文本终端看起来像显示器和键盘，但显示的不是图形，而是基于文本的 `command-line interface`，并且在 1970 年代后期和 1980 年代广泛用于连接大型主机。后来真正的硬件终端减少了，而今天的终端 app 更接近一种 `terminal emulator`，也就是用软件去模拟当年的工作方式。

`shell` 也是很老的概念。GNU Bash 手册说明，Bash 是 GNU 操作系统的 shell，也就是 `command language interpreter`。它也说明，Unix shell 既是命令解释器，也是编程语言。

你不需要背完整段历史。只要记住下面这条流向，就能解释 terminal 和 shell 为什么会一直留到今天。

- 过去：人们通过单独的终端设备向中央计算机输入命令。
- 现在：终端 app 用软件提供这种基于文本的工作方式。
- shell：解释并执行用户输入命令的程序。

这也就是为什么即使到了今天的开发环境里，`打开终端`、`在 shell 里运行`、`在命令行输入` 这些说法还会保留下来。它们都连着同一条流向：`不是点图形按钮，而是用文本输入命令并执行。`

## 终端是画面，shell 是解释命令的程序

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

这里不会深入比较按操作系统区分的 shell 差异。但会尽量标明示例命令是按什么基准来的。

## 命令不是普通句子，而是执行请求

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

在 Windows PowerShell 里，可以用 `Get-Location` 来检查当前位置，也可以用 `Set-Location` 来移动。Microsoft 文档说明，`Get-Location` 用来显示当前位置，而 `Set-Location` 用来设置当前工作位置。

你不需要背下所有命令。真正重要的是：`命令到底在什么地方执行。`

同一个命令，只要当前文件夹不同，执行目标就可能完全不同。

## 工作文件夹是命令的基准位置

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

## 区分相对路径和绝对路径

`路径(path)` 是表示文件或文件夹位置的字符串。这里区分 `相对路径(relative path)` 与 `绝对路径(absolute path)`。

这两个词可以这样区分。

- 相对路径：以当前工作文件夹为基准去寻找的位置。
- 绝对路径：从文件系统起点一路完整写出来的位置。

例如，如果当前工作文件夹是 `/Users/someone/ws/project-name`，那么下面这个相对路径就可能指向文档文件夹。

例如，`docs/parts` 就是相对路径。

相反，绝对路径会把起点到终点都完整写出来。

```text
/Users/someone/ws/project-name/docs/parts
```

相对路径短而方便。但只要当前工作文件夹一变，它的意义就会跟着变。

`docs/parts` 在 `project-name` 文件夹里执行时有意义；但如果换到别的项目文件夹去执行，它就会指向完全不同的位置，甚至变成不存在的路径。

## 养成先看文件列表的习惯很重要

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

这里会先展示以 macOS/Linux 为基准的命令；如果 Windows 需要不同命令，就另外标出来。

## Colab 里没有终端吗

Colab 也能执行命令。但如果把它理解成和本地 PC 终端完全一样，就会产生误解。

如果在 Colab 代码单元里像下面这样加上 `!`，就能执行 shell 命令。

问题场景：确认即使在 Colab 代码单元里，也能执行用来检查当前工作位置的 shell 命令。
输入(input)：在代码单元中执行的 `!pwd` 命令。
期待输出(output)：打印出以 Colab runtime 为基准的当前文件夹路径。
要确认的概念：Colab 里的 `!` 命令并不是调用我自己电脑的终端，而是在 Colab runtime 里执行 shell 命令。

```python
!pwd
```

这时，命令不是在我的笔记本电脑上执行，而是在 Colab runtime 中执行。所以文件位置、安装好的包、保存下来的文件，都可能和本地 PC 不一样。

整理起来就是下面这样。

- 我自己 PC 的终端：基于我电脑里的文件和环境执行。
- Colab 代码单元里的 `!` 命令：基于 Colab runtime 的文件和环境执行。

这也是为什么我们在 P2-3.5 里区分 `!pip install numpy` 和 `%pip install numpy`。即使代码单元里可以执行 shell 命令，也不表示它们就是 Python 语法。

## 终端里常见的错误

终端错误看起来很复杂，但通常可以先分成几类。

| 情况 | 先检查的问题 |
| --- | --- |
| 提示找不到文件 | 当前工作文件夹对吗？ |
| 提示找不到命令 | 这个程序装了吗，而且 PATH 能找到它吗？ |
| Python 文件执行不了 | 有没有把终端命令和 Python 代码混着用？ |
| 在 Colab 能运行，本地不行 | 本地环境里装了同样的包吗？ |
| 在本地能运行，Colab 不行 | 文件有没有上传到 Colab runtime 里？ |

这一节不会解决所有错误。但会建立一种习惯：看错误时，先把它分成 `代码本身的错误` 和 `命令执行位置的错误`。

## 用案例来看

### 案例 1. 明明文件存在，为什么 `python example.py` 还是失败

假设一个学习者下载了 `example.py` 文件，准备执行。这个文件明明就放在桌面上的项目文件夹里，但在终端里输入 `python example.py` 却报错说找不到文件。

人们常常会先想到：`文件是不是坏了？`、`Python 是不是有问题？` 但这时更常见的原因是，当前工作文件夹并不是项目文件夹。同一个命令，只要从不同文件夹执行，就会去找完全不同的位置。

如果把这一节的核心词 `终端`、`shell`、`工作文件夹`、`相对路径` 区分开，解释就会改变。问题可能不是代码本身，而是 `命令到底以哪个位置为基准执行`，所以 `pwd`、`ls`、`cd` 这些命令才会先出现。

可确认的结果会在打印当前位置时立刻出现。如果 `pwd` 的结果并不是项目文件夹，那么同一个 `python example.py` 命令失败，就应该被解释成位置问题，而不是代码问题。

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

- David S. Lawyer, [Text-Terminal-HOWTO](https://tldp.org/HOWTO/Text-Terminal-HOWTO.html){: target="_blank" rel="noopener noreferrer" }, The Linux Documentation Project, 确认日期: 2026-06-24.
- Free Software Foundation, [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html){: target="_blank" rel="noopener noreferrer" }, GNU Bash 5.3 manual, 确认日期: 2026-06-24.
- Microsoft, [Get-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 确认日期: 2026-06-24.
- Microsoft, [Set-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, 确认日期: 2026-06-24.
- Python Software Foundation, [os.getcwd](https://docs.python.org/3/library/os.html#os.getcwd){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-06-24.

# P2-7.6 补充学习：Windows、macOS、Linux 终端使用方法

> Section ID: `P2-7.6`
> Version: `v2026.07.19`

在 P2-7.2 中，我们看过终端（terminal）、shell、工作文件夹（working directory）的概念。这里要处理的是，如何在实际操作系统中确认这些概念。

这里补充说明 `按操作系统进入终端的步骤` 和 `确认基本位置的命令`。

这个补充学习练习的是：“命令要输入在哪里，当前位置怎么确认，如何移动到实践文件夹”。Python 安装会在 P2-7.7 中单独处理。这里集中看在不同操作系统的终端里，如何完成同一目的的检查。

这个补充学习整理了在 Windows、macOS、Linux 中打开终端、确认当前位置、并移动到实践文件夹的步骤。执行环境这一概念本身会在 P2-7.1 和 P2-7.2 中处理。

| 术语 | 本节先要抓住的意思 |
| --- | --- |
| Windows Terminal / PowerShell | 在 Windows 中开始输入命令时经常遇到的终端应用和 shell 组合。 |
| Terminal / zsh | 在 macOS 中经常遇到的默认终端应用和 shell 组合。 |
| `pwd`, `ls`, `cd` | 用来确认当前位置、查看列表、移动文件夹的基本命令。 |
| `Get-Location`, `Get-ChildItem`, `Set-Location` | 在 PowerShell 中完成相同目的的命令。 |
| 路径（path）差异 | 像 Windows 的 `C:\\...` 与 macOS/Linux 的 `/...` 这样的操作系统路径表示差异。 |

## 本补充学习的范围

这个补充学习处理的是：在 Windows、macOS、Linux 中第一次打开终端，并在实践前完成最低限度确认的步骤。终端与 shell 的概念定义会在 P2-7.2 再次出现，判断是否需要安装 Python 会在 P2-7.7 再次处理，shell 符号与环境变量会在 P2-7.8 再次处理，本地环境检查顺序会在 P2-7.9 再次整理。

这里回答下面这些问题。

- 在 Windows 中可以打开什么终端？
- 在 macOS 中应该怎样理解 Terminal？
- 为什么在 Linux 中终端使用会经常出现？
- 如何确认当前位置和文件列表？
- 为什么 Windows 命令与 macOS/Linux 命令会有些不同？
- 在执行复制粘贴的命令时要注意什么？

这个补充学习先收束即使操作系统不同也共通的检查顺序：`先确认当前位置`、`查看文件列表`、`移动到实践文件夹`。shell script、pipe、redirection、管理员权限、环境变量（environment variable）会在 P2-7.8 补充学习中再次回收。

## 本补充学习的目标

- 能在入门层面说明如何在 Windows、macOS、Linux 中打开终端。
- 能说明打开终端后首先要确认当前位置。
- 能说明 Windows PowerShell 与 macOS/Linux shell 的命令有些地方不同。
- 能说明 `pwd`、`ls`、`cd`、`Get-Location`、`Get-ChildItem`、`Set-Location` 分别是做什么的。
- 在复制并执行命令之前，能先确认当前文件夹和该命令的目的。

## 三个标准

| 标准 | 为什么重要 | 本节所需的理解程度 |
| --- | --- | --- |
| 操作系统不同，终端应用、默认 shell、路径表示也会稍有不同 | 如果直接照搬别的操作系统示例，路径和命令可能会对不上 | 理解即使目的相同，命令写法也可能略有不同 |
| 即便如此，共通地首先要看的仍然是当前位置和文件列表 | 即使操作系统不同，实践前的检查顺序也不会差太多 | 保持“位置确认优先”的标准 |
| 终端快捷键可能与普通应用不同 | 如果把复制粘贴和中断执行混淆，工作会被打断 | 记住 `Ctrl+C` 这类行为要按环境小心处理 |

## 不同操作系统中的终端应用和 shell 可能不同

在使用终端时，最先出现的混淆通常是“终端应用”和“在里面运行的 shell”混在一起。

Microsoft 文档把 Windows Terminal 说明为一个现代宿主应用，它可以运行 Command Prompt、PowerShell、WSL 的 bash 等命令行 shell。也就是说，Windows Terminal 并不只代表一种 shell，而更像是可以用标签页打开多种 shell 的应用。

Apple 的 Terminal User Guide 把 macOS 中的 Terminal 介绍为创建和管理 shell script 的工具。在 macOS 中打开 Terminal 时，通常会使用 Unix 系列 shell。

Ubuntu 文档说明，Linux 虽然也有 GUI，但传统 Unix 环境使用命令行界面（command line interface, CLI），并且在大多数 Linux 发行版中，都能在终端里输入类似的命令。

这里可以这样整理。

| 操作系统 | 经常遇到的终端应用 | 经常遇到的 shell |
| --- | --- | --- |
| Windows | Windows Terminal、PowerShell、Command Prompt | PowerShell、Command Prompt、WSL 的 bash |
| macOS | Terminal、iTerm2、VS Code Terminal | zsh、bash |
| Linux | GNOME Terminal、Konsole、VS Code Terminal | bash、zsh |

本 Part 的实践会尽量标明命令是以哪个环境为基准。如果没有标明，通常多半是以 macOS/Linux 系 shell 为基准。

## 在 Windows 中先以 PowerShell 为基准

在 Windows 中会遇到好几种命令输入窗口。

- Windows Terminal
- PowerShell
- Command Prompt
- VS Code 的 Terminal 面板
- 如果安装了 WSL，则还有 Linux shell

这里在需要说明 Windows 时，先以 PowerShell 作为默认基准。Command Prompt 在旧资料中经常出现，但在 Python 学习和现代开发环境中，你更可能经常遇到 PowerShell 或 Windows Terminal。

在 Windows 中打开终端，最简单的方法通常是下面几种之一。

1. 在开始菜单里搜索 `Terminal` 或 `PowerShell`。
2. 如果正在使用 VS Code，就在顶部菜单中选择 `Terminal > New Terminal`。
3. 在项目文件夹中使用鼠标右键菜单提供的终端打开功能。这个菜单名称会因 Windows 版本和已安装工具而不同。

打开终端后，先确认当前位置。

```powershell
Get-Location
```

确认文件和文件夹列表。

```powershell
Get-ChildItem
```

移动文件夹。

```powershell
Set-Location C:\Users\someone\ws\project-name
```

在 PowerShell 中，也经常会使用短别名（alias）。

```powershell
pwd
ls
cd C:\Users\someone\ws\project-name
```

不过刚开始学习时，最好也同时知道正式命令名。以后查文档时，用 `Get-Location`、`Get-ChildItem`、`Set-Location` 来搜索，更容易找到准确资料。

## 在 macOS 中，通常会打开 Terminal 并遇到 zsh shell

在 macOS 中，可以使用默认应用 Terminal。

打开 Terminal 的方式有很多。

1. 在 Spotlight 搜索中输入 `Terminal`。
2. 在 Finder 中打开 `Applications > Utilities > Terminal`。
3. 如果正在使用 VS Code，就选择 `Terminal > New Terminal`。

打开终端后，确认当前位置。

```bash
pwd
```

确认文件和文件夹列表。

```bash
ls
```

移动到项目文件夹。

```bash
cd /Users/someone/ws/project-name
```

在 macOS 中，路径经常会显示成 `/Users/...` 形式。这与 Windows 的 `C:\Users\...` 形式不同，所以如果直接照抄别的操作系统示例，路径可能就不匹配。

在 macOS 中粘贴终端命令时，要特别小心带有 `sudo` 的命令。`sudo` 可能会让命令以管理员权限执行。在本 Part 前段的实践里，大多数情况下并不需要 `sudo`。

## 在 Linux 中，终端经常出现在学习资料里

在 Linux 发行版中，终端使用经常出现在学习资料里。Ubuntu 文档介绍了通过搜索功能和 `Ctrl + Alt + T` 这类快捷键打开终端的方法。菜单名称会因桌面环境而不同，但在很多 Linux 环境中，都可以通过搜索终端应用来打开它。

在 Linux 中打开终端后，先确认当前位置。

```bash
pwd
```

确认文件和文件夹列表。

```bash
ls
```

移动到项目文件夹。

```bash
cd /home/someone/ws/project-name
```

在 Linux 中，用户主目录经常是 `/home/用户名` 这种形式。这与 macOS 的 `/Users/用户名` 不同。

在 Linux 资料里，也经常会看到 `sudo apt install ...` 这类命令。这些命令可能会安装系统包。在这个 Python 入门阶段，不要不加判断地执行，先确认这个命令为什么需要。

## Tip：终端快捷键只先记少量即可

不需要把所有终端快捷键都背下来。先以“打开、复制粘贴、标签页、命令补全、中断执行”为标准即可。

| 情况 | Windows Terminal | macOS Terminal | Linux/Ubuntu 系 |
| --- | --- | --- | --- |
| 打开新标签页 | `Ctrl + Shift + T` | `Command + T` | 因终端应用而异，但经常会遇到 `Ctrl + Shift + T` |
| 复制 | `Ctrl + Shift + C` | `Command + C` | 经常会遇到 `Ctrl + Shift + C` |
| 粘贴 | 经常使用 `Ctrl + Shift + V` | `Command + V` | 经常使用 `Ctrl + Shift + V` |
| 中断正在运行的命令 | `Ctrl + C` | `Control + C` 或 `Command + .` | `Ctrl + C` |
| 文件/文件夹名自动补全 | `Tab` | `Tab` | `Tab` |
| 再次查看上一条命令 | `↑` | `↑` | `↑` |

这个表并不表示“所有环境中都一定完全一样”。它会因终端应用、shell、键盘布局，以及是否在 VS Code 这类编辑器里的终端中而不同。如果实际快捷键不同，就在应用菜单或设置里确认。

这里尤其有用的是 `Tab`。不用把文件夹名全部输完，只需输入前半部分后按 `Tab`，就可以补全可能的文件或文件夹名称。

例如，想移动到 `docs` 文件夹时，可以先像下面这样输入，然后按 `Tab`。

```bash
cd do
```

如果终端能找到 `docs`，就会自动补全。如果候选项有多个，可能不会一次完成。这时可以再多输入一点，或者在某些终端里按两次 `Tab` 查看候选项。

快捷键是提升速度的工具。但在一开始，比起速度，更重要的是确认当前位置和你即将执行的命令。

## Tip：Ctrl+C 和 Ctrl+V 在终端里可能表现不同

在普通应用里，人们习惯了 `Ctrl + C` 是复制，`Ctrl + V` 是粘贴。但在终端里，它们可能会表现不同。尤其是 `Ctrl + C`，经常被用作中断正在运行命令的信号。

例如，当你在终端里运行 Python 服务器、耗时很长的安装命令、或一个无限循环程序时，按下 `Ctrl + C` 可能不是复制，而是在请求中断执行。

所以，在终端里，最好把复制和粘贴快捷键单独记住。

| 环境 | 复制 | 粘贴 | 中断执行 |
| --- | --- | --- | --- |
| Windows Terminal | `Ctrl + Shift + C` | 经常使用 `Ctrl + Shift + V` | `Ctrl + C` |
| macOS Terminal | `Command + C` | `Command + V` | `Control + C` 或 `Command + .` |
| Linux/Ubuntu 系终端 | 经常使用 `Ctrl + Shift + C` | 经常使用 `Ctrl + Shift + V` | `Ctrl + C` |

这个区分很重要。

- 在普通文档中复制文字时，使用的是 `Ctrl + C` 或 `Command + C`。
- 在终端里停止正在运行的命令时，通常使用的是 `Ctrl + C`。
- 在终端中复制文字时，在 Windows/Linux 中经常使用 `Ctrl + Shift + C`。
- 向终端里粘贴时，在 Windows/Linux 中经常使用 `Ctrl + Shift + V`。

不过，快捷键也可能因终端应用设置而改变。Windows Terminal 可以修改键盘快捷键，macOS Terminal 也会在菜单中显示实际快捷键。如果快捷键没有按预期工作，就检查当前正在使用的终端应用菜单与设置。

这里先记住下面这些标准。

- 如果按下 `Ctrl + C` 却没有发生复制，那么在终端里它可能表示中断执行。
- 如果 Windows/Linux 终端里的复制粘贴不起作用，就检查 `Ctrl + Shift + C` 和 `Ctrl + Shift + V`。
- 在 macOS Terminal 中，先按一般 Mac 应用那样去想 `Command + C` 和 `Command + V`。

## 三种操作系统中共通要先确认的事

即使操作系统不同，实践前的确认顺序也很相似。

1. 打开终端。
2. 确认当前位置。
3. 确认文件列表。
4. 移动到实践文件夹。
5. 再次确认当前位置和文件列表。
6. 执行 Python 命令或包安装命令。

以 Windows PowerShell 为基准，流程如下。

```powershell
Get-Location
Get-ChildItem
Set-Location C:\Users\someone\ws\project-name
Get-Location
Get-ChildItem
```

以 macOS/Linux 为基准，流程如下。

```bash
pwd
ls
cd /Users/someone/ws/project-name
pwd
ls
```

在 Linux 中，移动路径可能会像下面这样。

```bash
cd /home/someone/ws/project-name
```

重要的并不是背下很多命令名，而是先养成确认“我现在在哪个文件夹里”的习惯。

## 路径分隔符不同

Windows 与 macOS/Linux 的路径表示方式不同。

| 区分 | Windows 示例 | macOS/Linux 示例 |
| --- | --- | --- |
| 用户文件夹 | `C:\Users\someone` | `/Users/someone`, `/home/someone` |
| 文件夹分隔符 | `\` | `/` |
| 项目示例 | `C:\Users\someone\ws\project-name` | `/Users/someone/ws/project-name` |

如果文档里出现 `/Users/someone/ws/project-name` 这种路径，它很可能是 macOS 示例。在 Linux 中更接近 `/home/someone/ws/project-name`，在 Windows 中则更接近 `C:\Users\someone\ws\project-name`。

因此，在复制路径示例时，需要改成自己电脑上的实际文件夹位置。

## 在运行 Python 命令之前要确认什么

在终端中运行 Python 之前，先确认下面这些内容。

- 当前终端是否以项目文件夹为基准打开？
- 要运行的 `.py` 文件是否位于当前文件夹？
- 所需数据文件是否在同一文件夹或指定路径中？
- 如果需要使用虚拟环境，当前虚拟环境是否已经激活？
- 在 `python`、`python3`、`py` 之中，哪个命令在我的环境里能运行？

Python 的执行命令会因操作系统和安装方式而不同。

```bash
python --version
```

```bash
python3 --version
```

在 Windows 中，如果安装了 Python Launcher，也可能会看到下面这个命令。

```powershell
py --version
```

这里不处理 Python 安装本身。这里只做到确认“哪个命令在我的环境里指向 Python”。真正需要安装的时点会在 P2-7.7 中单独处理。

## 复制粘贴的命令要先读再执行

从文档中复制并粘贴命令是很常见的事。这本身并不是坏习惯。Ubuntu 文档也说明，即使是熟练用户，也经常复制粘贴命令。

但是，在执行复制来的命令之前，应该先读一遍。

先确认下面这些内容。

- 这个命令默认假设你现在在哪个文件夹？
- 它是给 Windows 用的，还是给 macOS/Linux 用的？
- 它只是检查状态，还是会改动系统？
- 它里面有没有 `sudo`、安装包、删除、移动路径之类的部分？
- 前面是否包含 `$`、`>`、`PS>` 这样的提示符号？

尤其是在前期练习中，先养成在执行前确认 `当前位置`、`命令目的`、`操作系统是否匹配` 的习惯，会更安全。

文档里为了说明终端提示符，可能会像下面这样写。

```text
$ python example.py
```

这时，`$` 可能并不是让你输入的字符。它通常只是表示提示符。真正要输入的是后面的部分。

```bash
python example.py
```

在 PowerShell 文档里，也可能会像下面这样写。

```text
PS C:\Users\someone> python example.py
```

这时也不是把整个 `PS C:\Users\someone>` 都输入进去。实际命令是 `python example.py`。

## 出错时先把“位置”和“环境”分开看

遇到终端错误时，不要立刻判断成 `我不会 Python`。先把问题拆开。

| 错误情况 | 先看什么 |
| --- | --- |
| 找不到文件 | 当前工作文件夹和文件列表 |
| 找不到命令 | 程序是否已安装，以及 PATH 设置 |
| 找不到包 | 当前 Python 环境，以及是否安装了该包 |
| 出现权限错误 | 执行位置、文件权限、是否需要管理员权限 |
| 在 Colab 中可以，在本地不行 | 本地 Python 和包安装状态 |

在前期实践中，最常见的问题并不是很深的代码错误，而是当前文件夹不对、包安装在别的环境里，或者把 Colab 和本地 PC 误当成同一个环境。

## 案例与示例

### 案例 1. 复制了同一条命令，但在 Windows 和 macOS 中看起来不一样

假设你把学习资料中的 `cd /Users/someone/ws/project-name` 命令原样复制并执行。它在 macOS 中看起来很自然，但在 Windows PowerShell 里，从路径格式开始就会显得陌生，有些人甚至连粘贴快捷键的行为都不同而被卡住。

人原本的直觉通常是 `文档里这样写，直接贴进去就行`。但实际上，不同操作系统里的终端应用、默认 shell、路径表示、复制粘贴方式都会略有不同。

这里想减少的差异，正是这种按操作系统变化的表示差异。关键不是把所有命令都背下来，而是读出 `确认当前位置`、`确认文件列表`、`移动到项目文件夹` 这些共同目的。在 Windows 中，可以让 `Get-Location`、`Set-Location`、`Get-ChildItem` 去对应这些目的；在 macOS/Linux 中，则对应 `pwd`、`cd`、`ls`。

可以确认的结果，会直接显示在“显示当前位置”的命令上。即使操作系统不同，只要最终能确认 `我现在在哪个文件夹里`，就能大幅降低路径表示差异带来的初期混乱。

## 检查清单

- 能说明 Windows Terminal 是可运行多种命令行 shell 的宿主应用。
- 能在 macOS Terminal 中用 `pwd`、`ls`、`cd` 确认位置和移动。
- 能在 Linux 中打开终端并确认当前位置和文件列表。
- 能说明 Windows PowerShell 中 `Get-Location`、`Get-ChildItem`、`Set-Location` 的用途。
- 能说明 Windows 与 macOS/Linux 的路径表示差异。
- 能说明终端快捷键会因环境不同而变化，并且应先确认 `Tab`、`Ctrl + C`、复制粘贴这些行为。
- 能说明普通应用中的 `Ctrl + C`、`Ctrl + V` 与终端里的复制、粘贴、中断执行快捷键可能不同。
- 能区分复制来的命令中，哪些是提示符，哪些才是实际要输入的命令。
- 能说明像 `sudo`、`rm`、`del`、`Remove-Item` 这样的命令，在确认含义之前不应执行。
- 能说明 `打开终端 -> 确认当前位置 -> 确认文件列表 -> 移动到实践文件夹 -> 再次确认位置和文件列表 -> 执行 Python 命令` 这个顺序。

## 来源与参考资料

- Microsoft, [What is Windows Terminal?](https://learn.microsoft.com/en-us/windows/terminal/){: target="_blank" rel="noopener noreferrer" }, Microsoft Learn，确认日期：2026-07-19。用于确认 Windows Terminal 是运行 Command Prompt、PowerShell、WSL bash 等命令行 shell 的宿主应用。
- Apple, [Keyboard shortcuts in Terminal on Mac](https://support.apple.com/guide/terminal/keyboard-shortcuts-trmlshtcts/mac){: target="_blank" rel="noopener noreferrer" }, Apple Support，确认日期：2026-07-19。用于确认 macOS Terminal 中新建窗口/标签页、复制粘贴、`Tab`、`Ctrl-C` 类行为的快捷键。
- Apple, [Terminal User Guide](https://support.apple.com/guide/terminal/welcome/mac){: target="_blank" rel="noopener noreferrer" }, Apple Support，确认日期：2026-07-19。用于确认 macOS Terminal 的角色，以及执行命令、指定文件和文件夹的说明。
- Ubuntu Documentation, [UsingTheTerminal](https://help.ubuntu.com/community/UsingTheTerminal){: target="_blank" rel="noopener noreferrer" }, Ubuntu Community Help Wiki，确认日期：2026-07-19。用于确认在 Ubuntu/Linux 中打开终端并执行命令行工作的入门语境。
- Microsoft, [Get-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation，确认日期：2026-07-19。用于确认 PowerShell 中查看当前工作位置的命令及其 `pwd` 别名。
- Microsoft, [Set-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation，确认日期：2026-07-19。用于确认 PowerShell 中改变当前工作位置的命令及其 `cd` 别名。
- Microsoft, [Get-ChildItem](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation，确认日期：2026-07-19。用于确认 PowerShell 中列出文件和文件夹的命令及其 `ls` 别名。

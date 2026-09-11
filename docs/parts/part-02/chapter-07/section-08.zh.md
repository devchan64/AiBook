# P2-7.8 补充学习：阅读 shell 执行流程

> Section ID: `P2-7.8`
> Version: `v2026.09.08`

shell 中的 `|` 将一个命令的输出连接到下一个命令的输入。`>` 与 `<` 将输出和输入连接到文件，环境变量(environment variable)向程序传递设置值。下面的 shell 命令以 Bash 为准，并假设可用 `python` 执行 Python。

## 标准输入与标准输出

命令行程序可以通过标准输入(standard input)接收数据，通过标准输出(standard output)发送结果。直接在终端运行时，通常连接键盘与屏幕，但也可以改为连接文件或其他程序。

将下面代码保存为 `read_numbers.py`。它读取每行一个数字的输入，并打印总和。输入 `10`、`20`、`30`，输出为 `60`。

```python
import sys

# 逐行读取标准输入，转换为整数后求和。
numbers = [int(line) for line in sys.stdin if line.strip()]
print(sum(numbers))
```

在 Bash 中使用以下命令创建输入文件 `numbers.txt`。`printf` 会将 `\n` 转换为换行。

```bash
printf '10\n20\n30\n' > numbers.txt
```

## 用管道连接命令

`cat` 将文件内容发送到标准输出。通过 `|` 连接后，这些内容成为 Python 程序的标准输入。

```bash
cat numbers.txt | python read_numbers.py
```

输出为 `60`。两个程序直接交换数据，无需先显示文件内容，再由人重新输入。后面的程序必须被编写为读取标准输入，这种连接才有意义。

管道并非只是要求按顺序执行命令，而是把前一个命令的标准输出连接到后一个命令的标准输入。用于错误消息的标准错误(standard error)默认不包含在这个连接中。

## 将文件连接到输入与输出

使用 `<`，无需 `cat` 即可将同一文件连接到 Python 的标准输入。

```bash
python read_numbers.py < numbers.txt
```

同时使用 `>`，可将结果保存到 `total.txt` 而非屏幕。

```bash
python read_numbers.py < numbers.txt > total.txt
```

命令成功后，屏幕不显示总和，`total.txt` 中保存 `60` 和一个换行。可用 `cat total.txt` 查看内容。

| Bash 写法 | 操作 |
| --- | --- |
| `< input.txt` | 将文件连接到标准输入 |
| `> output.txt` | 将标准输出写入文件，覆盖已有内容 |
| `>> output.txt` | 将标准输出追加到文件末尾 |
| `2> errors.log` | 将标准错误写入单独文件 |

`python train.py > train.log` 也只保存标准输出，不能假定所有错误消息都会进入该文件。文件路径以当前工作文件夹为基准解释。

## 将命令保存为 shell 脚本

可把需要重复的命令保存到 `run_summary.sh`。

```bash
python read_numbers.py < numbers.txt > total.txt
cat total.txt
```

在包含这三个文件的文件夹执行以下命令，Bash 会读取脚本、保存总和并打印。

```bash
bash run_summary.sh
```

shell 脚本(shell script)是由 shell 解释的命令文件，与保存 Python 代码的 `.py` 文件使用不同的解释程序。

## 用环境变量传递设置

环境变量是在运行程序时传入的名称与值的组合。例如，可以在代码外指定数据文件夹。

在 Bash 中执行以下命令。

```bash
export BOOK_DATA_DIR="./data"
```

`export` 使此 shell 后续启动的子进程接收到这个值，不会改变其他已经运行的终端的环境。

将下面代码保存为 `show_config.py`，在同一 shell 执行 `python show_config.py`，会打印 `./data`。

```python
import os

# 环境变量不存在时，打印未设置状态。
print(os.environ.get("BOOK_DATA_DIR", "not set"))
```

在 Windows PowerShell 中，可按以下方式设置环境变量。

```powershell
$env:BOOK_DATA_DIR = "./data"
python show_config.py
```

环境变量的值是字符串。指定文件夹路径不会自动创建文件夹。API 密钥等秘密值也可以这样传递，但不应原样留在代码或输出日志中。

## 改变数字与输出保存方式

将 `numbers.txt` 的最后一个数字从 `30` 改为 `40`，总和会从 `60` 变为 `70`。执行以下命令，`total.txt` 中只保留新总和 `70`。

```bash
python read_numbers.py < numbers.txt > total.txt
```

保持相同输入，将 `>` 改为 `>>` 再执行，文件中会累积两行 `70`。计算代码相同，改变的只是 shell 的输出连接方式。

## 检查命令会改变的对象

| 写法 | 检查对象 |
| --- | --- |
| `>` | 将被覆盖的文件路径 |
| `rm`、`del`、`Remove-Item` | 将被删除的文件与文件夹 |
| `sudo` | 将以提升后的权限执行的命令 |
| 含秘密值的环境变量 | 值是否留在命令历史、日志或仓库中 |

PowerShell 管道还可以在命令间传递对象，并非所有语法都与 Bash 相同。尤其不要把上面的 `<` 输入重定向直接照搬到 PowerShell。

## 检查清单

- 能区分解释 shell 脚本与 Python 脚本的程序。
- 能说明 `|` 连接标准输出与标准输入。
- 能区分 `<`、`>`、`>>` 对应的文件读取、覆盖与追加。
- 能说明标准输出与标准错误是独立通道。
- 能在 Python 中读取通过环境变量传递的设置值。
- 能确认改变输入数字与输出连接方式后，文件内容如何变化。

## 来源与参考资料

- GNU Project, [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html){: target="_blank" rel="noopener noreferrer" }, GNU Bash 5.3 manual，确认日期：2026-07-20。用于确认 Bash 的 shell 角色、pipeline、redirection、变量与环境变量语法。
- Microsoft Learn, [about_Pipelines](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_pipelines){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation，确认日期：2026-07-20。用于确认 PowerShell 中 `|` 是把一个命令结果发送给下一个命令的 pipeline operator。
- Microsoft Learn, [about_Redirection](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_redirection){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation，确认日期：2026-07-20。用于确认 PowerShell 中 `>`、`>>`、`n>` 等 redirection operator 会把输出流发送或追加到文件。
- Microsoft Learn, [about_Environment_Variables](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_environment_variables){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation，确认日期：2026-07-20。用于确认环境变量是操作系统和程序使用的字符串设置值，并可被子进程继承。

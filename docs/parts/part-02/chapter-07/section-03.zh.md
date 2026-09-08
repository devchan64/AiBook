# P2-7.3 Python 解释器(interpreter)与脚本(script)

> Section ID: `P2-7.3`
> Version: `v2026.09.08`

`python` 是打开交互式 Python 的终端命令，`python hello.py` 则执行保存在文件中的代码。`print("hello")` 是解释器读取的 Python 代码。执行方式决定输入位置与保存结果的方法。

## 交互执行与脚本的背景

如果只把 Python 理解成“只能运行保存在文件里的程序的语言”，其实很难真正理解它。Python 官方 FAQ 把 Python 解释为一种 interpreted、interactive、object-oriented 的编程语言。它也说明，Guido van Rossum 是在实现 ABC 语言以及参与 Amoeba 分布式操作系统工作时，开始构想 Python 的；而在只靠 C 程序或 Bourne shell script 很难处理系统管理工作的背景下，需要一种更可扩展的脚本语言。

如果把这段背景压缩成入门者能抓住的程度，就是下面这样。

- shell script：适合把操作系统命令串起来做自动化。
- 像 C 这样的编译型语言：又快又强，但对小型自动化和小实验来说可能太重。
- Python：同时提供可读的高级语法、交互执行和脚本执行。

所以，在 Python 里自然会同时看到两种使用方式。

- 交互执行：立刻测试一个小表达式。
- 脚本执行：把多行工作保存成文件，然后反复执行。

AI 学习中经常使用 Python，也与此有关：可以用小段代码立即验证公式，较长的实验则容易保存为文件或笔记本。

## Python 解释器

Python 解释器(Python interpreter)是读取并执行 Python 代码的程序。官方文档说明，解释器可从命令行调用，在终端中不指定文件或其他执行选项时，会进入交互模式(interactive mode)。

## 交互模式与提示符

如果你在终端里运行 Python，就可以使用 `交互模式(interactive mode)`。

```bash
python
```

根据环境不同，命令名也可能是 `python3`。

```bash
python3
```

进入交互模式后，通常会看到 `>>>` 提示符。Python 官方文档也说明，交互模式里的默认提示符就是 `>>>`。

在 `>>>` 后输入表达式或函数调用，会立即显示结果。下面的 `>>>` 是提示符标记，不是要输入的代码。

```pycon
>>> 1 + 2
3
>>> print("hello")
hello
```

交互模式特别适合立即确认计算。

交互模式尤其适合下面这些情况。

- 检查一个很短的计算。
- 试试看某段语法。
- 立刻打印一个小值。

但在交互模式里输入的内容，通常不会作为文件保留下来。下次要再运行，还得再打一次。所以当多行代码需要反复执行时，我们会使用 `脚本(script)` 文件。

## 保存在文件中的脚本

`脚本(script)` 是把要执行的代码保存在文件里的形式。Python 文件通常使用 `.py` 扩展名。

例如，假设我们把下面这些内容保存到一个叫 `hello.py` 的文件中。

把下面两行保存到 `hello.py` 并执行，会依次打印 `hello` 和 `3`。

```python
# 脚本会从上到下依次执行多条语句。
print("hello")
print(1 + 2)
```

如果终端当前就在同一个文件夹里，就可以这样运行。

```bash
python hello.py
```

根据环境不同，也可能使用下面这个命令。

```bash
python3 hello.py
```

脚本执行和交互执行是不同的。

| 执行方式 | 输入位置 | 优点 | 需要注意的点 |
| --- | --- | --- | --- |
| 交互执行 | `>>>` 提示符 | 适合立即确认一行 | 输入内容可能不会保留成文件 |
| 脚本执行 | `.py` 文件 | 容易保存、修改、重跑、共享 | 必须确认当前工作文件夹和文件路径 |

在 AI 学习里，有时需要立刻检查一个小计算，有时又需要把同一段代码反复修改后再执行。所以两种方式都会遇到。

## shell 与 Python 的输入位置

在 shell 提示符下，用 `python hello.py` 请求执行文件；在 Python 的 `>>>` 下，输入 `print("hello")` 这样的 Python 代码。

如果在 Python 交互模式误输文件执行命令，会出现如下错误。

```pycon
>>> python hello.py
  File "<stdin>", line 1
    python hello.py
           ^^^^^
SyntaxError: invalid syntax
```

这时无需修改 `hello.py` 文件。在 `>>>` 输入 `exit()` 返回 shell，再运行 `python hello.py`。错误消息的细节可能随 Python 版本而变化。

## 笔记本单元与执行状态

Colab 或 Jupyter 的 `代码单元(code cell)`，会按单元来执行 Python 代码。

代码单元既像交互执行那样立即显示结果，又能在笔记本中留下记录。

```python
# 无论从终端还是代码单元运行，用来确认输出的代码都是一样的。
print("hello")
```

代码单元像交互执行一样，适合立即确认结果。同时，它又能把代码、结果和说明一起保留在笔记本文件中，所以很适合学习。

但代码单元也和脚本文件不同。只要单元执行顺序改变，结果就可能改变；前一个单元里创建的变量，也可能会被后一个单元拿来使用。

如果把三种执行位置再分开，就是下面这样。

- 交互模式：快速确认一行一行。
- 脚本文件：把整个文件保存下来并反复运行。
- 笔记本代码单元：边保留说明和结果，边按单元执行。

以后当练习变长时，就会出现这样的情况：`在笔记本里能跑，但搬到脚本里就不行了。` 那时就要把单元执行顺序、文件路径、必要的 import、包安装状态分开检查。

## 模块执行选项 -m

在终端里，你会经常看到下面这样的命令。

```bash
python -m pip install numpy
```

这里的 `-m`，是一种请求 Python 去把某个 `模块(module)` 当作脚本执行的方式。Python 官方文档说明，`python -m module` 这种形式会把一个库模块当作脚本运行。

两条命令指定执行对象的方式不同。

- `python hello.py`：运行一个文件。
- `python -m pip ...`：通过 Python 去运行名为 `pip` 的模块。

`-m` 是解释器的执行选项，不是 Python 代码语法。`python -m pip` 会在命令开头指定的 Python 中运行 pip。

## 按执行方式检查错误

即使是同样的 Python 代码，只要执行方式不同，先检查的点也会不同。

| 情况 | 先检查什么 |
| --- | --- |
| 在交互模式里不工作 | 我现在是不是在 `>>>` 提示符里？ |
| 脚本文件打不开 | 当前工作文件夹里有这个文件吗？ |
| 找不到 `python` 命令 | Python 装了吗，命令名对吗？ |
| 在 Colab 里能跑，本地不行 | 本地是不是也有同样的文件和包？ |
| 搬到脚本里就不行 | 有没有依赖过笔记本单元执行顺序留下来的值？ |

## 只留在笔记本中的变量

在前面的笔记本单元运行 `name = "Mina"` 后，另一个单元运行 `print(name)` 会打印 `Mina`。但如果只把 `print(name)` 移到 `hello.py`，新启动的 Python 没有定义 `name`，就会产生 `NameError`。

```python
# 在新的执行中，先定义所需的值。
name = "Mina"
print(name)
```

把两行一起保存后，脚本也会打印 `Mina`。将笔记本代码移到文件时，除了输出单元，还应包含该单元使用的变量定义和 import。

## 检查清单

- 能把 Python 解释器(interpreter)解释成读取并执行 Python 代码的程序。
- 能说明在交互模式(interactive mode)里，Python 代码是输入在 `>>>` 提示符里的。
- 能说明脚本(script)是保存在 `.py` 文件里的执行单位。
- 能区分 `python hello.py` 是终端命令，而 `print("hello")` 是 Python 代码。
- 能说明 Colab/Jupyter 代码单元会按单元执行 Python 代码。
- 能说明 `python -m pip ...` 里的 `-m` 是终端传给 Python 解释器的执行选项。
- 能说明运行 Python 时，先要区分当前位置是 shell、Python 提示符还是代码单元，以及自己要执行的是一行、一份文件还是一个笔记本单元。

## 来源与参考资料

- Python Software Foundation, [General Python FAQ](https://docs.python.org/3/faq/general.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-07-20。用于支撑 Python 是解释型、交互式编程语言这一说明，并确认 Guido van Rossum 的早期开发背景。
- Python Software Foundation, [Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-07-20。用于确认解释器调用、交互模式与脚本文件执行之间的区别。
- Python Software Foundation, [Command line and environment](https://docs.python.org/3/using/cmdline.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, 确认日期: 2026-07-20。用于确认 `python script.py`、`python -c`、`python -m module-name` 等命令行执行方式。

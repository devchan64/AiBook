# P2-7.5 依赖（dependency）与可复现性（reproducibility）

> Section ID: `P2-7.5`
> Version: `v2026.09.15`

要重新运行相同代码，还需要匹配所需的包、Python 版本、数据文件与执行位置。依赖(dependency)是代码需要的外部要素；可复现性(reproducibility)是重新构建执行条件后，能够确认相同运行行为或结果的性质。

| 术语 | 本节先要抓住的意思 |
| --- | --- |
| 依赖（dependency） | 我的代码所依靠的外部包和执行条件。 |
| 可复现性（reproducibility） | 把条件留下来，使同一份代码以后还能再次运行的性质。 |
| `requirements.txt` | 记录所需包列表和版本的代表性文件。 |
| 版本固定（version pinning） | 通过明确写出特定包版本来减少环境差异的方法。 |
| 环境记录（environment record） | 重新执行所需的备注，例如 Python 版本、包列表、运行位置等。 |

## 直接依赖与间接依赖

依赖（dependency）是我的代码为了运行而需要的外部条件。在 Python 实践里，最先遇到的通常是包依赖。

例如，下面这段代码需要 NumPy。

计算 NumPy 数组 `[1, 2, 3]` 的均值，会打印 `2.0`。代码使用 `import numpy`，因此运行环境需要 NumPy。

```python
# 导入 pandas，将 CSV 读取为表格。
import numpy as np

# values 是用来确认 NumPy 安装和平均值计算是否都正常的小数组。
values = np.array([1, 2, 3])
print(values.mean())
```

这段代码并不是只有 Python 就够了。还必须安装 NumPy。

- 我的代码：使用 `import numpy as np`。
- 所需外部包：NumPy。
- 因此，NumPy 就是这段代码的依赖。

依赖还可以分成直接依赖和间接依赖。

- 直接依赖：我在代码里直接使用的包。
- 间接依赖：我安装的包在内部又需要的其他包。

安装一个包时，也可能同时安装它所需的其他包。

## 重新运行所需的条件

可复现性（reproducibility）是指：在同样代码、同样条件下再次运行时，仍然可以期待同样行为的性质。

在 AI 和数据实践中，可复现性很重要。阅读数学说明时，这个问题看起来可能不大，但一旦开始运行代码，环境差异就可能改变结果。

- Python 版本可能不同。
- 包版本可能不同。
- 操作系统可能不同。
- 数据文件位置可能不同。
- Colab runtime 可能已经被重置。

因此，如果想共享实践内容，只给代码可能不够。你还需要把“我是在哪个环境里运行的”一起留下。

## 重置后的笔记本运行时

在 AI 学习中，“今天运行过的笔记本”一个月后再打开，是很常见的事。

在运行当天，下面这些条件是成立的。

- Colab runtime 处于开启状态。
- `numpy`、`pandas`、`matplotlib` 已经安装好了。
- 数据文件上传到了 `/content/data/` 文件夹。
- 代码单元从上到下按顺序执行过。

一个月后，情况可能已经不同。

- Colab runtime 被重置了，手动安装过的包消失了。
- 数据文件没有重新上传。
- 从中间单元开始执行，所以前面创建的变量不存在。
- 默认包版本改变了。

这时如果立刻判断“代码错了”，就可能错过真正原因。首先要检查执行条件有没有重新搭起来。可复现性就是一种让这种检查更容易的记录习惯。

## requirements.txt 安装列表

pip 文档把 requirements files 说明为：交给 `pip install` 的安装项目列表文件。常见文件名就是 `requirements.txt`。

例如，可以创建下面这样的文件。

```text
numpy
pandas
matplotlib
```

然后可以像下面这样安装。

```bash
python -m pip install -r requirements.txt
```

这个文件的作用如下。

- `requirements.txt` 不是 Python 代码。
- 它也不是终端命令。
- 它是写下“需要安装哪些包”的文件。

如果有这个文件，别人就能更容易知道“这个项目需要哪些包”。

## CSV 均值计算项目

假设一个小实践文件夹是下面这样组成的。

```text
score-summary/
  summary.py
  scores.csv
  requirements.txt
```

`summary.py` 会读取 CSV 文件并计算平均值。

[scores.csv](/AiBook/assets/part-02/chapter-07/scores.csv){ .csv-preview }

下载 `scores.csv`，放到 `summary.py` 所在文件夹。CSV 每行对应一名学生，`score` 列为 `82, 91, 77, 88`。在 `score-summary` 文件夹执行，会打印均值 `84.5`。

```python
# 导入 pandas，将 CSV 读取为表格。
import pandas as pd

# 读取 scores.csv，并计算表格数据中 score 列的平均值。
scores = pd.read_csv("scores.csv")
print(scores["score"].mean())
```

在 `requirements.txt` 中写入代码直接使用的包 `pandas`。

```text
pandas
```

接收的人进入该文件夹后，可以用下面的命令准备好所需包。

```bash
python -m pip install -r requirements.txt
```

安装与执行使用项目的同一个 Python。准备完成后，以 `python summary.py` 执行计算。只安装 requirements 并不能补上缺失的 CSV，还需要数据文件。

## 版本指定与已安装包的记录

包会随着时间变化。今天安装的 NumPy，并不能保证一年后安装到的还是同样版本。

所以可以把版本写下来。

```text
numpy==2.0.0
pandas==2.2.2
matplotlib==3.9.0
```

`==` 表示指定某个特定版本。这种方式可以称为版本固定（version pinning）。

pip 用户指南说明，可以把 `pip freeze` 的结果写入 requirements 文件，用于可重复安装（repeatable installs）。这时，文件里会记录执行 `pip freeze` 当时环境中已安装的包和版本。

例如，你可能会遇到下面这条命令。

```bash
python -m pip freeze > requirements-snapshot.txt
```

然后在另一个环境里，可以像下面这样安装。

```bash
python -m pip install -r requirements-snapshot.txt
```

`>` 将输出保存到文件，同名文件已存在时会覆盖它。`pip freeze` 输出当前环境已安装的包，因此可能包含项目未使用的包。

固定版本并不能使所有执行条件相同。操作系统、Python 版本、硬件与包的分发状态也可能产生影响。

例如，在制作学习资料时，可以考虑下面两种方式的差别。

- `pandas`：可能会安装最新版本，因此随着时间推移环境可能改变。
- `pandas==2.2.2`：因为要求特定版本，所以能更接近当时的环境。

上述版本号用于说明写法。实际安装列表应记录经项目运行确认的版本。

## 安装列表与项目元数据

requirements 文件与项目分发时的安装要求用途不同。

- requirements 文件：为了构成某个特定环境而要安装的列表
- 项目配置文件：用于分发包，或说明项目元数据的文件

## 笔记本安装命令与环境记录

Colab 很容易开始使用。但可复现性问题并不会消失。

Colab runtime 可能被重置。那时之前安装过的包也可能消失。并且，Colab 提供的默认包版本也可能随着时间发生变化。

所以，最好在笔记本顶部留下所需安装命令，或者养成记录“我是在哪个环境里运行的”的习惯。

下面的单元在当前笔记本内核安装 NumPy、pandas 和 Matplotlib。创建新运行时后，可用它重新准备所需的包。

```text title="IPython · 笔记本代码单元"
# 在当前代码单元环境中安装复现笔记本所需的主要包。
%pip install numpy pandas matplotlib
```

这个命令很方便，但从长期看，把包版本和执行日期一起留下会更安全。

例如，可以在笔记本最上方留下下面这样的简短备注。

- 编写日期：2026-07-20
- 执行环境：Google Colab
- 主要包：numpy, pandas, matplotlib
- 再次运行时要检查的内容：runtime 是否被重置，数据文件是否已上传

即使只是这个程度的备注，也能减少以后反复追踪同一错误所花的时间。

## 执行记录项目

执行记录应包含以下项目。

- 使用的是哪个 Python 版本
- 需要哪些包
- 重要包的版本是什么
- 代码是以哪个文件夹为基准运行的
- 数据文件应该放在哪里
- 是 Colab 还是本地 PC

有了这些信息，将来出现错误时，就更容易缩小原因范围。

## 缺少文件与缺少包的区别

在 CSV 均值计算项目中，分别省略不同条件，失败位置也不同。

| 执行条件 | 结果 | 需要恢复的项目 |
| --- | --- | --- |
| 没有 pandas | `import pandas` 处出现 `ModuleNotFoundError` | 向正在运行的 Python 安装包 |
| 有 pandas，但没有 scores.csv | `read_csv` 处出现 `FileNotFoundError` | 检查数据文件与当前工作文件夹 |
| 包与 CSV 都已准备 | 打印均值 `84.5` | 记录这些条件与执行命令 |

把 CSV 中的分数 `82` 改为 `100`，即使代码与包相同，均值也会变为 `89.0`。要比较结果，除了环境，还需确认输入数据相同。

## 根据安装列表重建环境

pip freeze 记录当前已安装的包，不负责验证兼容性或计算锁文件。在新虚拟环境中安装列表后，还需要执行依赖检查和实际示例。请选择项目的 Python，并在包含 scores.csv 与 summary.py 的目录中执行。

```bash
python --version
python -m pip install -r requirements.txt
python -m pip check
python summary.py
```

声明的依赖一致时，pip check 输出 No broken requirements found. 这不保证 CSV 已准备好或代码正确。还要确认最后一条命令输出 84.5，才能验证输入、包与执行连接起来。需要相同结果的实验还应记录代码和数据版本；使用随机数时，记录种子及相关库设置。仅靠种子不能保证不同操作系统或硬件上的运行完全一致。

## 检查清单

- 能把依赖（dependency）解释为我的代码运行所需的外部包。
- 能把可复现性（reproducibility）解释为以后还能再次运行同一份代码的条件。
- 能说明 `requirements.txt` 是装载待安装包列表的文件。
- 能说明 `python -m pip install -r requirements.txt` 是根据 requirements 文件来安装包的命令。
- 能说明 `pip freeze` 可以用来记录当前环境里安装的包和版本。
- 能说明版本固定可以提高可复现性，但并不能解决所有问题。
- 能检查这段代码依赖哪些外部包、它们装在哪个 Python 环境里、以及是否留下了以后重建同样环境的记录。

## 来源与参考资料

- Python Packaging Authority, [User Guide](https://pip.pypa.io/en/stable/user_guide/){: target="_blank" rel="noopener noreferrer" }, pip documentation，确认日期：2026-07-20。用于确认 `python -m pip`、包安装、requirements 文件，以及为了 repeatable installs 使用 `pip freeze` 的语境。
- Python Packaging Authority, [pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/){: target="_blank" rel="noopener noreferrer" }, pip documentation，确认日期：2026-07-20。用于确认它会以 requirements 格式输出当前环境中已安装的包。
- Python Packaging Authority, [install_requires vs requirements files](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide，确认日期：2026-07-20。用于确认项目分发用依赖元数据与复现执行环境用 requirements 文件之间的角色差异。

- [pip check](https://pip.pypa.io/en/stable/cli/pip_check/){: target="_blank" rel="noopener noreferrer" }, 查阅日期：2026-09-15。

- [NumPy random compatibility policy](https://numpy.org/doc/stable/reference/random/compatibility.html){: target="_blank" rel="noopener noreferrer" }, 查阅日期：2026-09-15。

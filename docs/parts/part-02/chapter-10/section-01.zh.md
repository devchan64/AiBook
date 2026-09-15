# P2-10.1 为什么笔记本有助于学习

> Section ID: `P2-10.1`
> Version: `v2026.09.15`

笔记本（notebook）是把代码、运行结果和说明保存在一起的计算文档。在 Jupyter Notebook 或 Google Colab 中，可以按单元运行代码，查看下方的数字、表格和图表，并记录解释。

## 代码单元与 Markdown 单元

单元（cell）是文档中的小块。代码单元执行计算；Markdown 单元记录标题、说明、公式和链接。输出附属于产生它的代码单元，不是独立的单元类型。

| 组成 | 作用 | 示例 |
| --- | --- | --- |
| Markdown 单元 | 记录问题与解释 | 同时查看三名学生的平均分与低分 |
| 代码单元 | 执行计算 | `sum(scores) / len(scores)` |
| 代码单元的输出 | 显示结果 | `67.33333333333333` |

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-cell-learning-flow-zh.mmd"
```

`[82, 75, 45]` 的平均值约为 67.33。Python 脚本可以用 `print()` 显示它。

```python
scores = [82, 75, 45]
average = sum(scores) / len(scores)
print(average)
```

Python 笔记本代码单元也会显示最后一个表达式的值。下面的单元把计算结果存入 `average`，再通过最后一行显示它，输出与前面的代码相同。

```python
scores = [82, 75, 45]
average = sum(scores) / len(scores)
average
```

在计算后的 Markdown 单元中写下“平均分约为 67.33，但有一名学生只有 45 分”，可以同时记录代表值与个体值的差异。修改代码不会自动更新这段解释。

## 分单元实验

把数据准备、计算和条件变更分开，更容易识别结果属于哪个阶段。

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-experiment-flow-zh.mmd"
```

第一个代码单元准备五名学生的分数。赋值语句不显示输出，但会在正在运行的 Python 内核中创建 `scores`。内核（kernel）是执行代码并维护变量等状态的进程。

```python
scores = [82, 75, 45, 90, 61]
```

第二个单元计算前面分数的平均值，显示 `70.6`。

```python
mean_score = sum(scores) / len(scores)
mean_score
```

第三个单元选择大于或等于标准 `60` 的分数，显示 `[82, 75, 90, 61]`。

```python
threshold = 60
passed = [score for score in scores if score >= threshold]
passed
```

把第三个单元中的 `threshold` 改为 `80`，只重新运行这个单元，会显示 `[82, 90]`。分数数据与平均值不变，改变的只有选择标准和结果。

## 输入变化与需要重算的单元

`mean_score` 保存的是计算当时的数值，不是持续关联 `scores` 的公式。把标准设为 60 并运行前面的三个单元后，把数据单元中最后一个分数从 `61` 改为 `100`，比较结果。

| 操作 | 内核中的最后一个分数 | 已保存的 `mean_score` | 标准为 60 的 `passed` |
| --- | --- | --- | --- |
| 只修改代码，不运行 | 61 | 70.6 | `[82, 75, 90, 61]` |
| 只重跑数据单元 | 100 | 70.6 | `[82, 75, 90, 61]` |
| 重跑数据 → 平均值 → 选择单元 | 100 | 78.4 | `[82, 75, 90, 100]` |

修改生成输入的单元后，还要重跑使用该输入的计算与输出。单元旁的执行编号能提示实际运行顺序，但不能保证当前代码、输入与输出一致，因为运行后仍可能编辑代码，或在其他单元中修改变量。

## 执行顺序与残留状态

页面上的单元顺序可能与实际执行顺序不同。运行下面的第一个单元，会在内核中保存 `x = 10`。

```python
x = 10
```

运行下一个单元会显示 `15`。

```python
x + 5
```

如果只把第一个单元改为 `x = 100` 而不运行，重跑第二个单元仍显示 `15`，因为内核保留的还是 `10`。依次运行第一个和第二个单元后，结果才变为 `105`。

重启内核会清除之前的变量状态。此时只运行第二个单元，会因 `x` 未定义而产生 `NameError`。重启后从上到下运行全部单元，可以检查文档中保留的代码能否重新生成结果。

| 检查对象 | 原因 |
| --- | --- |
| 导入与数据准备单元 | 确认所需输入与包 |
| 重启内核后运行全部 | 检查是否依赖之前留下的值 |
| 代码与输出一致 | 检查修改后的代码是否真正运行 |
| 输出与解释一致 | 检查说明是否反映结果变化 |

## 案例：平均值相同，离散程度不同

下面两组分数的平均值都是 12。只比较平均值看不出差异，因此还要计算数值偏离平均值的程度。这里使用描述统计中的方差，即偏差平方和除以数据项数。

```python
sample_a = [10, 12, 13, 11, 14]
sample_b = [8, 16, 9, 15, 12]

mean_a = sum(sample_a) / len(sample_a)
mean_b = sum(sample_b) / len(sample_b)
variance_a = sum((value - mean_a) ** 2 for value in sample_a) / len(sample_a)
variance_b = sum((value - mean_b) ** 2 for value in sample_b) / len(sample_b)

print("means:", mean_a, mean_b)
print("variances:", variance_a, variance_b)
```

```text
means: 12.0 12.0
variances: 2.0 10.0
```

解释可以写成“平均值相同，但 B 的方差是 A 的五倍”。把 B 改为 `[10, 14, 11, 13, 12]` 后重跑，平均值仍为 12，方差变为 2。此时两组数据的平均值与方差都相同，原来的解释也要修改。

笔记本可以同时保留输入、计算、输出与解释。但修改输入后，仍需要分别重跑计算和修改解释。

## 笔记本与脚本的用途

笔记本适合结合说明查看中间结果的探索。需要重复执行的任务，或在多处复用的函数，可以分离到 `.py` 脚本或模块中。

| 任务 | 组织示例 |
| --- | --- |
| 结合数据与图表解释 | 在笔记本中放置代码、输出和解释 |
| 比较实验条件 | 记录各条件的结果与说明 |
| 在多个实验中复用处理 | 把公共函数分离到 Python 模块 |
| 重复执行固定任务 | 使用输入和执行顺序明确的脚本 |

例如，把分数统计函数放进模块，笔记本调用函数，比较两组输入的结果并记录解释。

## 检查清单

- 能把笔记本解释为结合代码、说明与输出的计算文档。
- 能区分代码单元与 Markdown 单元。
- 能解释笔记本为何适合记录 AI 数学和 Python 实践。
- 能解释单元执行顺序如何影响结果。
- 能解释笔记本为何不能完全代替脚本。
- 能同时记录问题、代码、输出与解释。
- 能把笔记本理解为执行工具和学习记录。

## 来源与参考资料

- Project Jupyter, [Project Jupyter Documentation](https://docs.jupyter.org/en/latest/){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation，确认日期：2026-07-20。用于确认 notebook 是把代码、说明、数据、可视化和交互放在一起的文档。
- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation，确认日期：2026-09-15。作为区分 notebook document、user interface、kernel 等组成部分的背景依据。
- Google, [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }, Google Colab，确认日期：2026-07-20。用于确认在浏览器 notebook 环境中一起执行和记录代码与说明的示例。
- IPython, [Execution semantics](https://ipython.readthedocs.io/en/stable/interactive/reference.html#execution-semantics){: target="_blank" rel="noopener noreferrer" }, 核对日期：2026-09-15。最后表达式显示与代码执行的依据。

# P2-2.1 重新阅读变量（variable）、函数（function）与表达式（expression）

> Section ID: `P2-2.1`
> Version: `v2026.07.20`

在 P2-1.2，我们建立了这样一种视角：公式、代码和数据是在用不同方式展示同一个计算。现在，我们来恢复阅读公式时最先遇到的基本记号。

\[
x
\]

\[
y = f(x)
\]

\[
\mathrm{loss} = f(\mathrm{prediction}, \mathrm{target})
\]

这些表达在你很久以前学数学时，也许显得太基础而被直接略过。但在 AI 文档里，如果你读不懂变量（variable）、函数（function）、表达式（expression），就很难找到模型（model）、输入（input）、输出（output）、损失（loss）、参数（parameter）分别站在什么位置。

这里的重点，是培养一种习惯：读公式里的符号时，要把它们读成 `哪个值`、`哪种关系`、`哪段计算`。

这里会重新整理 `变量`、`函数`、`表达式`、`输入`、`输出`。如果 1.2 给你的是“公式、代码、数据是同一计算的不同面孔”这种感觉，那么这一节整理的就是：读懂这个计算所需的最小符号语法。

## 本节目标

- 能把变量（variable）读成贴在数值或数据上的名字。
- 能把函数（function）读成把输入变成输出的关系。
- 能把表达式（expression）看成一种可计算关系或步骤的压缩表达。
- 能把 `y = f(x)` 解释为模型执行（inference）的最简单形式。
- 能在不混淆的前提下，把数学变量和代码变量连接起来。

## 三个判断标准

阅读正文时起标准作用的三个视角如下。

| 标准 | 为什么重要 | 本节需要达到的理解程度 |
| --- | --- | --- |
| 变量不是值本身，而是指向值的名字 | 它避免你立刻把符号和它代表的东西混为一谈。 | 理解变量是装载值的名字。 |
| 函数是把输入变成输出的关系 | 它让你把模型和规则放在同一个结构里阅读。 | 理解 `y = f(x)` 应被读成输入-变换-输出。 |
| 表达式是把计算或关系简短写下来的方式 | 它会成为解释损失、预测、误差公式的起点。 | 理解表达式是计算步骤的压缩形式。 |

## 变量是指向值的名字

变量（variable）是指向值的名字。在数学里，常常使用 `x`、`y`、`n`、`w` 这类短符号。

\[
x = 3,\quad y = 2,\quad n = 4
\]

这里的 `x`、`y`、`n` 并不是值本身，而是指向这些值的名字。在 AI 文档里，变量名通常还带着更多含义。例如，`x` 常常表示输入数据，`y` 表示答案或目标值，`w` 表示权重（weight），`b` 表示偏置（bias），`ŷ` 表示模型做出的预测（prediction），`L` 表示损失（loss）。

符号在不同文档里可能代表不同含义。所以看到公式时，第一件事要找的是：`这篇文字把这个符号定义成了什么？` 即使同样是 `x`，在一篇文档里它可能是一个值，在另一篇里可能是向量，在第三篇里甚至可能是整个数据集。

## 代码里的变量和数学里的变量

变量在 Python 代码中也会出现。

问题情境：用最简单的例子确认数学变量和代码变量是如何对应的。
输入（input）：两个整数值，以及保存它们之和的变量。
期望输出（output）：不会打印输出，但会建立一个变量名指向具体值的结构。
要确认的概念：代码变量也是指向某个值的名字，但它处理的是执行过程中可被重新赋值的具体存储目标。

```python
# x 和 y 是给计算值起的名字。
x = 3
y = 2

# total 是把两个值相加后得到的表达式结果。
total = x + y
```

示例结果：

```text
x 指向 3，y 指向 2，total 指向 5。
```

数学变量和代码变量是相似的。两者都会把名字附着到某个值上。但它们并不完全相同。

| 视角 | 数学里的变量 | 代码里的变量 |
| --- | --- | --- |
| 主要角色 | 简洁地表达关系 | 在执行中保存并引用值 |
| 值是否变化 | 取决于语境，可固定也可变化 | 在执行流程中可被重新赋值 |
| 数据类型 | 往往由语境推断 | 有具体类型，如 int、float、string、array |
| 错误 | 定义模糊时难以解释 | 可能在执行中出现类型、shape、命名错误 |

这个差异很重要。在公式里，只说 `x` 是一个向量可能就够了。但在代码里，你必须确认 `x` 实际上是什么 shape、什么 type、是不是空的。

问题情境：把数学里的 `x` 换成代码里的真实数组值，并检查它的 shape 和 type。
输入（input）：包含三个值的 NumPy 数组 `x`。
期望输出（output）：打印出数组值、`shape` 和 `dtype`。
要确认的概念：在代码里，不只是名字要读，还必须一起读实际值、shape 和 type。

```python
# 这个例子通过变量、函数和数组属性检查输入值与计算结果的含义。
import numpy as np

# x 是装着多个数字的数组变量。
x = np.array([1, 2, 3])

print(x)

# shape 和 dtype 是观察数组形状和值类型的要点。
print(x.shape)
print(x.dtype)
```

示例运行结果：

```text
[1 2 3]
(3,)
int64
```

这个例子是把数学记号 `x` 变成可在代码中检查的值的最小示例。读者在这里必须立刻看到的是：仅仅读名字 `x` 并不够，值本身、它的 `shape`、它的 `dtype` 都要一起读。

## 函数是把输入变成输出的关系

函数（function）是接收输入（input）并生成输出（output）的关系。

\[
y = f(x)
\]

这个表达可以读成：`x 进入，经过叫作 f 的关系或规则，然后输出 y。`

在 AI 语境里，`f` 可能是人直接写下来的规则，也可能是一个学出来的模型。比如，如果它是规则函数，你可以把它读成“年龄大于等于 19 就分类为成年人”；如果它是学出来的模型，你可以把它读成“根据输入特征预测购买可能性”。

在代码里，两者都可能像函数那样被调用。

问题情境：确认即使是规则判断，在代码里也会以函数调用的形式出现。
输入（input）：接收年龄并返回是否为成年的函数 `is_adult`，以及输入值 `20`。
期望输出（output）：打印出 `True`。
要确认的概念：函数就是接收输入、生成输出的关系，这件事可以在最简单的规则例子里看到。

```python
# 这个例子通过变量、函数和数组属性检查输入值与计算结果的含义。
def is_adult(age):
    # age 是要判断的输入值，True/False 是函数输出。
    return age >= 19

print(is_adult(20))
```

示例运行结果：

```text
True
```

模型也可以被广义地视为“接收输入、输出结果”的函数。

问题情境：看看把模型调用也读成函数调用的最小形式。
输入（input）：接收 `input_data` 并生成预测的调用式 `model(input_data)`。
期望输出（output）：不会打印输出，但会展示把结果放进变量 `prediction` 的结构。
要确认的概念：在 AI 语境里，模型也可以被读成把输入变成输出的函数。

```python
# input_data 是传入模型的输入，prediction 是模型返回的预测值。
prediction = model(input_data)
```

不过，机器学习模型和简单规则函数并不一样。模型内部有学习得到的参数（parameter），即使函数结构相同，只要参数值不同，输出就会不同。

## 表达式是在表达计算关系

表达式（expression）是由值、变量、运算符（operator）、函数组合起来，用来表达某种计算关系的形式。

\[
x + y
\]

\[
2x + 1
\]

\[
f(x)
\]

\[
(\mathrm{prediction} - \mathrm{target})^2
\]

在数学文档里，表达式通常很短，但里面其实包含了计算顺序。

\[
(\mathrm{prediction} - \mathrm{target})^2
\]

这个表达式可以读成：先用预测值减去目标值，再把这个差平方，从而把误差的大小变成正数。

在代码里，可以这样写。

问题情境：把表达式 `(prediction - target)^2` 展开成代码步骤并计算。
输入（input）：预测值 `2.8` 与目标值 `3.0`。
期望输出（output）：打印出平方误差值。
要确认的概念：表达式不是抽象符号游戏，而是可以展开成真实计算顺序的东西。

```python
# prediction 是模型预测值，target 是用来比较的真实值。
prediction = 2.8
target = 3.0

# error 和 squared_error 用来观察预测值偏离真实值的程度。
error = prediction - target
squared_error = error ** 2

print(squared_error)
```

示例运行结果：

```text
0.04000000000000007
```

这里重要的是：表达式不是单纯的符号游戏。表达式会决定比较哪些值、让哪些值的大小变得重要、以及产生什么样的结果。

## 在 AI 里经常遇到的基本关系

如果把 AI 文档里经常遇到的关系尽可能简化，会变成下面这样。

```text
prediction = model(input)
loss = compare(prediction, target)
updated_parameters = update(parameters, loss)
```

这并不是在精确写出真实学习算法，但它有助于固定变量、函数和表达式的位置。

- `input`：进入模型的数据
- `model`：把输入变成输出的函数或系统
- `prediction`：模型生成的输出
- `target`：作为比较标准的值
- `loss`：把 prediction 和 target 的差异用数字表示出来的值
- `parameters`：在学习过程中被调整的值
- `update`：让 parameters 朝着减小 loss 的方向改变的步骤

一旦知道了这个结构，后面遇到的公式就会少一些陌生感。即使是复杂公式，最终也可以读成：给值命名，通过关系做变换，再比较某个计算结果。

## 名字有助于理解，但它不保证理解

变量名有助于理解。像 `input_data`、`target`、`prediction` 这样的名字，通常会比只有 `x`、`y` 更容易读懂。但你不能只相信名字。

问题情境：看看一种情况，变量名看起来很合理，但值的意义和结构仍然需要另外检查。
输入（input）：两组看起来像预测和答案的列表。
期望输出（output）：不会打印输出，但会展示一种状态：仅凭名字还无法知道值的完整类型和意义。
要确认的概念：变量名只是线索，真实值的 shape 和意义仍需额外确认。

```python
# prediction 和 target 是用来并排比较多个样本预测值与真实值的列表。
prediction = [0, 1, 1, 0]
target = [0, 1, 0, 0]
```

只看名字，这段代码似乎已经告诉我们 prediction 和 target 是什么。但实际上，我们还必须检查：每个值到底是类别编号、概率，还是布尔值；两组数据长度是否相同；顺序是否一致。

在 AI 中，错误往往发生在公式和数据、代码的连接点。即使变量名看起来很合理，你仍然必须检查实际值的 shape、type、meaning 和 unit。

## 用案例来看

### 案例 1. 当 `y = f(x)` 不再只是抽象公式，而开始被读成模型执行的瞬间

假设一个学习者看到 `y = f(x)` 时，觉得这只是很多年前数学课里的函数题。但在 AI 文档中，这个表达经常正是最基本的计算结构：`把输入 x 放进模型 f，得到输出 y`。

例如，假设客户信息是输入，而模型输出购买可能性。那么 `x` 可以读成客户特征组合，`f` 读成学好的模型，`y` 读成预测分数或分类结果。也就是说，这三个符号分别站在数据、模型和输出的位置上。

这个案例说明了为什么变量和函数不只是简单的数学词汇。要能读 AI 公式，你就必须把 `x`、`y` 不仅看成值名字，还要连到输入、答案、预测、权重这些语境上。

归根到底，重要的不是符号本身，而是角色。只要你能读出这个表达“放进去什么，又拿出来什么”，那么以后再加上损失和参数，也仍然可以在同一结构上解释。

## 检查清单

- 你能把变量解释成贴在值或数据上的名字吗？
- 你能把函数解释成把输入变成输出的关系吗？
- 你能把表达式解释成可计算关系的压缩表达吗？
- 你能把 `y = f(x)` 读成 AI 模型执行的基本结构吗？
- 你能说明代码变量和数学变量相似，但在 type、shape、重新赋值上又不同吗？
- 你能说明不能只相信变量名，而还要检查它的意义、type 和 shape 吗？
- 你能在读变量、函数、表达式时，一起检查值的意义、输入输出关系，以及代码里的 type 和 shape 吗？

## 来源与参考资料

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, 确认日期：2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, 确认日期：2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, 确认日期：2026-07-19.
- Python Software Foundation, [Assignment statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements){: target="_blank" rel="noopener noreferrer" }, Python Language Reference, 确认日期：2026-07-19. 这是确认代码变量与重新赋值说明的直接参考资料。
- NumPy Developers, [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, 确认日期：2026-07-19. 这个官方参考资料支持检查数组变量 `shape` 和 `dtype` 的示例。

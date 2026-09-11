# P2-8.1 值、变量与类型

> Section ID: `P2-8.1`
> Version: `v2026.09.08`

`82` 与 `"82"` 在屏幕上看起来相似，计算结果却不同。`82 + 3` 得到 `85`，而 `"82" + 3` 会报错，因为数字与字符串的类型(type)不同。

| 标准 | 为什么重要 |
| --- | --- |
| 值(value)是计算处理的数据 | 数字、文本与真假值都可作为运算输入。 |
| 变量(variable)是指向值的名称 | 可通过名称复用值，或改为指向其他值。 |
| 类型(type)是值的种类 | 区分可以应用于值的运算。 |

## 值与运算

数字 `3`、`3.14`，字符串 `"AI"`，以及真假值 `True`、`False` 都是值。运算(operation)是对这些值进行的处理。

数字 `3` 与 `2` 相加得到 `5`，字符串 `"AI"` 与 `"Book"` 相加得到 `AIBook`。以下代码依次打印两种结果。

```python
print(3 + 2)
print("AI" + "Book")
```

同一个 `+` 对数字执行加法，对字符串执行拼接。

## 变量与赋值

Python 用 `=` 将名称与值关联，这一操作称为赋值(assignment)。

宽 `20`、高 `45` 的矩形，面积为 `900`。代码中的 `width` 与 `height` 指向长度，`area` 指向乘积。

```python
width = 20
height = 45
area = width * height
print(area)
```

数学等式描述两边相等的关系。Python 赋值语句先计算右侧，再将左侧名称关联到结果。`area = width * height` 不是持续维护面积与两条边之间关系的公式。以后改变 `width`，`area` 不会自动重新计算。

同一个名称也能赋予新值。下面的 `score` 先指向 `10`，再指向 `12`，因此打印 `12`。

```python
score = 10
score = 12
print(score)
```

变量有时被比作盒子，但对 Python 而言，理解为指向值的名称更准确，因为两个名称可以指向同一对象。

## 基本类型

类型是值的种类，决定哪些运算可用。将值传给 `type()`，即可检查其类型。

以下代码依次打印 `3`、`3.14`、`"AI"`、`True` 的类型，结果为 `<class 'int'>`、`<class 'float'>`、`<class 'str'>`、`<class 'bool'>`。

```python
print(type(3))
print(type(3.14))
print(type("AI"))
print(type(True))
```

| 类型 | 读法 | 例子 | 含义 |
| --- | --- | --- | --- |
| `int` | integer | `3`、`100` | 整数 |
| `float` | floating-point number | `3.14`、`0.5` | 浮点数 |
| `str` | string | `"AI"`、`"42"` | 字符串 |
| `bool` | boolean | `True`、`False` | 真或假 |

`float` 常用于带小数部分的数。小数部分为 0 的值，如 `3.0`，也可以用 `float` 表示。

## 重新赋值与类型

Python 中，同一个名称可以指向不同类型的值。先把整数 `82` 赋给 `score`，再赋予字符串 `"82"`，打印的类型便从 `<class 'int'>` 变为 `<class 'str'>`。

```python
score = 82
print(type(score))

score = "82"
print(type(score))
```

具有类型的是名称所指向的值。名称无需预先声明类型，但运算仍遵循类型规则。如下将字符串 `"82"` 与整数 `3` 相加，会产生 `TypeError`。

```python
score = "82"
bonus = 3

print(score + bonus)
```

字符串与整数无法直接用 `+` 相加。如果要为分数增加 3 分奖励，需先将分数转换为数字。

## Python 的语言特性

何时检查类型、如何执行代码、主要用于什么，是不同的分类标准。

| 分类 | 含义 | 例子 |
| --- | --- | --- |
| 静态类型(static typing) | 执行前检查类型 | Java、C、C++ 中可见 `int score` 这样的类型声明。 |
| 动态类型(dynamic typing) | 运行时按值的类型处理运算 | Python 中 `score` 可先指向整数，再指向字符串。 |
| 编译(compilation) | 将代码转换为其他可执行形式 | C/C++ 中可见为生成可执行文件而进行的编译步骤。 |
| 解释器(interpreter) | 读取并执行代码的程序 | Python 解释器执行交互输入或脚本。 |
| 脚本与胶水(scripting/glue) | 连接文件与已有工具的用途 | Python 读取数据文件并交给分析库。 |

这些分类并不互斥。Python 官方摘要将其描述为高级(high-level)、解释式(interpreted)、具有动态语义(dynamic semantics)的语言。

## 数字与字符串

数字 `30` 加数字 `1`，得到 `31`。字符串 `"30"` 加字符串 `"1"`，打印 `301`。

```python
age_number = 30
age_text = "30"

print(age_number + 1)
print(age_text + "1")
```

从 CSV 或 Excel 读取的值，也可能因读取方式与数据内容而成为字符串。用于数量或分数计算前，需要检查实际类型。

| 原始数据 | 人理解的含义 | 检查点 |
| --- | --- | --- |
| `"100"` | 数量 100 | 是字符串还是数字 |
| `"0.92"` | 概率分数 0.92 | 数值计算前是否需要转为 `float` |
| `"True"` | 看起来表示真的文本 | 是否为实际 `bool` |
| `"2026-06-24"` | 日期 | 是字符串还是日期类型 |

## 比较与布尔值

比较(comparison)的结果是布尔值 `True` 或 `False`。判断分数 `92` 是否不低于标准 `60`，得到 `True`。以下代码打印结果及类型 `<class 'bool'>`。

```python
score = 92
passed = score >= 60

print(passed)
print(type(passed))
```

`>=` 比较左值是否大于或等于右值。预测分数是否达到阈值(threshold)、数据是否有缺失值等判断，也可以用布尔值表示。

## 案例：字符串分数是否通过

假设判断学生 Kim 的分数 `82.5` 是否达到标准 `60.0`。姓名作为字符串，分数与标准作为数字，判断结果作为布尔值。以下代码依次打印 `Kim`、`82.5`、`True`。

```python
student_name = "Kim"
score = 82.5
threshold = 60.0

passed = score >= threshold

print(student_name)
print(score)
print(passed)
```

但如果文件中的分数读入为字符串 `"82.5"`，就不能直接进行相同比较。以下代码无法对 `str` 与 `float` 应用 `>=`，因此产生 `TypeError`。

```python
score = "82.5"
threshold = 60.0

print(score >= threshold)
```

可以用 `float()` 将字符串中的数转换为数字。以下代码打印转换前后的类型 `<class 'str'>`、`<class 'float'>`，以及通过结果 `True`。

```python
score_text = "82.5"
score = float(score_text)
threshold = 60.0

print(type(score_text))
print(type(score))
print(score >= threshold)
```

`score_text` 指向原始字符串，`score` 指向转换后的数字。将最后代码中的 `threshold` 改为 `90.0`，结果变为 `False`。分数类型匹配后才能执行比较，改变比较标准则会改变判断结果。

## 检查清单

- 能区分值、变量与类型。
- 能说明 Python 的 `=` 是向名称赋值的语法。
- 能说明 `int`、`float`、`str`、`bool` 的基本差异。
- 能区分看起来像数字的字符串与实际数字。
- 能用 `type()` 检查值的类型。
- 能说明出现类型错误时应先检查数据状态。
- 能说明即使屏幕上看起来像数字，也应先检查实际类型的原因。

## 来源与参考资料

- Python Software Foundation, [What is Python? Executive Summary](https://www.python.org/doc/essays/blurb/){: target="_blank" rel="noopener noreferrer" }, Python.org，确认日期：2026-07-20。用于确认 Python 的动态语义(dynamic semantics)、动态类型(dynamic typing)和高层内置数据结构说明。
- Python Software Foundation, [An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认 Python 交互式示例中 prompt、数字、字符串和列表的介绍方式。
- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认 `int`、`float`、`str`、`bool` 等基本类型，以及不同类型对应的运算差异。
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation，确认日期：2026-07-20。用于确认 Python 对象具有 identity、type、value 这一说明。

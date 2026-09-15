# P2-8.2 列表（list）：有顺序的值集合

> Section ID: `P2-8.2`
> Version: `v2026.09.15`

## 顺序与索引

列表是按顺序保存多个值的数据结构。通过索引（index），可以从分数、句子或文件名列表中取出特定值。

把四个分数 `82, 75, 91, 68` 放入方括号，并命名为 `scores`。代码会输出 `[82, 75, 91, 68]` 和类型 `<class 'list'>`。

```python
scores = [82, 75, 91, 68]

print(scores)
print(type(scores))
```

Python 列表中的每个值都可以称为项或元素。

列表的第一个索引是 `0`。代码依次输出索引 `0` 和 `1` 对应的值 `82`、`75`。

```python
scores = [82, 75, 91, 68]

print(scores[0])
print(scores[1])
```

负数索引从末尾计数。`-1` 表示最后一项。

| 表达式 | 含义 | 值 |
| --- | --- | --- |
| `scores[0]` | 第一项 | `82` |
| `scores[1]` | 第二项 | `75` |
| `scores[-1]` | 最后一项 | `68` |

## 越界索引与空列表

长度为 4 的列表，非负索引是 0 到 3。`scores[4]` 请求第五项，会引发 `IndexError`。切片的结束位置即使超过列表长度，也只返回可用部分。

| 表达式 | `scores = [82, 75, 91, 68]` 时的结果 |
| --- | --- |
| `scores[3]` | `68` |
| `scores[4]` | `IndexError` |
| `scores[2:10]` | `[91, 68]` |
| `scores[4:10]` | `[]` |

空列表的 `len([])` 和 `sum([])` 都是 0，但这不意味着平均值也是 0。`sum([]) / len([])` 会除以零，引发 `ZeroDivisionError`。计算平均值之前，应确认至少收集到一项数据。

## 列表与数组

学过其他语言的读者可能直接把列表理解为数组，因为两者都有顺序，也能通过索引取值。

Python 列表更接近按顺序保存多个值的通用容器。AI 数值计算中的数组通常指把同类数字按一定结构组织起来，以便高效计算的数据结构。

Python 文档把 `list` 定义为可变序列。标准库的 `array` 模块另行提供高效存放数值的数组。`array` 在某些方面与列表相似，但元素类型受创建时指定的类型代码约束。

遇到多维数组时，这种区别更容易混淆。Python 也能在列表中放入列表，形成类似表格的结构。

把 `[1, 2, 3]` 和 `[4, 5, 6]` 两行放入一个列表，就构成嵌套列表。代码输出整个结构，以及第二行第一个值 `4`。

```python
rows = [
    [1, 2, 3],
    [4, 5, 6],
]

print(rows)
print(rows[1][0])
```

这种形状看起来像矩阵或二维数组，但它仍然是列表中包含列表的结构。NumPy 的 `ndarray` 是具有 shape、axis、dtype 等信息的计算结构，文档将其称为 N 维数组。嵌套列表看起来像矩阵，并不意味着它就是数值计算用的多维数组。

| 方面 | Python 列表 | 数值计算中的数组 |
| --- | --- | --- |
| 核心想法 | 有顺序的值集合 | 结构化组织、用于计算的同类数值 |
| 主要用途 | 保存样本、文件名、文本等对象 | 对向量、矩阵、模型输入进行数值计算 |
| 值的类型 | 可以混合类型，通常按共同目的组织 | 通常要求相同数值类型 |
| 改变方式 | 容易添加或删除值 | 大小、轴和运算方式更重要 |

## 选择数据结构

Python 列表可理解为一种可变序列：保存有顺序的值，按需在末尾添加或取出项，并便于逐项处理。官方教程分别介绍列表方法、栈的用法、用作队列的局限，以及字典、集合和元组。

列表不能代替所有集合结构。应根据处理值的依据选择不同结构。

| 结构 | 核心问题 | 与列表的区别 |
| --- | --- | --- |
| 列表 | 按顺序保存并逐项处理多个值？ | 索引和顺序重要，可添加或修改元素 |
| 元组 | 保留固定的组合？ | 不可变序列，常用于固定组合 |
| 字典 | 通过名称或键查找值？ | 通过键而非位置访问 |
| 集合 | 需要去重和成员检查？ | 唯一性和成员检查比顺序更重要 |
| 双端队列 | 经常在两端添加或取出？ | 频繁从前端取出时，`collections.deque` 更合适 |
| 数组 | 对同类数值进行结构化计算？ | 数值类型、形状、轴和运算方式重要 |

## 修改元素与引用

列表是可变序列，可以添加或修改元素。

在分数末尾添加 `68`，并把第二个分数从 `75` 改为 `77`，结果为 `[82, 77, 91, 68]`。

```python
scores = [82, 75, 91]

scores.append(68)
scores[1] = 77

print(scores)
```

`append()` 在末尾添加值。`scores[1] = 77` 修改第二项。

`other_scores = scores` 为同一列表增加一个名称，并不复制列表。通过 `other_scores` 添加 `68` 后，两次输出都是 `[82, 75, 91, 68]`。

```python
scores = [82, 75, 91]
other_scores = scores

other_scores.append(68)

print(scores)
print(other_scores)
```

`scores` 和 `other_scores` 指向同一个列表，并非两个副本。通过一方添加值，另一方也能看到相同变化。

## 修改方法的返回值

`append()` 修改原列表并返回 `None`。代码输出 `[82, 75, 91]` 和 `None`。

```python
scores = [82, 75]
result = scores.append(91)
print(scores)
print(result)
```

`result` 不是修改后的列表。如果写成 `scores = scores.append(91)`，虽然原列表添加了值，但名称 `scores` 随后会指向返回值 `None`。要继续使用列表，只调用 `scores.append(91)` 即可。

## 连接、切片与删除

阅读 Python 列表代码时，经常先遇到符号和方括号语法，而非函数名。其他语言中的 `concat`、`join`、`slice`、`splice` 等操作，在 Python 中可能由运算符、切片、赋值或 `del` 语句表达。

### 连接

用 `+` 可将两个列表连接成新列表。要在现有列表末尾继续添加多个值，可以使用 `extend()`。

`[1, 2] + [3, 4]` 创建新列表 `[1, 2, 3, 4]`，而 `front` 保持 `[1, 2]`。`extend()` 则把原有 `scores` 改为 `[82, 75, 91, 68]`。

```python
front = [1, 2]
back = [3, 4]

combined = front + back
print("combined:", combined)
print("front after +:", front)

scores = [82, 75]

scores.extend([91, 68])
print("scores after extend:", scores)
```

`+` 新建连接结果，`extend()` 修改原列表。

### 切片

切片用于从列表中取出一段元素。

从五个分数中分别取出中间一段、前两项和后面一段，依次输出 `[75, 91, 68]`、`[82, 75]`、`[68, 88]`。

```python
scores = [82, 75, 91, 68, 88]

print(scores[1:4])
print(scores[:2])
print(scores[3:])
```

`scores[1:4]` 从索引 1 取到索引 4 之前，结果为 `[75, 91, 68]`，不包含索引 4 的值 `88`。

列表切片会创建一个包含所选元素的新列表。

### 删除与替换区间

Python 列表没有单独的 `splice()` 方法来删除或替换中间区间。类似操作由 `del`、`insert()` 或切片赋值实现。

从 `["A", "B", "C", "D"]` 中删除索引 1 到索引 3 之前的元素，会输出 `['A', 'D']`。

```python
items = ["A", "B", "C", "D"]

del items[1:3]

print(items)
```

`del items[1:3]` 删除索引 1 到 3 之前的区间，结果是 `["A", "D"]`。

把中间两项 `"B"`、`"C"` 替换为三项 `"X"`、`"Y"`、`"Z"`。结果为 `['A', 'X', 'Y', 'Z', 'D']`，长度从 4 增加到 5。

```python
items = ["A", "B", "C", "D"]

items[1:3] = ["X", "Y", "Z"]

print(items)
```

### 字符串连接：join

`join` 在 Python 中很常见，但它不是列表方法，而是字符串方法，用于把一组字符串连接成一个字符串。

用空格连接 `["AI", "needs", "data"]` 会输出 `AI needs data`。`" ".join(words)` 中的空格字符串就是分隔符。

```python
words = ["AI", "needs", "data"]

sentence = " ".join(words)

print(sentence)
```

结果是 `"AI needs data"`。操作主体是字符串 `" "`，不是列表；它把 `words` 中的字符串用空格连接起来。

| 目的 | 常见 Python 写法 | 注意事项 |
| --- | --- | --- |
| 连接两个列表 | `front + back` | 创建新列表 |
| 扩展已有列表 | `items.extend(values)` | 修改原列表 |
| 读取区间 | `items[1:4]` | 不包含结束索引 |
| 删除区间 | `del items[1:4]` | 修改原列表 |
| 替换区间 | `items[1:4] = values` | 替换前后长度可不同 |
| 把字符串列表合为一个字符串 | `" ".join(words)` | `join()` 是字符串方法 |

## 初始化列表

初始化是首次创建数据结构。根据值已准备好还是稍后收集，选择开始时的形式。

### 已经知道值时

已知的值可直接写入方括号。代码分别按输入顺序输出分数、标签和布尔值列表。

```python
scores = [82, 75, 91, 68]
labels = ["positive", "negative", "neutral"]
flags = [True, False, True]

print(scores)
print(labels)
print(flags)
```

这种方式能直接展示教学示例或小型配置列表的值组成。

### 从空列表开始

向空列表 `[]` 依次添加 `82`、`75`，会输出 `[82, 75]`。每得到一个待收集的值，就调用一次 `append()`。

```python
passed_scores = []

passed_scores.append(82)
passed_scores.append(75)

print(passed_scores)
```

列表创建后仍可添加元素。实际数据处理中，经常通过循环把符合条件的值收集到空列表中。

### 用相同值填充指定长度

`[0] * 5` 将初始值 `0` 重复五次，输出 `[0, 0, 0, 0, 0]`。

```python
predictions = [0] * 5

print(predictions)
```

这会创建 `[0, 0, 0, 0, 0]`。对于数字、字符串等简单值很直观，但嵌套列表需要注意。

`[[]] * 3` 的三个位置引用同一个内部空列表。通过第一个位置添加 `"A"`，会输出 `[['A'], ['A'], ['A']]`。

```python
rows = [[]] * 3

rows[0].append("A")

print(rows)
```

要独立修改各行，需要分别创建内部列表。改为 `rows = [[], [], []]` 后，结果是 `[['A'], [], []]`，只有第一行改变。

## 分数、句子与文件列表

当多个值具有共同目的或上下文，且位置、顺序有意义时，可以使用列表。

### 多个分数

`[82, 75, 91, 68]` 的最大值为 `91`、最小值为 `68`、平均值为 `79.0`。`sum()` 求和，`len()` 求项数，两者相除得到平均值。

```python
scores = [82, 75, 91, 68]

print(max(scores))
print(min(scores))
print(sum(scores) / len(scores))
```

### 多个句子

`for` 按顺序取出列表中的三个句子，`text` 依次指向各句子，每个句子单独输出一行。

```python
texts = [
    "AI is useful.",
    "Data quality matters.",
    "Models can fail.",
]

for text in texts:
    print(text)
```

LLM 和文本分类练习中经常使用句子列表。

### 多个模型输出

把模型分数 `[0.92, 0.31, 0.77, 0.12]` 与阈值 `0.8` 比较。只有第一个值通过，因此输出一次 `above threshold` 和三次 `check`。

```python
probabilities = [0.92, 0.31, 0.77, 0.12]

for probability in probabilities:
    if probability >= 0.8:
        print("above threshold")
    else:
        print("check")
```

把阈值改为 `0.7`，第三个值 `0.77` 也会通过，于是输出两次 `above threshold`。通过指定阈值并不保证预测正确。

### 多个文件名

代码依次取出并输出 `train.csv`、`valid.csv`、`test.csv` 三个文件名，并不读取文件内容。

```python
file_names = [
    "train.csv",
    "valid.csv",
    "test.csv",
]

for file_name in file_names:
    print(file_name)
```

## 案例：检查第三个预测分数

假设按输入顺序保存预测分数 `[0.92, 0.31, 0.77, 0.12]`。第三个输入对应索引 `2` 的分数 `0.77`。在末尾添加新分数 `0.85` 后，原有位置不变，项数增至 `5`。

```python
probabilities = [0.92, 0.31, 0.77, 0.12]
print(probabilities[2])

probabilities.append(0.85)
print(probabilities)
print(len(probabilities))
```

输出依次为 `0.77`、`[0.92, 0.31, 0.77, 0.12, 0.85]`、`5`。若输入与预测按位置对应，不应只改变其中一方的顺序。仅对分数排序后，第三个位置可能不再代表第三个输入。

## 检查清单

- 能将列表解释为有顺序的值集合。
- 能解释 `scores[0]` 和 `scores[-1]`。
- 能区分已知值、空列表和重复值的初始化方式。
- 能读懂 `append()` 添加元素的过程。
- 能大致区分 `+`、`extend()`、切片、`del` 和切片赋值。
- 能解释 `join()` 是字符串方法而非列表方法。
- 能说明 Python 列表没有 JavaScript 式 `splice()`，类似操作使用 `del`、`insert()` 和切片赋值。
- 能解释多个名称可以引用同一个列表。
- 能说明重复创建嵌套列表时需要注意的问题。

- 能解释索引越界与切片的差别、空列表的平均值错误，以及 `append()` 的返回值。

## 来源与参考资料


- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。用于确认列表方法、把列表当作 stack 使用的例子、列表推导式与嵌套列表示例。
- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-09-15。用于确认序列类型、mutable sequence 操作、索引与切片行为。
- Python Software Foundation, [array — Efficient arrays of numeric values](https://docs.python.org/3/library/array.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation，确认日期：2026-07-20。用于确认标准库 `array` 会高效存储相同基本类型的值。
- NumPy Developers, [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html){: target="_blank" rel="noopener noreferrer" }, NumPy Manual，确认日期：2026-07-20。用于确认 NumPy 数组不同于普通 Python 列表，是高效处理大量数值数据的核心结构。
